<template>
  <div class="match-ui-container">
    <!-- 顶部标签，参考单选题设计 -->
    <div class="tag-row">
      <span class="tag">判断题</span>
    </div>

    <!-- 题干部分：完全参考 QuestionChoiceEditor.vue 的无边框设计 -->
    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          v-model="localQuestion.title" 
          class="q-textarea" 
          placeholder="请输入题干内容..."
        ></textarea>
      </div>
    </div>

    <!-- 选项部分：结合 QuestionTrueFalse.vue 的样式与编辑器的选中逻辑 -->
    <div class="options-container">
      <div
        v-for="opt in judgeOptions"
        :key="opt.value"
        class="opt-card"
        :class="{ 'is-selected': modelValue.answer === opt.value }"
        @click="setCorrect(opt.value)"
      >
        <div class="opt-content">
          <!-- 这里的 label 参考单选题 A/B 的位置，改为 正确/错误[cite: 1, 2] -->
          <span class="opt-label">{{ opt.label }}.</span>
          <span class="opt-text-display">{{ opt.text }}</span>
        </div>

        <!-- 选中状态指示[cite: 1] -->
        <div class="opt-actions" v-if="modelValue.answer === opt.value">
          <div class="check-mark">✓</div>
        </div>
      </div>
    </div>

    <!-- 答案解析部分：完全复刻单选题底部的反馈区域[cite: 1] -->
    <div class="feedback-section">
      <div class="section-divider"></div>
      
      <div class="feedback-header">
        <div class="left-labels">
          <span class="tag answer-tag">答案解析</span>
          <span class="answer-indicator">
            当前正确项：<strong>{{ modelValue.answer ? '正确' : '错误' }}</strong>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionTrueFalseEditor",
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: { 
      type: Object, 
      default: () => ({
        title: '',
        answer: true, // true 为正确，false 为错误
        analysis: ''
      })
    }
  },
  data() {
    return {
      judgeOptions: [
        { label: '√', text: '正确', value: true },
        { label: '×', text: '错误', value: false }
      ]
    };
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    }
  },
  methods: {
    setCorrect(val) {
      // 保持与单选题一致的更新模式[cite: 1]
      const updated = { ...this.modelValue, answer: val };
      this.$emit('update:modelValue', updated);
    }
  }
};
</script>

<style scoped>
/* 基础容器参考单选题[cite: 1] */
.match-ui-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 16px;
  box-sizing: border-box;
}

.tag-row { margin-bottom: 4px; }
.tag {
  background: #e6f4ff;
  color: #1677ff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

/* 题干样式：完全复刻单选题的无边框大字设计[cite: 1] */
.question-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}
.q-index {
  font-size: 20px;
  font-weight: bold;
  line-height: 28px;
  margin-right: 8px;
  color: #1677ff;
}
.q-input-wrapper { flex: 1; }
.q-textarea {
  width: 100%;
  border: none;
  outline: none;
  font-size: 18px;
  font-weight: bold;
  color: #262626;
  background: transparent;
  resize: none;
  padding: 0;
  margin: 0;
  line-height: 28px;
  height: 56px; 
  min-height: 56px;
  display: block;
}

/* 选项卡片：结构参考单选题[cite: 1] */
.options-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.opt-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #f9f9f9;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.opt-card:hover {
  border-color: #d9d9d9;
  background: #f5f5f5;
}
.opt-card.is-selected {
  border-color: #3b82f6;
  background-color: #eff6ff;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.1);
}

.opt-content {
  display: flex;
  align-items: center;
  flex: 1;
}
.opt-label {
  font-weight: 700;
  color: #1677ff;
  margin-right: 12px;
  font-size: 18px;
}
.opt-text-display {
  font-size: 15px;
  color: #434343;
  font-weight: 500;
}

.check-mark {
  color: #1677ff;
  font-size: 18px;
  font-weight: bold;
}

/* 答案解析样式：完全复刻单选题[cite: 1] */
.feedback-section { margin-top: 24px; }
.section-divider {
  height: 1px;
  background: linear-gradient(to right, #eee 0%, #fff 100%);
  margin-bottom: 20px;
}
.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.answer-tag {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #d9f7be;
}
.answer-indicator {
  font-size: 13px;
  color: #8c8c8c;
  margin-left: 10px;
}
.answer-indicator strong { color: #52c41a; }

.ai-gen-btn {
  font-size: 13px;
  color: #722ed1;
  background: #f9f0ff;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  border: 1px solid #efdbff;
}

.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
}
.analysis-textarea {
  width: 100%;
  min-height: 90px;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  line-height: 1.6;
  color: #595959;
  resize: vertical;
}
.card-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}
.char-count { font-size: 12px; color: #bfbfbf; }
</style>