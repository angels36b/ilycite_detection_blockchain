import pandas as pd 
from neo4j import GraphDatabase
#we connect to the neo4j database
#Мы подключаемся к базе данных 
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "neo4j123"

print ("Intentando conectar")
try:
    driver = GraphDatabase.driver(URI, auth = (USER, PASSWORD))
    driver.verify_connectivity()
    print("!Exito La conexxion a Neo4j esta funcioando perfect")
    driver.close()

except Exception as e:
    print("Error:No se pudo conectar")
    print("detalle del error: {e}", str(e))
#Мы создаем переменную и создаем фрейм данных
df_features = pd.read_csv("elliptic_txs_features.csv", header = None)
df_features.rename(columns = {0:'txId', 1:'time_step'},inplace=True)
df_classes = pd.read_csv("elliptic_txs_classes.csv")
df_edge = pd.read_csv("elliptic_txs_edgelist.csv")

#unimos los features y class
df_nodos = pd.merge(df_features, df_classes, on="txId", how="left")

df_nodos.columns = df_nodos.columns.astype(str)
df_edge.columns = df_edge.columns.astype(str)

list_nodos = df_nodos.to_dict("records")
list_arist = df_edge.to_dict("records")

def create_nodos(tx, batch_nodos):
    query="""
    UNWIND $batch AS fila
    MERGE (t:Transaction {id: fila.txId})
    SET t.class = fila.class,
        t.time_step = fila.time_step
    """
    tx.run(query, batch=batch_nodos)

def create_aristas(tx, batch_aristas):
    query = """
    UNWIND $batch AS fila
    MATCH (t1:Transaction {id: fila.txId1})
    MATCH (t2:Transaction {id: fila.txId2})
    MERGE (t1)-[:SENDS_TO]->(t2)
    """
    tx.run(query, batch=batch_aristas)

# --- 4. EJECUCIÓN (El envío a Neo4j) ---
print("Conectando a Neo4j y enviando datos...")
with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
    with driver.session() as session:
        
        print("1/2: Creando Nodos en Neo4j (esto puede tardar unos segundos)...")
        lote_size = 10000
        for i in range(0, len(list_nodos), lote_size):
            lote = list_nodos[i : i + lote_size]
            session.execute_write(create_nodos, lote)
            print(f"   -> Nodos {i} al {i + len(lote)} inyectados.")
            
        print("2/2: Creando Aristas en Neo4j (esto también tomará unos segundos)...")
        for i in range(0, len(list_arist), lote_size):
            lote = list_arist[i : i + lote_size]
            session.execute_write(create_aristas, lote)
            print(f"   -> Aristas {i} al {i + len(lote)} inyectadas.")