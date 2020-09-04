var ec_left1 = echarts.init(document.getElementById('echarts_0'));


var ddd = [{}];

ec_left1_Option = {
    tooltip: {
        show: false
    },

    series: [{
        gridSize: 2,
        type: 'wordCloud',
        sizeRange: [12, 55],
        rotationRange: [-45, 0, 45, 90],
        textStyle: {
            normal: {
                color: function () {
                    return 'rgb(' + [
                        Math.round(Math.random() * 255),
                        Math.round(Math.random() * 255),
                        Math.round(Math.random() * 255)
                    ].join(',') + ')';
                }
            }
        },
        right:null,
        bottom:null,
        data:[]

    }]
};


ec_left1.setOption(ec_left1_Option)