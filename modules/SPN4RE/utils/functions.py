import torch, collections


def list_index(list1: list, list2: list) -> list:

    index = None
    try:
        start = [i for i, x in enumerate(list2) if x == list1[0]]
        end = [i for i, x in enumerate(list2) if x == list1[-1]]
        if len(start) == 1 and len(end) == 1:
            index = (start[0], end[0])
        else:
            for i in start:
                for j in end:
                    if i <= j:
                        if list2[i:j+1] == list1:
                            index = (i, j)
                            break

    except:
        print(f"can not index `{list1}` in `{list2}`.")

    assert index, f"can not index `{list1}` in `{list2}`."
    return index[0], index[1]





# def list_index(list1: list, list2: list) -> list:
#     start = [i for i, x in enumerate(list2) if x == list1[0]]
#     end = [i for i, x in enumerate(list2) if x == list1[-1]]
#     if len(start) == 1 and len(end) == 1:
#         return start[0], end[0]
#     else:
#         for i in start:
#             for j in end:
#                 if i <= j:
#                     if list2[i:j+1] == list1:
#                         break
#         return i, j
#

def remove_accents(text: str) -> str:
    accents_translation_table = str.maketrans(
    "áéíóúýàèìòùỳâêîôûŷäëïöüÿñÁÉÍÓÚÝÀÈÌÒÙỲÂÊÎÔÛŶÄËÏÖÜŸ",
    "aeiouyaeiouyaeiouyaeiouynAEIOUYAEIOUYAEIOUYAEIOUY"
    )
    return text.translate(accents_translation_table)


def data_process(input_doc, relational_alphabet, tokenizer):
    samples = []
    with open(input_doc) as f:
        lines = f.readlines()
        lines = [eval(ele) for ele in lines]
    for i in range(len(lines)):
        token_sent = [tokenizer.cls_token] + tokenizer.tokenize(remove_accents(lines[i]["sentText"])) + [tokenizer.sep_token]
        triples = lines[i]["relationMentions"]
        target = {"relation": [], "head_start_index": [], "head_end_index": [], "tail_start_index": [], "tail_end_index": []}
        for triple in triples:
            head_entity = remove_accents(triple["em1Text"])
            tail_entity = remove_accents(triple["em2Text"])
            head_token = tokenizer.tokenize(head_entity)
            tail_token = tokenizer.tokenize(tail_entity)
            relation_id = relational_alphabet.get_index(triple["label"])
            head_start_index, head_end_index = list_index(head_token, token_sent)
            assert head_end_index >= head_start_index
            tail_start_index, tail_end_index = list_index(tail_token, token_sent)
            assert tail_end_index >= tail_start_index
            target["relation"].append(relation_id)
            target["head_start_index"].append(head_start_index)
            target["head_end_index"].append(head_end_index)
            target["tail_start_index"].append(tail_start_index)
            target["tail_end_index"].append(tail_end_index)
        sent_id = tokenizer.convert_tokens_to_ids(token_sent)
        samples.append([i, sent_id, target])
    return samples


def _get_best_indexes(logits, n_best_size):
    """Get the n-best logits from a list."""
    index_and_score = sorted(enumerate(logits), key=lambda x: x[1], reverse=True)
    best_indexes = []
    for i in range(len(index_and_score)):
        if i >= n_best_size:
            break
        best_indexes.append(index_and_score[i][0])
    return best_indexes


def generate_span(start_logits, end_logits, info, args):
    seq_lens = info["seq_len"] # including [CLS] and [SEP]
    sent_idxes = info["sent_idx"]
    _Prediction = collections.namedtuple(
        "Prediction", ["start_index", "end_index", "start_prob", "end_prob"]
    )
    output = {}
    start_probs = start_logits.softmax(-1)
    end_probs = end_logits.softmax(-1)
    start_probs = start_probs.cpu().tolist()
    end_probs = end_probs.cpu().tolist()
    for (start_prob, end_prob, seq_len, sent_idx) in zip(start_probs, end_probs, seq_lens, sent_idxes):
        output[sent_idx] = {}
        for triple_id in range(args.num_generated_triples):
            predictions = []
            start_indexes = _get_best_indexes(start_prob[triple_id], args.n_best_size)
            end_indexes = _get_best_indexes(end_prob[triple_id], args.n_best_size)
            for start_index in start_indexes:
                for end_index in end_indexes:
                    # We could hypothetically create invalid predictions, e.g., predict
                    # that the start of the span is in the sentence. We throw out all
                    # invalid predictions.
                    if start_index >= (seq_len-1): # [SEP]
                        continue
                    if end_index >= (seq_len-1):
                        continue
                    if end_index < start_index:
                        continue
                    length = end_index - start_index + 1
                    if length > args.max_span_length:
                        continue
                    predictions.append(
                        _Prediction(
                            start_index=start_index,
                            end_index=end_index,
                            start_prob=start_prob[triple_id][start_index],
                            end_prob=end_prob[triple_id][end_index],
                        )
                    )
            output[sent_idx][triple_id] = predictions
    return output


