<script>
import * as echarts from 'echarts';
import { markRaw } from 'vue';

// 测试用例，主要是原始数据之前还没做好，屎山还在叠加，不过不如重生的SHIT
import ttk_ttm_data from '@/data/ttk_ttm.js';
// const ttk_ttm_data = {
//   "冲锋枪": {
//     "P2020（双持）": { "rank": 1, "TTK": 0.87, "TTM": 1.41 },
//     "猎兽冲锋枪全自动": { "rank": 2, "TTK": 0.91, "TTM": 1.67 },
//     "R-99": { "rank": 3, "TTK": 0.88, "TTM": 1.12 },
//     "电能冲锋枪": { "rank": 4, "TTK": 0.92, "TTM": 1.25 },
//     "C.A.R.": { "rank": 5, "TTK": 0.84, "TTM": 1.20 }
//   },
//   "步枪": {
//     "赫姆洛克三连发": { "rank": 1, "TTK": 1.24, "TTM": 2.76 },
//     "哈沃克全自动": { "rank": 2, "TTK": 0.83, "TTM": 1.49 },
//     "VK-47 平行步枪": { "rank": 3, "TTK": 1.00, "TTM": 1.60 },
//     "R-301 卡宾枪": { "rank": 4, "TTK": 0.93, "TTM": 1.17 }
//   },
//   "霰弹枪": {
//     "和平捍卫者(进空投）紫枪栓": { "rank": 1, "TTK": 0.73, "TTM": 1.50 },
//     "敖犬": { "rank": 2, "TTK": 0.98, "TTM": 1.45 },
//     "EVA-8": { "rank": 3, "TTK": 1.05, "TTM": 1.22 },
//     "莫桑比克": { "rank": 4, "TTK": 1.50, "TTM": 1.00 }
//   },
//   "狙击枪": {
//     "克雷贝尔": { "rank": 1, "TTK": 0.25, "TTM": 1.80 },
//     "充能步枪": { "rank": 2, "TTK": 0.75, "TTM": 1.25 },
//     "长弓": { "rank": 3, "TTK": 1.10, "TTM": 1.60 },
//     "哨兵": { "rank": 4, "TTK": 0.85, "TTM": 1.40 }
//   },
//    "机枪": {
//     "专注": { "rank": 1, "TTK": 0.78, "TTM": 2.50 },
//     "喷火": { "rank": 2, "TTK": 0.95, "TTM": 2.80 },
//     "L-STAR": { "rank": 3, "TTK": 0.90, "TTM": 1.90 }
//   },
//   "弓箭": {
//     "波塞克": { "rank": 1, "TTK": 0.60, "TTM": 2.20 }
//   }
// };

// 默认图表配置，参考 chart.vue
const DEFAULT_OPTIONS = {
    backgroundColor: '#212121',
    grid: {
        top: '20px',
        right: '350px',
        bottom: '100px', // 增加底部边距以缩小图表高度
        left: '150px',
        containLabel: false
    },
    tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(33, 33, 33, 0.9)',
        borderColor: '#50BBAA',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: (params) => {
            const { seriesName, data, color } = params;
            if (!data) return '';
            const [ttk, ttm, rank, category] = data; // 从数据点中解构信息
            return `
        <div style="font-weight: bold; margin-bottom: 8px;">
          <span style="display: inline-block; width: 10px; height: 10px; background-color: ${color}; border-radius: 50%; margin-right: 8px;"></span>
          ${seriesName}
        </div>
        <div style="padding-left: 18px;">在 ${category} 中排名第 <span style="font-weight: bold;">${rank}</span></div>
        <div style="padding-left: 18px;">TTK: <span style="font-weight: bold;">${ttk.toFixed(3)}s</span></div>
        <div style="padding-left: 18px;">TTM: <span style="font-weight: bold;">${ttm.toFixed(3)}s</span></div>
      `;
        }
    },
    legend: {
        type: 'scroll',
        orient: 'vertical',
        right: 20,
        top: 60,
        bottom: 60,
        textStyle: {
            fontSize: 14,
            color: '#fff'
        },
    },
    xAxis: {
        type: 'value',
        name: '←左上更好         Time-To-Kill (s)',
        nameLocation: 'middle',
        nameGap: 35,
        nameTextStyle: { fontSize: 16, color: '#ccc' },
        axisLabel: { formatter: '{value} s', color: '#ccc' },
        splitLine: { lineStyle: { color: '#444' } },
        interval: 0.2 // 强制刻度步长为 0.5
    },
    yAxis: {
        type: 'value',
        name: 'Time-To-Miss (s)      左上更好→',
        nameLocation: 'middle',
        nameGap: 55,
        nameTextStyle: { fontSize: 16, color: '#ccc' },
        axisLabel: { formatter: '{value} s', color: '#ccc' },
        splitLine: { lineStyle: { color: '#444' } },
        interval: 1 // 强制刻度步长为 0.5
    },
    dataZoom: [
        { type: 'inside', xAxisIndex: 0 },
        { type: 'inside', yAxisIndex: 0 },
        { type: 'slider', xAxisIndex: 0, bottom: 20, height: 25 },
    ],
};


