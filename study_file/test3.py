import torch
import pandas as pd
import matplotlib.pyplot as plt

# 设置CPU生成随机数的种子，方便下次复现实验结果。
torch.manual_seed(9)
df=pd.read_excel("激光标定数据.xlsx")
x1=df["实际距离2"]
x1_list=x1.values.tolist()
x1_list_thousand=[xx for xx in x1_list]
x=torch.tensor(x1_list_thousand, dtype=torch.float32)
y1=df["AD转换后的输出2"]
y1_list=y1.values.tolist()
y1_list_thousand=[yy for yy in y1_list]
y=torch.tensor(y1_list_thousand, dtype=torch.float32)
# 设置学习率
lr = 0.005

# 创建训练数据
print(type(x),type(y))
print(x)
print(y)

# 随机参数w和b
w = torch.randn((1), requires_grad=True)
b = torch.randn((1), requires_grad=True)

for i in range(2000):
    # 前向传播
    # torch.mul作element-wise的矩阵点乘，维数不限，可以矩阵乘标量
    # 当a, b维度不一致时，会自动填充到相同维度相点乘。
    wx = torch.mul(w, x)
    # 支持广播相加
    y_pred = torch.add(wx, b)
    
    # 计算MSE Loss
    # 反向传播， ✖2分之一是为了方便求导
    loss = abs(y - y_pred).mean()
    
    # 反向传播, 计算当前梯度
    loss.backward()
    
    b.data.sub_(lr * b.grad)
    w.data.sub_(lr * w.grad)
    
     # 绘图
    if i % 10 == 0:
        plt.cla()   
        plt.scatter(x.data.numpy(), y.data.numpy())
        plt.plot(x.data.numpy(), y_pred.data.numpy(), 'r-', lw=5)
        plt.text(2, 20, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 20, 'color':  'red'})
        plt.title("Iteration: {}\nw: {} b: {}".format(i, w.data.numpy(), b.data.numpy()))
        plt.pause(0.3)

        if loss.data.numpy() < 1:
            print(w.data.numpy(),b.data.numpy())
            break
plt.show()
