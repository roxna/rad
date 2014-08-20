/**
 * Created by roxnairani on 8/10/14.
 */

$(document).ready(function(){

    var prepareChartBlock = function(){
        $('#dashboard-block').hide();
        $('#chart-block').show();
        $('#form-block').hide();
    };

    // CHART BLOCK - DATA/ROAMING ANALYSIS

    $(document).on('click', '#data', function(){
        prepareChartBlock();
        $('#page-header').html('Roaming/Data breakdown');
        $.ajax({
            url: "/api/v1/data/?format=json/",
            type: "GET",
            dataType: "json",
            success: function(data_analysis) {
                console.log(data_analysis);
                var data_2G = 0;
                var data_3G = 0;
                var data_4G = 0;
                for (var i = 0; i < data_analysis.objects.length; i++) {
                    if (data_analysis.objects[i].type == 1) {data_2G++;}
                    else if (data_analysis.objects[i].type == 2) {data_3G++;}
                    else if (data_analysis.objects[i].type == 3) {data_4G++;}
                }
                // CHART 3 - Pie chart of Data (2/3/4G) breakdown
                $('#chart3-body').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,
                        plotShadow: false
                    },
                    title: {text: 'Overview of data subscription'},
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Booster spend',
                            data: [
                                ['2G Data', data_2G],
                                ['3G Data', data_3G],
                                ['4G Data', data_4G],
                            ]
                        }
                    ]
                });
            }
        });
        $.ajax({
            url: "/api/v1/roaming/?format=json/",
            type: "GET",
            dataType: "json",
            success: function(roaming_analysis) {
                console.log(roaming_analysis);


//              To eventually crunch this data (hydrate-dehydrate) in python
                var national_incoming_calls = 0;
                var national_outgoing_calls = 0;
                var national_incoming_sms = 0;
                var national_outgoing_sms = 0;
                for (var i=0; i<roaming_analysis.objects.length; i++){
                    if (roaming_analysis.objects[i].type == 1){national_incoming_calls++;}
                    else if (roaming_analysis.objects[i].type == 2){national_outgoing_calls++;}
                    else if (roaming_analysis.objects[i].type == 3){national_incoming_sms++;}
                    else if (roaming_analysis.objects[i].type == 3){national_outgoing_sms++;}
                }

                // CHART 1 - Pie chart of Roaming breakdown
                $('#chart1-body').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,
                        plotShadow: false
                    },
                    title: {text: 'Roaming Call/SMS breakdown'},
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Booster spend',
                            data: [
                                ['Calls', national_incoming_calls + national_outgoing_calls],
                                ['SMS', national_incoming_sms + national_outgoing_sms],
                            ]
                        }
                    ]
                });

                // CHART 2 - BAR CHART (POTENTIAL TO MAKE IT DRILL DOWN
                $('#chart2-body').highcharts({
                    chart: { type: 'column'},
                    title: {text: 'Breakdown of roaming spend'},
                    xAxis: { categories: ['Calls', 'SMS']},
                    yAxis: {
                        min: 0,
                        title: {text: 'Roaming'},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{series.color}">{series.name}</span>: {point.percentage:.0f}%<br/>',
                        shared: true
                    },
                    plotOptions: {
                        column: {stacking: 'percent'}
                    },
                    series: [
                        {
                            name: 'Incoming',
                            data: [national_incoming_calls, national_incoming_sms]
                        },
                        {
                            name: 'Outgoing',
                            data: [national_outgoing_calls, national_outgoing_sms]
                        },
                    ]
                });
            }
        });
    });

});