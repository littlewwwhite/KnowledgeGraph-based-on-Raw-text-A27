<template>
  <div ref="chatBox" class="chat-box custom-scrollbar">
    <div class="messages-wrapper">
      <div
        v-for="(message, index) in messages"
        :key="message.id"
        class="message-container"
        :class="message.type"
        :style="{ animationDelay: `${Math.min(index * 50, 200)}ms` }"
      >
        <div class="message-bubble" :class="message.type">
          <img v-if="message.filetype === 'image'" :src="message.url" class="message-image" alt="">
          <p v-else class="message-text">{{ message.text }}</p>
        </div>
        <span class="message-time">{{ formatTime(message.timestamp) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    required: true,
    default: () => []
  }
})

const chatBox = ref(null)

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTo({
        top: chatBox.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

watch(
  () => props.messages.length,
  () => {
    scrollToBottom()
  }
)

defineExpose({ scrollToBottom })
</script>

<style lang="less" scoped>
.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  background: linear-gradient(
    180deg,
    var(--color-neutral-50) 0%,
    var(--color-neutral-100) 100%
  );
}

.messages-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  min-height: 100%;
  justify-content: flex-end;
}

.message-container {
  display: flex;
  flex-direction: column;
  max-width: 75%;
  animation: fadeInUp var(--duration-normal) var(--ease-out) both;

  &.sent {
    align-self: flex-end;
    align-items: flex-end;
  }

  &.received {
    align-self: flex-start;
    align-items: flex-start;
  }
}

.message-bubble {
  position: relative;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-xl);
  word-break: break-word;
  transition: transform var(--duration-fast) var(--ease-default),
              box-shadow var(--duration-fast) var(--ease-default);

  &:hover {
    transform: translateY(-1px);
  }

  &.sent {
    background: var(--msg-sent-bg);
    color: var(--msg-sent-text);
    border-bottom-right-radius: var(--radius-sm);
    box-shadow: var(--shadow-primary);

    &:hover {
      box-shadow: 0 6px 20px rgba(60, 165, 191, 0.35);
    }
  }

  &.received {
    background: var(--msg-received-bg);
    color: var(--msg-received-text);
    border: 1px solid var(--msg-received-border);
    border-bottom-left-radius: var(--radius-sm);
    box-shadow: var(--shadow-sm);

    &:hover {
      box-shadow: var(--shadow-md);
    }
  }
}

.message-text {
  margin: 0;
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message-time {
  font-size: var(--text-xs);
  color: var(--color-neutral-400);
  margin-top: var(--space-1);
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-default);
}

.message-container:hover .message-time {
  opacity: 1;
}

.message-image {
  max-width: 280px;
  max-height: 45vh;
  object-fit: contain;
  border-radius: var(--radius-lg);
  display: block;
}

/* Typing indicator animation */
.message-bubble.received.typing {
  .message-text {
    display: flex;
    align-items: center;
    gap: 4px;

    &::after {
      content: '';
      display: inline-flex;
      width: 20px;
      height: 8px;
      background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 8'%3E%3Ccircle cx='4' cy='4' r='2' fill='%237d8a97'%3E%3Canimate attributeName='opacity' values='0.3;1;0.3' dur='1.2s' repeatCount='indefinite' begin='0s'/%3E%3C/circle%3E%3Ccircle cx='12' cy='4' r='2' fill='%237d8a97'%3E%3Canimate attributeName='opacity' values='0.3;1;0.3' dur='1.2s' repeatCount='indefinite' begin='0.2s'/%3E%3C/circle%3E%3Ccircle cx='20' cy='4' r='2' fill='%237d8a97'%3E%3Canimate attributeName='opacity' values='0.3;1;0.3' dur='1.2s' repeatCount='indefinite' begin='0.4s'/%3E%3C/circle%3E%3C/svg%3E") no-repeat;
      background-size: contain;
    }
  }
}

@media (max-width: 768px) {
  .chat-box {
    padding: var(--space-4);
  }

  .message-container {
    max-width: 85%;
  }

  .message-bubble {
    padding: var(--space-2) var(--space-3);
  }
}
</style>
