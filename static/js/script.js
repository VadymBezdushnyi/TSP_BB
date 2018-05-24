var width = 3;
var height = 3;
var max_size = 15;
var data = zero_matrix(max_size, max_size);
var result;
var finalNode = 0;

var INF = 1000 * 1000;
var MAX_VALUE = 1000;

var color_main_1 = '#FFFFFF';
var color_main_2 = '#F9F9F9';
var color_disabled = '#EEEEEE';
var color_special = '#BBFF99';

var timeouts = [];

var colorizer = function (i, j) {
    return (i < height && j < width ? ((i + j) % 2 == 0 ? color_main_1 : color_main_2) : color_disabled);
};

function zero_matrix(width, height) {
    var data = [], row = [];
    for (var i = 0; i < width; i++) row.push(0);
    for (var i = 0; i < height; i++) data.push(row.slice());
    return data;
}

window.onload = function () {
    init();
    set_size(3, 3);
}

function set_size(nwidth, nheight) {
    if (nwidth > max_size || nwidth < 1 || nheight > max_size || nheight < 1)
        return;
    width = nwidth;
    height = nheight;
    rebuild_matrix();
    set_matrix("output-matrix", zero_matrix(max_size, max_size));
    $("#size").empty().append(width + "x" + height);
    $("#size-width").empty().append(width);
    $("#size-height").empty().append(height);
}

function change_size(diff_widtn, diff_height) {
    set_size(width + diff_widtn, height + diff_height);
}

function getId(i, j) {
    return id = 'A-' + i + '-' + j;
}

function random() {
    for (var i = 0; i < max_size; i++) {
        for (var j = 0; j < max_size; j++) {
            data[i][j] = Math.floor((Math.random() * 40) + 5);
        }
    }
    rebuild_matrix();
}

function fill(val) {
    for (var i = 0; i < max_size; i++)
        for (var j = 0; j < max_size; j++)
            data[i][j] = val;
    rebuild_matrix();
}

function enabled(i, j) {
    return i !== j && i < height && j < width;
}


function rebuild_matrix() {
    $("#message").empty();
    var content = ''
    for (var i = 0; i < max_size; i++) {
        content += '<tr>';
        for (var j = 0; j < max_size; j++) {
            content += '<td>';
            content += '<input style="background-color:' + colorizer(i, j) +
                '" class="matrix-cell" id="' + getId(i, j) + '" value="' +
                (enabled(i, j) ? data[i][j] : ((i === j) ? "&infin;" : 0)) + '" ' + (enabled(i, j) ? '' : 'disabled') + '/>';
            content += '</td>';
        }
        content += '</tr>';
    }
    $('#input-matrix').empty().append(content);
    $("#input-matrix").on('mouseup', '.matrix-cell', function () {
        $(this).select();
    });
    $("#input-matrix").on('change', '.matrix-cell', function () {
        var splitted = $(this).attr("id").split("-");
        data[parseInt(splitted[1])][parseInt(splitted[2])] = $(this).val();
    });
}


function set_matrix(id, data) {
    result = data;
    var content = '';
    for (var i = 0; i < max_size; i++) {
        content += '<tr>';
        for (var j = 0; j < max_size; j++) {
            content += '<td>';
            if (enabled(i, j) && data[i][j] != 0)
                content += '<a style="background-color:' + colorizer(i, j) + '" class="matrix-cell output ' + (enabled(i, j) ? 'enabled' : 'disabled') + '" >' + format_fraction(data[i][j]) + '</a>';
            else
                content += '<a style="background-color:' + colorizer(i, j) + '" class="matrix-cell output zero ' + (enabled(i, j) ? 'enabled' : 'disabled') + '" >0</a>';
            content += '</td>';
        }
        content += '</tr>';
    }
    $('#' + id).empty().append(content);
}


function set_status(ok) {
    if (ok)
        $("#message").css({color: "#494"});
    else
        $("#message").css({color: "#944"});
}

function sample1() {
    set_size(5, 5);
    random();

    x = [[INF, 2, 3, 4, 1],
        [2, INF, 2, 3, 7],
        [3, 3, INF, 3, 2],
        [3, 3, 2, INF, 2],
        [2, 2, 1, 2, INF]];
    for (var i = 0; i < height; i++)
        for (var j = 0; j < width; j++)
            data[i][j] = x[i][j];
    rebuild_matrix();
}

