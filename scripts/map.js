
d3.select(window).on("resize", throttle);

var zoom = d3.behavior.zoom()
    .scaleExtent([1, 9])
    .on("zoom", move);


var width = document.getElementById('div_wmap').offsetWidth;
var height = width / 2;

var topo,projection,path,svg,g;

var graticule = d3.geo.graticule();

var tooltip = d3.select("#div_wmap")
				.append("div")
				.attr("class", "tooltip hidden")


setup(width,height);

function setup(width,height){
  projection = d3.geo.mercator()
    .translate([(width/2), (height/2)])
    .scale( width / 2 / Math.PI);

  path = d3.geo.path().projection(projection);

  svg = d3.select("#div_wmap").append("svg")
      .attr("width", width)
      .attr("height", height)
      .call(zoom)
      .on("click", click)
      .append("g");

  g = svg.append("g");

}

d3.json("data/world-topo-min.json", function(error, world) {

  var countries = topojson.feature(world, world.objects.countries).features;

  topo = countries;
  draw(topo);

});

function draw(topo) {

  svg.append("path")
     .datum(graticule)
     .attr("class", "graticule")
     .attr("d", path);


  g.append("path")
   .datum({type: "LineString", coordinates: [[-180, 0], [-90, 0], [0, 0], [90, 0], [180, 0]]})
   .attr("class", "equator")
   .attr("d", path);


  var country = g.selectAll(".country").data(topo);

  country.enter().insert("path")
      .attr("class", "country")
      .attr("d", path)
      .attr("id", function(d,i) { return d.id; })
      .attr("title", function(d,i) { return d.properties.name; })
      .style("fill", function(d, i) { return d.properties.color; });
      //.style("fill",'blue');

  //offsets for tooltips
  var offsetL = document.getElementById('div_wmap').offsetLeft+20;
  var offsetT = document.getElementById('div_wmap').offsetTop+10;

  //tooltips
  country.on("mousemove", function(d,i) {

      var mouse = d3.mouse(svg.node()).map( function(d) { return parseInt(d); } );
      
      console.log(d.properties.name)

      tooltip.classed("hidden", false)
                .html("<h1>Bar Graph</h1><br> <svg class='chart'></svg>")
                .style("left", (d3.event.pageX - 34) + "px")
                .style("top", (d3.event.pageY - 12) + "px")

     // .style("fill", "blue");
     
 
     
      })


  country.on("mouseout",  function(d,i) {
        tooltip.classed("hidden", true);
      }); 


  //EXAMPLE: adding some capitals from external CSV file
  // d3.csv("data/country-capitals.csv", function(err, capitals) {

  //   capitals.forEach(function(i){
  //     addpoint(i.CapitalLongitude, i.CapitalLatitude, i.CapitalName );
  //   });

  // });

}


function redraw() {
  width = document.getElementById('div_wmap').offsetWidth;
  height = width / 2;
  d3.select('svg').remove();
  setup(width,height);
  draw(topo);
}


function move() {

  var t = d3.event.translate;
  var s = d3.event.scale; 
  zscale = s;
  var h = height/4;


  t[0] = Math.min(
    (width/height)  * (s - 1), 
    Math.max( width * (1 - s), t[0] )
  );

  t[1] = Math.min(
    h * (s - 1) + h * s, 
    Math.max(height  * (1 - s) - h * s, t[1])
  );

  zoom.translate(t);
  g.attr("transform", "translate(" + t + ")scale(" + s + ")");

  //adjust the country hover stroke width based on zoom level
  d3.selectAll(".country").style("stroke-width", 1.5 / s);

}



var throttleTimer;
function throttle() {
  window.clearTimeout(throttleTimer);
    throttleTimer = window.setTimeout(function() {
      redraw();
    }, 200);
}


//geo translation on mouse click in div_wmap
function click() {
  var latlon = projection.invert(d3.mouse(this));
  console.log(latlon);


}


// //function to add points and text to the div_wmap (used in plotting capitals)
// function addpoint(lat,lon,text) {

//   var gpoint = g.append("g").attr("class", "gpoint");
//   var x = projection([lat,lon])[0];
//   var y = projection([lat,lon])[1];

//   gpoint.append("svg:circle")
//         .attr("cx", x)
//         .attr("cy", y)
//         .attr("class","point")
//         .attr("r", 1.5);

//   //conditional in case a point has no associated text
//   if(text.length>0){

//     gpoint.append("text")
//           .attr("x", x+2)
//           .attr("y", y+2)
//           .attr("class","text")
//           .text(text);
//   }

// }

// make bar graph
var width = 300,
    height = 300;

var y = d3.scale.linear()
    .range([height, 0]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", height);

d3.tsv("data.tsv", type, function(error, data) {
  y.domain([0, d3.max(data, function(d) { return d.value; })]);

  var barWidth = width / data.length;

  var bar = chart.selectAll("g")
      .data(data)
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; });

  bar.append("rect")
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); })
      .attr("width", barWidth - 1);

  bar.append("text")
      .attr("x", barWidth / 2)
      .attr("y", function(d) { return y(d.value) + 3; })
      .attr("dy", ".75em")
      .text(function(d) { return d.value; });
});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
}


// var data;
//     var scale = 1.25
//     var delay = 1600
//     var canvas = d3.select(".chart")
//         .attr("width", width)
//         .attr("height", height);
//         .style("border", "1px solid #111")

//     var line =  d3.line()
//         .x(function(d) { return d.x })
//         .y(function(d) { return d.y })
//         .curve(d3.curveBasis)

//     d3.json("data/house_rep.json", function(err, faces) {      
//         render(0)
//         function render(i) {
//             var drawing = faces[i]
//             var strokes = strokifyDrawing(drawing.drawing)
//             center(strokes)

//             var ps = canvas.selectAll("path").data(strokes)
//             ps.exit().remove()
//             var psE = ps.enter().append("path")
//             ps = psE.merge(ps)
//             ps
//                 .attr("d", line)
//                 .style("fill", "none")
//                 .style("stroke", "#111")
//                 .style("stroke-width", 3)
//                 .style("stroke-linecap", "round")
        
//         } 
//   })
//     function center(strokes) {
//         var minY = Infinity
//         var maxY = -Infinity
//         var minX = Infinity
//         var maxX = -Infinity
//         var centroidX = 0
//         var centroidY = 0
//         var count = 0
//         strokes.forEach(function(stroke) {
//             stroke.forEach(function(p) {
//             centroidX += p.x
//             centroidY += p.y
//             count++
//             })
//         })
//         centroidX /= count;
//         centroidY /= count;
//         strokes.forEach(function(stroke) {
//             stroke.forEach(function(p) {
//                 p.x *= scale
//                 p.y *= scale
//                 p.x += width/2 - centroidX * scale
//                 p.y += height/2 - centroidY * scale
//                 if(p.y < minY) minY = p.y
//                 if(p.y > maxY) maxY = p.y
//                 if(p.x < minX) minX = p.x
//                 if(p.x > maxX) maxX = p.x
//             })
//         })
//         var diffX = minX - (width - maxX)
//         var diffY = minY - (height - maxY)
//         strokes.forEach(function(stroke) {
//             stroke.forEach(function(p) {
//                 p.x -= diffX/2
//                 p.y -= diffY/2
//             })
//         })
//     }
//     function strokifyDrawing(drawing) {
//         var strokes = drawing.div_wmap(function(s) {
//             var points = []
//             s[0].forEach(function(x,i) {
//                 points.push({x: x, y: s[1][i] })
//             })
//             return points;
//         })
//         return strokes
//     }
// }