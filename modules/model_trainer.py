import os
import json
import random
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
        self.test_result_format = os.path.join(output_dir, 'test_result_format.json')
        self.test_result_refine = os.path.join(output_dir, 'test_result_refine.json')

        # 这个是保存了关系的 id 与类别的映射表的文件
        self.data_instance_path = os.path.join(output_dir, 'alphabet.json')
        self.final_knowledge_graph = os.path.join(output_dir, 'knowledge_graph.json}')

        self.split_data()
        self.generate_running_cmd()

    def generate_running_cmd(self):
        params = "python -m main"
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

        os.system(self.params)

    def relation_align(self):
        """

        读取预测的结果，并将结果跟 test_file 中的三元组对应上
        将预测的结果跟训练集对齐，转化为 SPN style 的文件，注意，此时先不跟上个版本的合并

        """

        """获取测试集和spn预测结果"""
        with open(self.test_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        test_lines = []
        for line in lines:
            test_line = json.loads(line)
            test_lines.append(test_line)

        with open(self.prediction, 'r', encoding='utf-8') as file:
            prediction = json.load(file)

        """
        test_pred_lines = convert_pred_to_spn_style(prediction) # 将预测结果转化为SPN训练时的style，返回数组
        test_line[9]["relationMentioned"] = func1(asdasd)
        prediction: ["pred_rel", "rel_prob", "head_start_index", "head_end_index", "head_start_prob", "head_end_prob", "tail_start_index", "tail_end_index", "tail_start_prob", "tail_end_prob"]
        """

        """这个是用index的版本"""

        # test_pred_lines = {}
        # for key, values in prediction.items():
        #     pred_relation = []
        #     for value in values:
        #         pred_rel = value[0]
        #         head_start_index = value[2]
        #         head_end_index = value[3]
        #         tail_start_index = value[6]
        #         tail_end_index = value[7]
        #         em1Text_index = [head_start_index, head_end_index]
        #         em2Text_index = [tail_start_index, tail_end_index]
        #         pred_relation.append([pred_rel, em1Text_index, em2Text_index])
        #     test_pred_lines.update({key: pred_relation})

        assert len(test_lines) == len(prediction)

        pred_lines = []
        # pred_rel ==> rel_label  # 使用 alphabet 里面
        # test_lines[i][head_start_index:head_end_index] ==> me1Text
        # ==> em2Text
        for test_line, pred in zip(test_lines, list(predictions.values())):

            triples = []
            for triple in pred:
                triple = {}
                triple["rel_text"] = ''
                # em1Text
                # em2Text

            triples.append(triple)

            test_line["relationMentions"] = triples

        # 将 test_lines 保存到文件里面


        # REVIEW use token replace the id_index
        test_pred_lines = {} # 保存SPN训练的结果
        for key, values in prediction.items():
            pred_relation = []
            for value in values:
                pred_rel = value[0]
                head_token = value[2]
                tail_token = value[4]
                pred_relation.append([pred_rel, head_token, tail_token])
            test_pred_lines.update({key: pred_relation})


        """save_data(test_pred_lines, test_result_format) """
        self.save_data(test_pred_lines, self.test_result_format)  # 保存到文件里面


    def refine_and_extend(self):
        """将生成的 test_result_format 重新经过一遍人工清洗"""
        refine_knowledge_graph(self.test_result_format, self.test_result_refine, fast_mode=True)

        # 然后跟 self.data_path 里面的 relations 合并，合并后保存到 self.final_knowledge_graph 里面
        # align

        return self.final_knowledge_graph
