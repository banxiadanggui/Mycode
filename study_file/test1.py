import pandas as pd
df=pd.read_excel("激光标定数据.xlsx")
a=0.682
b=-769.504
x=df["测试输入"]
y=df["测试输出"]
mse=sum((yy-(a*xx+b))**2 for xx,yy in zip(x,y))/len(x)
print(mse)