//var w = window.innerWidth;
//var h = window.innerHeight;

var w = $( 'div.a' ).width();
var h = $( 'div.a' ).height()*0.1;

var focus_node = null
var text_center = false;
var size = d3.scale.pow().exponent(1)
  .domain([1,100])
  .range([1,100]);

//var tooltip = Tooltip("vis-tooltip", 400);
//var tool = tooltip;

var force = d3.layout.force()
    .gravity(0.07)   //가운데로 모이는 정도 숫자가 클수록 모인다.
    .charge(-2000)   //가운데로 모이는 정도.서로 달라붙는 정도 숫자가 클수록
    .linkDistance(0)// link 길이
    .friction(0.95)  //흐물거리는 정도
    .size([w,h]);
var color = d3.scale.linear()
    .domain([0, 1, 2, 3])
    .range(["#fffa30", "#fffbb6", "#ffffec", "#fff88e"]);
var nominal_base_node_size = 15;
var nominal_text_size = 6;
var max_text_size = 24;
var nominal_stroke =4;
var max_stroke = 15;
var max_base_node_size = 80;
var min_zoom = 0.5;
var max_zoom = 100;
var svg = d3.select(".a").append("svg");
var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])
var g = svg.append("g");

// Load JSON by input and output name. e.g. C0001_C0002.json by bnmin on Jul 23, 2015

var json_file = 'json/' + input + '_' + output + '.json';

d3.json(json_file, function(error, json) {
  if (error) throw error;

  force
      .nodes(json.nodes)
      .links(json.links)
      .on("tick", tick)
      .start();

  var link = g.selectAll(".link")
      .data(json.links)
      .enter().append("line")
      .attr("class", "link")
      .attr("marker-end", "url(#end)")
  	  .style("stroke-width",nominal_stroke);      

//Set up tooltip
var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function (d) {
    return  d.chemical_name + "";
})
svg.call(tip);


      
  var labels = g.selectAll("text")
    .data(json.links)
  .enter().append("text")
    .attr("class", "linktext")
    .attr("x", function(d) { return (d.source.y + d.target.y) / 2; }) 
    .attr("y", function(d) { return (d.source.x + d.target.x) / 2; }) 
    .attr("text-anchor", "middle") 
    .style("font-size", nominal_text_size + "px")
    .text(function(d) { return d.reaction }); 

  var node = g.selectAll(".node")
      .data(json.nodes)
      .enter().append("g")
      .attr("class", "node")
      .call(force.drag)
      .style("fill", function(d) { return color(d.degree);}) 
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
//      .on('dblclick', connectedNodes);
//  node.append("circle")
//      .attr("r", function (d) {
//      return ((d.path1 + d.path2 + d.path3)*3 + 7);
//      });
//      function (d) {
//      return color(d.path1 + d.path2 + d.path3);
//      })
//  node.append("text")
//      .attr("dx", 17)
//      .attr("dy", ".21em")
//      .text(function(d) { return d.name });

  var circle = node.append("path")
      .attr("d", d3.svg.symbol()
      .size(function(d) { return Math.PI*Math.pow(size(d.size)||nominal_base_node_size,2); })
      .type(function(d) { return d.type; }))
/*  
  var text = g.selectAll(".text")
    .data(json.nodes)
    .enter().append("text")
    .attr("dy", ".21em")
    .attr("dx", "-1.5em")
	.style("font-size", nominal_text_size*1.2 + "px")
    .text(function(d) { return d.name })
    .style("pointer-events","none");
 */
  zoom.on("zoom", function() {
  
  var stroke = nominal_stroke;
    if (nominal_stroke*zoom.scale()>max_stroke) stroke = max_stroke/zoom.scale();
    link.style("stroke-width",stroke);
    circle.style("stroke-width",stroke);
	   
  var base_radius = nominal_base_node_size;
    if (nominal_base_node_size*zoom.scale()>max_base_node_size) base_radius = max_base_node_size/zoom.scale();
        circle.attr("d", d3.svg.symbol()
        .size(function(d) { return Math.PI*Math.pow(size(d.size)*base_radius/nominal_base_node_size||base_radius,2); })
        )
		

	g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
	});
	 
  svg.call(zoom);	  
	
  resize();
  window.focus();    
      
      
  function tick(e) {


    var k = 30 * e.alpha;
    json.links.forEach(function(d, i) {
      d.source.y -= k;
      d.target.y += k;
    });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    labels.attr("x", function(d) { return (d.source.x + d.target.x) / 2; }) 
        .attr("y", function(d) { return (d.source.y + d.target.y) / 2; });     
    link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });
		
    node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });


  };
  //---Insert-------for direction
svg.append("svg:defs").selectAll("marker")
    .data(["end"])
  .enter().append("svg:marker")
    .attr("id", String)
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", 0)
    .attr("markerWidth", 4)
    .attr("markerHeight", 4)
    .attr("orient", "auto")
  .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5")
    .style("fill", "#D8D8D8")    
    .style("stroke", "#FFFFFF")
    .style("stroke-opacity", "0.1")
    .style("stroke-width", "1.3px");
