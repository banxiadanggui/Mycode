import torch
import numpy as np
A=[0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,1]
B=[1,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,0]
# Training data for XOR function
#list L=[[0 for i in range(26) if _!=i] for _ in range(26)]
X = torch.tensor([A,B], dtype=torch.float32)
y = torch.tensor([[0],[1]], dtype=torch.float32)

# Neural network model with one hidden layer
model = torch.nn.Sequential(
    torch.nn.Linear(25, 100),    # Hidden layer with 2 neurons
    # Output layer
    torch.nn.Sigmoid(),
    torch.nn.Linear(100,1),    # Hidden layer with 2 neurons
    # Output layer
    torch.nn.Sigmoid()
)

# Loss function and optimizer
criterion = torch.nn.BCELoss()
#criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

for epoch in range(10000):
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

# Testing
with torch.no_grad():
    print(model(X).round())  # Rounded output to 0 or 1
    


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