def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, W + 1):
            # 如果背包容量小于当前物品的重量，那么不选这个物品
            if j < weights[i - 1]:
                dp[i][j] = dp[i - 1][j]
            else:
                # 要么选择当前物品，要么不选。选择二者的最大价值
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1])

    # 通过dp数组回溯，确定选择的物品
    selected_items = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i)  # 添加物品的编号
            w -= weights[i - 1]

    return dp[n][W], selected_items


weights = [35, 30, 60, 50, 40, 10, 25]
values = [10, 40, 30, 50, 35, 40, 30]
W = 150

max_value, selected_items = knapsack(weights, values, W)
print(f"选择的物品编号为: {selected_items}")
print(f"背包中的最大价值为: {max_value}")
