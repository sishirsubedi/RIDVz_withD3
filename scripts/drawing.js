var drawingWidth = 100
var drawingHeight= 100;
var margin = { top: 0, right: 0, bottom: 0, left: 0 };
var xAxisLabelHeader = "X Header";
var yAxisLabelHeader = "Y Header";
var data;
var canvas;
var chartWidth;
var chartHeight;
console.log(drawingWidth);
init();

function init() {
 	chartWidth = drawingWidth;
    chartHeight = drawingHeight;
    var scale = 1.25
    var delay = 1600
    var svg = d3.select("#drawing").append("svg")
        .attr("width", "1280")
        .attr("height", "600")
        .attr("viewBox", "0 0 1280 600")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("id","testDraw")
        // .style("border", "1px solid #111")
        

    var line =  d3.line()
        .x(function(d) { return d.x })
        .y(function(d) { return d.y })
        .curve(d3.curveBasis)

    d3.json("./data/house_rep.json", function(err,house) {      
        render(0)
        function render(i) {
            var drawing = house[i]
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
                
        
            setTimeout(function() {
                i++

                if(i >= house.length) i = 0;
                render(i)
            }, delay)
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


	



   