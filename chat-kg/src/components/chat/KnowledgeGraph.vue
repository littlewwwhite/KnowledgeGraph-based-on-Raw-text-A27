<template>
  <div ref="graphContainer" class="knowledge-graph"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  graph: {
    type: Object,
    default: null
  }
})

const graphContainer = ref(null)
let chartInstance = null

const generateOption = (graph) => {
  if (!graph || !graph.nodes) return null

  const nodes = graph.nodes.map((node, idx) => ({
    ...node,
    id: idx,
    symbolSize: 5,
    label: { show: true }
  }))

  return {
    tooltip: {
      show: true,
      showContent: true,
      trigger: 'item',
      triggerOn: 'mousemove',
      alwaysShowContent: false,
      showDelay: 0,
      hideDelay: 200,
      enterable: false,
      position: 'right',
      confine: false,
      formatter: (x) => x.data.name
    },
    series: [
      {
        type: 'graph',
        draggable: true,
        layout: 'force',
        data: nodes,
        links: graph.links,
        categories: graph.categories,
        roam: true,
        label: {
          position: 'right'
        },
        force: {
          repulsion: 100
        },
        lineStyle: {
          color: 'source',
          curveness: 0.1
        }
      }
    ]
  }
}

const updateChart = () => {
  if (!chartInstance) return

  if (props.graph && props.graph.nodes && props.graph.nodes.length > 0) {
    const option = generateOption(props.graph)
    if (option) {
      chartInstance.setOption(option)
    }
  }
}

watch(
  () => props.graph,
  () => {
    updateChart()
  },
  { deep: true }
)

onMounted(() => {
  if (graphContainer.value) {
    chartInstance = echarts.init(graphContainer.value)
    updateChart()
  }
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style lang="less" scoped>
.knowledge-graph {
  width: 400px;
  height: 300px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 0.6px 2.3px rgba(0, 0, 0, 0.1),
    0px 1px 5px rgba(0, 0, 0, 0.08);
}
</style>
