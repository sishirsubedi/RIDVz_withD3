<!DOCTYPE html>
<html>
<title>RidViz</title>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<link rel="stylesheet" href="./styles/w3.css">
<link rel="stylesheet" href="./styles/simple-style.css">
<link rel="stylesheet" href="./styles/cool_buttons.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script src="./scripts/buttons.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.11.0/d3.js"></script>
<script src="https://d3js.org/d3-queue.v3.min.js"></script>
<script src="./scripts/cluster.js"></script>
<script src="./scripts/evaluation.js"></script>
<!--<script src="./scripts/ui_options.js"></script>-->

<body>
  <div id="title" class="w3-container">
    <a class="home" href="index.php"><h1><center>RIDVz- Recognizable Image Drawing and Visualization</center></h1></a>
  </div>
    <div class="w3-container" id="mainButtons">
    <a href="#" class="btn-3d maroon " onclick="show_info()">Project Information</a>
    <a href="#" class="btn-3d maroon " onclick="show_image_menu()">Choose Object</a>
  </div>
  
  <div  id="animation">
    <svg id="welcome_1" viewBox="0 0 1000 300">
    <path class="path" fill="#FFFFFF" stroke="#000000" stroke-width="4" stroke-miterlimit="10"  d="M 159.00,114.00
            C 160.00,114.00 172.00,107.00 173.00,107.00
              174.00,107.00 184.00,93.00 184.00,93.00
              184.00,93.00 186.00,79.00 186.00,78.00
              186.00,77.00 184.00,65.00 182.00,64.00
              180.00,63.00 172.00,59.00 171.00,58.00
              170.00,57.00 156.00,55.00 156.00,55.00
              156.00,55.00 143.00,56.00 141.00,57.00
              139.00,58.00 136.00,60.00 135.00,63.00
              134.00,66.00 133.00,73.00 132.00,76.00
              131.00,79.00 132.00,90.00 133.00,92.00
              134.00,94.00 137.00,106.00 139.00,106.00
              141.00,106.00 146.00,110.00 149.00,111.00
              152.00,112.00 158.00,114.00 159.00,114.00 Z
            M 185.00,54.00
            C 185.00,54.00 207.00,39.00 207.00,39.00M 196.00,76.00
            C 196.00,76.00 224.00,70.00 224.00,70.00M 190.00,98.00
            C 190.00,98.00 216.00,108.00 216.00,108.00M 175.00,117.00
            C 175.00,117.00 186.00,137.00 186.00,137.00M 150.00,123.00
            C 150.00,123.00 147.00,147.00 147.00,147.00M 126.00,111.00
            C 126.00,111.00 114.00,133.00 114.00,133.00M 122.00,93.00
            C 121.00,93.00 91.00,105.00 91.00,105.00M 118.00,73.00
            C 118.00,73.00 84.00,74.00 84.00,74.00M 126.00,54.00
            C 126.00,54.00 98.00,39.00 98.00,39.00M 146.00,45.00
            C 146.00,45.00 138.00,24.00 138.00,24.00M 163.00,45.00
            C 163.00,45.00 173.00,23.00 173.00,23.00M 541.00,185.75
            C 541.00,185.75 554.50,185.75 554.50,185.75M 541.00,290.00
            C 541.00,290.00 540.25,184.50 540.25,184.50
              540.25,184.50 536.75,187.00 536.75,187.00
              536.75,187.00 531.50,191.00 531.50,191.00
              531.50,191.00 526.00,191.50 526.00,191.50
              526.00,191.50 521.75,189.75 521.50,189.50
              521.25,189.25 516.50,185.25 516.50,184.50
              516.50,183.75 517.25,177.50 517.50,177.25
              517.75,177.00 521.00,172.75 521.00,172.50
              521.00,172.25 525.75,170.00 525.75,169.75
              525.75,169.50 518.75,169.25 518.75,169.25
              518.75,169.25 513.50,168.50 513.00,168.00
              512.50,167.50 510.00,166.25 510.00,165.00
              510.00,163.75 509.75,160.00 510.00,159.50
              510.25,159.00 512.75,154.50 513.25,154.00
              513.75,153.50 516.75,150.25 517.00,150.25
              517.25,150.25 519.75,149.75 520.50,150.00
              521.25,150.25 523.75,150.75 524.00,150.75
              524.25,150.75 516.25,144.25 516.25,144.25
              516.25,144.25 511.25,142.25 511.00,141.25
              510.75,140.25 510.50,137.25 510.50,136.25
              510.50,135.25 510.25,133.00 511.00,132.25
              511.75,131.50 514.00,129.75 515.00,129.50
              516.00,129.25 518.25,128.50 519.00,128.50
              519.75,128.50 521.25,128.50 522.25,128.50
              523.25,128.50 525.00,130.50 525.75,130.75
              526.50,131.00 529.25,133.00 529.50,133.75
              529.75,134.50 532.00,137.25 532.00,137.50
              532.00,137.75 532.00,134.00 532.00,133.75
              532.00,133.50 530.75,129.75 531.00,129.00
              531.25,128.25 532.00,127.00 532.50,125.75
              533.00,124.50 533.00,122.50 534.25,122.00
              535.50,121.50 536.75,120.00 538.25,119.75
              539.75,119.50 542.00,119.75 542.50,119.75
              543.00,119.75 544.75,119.75 545.50,120.00
              546.25,120.25 547.25,121.25 547.75,121.75
              549.00,124.75 548.75,127.50 549.00,128.50
              549.25,129.50 549.25,130.00 549.00,131.50
              548.75,133.00 548.25,134.50 548.25,135.00
              548.25,135.50 550.50,132.50 551.00,131.50
              551.50,130.50 553.00,128.25 553.50,127.75
              554.00,127.25 554.75,126.00 556.25,126.00
              557.75,126.00 559.00,126.00 560.00,126.00
              561.00,126.00 562.25,126.00 563.00,126.00
              563.75,126.00 565.00,126.75 565.25,127.00
              565.50,127.25 570.75,131.25 570.75,131.25
              570.75,131.25 571.00,134.00 571.00,134.75
              571.00,135.50 572.00,140.00 571.75,140.25
              571.50,140.50 571.00,141.25 570.50,141.75
              570.00,142.25 569.50,142.50 568.75,143.25
              568.00,144.00 564.75,146.25 564.25,146.50
              563.75,146.75 565.75,147.25 566.75,147.25
              567.75,147.25 569.50,147.25 570.50,147.50
              571.50,147.75 574.75,148.75 575.25,149.25
              576.75,151.00 576.75,153.00 577.00,153.50
              577.00,156.25 577.50,157.25 577.00,158.25
              575.50,161.25 576.25,161.25 574.00,162.00
              570.00,163.25 570.25,163.25 568.50,163.25
              566.75,163.25 565.75,163.25 565.25,163.00
              563.50,162.25 570.00,165.50 570.50,165.75
              574.00,170.50 574.50,170.75 574.75,172.00
              570.50,180.00 570.50,180.25 569.00,180.25
              560.50,176.00 563.75,178.75 564.50,179.50
              565.25,180.25 566.00,182.25 566.75,183.25
              567.50,184.25 568.00,184.25 568.25,186.00
              568.50,187.75 568.50,193.00 568.50,193.00
              568.50,193.00 564.75,196.00 564.50,196.25
              564.25,196.50 560.25,196.75 560.00,196.75
              559.75,196.75 557.00,196.00 556.75,195.75
              556.50,195.50 555.75,194.50 555.75,194.00
              555.75,193.50 555.00,189.25 555.00,189.25
              555.00,189.25 555.25,184.75 555.25,184.75
              555.25,184.75 553.75,290.25 553.75,290.25
              553.75,290.25 543.00,290.50 543.00,290.50M 233.00,292.00
            C 233.00,292.00 233.00,189.00 233.00,189.00
              233.00,189.00 297.00,124.00 297.00,124.00
              297.00,124.00 346.00,186.00 346.00,186.00
              346.00,186.00 242.00,190.00 242.00,190.00
              242.00,190.00 349.00,291.00 349.00,291.00
              349.00,291.00 346.00,194.00 346.00,194.00
              346.00,194.00 239.00,291.00 239.00,291.00
              239.00,291.00 339.00,292.00 339.00,292.00M -8.00,293.00
            C -8.00,293.00 708.00,290.00 708.00,290.00"/> 
    </svg>
  </div>
  

  <div class="w3-container" id="project_info">
    <b> <h1><center>Project description and purpose:</center></h1></b>
    Have you ever wondered how different countries view different items? How income and other political features of a country, make the perspective of an item
    change?</br>
    How humans perceive physical objects in their mind and how their geographical and cultural background influences these decisions remain an interesting research 
    topic in various areas of sciences such as cognitive science, psychology, engineering, etc. In this project, we aim to use visualization and machine learning 
    tools to study how people from different countries describe the same object by analyzing their sketch patterns. Further, we aim to investigate relationships
    between users sketch patterns and their background. For example, we are interested to analyze how people from different countries draw sketch of a house, 
    and if there are any similarities based on culture, geography, or economic condition of the country they belong. 
    </br> 
    <b> <h1><center>Our Data:</center></h1></b>
    We got our data from Google's Quick draw project. You can find the link below: (https://quickdraw.withgoogle.com/data). </br>
    <img src="images/Quickdraw.png" class="center" width="400" height="300" ></br>
    We gathered all the sketches for the 5 different object we have chosen to analyze, and we have
    developed algorithms for those objects to gather the finding that we have accomplished in this project. You are welcome to look over the data set to see the amount of data that we have been able to analyze.
    </br> 
    <b> <h1><center>How to use our tool:</center></h1></b>
    Our tool is very simple to use... In the beginning you are given 2 options: one to select either project information (in which you are now) and the other is to choose and Object.
    If you select "choose object" it will give you the five choices we have chosen to evaluate: Cake, Dog, House, Tornado and Face. When you select the object you are interested in,
    you are given 3 options: to see the world map which shows the view summary for that country for that object, or the cluser view which with the use of Machine Learning techniques,
    we were able to see how the perespectives of ceratin countries where similar, or the evaluation view.
    </br> 
    <b> <h1><center>Project Team:</center></h1></b>
    Our project team was composed of 3 people: </br>
    <img src="images/Nishant.png" class="center" width="250" height="300" ></br>
    Nishant was the person that came up with the idea of analyzing this dataset, and the outcome that we could provide. He had awesome ideas on how we could analyze the sketches and the dataset.
    </br>
    <img src="images/Sishir.png" class="center" width="250" height="300"></br>
    Sishir was a great addition to our team, as he had the most experience with Machine Learning. He was able to develop algorithms needed for the analysis of the dataset, and ways to cluser the objects together.
    </br>
    <img src="images/Johana.png" class="center" width="250" height="300"></br>
    And last but not least, Johana. She was the person that developed the map view of the analysis. She also helped in developing our site.
  </div>
  
  <div class="w3-container" id="image_menu">
    <center>
  
    <div class="hvrbox" id="cake" onclick="show_map_cluster_menu('cake')">
        <img src="/images/cake.png" alt="Cake" class="hvrbox-layer_bottom">
        <div class="hvrbox-layer_top">
		      <div class="hvrbox-text">Cake</div>
	      </div>
    </div>
    
     <div class="hvrbox" id="dog" onclick="show_map_cluster_menu('dog')">
        <img src="/images/dog.png" alt="Dog" class="hvrbox-layer_bottom">
        <div class="hvrbox-layer_top">
		      <div class="hvrbox-text">Dog</div>
	      </div>
    </div>
    
    <div class="hvrbox" id="house" onclick="show_map_cluster_menu('house')">
        <img src="/images/house.png" alt="house" class="hvrbox-layer_bottom">
        <div class="hvrbox-layer_top">
		      <div class="hvrbox-text">House</div>
	      </div>
    </div>
    
    <div class="hvrbox" id="hurricane" onclick="show_map_cluster_menu('tornado')">
        <img src="/images/hurricane.png" alt="hurricane" class="hvrbox-layer_bottom">
        <div class="hvrbox-layer_top">
		      <div class="hvrbox-text">Hurricane</div>
	      </div>
    </div>
    
    <div class="hvrbox" id="face" onclick="show_map_cluster_menu('face')">
        <img src="/images/myface.png" alt="face" class="hvrbox-layer_bottom">
        <div class="hvrbox-layer_top">
		      <div class="hvrbox-text">Face</div>
	      </div>
    </div>
    </center>
    
  </div>
  
    <div class="w3-container" id="map_cluster_choice_btns">
      <img src="/images/myface.png" id="selected_image">
    <a href="#" class="btn-3d maroon " onclick="show_map()">Representative World Map</a>
    <a href="#" class="btn-3d maroon " onclick="show_cluster()">Country Clusters</a>
    <a href="#" class="btn-3d maroon " onclick="show_evaluation()">Evaluation</a>
    
  </div>
  
  
  <div class="w3-container"  id="chartDiv">
     <div class="details w3-container">
        <h2 class="country"></h2>
        <div id="drawing"> </div>
      </div>
  </div>
  
  
