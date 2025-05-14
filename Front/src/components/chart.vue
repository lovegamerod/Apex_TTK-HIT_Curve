<script>
import * as echarts from 'echarts';
import ttks from '../data/id_stats.js';
import names from '../data/id_name.js';
import { markRaw } from 'vue';

export default {
  data() {
    return {
      chartInstance: null, // 存储图表实例
      ttk: this.percentage(ttks,names),
      name: names,
    };
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    // 组件卸载前销毁图表
    if (this.chartInstance) {
      this.chartInstance.dispose();
      this.chartInstance = null;
    }
  },
  methods: {
    percentage(ttks,names) {
      var result = [];
      var item = {};
      var vals = [];
      var val = [];
      for (var i in ttks){
        item = {};
        vals = [];
        for (var j in ttks[i]){
          val = [];
          val[0] = ttks[i][j][0] *  100;
          val[1] = ttks[i][j][1];
          vals.push(val);
        }
        item["name"] = names[i];
        item["type"] = "line";
        item["data"] = vals;
        result.push(item);
      }
      return result;
    },
    initChart() {
      // 初始化图表
      this.chartInstance = markRaw(echarts.init(this.$refs.chartContainer));
      var keys = Object.keys(this.ttk);
      const option = {
        title: {
            text: "title"
        },
        tooltip: {},
        legend: {
          type: 'scroll',
          
        },
        xAxis: {
            type: 'value',
            axisLabel: {
              formatter: '{value} %',
              align: 'center'
            },
            min: 0,
            max: 100,
            interval: 10
        },
        yAxis: {
            type: 'value',
            axisLabel: {
              formatter: '{value} s',
              align: 'right'
            },
            min: 0,
            max: 10,
            maxInterval: 0.5
        },
        series: this.ttk
      };
      this.chartInstance.setOption(option);

      window.addEventListener('resize', function() {
        this.chartInstance?.resize();
      });
    },
  }
};
</script>
<template>
    <div ref="chartContainer" style="width: 600px; height: 400px;"></div>
</template>