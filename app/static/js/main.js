 d3.json('data/data.json', function(data) {
            for (var i = 0; i < data.length; i++) {
                data[i] = MG.convert.date(data[i], 'date');
            }

            var all_the_data = MG.clone(data[0]);
            for (i = 1; i < data.length; i++){
                for (var j = 0; j < data[i].length; j++){
                    if (i === 3 && all_the_data[j].date < new Date('2014-02-01')) {
                    } else {
                        all_the_data[j]['value' + (i + 1)] = data[i][j].value;
                    }
                }
            }

            var markers = [{
                'date': new Date('2016-02-03T00:00:00.000Z'),
                'label': 'First sexual transmission reported'
            }, {
                'date': new Date('2016-04-14T00:00:00.000Z'),
                'label': 'CDC confirms link with Microcephaly'
            }];

            MG.data_graphic({
                title: "",
                description: "",
                data: all_the_data,
                width: 1000,
                height: 400,
                right: 40,
                left: 90,
                bottom: 50,
                y_rug: "true",
                target: '#aggregate',
                y_extended_ticks: true,
                x_accessor: 'date',
                y_accessor: ['value', 'value2', 'value3', 'value4'],
                y_label: 'Tweets',
                y_scale_type: 'log',
                min_y: 0,
                max_y: 280000,
                markers: markers,
                aggregate_rollover: true,
                mouseover: console.log(this)
            });
        });

  var colors = ['#05b378', '#f8b128', '#4040e8'];

                var margin = {top: 30, right: 20, bottom: 30, left: 40},
                    width = 250,
                    height = 250;

                var x = d3.scale.ordinal()
                    .rangeRoundBands([0, width], .1);

                var y = d3.scale.linear()
                    .range([height, 0]);

                var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom");

                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .ticks(10);

                var T1 = [2];
                var T2 = [-2];
                var T3 = [3];

                var data = [{"period": "Concern", "value": T1}, {"period": "Mistrust", "value": T2},
                    {"period": "Humor", "value": T3}];

                var svg = d3.select("#barChart").append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
                    x.domain(data.map(function(d) { return d.period; }));

                    y.domain([-5, 5]);

                    svg.append("g")
                        .attr("class", "x axis")
                        .attr("transform", "translate(0," + height + ")")
                        .call(xAxis);

                    svg.append("g")
                        .attr("class", "y axis")
                        .call(yAxis)
                        .append("text")
                        .attr("transform", "rotate(-90)")
                        .attr("y", 6)
                        .attr("dy", ".71em")
                        .style("text-anchor", "end");

                    var title = svg.append("text")
                        .attr("x", (width / 2) + 5)
                        .attr("y", 0 - (margin.top / 2))
                        .attr("text-anchor", "middle")
                        .style("font-size", "18px")
                        .text("Deviations from Average");

                    svg.selectAll(".bc_bar")
                        .data(data)
                        .enter().append("rect")
                        .attr("class", "bc_bar")
                        .attr("id", function(d){ return  d.period;})
                        .attr("x", function(d) {return x(d.period);})
                        .attr("width", x.rangeBand())
                        .attr("y", function(d) {
                            if(d.value > 0) {
                                return y(d.value)
                            }
                            else{
                                return 125;
                            }
                        })
                        .attr("height", function(d) {
                            var value = parseFloat(height)/2.0 - y(d.value);
                            if(value > 0){
                                return value;
                            }
                            else{
                                return -value;
                            }
                        })
                        .attr("fill", function(d, index){ return(colors[index])});

                 /* scope.$watch('variable', function(newValue){
                    var selected = {};
                    for( i = 0; i < scope.data.length; i++){
                        if(scope.data[i].name == newValue){
                            selected = scope.data[i];
                        }
                    }
                    svg.selectAll("#T1" + scope.cluster ).transition().attr("y", function() { return y(selected.T1[scope.cluster]); })
                                .attr("height", function(d) { return height - y(selected.T1[scope.cluster]); }).duration(1000);
                    svg.selectAll("#T2" + scope.cluster ).transition().attr("y", function() { return y(selected.T2[scope.cluster]); })
                                .attr("height", function(d) { return height - y(selected.T2[scope.cluster]); }).duration(1000);
                    svg.selectAll("#T3" + scope.cluster ).transition().attr("y", function() { return y(selected.T3[scope.cluster]); })
                                .attr("height", function(d) { return height - y(selected.T3[scope.cluster]); }).duration(1000);
                        title.text(newValue);
                }); */
