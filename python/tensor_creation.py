import pandas as pd
import torch
from torch_geometric.data import Data

df_features = pd.read_csv("elliptic_txs_features.csv", header =None)
df_features.rename(columns={0:'txId', 1:'time_step'}, inplace=True)

df_classes = pd.read_csv("elliptic_txs_classes.csv")
df_edge = pd.read_csv("elliptic_txs_edgelist.csv")

# 2. Extraer todos los IDs únicos de las características
nodos_unicos = df_features['txId'].unique()

print(f"Всего найдено узлов {len(nodos_unicos)}")

# 3. Crear el diccionario de mapeo {ID_Original : Nuevo_Indice_PyTorch}
# La función 'enumerate' cuenta automáticamente 0, 1, 2, 3...#
#Создать отображение реалного идентификатора
node_to_idx = { node_id:index for index, node_id in enumerate(nodos_unicos)}
print("\n Validation - sample of dictionary")

muestra = {k:node_to_idx[k] for k in list(node_to_idx)[:5]}
for real, pytorch in muestra.items():
    print(f"ID Real:{real} --> Indice IA: {pytorch}")

df_edge['txId1'] = df_edge['txId1'].map(node_to_idx)
df_edge['txId2'] = df_edge['txId2'].map(node_to_idx)
df_edge = df_edge.dropna() #Se actualiza la variable asi misma usando dropna
                            #Si encuentra un espacio vacio(NaN). provocado por un ID que esta en el diccionario
                            #borra esa fila completa

#6. Unir caracteristicas y clases
df_nodos = pd.merge(df_features, df_classes, on="txId", how="left")

# 7 Translate the text classes into mathematics
class_mapping = {'1': 1, '2':0, 'unknown': 2}
df_nodos['class'] = df_nodos['class'].astype(str).map(class_mapping)

#8 tensor
x_features = df_nodos.drop(columns=['txId', 'time_step', 'class']).values
x_tensor = torch.tensor(x_features, dtype=torch.float)

y_tensor = torch.tensor(df_nodos['class'].values, dtype=torch.long)

edge_index_tensor = torch.tensor(df_edge[['txId1', 'txId2']].values, dtype=torch.long).t().contiguous()

graph_data = Data(x=x_tensor, edge_index=edge_index_tensor, y=y_tensor)
print("\n--- RESULTADO FINAL: EL GRAFO VECTORIZADO ---")
print(graph_data)  