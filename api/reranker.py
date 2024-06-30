from FlagEmbedding import FlagReranker

path = "D:\\Workspace\\models\\bge-reranker-base"
reranker = FlagReranker(path, use_fp16=True, device='cuda')


def sort(query: str, contents: [str]):
    arr = []
    for content in contents:
        arr.append((query, content))
    scores = reranker.compute_score(arr)

    # 将分数和内容绑定在一起，形成一个元组列表
    scored_contents = list(zip(scores, contents))
    # 过滤掉分数小于0的元素
    filtered_contents = [(score, content) for score, content in scored_contents if score >= 0]
    # 按照分数从大到小排序
    filtered_contents.sort(key=lambda x: x[0], reverse=True)
    # 提取排序后的内容
    sorted_contents = [content for score, content in filtered_contents]

    return sorted_contents


def sort_include_score(query: str, contents: [str]):
    arr = []
    for content in contents:
        arr.append((query, content))
    scores = reranker.compute_score(arr)

    # 将分数和内容绑定在一起，形成一个元组列表
    scored_contents = list(zip(scores, contents))
    # 过滤掉分数小于0的元素
    filtered_contents = [(score, content) for score, content in scored_contents if score >= 0]
    # 按照分数从大到小排序
    filtered_contents.sort(key=lambda x: x[0], reverse=True)
    # 提取排序后的内容
    sorted_contents = [(content, score) for score, content in filtered_contents]

    return sorted_contents



