import numpy as np
import pandas as pd
from pyomo import *

def read_data():
    df = pd.read_excel("附件1.xlsx", sheet_name="乡村种植的农作物")
    one_season_df = df[(df['作物类型'] == "粮食")|(df['作物类型'] == "粮食（豆类）")]
    one_season_df = one_season_df[one_season_df['作物编号'] <= 15]
    two_season_df = df[(df['作物类型'] == "蔬菜")|(df['作物类型'] == "蔬菜（豆类）")]
    two_season_df = two_season_df[two_season_df['作物编号'] <= 34]
    carrot_df = df[(df['作物类型'] == "蔬菜")]
    carrot_df = carrot_df[carrot_df['作物编号'] >= 35]
    mushroom_df = df[(df['作物类型'] == "食用菌")]
    #print(one_season_df['作物名称'])
    #print(two_season_df['作物名称'])
    #print(carrot_df['作物名称'])
    #print(mushroom_df['作物名称'])

    farm_df = pd.read_excel("附件1.xlsx", sheet_name="乡村的现有耕地")
    farm_df = pd.DataFrame(farm_df[(farm_df['地块类型'] == '平旱地') | (farm_df['地块类型'] == '梯田') | (farm_df['地块类型'] == '山坡地')])
    print(farm_df)
    return one_season_df,farm_df

def only_one_season(df: pd.DataFrame, farm_df: pd.DataFrame):
    cost = {}
    id_to_name = {i : df[df['作物编号'] == i]['作物名称'].values[0] for i in df['作物编号']}
    promissing_sold = {i:0 for i in df['作物编号']}
    promissing_sold_three = {i: [] for i in df['作物编号']}
    # print(promissing_sold)
    # print(df[df['作物编号'] == 1]['作物名称'].values)
    # print(id_to_name)
    price_df = pd.read_excel("附件2.xlsx", sheet_name="2023年统计的相关数据")
    price_df = pd.DataFrame(price_df[(price_df['地块类型'] == '平旱地') | (price_df['地块类型'] == '梯田') | (price_df['地块类型'] == '山坡地')])
    # print(price_df)
    # print(len(price_df))
    for i in range(len(price_df)):
        cost[price_df.loc[i]['作物编号']] = int(price_df.loc[i]['种植成本/(元/亩)'])
        # print(cost[price_df.loc[i]['作物编号']])
        promissing_sold_three[price_df.loc[i]['作物编号']].append(int(price_df.loc[i]['亩产量/斤']))

    put_df = pd.read_excel("附件2.xlsx", sheet_name="2023年的农作物种植情况")
    # print(put_df[put_df['种植地块'].str.contains('A')])
    trans_dict = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    # print(put_df.loc[25])
    for i in range(26):
        for key in trans_dict.keys():
            if key in put_df.loc[i]['种植地块']:
                promissing_sold[put_df.loc[i]['作物编号']] += promissing_sold_three[put_df.loc[i]['作物编号']][trans_dict[key]] * put_df.loc[i]['种植面积/亩']

    print(promissing_sold)
def main():
    df, farm_df = read_data()
    only_one_season(df,farm_df)




main()