
;(function() {

  console.log("starting page...")

  var data;
  var dataXRange = { min: 0, max: 100 };
  var dataYRange = { min: 0, max: 100 };
   
   var width = 800;
   var height = 500;
   var circleRadius =100;


   var svg = d3.select("body")
   				.append("svg")
   				.attr("width", width)
   				.attr("height",height)
   				.append("g")


  //   d3.json("./data/clusters2.json", function(error, json) {
		// 	if (error) {
		// 		return console.warn("error",error);
		// 	} else {
		// 		data = json;
		// 	}
		// })

data = [1,2,3]
var circle = svg.selectAll("circle")
			.data(data)
			.enter().append("circle")
        .attr("r", circleRadius)
        .attr("cx", function (d) { return d*100+50 })
        .attr("cy", function (d) { return d*10 + 100 })
        .style("fill", "red")// function(d) { return color(d.cluster); })
       

	})();