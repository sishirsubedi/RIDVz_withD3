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
    .style("cursor", "move")
    // .style("fill","#A9A9A9")
    .attr("viewBox", "50 10 " + (width) + " " + (height))
    .attr("preserveAspectRatio", "xMinYMin");
    // .attr("id","worldMap")
    // .on('mouseover', function (d) {
    //         d3.select("#worldMap")
    //             .style("stroke", "white")
    //             .style("stroke-width", 1.25)
    //             .style("cursor", "pointer")
    //             .style("fill","#FFFFFF");

    //         d3.select(".country")
    //             .text(d.properties.name);
    //             console.log(d.properties.name)

    //         d3.select(".drawing")
    //              .text("insert drawing");
    //         //     console.log(d.details.females)

    //         // d3.select(".males")
    //         //     .text(d.details && d.details.males && "Male " + d.details.males || "Not available");

    //         d3.select('.details')
    //             .style('visibility', "visible")
    //     })
    //     .on('mouseout', function (d) {
    //         d3.select("#worldMap")
    //             .style("stroke", null)
    //             .style("stroke-width", 0.25)
    //             .style("fill","#FFFFFF")

    //         d3.select('.details')
    //             .style('visibility', "hidden");
    //     });
    
    
    
    
//group element
var map = svg.append("g")
    .attr("class", "map");
    



var chart = d3.select("#chartDiv")
    .style("display", "none");
    
var bubble_chart = d3.select("#clusterDiv")
    .style("display", "none");