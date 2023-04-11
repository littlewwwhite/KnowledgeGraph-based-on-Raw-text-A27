<template>
  <div class="chat-container">
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
        <a-button size="large" @click="clearChat">
          <template #icon> <ClearOutlined /> </template>
        </a-button>
        <a-input
          type="text"
          class="user-input"
          v-model:value="state.inputText"
          @keydown.enter="sendMessage"
          placeholder="输入问题……"
        />
        <a-button size="large" @click="sendMessage" :disabled="!state.inputText">
          <template #icon> <SendOutlined /> </template>
        </a-button>
      </div>
    </div>
    <div class="info">
      <h1>{{ info.title }}</h1>
      <p class="description" >{{ info.description }}</p>
      <a-image v-if="info.image" :src="info.image" :alt="info.title"/>
      <!-- <p>三元组数量：{{ info.triples.length }}</p> -->
      <p v-show="info.graph?.nodes.length > 0"><b>关联图谱</b></p>
      <div id="lite_graph" v-show="info.graph?.nodes.length > 0"></div>
      <a-collapse v-model:activeKey="state.activeKey" v-if="info.graph?.sents.length > 0" accordion>
        <a-collapse-panel
          v-for="(sent, index) in info.graph.sents"
          :key="index"
          :header="'相关描述 ' + (index + 1)"
          :show-arrow="false"
          ghost
        >
          <p>{{ sent }}</p>
        </a-collapse-panel>
      </a-collapse>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts';
import { reactive, ref, onMounted } from 'vue'
import { SendOutlined, ClearOutlined } from '@ant-design/icons-vue'

let myChart = null;
const chatBox = ref(null)
const state = reactive({
  history: [],
  messages: [],
  activeKey: [],
  inputText: ''
})

const default_info = {
  title: '知识图谱问答 ChatKG',
  description: '由江南大学人工智能与计算机学院开发的基于知识图谱的问答系统，支持多轮对话，支持外部信息检索',
  image: 'https://news.jiangnan.edu.cn/__local/6/D9/98/C642DE3CDC7F72EC01C8A84FEE8_39252AC8_1D99C.jpg',
  graph: null,
}

const info = reactive({
  ...default_info
})

const scrollToBottom = () => {
  setTimeout(() => {
    chatBox.value.scrollTop = chatBox.value.scrollHeight - chatBox.value.clientHeight
  }, 10) // 10ms 后滚动到底部
}

const appendMessage = (message, type) => {
  state.messages.push({
    id: state.messages.length + 1,
    type,
    text: message
  })
  scrollToBottom()
}


const appendPicMessage = (pic, type) => {
  state.messages.push({
    id: state.messages.length + 1,
    type,
    filetype: "image",
    url: pic
  })
  scrollToBottom()
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
  scrollToBottom()
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
      let pic
      let wiki
      let graph
      // 逐步读取响应文本
      const readChunk = () => {
        return reader.read().then(({ done, value }) => {
          if (done) {
            console.log('Finished')
            return
          }

          info.image = pic
          info.graph = graph
          // 处理维基百科的内容
          info.title = wiki?.title
          info.description = wiki?.summary
          if (info.graph) {
            myChart.setOption(graphOption(info.graph));
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
            wiki = data.wiki
            graph = data.graph
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

const graphOption = (graph) => {
  console.log(graph)
  graph.nodes.forEach(node => {
    node.symbolSize = 5;
    node.label = {
      show: true
    }
  });
  let option = {
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
        draggable: true,
        layout: 'force',
        data: graph.nodes.map(function (node, idx) {
          node.id = idx;
          return node;
        }),
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
        },
      }
    ]
  };

  return option
}


const sendDeafultMessage = () => {
  setTimeout(() => {
    appendMessage('你好？我是 ChatKG，有什么可以帮你？', 'received')
  }, 1000);
}

const clearChat = () => {
  state.messages = []
  state.history = []
  info.title = default_info.title
  info.description = default_info.description
  info.image = default_info.image
  info.graph = default_info.graph
  info.sents = default_info.sents
  sendDeafultMessage()
}

onMounted(() => {
  sendDeafultMessage()
  myChart = echarts.init(document.getElementById('lite_graph'));

})
</script>

<style lang="less" scoped>
.chat-container {
  display: flex;
  gap: 1.5rem;
}

.chat {
  display: flex;
  width: 100%;
  max-width: 800px;
  flex-grow: 1;
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
  margin-bottom: 0;
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

input.user-input {
  flex: 1;
  height: 40px;
  padding: 0.5rem 1rem;
  background-color: #fff;
  border: none;
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 1.2rem;
  margin: 0 1rem;
  color: #111111;
  font-size: 16px;
  // line-height: 22px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
}

.ant-btn-icon-only {
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
}

// button:disabled {
//   // background: #ccc;
//   cursor: not-allowed;
// }

div.info {
  width: 400px;
  min-width: 400px;
  height: calc(100vh - 200px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  flex-grow: 0;

  // 平滑滚动
  scroll-behavior: smooth;

  &::-webkit-scrollbar {
    width: 0rem;
  }
  // background-color: #ccc;
  // margin: 0 1rem;

  & > h1 {
    font-size: 1.5rem;
    margin: 0.5rem 0;
    // padding: 0.5rem;
    // text-align: center;
  }

  & > p.description {
    font-size: 1rem;
    margin: 0;
    // padding: 0.5rem;
    // max-height: 10rem;
    margin-bottom: 20px;
    // text-align: center;
  }

  .ant-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 8px;
    overflow: hidden;
    overflow-y: hidden
  }

  #lite_graph {
    width: 400px;
    height: 300px;
    background: #f2f2f2;
    // border: 4px solid #ccc;
    border-radius: 8px;
    margin-bottom: 1rem;
    box-shadow: 0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 0.6px 2.3px rgba(0, 0, 0, 0.1),
      0px 1px 5px rgba(0, 0, 0, 0.08);
  }
}
</style>