//---endInsert-------
  
  function resize() {
    var width = $( 'div.a' ).width(), height = $( 'div.a' ).height()*0.90;
	svg.attr("width", width).attr("height", height);
    
	force.size([force.size()[0]+(width-w)/zoom.scale(),force.size()[1]+(height-h)/zoom.scale()]).resume();
    w = width;
	h = height;
	};  
  




// ---Insert-------for chemical, reaction information
function showinfo(d) {
  var header1 = document.getElementById('info');
			
		info.innerHTML = '<iframe src="C_info_html/' + d.name + '.html" width=100% height=310px marginwidth="0" marginheight="0" scrolling="overflow-x:hidden" frameborder="0" scrolling="no" ></iframe>' ;
};

function showlinkinfo(d) {
  var header2 = document.getElementById('linkinfo');
			
		linkinfo.innerHTML = '<embed src="R_info_html/' + d.reaction + '.html" width=100% height=310px marginwidth="0" marginheight="0" scrolling="overflow-x:hidden" frameborder="0" scrolling="no" ></embed>' ;

};


var circles = g.selectAll("path");
circles.on("click", showinfo);
var lines = svg.selectAll("line");
lines.on("click", showlinkinfo);
// ---endInsert-------





});



// ---Insert-------for highlight pathway
var toggle = 0;
var toggle2 = 0;
var toggle3 = 0;
var ecolitoggle = 0;
var toggle4 = 0;
var toggle5 = 0;
var toggle6 = 0;
var toggle7 = 0;
var toggle8 = 0;
var toggle9 = 0;
var toggle10 = 0;
var toggle11 = 0;
var toggle12 = 0;
function hlpath1() {
      
      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.ATP_1 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.ATP_1 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.ATP_1 != 1;
        });
      if (toggle == 0){
          var pathinfo = document.getElementById('pathway');
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle = 1;
        toggle2 = 0;
        toggle3 = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;
      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle = 0;
      }
};

function hlpath2() {
      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.ATP_2 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.ATP_2 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.ATP_2 != 1;
        });
      if (toggle2 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle2 = 1;
        toggle = 0;
        toggle3 = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;

      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle2 = 0;
      }
  };

function hlpath3() {
      
      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.ATP_3 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.ATP_3 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.ATP_3 != 1;
        });
      if (toggle3 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 1;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle3 = 0;
      }
  };  
var hlecoli = function() {
      
      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = link.filter(function (d, i) {
            return d.ecoli != 0;
        });
        var unselected = link.filter(function (d, i) {
            return d.ecoli != 1;
        });
      if (ecolitoggle == 0){
        selected.style("fill", "#1E96FF");
        selected.style("stroke", "#1E96FF");
        ecolitoggle = 1;
      } else {
        //put them back to
        d3.selectAll(".link").style("stroke", "#D8D8D8");
        ecolitoggle = 0;
      }
  };


function hlpath4() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.CO2_1 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.CO2_1 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.CO2_1 != 1;
        });
      if (toggle4 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 1;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle4 = 0;
      }
  };
function hlpath5() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.CO2_2 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.CO2_2 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.CO2_2 != 1;
        });
      if (toggle5 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 1;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle5 = 0;
      }
  };
function hlpath6() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.CO2_3 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.CO2_3 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.CO2_3 != 1;
        });
      if (toggle6 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 1;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle6 = 0;
      }
  };
function hlpath7() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADH_1 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADH_1 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADH_1 != 1;
        });
      if (toggle7 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 1;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle7 = 0;
      }
  };
function hlpath8() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADH_2 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADH_2 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADH_2 != 1;
        });
      if (toggle8 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 1;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle8 = 0;
      }
  };
function hlpath9() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADH_3 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADH_3 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADH_3 != 1;
        });
      if (toggle9 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 1;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle9 = 0;
      }
  };
function hlpath10() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADPH_1 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADPH_1 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADPH_1 != 1;
        });
      if (toggle10 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 1;
        toggle11 = 0;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle10 = 0;
      }
  };
function hlpath11() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADPH_2 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADPH_2 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADPH_2 != 1;
        });
      if (toggle11 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 1;
        toggle12 = 0;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle11 = 0;
      }
  };
function hlpath12() {

      var node = svg.selectAll(".node");
      var link = svg.selectAll(".link");
        var selected = node.filter(function (d, i) {
            return d.NADPH_3 != 0;
        });
        var unselectedlink = link.filter(function (d, i) {
            return d.NADPH_3 != 1;
        });
        var unselected = node.filter(function (d, i) {
            return d.NADPH_3 != 1;
        });
      if (toggle12 == 0){
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        unselected.style("opacity", "0.1");
        unselectedlink.style("opacity", "0.1");
        toggle3 = 0;
        toggle2 = 0;
        toggle = 0;
        toggle4 = 0;
        toggle5 = 0;
        toggle6 = 0;
        toggle7 = 0;
        toggle8 = 0;
        toggle9 = 0;
        toggle10 = 0;
        toggle11 = 0;
        toggle12 = 1;




      } else {
        //put them back to
        d3.selectAll(".node").style("opacity", "1");
        d3.selectAll(".link").style("opacity", "1");
        toggle12 = 0;
      }
  };



  

// ---endInsert------- for highlight
