/**
 * Created by roxnairani on 8/10/14.
 */

$(document).ready(function(){

    var prepareChartBlock = function(){
        $('#dashboard-block').hide();
        $('#chart-block').show();
        $('#form-block').hide();
    };

    // CHART BLOCK - PLANS ANALYSIS

    $(document).on('click', '#more', function(){
        prepareChartBlock();
        $.ajax({
            url: "/api/v1/plan/?format=json/",
            type: "GET",
            dataType: "json",
            success: function(more_analysis) {
                console.log(more_analysis);
                $('#page-header').html('Plan breakdown');
                var prepaid_plans = 0;
                var postpaid_plans = 0;
                var postpaid_plans_599 = 0;
                var postpaid_plans_799 = 0;
                var inr_plans = 0;
                var usd_plans = 0;

                for (var i=0; i<more_analysis.objects.length; i++){
                    if (more_analysis.objects[i].type == 0){prepaid_plans++;}
                    else if (more_analysis.objects[i].type == 1){postpaid_plans++;}
                    if (more_analysis.objects[i].min_rental == "599.00"){postpaid_plans_599++;}
                    else if (more_analysis.objects[i].min_rental == "799.00"){postpaid_plans_799++;}
                    if (more_analysis.objects[i].currency == "INR"){inr_plans++;}
                    else if (more_analysis.objects[i].currency == "USD"){usd_plans++;}
                }
                // CHART 1 - Pie chart of Postpaid-Prepaid breakdown
                $('#chart1-body').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,
                        plotShadow: false
                    },
                    title: {text: 'Plan breakdown by post/pre-paid'},
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
                            name: '%',
                            data: [
                                ['Postpaid', postpaid_plans],
                                ['Prepaid', prepaid_plans],
                            ]
                        }
                    ]
                });

                // CHART 2 - Bar chart of Postpaid breakdown
                $('#chart2-body').highcharts({
                    chart: { type: 'column'},
                    title: {text: 'Breakdown of plan subscriptions'},
                    xAxis: { categories: ['Postpaid']},
                    yAxis: {
                        min: 0,
                        title: {text: 'No. of plans'},
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
                    series: [{
                        name: 'Plan 599',
                        data: [postpaid_plans_599]
                    }, {
                        name: 'Plan 799',
                        data: [postpaid_plans_799]
                    }]
                });

                // CHART 3 - Pie chart of currency breakdown
                $('#chart3-body').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,
                        plotShadow: false
                    },
                    title: {text: 'Plan breakdown by currency'},
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
                            name: '%',
                            data: [
                                ['INR', inr_plans],
                                ['USD', usd_plans],
                            ]
                        }
                    ]
                });

            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

});