import os
from data.schema import schema_v2

os.environ["CUDA_VISIBLE_DEVICES"] = '1'
from paddle import inference as paddle_infer
from paddlenlp import Taskflow

# 定义一个函数，用于关系抽取
def paddle_relation_ie(content):
    relation_ie = Taskflow("information_extraction", schema=schema_v2.schema, batch_size=1)
    return relation_ie(content)


# 关系抽取并修改json文件
def rel_json(content):
    all_relations = [] # 定义一个空列表，用于存储每个chapter的关系信息
    res_relation = paddle_relation_ie(content)  # 传入文本进行关系识别
    for rel in res_relation:
        for sub_type, sub_rel in rel.items():
            for sub in sub_rel:
                if sub.get("relations") is None:
                    continue
                for rel_type, rel_obj in sub["relations"].items():
                    for obj in rel_obj:
                        if not sub['text'] or not obj['text']:
                            continue
                        rel_triple = {"em1Text": sub['text'],"em2Text": obj['text'],"label": rel_type}
                        all_relations.append(rel_triple)
    return all_relations


# 执行函数
def uie_execute(texts):

    sent_id = 0
    all_items = []
    for line in texts:
        line = line.strip()
        all_relations = rel_json(line)

        item = {}
        item["id"] = sent_id
        item["sentText"] = line
        item["relationMentions"] = all_relations

        sent_id += 1
        if sent_id % 10 == 0 and sent_id != 0:
            print("Done {} lines".format(sent_id))

        all_items.append(item)

    return all_items