export default {
    data() {
        return {
            chartInstance: null,
            ttk_ttm: ttk_ttm_data,
            categories: [],
            filter: {},
            ALL: true,
        };
    },
    mounted() {
        this.initCategoriesAndFilter();
        this.initChart();
        window.addEventListener('resize', this.resizeChart);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.resizeChart);
        if (this.chartInstance) {
            this.chartInstance.dispose();
            this.chartInstance = null;
        }
    },
    methods: {
        /**
         * 初始化图表实例并设置其初始配置。
         */
        initChart() {
            const chartDom = this.$refs.chartContainer;
            this.chartInstance = markRaw(echarts.init(chartDom, 'dark'));
            this.updateChartSeries([]); // 初始加载所有数据
        },

        /**
         * 将原始数据格式化为 ECharts 所需的 series 格式。
         * @param {string[]} selectedCategories - 要包含的类别名称数组。如果为空，则包含所有类别。
         * @returns {object[]} ECharts 的 series 对象数组。
         */
        formatChartData(selectedCategories = []) {
            const seriesData = [];
            const categoriesToProcess = selectedCategories.length > 0 ? selectedCategories : this.categories;

            for (const category of categoriesToProcess) {
                if (this.ttk_ttm[category]) {
                    for (const weaponName in this.ttk_ttm[category]) {
                        const weaponData = this.ttk_ttm[category][weaponName];
                        seriesData.push({
                            name: weaponName,
                            type: 'scatter',
                            // 将 TTK, TTM, Rank 和类别名称存储在数据数组中
                            data: [[weaponData.TTK, weaponData.TTM, weaponData.rank, category]],
                            symbolSize: 12,
                            emphasis: {
                                focus: 'series',
                                label: {
                                    show: true,
                                    formatter: '{b}',
                                    position: 'top',
                                    color: '#fff',
                                    fontSize: 14,
                                }
                            }
                        });
                    }
                }
            }
            return seriesData;
        },

        /**
         * 从数据中提取类别名称并初始化筛选器状态。
         */
        initCategoriesAndFilter() {
            this.categories = Object.keys(this.ttk_ttm);
            this.categories.forEach(cat => {
                this.filter[cat] = false;
            });
        },

        /**
         * 处理类别筛选器按钮的点击事件。
         */
        changeFilter(category) {
            this.filter[category] = !this.filter[category];
            this.handleFilter();
        },

        /**
         * 处理“ALL”按钮的点击事件，重置所有筛选器。
         */
        handleAll() {
            this.ALL = true;
            this.categories.forEach(cat => {
                this.filter[cat] = false;
            });
            this.updateChartSeries([]);
        },

        /**
         * 根据当前的筛选器状态应用筛选。
         */
        handleFilter() {
            const selectedCategories = this.categories.filter(cat => this.filter[cat]);

            if (selectedCategories.length === 0) {
                this.handleAll();
                return;
            }

            this.ALL = false;
            this.updateChartSeries(selectedCategories);
        },

        /**
         * 根据所选类别更新图表的 series 数据。
         */
        updateChartSeries(selectedCategories) {
            const newSeries = this.formatChartData(selectedCategories);
            const option = {
                ...DEFAULT_OPTIONS,
                series: newSeries
            };
            this.chartInstance.setOption(option, { replaceMerge: ['series'] });
        },

        /**
         * 调整图表大小以适应窗口。
         */
        resizeChart() {
            if (this.chartInstance) {
                this.chartInstance.resize();
            }
        }
    }
};
</script>

<template>
    <div class="main-container">
        <div ref="chartContainer" class="chart-container"></div>
        <div class="controls-container">
            <div v-for="category in categories" :key="category" class="checkbox">
                <button class="checkbtn" :class="{ active: filter[category] }" @click="changeFilter(category)">
                    <span class="label">{{ category }}</span>
                </button>
            </div>
            <div class="checkbox">
                <button class="checkbtn" :class="{ active: ALL }" @click="handleAll">
                    <span class="label">ALL</span>
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main-container {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #212121;
}

.chart-container {
    width: 100%;
    flex-grow: 1;
    /* 让图表容器占据所有可用垂直空间 */
    min-height: 0;
    /* 防止 flex item 溢出 */
}

.controls-container {
    flex-shrink: 0;
    /* 防止控制容器被压缩 */
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    padding: 10px 0 20px 0;
    background-color: #212121;
}

.checkbox {
    display: flex;
    align-items: center;
    padding: 10px 15px;
    font-family: Arial, sans-serif;
}

.checkbtn {
    width: 168px;
    height: 100px;
    background: #212121;
    outline: 0 solid #307B6E;
    border-radius: 15px;
    box-shadow: 0 0 0 1px #50BBAA;
    transition: outline-width 0.2s, background-color 0.2s;
    border-width: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.label {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff7b;
    transition: color 0.2s;
}

.checkbtn:hover {
    outline-width: 8px;
}

.checkbtn.active {
    outline-width: 8px;
    outline-color: #50BBAA;
}

.checkbtn.active .label {
    color: #ffffff;
}
</style>
