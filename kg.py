import os
import re
import json
import random
from prepare.preprocess import process_text
from utils import refine_knowledge_graph
from prepare.process import uie_execute, gpu_init


class ModelTrainer:

    def __init__(self, data_path, output_dir) -> None:
        """ 用来训练 SPN 的一个类

        Args:
            data_path: 用于训练的所有数据，没有切分训练、测试、验证
            output_dir: 保存测试之后的数据的文件夹

        """
        self.data_path = data_path
        self.generated_data_directory = output_dir

        os.makedirs(output_dir, exist_ok=True)
        self.train_file = os.path.join(output_dir, "train.json")
        self.valid_file = os.path.join(output_dir, "valid.json")
        self.test_file = os.path.join(output_dir, "test.json")

        self.prediction = os.path.join(output_dir, 'prediction.json') # 或者 .pickle
        self.test_result_format = os.path.join(output_dir, 'test_result_format.json')
        self.test_result_refine = os.path.join(output_dir, 'test_result_refine.json')

        self.final_knowledge_graph = os.path.join(output_dir, 'knowledge_graph.json}')

        self.split_data()
        self.generate_running_cmd()

    def generate_running_cmd(self):
        params = "python -m main"
        params += " --bert_directory BERT_PATH"
        params += " --max_epoch 100"
        params += " --max_span_length 10"
        params += " --num_generated_triples 15"
        params += " --max_grad_norm 2.5"
        params += " --na_rel_coef 0.25"
        params += f" --train_file {self.train_file}"
        params += f" --valid_file {self.valid_file}"
        params += f" --test_file {self.test_file}"
        params += f" --generated_data_directory {self.generated_data_directory}"
        return params

    def split_data(self):
        """将知识图谱数据(SPN_style)切分为三个文件"""

        with open(self.data_path, 'r') as f:
            lines = [json.loads(line) for line in f.readlines()]
            lines = random.shuffle(lines)

        dataset_length = len(lines)
        # 按照 4:1:5 的比例切分数据集，并分别保存到三个路径里面

        """ 伪代码
        train_lines, valid_lines, test_lines = split(lines)

        save(train_lines, self.train_file)
        save(valid_lines, self.valid_file)
        save(test_lines, self.test_file)
        """

        # TODO Code Here

    def train_and_test(self):
        """训练并测试这个模型，测试的预测结果会保存到 self.prediction 这个文件里面。"""
        os.system(self.params)

    def relation_align(self):
        """读取预测的结果，并将结果跟 test_file 中的三元组对应上"""

        # 将预测的结果跟训练集对齐，转化为 SPN style 的文件，注意，此时先不跟上个版本的合并

        """伪代码
        test_lines = read_json_file_lines(self.test_file)

        prediction = read_test_file(self.prediction)
        test_pred_lines = convert_pred_to_spn_style(prediction) # 返回的是数组
        save(test_pred_lines, self.test_result_format)
        """
        pass

    def refine_and_extend(self):
        """将生成的 test_result_format 重新经过一遍人工清洗"""
        refine_knowledge_graph(self.test_result_format, self.test_result_refine)

        # 然后跟 self.data_path 里面的 relations 合并，合并后保存到 self.final_knowledge_graph 里面


        return self.final_knowledge_graph


class KnowledgeGraphBuilder:

    def __init__(self) -> None:
        self.data_dir = "data/project_v1"  # 存放生成的数据的地方
        self.text_path = "data/raw_data.txt" # 原始的文本文件
        self.base_kg_path = os.path.join(self.data_dir, "base.json") # 生成的三元组文件
        self.refined_kg_path = os.path.join(self.data_dir, "base_refined.json")# 筛选过后的三元组文件

        self.version = 0    # 会随着迭代次数的增加而增加

        self.kg_paths = [] # 一个数组，代表不同迭代版本的知识图谱

        gpu_init(0, 20000) # 初始化 GPU


    def run_iteration(self):
        print(f"Start Runing Iteration v{self.version}")

        cur_data_path = self.kg_path[-1]
        cur_out_path = os.path.join(self.data_dir, f"iteration_v{self.version}")
        trainer = ModelTrainer(cur_data_path, cur_out_path)

        # 判断是否已经训练过了，毕竟这个地方可能会出问题的
        if not os.path.exists(trainer.prediction):
            trainer.train_and_test()

        trainer.relation_align()
        trainer.refine_and_extend()
        self.version += 1

        self.kg_paths.append(trainer.final_knowledge_graph)


    def get_base_kg_from_txt(self):
        """ Get base knowledge graph by UIE and format it to SPN style
        input: self.text_path
        output: self.base_kg_path
        """
        # 1. 清洗文本，切分句子为指定长度
        texts = process_text(self.text_path,480)

        # 3. 喂给 UIE 并得到 relations，注意这里要保存句子的 id（从 0 开始算
        #    注意：这里如果发现已经存在了 self.base_kg_path，就跳过 UIE
        #    如果想要重新使用 UIE 抽取，删掉这个文件就行
        if not os.path.exists(self.base_kg_path):
            all_items = uie_execute(texts)
            with open(self.base_kg_path, 'w') as f:
                for item in all_items():
                    f.writelines(json.dumps(item, ensure_ascii=False) + "\n")

        # 4. 算法验证，使用 bertTokenizer 检测一下实体是否还存在于句子里面
        filtted_items = auto_filter(all_items)

        # 5. 人工筛选并保存，因为需要加断点，所以需要一边做一边保存
        manual_filter(filtted_items, self.refined_kg_path)

    def save_to_local(self):
        """用于将这个类保存到本地的一个方法"""

        pass

    def load_from_local(self, path):
        pass


if __name__ == "__main__":

    KG = KnowledgeGraphBuilder()

    # startup
    KG.get_base_kg_from_txt()  # 预计用时：