import math
import random

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def haversine_distance(lat1, lon1, lat2, lon2):
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine 公式计算距离
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球半径（单位：公里）

    # 计算距离
    distance = c * r
    return distance


@app.route("/", methods=['POST'])
def receive_data():
    try:
        # 获取前端发送的 JSON 数据
        data = request.get_json()

        # 在这里处理数据并执行相应的操作
        # 这里只是一个示例，你可以根据自己的需求来处理数据
        print("Received data:", data)
        response_data = processing(data)

        # 将响应数据转换为 JSON 格式并返回
        return jsonify(response_data), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
def check_collision(temp,qrand, obstacle,target):
    """
    求路径到障碍物的距离 小于半径即为碰撞
    """
    for obs in obstacle:


        distance_to_obs =point_to_line_segment_distance(temp,qrand,obs)
        if distance_to_obs <(obs["radius"]+100.0)/1000:  # 100参数为防止接近障碍物太近,同时这里不完善的地方在于当飞机正面为障碍物时很难规划下一步路径
            return True

    return False



def point_to_line_segment_distance(temp, qrand, obs):
    """
    计算点 obs 到线段 temp-qrand 的最短距离。
    temp 和 qrand 是线段的两端点，obs 是待计算距离的点。
    所有输入参数为 [纬度, 经度] 格式。
    """
    # 提取线段端点和点的坐标
    lat1, lon1,a = temp
    lat2, lon2,b = qrand
    lat3=obs["latitude"]
    lon3=obs["longitude"]


    dx1 = lon2 - lon1  # 向量 AB 的 x 分量
    dy1 = lat2 - lat1  # 向量 AB 的 y 分量
    dx2 = lon3 - lon1  # 向量 AC 的 x 分量
    dy2 = lat3 - lat1  # 向量 AC 的 y 分量

    # 计算向量 AB 的平方长度
    length_sq = dx1 ** 2 + dy1 ** 2

    if length_sq == 0:  # 线段退化成一个点
        return haversine_distance(lat1, lon1, lat3, lon3)

    # 计算点到线段的投影比例 t
    t = (dx1 * dx2 + dy1 * dy2) / length_sq

    # 如果投影点在 [0, 1] 之间，则投影点在线段上
    if t < 0:
        t = 0
    elif t > 1:
        t = 1

    # 投影点的坐标
    proj_lat = lat1 + t * dy1
    proj_lon = lon1 + t * dx1

    # 计算投影点到点 obs 的距离
    return haversine_distance(lat3, lon3, proj_lat, proj_lon)

def processing(request):
    flag = request["flag"]
    reply = {}
    if flag == 1:
        # 单独执行路径规划任务
        print("################单独执行路径规划任务#################")
        uavs = []
        obstacle = []
        for el in request["uav_arr"]:
            uav = {}
            uav["id"] = el["id"]
            uav["takeoffLatitude"] = float(el["takeoffLatitude"])
            uav["takeoffLongitude"] = float(el["takeoffLongitude"])
            uav["takeoffheight"] = float(el["takeoffheight"])
            uav["landingLatitude"] = float(el["landingLatitude"])
            uav["landingLongitude"] = float(el["landingLongitude"])
            uav["landingheight"] = float(el["landingheight"])
            uavs.append(uav)
        for el in request["obs_arr"]:
            obs = {}
            obs["id"] = el["id"]
            obs["latitude"] = float(el["latitude"])
            obs["longitude"] =float(el["longitude"])
            obs["radius"] = float(el["radius"])
            obstacle.append(obs)
            # 执行路径规划并生成无人机的路径
        reply["uavpath"] = []
        for i in range(len(uavs)):
            singleresult = {}
            singleresult['id'] = i
            singleresult['path'] = []
            verlocity = 0.2
            numberofpoint =400


            k = 0
            step = 0

            for _ in range(5):# 停留5秒
                    path1 = {}
                    path1["step"] = k
                    path1["latitude"] = uavs[i]["takeoffLatitude"]
                    path1["longitude"] = uavs[i]["takeoffLongitude"],
                    path1["height"] = uavs[i]["takeoffheight"]
                    singleresult['path'].append(path1)
                    k = k + 1
            temp = [uavs[i]["takeoffLatitude"],uavs[i]["takeoffLongitude"],uavs[i]["takeoffheight"]]
            target=[uavs[i]["landingLatitude"],uavs[i]["landingLongitude"],uavs[i]["landingheight"]]
            for _ in range(numberofpoint):
                path1 = {}
                qrand = [random.uniform(min(temp[0], uavs[i]["landingLatitude"]),  max(temp[0],uavs[i]["landingLatitude"])),
                         random.uniform(min(temp[1],uavs[i]["landingLongitude"]),max(temp[1],uavs[i]["landingLongitude"])),
                         random.uniform(min(temp[2],uavs[i]["landingheight"]), max(temp[2],uavs[i]["landingheight"]))]
                if not check_collision(temp,qrand,obstacle,target):# 路径不经过障碍物且有一段距离
                  temp=[qrand[0],qrand[1],qrand[2]]# 更新最新路径点
                  path1["step"] = step + k
                  step=step+1
                  path1["latitude"] =qrand[0]
                  path1["longitude"] =qrand[1]
                  path1["height"] =qrand[2]
                  singleresult['path'].append(path1)
                  reply["uavpath"].append(singleresult)
                  if  haversine_distance(qrand[0],qrand[1],uavs[i]["landingLatitude"],uavs[i]["landingLongitude"])<2:
                      print(f"无人机编号{i}成功到达终点")
                      break


    else:
        reply['msg'] = "server is ok!"

    return reply


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9111, debug=True)
