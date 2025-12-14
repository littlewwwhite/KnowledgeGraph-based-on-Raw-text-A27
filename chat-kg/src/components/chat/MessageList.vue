<template>
  <div ref="chatBox" class="chat-box">
    <div
      v-for="message in messages"
      :key="message.id"
      class="message-box"
      :class="message.type"
    >
      <img v-if="message.filetype === 'image'" :src="message.url" class="message-image" alt="">
      <p v-else style="white-space: pre-line" class="message-text">{{ message.text }}</p>
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

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight - chatBox.value.clientHeight
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
  padding: 1rem;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;

  &::-webkit-scrollbar {
    width: 0rem;
  }
}

.message-box {
  width: fit-content;
  display: inline-block;
  padding: 0.5rem;
  border-radius: 0.5rem;
  margin: 0.5rem 0;
  box-sizing: border-box;
  padding: 10px 16px;
  user-select: text;
  word-break: break-word;
  font-size: 14px;
  line-height: 20px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
  font-weight: 400;
  box-shadow: 0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16);
  max-width: 80%;
}

.message-box.sent {
  color: white;
  background-color: #efefef;
  background: linear-gradient(90deg, #40788c 10.79%, #005f77 87.08%);
  align-self: flex-end;
}

.message-box.received {
  color: #111111;
  background-color: #ffffff;
  text-align: left;
}

p.message-text {
  word-wrap: break-word;
  margin-bottom: 0;
}

img.message-image {
  max-width: 300px;
  max-height: 50vh;
  object-fit: contain;
}
</style>
