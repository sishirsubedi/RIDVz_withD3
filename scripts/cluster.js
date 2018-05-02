// var simulation;
function clusterOption() {
  // var ele = document.getElementById("cluster_dropdown");
  // var option = ele.options[ele.selectedIndex].value;
  // console.log(option);
  // return option;
  d3.select("#bubble-chart svg").remove();
  var ele = document.getElementById("selected_image");
  var curr = ele.getAttribute("data-current");
  var fileName = "data/1_" + curr + "_cluster.csv";
  d3.queue()
      .defer(d3.csv, fileName)
      // .defer(d3.json, "data/continent-names.json")
      .await(createBubbleChart);
}

function show_cluster() {
  
    document.getElementById("chartDiv").style = "display: none;";
    document.getElementById("clusterDiv").style = "display: block;";
    document.getElementById("evalDiv").style = "display: none;";
    
    var ele = document.getElementById("selected_image");
    var curr = ele.getAttribute("data-current");
    
    if(!d3.select("#bubble-chart svg").empty()) {
      // simulation.stop();
      d3.select("#bubble-chart svg").remove();
    }
    
    var rad_buttons = document.getElementsByName('grouping');
    for(var i = 0; i < rad_buttons.length; i++) {
      rad_buttons[i].checked = false;
    }
    
    document.getElementById('combine').checked = true;
    
    
    var clusterType = getClusterType();
    var type;
    if(clusterType == "Geo_Cluster") {
  	  type = "_geo.csv";
  	} else if(clusterType == "direction") {
  	  type = "_direction.csv";
  	} else if(clusterType == "time") {
  	  type = "_time.csv";
  	}
    var fileName = "data/1_" + curr + type;
    var countries = [];
    var continentNames = {};
    console.log(fileName);
    d3.queue()
      .defer(d3.csv, fileName)
      // .defer(d3.json, "data/continent-names.json")
      .await(createBubbleChart);
}

function getClusterType() {
  var ele = document.getElementById("cluster_dropdown");
  var option = ele.options[ele.selectedIndex].value;
  // console.log(option);
  return option;
}

