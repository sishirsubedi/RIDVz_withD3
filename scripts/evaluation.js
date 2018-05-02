function show_evaluation() {
    document.getElementById("chartDiv").style = "display: none;";
    document.getElementById("clusterDiv").style = "display: none;";
    document.getElementById("evalDiv").style = "display: block;";
    // document.getElementById("selected_image").style = "display: none;";
}

function load_evaluation(input_image){
    
    
    console.log(input_image)
    
    
// set the dimensions and margins of the graph
var margin = {top: 40, right: 40, bottom: 30, left: 40};
  var width = 1280,
      height = 600;
var padding = 100; 

// set the ranges
var x = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
var y = d3.scaleLinear()
          .range([height, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#evalDiv").append("svg")
    .attr('id','barchart')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

// get the data
d3.csv("./data/cluster_evaluation2.csv", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
    d.Score = +d.Score;
  });

  // Scale the range of the data in the domains
  x.domain(data.map(function(d) { return d.Continent_Cluster; }));
  y.domain([0, d3.max(data, function(d) { return d.Score; })]);

  // append the rectangles for the bar chart
  svg.selectAll(".bar")
      .data(data)
      .data(data.filter(function(d){return d.image_object == input_image;}))
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.Continent_Cluster); })
      .attr("width", x.bandwidth())
      .attr("y", function(d) { return y(d.Score); })
      .attr("height", function(d) { return height - y(d.Score); })
      .attr("fill", function(d) { 
          
          if (input_image =='house'){
              return "#9F6687";
          }
          else if (input_image=='cake'){
        return "#535D27";
           }
        else if (input_image=='dog'){
        return "#956233";
           }
       else if (input_image=='tornado'){
        return "#1B625E";
           }
    else if (input_image == 'face'){
        return "#68353C";
           }
          
    
    
    
      });
  
  
  // add the x Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
      
  // add the y Axis
  svg.append("g")
      .call(d3.axisLeft(y));
  
        //   // now add titles to the axes
        // svg.append("text")
        //     .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
        //     .text("Value");

        // svg.append("text")
        //     .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
        //     .attr("transform", "translate("+ (width) +","+(height-(padding))+")")  // centre below axis
        //     .text("Date");
            
  
  
  d3.select("#barchart").remove();

});
    
}
