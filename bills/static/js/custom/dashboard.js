/**
 * Created by roxnairani on 8/18/14.
 */

$(document).ready(function() {

    var prepareDashboardBlock = function(){
        $('#dashboard-block').show();
        $('#chart-block').hide();
        $('#form-block').hide();
    };

    // SET UP INITIAL DASHBOARD VIEW

    var load_dashboard = function () {
        $.ajax({
            url: "/dashboard_analysis/",
            type: "GET",
            dataType: "html",
            success: function (dashboard_analysis) {
                dashboard_analysis = jQuery.parseJSON(dashboard_analysis);
                // CHART 0 - Pie chart on dashboard
                $('#chart0').highcharts({
                    chart: {
                        plotBackgroundColor: null,
                        plotBorderWidth: 1,
                        plotShadow: false
                    },
                    title: {text: 'Overview of customer spend'},
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            colors: ['#f56954', '#00a65a', '#0073b7', '#f39c12'],
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            }
                        }
                    },
                    series: [
                        {
                            type: 'pie',
                            name: 'Overall spend',
                            data: [
                                ['Calls', parseFloat(dashboard_analysis.total_calls)],
                                ['Boosters (SMS)', parseFloat(dashboard_analysis.total_boosters)],
                                ['Data', parseFloat(dashboard_analysis.total_data)],
                                ['Roaming', parseFloat(dashboard_analysis.total_roaming)],
                            ]
                        }
                    ]
                });
            },
            error: function (error_message) {
                console.log(error_message);
            }
        });
    };

    load_dashboard();

    // DASHBOARD BLOCK

    $(document).on('click', '#dashboard', function () {
        prepareDashboardBlock();
        $.ajax({
            url: "/dashboard/",
            type: "GET",
            dataType: "html",
            success: function (dashboard_template) {
                load_dashboard();
                $('#page-header').html('Dashboard');
            },
            error: function (error_message) {
                console.log(error_message);
            }
        });
    });

});