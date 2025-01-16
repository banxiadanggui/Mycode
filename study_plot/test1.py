import matplotlib.pyplot as plt
x=list(range(1,100))
y=[x_1**2 for x_1 in x]
plt.scatter(x,y,c='red',edgecolors='none',s=20)
plt.title("test1",fontsize=20)
plt.xlabel("time",fontsize=20)
plt.ylabel("speed",fontsize=20)
plt.tick_params(axis='both',labelsize=20)
plt.show()