import gurobipy as gp
from gurobipy import GRB

# 创建优化模型
model = gp.Model("Crop_Optimization_with_Area")

# 参数设置
num_land = 2  # 地块数量
num_crops = 3  # 作物数量（0: 小麦, 1: 玉米, 2: 豆类）
num_years = 3  # 规划年数
A = [100, 120]  # 每块地的总面积
P = [100, 120, 80]  # 销售价格
C = [50, 60, 40]    # 种植成本
Y = [2, 2.5, 1.8]   # 亩产量

# 决策变量 a[i,j,t] 表示地块 i 在 t 年分配给作物 j 的种植面积（连续变量）
a = model.addVars(num_land, num_crops, num_years, vtype=GRB.CONTINUOUS, name="area")

# 决策变量 x[i,j,t] 表示是否种植作物 j （0-1变量）
x = model.addVars(num_land, num_crops, num_years, vtype=GRB.BINARY, name="crop")

# 目标函数：最大化总收益
model.setObjective(gp.quicksum(P[j] * Y[j] * a[i,j,t] - C[j] * a[i,j,t]
                               for i in range(num_land) for j in range(num_crops) for t in range(num_years)),
                   GRB.MAXIMIZE)

# 约束1：每块地每年作物种植面积不能超过该地块总面积
for i in range(num_land):
    for t in range(num_years):
        model.addConstr(gp.quicksum(a[i,j,t] for j in range(num_crops)) <= A[i])

# 约束2：不能连续两年种植同一种作物
for i in range(num_land):
    for j in range(num_crops):
        for t in range(num_years - 1):
            model.addConstr(x[i,j,t] + x[i,j,t+1] <= 1)

# 约束3：每三年内至少种植一次豆类
for i in range(num_land):
    for t in range(num_years - 2):
        model.addConstr(gp.quicksum(x[i,2,t+k] for k in range(3)) >= 1)

# 约束4：面积变量 a[i,j,t] 必须和种植决策 x[i,j,t] 关联
for i in range(num_land):
    for j in range(num_crops):
        for t in range(num_years):
            model.addConstr(a[i,j,t] <= A[i] * x[i,j,t])  # 只有种植了该作物，面积才大于0

# 求解模型
model.optimize()

# 输出结果
for i in range(num_land):
    for j in range(num_crops):
        for t in range(num_years):
            if a[i,j,t].x > 0.01:  # 输出非零种植面积
                print(f"Land {i}, Year {t}, Crop {j}, Area: {a[i,j,t].x} acres.")
