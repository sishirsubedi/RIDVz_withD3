function show_info() {
    document.getElementById("project_info").style = "display: block;";
    document.getElementById("animation").style = "display: none;";
    document.getElementById("image_menu").style = "display: none;";
    document.getElementById("chartDiv").style = "display: none;";
    document.getElementById("clusterDiv").style = "display: none;";
    document.getElementById("evalDiv").style = "display: none;";
    document.getElementById("map_cluster_choice_btns").style = "display: none;";
    //document.getElementById("clusterDiv").style = "visibility: hidden;";
    
}
function show_image_menu() {
    document.getElementById("image_menu").style = "display: block;";
    document.getElementById("project_info").style = "display: none;";
    document.getElementById("animation").style = "display: none;";
    document.getElementById("map_cluster_choice_btns").style = "display: none;";
    //document.getElementById("clusterDiv").style = "visibility: visible;";
}
function show_map_cluster_menu(input_image) {
    
    document.getElementById("map_cluster_choice_btns").style = "display: block;";
    document.getElementById("animation").style = "display: none;";
    document.getElementById("image_menu").style = "display: block; padding: 0;";
    document.getElementById("chartDiv").style = "display: none;";
    document.getElementById("clusterDiv").style = "display: none;";
    document.getElementById("project_info").style = "display: none;";
    document.getElementById("mainButtons").style = "display: none;";
    document.getElementById("evalDiv").style = "display: none;";
    
    var ele = document.getElementById("selected_image");
    var att = document.createAttribute("data-current");
    if(input_image == 'face') {
        document.getElementById("selected_image").src = "./images/myface.png";
        att.value = "face"; 
    } else if(input_image == 'cake') {
        document.getElementById("selected_image").src = "./images/cake.png";
        att.value = "cake"; 
    } else if(input_image == 'dog') {
        document.getElementById("selected_image").src = "./images/dog.png";
        att.value = "dog"; 
    } else if(input_image == 'tornado') {
        document.getElementById("selected_image").src = "./images/hurricane.png";
        att.value = "tornado"; 
    } else if(input_image == 'house') {
        document.getElementById("selected_image").src = "./images/house.png";
        att.value = "house"; 
    }
    ele.setAttributeNode(att); 
    console.log(ele.getAttribute("data-current"));
    load_choice(input_image);
}

function load_choice(input_image) {
    console.log(input_image);
    var rep_file_name = "";
    if(input_image == 'face') {
        rep_file_name = "./data/face_rep.json";
    } else if(input_image == 'cake') {
        rep_file_name = "./data/cake_rep.json";
    } else if(input_image == 'dog') {
        rep_file_name = "./data/dog_rep.json";
    } else if(input_image == 'tornado') {
        rep_file_name = "./data/tornado_rep.json";
    } else if(input_image == 'house') {
        rep_file_name = "./data/house_rep.json";
    }
    console.log(rep_file_name);
    d3.queue()
        .defer(d3.json, "./data/50m.json")
        .await(function (error, world, data) {
            if (error) {
                console.error('Oh man, something went wrong: ' + error);
            }
            else {
                drawMap(world, rep_file_name);
            }
    });
}

