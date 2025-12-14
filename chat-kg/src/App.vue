<script setup>
import { KeepAlive } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="app-container">
    <header class="app-header glass">
      <div class="header-content">
        <div class="logo-section">
          <span class="logo-icon">🧠</span>
          <span class="logo-text gradient-text">ChatKG</span>
        </div>

        <nav class="main-nav">
          <RouterLink to="/" class="nav-link" active-class="active">
            <span class="nav-icon">🏠</span>
            <span class="nav-text">Home</span>
          </RouterLink>
          <RouterLink to="/chat" class="nav-link" active-class="active">
            <span class="nav-icon">💬</span>
            <span class="nav-text">Chat</span>
          </RouterLink>
          <RouterLink to="/kg" class="nav-link" active-class="active">
            <span class="nav-icon">🔗</span>
            <span class="nav-text">Graph</span>
          </RouterLink>
          <RouterLink to="/about" class="nav-link" active-class="active">
            <span class="nav-icon">ℹ️</span>
            <span class="nav-text">About</span>
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>
  </div>
</template>

<style lang="less" scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-page);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  border-bottom: 1px solid var(--color-neutral-150);
  animation: fadeInDown var(--duration-slow) var(--ease-out);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-3) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.logo-icon {
  font-size: var(--text-2xl);
}

.logo-text {
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  letter-spacing: var(--tracking-tight);
}

.main-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  background: var(--color-neutral-100);
  padding: var(--space-1);
  border-radius: var(--radius-xl);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-lg);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-neutral-600);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-default);
  position: relative;

  &:hover {
    color: var(--color-neutral-800);
    background: var(--color-neutral-200);
  }

  &.active {
    color: var(--color-primary-700);
    background: var(--color-neutral-0);
    box-shadow: var(--shadow-sm);

    .nav-icon {
      transform: scale(1.1);
    }
  }
}

.nav-icon {
  font-size: var(--text-base);
  transition: transform var(--duration-fast) var(--ease-spring);
}

.nav-text {
  line-height: 1;
}

.app-main {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-6);
}

@media (max-width: 768px) {
  .header-content {
    padding: var(--space-3) var(--space-4);
    flex-direction: column;
    gap: var(--space-3);
  }

  .logo-section {
    align-self: flex-start;
  }

  .main-nav {
    width: 100%;
    justify-content: center;
  }

  .nav-link {
    padding: var(--space-2) var(--space-3);
  }

  .nav-text {
    display: none;
  }

  .nav-icon {
    font-size: var(--text-lg);
  }

  .app-main {
    padding: 0 var(--space-4);
  }
}
</style>
