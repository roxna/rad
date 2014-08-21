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

    // CHART BLOCK - BOOSTERS ANALYSIS

    $(document).on('click', '#boosters', function(){
        prepareChartBlock();
        $.ajax({
            url: "/api/v1/booster/?format=json/",
            type: "GET",
            dataType: "json",
            beforeSend: function(){
                $('#loading-image').show();
            },
            complete: function(){
                $('#loading-image').hide();
            },
            success: function(booster_analysis) {
                $('#page-header').html('Boosters (SMS etc) Analysis');
                var outgoing_local_same_network = 0;
                var outgoing_local_other_network = 0;
                var outgoing_std_same_network = 0;
                var outgoing_std_other_network = 0;
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

                for (var i = 0; i < booster_analysis.objects.length; i++) {
                    if (booster_analysis.objects[i].type == 1) {outgoing_local_same_network++;}
                    else if (booster_analysis.objects[i].type == 2) {outgoing_local_other_network++;}
                    else if (booster_analysis.objects[i].type == 3) {outgoing_std_same_network++;}
                    else if (booster_analysis.objects[i].type == 4) {outgoing_std_other_network++;}
                    else if (booster_analysis.objects[i].type == 5) {outgoing_intl++;}

                    if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 6) {time_00_06++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 8) {time_06_08++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 10) {time_08_10++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 12) {time_10_12++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 14) {time_12_14++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 16) {time_14_16++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 18) {time_16_18++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 20) {time_18_20++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 22) {time_20_22++;}
                    else if (parseInt(booster_analysis.objects[i].time.slice(0, 2)) < 24) {time_22_24++;}

                    // CHART 1 - Pie chart of Local-STD-Intl breakdown
                    $('#chart1-body').highcharts({
                        chart: {
                            plotBackgroundColor: null,
                            plotBorderWidth: 1,//null,
                            plotShadow: false
                        },
                        title: {text: 'Overview of SMS spend'},
                        tooltip: {
                            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                colors: ['#36B569', '#00a65a','#78F2A9'],
                                dataLabels: {
                                    enabled: true,
                                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                }
                            }
                        },
                        series: [
                            {
                                type: 'pie',
                                name: 'Booster spend',
                                data: [
                                    ['Local SMS', outgoing_local_same_network + outgoing_local_other_network],
                                    ['STD SMS', outgoing_std_same_network + outgoing_std_other_network],
                                    ['Intl SMS', outgoing_intl],
                                ]
                            }
                        ]
                    });

                    // CHART 2 - Bar chart of detailed breakdown
                    $('#chart2-body').highcharts({
                        chart: { type: 'column'},
                        title: {text: 'Breakdown of SMS spend'},
                        xAxis: { categories: ['Local', 'STD']},
                        yAxis: {
                            min: 0,
                            title: {text: 'No. of calls'},
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
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
                                name: 'Same network',
                                data: [outgoing_local_same_network, outgoing_std_same_network],
                                color: '#787F7A'
                            },
                            {
                                name: 'Other network',
                                data: [outgoing_local_other_network, outgoing_std_other_network],
                                color: '#C3FFD5'
                            }
                        ]
                    });

                    // CHART 3 - Scatter plot of time of day calls made
                    $('#chart3-body').highcharts({
                        chart: {type: 'column'},
                        title: {text: 'SMS by time of day'},
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
                            title: {text: 'No. of texts'},
                            min: 0
                        },
                        plotOptions: {
                            scatter: {
                                marker: {
                                    radius: 3,
                                    states: {
                                        hover: {
                                            enabled: true,
                                            lineColor: '#7BF597'
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
                        series: [
                            {
                                name: '# SMS',
                                color: '#7BF597',
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
                            }
                        ]
                    });
                }
            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

});