//
// Copyright 2015 Benjamin David Holmes, All rights reserved.
//

// Modified from http://bl.ocks.org/mbostock/3884955#index.html
function drawAveragePricesGraph(dataUrl) {
	var margin = {top: 20, right: 80, bottom: 30, left: 60},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;

	var parseDate = d3.time.format("%Y-%m-%d").parse;

	var x = d3.time.scale()
		.range([0, width]);

	var y = d3.scale.linear()
		.range([height, 0]);

	var color = d3.scale.category10();

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom");

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	var line = d3.svg.line()
		.interpolate("cardinal")
		.x(function(d) { return x(d.date); })
		.y(function(d) { return y(d.price); })
		.defined(function(d) { return d.price; });

	var svg = d3.select("#average").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	  .append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.tsv(dataUrl, function(error, data) {
	  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

	  data.forEach(function(d) {
		d.date = parseDate(d.date);
	  });

	  var propertyTypes = color.domain().map(function(name) {
		return {
		  name: name,
		  values: data.map(function(d) {
			return {date: d.date, price: +d[name]};
		  })
		};
	  });

	  x.domain(d3.extent(data, function(d) { return d.date; }));

	  y.domain([
		d3.min(propertyTypes, function(c) { return d3.min(c.values, function(v) { return v.price; }); }),
		d3.max(propertyTypes, function(c) { return d3.max(c.values, function(v) { return v.price; }); })
	  ]);

	  var propertyType = svg.selectAll(".propertyType")
		  .data(propertyTypes)
		  .enter().append("g")
		  .attr("class", "propertyType");

	  propertyType.append("path")
		  .attr("class", "line")
		  .attr("d", function(d) { return line(d.values); })
		  .style("stroke", function(d) { return color(d.name); });

	  var point = propertyType.append("g")
		  .attr("class", "line-point");

		point.selectAll('circle')
		.data(function(d){ return d.values})
		.enter().append('circle')
		.attr("cx", function(d) { return x(d.date) })
		.attr("cy", function(d) { return y(d.price) })
		.attr("r", 3.5)
		.style("fill", "white")
		.style("stroke", function(d) { return color(this.parentNode.__data__.name); })
		.style("visibility", function(d) { return d.price > 0 ? "visible" : "hidden" });

	  propertyType.append("text")
		  .datum(function(d) { return {name: d.name, value: getLastValue(d.values)}; })
		  .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.price) + ")"; })
		  .attr("x", 5)
		  .attr("dy", ".35em")
		  .style("font-weight", "bold")
		  .text(function(d) { return d.name; });

	  svg.append("g")
		  .attr("class", "x axis")
		  .attr("transform", "translate(0," + height + ")")
		  .call(xAxis)

	  svg.append("g")
		  .attr("class", "y axis")
		  .call(yAxis)
		.append("text")
		  .attr("transform", "rotate(-90)")
		  .attr("y", 6)
		  .attr("dy", ".71em")
		  .style("text-anchor", "end")
		  .style("font-weight", "bold")
		  .text("Price (£)");
	});
}

function getLastValue(values) {
	for(i = values.length - 1; i > 0; i--) {
		if(values[i].price > 0) {
			return values[i];
		}
	}
	return 0;
}