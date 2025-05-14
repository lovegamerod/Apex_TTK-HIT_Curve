<script>
import * as echarts from 'echarts';
import ttks from '@/data/id_stats.js';
import names from '@/data/id_name.js';
import { markRaw } from 'vue';
import classes from '@/data/Class.js';

export default {
  data() {
    return {
      chartInstance: null, // 存储图表实例
      ttk: this.percentage(ttks,names),
      name: names,
      classes: this.addall(classes,ttks),
      filter: "ALL"
    };
  },
  watch: {
    filter(newValue){
      if (newValue != "ALL"){
        this.chartInstance.setOption(this.changeOption({
          series: this.ttk.filter(item => this.classes[newValue].includes(item["id"])),
        }),true);
        // 若不包含波塞克则y轴最大值自动
        if (newValue != "Marksman"){
          this.chartInstance.setOption({
            yAxis:{
              max: 'dataMax',
            }
          })
        }
      }else{
        this.chartInstance.setOption(this.changeOption(),true);
      }
      console.log(this.chartInstance.getOption().yAxis[0].max)
    }
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
      // 将ttks中的数据转换为echarts的option中series的格式,并将小数处理成百分数
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
        item["id"] = i;
        item["name"] = names[i];
        item["type"] = "line";
        item["data"] = vals;
        result.push(item);
      }
      return result;
    },
    addall(classes,ttks) {
      // 为类别中加上全部
      classes["ALL"] = Object.keys(ttks)
      return classes;
    },
    changeOption(newOption){
      // 修改option,无参数则默认
      const option = {
        grid: {
          top: '10%',
          right: '30%',
          bottom: '3%',
          left: '5%',
          containLabel: true
        },
        backgroundColor: '#212121',
        tooltip: {},
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: 10,
          top: 20,
          bottom: 20,
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
            maxInterval: 1,
            minInterval: 0.3,
            splitNumber: 10
        },
        series: this.ttk
      };

      if (newOption){
        for (var i in newOption){
          option[i] = newOption[i];
        }
      }
      return option;
    },
    initChart() {
      // 初始化图表
      this.chartInstance = markRaw(echarts.init(this.$refs.chartContainer,"dark"));
      const option = this.changeOption();
      this.chartInstance.setOption(option);

      window.addEventListener('resize', ()=>{
        if (this.chartInstance) this.chartInstance.resize();
      });
    },
  }
};
</script>
<template>
  <div ref="main_container" style="width: 100%; height: 100%; overflow: auto;"> 
    <div ref="chartContainer" style="width: 100%; height: 600px; min-width: 750px;"></div>
  </div>
  <div style="display: flex; flex-direction: row ; align-items: center;">
    <div v-for="(item, index) in classes" style="flex-grow: 1;">
      <input type="radio" :key="index" :value="index" :id="index" v-model="filter"  />
      <label :key="index" :for="index">{{ index }}</label>
    </div>
  </div>
</template>