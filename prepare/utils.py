import json

def check_input(prompt, keys):

    checked = False
    while not checked:
        user_input = input(f"{prompt} > ")
        if user_input in keys:
            checked = True
        else:
            print("输入错误，请重新输入")

    return user_input


def refine_knowledge_graph(kg_path, refined_kg_path, fast_mode=True):
    """用于手工对知识图谱进行筛选，也就是遍历 sentence 和 relations，然后手工筛选
    kg_path: 原始三元组存储路径
    refined_kg_path: 筛选后三元组存储路径
    fast_mode: 如果为 True，直接写入
    """

    # 判断是否继续

    print(f"源数据：{kg_path}")
    print(f"筛选后数据：{refined_kg_path}\n")

    try:
        with open(kg_path, 'r', encoding='UTF-8') as f_src, open(refined_kg_path, 'w', encoding='UTF-8') as f_refined:
            start_pos = 0
            kg_lines = f_src.readlines()
            refined_lines = f_refined.readlines()
            for i in range(len(refined_lines)):
                if refined_lines[i]["id"] == kg_lines[i]["id"]:
                    f_refined.writelines(json.dumps(refined_lines[i], ensure_ascii=False) + "\n")
                    start_pos += 1

        print(f"检测到已经筛选过 {start_pos} 条数据，将从第 {start_pos + 1} 条开始筛选\n")

    except:
        print("检测到没有筛选过数据，将从第 1 条开始筛选\n")
        start_pos = 0

    with open(kg_path, 'r', encoding='UTF-8') as f_in, open(refined_kg_path, 'a+', encoding='UTF-8') as f_out:
        lines = f_in.readlines()

        total = len(lines)

        for pos in range(start_pos, total):
            line = json.loads(lines[pos])

            if fast_mode:
                f_out.writelines(json.dumps(line, ensure_ascii=False) + "\n")
                print("fast_mode已打开，数据不需要筛选，已保存！")
                continue

            print(f"【 {pos+1}/{total} 】在这个句子中 >>>>>>>>")

            refined_triples = []
            print(line["sentText"])
            for triple in line["relationMentions"]:
                print(f"\n主体：【{triple['em1Text']}】, 关系：【{triple['label']}】，客体：【{triple['em2Text']}】")
                user_input = check_input(
                    prompt="是否构成关系？是则直接【Y】，否则输入【N】，输入【回车】暂时退出",
                    keys=["Y", "y", "N", "n", ""])

                if user_input == "Y" or user_input == "y":
                    refined_triples.append(triple)
                elif user_input == "":
                    print("退出筛选！")
                    exit(0)

            line["relationMentions"] = refined_triples
            f_out.writelines(json.dumps(line, ensure_ascii=False) + "\n")
            print("已保存！\n")

    print("筛选完成！辛苦！")

    return refined_kg_path

#
# if __name__ == "__main__":
#     kg_path = "res_base_v4.json"
#     refined_kg_path = "res_base_v4_refine.json"
#
#     refine_knowledge_graph(kg_path, refined_kg_path)
