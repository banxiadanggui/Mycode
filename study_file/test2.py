# ...[省略前面的代码]...
import torch
import pandas as pd
import matplotlib.pyplot as plt

# 设置CPU生成随机数的种子，方便下次复现实验结果。
torch.manual_seed(9)
df=pd.read_excel("激光标定数据.xlsx")
x1=df["实际距离2"]
x1_list=x1.values.tolist()
x1_list_thousand=[xx/1000. for xx in x1_list]
x=torch.tensor(x1_list_thousand, dtype=torch.float32)
y1=df["AD转换后的输出2"]
y1_list=y1.values.tolist()
y1_list_thousand=[yy/1000. for yy in y1_list]
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
    wx = w * x
    y_pred = wx + b / 1000  # 确保b是张量并进行了相应的转换

    # 计算MSE Loss
    loss = (y - y_pred).pow(2).mean()

    # 反向传播
    loss.backward()

    # 更新参数
    with torch.no_grad():
        b -= lr * b.grad
        w -= lr * w.grad
    b.grad.zero_()
    w.grad.zero_()

    # 绘图
    if i % 10 == 0:
        plt.cla()
        plt.scatter(x.detach().numpy(), y.detach().numpy())
        plt.plot(x.detach().numpy(), y_pred.detach().numpy(), 'r-', lw=5)
        plt.text(2, 20, f'Loss={loss.item():.4f}', fontdict={'size': 20, 'color': 'red'})
        plt.title(f"Iteration: {i}, w: {w.detach().numpy()}, b: {b.detach().numpy()}")
        plt.pause(0.3)

        # 确保break在plt.pause之后
        if loss.item() < 1:
            print(w.detach().numpy(), b.detach().numpy())
            break

plt.show()