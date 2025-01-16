import random
import numpy as np

##random.seed(0)
n=30#itemnum
ability=200
valueList=[random.randint(0,100)for _ in range(n)]
weightList=[random.randint(0,20)for _ in range(n)]
round=100
selectNum=50
mutationRate=0.3
parentPopulation=100
childrenPopulation=200
def init(n):
    Pool=[random.randint(0,1) for _ in range (n)]
    return Pool
def getConflict(List):
    value=0
    weight=0
    for i in range(n):
        value+=List[i]*valueList[i]
        weight+=List[i]*weightList[i]
    if weight>ability:
        return -1
    return value
def select(Pool,Pool2,selectNum):
    weight=[n-getConflict(i) for i in Pool]
    selectedPool=random.choices(Pool,weights=weight,k=int(selectNum/2))
    
    conflictList=[getConflict(i) for i in Pool2]
    sorted_cList=sorted(conflictList)
    newpool = [Pool2[conflictList.index(sorted_cList[i])] for i in range(selectNum-int(selectNum/2))]
    return selectedPool+newpool
def crossOver(Pool,childrenPopulation):
    childPool=[]
    for i in range(int(childrenPopulation/2)):
        a=random.choice(Pool)
        b=random.choice(Pool)
        cutPos=random.randint(0,n-1)
        child1=a[0:cutPos]+b[cutPos:n]
        child2=b[0:cutPos]+a[cutPos:n]
        childPool.append(child1)
        childPool.append(child2)
    return childPool
def mutation(Pool,mutationRate):
    for list in Pool:
        for i in range(int(len(list)*mutationRate)):
            pos=random.randint(0,n-1)
            list[pos]=random.randint(0,1)
    return Pool
def competation(Pool,Pool2,parentPopulation):
    weight=[pow(n-getConflict(i),2) for i in Pool]
    parentPool=random.choices(Pool,weights=weight,k=int(parentPopulation/2))
    
    conflictList=[getConflict(i) for i in Pool2]
    sorted_cList=sorted(conflictList)
    newpool = [Pool2[conflictList.index(sorted_cList[i])] for i in range(parentPopulation-int(parentPopulation/2))]
    ##conf=np.vectorize(getConflict)
    ##indices=np.argsort(conf(Pool2))
    ##newpool=np.array(Pool2)[indices].tolist()
    return parentPool+newpool##[0:(parentPopulation-int(parentPopulation/2)-1)]

dna=init(n)
bestdna=dna
for t in range(round):
    value=getConflict(dna)
    flag=0
    for i in range(0,n):
        moved_dna=dna
        moved_dna[i]=1-moved_dna[i]
        if getConflict(moved_dna)>value:
            dna=moved_dna
            break
        else:
            flag+=1
    if flag>=n/2:
        if getConflict(dna)>getConflict(bestdna):
            bestdna=dna
        for i in range(n):
            dna[i]=abs(dna[i]-random.randint(0,1))
print("value",valueList)
print("weight",weightList)   
print(bestdna,getConflict(bestdna))