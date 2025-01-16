import heapq
# 定义哈夫曼树的节点类
class Node:
    def __init__(self, char, freq):
        self.char = char  
        self.freq = freq  
        self.left = None  
        self.right = None  
    def __compare__(self, other):
        return self.freq < other.freq

# 递归获取哈夫曼编码
def get_codes(node, current_code, huffman_codes):
    if node is None:
        return
    if node.char is not None:
        huffman_codes[node.char] = current_code
    # 递归处理左右子树
    get_codes(node.left, current_code + '0', huffman_codes)
    get_codes(node.right, current_code + '1', huffman_codes)

# 构造哈夫曼树，并获取哈夫曼编码
def huffman_coding(chars, freqs):
    nodes = [Node(char, freq) for char, freq in zip(chars, freqs)]
    heapq.heapify(nodes)  
    # 利用堆构建树
    while len(nodes) > 1:
        left = heapq.heappop(nodes)  # 获取并移除频率最小的节点
        right = heapq.heappop(nodes)  # 获取并移除频率次小的节点
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(nodes, merged)
        
    root = nodes[0]  # 获取哈夫曼树的根节点
    huffman_codes = {}
    get_codes(root, "", huffman_codes)  # 从根节点开始获取哈夫曼编码
    return huffman_codes

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
freqs = [0.25, 0.1, 0.12, 0.2, 0.15, 0.07, 0.11]
codes = huffman_coding(chars, freqs)
# 按照abcdefg的顺序输出哈夫曼编码
for char in chars:
    print(f"字符：{char}, 哈夫曼编码：{codes[char]}")