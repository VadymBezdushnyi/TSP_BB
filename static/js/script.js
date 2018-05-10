var width = 3;
var height = 3;
var max_size = 30;
var data = zero_matrix(max_size, max_size);
var result = zero_matrix(max_size, max_size);


var color_main_1 = '#FFFFFF';
var color_main_2 = '#F9F9F9';
var color_disabled = '#EEEEEE';
var color_special = '#BBFF99';


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
            data[i][j] = Math.floor((Math.random() * 400) + 5);
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
    set_size(4, 4);
    fill(0);
    var INF = 100000;
    x = [[INF, 5, 11, 9], [10, INF, 8, 7], [7, 14, INF, 8], [12, 6, 15, INF]];
    for (var i = 0; i < height; i++)
        for (var j = 0; j < width; j++)
            data[i][j] = x[i][j];
    rebuild_matrix();
}

function sample2() {
    set_size(6, 6);
    fill(0);
    x = [[-2, 0, 0, 0, 1, 0], [0, 2, 1, 0, 0, 2], [0, 0, 2, 1, 0, 0], [1, 0, 0, 2, 2, 0], [0, 0, 0, 0, -3, 1], [0, 0, 0, 0, 0, -3]];
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
    var INF = 1000
    for (var i = 0; i < height; i++)
        subdata[i][i] = INF

    $.getJSON('/calculate', {
        "matrix": subdata,
        "width": width,
        "height": height
    }, function (data) {
        visualize(data.result);
        $("#message").empty().append(data.message);
        set_status(data.ok);
    });
}

function first_letter_color(text, color) {
    return '<span class="first-char">' + text[0] + '</span>' + text.slice(1);
}
