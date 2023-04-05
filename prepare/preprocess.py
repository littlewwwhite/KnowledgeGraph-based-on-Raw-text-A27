import re
from zhconv import convert

# 打开并删除文本中的特殊字符
def clean_to_sentence(file_path):
    with open(file_path, 'r', encoding='utf-8') as f_in:
        dirty_text = f_in.read()
    # 保留中文、英文、数字、字母、标点符号，替换换行符为分号，将繁体转换为简体
    pattern = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9\s，。？！、‘’；《》【】（）：\-/“”\n\t]')
    clean_text = pattern.sub('', dirty_text)
    # clean_text = clean_text.replace('\n', '；')
    clean_text = convert(clean_text, 'zh-cn')
    split_pattern = re.compile('([。？！])')
    clean_sentences = split_pattern.split(clean_text)
    return clean_sentences

# 将文本按照句子分割
def add_sentences(sentences, max_line_length=480):
    current_line = ''
    output = []
    for sentence in sentences:
        if len(current_line) + len(sentence) + 1 > max_line_length:
            output.append(current_line.strip())
            current_line = ''
        current_line += sentence + ' '
    if current_line:
        output.append(current_line.strip())
    return output

# 将文本按照句子分割
def process_text(input_file, max_line_length):
    sentences = clean_to_sentence(input_file)
    formatted_output = add_sentences(sentences, max_line_length)
    return formatted_output