/**
 * 将TTK数据转换为ECharts图表格式，并将小数转换为百分比
 * @param {Object} ttks - TTK数据对象
 * @param {Object} names - 武器名称映射对象
 * @returns {Array} ECharts series格式的数据
 */
const chartDataFormatter = (ttks, names) => {
  return Object.entries(ttks).map(([id, data]) => ({
    id,
    name: names[id],
    type: 'line',
    data: data.map(([x, y]) => [x * 100, y])
  }));
};

export { chartDataFormatter };