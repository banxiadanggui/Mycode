from itertools import permutations
n=10
for queenList in permutations([i for i in range(0,n)]):
    flag=0
    a=[0 for i in range(2*n-1)]
    b=[0 for i in range(2*n-1)]
    for i in range(0,n-1):
        if a[queenList[i]+i] == 0:
            a[queenList[i]+i]=1
        else: 
            flag=1
            break
        if b[queenList[i]-i+n-1] == 0:
            b[queenList[i]-i+n-1]=1
        else: 
            flag=1
            break
    if flag == 0:
        print(queenList)    
        break
        
        
