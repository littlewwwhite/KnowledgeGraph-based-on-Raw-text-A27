import json

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

        print(f"检测到已经筛选过 {start_pos} 条数据，将从第 {start_pos + 1} 条开始筛选")

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

    print("筛选完成！辛苦！")

    return refined_kg_path