<script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script src="./scripts/load_map.js"></script>


<div class="w3-container"  id="clusterDiv">
<div id="cluster_options">
  <select id="cluster_dropdown" onchange="show_cluster()">
    <option value="Geo_Cluster">All features</option>
    <option value="direction">Direction</option>
    <option value="time">Time</option>
  </select>
  <div style="display: block;">
    <span>
      <label><input class="w3-radio cluster_grouping" id="combine" type="radio" name="grouping" value="combine" checked>Combine</label>
      <label><input class="w3-radio cluster_grouping" id="cluster" type="radio" name="grouping" value="cluster">Cluster</label>
      <label><input class="w3-radio cluster_grouping" id="country-centers" type="radio" name="grouping" value="country-centers">World Map</label>
    </span>
    &nbsp;&nbsp;&nbsp;&nbsp;
    <span>
      <label><input class="w3-radio" id="colors" type="radio" name="fill" value="color-view" checked>color-view</label>
      <label><input class="w3-radio" id="flags" type="radio" name="fill" value="flag-view">flag-view</label>
    </span>
  </div>
</div>
<div id="country-info"></div>
<div id="bubble-chart" style="margin-top:2%;"></div>
<div class="infobox" style="visibility: hidden;">
  <h3 class="title">Country</h3>
</div>


</div>


<div class="w3-container"  id="evalDiv">
    <center>
    <a href="#" class="evalbutton" onclick="load_evaluation('dog')">Dog</a>
    <a href="#" class="evalbutton" onclick="load_evaluation('house')">House</a>
    <a href="#" class="evalbutton" onclick="load_evaluation('tornado')">Tornado</a>
    <a href="#" class="evalbutton" onclick="load_evaluation('face')">Face</a>
    <a href="#" class="evalbutton" onclick="load_evaluation('cake')">Cake</a>
    
    <div id="barchart"></div>

    </center>
         
  </div>
  
</body>
</html>
