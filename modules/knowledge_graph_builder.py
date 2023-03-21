import os
import json
from prepare.preprocess import process_text
from prepare.utils import refine_knowledge_graph
from prepare.process import uie_execute
from prepare.filter import auto_filter

from modules.model_trainer import ModelTrainer


class KnowledgeGraphBuilder:

    def __init__(self, args) -> None:
        """

        文件的存储路径，以及一些参数的初始化

        """
        self.data_dir = os.path.join("data", args.project)  # 存放生成的数据的地方
        self.text_path = os.path.join("data", "raw_data.txt") # 原始的文本文件
        self.base_kg_path = os.path.join(self.data_dir, "base.json") # 生成的三元组文件
        self.refined_kg_path = os.path.join(self.data_dir, "base_refined.json")# 筛选过后的三元组文件


        self.model_name_or_path = "bert-base-chinese" # 预训练模型的名字
        self.version = 0    # 会随着迭代次数的增加而增加
        self.kg_paths = [] # 一个数组，代表不同迭代版本的知识图谱
        self.GPU = "0"  # GPU 的编号

        os.makedirs(self.data_dir, exist_ok=True)


    def run_iteration(self):
        print(f"Start Runing Iteration v{self.version}")

        cur_data_path = self.kg_path[-1]
        cur_out_path = os.path.join(self.data_dir, f"iteration_v{self.version}")
        trainer = ModelTrainer(cur_data_path, cur_out_path, self.model_name_or_path)

        # 判断是否已经训练过了，毕竟这个地方可能会出问题的
        if not os.path.exists(trainer.prediction):
            trainer.train_and_test()

        trainer.relation_align()
        trainer.refine_and_extend()
        self.version += 1

        self.kg_paths.append(trainer.final_knowledge_graph)

    def extend_ratio(self):
        """用于计算扩展的比例，如果扩展的比例小于 10%，则认为已经收敛"""

        pre_kg = self.kg_paths[-2]
        cur_kg = self.kg_paths[-1]

        total_rel = 0  # 图谱中的所有三元组的数量（之前的）
        extend_rel = 0 # 图谱中扩展的三元组的数量
        with open(pre_kg, 'r') as f_pre, open(cur_kg, 'r') as f_cur:
            pre_lines = [json.loads(line) for line in f_pre.readlines()]
            cur_lines = [json.loads(line) for line in f_cur.readlines()]

            assert len(pre_lines) == len(cur_lines)

            for pre_line, cur_line in zip(pre_lines, cur_lines):
                pre_rels = pre_line['relations']
                cur_rels = cur_line['relations']

                total_rel += len(pre_rels)
                extend_rel += len(cur_rels) - len(pre_rels)
                assert len(pre_rels) <= len(cur_rels)

        return extend_rel / total_rel


    def get_base_kg_from_txt(self):
        """ Get base knowledge graph by UIE and format it to SPN style
        input: self.text_path
        output: self.refined_kg_path
        """
        # 1. 清洗文本，切分句子为指定长度
        texts = process_text(self.text_path, 480)

        # 3. 喂给 UIE 并得到 relations，注意这里要保存句子的 id（从 0 开始算
        #    注意：这里如果发现已经存在了 self.base_kg_path，就跳过 UIE
        #    如果想要重新使用 UIE 抽取，删掉这个文件就行
        if not os.path.exists(self.base_kg_path):
            all_items = uie_execute(texts)
            with open(self.base_kg_path, 'w') as f:
                for item in all_items():
                    f.writelines(json.dumps(item, ensure_ascii=False) + "\n")
        else:
            print(f"Base KG already exists in {self.base_kg_path}, skip UIE.")

        # 4. 算法验证，使用 bertTokenizer 检测一下实体是否还存在于句子里面
        filtted_items = auto_filter(all_items, self.model_name_or_path)

        # 5. 人工筛选并保存，因为需要加断点，所以需要一边做一边保存
        refine_knowledge_graph(filtted_items, self.refined_kg_path, fast_mode=True)

    def save(self, save_path=None):
        if save_path is None:
            save_path = os.path.join(self.data_dir, f"iter_v{self.version}.json")

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    def load(self, load_path=None):
        with open(load_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.__dict__.update(state)# 作用是将 state 中的键值对更新到 self.__dict__ 中