function sample2() {
    set_size(7, 7);
    random();
    x = [[0, 3, 93, 13, 33, 9, 57],
        [4, 0, 77, 42, 21, 16, 34],
        [45, 17, 0, 36, 16, 28, 25],
        [39, 90, 80, 0, 56, 7, 91],
        [28, 46, 88, 33, 0, 25, 57],
        [3, 88, 18, 46, 92, 0, 7],
        [44, 26, 33, 27, 84, 39, 0]];
    for (var i = 0; i < height; i++)
        for (var j = 0; j < width; j++)
            data[i][j] = x[i][j];
    rebuild_matrix();
}


function sample3() {
    set_size(11, 11);
    random();
    x = [[0, 327, 353, 144, 217, 452, 333, 318, 304, 149, 280],
        [327, 0, 243, 183, 376, 174, 90, 158, 403, 251, 56],
        [353, 243, 0, 263, 245, 190, 155, 85, 217, 205, 206],
        [144, 183, 263, 0, 250, 318, 199, 203, 311, 118, 138],
        [217, 376, 245, 250, 0, 417, 327, 268, 90, 134, 320],
        [452, 174, 190, 318, 417, 0, 119, 150, 405, 330, 187],
        [333, 90, 155, 199, 327, 119, 0, 74, 337, 221, 74],
        [318, 158, 85, 203, 268, 150, 74, 0, 267, 183, 122],
        [304, 403, 217, 311, 90, 405, 337, 267, 0, 194, 349],
        [149, 251, 205, 118, 134, 330, 221, 183, 194, 0, 195],
        [280, 56, 206, 138, 320, 187, 74, 122, 349, 195, 0]];
    for (var i = 0; i < height; i++)
        for (var j = 0; j < width; j++)
            data[i][j] = x[i][j];
    rebuild_matrix();
}


function calculate() {
    set_status(true);
    $("#message").empty().append("Calculation...");
    var subdata = []
    for (var i = 0; i < height; i++)
        subdata.push(data[i].slice(0, width));

    for (var i = 0; i < height; i++)
        for (var j = 0; j < width; j++)
            subdata[i][j] = ((i === j) ? INF : Math.min(data[i][j], MAX_VALUE));


    $.getJSON('/calculate', {
        "matrix": subdata,
        "width": width,
        "height": height
    }, function (data) {
        result = data.result;
        set_status(data.ok);
        if (data.ok) {
            $("#message").empty().append("Visualization...");
            console.log("result");
            console.log(result);
            visualizeVisjs(data.result);
            $("#message").empty().append(data.message);
            set_status(data.ok);
        } else {
            $("#message").empty().append(data.message);
        }

    });
}

function first_letter_color(text, color) {
    return '<span class="first-char">' + text[0] + '</span>' + text.slice(1);
}

var tree_nodes = null;
var tree_edges = null;
var tree_network = null;


var graph_nodes = null;
var graph_edges = null;
var graph_network = null;


