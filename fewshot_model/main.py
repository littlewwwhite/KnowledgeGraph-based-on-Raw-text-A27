import json, os
# os.environ["CUDA_VISIBLE_DEVICES"] = '2'
import process, preprocess

'''
需要的数据：
    1、input_file：原始数据
    2、19行输出文件位置
    3、process文件第七行的task_path改为预训练文件路径
'''

input_file = 'data/clean_data.txt'
max_line_length = 480

formatted_output = preprocess.process_text(input_file, max_line_length)

new_items = process.uie_execute(formatted_output)

with open("data/clean_data_res_doc2_300epoch.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(new_items, ensure_ascii=False))

