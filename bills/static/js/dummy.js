/**
 * Created by roxnairani on 8/13/14.
 */

// CHART 0

$('#chart0-header').html('Overview of customer spend');
Morris.Donut({
    element: 'chart0',
    resize: true,
    colors: ["green", "orange", "grey", "blue"],
    data: [
        {label: "Calls", value: dashboard_analysis.total_calls},
        {label: "Boosters (SMS)", value: dashboard_analysis.total_boosters},
        {label: "Data", value: dashboard_analysis.total_data},
        {label: "Roaming", value: dashboard_analysis.total_roaming},
    ],
    hideHover: 'auto'
});

// CHART 1 - Donut chart of Local-STD-Intl Calls breakdown

// FLOT PIE CHART
    $('#chart1-header').html('Overview of calls spend');
    var data = [
        {label: "Local calls", color: "green", data: calls_analysis.outgoing_local_same_network + calls_analysis.outgoing_local_other_network + calls_analysis.outgoing_local_fixed_landline},
        {label: "STD calls", color: "orange", data: calls_analysis.outgoing_std_same_network + calls_analysis.outgoing_std_other_network + calls_analysis.outgoing_std_fixed_landline},
        {label: "Int'l calls", color: "grey", data: calls_analysis.outgoing_intl},
    ];
    $.plot($("#chart1"), data, {
        series: {
            pie: {
                show: true,
                radius: 1,
                label: {
                    show: true,
                    radius: 2/3,
                    formatter: function(label, series){
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
                    },
                    threshold: 0.1
                }
            }
        },
        legend: {
            show: false
        }
    });

// MORRIS DONUT CHART
    Morris.Donut({
        element: 'chart1',
        resize: true,
        colors: ["green", "orange", "grey"],
        data: [
            {label: "Local calls", value: calls_analysis.outgoing_local_same_network + calls_analysis.outgoing_local_other_network + calls_analysis.outgoing_local_fixed_landline},
            {label: "STD calls", value: calls_analysis.outgoing_std_same_network + calls_analysis.outgoing_std_other_network + calls_analysis.outgoing_std_fixed_landline},
            {label: "Int'l calls", value: calls_analysis.outgoing_intl},
        ],
        hideHover: 'auto'
    });

// MORRIS BAR CHART #2
        Morris.Bar({
            element: 'chart2',
            resize: true,
            data: [
                {y: 'Local', a: calls_analysis.outgoing_local_same_network,
                                b: calls_analysis.outgoing_local_other_network,
                                c: calls_analysis.outgoing_local_fixed_landline},
                {y: 'STD', a: calls_analysis.outgoing_std_same_network,
                            b: calls_analysis.outgoing_std_other_network,
                            c: calls_analysis.outgoing_std_fixed_landline},
            ],
            barColors: ["lightgrey", "grey", "darkgrey"],
            xkey: 'y',
            ykeys: ['a', 'b', 'c'],
            labels: ['Same network', 'Other network', 'Fixed landline'],
            hideHover: 'auto'
        });


// SMS CHARTS

 $('#chart1-header').html('Overview of boosters spend');
    Morris.Donut({
        element: 'chart1',
        resize: true,
        colors: ["green", "orange", "grey"],
        data: [
            {label: "Local SMS", value: booster_analysis.outgoing_local_same_network + booster_analysis.outgoing_local_other_network},
            {label: "STD SMS", value: booster_analysis.outgoing_std_same_network + booster_analysis.outgoing_std_other_network},
            {label: "Int'l SMS", value: booster_analysis.outgoing_intl},
        ],
        hideHover: 'auto'
    });

    // CHART 2 - Bar chart of detailed breakdown
    $('#chart2-header').html('Breakdown of booster spend');
    Morris.Bar({
        element: 'chart2',
        resize: true,
        data: [
            {y: 'Local', a: booster_analysis.outgoing_local_same_network,
                            b: booster_analysis.outgoing_local_other_network},
            {y: 'STD', a: booster_analysis.outgoing_std_same_network,
                        b: booster_analysis.outgoing_std_other_network},
        ],
        barColors: ["lightgrey", "grey"],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Same network', 'Other network'],
        hideHover: 'auto'
    });
