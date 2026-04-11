window.addEventListener('DOMContentLoaded', () => {
    // Configuración base (cambia la contraseña si es necesario)
    const baseConfig = {
        containerId: "graph-container",
        neo4j: {
            serverUrl: "neo4j://127.0.0.1:7687",
            serverUser: "neo4j",
            serverPassword: "neo4j123"  // ← Asegúrate que sea tu contraseña actual
        },
        labels: {
            "Transaction": {
                caption: "Property 1",
                community: "Property 2"
            }
        },
        relationships: {
            "TRANSACTION": {
                caption: "amount",
                thickness: "amount"
            }
        },
        initialCypher: "MATCH (n:Transaction) RETURN n LIMIT 25"
    };

    function initViz(config) {
        try {
            if (window.viz) {
                // Si ya existe, limpiar contenedor
                const container = document.getElementById('graph-container');
                if (container) container.innerHTML = '';
            }
            window.viz = new (NeoVis.default || NeoVis)(config);
            window.viz.render();
            console.log("NeoVis engine initialized with query:", config.initialCypher);
        } catch (e) {
            console.error("NeoVis failed to start:", e);
        }
    }

    // Inicializar
    initViz(baseConfig);

    // Funciones globales
    window.handleSearch = function() {
        const input = document.getElementById('walletInput');
        const address = input ? input.value.trim() : null;
        if (address) {
            window.searchWallet(address);
        } else {
            alert("Please enter an address");
        }
    };

    window.searchWallet = function(address) {
        const newConfig = {
            ...baseConfig,
            initialCypher: `MATCH (a:Transaction {\`Property 1\`: "${address}"})-[r*1..2]-(neighbors) RETURN a, r, neighbors LIMIT 50`
        };
        initViz(newConfig);
    };
});





