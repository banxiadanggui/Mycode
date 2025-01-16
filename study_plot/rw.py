import matplotlib.pyplot as plt
from my_randomwalk import RandomWalk

while True:
    rw=RandomWalk()
    rw.fill_walk()
    plt.scatter(rw.x,rw.y,s=15)
    plt.show()
    keep=input("make another")
    if keep=='no':
        break