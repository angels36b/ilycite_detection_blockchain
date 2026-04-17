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
                caption: "id", // Aquí Neo4j leerá el ID de la transacción
                community: "class" // Aquí Neo4j leerá la clase para darle color
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
    //Etapa Funcion del velocimetro
   

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
        const numericId = parseInt(address);

        const newConfig = {
            ...baseConfig, 
            initialCypher: `MATCH (a:Transaction {id: ${numericId}})-[r]-(neighbors) RETURN a, r, neighbors LIMIT 50`
        };
        console.log("running search", newConfig.initialCypher);
        initViz(newConfig);
    };
});

function updateRiskScore (percentage){
    //create data array what to draw
    const data = [
        {
            domain: {x:[0,1], y:[0,1]}, //use the whole drawing area
            value: percentage, //The needle position comes from the input number
            title:{text: "GNN Risk Score", font:{size: 18}},
            type: "indicator", //this is a gauge/indicator chart
            mode: "gauge+number", //Show botj the gauge dial AND the numeric value inside
            gauge: {
                axis: {range:[0,100], tickwidth:1, tickcolor: "darkblue"},
                bar: {color: "#1e3a8a"},
                bgcolor:"white",
                borderwidth:2,
                bordercolor: "gray",
                steps: [
                    {range: [0,40], color: "#a8d5ba"},
                    {range:[40,80], color: "#f7d59c"},
                    {range: [80,100], color: "#f4a29e"},
                ],
                threshold:{
                    line: {color: "red", width: 4},
                    thickness:0.75,
                    value:90
                }

            }
        }
    ];

    const layout = {
        width: 300,
        height: 250,
        margin: {t:25, r:25, l:25, b:25},
        paper_bgcolor: "transparent",
        font: {color: "#1e3a8a", family: "Arial"}
    };
    //Execution Command
    Plotly.newPlot('plotly-score-container', data, layout);
}

updateRiskScore(0);


