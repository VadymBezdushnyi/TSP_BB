var nodes = null;
var edges = null;
var network = null;
// randomly create some nodes and edges
var dataGraph = getScaleFreeNetwork(25);
var seed = 2;


function getScaleFreeNetwork(nodeCount) {
    var nodes = [];
    var edges = [];
    var connectionCount = [];

    // randomly create some nodes and edges
    for (var i = 0; i < nodeCount; i++) {
        nodes.push({
            id: i,
            label: String(i)
        });

        connectionCount[i] = 0;

        // create edges in a scale-free-network way
        if (i == 1) {
            var from = i;
            var to = 0;
            edges.push({
                from: from,
                to: to
            });
            connectionCount[from]++;
            connectionCount[to]++;
        }
        else if (i > 1) {
            var conn = edges.length * 2;
            var rand = Math.floor(Math.random() * conn);
            var cum = 0;
            var j = 0;
            while (j < connectionCount.length && cum < rand) {
                cum += connectionCount[j];
                j++;
            }


            var from = i;
            var to = j;
            edges.push({
                from: from,
                to: to
            });
            connectionCount[from]++;
            connectionCount[to]++;
        }
    }

    return {nodes: nodes, edges: edges};
}

var randomSeed = 764; // Math.round(Math.random()*1000);
function seededRandom() {
    var x = Math.sin(randomSeed++) * 10000;
    return x - Math.floor(x);
}

function getScaleFreeNetworkSeeded(nodeCount, seed) {
    if (seed) {
        randomSeed = Number(seed);
    }
    var nodes = [];
    var edges = [];
    var connectionCount = [];
    var edgesId = 0;


    // randomly create some nodes and edges
    for (var i = 0; i < nodeCount; i++) {
        nodes.push({
            id: i,
            label: String(i)
        });

        connectionCount[i] = 0;

        // create edges in a scale-free-network way
        if (i == 1) {
            var from = i;
            var to = 0;
            edges.push({
                id: edgesId++,
                from: from,
                to: to
            });
            connectionCount[from]++;
            connectionCount[to]++;
        }
        else if (i > 1) {
            var conn = edges.length * 2;
            var rand = Math.floor(seededRandom() * conn);
            var cum = 0;
            var j = 0;
            while (j < connectionCount.length && cum < rand) {
                cum += connectionCount[j];
                j++;
            }


            var from = i;
            var to = j;
            edges.push({
                id: edgesId++,
                from: from,
                to: to
            });
            connectionCount[from]++;
            connectionCount[to]++;
        }
    }

    return {nodes: nodes, edges: edges};
}

function addNode(qid, qlabel) {
    try {
        nodes.add({
            id: qid,
            label: qlabel
        });
    }
    catch (err) {
        alert(err);
    }
}

function updateNode(id, label) {
    try {
        nodes.update({
            id: id,
            label: label
        });
    }
    catch (err) {
        alert(err);
    }
}

function addEdge(id, from, to) {
    try {
        edges.add({
            id: id,
            from: from,
            to: to
        });
    }
    catch (err) {
        alert(err);
    }
}

function updateEdge(id, from, to) {
    try {
        edges.update({
            id: id,
            from: from,
            to: to
        });
    }
    catch (err) {
        alert(err);
    }
}

function setDefaultLocale() {
    var defaultLocal = navigator.language;
    var select = document.getElementById('locale');
    select.selectedIndex = 0; // set fallback value
    for (var i = 0, j = select.options.length; i < j; ++i) {
        if (select.options[i].getAttribute('value') === defaultLocal) {
            select.selectedIndex = i;
            break;
        }
    }
}

function destroy() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
}
function draw() {
    // create an array with nodes
    nodes = new vis.DataSet();

    // create an array with edges
    edges = new vis.DataSet();


    // create a network
    var container = document.getElementById('mynetwork');
    var dataGraph = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    network = new vis.Network(container, dataGraph, options);

}

function visualize(res) {
    draw();
    console.log(res);
    for (var i = 0; i < res.time_entries.length; i++) {
        var obj = res.time_entries[i];
        // console.log(obj);
        obj.created.forEach(function(el){
            addNode(el, el.toString());
            if(el !== 1){
                addEdge(el, el, Math.floor(el/2));
            }
        });
        obj.created.forEach(function(el){
            var clickedNode = nodes.get(el);
            clickedNode.color = {
                border: '#000000',
                background: '#000000',
                highlight: {
                    border: '#2B7CE9',
                    background: '#D2E5FF'
                }
            }
        });
    };


}

function clearPopUp() {
    document.getElementById('saveButton').onclick = null;
    document.getElementById('cancelButton').onclick = null;
    document.getElementById('network-popUp').style.display = 'none';
}

function cancelEdit(callback) {
    clearPopUp();
    callback(null);
}

function saveData(dataGraph, callback) {
    dataGraph.id = document.getElementById('node-id').value;
    dataGraph.label = document.getElementById('node-label').value;
    clearPopUp();
    callback(dataGraph);
}

function init() {
    setDefaultLocale();
    draw();
}
