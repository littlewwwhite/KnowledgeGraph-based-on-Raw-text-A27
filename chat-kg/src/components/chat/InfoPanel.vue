<template>
  <div class="info">
    <h1>{{ title }}</h1>

    <p class="description" v-if="description && typeof description === 'string'">{{ description }}</p>
    <div v-else-if="description && Array.isArray(description)">
      <p class="description" v-for="(desc, index) in description" :key="index">{{ desc }}</p>
    </div>

    <img v-if="image && typeof image === 'string'" :src="image" class="info-image" alt="">
    <div v-else-if="image && Array.isArray(image)">
      <img v-for="(img, index) in image" :key="index" :src="img" class="info-image" alt="">
    </div>

    <p v-show="hasGraph"><b>关联图谱</b></p>
    <KnowledgeGraph v-show="hasGraph" :graph="graph" />

    <a-collapse v-model:activeKey="activeKey" v-if="hasSents" accordion>
      <a-collapse-panel
        v-for="(sent, index) in graph.sents"
        :key="index"
        :header="'相关描述 ' + (index + 1)"
        :show-arrow="false"
        ghost
      >
        <p>{{ sent }}</p>
      </a-collapse-panel>
    </a-collapse>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import KnowledgeGraph from './KnowledgeGraph.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: [String, Array],
    default: ''
  },
  image: {
    type: [String, Array],
    default: null
  },
  graph: {
    type: Object,
    default: null
  }
})

const activeKey = ref([])

const hasGraph = computed(() => {
  return props.graph && props.graph.nodes && props.graph.nodes.length > 0
})

const hasSents = computed(() => {
  return props.graph && props.graph.sents && props.graph.sents.length > 0
})
</script>

<style lang="less" scoped>
div.info {
  width: 400px;
  min-width: 400px;
  height: calc(100vh - 135px);
  overflow-y: auto;
  flex-grow: 0;
  scroll-behavior: smooth;

  &::-webkit-scrollbar {
    width: 0rem;
  }

  & > h1 {
    font-size: 1.5rem;
    margin: 0.5rem 0;
  }

  p.description {
    font-size: 1rem;
    margin: 0;
    margin-bottom: 20px;
  }

  img {
    width: 100%;
    height: fit-content;
    object-fit: contain;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }
}
</style>
