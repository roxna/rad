/**
 * Created by roxnairani on 8/10/14.
 */

$(document).ready(function(){

    $('#loading-image').hide();

    var prepareChartBlock = function(){
        $('#dashboard-block').hide();
        $('#chart-block').show();
        $('#form-block').hide();
    };

    // CHART BLOCK - CALLS ANALYSIS

    $(document).on('click', '#calls', function(){
        prepareChartBlock();
        $.ajax({
            url: "/api/v1/call/?format=json",
            type: "GET",
            dataType: "json",
            beforeSend: function(){
                $('#loading-image').show();
            },
            complete: function(){
                $('#loading-image').hide();
            },
            success: function(calls_analysis) {
                console.log(calls_analysis);

//              To eventually crunch this data (hydrate-dehydrate) in python
                var outgoing_local_same_network = 0;
                var outgoing_local_other_network = 0;
                var outgoing_local_fixed_landline = 0;
                var outgoing_std_same_network = 0;
                var outgoing_std_other_network = 0;
                var outgoing_std_fixed_landline = 0;
                var outgoing_intl = 0;

                var time_00_06 = 0;
                var time_06_08 = 0;
                var time_08_10 = 0;
                var time_10_12 = 0;
                var time_12_14 = 0;
                var time_14_16 = 0;
                var time_16_18 = 0;
                var time_18_20 = 0;
                var time_20_22 = 0;
                var time_22_24 = 0;

                for (var i = 0; i < calls_analysis.objects.length; i++) {
                    if (calls_analysis.objects[i].type == 1) {outgoing_local_same_network++;}
                    else if (calls_analysis.objects[i].type == 2) {outgoing_local_other_network++;}
                    else if (calls_analysis.objects[i].type == 3) {outgoing_local_fixed_landline++;}
                    else if (calls_analysis.objects[i].type == 4) {outgoing_std_same_network++;}
                    else if (calls_analysis.objects[i].type == 5) {outgoing_std_other_network++;}
                    else if (calls_analysis.objects[i].type == 6) {outgoing_std_fixed_landline++;}
                    else if (calls_analysis.objects[i].type == 7) {outgoing_intl++;}

                    var time = parseInt(calls_analysis.objects[i].time.slice(0, 2));
                    if (time < 6) {time_00_06++;}
                    else if (time < 8) {time_06_08++;}
                    else if (time < 10) {time_08_10++;}
                    else if (time < 12) {time_10_12++;}
                    else if (time < 14) {time_12_14++;}
                    else if (time < 16) {time_14_16++;}
                    else if (time < 18) {time_16_18++;}
                    else if (time < 20) {time_18_20++;}
                    else if (time < 22) {time_20_22++;}
                    else if (time < 24) {time_22_24++;}

                }

                $('#page-header').html('Calls Analysis');

                // CHART 1 - Pie chart of Local-STD-Intl breakdown
                $('#chart1-body').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,//null,
                        plotShadow: false
                    },
                    title: {text: 'Overview of calls spend'},
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            colors: ['#7F5852', '#f56954', '#FFB0A4'],
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            }
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Calls spend',
                            data: [
                                ['Local calls', outgoing_local_same_network + outgoing_local_other_network + outgoing_local_fixed_landline],
                                ['STD calls', outgoing_std_same_network + outgoing_std_other_network + outgoing_std_fixed_landline],
                                ['Intl calls', outgoing_intl],
                            ]
                        }
                    ]
                });

                // CHART 2 - Bar chart of detailed breakdown
                $('#chart2-body').highcharts({
                    chart: { type: 'column'},
                    title: {text: 'Breakdown of calls spend'},
                    xAxis: { categories: ['Local', 'STD']},
                    yAxis: {
                        min: 0,
                        title: {text: 'No. of calls'},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        pointFormat: '<span style="color:{series.color}">{series.name}</span>: {point.percentage:.0f}%<br/>',
                        shared: true
                    },
                    plotOptions: {
                        column: {
                            stacking: 'percent'
                        }
                    },
                    series: [
                        {
                            name: 'Same network',
                            data: [outgoing_local_same_network, outgoing_std_same_network],
                            color: '#7F7F7F'
                        },
                        {
                            name: 'Other network',
                            data: [outgoing_local_other_network, outgoing_std_other_network],
                            color: '#7F6F6E'
                        },
                        {
                            name: 'Fixed landline',
                            data: [outgoing_local_fixed_landline, outgoing_std_fixed_landline],
                            color: '#FFDEDC'
                        }
                    ]
                });

                // CHART 3 - Scatter plot of time of day calls made
                $('#chart3-body').highcharts({
                    chart: {type: 'column'},
                    title: {text: 'Calls made by time of day'},
                    xAxis: {
                        title: {
                            enabled: true,
                            text: 'Time of day'
                        },
                        type: 'category',
                        startOnTick: true,
                        endOnTick: true,
                        showLastLabel: true
                    },
                    yAxis: {
                        title: {text: 'No. of calls'},
                        min: 0
                    },
                    plotOptions: {
                        scatter: {
                            marker: {
                                radius: 3,
                                states: {
                                    hover: {
                                        enabled: true,
                                        lineColor: '#f56954'
                                    }
                                }
                            },
                            states: {
                                hover: {
                                    marker: {
                                        enabled: false
                                    }
                                }
                            },
                            tooltip: {
                                headerFormat: '<b>{series.name}</b><br>',
                                pointFormat: '{point.x} cm, {point.y} kg'
                            }
                        }
                    },
                    series: [{
                        name: 'All calls',
                        color: '#f56954',
                        data: [
                            ['00:00-06:00', time_00_06],
                            ['06:00-08:00', time_06_08],
                            ['08:00-10:00', time_08_10],
                            ['10:00-12:00', time_10_12],
                            ['12:00-14:00', time_12_14],
                            ['14:00-16:00', time_14_16],
                            ['16:00-18:00', time_16_18],
                            ['18:00-20:00', time_18_20],
                            ['20:00-22:00', time_20_22],
                            ['22:00-24:00', time_22_24],
                        ]
                    }]
                });
            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

});