import math
import json
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
        with open ('data.json','w',encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
        # 在这里处理数据并执行相应的操作
        print("Received data:", data)
        response_data = processing(data)
        with open ('record3.json','w',encoding='utf-8') as f:
            json.dump(receive_data,f,indent=4,ensure_ascii=False)
        # 将响应数据转换为 JSON 格式并返回
        return jsonify(response_data), 200
    except Exception as e:
        print(e,'failed')
        return jsonify({"error": str(e)}), 500

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
            obstacle.append([el["latitude"], el["longitude"], el["radius"]])
            obstacle.append(obs)
        reply["uavpath"] = []
        for i in range(len(uavs)):
            singleresult = {}
            singleresult['id'] = i
            singleresult['path'] = []
            verlocity = 0.2
            numberofpoint = max(int(haversine_distance(uavs[i]["takeoffLatitude"], uavs[i]["takeoffLongitude"],
                                                   uavs[i]["landingLatitude"], uavs[i]["landingLongitude"]) / verlocity),2)
            lats = np.linspace(uavs[i]["takeoffLatitude"], uavs[i]["landingLatitude"], numberofpoint)
            lons = np.linspace(uavs[i]["takeoffLongitude"], uavs[i]["landingLongitude"], numberofpoint)
            heights = np.linspace(uavs[i]["takeoffheight"], uavs[i]["landingheight"], numberofpoint)
            k = 0
            if i == 0:
                for _ in range(5):
                    path1 = {}
                    path1["step"] = k
                    path1["latitude"] = uavs[i]["takeoffLatitude"]
                    path1["longitude"] = uavs[i]["takeoffLongitude"],
                    path1["height"] = uavs[i]["takeoffheight"]
                    singleresult['path'].append(path1)
                    k = k + 1
            for step in range(numberofpoint):
                path1 = {}
                path1["step"] = step + k
                path1["latitude"] = lats[step] 
                path1["longitude"] = lons[step]
                path1["height"] = heights[step]
                singleresult['path'].append(path1)
            reply["uavpath"].append(singleresult)
    else:
        print(flag)
        reply['msg'] = "server is ok!"

    return reply

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9111, debug=True)
