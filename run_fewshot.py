import json, os
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
from fewshot_model.preprocess import process_text
from fewshot_model.process import uie_execute

'''
需要的数据：
    1、input_file：原始数据
    2、19行输出文件位置
    3、process文件第七行的task_path改为预训练文件路径
'''

input_file = 'data/clean_data.txt'
max_line_length = 480

formatted_output = process_text(input_file, max_line_length)

# # 保存分割后的句子
# with open("data/clean_data_res_doc2_300epoch.txt", "w", encoding='utf-8') as f:
#     f.write(json.dumps(formatted_output, ensure_ascii=False))

new_items = uie_execute(formatted_output)


with open("data/clean_data_res_41lines_100epoch.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(new_items, ensure_ascii=False))

