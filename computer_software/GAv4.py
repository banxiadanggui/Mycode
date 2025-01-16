import math
import random
import json
import copy
import numpy as np
import matplotlib.pyplot as plt
#random.seed(a=100)
t=0
class GeneticAlgorism:
    def __init__(self,uav,obstacles,pop_size=100,mutationrate=1,generations=300,steps=5):
        #100 1 500 10超
        #100 1 100 5cao
        self.minlongitude=109.70
        self.maxlongitude=110.69
        self.minlatitude=19.0
        self.maxlatitude=20.0
        self.uav=uav
        self.obstacles=obstacles
        self.pop_size=pop_size
        self.mutationRate=mutationrate
        self.generations=generations
        self.steps=steps
        self.population=self.init_pop()
        self.fitnesslist=self.fitnesses()
        self.testlist=[]
    def init_pop(self):
        pool = [
        [
            {"step": j, "latitude": (random.uniform(self.maxlatitude, self.minlatitude) if j!=0 and j!=self.steps-1 else(self.uav["landingLatitude"] if j == self.steps-1 else self.uav["takeoffLatitude"])),
             "longitude": (random.uniform(self.maxlongitude, self.minlongitude) if j!=0 and j!=self.steps-1 else(self.uav["landingLongitude"] if j == self.steps-1 else self.uav["takeoffLongitude"])),
             "height": (random.uniform(self.uav["landingheight"], self.uav["takeoffheight"]) if j!=0 and j!=self.steps-1 else(self.uav["landingheight"] if j == self.steps-1 else self.uav["takeoffheight"]))
            } for j in range(self.steps)
        ]
        for _ in range(self.pop_size)
        ]
        return pool
    def haversine_distance(self,lat1, lon1, hei1, lat2, lon2, hei2):
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
    def checkObstacle(self,step1,step2):
        for obs in self.obstacles:
            linetopoint=float(np.divide((step2["latitude"]-step1["latitude"])*(obs["longitude"]-step1["longitude"])-(step2["longitude"]-step1["longitude"])*(obs["latitude"]-step1["latitude"]),((step2["latitude"]-step1["latitude"])**2+(step2["longitude"]-step1["longitude"])**2)**0.5))
            linetopoint=abs(linetopoint)
            if linetopoint<=obs["radius"]/110320:
                return True
        return False
    def selection(self):
        l=[i**0.5 for i in self.fitnesslist]
        copiedlist=copy.deepcopy(self.population)
        selectedpool=random.choices(copiedlist,weights=l,k=self.pop_size)
        return selectedpool
    def crossover(self,parent1,parent2):
        child=[]
        start=random.randint(1,self.steps-3)
        end=random.randint(start+1,self.steps-2)
        child=parent1[:start]+parent2[start:end]+parent1[end:]
        return child
    def mutate(self,path):
        a=path
        if random.random() <self.mutationRate:
            p=random.randint(1,len(path)-2)
            a[p]["latitude"]+=random.uniform(-0.1,0.1)
            a[p]["longitude"]+=random.uniform(-0.1,0.1)
            for p2 in range(1,len(path)-3):
                if self.checkObstacle(path[p2],path[p2+1]) == True:
                    a[p2]["latitude"]+=random.uniform(-0.1,0.1)
                    a[p2]["longitude"]+=random.uniform(-0.1,0.1)
            # a[p]["latitude"]+=(random.uniform(19.00,19.99)-a[p]["latitude"])
            # a[p]["longitude"]+=(random.uniform(109.7,110.7)-a[p]["longitude"])
        return a
    def fitness(self,path):
        total_distance=0
        for i in range(len(path)-1):
            if self.checkObstacle(path[i],path[i+1]) == True:
                total_distance+=self.haversine_distance(path[i]["latitude"],path[i]["longitude"],path[i]["height"],path[i+1]["latitude"],path[i+1]["longitude"],path[i+1]["height"])*(1000)
            else :
                total_distance+=self.haversine_distance(path[i]["latitude"],path[i]["longitude"],path[i]["height"],path[i+1]["latitude"],path[i+1]["longitude"],path[i+1]["height"])
        fitness=1/total_distance
        return fitness
    def fitnesses(self):
        List=[]
        for path in self.population:
            List.append(self.fitness(path))
        return List
    def testfitnesses(self,list):
        List=[]
        for path in list:
            List.append(self.fitness(path))
        return List
    def evolve_population(self):
        selected_population = self.selection()
        sorted_population = sorted(self.population, key=lambda x:self.fitness(x), reverse=True)
        elite_count = 20 
        next_generation = sorted_population[:elite_count]
        self.testlist=self.testfitnesses(next_generation)
        for i in range(elite_count, self.pop_size, 2):
            parent1, parent2 = selected_population[i % self.pop_size], selected_population[(i + 1) % self.pop_size]
            child1 = self.mutate(self.crossover(parent1, parent2))
            child2 = self.mutate(self.crossover(parent2, parent1))
            next_generation.append(child1)
            next_generation.append(child2)     
        self.testlist=self.testfitnesses(next_generation) 
        a=self.testlist 
        self.population = next_generation[:self.pop_size]
        self.fitnesslist=self.fitnesses()
    def write(self,index):
        with open ("record.json","a") as record:
            json.dump(index,record,indent = 4,ensure_ascii=False)
    def find_best_route(self):
        for _ in range(self.generations):
            self.evolve_population()
            best_route = max(self.population, key=lambda x:self.fitness(x))
            best_distance = 1 / self.fitness(best_route)
            # if best_distance<1.05*self.haversine_distance(self.uav["takeoffLatitude"],self.uav["takeoffLongitude"],self.uav["takeoffheight"],self.uav["landingLatitude"],self.uav["landingLongitude"],self.uav["landingheight"]):
            #     break
        print(best_distance)
        return best_route#, best_distance

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
            solver=GeneticAlgorism(uavs[i],obstacles)
            singleresult = {}
            singleresult['id'] = i
            singleresult['path'] = solver.find_best_route()
            reply["uavpath"].append(singleresult)
    else:
        print(flag)
        reply['msg'] = "server is ok!"  
    if t == 1: 
        x,y,xo,yo,so=[],[],[],[],[]
        for a in reply["uavpath"][0]["path"]:
            x.append(a["latitude"])
            y.append(a["longitude"])
        plt.plot(x,y)
        for obs in obstacles:
            xo.append(obs["latitude"])
            yo.append(obs["longitude"])
            so.append(obs["radius"]*0.2)
        plt.scatter(xo,yo,color='red',s=so)
        for i, (xi, yi) in enumerate(zip(x, y)):
            plt.text(xi, yi, str(i), fontsize=9, ha='right', va='bottom')
        plt.show()
        with open ("record2.json","w") as record:
            json.dump(reply,record,indent = 4,ensure_ascii=False) 
    return reply
def test():
    with open ("data.json","r") as input:
        data=json.load(input)
    processing(data)

if t==1:
    test()