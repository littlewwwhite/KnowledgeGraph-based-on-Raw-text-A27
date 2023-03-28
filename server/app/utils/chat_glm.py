import os
import json
from transformers import AutoTokenizer, AutoModel

model = None
tokenizer = None
init_history = None

def predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history
    return model.chat(tokenizer, user_input, history)


def stream_predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history

    if "江南大学" in user_input:
        image = r"https://news.jiangnan.edu.cn/__local/6/D9/98/C642DE3CDC7F72EC01C8A84FEE8_39252AC8_1D99C.jpg"
    else:
        image = None

    for response, history in model.stream_chat(tokenizer, user_input, history):
        updates = {}
        for query, response in history:
            updates["query"] = query
            updates["response"] = response
        yield json.dumps({"history": history, "updates": updates, "image": image}, ensure_ascii=False).encode('utf8') + b'\n'


def start_model():
    global model, tokenizer, init_history

    tokenizer = AutoTokenizer.from_pretrained("/fast/zwj/ChatGLM-6B/weights", trust_remote_code=True)
    model = AutoModel.from_pretrained("/fast/zwj/ChatGLM-6B/weights", trust_remote_code=True).half().cuda()
    model.eval()

    pre_prompt = "你叫 ChatKG，是一个知识图谱问答机器人，由江南大学先进技术研究院研发，此为背景。下面开始聊天吧！"
    _, history = predict(pre_prompt, [])
    init_history = history