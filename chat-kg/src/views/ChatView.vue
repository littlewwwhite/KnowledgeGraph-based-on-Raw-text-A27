<template>
  <div class="chat">
    <div ref="chatBox" class="chat-box">
      <div
        v-for="message in state.messages"
        :key="message.id"
        class="message-box"
        :class="message.type"
      >
        <img v-if="message.filetype === 'image'" :src="message.url" class="message-image" alt="">
        <p v-else style="white-space: pre-line" class="message-text">{{ message.text }}</p>
      </div>
    </div>
    <div class="input-box">
      <button @click="clearChat"><clear-outlined /></button>
      <input
        type="text"
        class="user-input"
        v-model="state.inputText"
        @keydown.enter="sendMessage"
        placeholder="输入问题……"
      />
      <button @click="sendMessage" :disabled="!state.inputText"><send-outlined /></button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { SendOutlined, ClearOutlined } from '@ant-design/icons-vue'

const chatBox = ref(null)
const state = reactive({
  history: [],
  messages: [],
  inputText: ''
})

const appendMessage = (message, type) => {
  state.messages.push({
    id: state.messages.length + 1,
    type,
    text: message
  })
  // 滚动到底部
  setTimeout(() => {
    chatBox.value.scrollTop = chatBox.value.scrollHeight - chatBox.value.clientHeight
  }, 10)
}


const appendPicMessage = (pic, type) => {
  state.messages.push({
    id: state.messages.length + 1,
    type,
    filetype: "image",
    url: pic
  })
  // 滚动到底部
  setTimeout(() => {
    chatBox.value.scrollTop = chatBox.value.scrollHeight - chatBox.value.clientHeight
  }, 10)
}

const updateLastReceivedMessage = (message, id) => {
  const lastReceivedMessage = state.messages.find((message) => message.id === id)
  if (lastReceivedMessage) {
    lastReceivedMessage.text = message
  } else {
    state.messages.push({
      id,
      type: 'received',
      text: message
    })
  }
  // 滚动到底部
  setTimeout(() => {
    chatBox.value.scrollTop = chatBox.value.scrollHeight - chatBox.value.clientHeight
  }, 10)
}

const sendMessage = () => {
  if (state.inputText.trim()) {
    appendMessage(state.inputText, 'sent')
    appendMessage('正在回答……', 'received')
    const user_input = state.inputText
    const cur_res_id = state.messages[state.messages.length - 1].id
    state.inputText = ''
    fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        prompt: user_input,
        history: state.history
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then((response) => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let pic;
      // 逐步读取响应文本
      const readChunk = () => {
        return reader.read().then(({ done, value }) => {
          if (done) {
            if (pic) {
              setTimeout(() => {
                appendPicMessage(pic, 'received')
              }, 500);
            }
            console.log('Finished')
            return
          }

          buffer += decoder.decode(value, { stream: true })
          console.log(buffer)
          const message = buffer.trim().split('\n').pop()
          // 尝试解析 message
          try {
            const data = JSON.parse(message)
            updateLastReceivedMessage(data.updates.response, cur_res_id)
            state.history = data.history
            pic = data.image
            buffer = ''
          } catch (e) {
            console.log(e)
          }

          return readChunk()
        })
      }


      return readChunk()
    })
  } else {
    console.log('Please enter a message')
  }
}

const clearChat = () => {
  state.messages = []
  state.history = []
}

onMounted(() => {
  state.inputText = '你好'
  setTimeout(() => {
    sendMessage()
  }, 100);
})
</script>

<style lang="less" scoped>
.chat {
  display: flex;
  max-width: 800px;
  margin: 0 auto;
  flex-direction: column;
  height: calc(100vh - 200px);
  background: #f2f2f2;
  // border: 4px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 0.6px 2.3px rgba(0, 0, 0, 0.1),
    0px 1px 5px rgba(0, 0, 0, 0.08);
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;

  // 平滑滚动
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
  // background: linear-gradient(90deg, #006880 10.79%, #005366 87.08%);
  background: linear-gradient(90deg, #555 10.79%, #333 87.08%);
  // background-color: #333;
  align-self: flex-end;
}

.message-box.received {
  color: #111111;
  background-color: #f7f7f7;
  text-align: left;
}

p.message-text {
  word-wrap: break-word;
}

img.message-image {
  max-width: 300px;
  max-height: 50vh;
  object-fit: contain;
}

.input-box {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-top: 1px solid #ccc;
}

/* 编写一个好看的输入框，小圆角，白色背景，柔和的阴影 */
input.user-input {
  flex: 1;
  padding: 0.8rem 1rem;
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 1.2rem;
  margin: 0 1rem;
  color: #111111;
  font-size: 16px;
  line-height: 22px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1),
    0 0 0 3px rgba(0, 0, 0, 0.1);
}

button {
  padding: 0.8rem 1rem;
  // background: linear-gradient(90deg, #006880 10.79%, #005366 87.08%);
  background: linear-gradient(90deg, #555 10.79%, #333 87.08%);
  // background-color: #333;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  // background: #ccc;
  cursor: not-allowed;
}
</style>
