<template>
  <div class="welcome">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <img :src="image" alt="Placeholder Image" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('My ChatKG 😎')
const description = ref('一个简单的知识图谱聊天机器人')
const image = ref('https://news.jiangnan.edu.cn/__local/6/D9/98/C642DE3CDC7F72EC01C8A84FEE8_39252AC8_1D99C.jpg')
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
