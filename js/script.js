// --- ETAPA 3.1 y 3.3: CONEXIÓN A NEO4J Y BÚSQUEDA ---

window.addEventListener('DOMContentLoaded', () => {
    
    // 1. Configuración base (Tu código)
    const baseConfig = {
        containerId: "graph-container",
        neo4j: {
            serverUrl: "neo4j://127.0.0.1:7687",
            serverUser: "neo4j",
            serverPassword: "neo4j123" 
        },
        labels: {
            "Transaction": {
                caption: "Property 1", // Aquí Neo4j leerá el ID de la transacción
                community: "Property 2" // Aquí Neo4j leerá la clase para darle color
            }
        },
        relationships: {
            "TRANSACTION": { // O "SENDS_TO", asegúrate de usar el nombre exacto de tus aristas
                caption: false,
                thickness: "amount"
            }
        },
        initialCypher: "MATCH (n:Transaction)-[r]->(m:Transaction) RETURN n, r, m LIMIT 25"
    };

    // 2. Motor de Renderizado (Tu código)
    function initViz(config) {
        try {
            if (window.viz) {
                // Si ya hay un grafo dibujado, limpia la pantalla para dibujar uno nuevo
                const container = document.getElementById('graph-container');
                if (container) container.innerHTML = '';
            }
            window.viz = new (NeoVis.default || NeoVis)(config);
            window.viz.render();
            console.log("Grafo cargado con éxito.");
        } catch (e) {
            console.error("Error al arrancar NeoVis:", e);
        }
    }

    // 3. Dibujar el grafo por primera vez al abrir la página
    initViz(baseConfig);

    // --- LÓGICA DE BÚSQUEDA ---

    // 4. Capturar el clic del botón
    window.handleSearch = function() {
        const input = document.getElementById('walletInput');
        const address = input ? input.value.trim() : null;
        
        if (address) {
            window.searchWallet(address);
        } else {
            alert("Por favor ingresa un ID de transacción.");
        }
    };

    // 5. Redibujar el grafo con el nodo específico
    window.searchWallet = function(address) {
        // Creamos una nueva configuración copiando la base, pero cambiamos la consulta
        const newConfig = {
            ...baseConfig, 
            initialCypher: `MATCH (a:Transaction {\`Property 1\`: "${address}"})-[r*1..2]-(neighbors) RETURN a, r, neighbors LIMIT 50`
        };
        initViz(newConfig);
        
       
    };
});


