import os, json
from prepare.schema import schema_v2

os.environ["CUDA_VISIBLE_DEVICES"] = '3'
import paddle.inference as paddle_infer
from paddlenlp import Taskflow

# 定义一个函数，用于关系抽取
def paddle_relation_ie(content):
    relation_ie = Taskflow("information_extraction", schema=schema_v2.schema, batch_size=1)
    return relation_ie(content)

# 定义一个函数，用于初始化GPU
def gpu_init(gpu_id, gpu_mem, ):
    config = paddle_infer.Config("./mobilenet.pdmodel", "./mobilenet.pdiparams")
    config.enable_use_gpu(gpu_mem, gpu_id)
    print("Use GPU is: {}".format(config.use_gpu())) # True
    print("Init mem size is: {}".format(config.memory_pool_init_size_mb())) # 100
    print("Init mem frac is: {}".format(config.fraction_of_gpu_memory_for_pool())) # 0.003
    print("GPU device id is: {}".format(config.gpu_device_id())) # 0

# def read_txt_file(path):
#     with open(path, 'r') as f:
#         while True:
#             line = f.readline()
#             if not line:
#                 break
#             yield line.strip()

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

# # 将实体和关系信息写入json文件
# def write_json(all_relations, write_dir, content, sent_id):
#     dict= {}
#     dict["id"] = sent_id
#     dict["sentText"] = content
#     dict["relationMentions"] = all_relations
#     with open(write_dir + ".json", "a", encoding="utf-8") as f:
#         json.dump(dict, f, ensure_ascii=False, separators=(',', ':'))
#         f.write('\n')

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

#
# def main():
#     gpu_init(0, 20000)
#     version = 'res_base_v2'
#     data_dir = '/data_F/zhijian/paddlenlp/data/'
#     txt_path = os.path.join(data_dir, 'raw_data/raw_data_lines.txt')
#     write_dir = os.path.join(data_dir, 'res_data/', version)
#     uie_execute(txt_path, write_dir)
#
#
# if __name__ == '__main__':
#     main()
