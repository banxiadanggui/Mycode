def knapsack(capacity, weights, values):
    n = len(weights)  
    items = [(values[i],weights[i], i + 1) for i in range(n)]
    # 根据价值重量降序排序
    items.sort(reverse=True)
    total_value = 0  
    bag = []  # 初始化背包内容为空列表，用于存储装入背包的物品
    for value,weight, index in items:
        if weight <= capacity:
            # 如果物品可以完全装入背包
            bag.append((index, weight))  
            total_value += value  
            capacity -= weight  
    return total_value, bag  # 返回背包中物品的总价值和背包内容
# 物品的重量和价值
weights = [35, 30, 60, 50, 40, 10, 25]
values = [10, 40, 30, 50, 35, 40, 30]
# 背包的总容量
capacity = 150
total_value, bag = knapsack(capacity, weights, values)
print("装进背包的物品及其重量：")
for item in bag:
    print(f"物品 {item[0]}：{item[1]}")
print(f"总价值：{total_value:.3f}")