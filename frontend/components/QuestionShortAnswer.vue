<template>
  <div class="match-ui-container">
    <div v-if="question.title" class="question-title-container">
      <div class="tag-row">
        <span class="tag">简答题</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ index }}.</span>
        <span class="question-text">{{ question.title }}</span>
      </div>
    </div>

    <div class="answer-area">
      <textarea
        class="answer-input"
        :class="{ 'is-result': status === 'result' }"
        :placeholder="status === 'result' ? '' : placeholder"
        :value="value"
        @input="handleInput"
        :disabled="status === 'result'"
        rows="5"
      ></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionShortAnswer',
  props: {
    // 外部绑定的答案内容
    value: {
      type: String,
      default: ''
    },
    index: {
      type: [Number, String],
      default: 1
    },
    question: {
      type: Object,
      required: true,
      default: () => ({ title: '' })
    },
    // typing: 答题模式; result: 结果只读模式
    status: {
      type: String,
      default: 'typing'
    },
    placeholder: {
      type: String,
      default: '请输入您的答案...'
    }
  },
  methods: {
    handleInput(e) {
      // 如果是结果模式，拒绝任何输入处理
      if (this.status === 'result') return;
      
      const val = e.target.value;
      // 仅向上传递数据，不维护内部副本以保持纯净
      this.$emit('input', val);
      this.$emit('answer-change', val);
    }
  }
}
</script>

<style scoped>
.match-ui-container {
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.question-title-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  text-align: left;
  width: 100%;
  /* 确保在小屏幕下不会溢出 */
  max-width: 800px;
  box-sizing: border-box; 
}

.tag {
  background-color: #e6f4ff;
  color: #1677ff;
  font-size: 13px;
  padding: 2px 10px;
  border-radius: 4px;
  font-weight: 500;
  align-self: flex-start;
}

.title-row {
  display: flex;
  align-items: flex-start;
  font-size: 17px;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
}

.question-index {
  margin-right: 8px;
  flex-shrink: 0;
}

.answer-area {
  width: 100%;
  max-width: 800px;
}

.answer-input {
  width: 100%;
  padding: 16px;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  font-size: 15px;
  color: #333;
  line-height: 1.6;
  resize: none;
  outline: none;
  transition: all 0.2s ease;
  /* 关键：确保 padding 不会撑破 100% 宽度 */
  box-sizing: border-box; 
  background-color: #fff;
  font-family: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  /* 解决 iOS 上默认的内阴影问题 */
  -webkit-appearance: none;
}

/* 答题中：焦点效果 */
.answer-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 结果模式 */
.answer-input.is-result {
  background-color: #f9f9f9;
  border-color: #e0e0e0;
  color: #666;
  cursor: not-allowed;
  box-shadow: none;
}

/* 移动端深度优化 */
@media (max-width: 640px) {
  .match-ui-container {
    padding: 16px; /* 减小外层边距 */
  }
  
  .question-title-container {
    margin-bottom: 16px;
    gap: 8px;
  }

  .title-row {
    font-size: 16px; /* 稍微缩小字号防止题目过长换行太多 */
  }

  .answer-input {
    padding: 12px;
    font-size: 14px;
    border-radius: 10px; /* 减小圆角，适配小屏幕 */
  }
}
</style>