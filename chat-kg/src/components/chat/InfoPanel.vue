<template>
  <div class="info-panel custom-scrollbar">
    <div class="panel-header">
      <div class="title-section">
        <span class="title-icon">💡</span>
        <h2 class="panel-title">{{ title }}</h2>
      </div>
    </div>

    <div class="panel-content">
      <!-- Description Section -->
      <div class="description-section" v-if="description">
        <p
          v-if="typeof description === 'string'"
          class="description-text"
        >
          {{ description }}
        </p>
        <div v-else-if="Array.isArray(description)" class="description-list">
          <p
            v-for="(desc, index) in description"
            :key="index"
            class="description-item"
          >
            {{ desc }}
          </p>
        </div>
      </div>

      <!-- Image Section -->
      <div class="image-section" v-if="image">
        <img
          v-if="typeof image === 'string'"
          :src="image"
          class="info-image"
          alt="Related image"
        >
        <div v-else-if="Array.isArray(image)" class="image-grid">
          <img
            v-for="(img, index) in image"
            :key="index"
            :src="img"
            class="info-image"
            alt="Related image"
          >
        </div>
      </div>

      <!-- Knowledge Graph Section -->
      <div class="graph-section" v-show="hasGraph">
        <div class="section-header">
          <span class="section-icon">🔗</span>
          <h3 class="section-title">Knowledge Graph</h3>
        </div>
        <div class="graph-container">
          <KnowledgeGraph :graph="graph" />
        </div>
      </div>

      <!-- Related Sentences Section -->
      <div class="sents-section" v-if="hasSents">
        <div class="section-header">
          <span class="section-icon">📝</span>
          <h3 class="section-title">Related Context</h3>
        </div>
        <a-collapse v-model:activeKey="activeKey" accordion class="custom-collapse">
          <a-collapse-panel
            v-for="(sent, index) in graph.sents"
            :key="index"
            :header="`Context ${index + 1}`"
            class="collapse-item"
          >
            <p class="sent-text">{{ sent }}</p>
          </a-collapse-panel>
        </a-collapse>
      </div>
    </div>
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
.info-panel {
  width: 380px;
  min-width: 380px;
  height: calc(100vh - 120px);
  overflow-y: auto;
  flex-shrink: 0;
  background: var(--color-neutral-0);
  border-radius: var(--radius-2xl);
  border: 1px solid var(--color-neutral-150);
  box-shadow: var(--shadow-lg);
  animation: slideInRight var(--duration-slow) var(--ease-out);
}

.panel-header {
  padding: var(--space-5) var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--color-neutral-150);
  background: linear-gradient(
    180deg,
    var(--color-neutral-0) 0%,
    var(--color-neutral-50) 100%
  );
  position: sticky;
  top: 0;
  z-index: 10;
}

.title-section {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.title-icon {
  font-size: var(--text-xl);
}

.panel-title {
  margin: 0;
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-neutral-800);
  line-height: var(--leading-tight);
}

.panel-content {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.description-section {
  animation: fadeInUp var(--duration-normal) var(--ease-out);
}

.description-text,
.description-item {
  margin: 0;
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--color-neutral-600);
}

.description-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.description-item {
  padding-left: var(--space-4);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 8px;
    width: 6px;
    height: 6px;
    background: var(--color-primary-400);
    border-radius: var(--radius-full);
  }
}

.image-section {
  animation: fadeInUp var(--duration-normal) var(--ease-out) 100ms both;
}

.image-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.info-image {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--duration-normal) var(--ease-default),
              box-shadow var(--duration-normal) var(--ease-default);

  &:hover {
    transform: scale(1.02);
    box-shadow: var(--shadow-md);
  }
}

.graph-section,
.sents-section {
  animation: fadeInUp var(--duration-normal) var(--ease-out) 200ms both;
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.section-icon {
  font-size: var(--text-base);
}

.section-title {
  margin: 0;
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-neutral-700);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}

.graph-container {
  background: var(--color-neutral-50);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-neutral-200);
  overflow: hidden;
}

// Custom collapse styles
.custom-collapse {
  background: transparent;
  border: none;

  :deep(.ant-collapse-item) {
    border: none;
    margin-bottom: var(--space-2);

    &:last-child {
      margin-bottom: 0;
    }
  }

  :deep(.ant-collapse-header) {
    padding: var(--space-3) var(--space-4) !important;
    background: var(--color-neutral-50);
    border-radius: var(--radius-md) !important;
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    color: var(--color-neutral-700);
    transition: all var(--duration-fast) var(--ease-default);

    &:hover {
      background: var(--color-neutral-100);
    }
  }

  :deep(.ant-collapse-content) {
    background: transparent;
    border: none;
  }

  :deep(.ant-collapse-content-box) {
    padding: var(--space-3) var(--space-4) !important;
  }
}

.sent-text {
  margin: 0;
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--color-neutral-600);
}

@media (max-width: 1200px) {
  .info-panel {
    width: 100%;
    min-width: 100%;
    height: auto;
    max-height: 50vh;
  }
}
</style>
