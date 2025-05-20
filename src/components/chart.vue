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
      classes: classes,
      filter:{},
      ALL: true,
    };
  },
  mounted() {
    this.initChart();
    this.initFilter();
  },
  beforeUnmount() {
    // 组件卸载前销毁图表
    if (this.chartInstance) {
      this.chartInstance.dispose();
      this.chartInstance = null;
    }
  },
  methods: {
    initFilter(){
      for (let i in this.classes){
        this.filter[i] = false
      }
    },
    handleAll(){
      if (this.ALL != true){
        this.initFilter()
        this.handleFilter()
      }
      this.ALL = true
    },
    changeFilter(key) {
      console.log(this.filter)
      if (this.filter.hasOwnProperty(key)) {
        this.filter[key] = !this.filter[key];
        this.handleFilter();
      }
    },
    handleFilter(){
      const selectedKeys = Object.entries(this.filter)
        .filter(([_, value]) => value)
        .map(([key]) => key);
      if (selectedKeys.length === 0){
        this.ALL = true
        this.chartInstance.setOption(this.changeOption(),true);
      }else{
        this.ALL = false
        const newSeris = []
        for (var i in selectedKeys){
          newSeris.push.apply(newSeris,this.ttk.filter(item => this.classes[selectedKeys[i]].includes(item["id"])))
        }
        this.chartInstance.setOption(this.changeOption({
          series: newSeris,
        }),true);
        if (Object.values(selectedKeys).includes("精确射手步枪") != true){
          this.chartInstance.setOption({
            yAxis:{
              max: 'dataMax',
            }
          })
        }
      }
    },
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
    changeOption(newOption){
      // 修改option,无参数则默认
      const option = {
        grid: {
          top: '35px',
          right: '230px',
          bottom: '3%',
          left: '20px',
          containLabel: true
        },
        backgroundColor: '#212121',
        tooltip: {},
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: 10,
          top: 30,
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
  <div ref="main_container" style="width: 100%;"> 
    <div ref="chartContainer" style="width: 100%; height: 600px; min-width: 750px;"></div>
  </div>
  <div style="display: flex; flex-direction: row ; align-items: center; justify-content: space-between; padding: 0 30px;">
    <div v-for="(item, index) in classes" :key="index" class="checkbox">
      <button class="checkbtn" :class="{active: this.filter[index]}" @click="changeFilter(index)">
        <span class="label">{{ index }}</span>
      </button>
    </div>
    <div class="checkbox">
      <button class="checkbtn" :class="{active: this.ALL}" @click="handleAll(ALL)">
        <span class="label">ALL</span>
      </button>
    </div>
  </div>
</template>
<style scoped>
.checkbox {
  display: flex;
  align-items: center;
  padding: 10px 0;
  font-family: Arial, sans-serif;
  color: black;
}

.checkbtn {
  width: 150px;
  height: 80px;
  background: #212121;
  outline: 0 solid #307B6E;
  border-radius: 15px;
  color: #000;
  box-shadow: 0 0 0 1px #50BBAA;
  transition: outline-width 0.2s;
  border-width: 0px;
  box-sizing: border-box;
}
.label { 
  font-size: 18px;
  font-weight: 700;
  color: #ffffff7b;
}

.checkbtn:hover {
  outline-width: 8px;
}

.checkbtn.active {
  outline-width: 8px;
  outline-color: #50BBAA;
}
</style>