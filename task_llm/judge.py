import torch
vocab=["aircraft","ronaldo","messi","paper","study","work"]
          
synpairs=[("ronaldo","messi"),("paper","study"),("study","work"),
              ("paper","work")]
N=6
X=[[] for _ in range(N*N)]
Y=[]

for i in range(6):
    for j in range():
        X.append()
        if (i,j) in synpairs:
            Y.append([0,1])
        else:
            Y.append([1,0])

X_in=torch.tensor(X)
Y_in=torch.tensor(Y)

model = torch.nn.Sequential(
    torch.nn.Linear(2, 10),  # Hidden layer with 2 neurons
    torch.nn.Sigmoid(),
    torch.nn.Linear(10, 1),  # Output layer
    torch.nn.Sigmoid()
)

# Loss function and optimizer
criterion = torch.nn.BCELoss()
# criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# Training loop
for epoch in range(10000):
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 100 == 0:  # Print every 1000 epochs
        print(f'Epoch [{epoch + 1}/10000], Loss: {loss.item():.4f}')

for name, param in model.named_parameters():
    if param.requires_grad:
        print(f'{name}: {param.data}')

# Testing
with torch.no_grad():
    print(model(X).round())  # Rounded output to 0 or 1
