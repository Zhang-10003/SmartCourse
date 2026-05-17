<template>
  <div class="report-grid">
    
    <div class="glass-card">
      <h2 class="card-title">
        <i class="ri-bar-chart-2-line"></i> 知识点掌握分布
      </h2>
      
      <div class="card-body">
        <div class="progress-group">
          <div 
            v-for="(item, index) in reportData.knowledgeDistribution" 
            :key="'kb-' + index" 
            class="progress-item"
          >
            <div class="progress-info">
              <span>{{ item.title }}</span>
              <span :style="{ color: item.color }">{{ item.percentage }}%</span>
            </div>
            <div class="progress-track">
              <div 
                class="progress-bar" 
                :style="{ width: item.percentage + '%', backgroundColor: item.color }"
              ></div>
            </div>
          </div>
        </div>

        <div class="llm-panel">
          <h4><i class="ri-robot-line"></i> LLM 智能化反馈总结</h4>
          <ul class="llm-list">
            <li v-for="(feedback, fIndex) in reportData.llmFeedback" :key="'fb-' + fIndex">
              {{ fIndex + 1 }}. <strong>{{ feedback.label }}：</strong>{{ feedback.text }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="glass-card">
      <h2 class="card-title">
        <i class="ri-lightbulb-line"></i> 后续教学与强化建议
      </h2>
      
      <div class="card-body">
        <div class="advice-stack">
          <div 
            v-for="(advice, aIndex) in reportData.teachingAdvice" 
            :key="'adv-' + aIndex" 
            class="advice-item"
          >
            <h5 :style="{ color: advice.color }">{{ advice.title }}</h5>
            <p>{{ advice.text }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps } from 'vue'

// 定义组件接收的属性，完美承接外部动态传入的 JSON 数据
defineProps({
  reportData: {
    type: Object,
    required: true,
    default: () => ({
      knowledgeDistribution: [],
      llmFeedback: [],
      teachingAdvice: []
    })
  }
})
</script>

<style scoped>
/* 引入基础变量 */
.report-grid {
  --border-color: rgba(226, 232, 240, 0.8);
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --primary-color: #3b82f6;

  display: grid;
  grid-template-columns: 1.1fr 0.9fr; 
  grid-template-rows: 1fr; /* 关键：强制左右卡片完全 1:1 等高对齐 */
  gap: 32px;
  width: 100%;
  max-width: 1200px;
  text-align: left;
}

/* 优雅的毛玻璃卡片样式 */
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
  height: 100%; 
  display: flex;
  flex-direction: column; 
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
}

.card-title i {
  font-size: 20px;
  color: var(--primary-color);
}

.card-body {
  flex: 1; 
  display: flex;
  flex-direction: column;
  justify-content: space-between; 
}

/* 进度条模块样式 */
.progress-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.progress-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.progress-track {
  height: 8px;
  background: rgba(226, 232, 240, 0.8);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* LLM 反馈面板样式 */
.llm-panel {
  margin-top: 32px;
  background: rgba(59, 130, 246, 0.03);
  border-left: 4px solid var(--primary-color);
  padding: 20px;
  border-radius: 0 16px 16px 0;
}

.llm-panel h4 {
  color: var(--primary-color);
  font-size: 15px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.llm-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.llm-list strong {
  color: var(--text-primary);
}

/* 后续教学建议垂直流样式 */
.advice-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.advice-item {
  background: #ffffff;
  border: 1px solid var(--border-color);
  padding: 20px;
  border-radius: 16px;
  flex: 1; 
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.advice-item h5 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
}

.advice-item p {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>