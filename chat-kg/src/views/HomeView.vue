<template>
  <div class="welcome">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <img src="/homegraph.png" alt="Placeholder Image" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('My ChatKG 😎')
const description = ref('一个简单的知识图谱聊天机器人')
const image = ref('chat-kg/src/assets/homegraph.png')
</script>

<style scoped>
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
  color: #333;
  text-align: center;
}

h1 {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 20px;
  margin-top: 100px;
}

p {
  font-size: 24px;
  text-align: center;
  margin-bottom: 40px;
}

img {
  width: 700px;
  height: 400px;
  object-fit: cover;
  margin-top: 50px;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.05);
}
</style>
