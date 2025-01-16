import numpy as np
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverFactory

def read_data():
    df = pd.read_excel("task_model/附件1.xlsx", sheet_name="乡村的现有耕地")
    # 地块面积
    area = {i:float(df.loc[i]['地块面积/亩']) for i in range(len(df))}
    # 地块类型
    # area_list = ['A', 'B', 'C', 'D', 'E', 'F']
    A = list(range(0, 6))
    B = list(range(6, 20))
    C = list(range(20, 26))
    D = list(range(26, 34))
    E = list(range(34, 51))
    F = list(range(51,54))


    area_dict = {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'E': E,
        'F': F
    }
    # print(area)
    df = pd.read_excel("task_model/附件1.xlsx",sheet_name="乡村种植的农作物")
    # print(df.notna)
    crop = {i+1:df.loc[i]['作物类型'] for i in range(len(df) - 4)}
    # print(crop)
    n1 = list(range(34, 37)) # 大白菜等
    n2 = list(range(19, 34)) # 除大白菜等和豆类以外的蔬菜
    n3 = list(range(37, 41)) # 食用菌
    n4 = [15] # 水稻
    n5 = list(range(0, 5)) # 粮食豆类
    n6 = list(range(16, 19)) # 蔬菜豆类
    n7 = list(range(5, 15)) # 除水稻、豆类以外的粮食

    crop_dict = {
        'n1': n1,
        'n2': n2,
        'n3': n3,
        'n4': n4,
        'n5': n5,
        'n6': n6,
        'n7': n7
    }

    df = pd.read_excel("task_model/附件2.xlsx",sheet_name="2023年统计的相关数据")
    # print(df)
    cost = {}
    cost['A'] = {'crop': list(range(1, 16))}
    cost['A']['cost'] = []
    cost['A']['price'] = []
    cost['A']['per'] = []
    for i in range(15):
        cost['A']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['A']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')])/2)
        cost['A']['per'].append(int(df.loc[i]['亩产量/斤']))
    cost['B'] = {'crop': list(range(1, 16))}
    cost['B']['cost'] = []
    cost['B']['price'] = []
    cost['B']['per'] = []
    for i in range(15, 30):
        cost['B']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['B']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['B']['per'].append(int(df.loc[i]['亩产量/斤']))
    cost['C'] = {'crop': list(range(1, 16))}
    cost['C']['cost'] = []
    cost['C']['price'] = []
    cost['C']['per'] = []
    for i in range(30, 45):
        cost['C']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['C']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['C']['per'].append(int(df.loc[i]['亩产量/斤']))
    cost['D'] = {'crop': list(range(16, 35))}
    cost['D']['cost'] = []
    cost['D']['price'] = []
    cost['D']['per'] = []
    for i in range(45, 64):
        cost['D']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['D']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['D']['per'].append(int(df.loc[i]['亩产量/斤']))
    cost['E'] = {'crop': list(range(17, 35))}
    cost['E']['cost'] = []
    cost['E']['price'] = []
    cost['E']['per'] = []
    for i in range(64, 82):
        cost['E']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['E']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['E']['per'].append(int(df.loc[i]['亩产量/斤']))

    cost['D']['crop'].extend(list(range(35, 38)))
    for i in range(82, 85):
        cost['D']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['D']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['D']['per'].append(int(df.loc[i]['亩产量/斤']))

    cost['E']['crop'].extend(list(range(38, 42)))
    for i in range(85, 89):
        cost['E']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['E']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['E']['per'].append(int(df.loc[i]['亩产量/斤']))

    cost['F'] = {'crop': list(range(17, 35))}
    cost['F']['cost'] = []
    cost['F']['price'] = []
    cost['F']['per'] = []
    for i in range(89, 107):
        cost['F']['cost'].append(int(df.loc[i]['种植成本/(元/亩)']))
        cost['F']['price'].append(sum([float(i) for i in df.loc[i]['销售单价/(元/斤)'].split('-')]) / 2)
        cost['F']['per'].append(int(df.loc[i]['亩产量/斤']))
    # print(cost)
    return area, area_dict, crop, crop_dict, cost
