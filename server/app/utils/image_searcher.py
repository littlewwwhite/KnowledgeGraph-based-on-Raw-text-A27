
image_pair = {
    "江南大学": "https://news.jiangnan.edu.cn/__local/6/D9/98/C642DE3CDC7F72EC01C8A84FEE8_39252AC8_1D99C.jpg"
}

def image_search(query):

    for key, value in image_pair.items():
        if key in query:
            return value

    return None