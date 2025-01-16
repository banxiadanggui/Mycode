import random
import numpy as np

random.seed(0)
n=1000
def init(pop):
    L=list(range(n))
    Pool=[random.sample(L,n) for i in range(pop)]
    return Pool
def getConflict(queenList):
    conflict=0
    a=[0 for i in range(2*n-1)]
    b=[0 for i in range(2*n-1)]
    c=[0 for i in range(n)]
    for i in range(0,n):
        if a[queenList[i]+i] == 0:
           a[queenList[i]+i]=1
        else: 
            conflict+=1
            continue
        if b[queenList[i]-i+n-1] == 0:
            b[queenList[i]-i+n-1]=1
        else: 
            conflict+=1
            continue
        if c[queenList[i]] == 0:
            c[queenList[i]]=1
        else: 
            conflict+=1
    return conflict
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
            list[pos]=random.randint(0,n-1)
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
round=300
selectNum=50
mutationRate=0.3
parentPopulation=100
childrenPopulation=200
parentPool=init(parentPopulation)
for t in range(round):
    selectedPool=select(parentPool,parentPool,selectNum)
    childPool=crossOver(selectedPool,childrenPopulation)
    mutatedchildPool=mutation(childPool,mutationRate)
    parentPool=competation(mutatedchildPool,parentPool,parentPopulation)
    min=n
    for i in parentPool:
        if getConflict(i)<min:
            min=getConflict(i)
            minPool=i
    print(min)
    
    
#print(parentPool)
min=n
for i in parentPool:
    if getConflict(i)<min:
        min=getConflict(i)
        minPool=i
print(minPool,min)
##import cProfile
import pstats
##p=pstats.Stats("result")
##print_stats()
##p.strip_dirs().sort_stats("name").print_stats()
###