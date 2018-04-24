function show_map() {
    document.getElementById("chartDiv").style = "display: block;";
    document.getElementById("clusterDiv").style = "display: none;";
    document.getElementById("evalDiv").style = "display: none;";
    
}
var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
    height = 600;

//cursor move in order to allow interactivity
var svg = d3.select("#chartDiv")
    .append("svg")
    .style("cursor", "move");
svg.attr("viewBox", "50 10 " + (width) + " " + (height))
    .attr("preserveAspectRatio", "xMinYMin")
    .attr("id","worldMap");
//group element
var map = svg.append("g")
    .attr("class", "map");




var chart = d3.select("#chartDiv")
    .style("display", "none");
    
var bubble_chart = d3.select("#clusterDiv")
    .style("display", "none");