def generate_relation(pred_rel_logits, info, args):
    rel_probs, pred_rels = torch.max(pred_rel_logits.softmax(-1), dim=2)
    rel_probs = rel_probs.cpu().tolist()
    pred_rels = pred_rels.cpu().tolist()
    sent_idxes = info["sent_idx"]
    output = {}
    _Prediction = collections.namedtuple(
        "Prediction", ["pred_rel", "rel_prob"]
    )
    for (rel_prob, pred_rel, sent_idx) in zip(rel_probs, pred_rels, sent_idxes):
        output[sent_idx] = {}
        for triple_id in range(args.num_generated_triples):
            output[sent_idx][triple_id] = _Prediction(
                            pred_rel=pred_rel[triple_id],
                            rel_prob=rel_prob[triple_id])
    return output


def generate_triple(output, info, args, num_classes):
    _Pred_Triple = collections.namedtuple(
        "Pred_Triple", ["pred_rel", "rel_prob", "head_start_index", "head_end_index", "head_start_prob", "head_end_prob", "tail_start_index", "tail_end_index", "tail_start_prob", "tail_end_prob"]
    )
    pred_head_ent_dict = generate_span(output["head_start_logits"], output["head_end_logits"], info, args)
    pred_tail_ent_dict = generate_span(output["tail_start_logits"], output["tail_end_logits"], info, args)
    pred_rel_dict = generate_relation(output['pred_rel_logits'], info, args)
    triples = {}
    for sent_idx in pred_rel_dict:
        triples[sent_idx] = []
        for triple_id in range(args.num_generated_triples):
            pred_rel = pred_rel_dict[sent_idx][triple_id]
            pred_head = pred_head_ent_dict[sent_idx][triple_id]
            pred_tail = pred_tail_ent_dict[sent_idx][triple_id]
            triple = generate_strategy(pred_rel, pred_head, pred_tail, num_classes, _Pred_Triple)
            if triple:
                triples[sent_idx].append(triple)
    # print(triples)
    return triples


def generate_strategy(pred_rel, pred_head, pred_tail, num_classes, _Pred_Triple):
    if pred_rel.pred_rel != num_classes:
        if pred_head and pred_tail:
            for ele in pred_head:
                if ele.start_index != 0:
                    break
            head = ele
            for ele in pred_tail:
                if ele.start_index != 0:
                    break
            tail = ele
            return _Pred_Triple(pred_rel=pred_rel.pred_rel, rel_prob=pred_rel.rel_prob, head_start_index=head.start_index, head_end_index=head.end_index, head_start_prob=head.start_prob, head_end_prob=head.end_prob, tail_start_index=tail.start_index, tail_end_index=tail.end_index, tail_start_prob=tail.start_prob, tail_end_prob=tail.end_prob)
        else:
            return
    else:
        return


# def strict_strategy(pred_rel, pred_head, pred_tail, num_classes, _Pred_Triple):
#     if pred_rel.pred_rel != num_classes:
#         if pred_head and pred_tail:
#             if pred_head[0].start_index != 0 and pred_tail[0].start_index != 0:
#                 return _Pred_Triple(pred_rel=pred_rel.pred_rel, rel_prob=pred_rel.rel_prob, head_start_index=pred_head[0].start_index, head_end_index=pred_head[0].end_index, head_start_prob=pred_head[0].start_prob, head_end_prob=pred_head[0].end_prob, tail_start_index=pred_tail[0].start_index, tail_end_index=pred_tail[0].end_index, tail_start_prob=pred_tail[0].start_prob, tail_end_prob=pred_tail[0].end_prob)
#             else:
#                 return
#         else:
#             return
#     else:
#         return


def formulate_gold(target, info):
    sent_idxes = info["sent_idx"]
    gold = {}
    for i in range(len(sent_idxes)):
        gold[sent_idxes[i]] = []
        for j in range(len(target[i]["relation"])):
            gold[sent_idxes[i]].append(
                (target[i]["relation"][j].item(), target[i]["head_start_index"][j].item(), target[i]["head_end_index"][j].item(), target[i]["tail_start_index"][j].item(), target[i]["tail_end_index"][j].item())
            )
    return gold


