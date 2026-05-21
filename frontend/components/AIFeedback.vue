<template>
  <div v-if="feedbackData" class="ai-feedback-component">
    <div class="ai-score-row">
      <span class="ai-label">得分：</span>
      <span class="ai-value">{{ feedbackData.score }}</span>
    </div>
    <div class="ai-text-row">
      <span class="ai-label">AI批改反馈：</span>
      <span class="ai-value">{{ feedbackData.feedback }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 定义组件的 Props，完美适配你前面给出的 JSON 结构
const props = defineProps({
  // 可以直接传整个响应 JSON (比如 mockResponseJson) 
  // 或者只传其中的 data 字段
  resJson: {
    type: Object,
    default: () => ({})
  }
})

// 计算属性：自动解析并提取 JSON 中的 score 和 feedback
const feedbackData = computed(() => {
  if (!props.resJson) return null
  
  // 如果直接传的是整个外层 JSON：{ code: 200, data: {...} }
  if (props.resJson.data) {
    return {
      score: props.resJson.data.score || '0/0',
      feedback: props.resJson.data.feedback || ''
    }
  }
  
  // 如果传的是内层 data：{ score: '...', feedback: '...' }
  if (props.resJson.score || props.resJson.feedback) {
    return {
      score: props.resJson.score || '0/0',
      feedback: props.resJson.feedback || ''
    }
  }
  
  return null
})
</script>

<style scoped>
/* 核心组件样式 */
.ai-feedback-component {
  border: none;
  padding: 30rpx;
  margin: 30rpx 0;
  font-size: 28rpx;
  line-height: 1.7;
  text-align: left;
  background: #fff5f5;
  border-radius: 16rpx;
}

/* 提示词颜色（红） */
.ai-label {
  color: #ff6b6b;
  font-weight: 600;
  font-size: 28rpx;
}

/* 冒号后面的内容颜色（完全复刻原图的黑） */
.ai-value {
  color: #333333;
  word-break: break-all;
  white-space: pre-wrap;
  font-size: 28rpx;
}

.ai-score-row {
  margin-bottom: 16rpx;
}

.ai-text-row {
  display: block;
}

.ai-score-row .ai-value {
  color: #ff6b6b;
  font-weight: 700;
  font-size: 36rpx;
}
</style>