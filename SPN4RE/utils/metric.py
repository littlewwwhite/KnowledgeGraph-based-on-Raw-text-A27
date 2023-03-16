def metric(pred, gold):
    assert pred.keys() == gold.keys()
    gold_num = 0
    rel_num = 0
    ent_num = 0
    right_num = 0
    pred_num = 0
    for sent_idx in pred:
        gold_num += len(gold[sent_idx])
        pred_correct_num = 0
        prediction = list(set([(ele.pred_rel, ele.head_start_index, ele.head_end_index, ele.tail_start_index, ele.tail_end_index) for ele in pred[sent_idx]]))
        pred_num += len(prediction)
        for ele in prediction:
            if ele in gold[sent_idx]:
                right_num += 1
                pred_correct_num += 1
            if ele[0] in [e[0] for e in gold[sent_idx]]:
                rel_num += 1
            if ele[1:] in [e[1:] for e in gold[sent_idx]]:
                ent_num += 1
        # if pred_correct_num != len(gold[sent_idx]):
        #     print("Gold: ", gold[sent_idx])
        #     print("Pred: ", prediction)
        #     print(pred[sent_idx])
    if pred_num == 0:
        precision = -1
        r_p = -1
        e_p = -1
    else:
        precision = (right_num + 0.0) / pred_num
        e_p = (ent_num + 0.0) / pred_num
        r_p = (rel_num + 0.0) / pred_num

    if gold_num == 0:
        recall = -1
        r_r = -1
        e_r = -1
    else:
        recall = (right_num + 0.0) / gold_num
        e_r = ent_num / gold_num
        r_r = rel_num / gold_num

    if (precision == -1) or (recall == -1) or (precision + recall) <= 0.:
        f_measure = -1
    else:
        f_measure = 2 * precision * recall / (precision + recall)

    if (e_p == -1) or (e_r == -1) or (e_p + e_r) <= 0.:
        e_f = -1
    else:
        e_f = 2 * e_r * e_p / (e_p + e_r)

    if (r_p == -1) or (r_r == -1) or (r_p + r_r) <= 0.:
        r_f = -1
    else:
        r_f = 2 * r_p * r_r / (r_r + r_p)
    print("gold_num = ", gold_num, " pred_num = ", pred_num, " right_num = ", right_num, " relation_right_num = ", rel_num, " entity_right_num = ", ent_num)
    print("precision = ", precision, " recall = ", recall, " f1_value = ", f_measure)
    print("rel_precision = ", r_p, " rel_recall = ", r_r, " rel_f1_value = ", r_f)
    print("ent_precision = ", e_p, " ent_recall = ", e_r, " ent_f1_value = ", e_f)
    return {"precision": precision, "recall": recall, "f1": f_measure}


def num_metric(pred, gold):
    test_1, test_2, test_3, test_4, test_other = [], [], [], [], []
    for sent_idx in gold:
        if len(gold[sent_idx]) == 1:
            test_1.append(sent_idx)
        elif len(gold[sent_idx]) == 2:
            test_2.append(sent_idx)
        elif len(gold[sent_idx]) == 3:
            test_3.append(sent_idx)
        elif len(gold[sent_idx]) == 4:
            test_4.append(sent_idx)
        else:
            test_other.append(sent_idx)

    pred_1 = get_key_val(pred, test_1)
    gold_1 = get_key_val(gold, test_1)
    pred_2 = get_key_val(pred, test_2)
    gold_2 = get_key_val(gold, test_2)
    pred_3 = get_key_val(pred, test_3)
    gold_3 = get_key_val(gold, test_3)
    pred_4 = get_key_val(pred, test_4)
    gold_4 = get_key_val(gold, test_4)
    pred_other = get_key_val(pred, test_other)
    gold_other = get_key_val(gold, test_other)
    # pred_other = dict((key, vals) for key, vals in pred.items() if key in test_other)
    # gold_other = dict((key, vals) for key, vals in gold.items() if key in test_other)
    print("--*--*--Num of Gold Triplet is 1--*--*--")
    _ = metric(pred_1, gold_1)
    print("--*--*--Num of Gold Triplet is 2--*--*--")
    _ = metric(pred_2, gold_2)
    print("--*--*--Num of Gold Triplet is 3--*--*--")
    _ = metric(pred_3, gold_3)
    print("--*--*--Num of Gold Triplet is 4--*--*--")
    _ = metric(pred_4, gold_4)
    print("--*--*--Num of Gold Triplet is greater than or equal to 5--*--*--")
    _ = metric(pred_other, gold_other)


def overlap_metric(pred, gold):
    normal_idx, multi_label_idx, overlap_idx = [], [], []
    for sent_idx in gold:
        triplets = gold[sent_idx]
        if is_normal_triplet(triplets):
            normal_idx.append(sent_idx)
        if is_multi_label(triplets):
            multi_label_idx.append(sent_idx)
        if is_overlapping(triplets):
            overlap_idx.append(sent_idx)
    pred_normal = get_key_val(pred, normal_idx)
    gold_normal = get_key_val(gold, normal_idx)
    pred_multilabel = get_key_val(pred, multi_label_idx)
    gold_multilabel = get_key_val(gold, multi_label_idx)
    pred_overlap = get_key_val(pred, overlap_idx)
    gold_overlap = get_key_val(gold, overlap_idx)
    print("--*--*--Normal Triplets--*--*--")
    _ = metric(pred_normal, gold_normal)
    print("--*--*--Multiply label Triplets--*--*--")
    _ = metric(pred_multilabel, gold_multilabel)
    print("--*--*--Overlapping Triplets--*--*--")
    _ = metric(pred_overlap, gold_overlap)



def is_normal_triplet(triplets):
    entities = set()
    for triplet in triplets:
        head_entity = (triplet[1], triplet[2])
        tail_entity = (triplet[3], triplet[4])
        entities.add(head_entity)
        entities.add(tail_entity)
    return len(entities) == 2 * len(triplets)


def is_multi_label(triplets):
    if is_normal_triplet(triplets):
        return False
    entity_pair = [(triplet[1], triplet[2], triplet[3], triplet[4]) for triplet in triplets]
    return len(entity_pair) != len(set(entity_pair))


def is_overlapping(triplets):
    if is_normal_triplet(triplets):
        return False
    entity_pair = [(triplet[1], triplet[2], triplet[3], triplet[4]) for triplet in triplets]
    entity_pair = set(entity_pair)
    entities = []
    for pair in entity_pair:
        entities.append((pair[0], pair[1]))
        entities.append((pair[2], pair[3]))
    entities = set(entities)
    return len(entities) != 2 * len(entity_pair)


def get_key_val(dict_1, list_1):
    dict_2 = dict()
    for ele in list_1:
        dict_2.update({ele: dict_1[ele]})
    return dict_2
