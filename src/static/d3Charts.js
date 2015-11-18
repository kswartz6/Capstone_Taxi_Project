//D3 histogram of region passenger count

function createBar(data){
	var record = [];
	console.log(data)
	var taxiData = data;
		for (i in data){
			record[i] = data[i].passenger_count;
		}
		console.log("printing record");
	console.log(record);
	var values = record;


	// A formatter for counts.
	var formatCount = d3.format(",.0f");

	var margin = {top: 10, right: 30, bottom: 30, left: 30},
	    width = 500 - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;

	var x = d3.scale.linear()
	    .domain([0, 10])
	    .range([0, width]);

	// Generate a histogram using twenty uniformly-spaced bins.
	var data = d3.layout.histogram()
	    .bins(x.ticks(20))
	    (values);

	var y = d3.scale.linear()
	    .domain([0, d3.max(data, function(d) { return d.y; })])
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var svg = d3.select("#barChart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var bar = svg.selectAll(".bar")
	    .data(data)
	  .enter().append("g")
	    .attr("class", "bar")
	    .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

	bar.append("rect")
	    .attr("x", 1)
	    .attr("width", x(data[0].dx) - 1)
	    .attr("height", function(d) { return height - y(d.y); });

	bar.append("text")
	    .attr("dy", ".75em")
	    .attr("y", 6)
	    .attr("x", x(data[0].dx) / 2)
	    .attr("text-anchor", "middle")
	    .text(function(d) { return formatCount(d.y); });

	svg.append("g")
	    .attr("class", "x axis")
	    .attr("transform", "translate(0," + height + ")")
	    .call(xAxis);
}

//D3 Donut Chart of passenger_count

function createDonutChart(data){
	var record = [];

		for (i = 0, l = data.length; i < l; ++i){
			record[i] = data[i].passenger_count;
		}

		var One = 0;
		var Two = 0;
		var Three = 0;
		var Four = 0;
		var Five = 0;
		var Six = 0;

	for (i = 0, l = record.length; i < l; ++i){
			switch(record[i]){
	 			case 1:
			 		++One;
			 		break;
	 			case 2:
			 		++Two
			 		break;
	 			case 3:
			 		++Three;
			 		break;
	 			case 4:
			 		++Four;
			 		break;
	 			case 5:
			 		++Five;
			 		break;
	 			case 6:
			 		++Six;
			 		break;
			}
		}
		console.log(One);
        var dataset = [
					{ label: 'One', count: One },
					{ label: 'Two', count: Two },
					{ label: 'Three', count: Three },
					{ label: 'Four', count: Four },
					{ label: 'Five', count: Five },
					{ label: 'Six', count: Six }
				];
				console.log(dataset);

        var width = 360;
        var height = 360;
        var radius = Math.min(width, height) / 2;
				var donutWidth = 75;
				var legendRectSize = 18;
				var legendSpacing = 4;

        var color = d3.scale.category20b();

        var svg = d3.select('#donutChart')
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .append('g')
          .attr('transform', 'translate(' + (width / 2) +
            ',' + (height / 2) + ')');

        var arc = d3.svg.arc()
					.innerRadius(radius - donutWidth)
          .outerRadius(radius);

        var pie = d3.layout.pie()
          .value(function(d) { return d.count; })
          .sort(null);


        var tooltip = d3.select('#donutChart')
          .append('div')
          .attr('class', 'tooltip');

        tooltip.append('div')
          .attr('class', 'label');

        tooltip.append('div')
          .attr('class', 'count');

        tooltip.append('div')
          .attr('class', 'percent');


        var path = svg.selectAll('path')
          .data(pie(dataset))
          .enter()
          .append('path')
          .attr('d', arc)
          .attr('fill', function(d, i) {
            return color(d.data.label);
          });
					path.on('mouseover', function(d) {
            var total = d3.sum(dataset.map(function(d) {
              return d.count;
            }));
            var percent = Math.round(1000 * d.data.count / total) / 10;
            tooltip.select('.label').html(d.data.label);
            tooltip.select('.count').html(d.data.count);
            tooltip.select('.percent').html(percent + '%');
            tooltip.style('display', 'block');
          });

          path.on('mouseout', function() {
            tooltip.style('display', 'none');
          });

			var legend = svg.selectAll('.legend')
				.data(color.domain())
				.enter()
				.append('g')
				.attr('class', 'legend')
				.attr('transform', function(d, i) {
					var height = legendRectSize + legendSpacing;
					var offset =  height * color.domain().length / 2;
					var horz = -2 * legendRectSize;
					var vert = i * height - offset;
					return 'translate(' + horz + ',' + vert + ')';
				});

			legend.append('rect')
				.attr('width', legendRectSize)
				.attr('height', legendRectSize)
				.style('fill', color)
				.style('stroke', color);

			legend.append('text')
				.attr('x', legendRectSize + legendSpacing)
				.attr('y', legendRectSize - legendSpacing)
				.text(function(d) { return d; });

      }
