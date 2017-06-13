/**
 * Created by Jeremy on 26/02/2017.
 */

function plotLineChart(days, feature, tagname) {
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    // Parse the date / time
    var parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%SZ");
    var formatTime = d3.timeFormat("%H:%M:%S");

    // Set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Define the axes
    var xAxis = d3.axisBottom(x).ticks(5);

    var yAxis = d3.axisLeft(y).ticks(5);

    // Define the line
    var valueline = d3.line()
        .x(function (d) {
            return x(d.date);
        })
        .y(function (d) {
            return y(d[feature]);
        })


// Define the div for the tooltip
    var div = d3.select("#" + tagname).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

// Adds the svg canvas
    var svg = d3.select("#" + tagname)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var url = "http://sleepify.zapto.org/api/stats/last/" + days + "/" + feature + "/?format=json"
// Get the data
    d3.json(url, function (data) {
         console.log(data)

        data.forEach(function (d) {
            d.date = parseDate(d["date"]);
        });


        // Scale the range of the data
        x.domain(d3.extent(data, function (d) {
            return d.date;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d[feature];
        })]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data));

        svg.selectAll("rect")
            .data(data)
            .enter().append("rect")
            .attr("r", 2)
            .attr("fill", "transparent")
            .attr("x", function (d) {
                return x(d.date);
            })
            .attr("y", function (d) {
                return y(d[feature]) - 10;
            })
            .attr("width", width / data.length)
            .attr("height", 20)
            .on("mouseover", function (d) {
                coor = d3.mouse(this)
                div.transition()
                    .duration(200)
                    .style("opacity", .9);
                div.html("Time: " + formatTime(d.date) + "<br/>" + feature + ":  " + d[feature].toFixed(2))
                    .style("left", coor[0] + 30 + "px")
                    .style("top", (coor[1] + 28) + "px");
            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            });


        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

    });

}
