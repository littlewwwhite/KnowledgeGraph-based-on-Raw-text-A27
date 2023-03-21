import os
import json
import random
import subprocess
from prepare.utils import refine_knowledge_graph



class ModelTrainer:

    def __init__(self, data_path, output_dir, model_name_or_path) -> None:
        """ 用来训练 SPN 的一个类

        Args:
            data_path: 用于训练的所有数据，没有切分训练、测试、验证
            output_dir: 保存测试之后的数据的文件夹

        """
        self.data_path = data_path
        self.generated_data_directory = output_dir
        self.model_name_or_path = model_name_or_path

        os.makedirs(output_dir, exist_ok=True)
        self.train_file = os.path.join(output_dir, "train.json")
        self.valid_file = os.path.join(output_dir, "valid.json")
        self.test_file = os.path.join(output_dir, "test.json")

        self.prediction = os.path.join(output_dir, 'prediction.json') # 或者 .pickle
        self.test_result_format = os.path.join(output_dir, 'test_result_format.json')# 保存了测试结果的文件
        self.test_result_refine = os.path.join(output_dir, 'test_result_refine.json')

        # 这个是保存了关系的 id 与类别的映射表的文件alphabet.json
        self.data_instance_path = os.path.join(output_dir, 'alphabet.json')
        self.final_knowledge_graph = os.path.join(output_dir, 'knowledge_graph.json}')

        self.split_data()
        self.params = self.generate_running_cmd()

    def generate_running_cmd(self):
        params = "python SPN4RE/main.py"
        params += f" --bert_directory {self.model_name_or_path}"
        params += " --max_epoch 20"
        params += " --max_span_length 10"
        params += " --num_generated_triples 15"
        params += " --max_grad_norm 2.5"
        params += " --na_rel_coef 0.25"
        params += f" --train_file {self.train_file}"
        params += f" --valid_file {self.valid_file}"
        params += f" --test_file {self.test_file}"
        params += f" --generated_data_directory {self.generated_data_directory}"
        return params

    def save_data(self, data, trg_path):
        """
        根据不同的数据类型将数据保存数据到指定的文件
        """
        if trg_path.endswith(".json"):
            with open(trg_path, 'w') as f:
                for line in data:
                    json_line = json.dumps(line, ensure_ascii=False)
                    f.write(json_line + "\n")
        elif trg_path.endswith(".txt"):
            with open(trg_path, 'w') as f:
                for line in data:
                    f.write(line + "\n")
        else:
            raise ValueError("不支持的文件格式")
        print(f"数据保存到 {trg_path} 成功")

    def split_data(self):
        """将知识图谱数据(SPN_style)切分为三个文件"""

        with open(self.data_path, 'r') as f:
            lines = [json.loads(line) for line in f.readlines()]
            lines = random.shuffle(lines)

        # dataset_length = len(lines)
        # 按照 4:1:5 的比例切分数据集，并分别保存到三个路径里面

        train_lines = lines[:int(len(lines) * 0.4)]
        valid_lines = lines[int(len(lines) * 0.4):int(len(lines) * 0.5)]
        test_lines = lines[int(len(lines) * 0.5):]
        self.save_data(train_lines, self.train_file)
        self.save_data(valid_lines, self.valid_file)
        self.save_data(test_lines, self.test_file)

    def train_and_test(self):
        """训练并测试这个模型，测试的预测结果会保存到 self.prediction 这个文件里面。"""

        # TODO work_dir 存在问题
        print(f"Running: $ {self.params}")

        log_file = os.path.join(self.output_dir, "running_log.txt")
        os.system(f"{self.params} > {log_file}")

        print("Done")

    def relation_align(self):
        """

        读取预测的结果，并将结果跟 test_file 中的三元组对应上
        将预测的结果跟训练集对齐，转化为 SPN style 的文件，注意，此时先不跟上个版本的合并
        将预测得到的结果跟测试集对齐后去除重复的三元组，保存到 knowledge_graph.json 文件中

        """

        # 读取50%的测试集
        with open(self.test_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # test_lines存放的是测试集的每一行
        test_lines = []
        for line in lines:
            test_line = json.loads(line)
            test_lines.append(test_line)

        # 读取SPN的预测结果
        with open(self.prediction, 'r', encoding='utf-8') as file:
            prediction = json.load(file)

        """
        test_line[9]["relationMentioned"] = func1(asdasd)
        prediction: ["pred_rel", "rel_prob", "head_start_index", "head_end_index", "head_start_prob", "head_end_prob", "tail_start_index", "tail_end_index", "tail_start_prob", "tail_end_prob"]
        """

        # 将预测结果转化为SPN训练时的style，返回数组
        test_pred_lines = {} # 保存prediction里面需要的部分
        for key, values in prediction.items():
            pred_relation = []
            for value in values:
                pred_rel = value[0]
                head_start_index = value[2]
                head_end_index = value[3]
                tail_start_index = value[6]
                tail_end_index = value[7]
                pred_relation.append([pred_rel, head_start_index, head_end_index, tail_start_index, tail_end_index])
            test_pred_lines.update({key: pred_relation})

        assert len(test_lines) == len(prediction)

        with open(self.data_instance_path, 'r') as f:
            id2rel = json.load(f)["instances"]

        # 将预测结果与测试集对齐
        pred_lines = []  # 保存SPN style的预测结果
        for test_line, pred in zip(test_lines, list(test_pred_lines.values())):

            triples = []
            pred_line = {}
            # eg. pred = [[4, 55, 55, 55, 55], [0, 55, 55, 55, 55]]
            for triple_pred in pred:

                triple = {"em1Text": test_line["sentText"][triple_pred[1]:triple_pred[2]],
                          "em2Text": test_line["sentText"][triple_pred[3]:triple_pred[4]],
                          "label": id2rel[triple_pred[0]]}  # 保存单个三元组

                # 实体从test_line的句子中截取
                # 关系从alphabet中获取
                triples.append(triple)

            pred_line["id"] = test_line["id"]
            pred_line["relationMentions"] = triples
            # eg. pred_lines = [{"id": 0, "relationMentions": [{"em1Text": "美国", "em2Text": "中国", "label": "国籍}]}]
            pred_lines.append(pred_line)

        # 去除origin_lines里面跟pred_lines重复的relationMentions项
        # eg. origin_lines = [{"id": 0,"sentText":"xxxxxx", "relationMentions": [{"em1Text": "美国", "em2Text": "中国", "label": "国籍}]}]
        with open(self.data_path, 'r') as f:
            origin_lines = [json.loads(l) for l in f.readlines()]

        # diff_lines = []
        # for pred_line in pred_lines:
        #     # 获取 pred_line 中的 relationMentions 字典
        #     # pred_relation_mentions = [pred_lines["id"],pred_lines["relationMentions"]]
        #     # 获取 origin_lines 中的 relationMentions 字典
        #     diff_line = {}
        #     for origin_line in origin_lines:
        #         if origin_line["id"] == pred_line["id"]:
        #             diff_line["id"] = origin_line["id"]
        #             # diff_line["relationMentions"] = [pred_line["relationMentions"] for "relationMentions" in pred_line.keys() if "relationMentions" not in origin_line or origin_line["relationMentions"] != pred_line["relationMentions"]]
        #             diff_line["relationMentions"] = set(pred_line["relationMentions"]) - set(origin_line["relationMentions"])

        #     # 保存 diff_line 到 diff_lines 里面
        #     diff_lines.append(diff_line)

        diff_lines = []
        for pred_line in lines:
            origin_line = origin_lines[origin_line["id"]]
            assert origin_line["id"] == pred_line["id"]

            diff_line = pred_line.copy()

            diff_rels = []
            for rel in pred_line["relationMentions"]:
                if rel not in origin_line["relationMentions"]:
                    diff_rels.append(rel)

            diff_line["relationMentions"] = diff_rels

            # 保存 diff_line 到 diff_lines 里面
            diff_lines.append(diff_line)

        # 将 test_lines 保存到文件里面
        self.save_data(diff_lines, self.test_result_format)

        # """save_data(test_pred_lines, test_result_format) """
        # self.save_data(test_pred_lines, self.test_result_format)  # 保存到文件里面


    def refine_and_extend(self):
        """将生成的 test_result_format 重新经过一遍人工清洗"""
        refine_knowledge_graph(self.test_result_format, self.test_result_refine, fast_mode=True)

        # 然后跟 self.data_path 里面的 relations 合并，合并后保存到 self.final_knowledge_graph 里面
        with open(self.data_path, 'r') as f:
            origin_lines = json.load(f)

        with open(self.test_result_refine, 'r') as f:
            test_result_refine = json.load(f)

        origin_res = []
        # 将较短的test_result_refine的relationMentions合并到origin_lines里面
        for test_result_refine_line in test_result_refine:

            for origin_line in origin_lines:
                if origin_line["id"] == test_result_refine_line["id"]:
                    origin_line["relationMentions"] = set(origin_line["relationMentions"] + test_result_refine_line["relationMentions"])

            origin_res.append(origin_line)

        # 将origin_res保存到文件里面
        self.save_data(origin_res, self.final_knowledge_graph)

        return self.final_knowledge_graph
