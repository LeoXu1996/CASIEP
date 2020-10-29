
//评估指标体系旭日图
function sun(chart1, a){

//定义数据
var data = [{
    name: "信息化\n基础环境",
    value:30,
    itemStyle: {
        color: '#334455'
        // color: '#334455'
        // color: '#FFAE57'//设定形状填充颜色
    },
    children: [{
        name: '信息化管\n理与运行',
        value:9,
        itemStyle: {
        color: '#334455'
            // color: '#FFAE57'
        },
        children: [{
            name: ' ',
            children: [{
                name: 'None'
            }]
        
        }]
    }, {
        name: '信息化\n基础设施',
        value:12,
        itemStyle: {
            color: '#334455'
            // color: '#FFAE57'
        },
        children: [{
            name: '40%',
            itemStyle:{
            shadowColor: '#334455'
            // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.011,    
            },
            children: [{
                name: '网络环境',
                value:4.8,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455'
                    // color:'#FFAE57', //设置字体颜色
                    
                },
            }]
        }, {
            name: '40%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.011,     
            },
            children: [{
                name: '计算环境',
                value:4.8,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        }, {
            name: '20%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.008,     
            },
            children: [{
                name: '存储环境',
                value:2.4,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        }]
    },{
        name: '信息化资源',
        value:9,
        itemStyle: {
            color: '#334455'
            // color: '#FFAE57'
        },
        children: [{
            name: '40%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.01,     //设置字体大小
            },
            children: [{
                name: '科学数据资源',
                value:3.6,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        }, {
            name: '20%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.006,     
            },
            children: [{
                name: '数字教育资源',
                value:1.8,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        },{
            name: '20%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.006,     
            },
            children: [{
                name: '科学传播资源',
                value:1.8,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        }, {
            name: '20%',
            itemStyle:{
                shadowColor: '#334455',
                // shadowColor: '#FFAE57',
            },
            label:{
                color: '#334455',
                // color:'#FFAE57',
                fontSize: a*0.006,     
            },
            children: [{
                name: '数字文献资源',
                value:1.8,
                itemStyle: {
                    color: '#334455'
                    // color: '#FFAE57'
                },
                label:{
                    color: '#334455',
                    // color:'#FFAE57',
                    
                },
            }]
        }]
    }]
}, {
    name: '信息化\n应用',
    value:50,
    itemStyle: {
        color: '#A9A9A9'
        // color: '#A9A9A9'
    },
    
    children: [{
        name: '科研信息\n化应用',
        value:20,
        itemStyle: {
            color: '#A9A9A9'
        },
        children: [{
            name: '30%',
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            label:{
                color:'#A9A9A9',
                fontSize: a*0.011,
            },
            children: [{
                name: '科学数据应用',
                value:6,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',
                },
            }]
        }, {
            name: '30%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.011,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '科学计算应用',
                value:6,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        },{
            name: '20%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.011,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '云计算应用',
                value:4,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        }, {
            name: '20%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.01,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '开放共享应用',
                value:4,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        }]
    }, {
        name: '管理信息\n化应用',
        value:15,
        itemStyle: {
            color: '#A9A9A9'
        },
        children: [{
            name: '60%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.011,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: 'ARP应用',
                label:{
                    color:'#A9A9A9',

                },
                value:9,
                itemStyle: {
                    color: '#A9A9A9'
                },
            }]
        }, {
            name: '40%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.01,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '非ARP应用',
                label:{
                    color:'#A9A9A9',

                },
                value:6,
                itemStyle: {
                    color: '#A9A9A9'
                },
            }]
        }]
    },{
        name: '教育信息\n化应用',
        value:7.5,
        itemStyle: {
            color: '#A9A9A9'
        },
        children: [{
            name: '70%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.01,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '学历教育',
                value:5.25,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        }, {
            name: '30%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.008,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '继续教育',
                value:2.25,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        }]
    },{
        name: '科学传\n播应用',
        value:7.5,
        itemStyle: {
            color: '#A9A9A9'
        },
        children: [{
            name: '60%',
            label:{
                color:'#A9A9A9',
                fontSize: a*0.008,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '网络传播',
                value:4.5,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',

                },
            }]
        }, {
            name: '40%',
            label:{
                color:'#A9A9A9',
                fontSize:a*0.008,
            },
            itemStyle:{
              shadowColor: '#A9A9A9',
            },
            children: [{
                name: '网络科普',
                value:3,
                itemStyle: {
                    color: '#A9A9A9'
                },
                label:{
                    color:'#A9A9A9',
                    
                },
            }]
        }]
    }]
},{
    name: '网络安全',
    value:20,
    itemStyle: {
        color: '#505050'
        // color: '#505050'
    },
    children: [{
        name: '网络安全\n管理',
        value:10,
        itemStyle: {
            color: '#505050'
        },
        children: [{
            name: '20%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                fontSize: a*0.007,     
            },
            children: [{
                name: '安全责任',
                value:2,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        }, {
            name: '30%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                fontSize: a*0.008,     
            },
            children: [{
                name: '安全规范与制度',
                value:3,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        },{
            name: '20%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                fontSize: a*0.007,     
            },
            children: [{
                name: '安全自查',
                value:2,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        }, {
            name: '30%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                fontSize: a*0.008,     
                 
            },
            children: [{
                name: '安全培训与教育',
                value:3,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        }]
    }, {
        name: '网络安全\n技术保障',
        value:10,
        itemStyle: {
            color: '#505050'
        },
        children: [{
            name: '70%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                    
                   
            },
            children: [{
                name: '信息系统安全',
                value:7,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        }, {
            name: '30%',
            itemStyle:{
              shadowColor: '#505050',  
            },
            label:{
                color:'#505050',
                fontSize: a*0.008,     
            },
            children: [{
                name: '主机安全',
                value:3,
                itemStyle: {
                    color: '#505050'
                },
                label:{
                    color:'#505050',
                },
            }]
        }]
    }]
}];

//定义图形样式
option = {
    backgroundColor: '#1B72C6', //背景色

    //系列列表
    series: [{
        type: 'sunburst', //图表类型为旭日图
        radius:[0,'90%'], //内半径和外半径
        center: ['50%', '50%'],//中心点
        data: data, //读取列表data中的数据
        roam:true,
        nodeClick:false,
        //文本签的样式
        label: {
            rotate: 'radial', //旋转角为”径向旋转“
            //fontWeight: 545, //文字字体粗细
            fontSize:a*0.009,
            lineHeight:15,
        },
        //旭日图扇形块的样式
        itemStyle: {
            borderColor: '#F8F8FF',
            // borderColor: '#333333',//边框颜色
            borderWidth: 2,//边框粗细
        },
        //多层配置
        levels: [{/*留给数据下钻的空白配置*/},
        {   // 最靠内测的第一层
            r0: '0%', //内半径
            r: '25%', //外半径
            //文本签样式
            label: {
                rotate: 'radial',
                color:'#F8F8FF' //字体颜色
                                // color:'#333333'
            }
        }, {//第二层
            r0: '25%',
            r: '50.5%',
            label: {
                rotate: 'radial',
                color:'#F8F8FF'
                // color:'#333333'
            }
        }, {//第三层
            r0: '55%',
            r: '65%',
            itemStyle: {
                shadowBlur: 2, //图形阴影的模糊大小

                color: 'transparent', //设置颜色为透明
            },
            label: {
                rotate: 'tangential', //文字”切向旋转“
                //fontSize: 10, //字号
            }
        }, {//第四层
            r0: '66.5%',
            r: '70%',
            itemStyle: {
                shadowBlur: 0,//图形阴影的模糊大小
                shadowColor: '#F8F8FF'//阴影颜色
                // shadowColor: '#FFAE57'//阴影颜色
            },
            label: {
                position: 'outside', //标签的位置
                textShadowBlur: 0, //文字本身的阴影长度
                textShadowColor: '#F8F8FF', //文字本身的阴影颜色
                // textShadowColor: '#333', //文字本身的阴影颜色
            },
            //鼠标悬停后不相关扇形块的配置项
            downplay: {
                label: {
                    opacity: 0.5 //透明度（值越大透明度越小）
                }
            }
        }]
    }]
};
        //使用制定的配置项和数据显示图表
        chart1.setOption(option);
        //自适应
        window.onresize = function () {
                
            chart1.resize();
            
        }

}
