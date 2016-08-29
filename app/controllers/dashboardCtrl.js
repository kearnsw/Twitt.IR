var dashboard = angular.module('dashboard', ['dateSlider']);
dashboard.controller('dashboardController', function($scope, $location) {

      $scope.$watch('dateValue', function(newValue){

            /* Get sample of tweets to display */
            $.ajax({
                url: 'http://127.0.0.1:2112/getTweets',
                type: 'POST',
                crossDomain: true,
                data: {'date': newValue, 'concept': "concern"},
                error: function (request, status, error) {
                    console.log(request.responseText);
                    console.log(error);
                },
                success: function (response) {
                    console.log(response);
                    $("#concernTweet").text(response);
                }
            });

            $.ajax({
                url: 'http://127.0.0.1:2112/getTweets',
                type: 'POST',
                crossDomain: true,
                data: {'date': newValue, 'concept': "mistrust"},
                error: function (request, status, error) {
                    console.log(request.responseText);
                    console.log(error);
                },
                success: function (response) {
                    console.log(response);
                    $("#mistrustTweet").text(response);
                }
            });

            $.ajax({
                        url: 'http://127.0.0.1:2112/getTweets',
                        type: 'POST',
                        crossDomain: true,
                        data: {'date': newValue, 'concept': "humor"},
                        error: function (request, status, error) {
                            console.log(request.responseText);
                            console.log(error);
                        },
                        success: function (response) {
                            console.log(response);
                            $("#humorTweet").text(response);
                        }
                    });

            $.ajax({
                        url: 'http://127.0.0.1:2112/getCount',
                        type: 'POST',
                        crossDomain: true,
                        data: {'date': newValue, 'concept': "total"},
                        error: function (request, status, error) {
                            console.log(request.responseText);
                            console.log(error);
                        },
                        success: function (response) {
                            console.log(response);
                            $("#totalTweets").text(response);
                            var total = response;


                            $.ajax({
                                url: 'http://127.0.0.1:2112/getCount',
                                type: 'POST',
                                crossDomain: true,
                                data: {'date': newValue, 'concept': "concern"},
                                error: function (request, status, error) {
                                    console.log(request.responseText);
                                    console.log(error);
                                },
                                success: function (response) {
                                    var frequency = parseInt(response) / parseInt(total);
                                    var deviation = parseFloat(frequency) / 0.11094;
                                    if(deviation < 1){
                                                deviation = -1 * (parseFloat(1) / deviation)
                                            }
                                    $scope.concernDeviation = {"value": deviation};
                                    $scope.$apply();
                                }
                            });

                            $.ajax({
                                        url: 'http://127.0.0.1:2112/getCount',
                                        type: 'POST',
                                        crossDomain: true,
                                        data: {'date': newValue, 'concept': "humor"},
                                        error: function (request, status, error) {
                                            console.log(request.responseText);
                                            console.log(error);
                                        },
                                        success: function (response) {
                                            var frequency = parseInt(response) / parseInt(total);
                                            var deviation = parseFloat(frequency) / 0.0064128;
                                            if(deviation < 1){
                                                deviation = -1 * (parseFloat(1) / deviation)
                                            }
                                            $scope.humorDeviation = {"value": deviation};
                                            $scope.$apply();
                                        }
                                    });

                            $.ajax({
                                        url: 'http://127.0.0.1:2112/getCount',
                                        type: 'POST',
                                        crossDomain: true,
                                        data: {'date': newValue, 'concept': "mistrust"},
                                        error: function (request, status, error) {
                                            console.log(request.responseText);
                                            console.log(error);
                                        },
                                        success: function (response) {
                                            var frequency = parseInt(response) / parseInt(total);
                                            var deviation = parseFloat(frequency) / 0.00916378;
                                            if(deviation < 1){
                                                deviation = -1 * (parseFloat(1) / deviation)
                                            }

                                            $scope.mistrustDeviation = {"value": deviation};
                                            $scope.$apply();
                                        }
                                    });
                        }
                    });


          });

    d3.json('data/data.json', function (data) {

        for (var i = 0; i < data.length; i++) {
            data[i] = MG.convert.date(data[i], 'date');
        }

        var all_the_data = MG.clone(data[0]);
        for (i = 1; i < data.length; i++) {
            for (var j = 0; j < data[i].length; j++) {
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
            aggregate_rollover: true
        });
    });

});
dashboard.directive('barChart', function() {
        return {
            restrict: 'E',
            scope: {
                humor: "=",
                concern: "=",
                mistrust: "="
            },
            link: function (scope, elem) {

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

                var svg = d3.select(elem[0]).append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
                x.domain(data.map(function (d) {
                    return d.period;
                }));

                y.domain([-10, 10]);

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
                    .attr("id", function (d) {
                        return d.period;
                    })
                    .attr("x", function (d) {
                        return x(d.period);
                    })
                    .attr("width", x.rangeBand())
                    .attr("y", function (d) {
                        if (d.value > 0) {
                            return y(d.value)
                        }
                        else {
                            return 125;
                        }
                    })
                    .attr("height", function (d) {
                        var value = parseFloat(height) / 2.0 - y(d.value);
                        if (value > 0) {
                            return value;
                        }
                        else {
                            return -value;
                        }
                    })
                    .attr("fill", function (d, index) {
                        return (colors[index])
                    });

                scope.$watch('concern', function (newValue, oldValue) {
                    console.log(newValue);
                    console.log("changed");

                    if(newValue >= 0 && oldValue <= 0){
                          svg.selectAll("#Concern").transition().duration(500).delay(500).attr("height", function() {
                                    return 0;
                                }).transition()
                                .attr("y", function() {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                } })
                                .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                    if (value > 0) {
                                            return value;
                                        }
                                        else {
                                            return -value;
                                        }
                                }).duration(500);
                    }

                    else if(newValue <= 0 && oldValue >= 0){
                        svg.selectAll("#Concern").transition().duration(500).delay(500).attr("height", function() {
                                    return 0;
                                }).attr("y", function(){return 125}).transition().attr("y", function() {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                } })
                                .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                    if (value > 0) {
                                            return value;
                                        }
                                        else {
                                            return -value;
                                        }
                                }).duration(500);
                    }

                    else {
                        svg.selectAll("#Concern").transition().attr("y", function () {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                }
                            })
                            .attr("height", function (d) {
                                var value = parseFloat(height) / 2.0 - y(newValue);
                                if (value > 0) {
                                    return value;
                                }
                                else {
                                    return -value;
                                }
                            }).duration(1000);
                    }

                });

                scope.$watch('mistrust', function (newValue, oldValue) {
                    console.log(newValue);
                    console.log("changed");
                    if(newValue >= 0 && oldValue <= 0){
                          svg.selectAll("#Mistrust").transition().duration(500).delay(500).attr("height", function() {
                                    return 0;
                                }).transition()
                                .attr("y", function() {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                } })
                                .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                    if (value > 0) {
                                            return value;
                                        }
                                        else {
                                            return -value;
                                        }
                                }).duration(500);
                    }
                    else if(newValue <= 0 && oldValue >= 0){
                    svg.selectAll("#Mistrust").transition().duration(500).delay(500).attr("height", function() {
                                return 0;
                            }).attr("y", function(){return 125}).transition().attr("y", function() {
                            if (newValue > 0) {
                                return y(newValue)
                            }
                            else {
                                return 125;
                            } })
                            .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                if (value > 0) {
                                        return value;
                                    }
                                    else {
                                        return -value;
                                    }
                            }).duration(500);
                    }

                    else {
                        svg.selectAll("#Mistrust").transition().attr("y", function () {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                }
                            })
                            .attr("height", function (d) {
                                var value = parseFloat(height) / 2.0 - y(newValue);
                                if (value > 0) {
                                    return value;
                                }
                                else {
                                    return -value;
                                }
                            }).duration(1000);
                    }

                });

                scope.$watch('humor', function (newValue, oldValue) {
                    console.log(newValue);
                    console.log("changed");
                    if(newValue >= 0 && oldValue <= 0){
                          svg.selectAll("#Humor").transition().duration(500).delay(500).attr("height", function() {
                                    return 0;
                                }).transition()
                                .attr("y", function() {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                } })
                                .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                    if (value > 0) {
                                            return value;
                                        }
                                        else {
                                            return -value;
                                        }
                                }).duration(500);
                    }
                    else if(newValue <= 0 && oldValue >= 0){
                        svg.selectAll("#Humor").transition().duration(500).delay(500).attr("height", function() {
                                    return 0;
                                }).attr("y", function(){return 125}).transition().attr("y", function() {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                } })
                                .attr("height", function(d) {var value = parseFloat(height) / 2.0 - y(newValue);
                                    if (value > 0) {
                                            return value;
                                        }
                                        else {
                                            return -value;
                                        }
                                }).duration(500);
                    }
                    else {
                        svg.selectAll("#Humor").transition().attr("y", function () {
                                if (newValue > 0) {
                                    return y(newValue)
                                }
                                else {
                                    return 125;
                                }
                            })
                            .attr("height", function (d) {
                                var value = parseFloat(height) / 2.0 - y(newValue);
                                if (value > 0) {
                                    return value;
                                }
                                else {
                                    return -value;
                                }
                            }).duration(1000);
                    }

                });
            }
        };
});