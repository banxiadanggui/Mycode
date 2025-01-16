import numpy as np
import pandas as pd
import pulp as pp

def read_data():
    df = pd.read_excel("附件1.xlsx", sheet_name="乡村的现有耕地")
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
    df = pd.read_excel("附件1.xlsx",sheet_name="乡村种植的农作物")
    # print(df.notna)
    crop = {i+1:df.loc[i]['作物类型'] for i in range(len(df) - 4)}
    # print(crop)
    n1 = list(range(35, 38)) # 大白菜等
    n2 = list(range(20, 35)) # 除大白菜等和豆类以外的蔬菜
    n3 = list(range(38, 42)) # 食用菌
    n4 = [16] # 水稻
    n5 = list(range(1, 6)) # 粮食豆类
    n6 = list(range(17, 20)) # 蔬菜豆类
    n7 = list(range(6, 16)) # 除水稻、豆类以外的粮食

    crop_dict = {
        'n1': n1,
        'n2': n2,
        'n3': n3,
        'n4': n4,
        'n5': n5,
        'n6': n6,
        'n7': n7
    }

    df = pd.read_excel("附件2.xlsx",sheet_name="2023年统计的相关数据")
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
def solve(area: dict, area_dict: dict[list], crop: dict, crop_dict: dict[list], cost: dict[dict[list]]):
    plant = np.zeros((16, 42, 55))
    # print(plant)
    for i in range(2,16):
        if i % 2 == 1:
            for j in crop_dict['n1']:
                for k in area_dict['D']:
                    plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in crop_dict['n2']:
                for k in (area_dict['D'] + area_dict['E']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        for j in crop_dict['n2']:
            for k in (area_dict['F']):
                plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 1:
            for j in crop_dict['n3']:
                for k in (area_dict['E']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in crop_dict['n4']:
                for k in (area_dict['D']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in crop_dict['n5']:
                for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in crop_dict['n6']:
                for k in (area_dict['D'] + area_dict['E']):
                    plant[i, j, k] = 1

    for i in range(2, 16):
        for j in crop_dict['n6']:
            for k in (area_dict['F']):
                plant[i, j, k] = 1

    for i in range(2, 16):
        if i % 2 == 0:
            for j in crop_dict['n7']:
                for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                    plant[i, j, k] = 1

    df = pd.read_excel("附件2.xlsx", sheet_name="2023年的农作物种植情况")
    df = df.ffill()
    # model = Model("plantBestProgramming")
    season = list(range(16))
    crops = list(range(41))
    grid = list(range(54))
    A = pp.LpVariable.dicts("A", (season, crops, grid), lowBound=0)
    model = pp.LpProblem("planBestProgramming",sense=pp.LpMaximize)
    model += (A[0][5][0] == 80)
    model += (A[1][5][0] == 80)
    y = 0
    for x in range(1, len(df)):
        if df.loc[x - 1]['种植地块'] != df.loc[x]['种植地块']:
            y += 1
            # print(f"A[1][{int(df.loc[x-1]['作物编号']) -1}][{i-1}] == {float(df.loc[x-1]['种植面积/亩'])}")
            # print(f"A[0][{int(df.loc[x]['作物编号']) -1}][{i}] == {float(df.loc[x]['种植面积/亩'])}")
            # print("-----------------------------")
            if y == 51:
                break
            model += (A[1][int(df.loc[x - 1]['作物编号']) - 1][y - 1] == int(df.loc[x - 1]['种植面积/亩']))
            model += (A[0][int(df.loc[x]['作物编号']) - 1][y] == int(df.loc[x]['种植面积/亩']))

    # model += (A[0][32][50] == 0.3)
    # model += (A[1][23][50] == 0.3)
    # model += (A[1][20][50] == 0.3)
    # model += (A[0][24][51] == 0.3)
    # model += (A[0][25][51] == 0.3)
    # model += (A[1][21][51] == 0.3)
    # model += (A[1][28][51] == 0.3)
    # model += (A[0][16][52] == 0.6)
    # model += (A[1][27][52] == 0.3)
    # model += (A[1][29][52] == 0.3)
    # model += (A[0][18][53] == 0.6)
    # model += (A[1][33][53] == 0.3)
    # model += (A[1][22][53] == 0.3)

    for i in range(2, 16):
        for j in range(1, 42):
            for k in range(0, 54):
                model += (A[i][j-1][k] <= plant[i, j, k] * area[k])

    for i in range(2, 16):
        for k in range(0, 54):
            model += pp.lpSum(A[i][j-1][k] for j in range(1, 42)) <= area[k]


    # for i in range(0, 11):
    #     for k in range(0, 54):
    #         model+= pp.lpSum(A[x][j-1][k] for x in range(i,i+6) for j in (crop_dict['n5'] + crop_dict['n6'])) >= area[k]

    for i in range(2, 16):
        if i % 2 == 0:
            for j in range(1,41):
                for k in area_dict['D']:
                    model += (A[i][j-1][k] == A[i][j][k])

    for i in range(0, 14):
        if i % 2 == 0:
            for j in (crop_dict['n5'] + crop_dict['n7']):
                for k in (area_dict['A'] + area_dict['B'] + area_dict['C']):
                   z = pp.LpVariable(lowBound=0,name=f"z_one_{i}_{j}_{k}",cat="Integer")
                   model += (z <= A[i][j-1][k])
                   model += (z <= A[i+2][j-1][k])
                   model += (z == 0)

    for i in range(0, 15):
        for j in (crop_dict['n2'] + crop_dict['n6']):
             for k in area_dict['F']:
                 z = pp.LpVariable(lowBound=0, name=f"z_two_{i}_{j}_{k}",cat="Integer")
                 model += (z <= A[i][j - 1][k])
                 model += (z <= A[i + 1][j - 1][k])
                 model += (z == 0)


    for i in range(0, 14):
        for j in crop_dict['n4']:
            for k in area_dict['D']:
                z = pp.LpVariable(lowBound=0, name=f"z_three_{i}_{j}_{k}",cat="Integer")
                model += (z <= A[i][j - 1][k])
                model += (z <= A[i + 2][j - 1][k])
                model += (z == 0)

    model += pp.lpSum(A[i][g-1][area] * (cost[key]['price'][cost[key]['crop'].index(g)] * cost[key]['per'][cost[key]['crop'].index(g)] - cost[key]['cost'][cost[key]['crop'].index(g)])  for key in area_dict.keys() for g in cost[key]['crop'] for area in area_dict[key] for i in range(2, 16)),"Objective"

    model.solve()
    print(pp.value(model.objective))
#导出
    file_name='result1_1.xlsx'
    sheet_name=["2024","2025","2026","2027","2028","2029","2030"]
    df_24 = pd.read_excel(file_name, sheet_name=sheet_name[0])
    print(df_24.shape)
    df.iloc[2:, 2:] = ''
    for i in season:
        for j in crops:
            for k in grid:
                if  A[i][j][k].varValue != None:
                    row_index = k+1  # 将 i 替换为具体的行号
                    col_index = j+1
                    df_24.iat[row_index,col_index]=A[i][j][k].varValue
                    if A[i][j][k].varValue > 0.0:
                        print(i,j,k,A[i][j][k].varValue)
                #print(type(A)value)
    # print(model.status)
    df_24.to_excel(file_name, sheet_name=sheet_name[0], index=False)

def test(area: dict, area_dict: dict[list], crop: dict, crop_dict: dict[list], cost: dict[dict[list]]):
    df = pd.read_excel("附件2.xlsx",sheet_name="2023年的农作物种植情况")
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
    # print(promised)
    # print(money)
    # print(sum(money))
def main():
    area, area_dict, crop, crop_dict, cost = read_data()
    test(area, area_dict, crop, crop_dict, cost)
    solve(area, area_dict, crop, crop_dict, cost)


main()