<template>
  <div class="match-ui-container">
    <div class="tag-row">
      <span class="tag">单选题</span>
    </div>

    <!-- 题干部分 -->
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

    <!-- 选项部分 -->
    <div class="options-container">
      <div
        v-for="(option, idx) in localQuestion.options"
        :key="idx"
        class="opt-card"
        :class="{ 'is-selected': currentAnswerIndex === idx }"
        @click="setCorrect(idx)"
      >
        <div class="opt-content">
          <span class="opt-label">{{ String.fromCharCode(65 + idx) }}.</span>
          <input 
            v-model="localQuestion.options[idx]" 
            class="opt-text-input" 
            placeholder="输入选项内容"
            @click.stop
          />
        </div>

        <div class="opt-actions">
          <div 
            v-if="localQuestion.options.length > 2"
            class="delete-btn" 
            @click.stop="removeOption(idx)"
          >×</div>
        </div>
      </div>

      <div class="add-btn-card" @click="addOption">
        <span>+ 添加新选项</span>
      </div>
    </div>

    <!-- 答案解析部分 (新增) -->
    <div class="feedback-section">
      <div class="section-divider"></div>
      
      <div class="feedback-header">
        <div class="left-labels">
          <span class="tag answer-tag">答案解析</span>
          <span class="answer-indicator">
            当前正确项：<strong>{{ String.fromCharCode(65 + currentAnswerIndex) }}</strong>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionSingleEditor",
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: { 
      type: Object, 
      default: () => ({
        title: '',
        options: ['', '', '', ''],
        analysis: '' // 确保数据结构里有这个字段
      })
    },
    answer: { type: [Number, Array], default: 0 }
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    },
    currentAnswerIndex() {
      return Array.isArray(this.answer) ? this.answer[0] : this.answer;
    }
  },
  methods: {
    setCorrect(idx) {
      const val = Array.isArray(this.answer) ? [idx] : idx;
      this.$emit('update:answer', val);
    },
    addOption() {
      this.localQuestion.options.push('');
    },
    removeOption(idx) {
      const newOptions = [...this.localQuestion.options];
      newOptions.splice(idx, 1);
      this.localQuestion.options = newOptions;

      // 调整正确答案索引
      if (this.currentAnswerIndex === idx) {
        this.setCorrect(0);
      } else if (this.currentAnswerIndex > idx) {
        this.setCorrect(this.currentAnswerIndex - 1);
      }
    }
  }
};
</script>

<style scoped>
.match-ui-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 16px;
  box-sizing: border-box;
}

.tag-row {
  margin-bottom: 4px;
}
.tag {
  background: #e6f4ff;
  color: #1677ff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

/* 题干样式 */
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
.q-input-wrapper {
  flex: 1;
}
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

/* 选项卡片 */
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
  font-size: 16px;
}
.opt-text-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #434343;
}

.delete-btn {
  color: #bfbfbf;
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
  transition: color 0.2s;
}
.delete-btn:hover {
  color: #ff4d4f;
}

.add-btn-card {
  border: 1px dashed #d9d9d9;
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  color: #8c8c8c;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}
.add-btn-card:hover {
  border-color: #1677ff;
  color: #1677ff;
  background: #f0f7ff;
}

/* 答案解析部分 (新增样式) */
.feedback-section {
  margin-top: 24px;
}
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
.answer-indicator strong {
  color: #52c41a;
}

.ai-gen-btn {
  font-size: 13px;
  color: #722ed1;
  background: #f9f0ff;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  border: 1px solid #efdbff;
  transition: all 0.2s;
}
.ai-gen-btn:hover {
  background: #f0e1ff;
  box-shadow: 0 2px 4px rgba(114, 46, 209, 0.1);
}

.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
  transition: all 0.3s;
}
.feedback-card:focus-within {
  background: #fff;
  border-color: #b7eb8f;
  box-shadow: 0 0 0 2px rgba(82, 196, 26, 0.06);
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
.char-count {
  font-size: 12px;
  color: #bfbfbf;
}
</style>