import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# 设置Matplotlib显示中文
plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
plt.rcParams['axes.unicode_minus'] = False

def creat_graph(n, p):
    tu = nx.Graph()  # 创建一个空的图对象
    tu.add_nodes_from(range(n))  # 添加节点
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.rand() < p:  # 根据概率p是否连接节点i和节点j
                tu.add_edge(i, j)  # 添加一条边
    return tu

def du_fenbu(tu):
    du = [val for (node, val) in tu.degree()]  # 获取每个节点的度
    du_fenbu = np.bincount(du)  # 统计度的分布
    du_prob = du_fenbu / sum(du_fenbu)  # 计算概率
    with open('degreeDistribution.txt', 'w',encoding="utf-8") as f:
        f.write("度 概率\n")
        for degree, prob in enumerate(du_prob):
            if prob > 0:
                f.write(f"{degree} {prob:.4f}\n")  # 将度和概率写入文件
    plt.figure(figsize=(8, 6))  # 设置图表尺寸
    plt.scatter(np.nonzero(du_prob)[0], du_prob[du_prob > 0], alpha=0.6, edgecolors="w", linewidth=0.5)
    plt.xlabel('度')
    plt.ylabel('概率')
    plt.title('度的分布')
    plt.savefig('度的散点图.png', dpi=300)  # 保存度分布图，提高分辨率
    plt.show()

def calculate_julei(tu):
    juleixishu = nx.clustering(tu)  # 计算每个节点的聚类系数
    du = dict(tu.degree())  # 获取节点的度
    pingjun_juleixishu = sum(juleixishu.values()) / len(juleixishu)  # 计算平均聚类系数
    print("平均聚类系数:", pingjun_juleixishu)
    # 输出每个节点的聚类系数到文件
    with open('每个节点的聚类系数.txt', 'w',encoding='utf-8') as f:
        f.write("节点 聚类系数\n")
        for node, cc in juleixishu.items():
            f.write(f"{node} {cc:.4f}\n")  # 将节点和聚类系数写入文件
    du_juleixishu = [(du[node], cc) for node, cc in juleixishu.items()]
    du_juleixishu = np.array(du_juleixishu)
    plt.figure(figsize=(8, 6))  # 设置图表尺寸
    plt.scatter(du_juleixishu[:, 0], du_juleixishu[:, 1], alpha=0.6, edgecolors="w", linewidth=0.5)
    plt.xlabel('度')
    plt.ylabel('聚类系数')
    plt.title('聚类系数和度的关系')
    plt.savefig('聚类系数和度的散点图.png', dpi=300)  # 保存聚类系数与度的关系图，提高分辨率
    plt.show()

def dijkstra(tu, start):
    # 所有距离均设为无限大
    distances = {node: float('infinity') for node in tu.nodes}
    distances[start] = 0
    # 创建一个集合，包含还没有找到最短路径的节点
    nodes = set(tu.nodes)
    while nodes:
        # 选出一个未处理的节点中，距离最小的节点
        closest_node = min(nodes, key=lambda node: distances[node])
        nodes.remove(closest_node)
        # 更新所有邻居节点的距离
        for neighbor in tu.neighbors(closest_node):
            tentative_value = distances[closest_node] + 1  # 所有边的权重设为1
            if tentative_value < distances[neighbor]:
                distances[neighbor] = tentative_value
    # 返回从起点到所有节点的距离
    return distances

def calculate_lenth(tu):
    path_length_sum = 0
    num_paths = 0
    for start_node in tu.nodes:
        distances = dijkstra(tu, start_node)
        path_length_sum += sum(dist for dist in distances.values() if dist < float('infinity'))
        num_paths += len(distances) - 1  # 减去到自身的路径
    if num_paths > 0:
        pingjun_lujing_changdu = path_length_sum / num_paths
        print("平均最短路径长度:", pingjun_lujing_changdu)
    else:
        print("图不是连通的; 不能计算平均最短路径长度。")

def calculate_relavative(tu):
    du_relavative = nx.degree_pearson_correlation_coefficient(tu)  # 计算度相关系数
    print("度度相关系数:", du_relavative)

if __name__ == "__main__":
    n = 1000  # 节点数量
    p = 0.05  # ER随机图概率
    tu = creat_graph(n, p)
    du_fenbu(tu)
    calculate_julei(tu)
    calculate_lenth(tu)
    calculate_relavative(tu)