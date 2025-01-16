def knapsack_01(capacity, weights, values):
    n = len(weights)  
    items = [(values[i] / weights[i], weights[i], values[i], i + 1) for i in range(n)]
    # 根据价值重量比降序排序
    items.sort(reverse=True)
    total_value = 0  
    bag = []  # 初始化背包内容为空列表，用于存储装入背包的物品和其重量
    for ratio,weight, value, index in items:
        if weight <= capacity:
            # 如果物品可以完全装入背包
            bag.append((index, weight))  
            total_value += value  
            capacity -= weight  
        else:
            # 如果物品需要分割
            fraction = capacity / weight  # 计算可以装入背包的物品部分
            bag.append((index, weight * fraction))  # 将物品的一部分加入背包
            total_value += value * fraction  # 增加背包中物品的总价值
            break  # 背包已满，退出循环
    return total_value, bag  # 返回背包中物品的总价值和背包内容

# 物品的重量和价值
weights = [35, 30, 60, 50, 40, 10, 25]
values = [10, 40, 30, 50, 35, 40, 30]
# 背包的总容量
capacity = 150
total_value, bag = knapsack_01(capacity, weights, values)
print("装进背包的物品及其重量：")
for item in bag:
    print(f"物品 {item[0]}：{item[1]}")
print(f"总价值：{total_value:.3f}")