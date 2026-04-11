import torch 
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

print("--- Building the IA Brain ---")

#1. We define the class that contains the architecture of the web
#1 Мы определяем класс, содержащий архитектуру веб-сайта
class AMLModel(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(AMLModel, self).__init__()

        #First layer: Takes the 165 features and compresses the to 64 hidden "neurons"
        self.conv1 = GCNConv(num_features, 64)

        #Second layer: Takes the 64 hidden neurons and outputs the final result (the classes)
        self.conv2 = GCNConv(64, num_classes)
    def forward(self, x, edge_index):
        #Layer 1 + ReLu Activation Function (to learn non-linead patterns)
        x=self.conv1(x,edge_index)
        x=F.relu(x)

        #Layer 2(Final output)
        x = self.conv2(x, edge_index)

        #Return probabilities (using Log-Softmax, ideal for classification)
        return F.log_softmax(x, dim=1)

#2. Instantiate (create) the model in memory
#we Know from the previus step that we have 165 features
#We have 2 classes we want to predict (0=licit, 1=Illicit)
model = AMLModel(num_features=165, num_classes=2)
print("\nValidation - Model Architecture Created:")
print(model)