def solve(area: dict, area_dict: dict[list], crop: dict, crop_dict: dict[list], cost: dict[dict[list]], promised: dict, price: dict):
    plant = np.zeros((16, 41, 54))
    # print(plant)
    for i in range(2,16):
        if i % 2 == 1:
            for j in crop_dict['n1']:
                for k in area_dict['D']:
                    plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in (crop_dict['n2'] + crop_dict['n6']):
                for k in (area_dict['D'] + area_dict['E']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        for j in (crop_dict['n2'] + crop_dict['n6']):
            for k in (area_dict['F']):
                plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 1:
            for j in crop_dict['n3']:
                for k in (area_dict['E']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        for j in crop_dict['n4']:
            for k in (area_dict['D']):
                plant[i, j, k] = 1

    for i in range(2, 16):
        for j in crop_dict['n5']:
            for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                plant[i, j, k] = 1


    for i in range(2, 16):
        for j in crop_dict['n7']:
            for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                plant[i, j, k] = 1

    # print(max(area.values()))
    # print(area)
    cost_year = {i: cost for i in range(7)}

    model = ConcreteModel()
    year = 8
    season = 16
    crops = 41
    grid = 54
    # A = model.addVars(season, crops, grid, lb=0, ub=max(area.values()), name="A", vtype=GRB.CONTINUOUS)
    # 植物所种地的限制
    model.A = Var(range(16), range(41), range(54),within=NonNegativeReals)
    #真实价格
    price_[i][j]
    yield_[i][j]
    model.NormalSell = Var(range(8), range(41),within=NonNegativeReals)
    model.UnNormalSell = Var(range(8), range(41), within=NonNegativeReals)
    for i in range(1, 8):
        for j in range(41):
            #model.constrants.add(model.NormalSell[i,j]<=sum(cost[key]['per'][cost[key]['crop'].index(g)]*model.A[i*2,j,k] for k in range(54))+sum(cost[key]['per'][cost[key]['crop'].index(g)]*model.A[i*2+1,j,k] for k in range(54)))
            model.constrants.add(model.NormalSell[i,j]<=sum(yield_[i][j]*model.A[i,j,k] for k in range(54))+sum(yield_[i][j]*model.A[i,j,k] for k in range(54)))
     
    for i in range(1, 8):
        for j in range(41):
            model.constrants.add(model.NormalSell[i,j]<=sum(cost[key]['per'][cost[key]['crop'].index(g)]*model.A[i,j,k] for k in range(54)))
    model.constraints = ConstraintList()
    for i in range(2, 16):
        for j in range(41):
            for k in range(54):
                model.constraints.add(model.A[i, j, k] <= plant[i, j, k] * area[k])

    # 种的植物面积不超过耕地面积
    for i in range(2, 16):
        for k in range(54):
            model.constraints.add(sum(model.A[i, j, k] for j in range(41)) <= area[k])

    # 解决豆类三年种植问题
    for i in range(11):
        for k in range(54):
            model.constraints.add(sum(model.A[x, j, k] for x in range(i,i+6) for j in (crop_dict['n5'] + crop_dict['n6'])) >= area[k])

    # 水稻只能单季节种植
    for i in range(2, 16):
        if i % 2 == 0:
            for k in area_dict['D']:
                model.constraints.add(model.A[i+1, 15, k] == model.A[i, 15, k])

    # A、B、C地种植单季节植物
    for i in range(2, 14):
        if i % 2 == 0:
            for j in (crop_dict['n5'] + crop_dict['n7']):
                for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                    model.constraints.add(model.A[i+1, j, k] == model.A[i, j, k])

    for i in range(2, 14):
        if i % 2 == 0:
            for j in (crop_dict['n5'] + crop_dict['n7']):
                for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                   model.constraints.add(model.A[i+2, j, k] * model.A[i, j, k] == 0)

    for i in range(2, 15):
        for j in (crop_dict['n2'] + crop_dict['n6']):
             for k in area_dict['F']:
                 model.constraints.add(model.A[i + 1, j, k] * model.A[i, j, k] == 0)

    for i in range(2, 14):
        for j in crop_dict['n4']:
            for k in area_dict['D']:
                model.constraints.add(model.A[i + 2, j, k] * model.A[i, j, k] == 0)

    df = pd.read_excel("task_model/附件2.xlsx", sheet_name="2023年的农作物种植情况")
    df = df.ffill()

    model.constraints.add(model.A[0, 5, 0] == 80)
    model.constraints.add(model.A[1, 5, 0] == 80)
    i = 0
    for x in range(1,len(df)):
        if df.loc[x-1]['种植地块'] != df.loc[x]['种植地块']:
            i += 1
            if i == 51:
                break
            model.constraints.add(model.A[1, int(df.loc[x-1]['作物编号']) -1, i-1] == float(df.loc[x-1]['种植面积/亩']))
            model.constraints.add(model.A[0, int(df.loc[x]['作物编号']) -1, i] == float(df.loc[x]['种植面积/亩']))

    model.constraints.add(model.A[0,32,50] == 0.3)
    model.constraints.add(model.A[1,23,50] == 0.3)
    model.constraints.add(model.A[1,20,50] == 0.3)
    model.constraints.add(model.A[0,24,51] == 0.3)
    model.constraints.add(model.A[0,25,51] == 0.3)
    model.constraints.add(model.A[1,21,51] == 0.3)
    model.constraints.add(model.A[1,28,51] == 0.3)
    model.constraints.add(model.A[0,16,52] == 0.6)
    model.constraints.add(model.A[1,27,52] == 0.3)
    model.constraints.add(model.A[1,29,52] == 0.3)
    model.constraints.add(model.A[0,18,53] == 0.6)
    model.constraints.add(model.A[1,33,53] == 0.3)
    model.constraints.add(model.A[1,22,53] == 0.3)


    model.obj = Objective(expr=sum(model.A[i,g-1,area] * cost[key]['per'][cost[key]['crop'].index(g)] * cost[key]['price'][cost[key]['crop'].index(g)] - model.A[i,g-1,area]*cost[key]['cost'][cost[key]['crop'].index(g)]  for key in area_dict.keys() for g in cost[key]['crop'] for area in area_dict[key] for i in range(2, 16)), sense=maximize)
    model.obj = Objective(expr=sum(model.NormalSell[i,j]*price[i][j]+ for i in range(2,16)for j in range (41)))
    solver = SolverFactory('gurobi')
    solver.solve(model,tee=True)
    print(model)
    #输出
    file_name='task_model/result1_1.xlsx'#添加了相对路径，使用时可更改
    sheet_name=["2023","2024","2025","2026","2027","2028","2029","2030"]
    df_output=[]
    for i in range (1,8):
        df_output.append(pd.read_excel(file_name, sheet_name=sheet_name[i])) 
    for i in range(16):
        for j in range(41):
            for k in range(54):
                if  model.A[i,j,k].value is not None and  i>=2:
                    row_index = k # 将 i 替换为具体的行号
                    col_index = j+2
                    if i%2 == 1:
                        row_index=k+28
                    df_output[int(i/2-1)].iat[row_index,col_index]=model.A[i,j,k].value
                    if model.A[i,j,k].value > 0.0:
                        if i==2 or i==3:
                            print(i,j,k,model.A[i,j,k].value)
                        df_output[int(i/2-1)].iat[row_index,col_index]=model.A[i,j,k].value
                
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
        for i in range(7):
            df_output[i].to_excel(writer, sheet_name=sheet_name[i+1], index=False)
    #输出结束
def test(area: dict, area_dict: dict[list], crop: dict, crop_dict: dict[list], cost: dict[dict[list]]):
    df = pd.read_excel("task_model/附件2.xlsx",sheet_name="2023年的农作物种植情况")
    df = df.ffill()
    # print(df.describe())
    promised = {i:0 for i in crop.keys()}
    money = 0
    # print(promised)
    money = [0 for _ in range(len(crop.keys())+1)]
    for i in range(len(df)):
        for key in area_dict.keys():
            if key in df.loc[i]['种植地块']:
                # print(key)
                promised[int(df.loc[i]['作物编号'])] += float(df.loc[i]['种植面积/亩']) * cost[key]['per'][cost[key]['crop'].index(int(df.loc[i]['作物编号']))]

                money[int(df.loc[i]['作物编号'])] += float(df.loc[i]['种植面积/亩']) * cost[key]['per'][cost[key]['crop'].index(int(df.loc[i]['作物编号']))] * cost[key]['price'][cost[key]['crop'].index(int(df.loc[i]['作物编号']))] - cost[key]['cost'][cost[key]['crop'].index(int(df.loc[i]['作物编号']))] * float(df.loc[i]['种植面积/亩'])
                break

    price = {}

    for key in cost.keys():
        for i in range(len(cost[key]['crop'])):
            price[cost[key]['crop'][i]] = cost[key]['price'][i]

    print(price)
    # print(promised)
    # print(money)
    # print(sum(money))
    return promised,price
def main():
    area, area_dict, crop, crop_dict, cost = read_data()
    promised, price = test(area, area_dict, crop, crop_dict, cost)
    solve(area, area_dict, crop, crop_dict, cost, promised, price)

main()