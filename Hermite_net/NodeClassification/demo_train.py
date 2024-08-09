import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torch
import torchvision.transforms as transforms
from Hermite_propogation import Legendre_prop  # Assuming your model is defined in legendre_net.py
import matplotlib.pyplot as plt

transform = transforms.Compose([
    transforms.ToTensor(),  # Convert PIL Image to tensor
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize image data
])

# Load CIFAR-10 dataset for training
train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                               download=True, transform=transform)

# Load CIFAR-10 dataset for testing
test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                              download=True, transform=transform)

# Define DataLoader for training dataset
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64,
                                           shuffle=True, num_workers=2)

# Define DataLoader for testing dataset
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64,
                                          shuffle=False, num_workers=2)

# Define your LegendreNet model
model = Legendre_prop(K=3)  # Initialize your LegendreNet model

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
train_losses = []


if __name__ == '__main__':
    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0.0
        for data in train_loader:
            optimizer.zero_grad()
            out = model(data.x, data.edge_index)  # Forward pass
            loss = criterion(out, data.y)  # Compute loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update parameters
            epoch_loss += loss.item() * data.num_graphs

        epoch_loss /= len(train_loader.dataset)
        train_losses.append(epoch_loss)
        print(f"Epoch {epoch + 1}, Train Loss: {epoch_loss:.4f}")

    # Test loop
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for data in test_loader:
            out = model(data.x, data.edge_index)
            loss = criterion(out, data.y)
            test_loss += loss.item() * data.num_graphs
            _, predicted = torch.max(out, 1)
            total += data.y.size(0)
            correct += (predicted == data.y).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100 * correct / total
    print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {accuracy:.2f}%")

    # Visualize the loss over epochs
    plt.plot(train_losses, label='Train Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss over Epochs')
    plt.legend()
    plt.show()

