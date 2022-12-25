# Import necessary libraries and modules
import torch
import torchvision
from torchvision import datasets, transforms

# Define hyperparameters
num_classes = 10
learning_rate = 0.001
num_epochs = 10

# Load and transform the dataset
train_dataset = datasets.MNIST(root='./data', train=True, transform=transforms.ToTensor())
test_dataset = datasets.MNIST(root='./data', train=False, transform=transforms.ToTensor())

# Define the network architecture
class ConvNet(torch.nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = torch.nn.Linear(7*7*32, num_classes)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

# Initialize the network and specify the loss function and optimization algorithm
model = ConvNet()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the network
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_dataset):
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)