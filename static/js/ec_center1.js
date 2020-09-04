var dom = document.getElementById("c2");
var ec_center = echarts.init(dom);

var mydata = [
    {name: '北京', value: Math.round(Math.random() * 1000)},
    {name: '天津', value: Math.round(Math.random() * 1000)},
    {name: '上海', value: Math.round(Math.random() * 1000)},
    {name: '重庆', value: Math.round(Math.random() * 1000)},
    {name: '河北', value: Math.round(Math.random() * 1000)},
    {name: '河南', value: Math.round(Math.random() * 1000)},
    {name: '云南', value: Math.round(Math.random() * 1000)},
    {name: '辽宁', value: Math.round(Math.random() * 1000)},
    {name: '黑龙江', value: Math.round(Math.random() * 1000)},
    {name: '湖南', value: Math.round(Math.random() * 1000)},
    {name: '安徽', value: Math.round(Math.random() * 1000)},
    {name: '山东', value: Math.round(Math.random() * 1000)},
    {name: '新疆', value: Math.round(Math.random() * 1000)},
    {name: '江苏', value: Math.round(Math.random() * 1000)},
    {name: '浙江', value: Math.round(Math.random() * 1000)},
    {name: '江西', value: Math.round(Math.random() * 1000)},
    {name: '湖北', value: Math.round(Math.random() * 1000)},
    {name: '广西', value: Math.round(Math.random() * 1000)},
    {name: '甘肃', value: Math.round(Math.random() * 1000)},
    {name: '山西', value: Math.round(Math.random() * 1000)},
    {name: '内蒙古', value: Math.round(Math.random() * 1000)},
    {name: '陕西', value: Math.round(Math.random() * 1000)},
    {name: '吉林', value: Math.round(Math.random() * 1000)},
    {name: '福建', value: Math.round(Math.random() * 1000)},
    {name: '贵州', value: Math.round(Math.random() * 1000)},
    {name: '广东', value: Math.round(Math.random() * 1000)},
    {name: '青海', value: Math.round(Math.random() * 1000)},
    {name: '西藏', value: Math.round(Math.random() * 1000)},
    {name: '四川', value: Math.round(Math.random() * 1000)},
    {name: '宁夏', value: Math.round(Math.random() * 1000)},
    {name: '海南', value: Math.round(Math.random() * 1000)},
    {name: '台湾', value: Math.round(Math.random() * 1000)},
    {name: '香港', value: Math.round(Math.random() * 1000)},
    {name: '澳门', value: Math.round(Math.random() * 1000)}
]
var app = {};
ec_center_option = null;
ec_center_option = {
    title: {
        text: '',
        subtext: '',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },

    //左侧小导航图标
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
            fontSize: 8,
            color: "white"
        },
        splitList: [
            {start: 1, end: 9},
            {start: 10, end: 99},
            {start: 100, end: 499},
            {start: 500, end: 999},
            {start: 1000, end: 49999},
            {start: 50000}],
        color: ['#95002F', '#BD003B', '#E03355', '#FF6F6F', '#FFBABA', '#FFE8E8']
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '累计确诊人数',
            type: 'map',
            mapType: 'china',
            roam: false, //拖动和缩放
            itemStyle: {
                normal: {
                    borderWidth: .5, //区域边框宽度
                    areaColor: "#ffefd5", //区域颜色
                },
                emphasis: { //鼠标滑过地图高亮的相关设置
                    borderWidth: .5,
                    borderColor: '#4b0082',
                    areaColor: "#C7FFFD",
                }
            },
            label: {
                normal: {
                    show: true, //省份名称
                    fontSize: 8,
                },
                emphasis: {
                    show: true,
                    fontSize: 8,
                }
            },
            data: [] //mydata //数据
        }
    ]
};
;
if (ec_center_option && typeof ec_center_option === "object") {
    ec_center.setOption(ec_center_option, true);
}