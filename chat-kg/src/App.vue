<script setup>
import { KeepAlive } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

// 打印当前页面的路由信息，使用 vue3 的 setup composition API
const route = useRoute()
console.log(route)



</script>

<template>
  <header class="header">
    <nav class="nav">
      <RouterLink to="/" class="nav-item">主页</RouterLink>
      <RouterLink to="/chat" class="nav-item" active-class="active">问答</RouterLink>
      <RouterLink to="/kg" class="nav-item" active-class="active">图谱</RouterLink>
      <RouterLink to="/about" class="nav-item" active-class="active">关于</RouterLink>
    </nav>
  </header>

    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
</template>

<style lang="less" scoped>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 40px 0;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-item {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: transparent;
  color: #333;
  font-size: 16px;
  transition: background-color 0.2s ease-in-out;
  margin: 0 10px;
}

.nav-item:hover {
  background-color: #eee;
  cursor: pointer;
}

.nav-item.active {
  background-color: #333;
  color: #fff;
}
</style>
