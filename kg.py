import os
import re
import json
import random

def check_input(prompt, keys):

    checked = False
    while not checked:
        user_input = input(f"{prompt} > ")
        if user_input in keys:
            checked = True

    return user_input


def refine_knowledge_graph(kg_path, refined_kg_path, fast_mode=False):
    """用于手工对知识图谱进行筛选，也就是遍历 sentence 和 relations，然后手工筛选

    fast_mode: 如果为 True，直接写入
    """

    # 判断是否继续
    try:
        with open(refined_kg_path, 'r') as f:
            start_pos = len(f.readlines())

    except:
        start_pos = 0

    with open(kg_path, 'w') as f_in, open(refined_kg_path, 'a+') as f_out:
        lines = f_in.readlines()
        for line in lines[start_pos:]:
            line = json.loads(f_in)

            if fast_mode:
                f_out.writelines(json.dumps(line, ensure_ascii=False) + "\n")
                continue

            refined_triples = []
            print(line["sentText"])
            for triple in line["relations"]:
                print(f"主体：{triple['em1Text']}, 关系：{triple['label']}，客体：{triple['em2Text']}")
                user_input = check_input("是否构成关系？是则直接【回车】，否则输入【Z】")
                if not user_input:
                    refined_triples.append(triple)

            line["relations"] = refined_triples
            f_out.writelines(json.dumps(line, ensure_ascii=False) + "\n")


class ModelTrainer():

    def __init__(self, data_path, generated_data_directory) -> None:
        """ 用来训练 SPN 的一个类

        Args:
            data_path: 用于训练的所有数据，没有切分训练、测试、验证
            generated_data_directory: 保存测试之后的数据的文件夹

        """
        self.data_path = data_path
        self.train_file = data_path.split(".")[0] + "_train.json"
        self.valid_file = data_path.split(".")[0] + "_valid.json"
        self.test_file = data_path.split(".")[0] + "_test.json"

        self.generated_data_directory = generated_data_directory
        self.prediction = os.path.join(generated_data_directory, 'prediction.json') # 或者 pickle
        self.test_result_format = os.path.join(generated_data_directory, 'test_resule_format.json')
        self.test_result_refine = os.path.join(generated_data_directory, 'test_resule_refine.json')

        self.params = "python -m main"
        self.params += " --bert_directory BERT_PATH"
        self.params += " --max_epoch 100"
        self.params += " --max_span_length 10"
        self.params += " --num_generated_triples 15"
        self.params += " --max_grad_norm 2.5"
        self.params += " --na_rel_coef 0.25"
        self.params += f" --train_file {self.train_file}"
        self.params += f" --valid_file {self.valid_file}"
        self.params += f" --test_file {self.test_file}"
        self.params += f" --generated_data_directory {self.generated_data_directory}"

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
        #
        #
        #
        #

    def train_and_test(self):
        os.system(self.params)

        return

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

        # 然后跟 self.data_path 里面的 relations 合并，合并后保存到 kg_v1 里面

        return "kg_v2 path"


class KG():

    def __init__(self) -> None:
        self.data_dir = ""
        self.text_path = ""
        self.kg_paths = [] # 一个数组，代表不同迭代版本的知识图谱

        self.trainer = ModelTrainer()




    def get_base_kg_from_txt(self, text_path, base_res_path):
        """ Get base knowledge graph by UIE and format it to SPN style

        Args:
            text_path: the raw sentence path.
            json_path: the formatted data.
        """

        # 将 extract.py 里面的内容在这里面调用，这里面可能也是包含了多个函数的调用的
        # 所要实现的功能是将 txt 文本变成 SPN 的格式，注意这里的文本应该是纯文本，
        # 类似于 paddlenlp/data/raw_data/raw_data.txt，而不是 paddlenlp/data/raw_data/raw_data_lines.txt
        # 也就是说，切分文本以及清洗文本也是在这里调用的，下面一些大致的流程，具体根据你之前的代码修改

        # 1. 清洗文本

        # 2. 切分句子

        # 3. 喂给 UIE 并得到 relations，注意这里要保存句子的 id（从 0 开始算）

        # 4. 算法验证，使用 bertTokenizer 检测一下实体是否还存在于句子里面

        # 5. 保存到指定文件 base_res_path

        pass

