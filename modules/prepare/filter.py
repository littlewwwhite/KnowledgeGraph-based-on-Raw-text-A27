from transformers import AutoTokenizer


def auto_filter(items, model_name_or_path):
    """用于自动过滤到一些错误的三元组，比如经过 bertTokenizer 之后，实体不在句子中了

    Args:
        items (数组): 所有的实例，每个实例是一个字典，包含了句子、实体、关系
        model_name_or_path (字符串): 预训练模型的名字或者路径

    Returns:
        过滤后的 items
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

    for example in items:

        sent_tokens = tokenizer.tokenize(example["sentText"])

        relations = []
        for relation in example["relationMentions"]:
            sub_tokens = tokenizer.tokenize(relation["em1Text"])
            obj_tokens = tokenizer.tokenize(relation["em2Text"])

            if len(sub_tokens) == 0 or len(obj_tokens) == 0:
                continue

            if len(sub_tokens) > 15 or len(obj_tokens) > 15:
                continue

            # 1. 判断 subject 是否在句子中，长短数组匹配问题
            sub_start = -1
            sub_end = -1
            for i in range(len(sent_tokens) - len(sub_tokens) + 1):
                if sent_tokens[i:i+len(sub_tokens)] == sub_tokens:
                    sub_start = i
                    sub_end = i + len(sub_tokens) - 1
                    break

            # 2. 判断 object 是否在句子中，长短数组匹配问题
            obj_start = -1
            obj_end = -1
            for i in range(len(sent_tokens) - len(obj_tokens) + 1):
                if sent_tokens[i:i+len(obj_tokens)] == obj_tokens:
                    obj_start = i
                    obj_end = i + len(obj_tokens) - 1
                    break

            # 3. 判断 subject 和 object 是否在句子中，长短数组匹配问题
            if sub_start == -1:
                print("subject not in sentText")
                print("subject", sub_tokens)
                # print("sentText", sent_tokens)
                continue

            if obj_start == -1:
                print("object not in sentText")
                print("object", obj_tokens)
                # print("sentText", sent_tokens)
                continue

            relations.append({
                "em1Text": relation["em1Text"],
                "em2Text": relation["em2Text"],
                "label": relation["label"],
                "em1Start": sub_start, # 以作备用吧
                "em1End": sub_end,
                "em2Start": obj_start,
                "em2End": obj_end
            })

        example["relationMentions"] = relations # 覆盖原来的 relations

    return items