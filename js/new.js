function gridData(widthCanvas, heightCanvas) {
    var data = new Array();
    var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
    var ypos = 1;
    var width = widthCanvas/10;
    var height = heightCanvas/10;

    // iterate for rows
    for (var row = 0; row < 10; row++) {
        data.push( new Array() );

        // iterate for cells/columns inside rows
        for (var column = 0; column < 10; column++) {
            if(row==0 || row ==1 && column < 2){
				data[row].push({
                x: xpos,
                y: ypos,
                width: width,
				height:height,
				image:"images/green.svg"
			})
			}else{
				data[row].push({
                x: xpos,
                y: ypos,
                width: width,
				height:height,
				image:"images/black.svg"
            })}
            // increment the x position. I.e. move it over by 50 (width variable)
            xpos += width;
        }
        // reset the x position after a row is complete
        xpos = 1;
        // increment the y position for the next row. Move it down 50 (height variable)
        ypos += height;
    }
    return data;
}

function animateGrid(){
  var men = d3.selectAll(".men")
              .transition()
              .delay(function(d,i) { return i * 50; })
              .duration(50)
              .style('opacity', 1);
}


var grid = d3.select("#people-grid");


console.log(gridData);
var gridData = gridData(parseInt(grid.style("width").replace("px","")),parseInt(grid.style("height").replace("px","")));
// I like to log the data to the console for quick debugging
console.log(gridData);


var row = grid.selectAll(".row")
    .data(gridData)
    .enter().append("g")
    .attr("class", "row");

var column = row.selectAll(".men")
    .data(function(d) { return d; })
    .enter().append("svg:image")
    .attr("class","men")
	.attr("xlink:href", function(d){return d.image;})
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return d.y; })
    .attr("width", function(d) { return d.width; })
	.attr("height", function(d) { return d.height; });


  var men = d3.selectAll(".men")
              .style('opacity', 0);