function addNode(qid, qlabel) {
    try {
        tree_nodes.add({
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
        tree_nodes.update({
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
        tree_edges.add({
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
        tree_edges.update({
            id: id,
            from: from,
            to: to
        });
    }
    catch (err) {
        alert(err);
    }
}


function destroy() {
    if (tree_network !== null) {
        tree_network.destroy();
        tree_network = null;
    }
}

var tree_options = {
    nodes: {
        shape: 'circle'
    },
    edges: {
        smooth: false
    },
    layout: {
        randomSeed: undefined,
        improvedLayout: true,
        hierarchical: {
            enabled: true,
            levelSeparation: 100,
            nodeSpacing: 100,
            treeSpacing: 200,
            blockShifting: true,
            edgeMinimization: true,
            parentCentralization: true,
            direction: 'DU',        // UD, DU, LR, RL
            sortMethod: 'directed'   // hubsize, directed
        }
    }
}

function set_graph_edges(id) {
    graph_edges.clear()

    var path_pool = result.nodes[id].tsp_matrix.paths_pool
    console.log("path_pool", path_pool)
    var pathLen = 0;
    path_pool.forEach(function (path) {
        for (var i = 0; i + 1 < path.length; i++) {
            console.log(path[i]);
            var edge_len = result.nodes[1].tsp_matrix.init_matrix[path[i]][path[i + 1]]
            graph_edges.add({
                id: path[i],
                from: path[i],
                to: path[i + 1],
                label: edge_len.toString()
            });
            pathLen += edge_len;
        }

    });
    infoContainer = document.getElementById('info');
    infoContainer.innerHTML = 'Lower_bound: ' + '<b>' + result.nodes[id].tsp_matrix.lower_bound + '</b>' + '<br>';
    infoContainer.innerHTML += '<b>' + 'Path length:' + '</b>' + pathLen;
    graph_network.fit()
}

function draw() {
    destroy();
    // create an array with tree_nodes
    tree_nodes = new vis.DataSet();

    // create an array with tree_edges
    tree_edges = new vis.DataSet();


    // create a tree_network
    tree_container = document.getElementById('mynetwork');
    tree_data = {
        nodes: tree_nodes,
        edges: tree_edges
    };

    tree_network = new vis.Network(tree_container, tree_data, tree_options);
    tree_network.on('click', function (properties) {
        var ids = properties.nodes;
        var clickedNode = tree_nodes.get(ids)[0];
        console.log(result.nodes[3])
        if (clickedNode !== undefined) {
            set_graph_edges(clickedNode.id)
        }
    });

    console.log('drawing graph')

    graph_nodes = new vis.DataSet();
    graph_edges = new vis.DataSet();

    var graph_container = document.getElementById('drawgraph');
    var graph_data = {
        nodes: graph_nodes,
        edges: graph_edges
    };
    var graph_options = {
        nodes: {
            shape: 'circle'
        },
        edges: {
            arrows: {
                to: {
                    enabled: true,
                    type: 'arrow'
                }
            },
            smooth: false
        }
    };
    graph_network = new vis.Network(graph_container, graph_data, graph_options);
}


function animate(res) {
    MAX_TIME = 10000;
    console.log("start animation");
    node_cnt = res.time_entries.length;
    console.log(finalNode)
    set_graph_edges(finalNode)
    for (var i = 0; i < node_cnt; i++) {
        var obj = (res.time_entries[i]);
        // console.log(obj);
        var timeit = (i + 1) * Math.min(Math.floor(MAX_TIME / node_cnt), 400);
        // var timeEl = obj;
        timeouts.push(
            setTimeout(function (obj) {
                obj.created.forEach(function (timeEl) {

                    tree_nodes.update({
                        id: timeEl,
                        label: timeEl.toString(),
                        color: (timeEl % 2 === 1 ? '#33BB33' : '#FF5522')
                    })
                });
                obj.deleted.forEach(function (timeEl) {

                    tree_nodes.update({
                        id: timeEl,
                        label: timeEl.toString(),
                        color: (timeEl % 2 === 1 ? '#559988' : '#995522')
                    });
                    // console.log("animation: " + timeit)
                });

                obj.final.forEach(function (timeEl) {
                    finalNode = timeEl
                    tree_nodes.update({
                        id: timeEl,
                        label: timeEl.toString(),
                        color: '#00FF00'
                    });
                    // console.log("animation: " + timeit)
                });


            }, timeit, obj)
        );
    }
    console.log("end animation")

}

function visualizeVisjs(res) {
    draw();


    for (var i = 0; i < timeouts.length; i++) {
        clearTimeout(timeouts[i]);
    }
    //quick reset of the timer array you just cleared
    timeouts = [];

    console.log(res);
    var tree_new_nodes = []
    var tree_new_edges = []

    var graph_new_nodes = []
    console.log(res.order)

    for (var i = 0; i < res.time_entries.length; i++) {
        var obj = res.time_entries[i];
        // console.log(obj);
        obj.created.forEach(function (el) {

            tree_new_nodes.push({
                id: el,
                label: el.toString()
            });

            if (el !== 1) {
                tree_new_edges.push({
                    id: el.toString(),
                    from: el,
                    to: Math.floor(el / 2)
                });
            }
        });
        obj.final.forEach(function (timeEl) {
            finalNode = timeEl;
        });
    }
    tree_nodes.add(tree_new_nodes);
    tree_edges.add(tree_new_edges);
    console.log(tree_edges);
    tree_network.fit()
    graph_network.fit()

    for (var i = 0; i < result.nodes[finalNode].tsp_matrix.paths_pool[0].length - 1; i++) {
        graph_new_nodes.push({
            id: i,
            label: (i + 1).toString()
        });
    }
    graph_nodes.add(graph_new_nodes);

    console.log("end");
    animate(res);
}

function init() {
    draw();
}
