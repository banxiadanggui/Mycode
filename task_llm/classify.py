import torch
import numpy as np
import matplotlib.pyplot as plt
#tensorboard --logdir=./tensorboard --logdir=./
N = 100 # number of points per class
D = 2 # dimensionality
K = 5 # number of classes
X_train = np.zeros((N*K,D)) # data matrix (each row = single example)
y_train = np.zeros(N*K, dtype='uint8') # class labels
for j in range(K):
  ix = range(N*j,N*(j+1))
  r = np.linspace(0.0,1,N) # radius
  t = np.linspace(j*4,(j+1)*4,N) + np.random.randn(N)*0.2 # theta
  X_train[ix] = np.c_[r*np.sin(t), r*np.cos(t)]
  y_train[ix] = j

Input=[[a,b] for a,b in X_train]
output=[[0 for i in range(5)]for j in y_train]
for i in range(len(y_train)):
    output[i][y_train[i]]=1
#print(Input)
#print(output)
# Training data for XOR function
X = torch.tensor(Input, dtype=torch.float32)
y = torch.tensor(output, dtype=torch.float32)

# Neural network model with one hidden layer
model = torch.nn.Sequential(
    torch.nn.Linear(2, 5),    # Hidden layer with 2 neurons
    torch.nn.Sigmoid(),
    torch.nn.Linear(5,5),    
    torch.nn.Sigmoid(),
    torch.nn.Linear(5,5),    
    torch.nn.Sigmoid()
)

# Loss function and optimizer
#criterion = torch.nn.BCELoss()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=10)

# Training loop
for epoch in range(15000):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 100 == 0:  # Print every 1000 epochs
        print(f'Epoch [{epoch+1}/10000], Loss: {loss.item():.4f}')

for name, param in model.named_parameters():
    if param.requires_grad:
        print(f'{name}: {param.data}')


# model.eval()
# output=model(input)
# plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=40, cmap=plt.cm.Spectral)
# plt.show()

# Testing
with torch.no_grad():
    print(model(X).round())  # Rounded output to 0 or 1
    N_test=30
    X_test=np.zeros((N_test*N_test,D))
    Y_test=np.zeros(N_test*N_test)
    X_array=np.linspace(-1.0,1.0,N_test)
    for n in range(N_test):
        for m in range(N_test):
            X_test[n*N_test+m]=np.c_[X_array[n],X_array[m]]
    Input_test=torch.tensor(X_test, dtype=torch.float32)
    Output_test=torch.tensor(Y_test,dtype=torch.float32)
    Output_test=model(Input_test)
    for i in range(N_test*N_test):
        Y_test[i]=5
        for j in range(0,5):
            if(Output_test[i][j]>0.5):
                Y_test[i]=j
                break
        #Y_test[i]=min(Output_test[i][0]*1+Output_test[i][1]*2+Output_test[i][2]*3+Output_test[i][3]*4+Output_test[i][4]*5,5)
        #print(Y_test)
    plt.scatter(Input_test[:, 0], Input_test[:, 1],c=Y_test, s=40, cmap=plt.cm.Spectral)
    plt.show()
    
    


# # Forward pass manually to capture activations
# with torch.no_grad():
#     # Input layer
#     input_layer = X
#     print("Input to the network:")
#     print(input_layer)

#     # Hidden layer 1: Linear + Sigmoid
#     hidden_layer_input = model[0](input_layer)  # First Linear Layer
#     hidden_layer_output = model[1](hidden_layer_input)  # Sigmoid Activation
#     print("\nHidden layer activations (after Sigmoid):")
#     print(hidden_layer_output.round(decimals=2))

#     # Output layer: Linear + Sigmoid
#     output_layer_input = model[2](hidden_layer_output)  # Second Linear Layer
#     output_layer_output = model[3](output_layer_input)  # Sigmoid Activation
#     print("\nOutput layer activations (after Sigmoid):")
#     print(output_layer_output.round(decimals=2))

#     # Rounded output for prediction
#     print("\nPredicted outputs (rounded):")
#     print(output_layer_output.round())