function drawMap(world, data) {
    var projection = d3.geoMercator() //d3.geoOrthographic()
        .scale(130)
        .translate([width / 2, height / 1.5]);
        
    console.log(data);

    // Actually drawing the lines
    var path = d3.geoPath().projection(projection);
    var features = topojson.feature(world, world.objects.countries).features;
    var categorical = [
      { "name" : "schemeAccent", "n": 8},
      { "name" : "schemeDark2", "n": 8},
      { "name" : "schemePastel2", "n": 8},
      { "name" : "schemeSet2", "n": 8},
      { "name" : "schemeSet1", "n": 9},
      { "name" : "schemePastel1", "n": 9},
      { "name" : "schemeCategory10", "n" : 10},
      { "name" : "schemeSet3", "n" : 12 },
      { "name" : "schemePaired", "n": 12},
      { "name" : "schemeCategory20", "n" : 20 },
      { "name" : "schemeCategory20b", "n" : 20},
      { "name" : "schemeCategory20c", "n" : 20 }
    ];                           
    var colorScale = d3.scaleOrdinal(d3[categorical[0].name]);

    map.append("g")
        .selectAll("path")
        .data(features)
        .enter().append("path")
        .attr("name", function (d) {
            return d.properties.name;
        })
        .attr("id", function (d) {
            return d.id;
        })
        .attr("d", path)
        .style("fill","#A9A9A9")
        .on('mouseover', function (d) {
            d3.select(this)
                .style("stroke", "white")
                .style("stroke-width", 1.25)
                .style("cursor", "pointer")
                .style("fill","#630110");

            d3.select(".country")
                .text(d.properties.name);
                console.log(d.id);
                
            init(data, d.id);

            //d3.select(".drawing")
             //    .text("insert drawing");
            //     console.log(d.details.females)

            // d3.select(".males")
            //     .text(d.details && d.details.males && "Male " + d.details.males || "Not available");

            d3.select('.details')
                .style('visibility', "visible")
        })
        .on('mouseout', function (d) {
            d3.select(this)
                .style("stroke", null)
                .style("stroke-width", 0.50)
                .style("fill","#A9A9A9");

            d3.select('.details')
                .style('visibility', "hidden");
                
            d3.select("#drawing svg").remove();
        });
        
    // init(data);
}

function init(input_file, choice) {
    var drawingWidth = 100
    var drawingHeight= 100;
    var margin = { top: 0, right: 0, bottom: 0, left: 0 };
    var xAxisLabelHeader = "X Header";
    var yAxisLabelHeader = "Y Header";
    var data;
    var canvas;
    var chartWidth;
    var chartHeight;
 	chartWidth = drawingWidth;
    chartHeight = drawingHeight;
    var scale = 1.25
    var delay = 1600
    var svg = d3.select("#drawing").append("svg")
        .attr("width", "1600")
        .attr("height", "600")
        .attr("viewBox", "200 0 1600 600")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("id","testDraw")
        // .style("border", "1px solid #111")
        

    var line =  d3.line()
        .x(function(d) { return d.x })
        .y(function(d) { return d.y })
        .curve(d3.curveBasis)

    d3.json(input_file, function(err,sketch) {    
        console.log(sketch);
        var i;
        for(i = 0; i < sketch.length; i++) {
            if(sketch[i].cc3 == choice) {
                break;
            }
        }
        render(i)
        function render(i) {
            var drawing = sketch[i]
            var strokes = strokifyDrawing(drawing.drawing)
            //center(strokes)

            var ps = svg.selectAll("path").data(strokes)
            ps.exit().remove()
            var psE = ps.enter().append("path")
            ps = psE.merge(ps)
            ps
                .attr("d", line)
                .style("fill", "none")
                .style("stroke", "#111")
                .style("stroke-width", 15)
                .style("stroke-linecap", "round")
                
        
            // setTimeout(function() {
            //     i++

            //     if(i >= sketch.length) i = 0;
            //     render(i)
            // }, delay)
        } 
	})
    function center(strokes) {
        var minY = Infinity
        var maxY = -Infinity
        var minX = Infinity
        var maxX = -Infinity
        var centroidX = 0
        var centroidY = 0
        var count = 0
        strokes.forEach(function(stroke) {
            stroke.forEach(function(p) {
            centroidX += p.x
            centroidY += p.y
            count++
            })
        })
        centroidX /= count;
        centroidY /= count;
        strokes.forEach(function(stroke) {
            stroke.forEach(function(p) {
                p.x *= scale
                p.y *= scale
                p.x += width/2 - centroidX * scale
                p.y += height/2 - centroidY * scale
                if(p.y < minY) minY = p.y
                if(p.y > maxY) maxY = p.y
                if(p.x < minX) minX = p.x
                if(p.x > maxX) maxX = p.x
            })
        })
        var diffX = minX - (width - maxX)
        var diffY = minY - (height - maxY)
        strokes.forEach(function(stroke) {
            stroke.forEach(function(p) {
                p.x -= diffX/2
                p.y -= diffY/2
            })
        })
    }
    function strokifyDrawing(drawing) {
        var strokes = drawing.map(function(s) {
            var points = []
            s[0].forEach(function(x,i) {
                points.push({x: x, y: s[1][i] })
            })
            return points;
        })
        return strokes
    }
}
