/**
 * Created by roxnairani on 8/10/14.
 */

$(document).ready(function(){

    var prepareDashboardBlock = function(){
        $('#dashboard-block').show();
        $('#chart-block').hide();
        $('#form-block').hide();
    };

    var prepareChartBlock = function(){
        $('#dashboard-block').hide();
        $('#chart-block').show();
        $('#form-block').hide();
    };

    var prepareFormBlock = function(){
        $('#dashboard-block').hide();
        $('#chart-block').hide();
        $('#form-block').show();
    };

    var load_dashboard = function(){
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
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [{
                        type: 'pie',
                        name: 'Overall spend',
                        data: [
                            ['Calls', parseFloat(dashboard_analysis.total_calls)],
                            ['Boosters (SMS)', parseFloat(dashboard_analysis.total_boosters)],
                            ['Data', parseFloat(dashboard_analysis.total_data)],
                            ['Roaming', parseFloat(dashboard_analysis.total_roaming)],
                        ]
                    }]
                });
            },
            error: function(error_message){
                console.log(error_message);
            }
         });
    };

    load_dashboard();

    // DASHBOARD BLOCK

    $(document).on('click', '#dashboard', function(){
        prepareDashboardBlock();
        $.ajax({
            url: "/dashboard/",
            type: "GET",
            dataType: "html",
            success: function (dashboard_template) {
                load_dashboard();
                $('#page-header').html('Dashboard');
            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

    // FORM BLOCK

    $.ajax({
        url: "/profile/",
        type: "GET",
        dataType: "html",
        success: function (profile_template) {
            $(document).on('click', '#profile', function() {
                $('#page-header').html('Profile');
                prepareFormBlock();
                $('#form-block').html(profile_template);
            });
        },
        error: function (error_message) {
            console.log(error_message);
        }
     });

    $(document).on('click', '#upload_data', function(){
        prepareFormBlock();
        $.ajax({
            url: "/upload_data/",
            type: "GET",
            dataType: "html",
            success: function (upload_data_template) {
                $('#page-header').html('Upload Data');
                $('#form-block').html(upload_data_template);
            },
            error: function (error_message) {
                console.log(error_message);
            }
        });
    });

    // CHART BLOCK

    $(document).on('click', '#calls', function(){
        prepareChartBlock();
        $.ajax({
            url: "/api/v1/call/?format=json/",
            type: "GET",
            dataType: "json",
            success: function(calls_analysis){
                console.log(calls_analysis);
                var outgoing_local_same_network = 0;
                var outgoing_local_other_network = 0;
                var outgoing_local_fixed_landline =0;
                var outgoing_std_same_network = 0;
                var outgoing_std_other_network = 0;
                var outgoing_std_fixed_landline = 0;
                var outgoing_intl = 0;
//                var map = {
//                    1: outgoing_local_same_network,
//                    2: outgoing_local_other_network,
//                    3: outgoing_local_fixed_landline,
//                    4: outgoing_std_same_network,
//                    5: outgoing_std_other_network,
//                    6: outgoing_std_fixed_landline,
//                    7: outgoing_intl,
//                };
                for (var i=0; i<calls_analysis.objects.length; i++){
//                    map[calls_analysis.objects[i].type]++;
                    if (calls_analysis.objects[i].type == 1){
                        outgoing_local_same_network++;
                    }
                    else if (calls_analysis.objects[i].type == 2){
                        outgoing_local_other_network++;
                    }
                    else if (calls_analysis.objects[i].type == 3){
                        outgoing_local_fixed_landline++;
                    }
                    else if (calls_analysis.objects[i].type == 4){
                        outgoing_std_same_network++;
                    }
                    else if (calls_analysis.objects[i].type == 5){
                        outgoing_std_other_network++;
                    }
                    else if (calls_analysis.objects[i].type == 6){
                        outgoing_std_fixed_landline++;
                    }
                    else if (calls_analysis.objects[i].type == 7){
                        outgoing_intl++;
                    }
                }

                $('#page-header').html('Calls Analysis');

                // CHART 1 - Pie chart of Local-STD-Intl breakdown
                $('#chart1').highcharts({
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
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [{
                        type: 'pie',
                        name: 'Calls spend',
                        data: [
                            ['Local calls', outgoing_local_same_network + outgoing_local_other_network + outgoing_local_fixed_landline],
                            ['STD calls', outgoing_std_same_network + outgoing_std_other_network + outgoing_std_fixed_landline],
                            ['Intl calls', outgoing_intl],
                        ]
                    }]
                });

                // CHART 2 - Bar chart of detailed breakdown
                $('#chart2').highcharts({
                    chart: { type: 'column'},
                    title: {text: 'Breakdown of calls spend'},
                    xAxis: { categories: ['Local', 'STD']},
                    yAxis: {
                        min: 0,
                        title: {text: 'No. of calls'},
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
                    series: [{
                        name: 'Same network',
                        data: [outgoing_local_same_network, outgoing_std_same_network]
                    }, {
                        name: 'Other network',
                        data: [outgoing_local_other_network, outgoing_std_other_network]
                    }, {
                        name: 'Fixed landline',
                        data: [outgoing_local_fixed_landline, outgoing_std_fixed_landline]
                    }]
                });

            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

    $(document).on('click', '#boosters', function(){
        prepareChartBlock();
        $.ajax({
            url: "/api/v1/booster/?format=json/",
            type: "GET",
            dataType: "json",
            success: function(booster_analysis){
                $('#page-header').html('Boosters (SMS etc) Analysis');
                var outgoing_local_same_network = 0;
                var outgoing_local_other_network = 0;
                var outgoing_std_same_network = 0;
                var outgoing_std_other_network = 0;
                var outgoing_intl = 0;
                for (var i=0; i<booster_analysis.objects.length; i++){
                    if (booster_analysis.objects[i].type == 1){
                        outgoing_local_same_network++;
                    }
                    else if (booster_analysis.objects[i].type == 2){
                        outgoing_local_other_network++;
                    }
                    else if (booster_analysis.objects[i].type == 3){
                        outgoing_std_same_network++;
                    }
                    else if (booster_analysis.objects[i].type == 4){
                        outgoing_std_other_network++;
                    }
                    else if (booster_analysis.objects[i].type == 5){
                        outgoing_intl++;
                    }
                }

                // CHART 1 - Pie chart of Local-STD-Intl breakdown
                $('#chart1').highcharts({
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
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: [{
                        type: 'pie',
                        name: 'Booster spend',
                        data: [
                            ['Local SMS', outgoing_local_same_network + outgoing_local_other_network],
                            ['STD SMS', outgoing_std_same_network + outgoing_std_other_network],
                            ['Intl SMS', outgoing_intl],
                        ]
                    }]
                });

                // CHART 2 - Bar chart of detailed breakdown
                $('#chart2').highcharts({
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
                    series: [{
                        name: 'Same network',
                        data: [outgoing_local_same_network, outgoing_std_same_network]
                    }, {
                        name: 'Other network',
                        data: [outgoing_local_other_network, outgoing_std_other_network]
                    }]
                });

            },
            error: function(error_message){
                console.log(error_message);
            }
        });
    });

    $(document).on('click', '#data', function(){
        prepareChartBlock();
        $('#page-header').html('Data/Roaming breakdown');
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
                    if (data_analysis.objects[i].type == 1) {
                        data_2G++;
                    }
                    else if (data_analysis.objects[i].type == 2) {
                        data_3G++;
                    }
                    else if (data_analysis.objects[i].type == 3) {
                        data_4G++;
                    }
                }
                // CHART 1 - Pie chart of Data (2/3/4G) breakdown
                $('#chart1').highcharts({
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
                var national_incoming_calls = 0;
                var national_outgoing_calls = 0;
                var national_incoming_sms = 0;
                var national_outgoing_sms = 0;
                for (var i=0; i<roaming_analysis.objects.length; i++){
                    if (roaming_analysis.objects[i].type == 1){
                        national_incoming_calls++;
                    }
                    else if (roaming_analysis.objects[i].type == 2){
                        national_outgoing_calls++;
                    }
                    else if (roaming_analysis.objects[i].type == 3){
                        national_incoming_sms++;
                    }
                    else if (roaming_analysis.objects[i].type == 3){
                        national_outgoing_sms++;
                    }
                }
                // CHART 2 - Pie chart of Roaming breakdown
                $('#chart2').highcharts({
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
            }
        });
    });

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
                for (var i=0; i<more_analysis.objects.length; i++){
                    if (more_analysis.objects[i].type == 0){
                        prepaid_plans++;
                    }
                    else if (more_analysis.objects[i].type == 1){
                        postpaid_plans++;
                    }
                    if (more_analysis.objects[i].min_rental == "599.00"){
                        postpaid_plans_599++;
                    }
                    else if (more_analysis.objects[i].min_rental == "799.00"){
                        postpaid_plans_799++;
                    }
                }
                // CHART 1 - Pie chart of Postpaid-Prepaid breakdown
                $('#chart1').highcharts({
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
                            name: 'Booster spend',
                            data: [
                                ['Postpaid', postpaid_plans],
                                ['Prepaid', prepaid_plans],
                            ]
                        }
                    ]
                });
                // CHART 2 - Bar chart of Postpaid breakdown
                $('#chart2').highcharts({
                    chart: { type: 'column'},
                    title: {text: 'Breakdown of calls spend'},
                    xAxis: { categories: ['Postpaid']},
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
                    series: [{
                        name: 'Plan 599',
                        data: [postpaid_plans_599]
                    }, {
                        name: 'Plan 799',
                        data: [postpaid_plans_799]
                    }]
                });

            }
        });
    });

});