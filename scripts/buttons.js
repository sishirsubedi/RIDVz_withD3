function show_info() {
    document.getElementById("project_info").style = "display: block;";
    document.getElementById("animation").style = "display: none;";
    document.getElementById("image_menu").style = "display: none;";
    document.getElementById("chartDiv").style = "display: none;";
    document.getElementById("clusterDiv").style = "display: none;";
    //document.getElementById("clusterDiv").style = "visibility: hidden;";
    
}
function show_image_menu() {
    document.getElementById("image_menu").style = "display: block;";
    document.getElementById("project_info").style = "display: none;";
    document.getElementById("animation").style = "display: none;";
    //document.getElementById("clusterDiv").style = "visibility: visible;";
}
