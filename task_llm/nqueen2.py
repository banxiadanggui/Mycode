import random
n=10000
def getConflict(queenList):
    conflict=0
    a=[0 for i in range(2*n-1)]
    b=[0 for i in range(2*n-1)]
    c=[0 for i in range(n)]
    for i in range(0,n-1):
        if a[queenList[i]+i] == 0:
           a[queenList[i]+i]=1
        else: 
            conflict+=1
        if b[queenList[i]-i+n-1] == 0:
            b[queenList[i]-i+n-1]=1
        else: 
            conflict+=1
        if c[queenList[i]] == 0:
            c[queenList[i]]=1
        else: 
            conflict+=1
    return conflict
def move(queenList):
    a=[0 for i in range(2*n-1)]
    b=[0 for i in range(2*n-1)]
    c=[0 for i in range(0,n)]
    for i in range(0,n-1):
        if a[queenList[i]+i] == 0:
           a[queenList[i]+i]=1
        else: 
            queenList[i]=random.randint(0,n-1)
        if b[queenList[i]-i+n-1] == 0:
            b[queenList[i]-i+n-1]=1
        else: 
            queenList[i]=random.randint(0,n-1)
        if c[queenList[i]] == 0:
            c[queenList[i]]=1
        else: 
            queenList[i]=random.randint(0,n-1)
    return getConflict(myqueenList),myqueenList
   
myqueenList=[]
for w in range (0,n):
    myqueenList[w]=random.randint(0,n-1)
nowConflict=getConflict(myqueenList)
t=0
max=3000
peaknumber=0
while(t<5000):
    [a,b]=move(myqueenList)
    if a<=nowConflict:
        myqueenList=b
        nowConflict=a
    else:
        peaknumber+=1
    if peaknumber>max:
        peaknumber=0
        for w in range (0,n):
            tmp=myqueenList[w]
            k=random.randint(0,n-1)
            while(k==tmp):
                k=random.randint(0,n-1)
            myqueenList[w]=k
    t+=1
print(myqueenList,nowConflict)
