<template>
  <div class="graph-container">
    <div id="graph-main" ref="chartRef"></div>
    <!-- <div id="graph-info">
      <div class="search-area">
        <input type="text" v-model="state.searchText" placeholder="输入关键词搜索" />
      </div>
      <div class="node-info">
        <div class="node-card" v-for="(sent, idx) in state.nodeInfo" :key="idx">
          <div class="node-sent" v-html="sent"></div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
const state = reactive({
  graph: {},
  searchText: '',
  showInfo: true,
  nodeInfo: []
})

let myChart;

const fetchWebkitDepData = () => {
  axios.get('/api/graph').then(response => response.data.data)
    .then(webkitDep => {
      state.graph = webkitDep
      myChart.hideLoading()
      webkitDep.nodes.forEach(function (node) {
        node.label = {
          show: node.symbolSize > 100
        }
        node.symbolSize = node.symbolSize / 10
      })
      const option = {
        tooltip: {
          show: true, //默认值为true
          showContent: true, //是否显示提示框浮层
          trigger: 'item', //触发类型，默认数据项触发
          triggerOn: 'mousemove', //提示触发条件，mousemove鼠标移至触发，还有click点击触发
          alwaysShowContent: false, //默认离开提示框区域隐藏，true为一直显示
          showDelay: 0, //浮层显示的延迟，单位为 ms，默认没有延迟，也不建议设置。在 triggerOn 为 'mousemove' 时有效。
          hideDelay: 200, //浮层隐藏的延迟，单位为 ms，在 alwaysShowContent 为 true 的时候无效。
          enterable: false, //鼠标是否可进入提示框浮层中，默认为false，如需详情内交互，如添加链接，按钮，可设置为 true。
          position: 'right', //提示框浮层的位置，默认不设置时位置会跟随鼠标的位置。只在 trigger 为'item'的时候有效。
          confine: false, //是否将 tooltip 框限制在图表的区域内。外层的 dom 被设置为 'overflow: hidden'，或者移动端窄屏，导致 tooltip 超出外界被截断时，此配置比较有用。
          // transitionDuration: 0.1, //提示框浮层的移动动画过渡时间，单位是 s，设置为 0 的时候会紧跟着鼠标移动。
          formatter: (x) => x.data.name
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            animation: false,
            label: {
              position: 'right',
              formatter: '{b}'
            },
            draggable: true,
            data: webkitDep.nodes.map(function (node, idx) {
              node.id = idx;
              return node;
            }),
            modularity: true, // 开启社区划分
            categories: webkitDep.categories,
            force: {
              edgeLength: 5,
              repulsion: 20,
              gravity: 0.2
            },
            lineStyle: {
              color: 'source',
              curveness: 0.1
            },
            edges: webkitDep.links,
            roam: true, // 开启鼠标缩放和平移漫游
            focusNodeAdjacency: true, // 高亮显示鼠标移入节点的邻接节点
          }
        ],
        // animationDuration: 1500, // 初始动画的时长
        // animationEasingUpdate: 'quinticInOut', // 数据更新动画的缓动效果
      }
      myChart.setOption(option)
    })
}

const getNeighborNodes = (node) => {
  const nodes = []
  // 遍历所有的边，找到与当前节点相连的节点
  state.graph.links.forEach(function (link) {
    if (link.source === node.id || link.target === node.id) {
      nodes.push(state.graph.nodes[link.source])
      nodes.push(state.graph.nodes[link.target])
    }
  })

  // 去除当前节点
  nodes.forEach(function (item, index) {
    if (item.id === node.id) {
      nodes.splice(index, 1)
    }
  })

  return nodes
}

const colorfulSents = (node, nerborNodes, sents) => {
  const nerborNodeNames = nerborNodes.map((item) => item.name)
  console.log(nerborNodeNames)
  const colorfulSents = sents.map((sent) => {
    sent = sent.replace(node.name, `<span style="color: #47c640">${node.name}</span>`)
    nerborNodeNames.forEach((name) => {
      sent = sent.replace(name, `<span style="color: #df2024">${name}</span>`)
    })
    return sent
  })
  return colorfulSents
}

const clickNode = (param) => {
  console.log('点击了', param)

  if (param.dataType === 'node') {
    state.showInfo = true
    const sents = param.data.lines.map((item) => state.graph.sents[item])
    const nerborNodes = getNeighborNodes(param.data)
    state.nodeInfo = colorfulSents(param.data, nerborNodes, sents)
  }
}

onMounted(() => {
  myChart = echarts.init(chartRef.value)
  myChart.showLoading()
  fetchWebkitDepData()
  chart.value.on('click', clickNode)
})
</script>

<style lang="less" scoped>
.graph-container {
  display: flex;
  flex-direction: row;
  max-width: 100%;
  height: calc(100vh - 200px);
  gap: 20px;
}

#graph-main,
#graph-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: 100%;
  background: #f5f5f5;
  border-radius: 8px;
}

#graph-main {
  width: 100%;
}

#graph-info {
  width: 400px;
  padding: 2rem 1rem;
  overflow: scroll;

  .search-area {
    // 优化 input 和 button 的样式
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 40px;
    margin-bottom: 1rem;

    input {
      flex: 1;
      width: 100%;
      padding: 0.5rem 1rem;
      background-color: #fff;
      border: none;
      border-radius: 8px;
      // box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1);
      font-size: 0.8rem;
      margin: 1rem 1rem;
      color: #111111;
      line-height: 22px;
      font-variation-settings: 'wght' 400, 'opsz' 10.5;
      transition: all 0.3s;
    }

    input:focus {
      outline: 2px solid #999;
    }

    // place holder
    input::-webkit-input-placeholder {
      color: #999999;
    }
  }
}

#graph-info,
.node-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow: scroll;

  // 隐藏滚动条
  &::-webkit-scrollbar {
    display: none;
  }
}

.node-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  width: 100%;
  height: 100%;
  overflow: scroll;
}

#graph-info .node-sent {
  margin: 1rem 0;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05);
  font-size: 0.8rem;
  color: #111111;
  line-height: 22px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
  transition: all 0.3s;
}
</style>
