import os
import json
from opencc import OpenCC
from transformers import AutoTokenizer, AutoModel
from app.utils.image_searcher import ImageSearcher
from app.utils.query_wiki import WikiSearcher
from app.utils.ner import Ner
from app.views.graph import search_node_item

model = None
tokenizer = None
init_history = None

ner = Ner()
image_searcher = ImageSearcher()
wiki_searcher = WikiSearcher()
cc = OpenCC('t2s')

def predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history
    return model.chat(tokenizer, user_input, history)


def stream_predict(user_input, history=None):
    global model, tokenizer, init_history
    if not history:
        history = init_history

    ref = ""

    # 获取实体
    graph = {}
    entities = []
    entities = ner.get_entities(user_input, etypes=["物体类", "人物类", "地点类", "组织机构类", "事件类", "世界地区类", "术语类"])
    print("entities: ", entities)

    # 获取实体的三元组
    for entity in entities:
        graph = search_node_item(entity, graph if graph else None)

    print("user_input: ", user_input)
    # graph = search_node_item(user_input)

    image = image_searcher.search(user_input)
    # wiki = wiki_searcher.search(user_input)

    for ent in [user_input] + entities:
        wiki = wiki_searcher.search(ent)
        if wiki is not None:
            break

    if wiki:
        ref += cc.convert(wiki.summary)
        wiki = {
            "title": cc.convert(wiki.title),
            "summary": cc.convert(wiki.summary),
        }
        print(wiki)
    else:
        wiki = {
            "title": "无相关信息",
            "summary": "暂无相关描述",
        }

    if model is not None:
        if ref:
            chat_input = f"参考资料：{ref}；根据上面资料，回答下面问题：{user_input}"
        else:
            chat_input = user_input

        for response, history in model.stream_chat(tokenizer, chat_input, history):
            updates = {}
            for query, response in history:
                updates["query"] = query
                updates["response"] = response

            result = {
                "history": history,
                "updates": updates,
                "image": image,
                "graph": graph,
                "wiki": wiki
            }
            yield json.dumps(result, ensure_ascii=False).encode('utf8') + b'\n'

    else:
        updates = {
            "query": user_input,
            "response": "模型加载中，请稍后再试"
        }

        result = {
            "history": history,
            "updates": updates,
            "image": image,
            "graph": graph,
            "wiki": wiki
        }
        yield json.dumps(result, ensure_ascii=False).encode('utf8') + b'\n'

def start_model():
    global model, tokenizer, init_history

    tokenizer = AutoTokenizer.from_pretrained("/fast/zwj/ChatGLM-6B/weights", trust_remote_code=True)
    model = AutoModel.from_pretrained("/fast/zwj/ChatGLM-6B/weights", trust_remote_code=True).half().cuda()
    model.eval()

    pre_prompt = "你叫 ChatKG，是一个军事领域知识图谱问答机器人，由江南大学先进技术研究院研发，此为背景。下面开始聊天吧！"
    _, history = predict(pre_prompt, [])
    init_history = history