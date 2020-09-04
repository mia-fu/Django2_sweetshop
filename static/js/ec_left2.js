var ec_left2 = echarts.init(document.getElementById('echarts_1'));

ec_left2_Option = {
    tooltip: {},
    legend: {},
    xAxis: {
        type: 'category',
        data: [],
        axisLine: {
            lineStyle: {
                color: 'white'
            }
        },
    },
    yAxis: {
        type: 'value',
        axisLine: {
            lineStyle: {
                color: 'white'
            }
        },
    },
    series: [{
        data: [],
        type: 'bar',
        showBackground: true,
        barMaxWidth: "50%",
        backgroundStyle: {
            color: 'rgba(220, 220, 220, 0.8)'
        },

    }]
};


ec_left2.setOption(ec_left2_Option)