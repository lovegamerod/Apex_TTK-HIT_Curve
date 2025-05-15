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
      filter: [],
      ALL: true,
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
    handleAll(ALL){
      this.filter = []
      if (ALL != true){
        this.ALL = true
      }
      this.handleFilter(this.filter)
    },
    handleFilter(filter){
      if (filter.length === 0){
        this.ALL = true
        this.chartInstance.setOption(this.changeOption(),true);
      }else{
        this.ALL = false
        const newSeris = []
        for (var i in filter){
          newSeris.push.apply(newSeris,this.ttk.filter(item => this.classes[filter[i]].includes(item["id"])))
        }
        this.chartInstance.setOption(this.changeOption({
          series: newSeris,
        }),true);
        if (Object.values(filter).includes("Marksman") != true){
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
  <div style="display: flex; flex-direction: row ; align-items: center;">
    <div v-for="(item, index) in classes" :key="index" class="checkbox">
      <button>
        <label class="checkbox" :for="index">
          <span class="label">{{ index }}</span>
          <input type="checkbox" :value="index" :id="index" v-model="filter" @change="handleFilter(filter)" />
          <span class="checkmark"></span>
        </label>
      </button>
    </div>
    <div class="checkbox">
      <button>
        <label class="checkbox" for="ALL">
          <span class="label">ALL</span>
          <input type="checkbox" id="ALL" value="ALL" v-model="ALL" @change="handleAll(ALL)" />
          <span class="checkmark"></span>
        </label>        
      </button>
    </div>
  </div>
</template>
<style scoped>
.checkbox {
  display: flex;
  align-items: center;
  padding: 15px 25px;
  font-family: Arial, sans-serif;
  color: black;
}

.checkbox input {
  display: none;
}

.checkbox .checkmark {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  background-color: #ffffff2b;
  box-shadow: rgba(0, 0, 0, 0.62) 0px 0px 5px inset, rgba(0, 0, 0, 0.21) 0px 0px 0px 24px inset,
        #22cc3f 0px 0px 0px 0px inset, rgba(224, 224, 224, 0.45) 0px 1px 0px 0px;
  cursor: pointer;
  position: relative;
}

.checkbox .checkmark::after {
  content: "";
  width: 18px;
  height: 18px;
  border-radius: 5px;
  background-color: #e3e3e3;
  box-shadow: transparent 0px 0px 0px 2px, rgba(0, 0, 0, 0.3) 0px 6px 6px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: background-color 0.3s ease-in-out;
}

.checkbox input:checked + .checkmark {
  background-color: #22cc3f;
  box-shadow: rgba(0, 0, 0, 0.62) 0px 0px 5px inset, #22cc3f 0px 0px 0px 2px inset, #22cc3f 0px 0px 0px 24px inset,
        rgba(224, 224, 224, 0.45) 0px 1px 0px 0px;
}

.checkbox input:checked + .checkmark::after {
  background-color: white;
}

.checkbox .label {
  margin-top: 3px;
  margin-right: 8px;
  user-select: none;
  font-weight: 700;
  cursor: pointer;
  color: #ffffff7b;
}

button {
  color: #090909;
  padding: 0;
  margin-right: -29px;
  margin-left: 25px;
  font-size: 18px;
  border-radius: 0.5em;
  background: linear-gradient(145deg, #1e1e1e, #232323);
  cursor: pointer;
  border: 1px solid #212121;
  transition: all 0.3s;
  box-shadow: 18px 18px 18px #1c1c1c, -18px -18px 18px #262626;
  position: relative;
  overflow: hidden;
}

button:active {
  color: #666;
  box-shadow: inset 4px 4px 12px #1c1c1c, inset -4px -4px 12px #262626;
}
</style>