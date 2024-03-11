import re
from zhconv import convert

# 打开并删除文本中的特殊字符
def clean_to_sentence(file_path):
    with open(file_path, 'r', encoding='utf-8') as f_in:
        dirty_text = f_in.read()
    # 去除非中英文和数字字符
    dirty_text = dirty_text.replace('彳艮', '很')
    dirty_text = dirty_text.replace('\n', '；')
    dirty_text = dirty_text.replace('\t', '；')
    dirty_text = "".join(dirty_text.split())

    pattern = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9，。？！、‘’；“”《》]')
    clean_text = pattern.sub('', dirty_text)
    clean_text = convert(clean_text, 'zh-cn') 
    clean_text = clean_text.replace(' ', '')
    clean_text = clean_text.replace('。 ', '。')
    clean_text = clean_text.replace('。；', '。')
    clean_sentences = [sent + "。" for sent in clean_text.split('。')]
    return clean_sentences

# 将文本按照句子分割
def add_sentences(sentences, max_line_length=480):
    current_line = ''
    output = []
    for sentence in sentences:
        if len(current_line) + len(sentence) + 1 > max_line_length:
            output.append(current_line.strip())
            current_line = ''
        current_line += sentence
    if current_line:
        output.append(current_line.strip())
    return output

# 将文本按照句子分割
def process_text(input_file, max_line_length):
    sentences = clean_to_sentence(input_file)
    formatted_output = add_sentences(sentences, max_line_length)
    return formatted_output


