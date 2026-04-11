import pandas as pd
import torch
from torch_geometric.data import Data

df_features = pd.read_csv("elliptic_txs_features.csv", header =None)
df_features.rename(columns={0:'txId', 1:'time_step'}, inplace=True)

df_classes = pd.read_csv("elliptic_txs_classes.csv")
df_edge = pd.read_csv("elliptic_txs_edgelist.csv")

# 2. Extraer todos los IDs únicos de las características
nodos_unicos = df_features['txId'].unique()
print(f"Total de nodos únicos encontrados: {len(nodos_unicos)}")

# 3. Crear el diccionario de mapeo {ID_Original : Nuevo_Indice_PyTorch}
# La función 'enumerate' cuenta automáticamente 0, 1, 2, 3...

node_to_idx = {node_id: index for index, node_id in enumerate(nodos_unicos)}

# 4. Validar mostrando los primeros 5 mapeos

print("\n Validación - Muestra del diccionario (ID Real -> Índice PyTorch):")
# Tomamos solo los primeros 5 elementos para imprimir
muestra = {k:node_to_idx[k] for k in list(node_to_idx)[:5]}
for real, pytorch in muestra.items():
    print(f"ID Real:{real} --> Indice IA: {pytorch}")

df_nodos = pd.merge(df_features, df_classes, on= "txId", how="left")

#Convert the label of the string class to int and after to dictionary
class_mapping = {'1':1, '2':0, 'unknown': 2}
df_nodos['class'] = df_nodos['class'].astype(str).map(class_mapping)

print("Validacion - Primeras 3 clases traducidas:")
print(df_nodos[['txId', 'class']].head(3))

print("\n--- PASO 4: CREACION DE LOS TENSORES DE PYTORCH ---")

x_features = df_nodos.drop(columns=['txId', 'time_step', 'class']).values
x_tensor = torch.tensor(x_features, dtype=torch.long)

# 2. Tensor Y (Clases/Respuestas)
y_tensor = torch.tensor(df_nodos['class'].values, dtype=torch.long)

# 3. Tensor Edge_Index (Topología): PyTorch exige que sea una matriz transpuesta de 2 filas (.t())
edge_index_tensor = torch.tensor(df_edge[['txId1', 'txId2']].values, dtype=torch.long).t().contiguous()
graph_data = Data(x=x_tensor, edge_index=edge_index_tensor, y=y_tensor)

print("\n--- !OBJETO DE DATOS PARA LA IA LISTO! ---")
print(graph_data)
print(f"Nodos totales:{graph_data.num_nodes}")
print(f"Aristas totales{graph_data.num_edges}")
print(f"Caracteristicas por nodo:{graph_data.num_node_features}")