function createBubbleChart(error, dataset) {
  // var clusterType ='Geo_Cluster'
  // console.log(countries);
	var clusterType = getClusterType();

// 	console.log(clusterType);

	var populations = dataset.map(function(country) { return +country.Population; });
	var meanPopulation = d3.mean(populations),
	  populationExtent = d3.extent(populations),
	  populationScaleX,
	  populationScaleY;
      
    var domain_type = d3.set(dataset.map(function(country) { return country.Cluster; }));
    var cluster_domain = d3.nest()
        .key(function(d) { return d.Cluster; })
        .rollup(function(v) { return {
          count: v.length,
        }; })
        .entries(dataset);;
    var cluster_keys = [];

    var radios_grouping = document.getElementsByName('grouping');
    
    var grouping_option;
    
    for (var i = 0, length = radios_grouping.length; i < length; i++)
    {
  	 if (radios_grouping[i].checked)
  	 {
  	   grouping_option = radios_grouping[i].value
  	   break;
  	 }
    }
      

	for(var i = 0; i < cluster_domain.length; i++) {
      cluster_keys.push(cluster_domain[i]["key"])
    }
	// console.log(domain_type.values());

	// var domain_type = d3.set(dataset.map(function(country) { return country.Geo_Cluster; }));

	var clusterColorScale = d3.scaleOrdinal(d3.schemeCategory10)
	    .domain(domain_type.values());

	var width = 900,
	  height = 600;
	  
	var svg,
	  circles,
	  circleSize = { min: 7.5, max: 50 };
	  
	var circleRadiusScale = d3.scaleSqrt()
	.domain(populationExtent)
	.range([circleSize.min, circleSize.max]);

	var forces,
	  forceSimulation;

	createSVG();
	createCircles();
	createForces();
	createForceSimulation();
	addFlagDefinitions();
	addFillListener();
	addGroupingListeners();

	function createSVG() {
	svg = d3.select("#bubble-chart")
	  .append("svg")
	    .attr("width", width)
	    .attr("height", height);
	}



	function flagFill() {
		return isChecked("#flags");
	}

	function isChecked(elementID) {
		return d3.select(elementID).property("checked");
	}

	function createCircles() {
		var formatPopulation = d3.format(",");
		circles = svg.selectAll("circle")
		  .data(dataset)
		  .enter()
		    .append("circle")
		    .attr("r", function(d) { return circleRadiusScale(d.Population); })
		    .attr("fill",function(d) {
		      return clusterColorScale(d.Cluster);
		    })
		    .on("mouseover", function(d) {
		      // updateCountryInfo(d)
		      console.log(d.CountryName)
		      d3.select(".infobox .title").text(d.CountryName);
		      d3.select(".infobox").style('visibility', 'visible');
		      
		    })
		    .on("mouseout", function(d) {
		      // updateCountryInfo();
		      d3.select(".infobox").style('visibility', 'hidden');
		    });

		updateCircles();

		function updateCountryInfo(country) {
		  var info = "";
		  if (country) {
		    info = [country.CountryName, formatPopulation(country.Population)].join(": ");
		  }
		  d3.select("#country-info").html(info)
		}
	}

	function updateCircles() {
		circles
		  .attr("fill", function(d) {
		    return flagFill() ? "url(#" + d.CountryCode + ")" : clusterColorScale(d.Cluster);
		  });
		  
	}

	function createForces() {
		var forceStrength = 0.05;//controls how fast circles transit

		forces = {
		  combine:        createCombineForces(),
		  countryCenters: createCountryCenterForces(),
		  cluster:      createContinentForces()
		};

		function createCombineForces() {
		  return {
		    x: d3.forceX(width / 2).strength(forceStrength),
		    y: d3.forceY(height / 2).strength(forceStrength)
		  };
		}

		function createCountryCenterForces() {
		  var projectionStretchY = 0.25,
		      projectionMargin = circleSize.max,
		      projection = d3.geoEquirectangular()
		        .scale((width / 2 - projectionMargin) / Math.PI)
		        .translate([width / 2, height * (1 - projectionStretchY) / 2]);

		  return {
		    x: d3.forceX(function(d) {
		        return projection([d.CenterLongitude, d.CenterLatitude])[0];
		      }).strength(forceStrength),
		    y: d3.forceY(function(d) {
		        return projection([d.CenterLongitude, d.CenterLatitude])[1] * (1 + projectionStretchY);
		      }).strength(forceStrength)
		  };
		}

		function createContinentForces() {
		  return {
		    x: d3.forceX(continentForceX).strength(forceStrength),
		    y: d3.forceY(continentForceY).strength(forceStrength)
		  };

		function continentForceX(d) {
		    var data_cluster_key;
	        var force_val;
	        var count = 1;
	        var num_rows;
	        if((cluster_keys.length%3) != 0) {
	          num_rows = Math.floor(cluster_keys.length/3) + 1;
	        } else {
	          num_rows = Math.floor(cluster_keys.length/3);
	        }
	        
	        data_cluster_key = d.Cluster;
	        
	        for(var i = 0; i < cluster_keys.length; i++) {
	          
	          if(data_cluster_key == cluster_keys[i]) {
	            force_val = (width/cluster_keys.length) * count;
	            break;
	          }
	          
	          if(count == 3) {
	            count = 1;
	          } else {
	            count++;
	          }
	        }
	        return force_val;
		  }

		  function continentForceY(d) {
		    var data_cluster_key;
	        var force_val;
	        var count = 1;
	        var num_rows;
	        if((cluster_keys.length%3) != 0) {
	          num_rows = Math.floor(cluster_keys.length/3) + 1;
	        } else {
	          num_rows = Math.floor(cluster_keys.length/3);
	        }
	        
	        console.log(num_rows);
	        
	        data_cluster_key = d.Cluster;
	       
	        
	        for(var i = 0; i < cluster_keys.length; i++) {
	          
	          if(data_cluster_key == cluster_keys[i]) {
	            force_val = (150 * (count));
	            break;
	          }
	          
	          if((count * 3) == (i + 1)) {
	            count++;
	          }
	        }
	        return force_val;
		  }

		}

	}

	function createForceSimulation() {
		forceSimulation = d3.forceSimulation()
		  .force("x", forces.combine.x)
		  .force("y", forces.combine.y)
		  .force("collide", d3.forceCollide(forceCollide));
		forceSimulation.nodes(dataset)
		  .on("tick", function() {
		    circles
		      .attr("cx", function(d) { return d.x; })
		      .attr("cy", function(d) { return d.y; });
		  });
	}

	function forceCollide(d) {
		return circleRadiusScale(d.Population) + 1;
	}

	function countryCenterGrouping() {
		return isChecked("#country-centers");
	}

	function addFlagDefinitions() {
		var defs = svg.append("defs");
		defs.selectAll(".flag")
		  .data(dataset)
		  .enter()
		    .append("pattern")
		    .attr("id", function(d) { return d.CountryCode; })
		    .attr("class", "flag")
		    .attr("width", "100%")
		    .attr("height", "100%")
		    .attr("patternContentUnits", "objectBoundingBox")
		      .append("image")
		      .attr("width", 1)
		      .attr("height", 1)
		      // xMidYMid: center the image in the circle
		      // slice: scale the image to fill the circle
		      .attr("preserveAspectRatio", "xMidYMid slice")
		      .attr("xlink:href", function(d) {
		        return "flags/" + d.CountryCode + ".svg";
		      });
	}

	function addFillListener() {
	d3.selectAll('input[name="fill"]')
	  .on("change", function() {
	   // toggleContinentKey(!flagFill() && !populationGrouping());
	    updateCircles();
	  });
	}

	function addGroupingListeners() {
		addListener("#combine",         forces.combine);
		addListener("#country-centers", forces.countryCenters);
		addListener("#cluster",         forces.cluster);

		function addListener(selector, forces) {
		  d3.select(selector).on("click", function() {
		    updateForces(forces);
		    // toggleContinentKey(!flagFill() && !populationGrouping());
		    // togglePopulationAxes(populationGrouping());
		  });
		}

		function updateForces(forces) {
		  forceSimulation
		    .force("x", forces.x)
		    .force("y", forces.y)
		    .force("collide", d3.forceCollide(forceCollide))
		    .alphaTarget(0.5)
		    .restart();
		}

	}

}
