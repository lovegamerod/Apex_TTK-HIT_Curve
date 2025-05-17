<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-items">
        <!-- 导航按钮 -->
        <button
          v-for="tab in tabs"
          :key="tab.component"
          @click="currentTab = tab.component"
          :class="{ active: currentTab === tab.component }"
        >
          {{ tab.name }}
        </button>
      </div>
      
      <!-- 语言选择下拉框 -->
      <select v-model="selectedLanguage" @change="changeLanguage" class="language-select">
        <option value="zh">中文</option>
        <option value="en">English</option>
      </select>
    </nav>

    <!-- 内容区域 -->
    <main class="content">
      <component :is="currentTab" />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import chart from '@/components/chart.vue'
import list from '@/components/list.vue'

export default {
  components: {
    chart,
    list,
  },
  setup() {
    const currentTab = ref('chart')
    const selectedLanguage = ref('zh')
    const tabs = [
      { name: '首页', component: 'chart' },
      { name: '关于', component: 'list' },
    ]

    const changeLanguage = () => {
      // 这里可以添加实际的语言切换逻辑
      console.log('切换语言到:', selectedLanguage.value)
    }

    return {
      currentTab,
      selectedLanguage,
      tabs,
      changeLanguage
    }
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #333;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
}

.nav-items {
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #555;
}

button.active {
  background-color: #666;
  font-weight: bold;
}

.language-select {
  padding: 0.5rem;
  background-color: #444;
  color: white;
  border: 1px solid #666;
  border-radius: 4px;
}

.content {
  margin-top: 70px; /* 留出导航栏空间 */
  padding: 1rem;
}
</style>