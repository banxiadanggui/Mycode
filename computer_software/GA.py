import math
import random
import json
import numpy as np
random.seed(0)
def haversine_distance(lat1, lon1, hei1, lat2, lon2, hei2):
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine 公式计算距离
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dhei = hei1 - hei2
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球半径（单位：公里）
    # 计算距离
    distance = math.sqrt((c * r)**2+dhei**2)
    return distance
def pointToLine(point,linePoint1,linePoint2):
    lat1=linePoint1["latitude"]
    lat2=linePoint2["latitude"]
    lat3=point["latitude"]
    lon1=linePoint1["longitude"]
    lon2=linePoint2["longitude"]
    lon3=point["longitude"]
    hei1=linePoint1["height"]
    hei2=linePoint2["height"]
    hei3=point["height"]
    dxline=lat2-lat1
    dyline=lon2-lon1
    dzline=hei2-hei1
    dxpoint=lat3-lat1
    dypoint=lon3-lon1
    dzpoint=hei3-hei1
    lenline_sqrt=dxline**2+dyline**2+dzline**2
    if lenline_sqrt == 0:
        return haversine_distance(lat1,lon2,hei1,lat3,lon3,hei3)
    t=(dxline*dxpoint+dyline*dypoint+dzline*dzpoint)/lenline_sqrt
    if t<0:
        t=0
    elif t>1:
        t=1
    pointx=lat1+t*dxline
    pointy=lon1+t*dyline
    pointz=hei1+t*dzline
    return haversine_distance(pointx,pointy,pointz,lat3,lon3,hei3)
def checkObstacle(step1,step2,obstacle):
    distance=pointToLine(obstacle,step1,step2)
    if distance < obstacle["radius"]:
        return True
    else :
        return False
def init(uva,n,population):
    Pool=[]
    for i in range(population):
        path=[]
        for j in range(n):
            pathStep={}
            pathStep["step"]=j
            if j == 0:
                pathStep["latitude"]=uva["takeoffLatitude"]
                pathStep["longitude"]=uva["takeoffLongitude"]
                pathStep["height"]=uva["takeoffheight"]
            elif j==n-1:
                pathStep["latitude"]=uva["landingLatitude"]
                pathStep["longitude"]=uva["landingLongitude"]
                pathStep["height"]=uva["landingheight"]
            else:
                pathStep["latitude"]=random.uniform(uva["landingLatitude"],uva["takeoffLatitude"])
                pathStep["longitude"]=random.uniform(uva["landingLongitude"],uva["takeoffLongitude"])
                pathStep["height"]=random.uniform(uva["landingheight"],uva["takeoffheight"])
            path.append(pathStep)        
        Pool.append(path)
    return Pool
def evalue(path,obstacles):
    #errorWeight=100000
    value=0
    for i in range(len(path)-1):
        for obstacle in obstacles:
            if checkObstacle(path[i],path[i+1],obstacle):
                value=0
            else :
                value+=haversine_distance(path[i]["latitude"],path[i]["longitude"],path[i]["height"],path[i+1]["latitude"],path[i+1]["longitude"],path[i+1]["height"])
    return (value+1)/10000
def select(Pool,selectNum,obstacles):
    weight=[evalue(i,obstacles) for i in Pool]
    selectedPool=random.choices(Pool,weights=weight,k=int(selectNum/2))
    sortedList=sorted(weight)
    newpool = [Pool[weight.index(sortedList[i])] for i in range(selectNum-int(selectNum/2))]
    return selectedPool+newpool
def crossOver(Pool,childrenPopulation):
    childPool=[]
    for i in range(int(childrenPopulation/2)):
        a=random.choice(Pool)
        b=random.choice(Pool)
        cutPos=random.randint(0,len(a)-1)
        child1=a[:cutPos]+b[cutPos:]
        child2=b[:cutPos]+a[cutPos:]
        childPool.append(child1)
        childPool.append(child2)
    return childPool
def mutation(Pool,mutationRate):
    for path in Pool:
        for _ in range(int(len(path)*mutationRate)):
            path[_]["latitude"]=random.uniform(19.00,19.99)
            path[_]["longitude"]=random.uniform(109.7,110.7)
    return Pool

def competation(Pool,parentPool,parentPopulation,obstacles):
    weight=[evalue(i,obstacles) for i in Pool]
    selectedPool=random.choices(Pool,weights=weight,k=int(parentPopulation/2))
    weight2=[evalue(i,obstacles) for i in parentPool]
    sortedList=sorted(weight2)
    newpool = [parentPool[weight.index(sortedList[i])] for i in range(parentPopulation-int(parentPopulation/2))]
    return selectedPool+newpool

def GeneticAlgorism(uav,obstacles,n):
    maxlen=100000
    round=5
    selectNum=5
    mutationRate=0.3
    parentPopulation=10
    childrenPopulation=20
    minPath=[]
    parentPool=init(uav,n,parentPopulation)
    with open ("record.json","w") as record:
        json.dump(uav,record,indent = 4,ensure_ascii=False)
    with open ("record.json","a") as record:
        json.dump(parentPool,record,indent = 4,ensure_ascii=False)
    for roundnumber in range(round):
        selectedPool=select(parentPool,selectNum,obstacles)
        childPool=crossOver(selectedPool,childrenPopulation)
        mutatedchildPool=mutation(childPool,mutationRate)
        parentPool=competation(mutatedchildPool,parentPool,parentPopulation,obstacles)
        if (roundnumber+1)%2 == 0:
            minlen=maxlen
            for i in parentPool:
                if evalue(i,obstacles)<minlen:
                    minlen=evalue(i,obstacles)
                    minPath=i
            print("roundnum:",roundnumber,"len",minlen)
    return minPath

def processing(request):
    flag = request["flag"]
    reply = {}
    if flag == 1:
        # 单独执行路径规划任务
        print("################单独执行路径规划任务#################")
        uavs = []
        obstacles = []
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
            obstacle = {}
            obstacle["id"] = el["id"]
            obstacle["latitude"] = float(el["latitude"])
            obstacle["longitude"] =float(el["longitude"])
            obstacle["radius"] = float(el["radius"])
            obstacle["height"] = 0
            #obstacles.append([el["latitude"], el["longitude"], el["radius"]])
            obstacles.append(obstacle)
        reply["uavpath"] = []
        for i in range(len(uavs)):
            verlocity = 0.2
            step_num = max(int(haversine_distance(uavs[i]["takeoffLatitude"], uavs[i]["takeoffLongitude"],uavs[i]["takeoffheight"],uavs[i]["landingLatitude"], uavs[i]["landingLongitude"],uavs[i]["landingheight"]) / verlocity),2)
            singleresult = {}
            singleresult['id'] = i
            singleresult['path'] = GeneticAlgorism(uavs[i],obstacles,step_num)
            reply["uavpath"].append(singleresult)
    else:
        print(flag)
        reply['msg'] = "server is ok!"

    return reply
def test():
    with open ("data.json","r") as input:
        data=json.load(input)
    processing(data)
test()