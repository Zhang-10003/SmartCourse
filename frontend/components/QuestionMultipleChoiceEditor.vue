<template>
  <div class="match-ui-container">
    <div class="tag-row">
      <span class="tag multiple-tag">多选题</span>
    </div>

    <!-- 题干部分 -->
    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          v-model="localQuestion.title" 
          class="q-textarea" 
          placeholder="请输入多选题题干内容..."
        ></textarea>
      </div>
    </div>

    <!-- 选项部分 -->
    <div class="options-container">
      <div
        v-for="(option, idx) in localQuestion.options"
        :key="idx"
        class="opt-card"
        :class="{ 'is-selected': isSelected(idx) }"
        @click="toggleCorrect(idx)"
      >
        <div class="opt-content">
          <!-- 多选框视觉反馈 -->
          <div class="checkbox-ui" :class="{ 'checked': isSelected(idx) }">
            <span v-if="isSelected(idx)">✓</span>
          </div>
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

    <!-- 答案解析部分 -->
    <div class="feedback-section">
      <div class="section-divider"></div>
      
      <div class="feedback-header">
        <div class="left-labels">
          <span class="tag answer-tag">答案解析</span>
          <span class="answer-indicator">
            正确答案：<strong>{{ formattedAnswer }}</strong>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionMultipleChoiceEditor",
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: { 
      type: Object, 
      default: () => ({
        title: '',
        options: ['', '', '', ''],
        analysis: ''
      })
    },
    // 多选题答案预期为数组，例如 [0, 2] 表示 A, C
    answer: { type: Array, default: () => [] }
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    },
    // 格式化后的答案字母，如 "A, B"
    formattedAnswer() {
      if (!this.answer || this.answer.length === 0) return '未设置';
      return [...this.answer]
        .sort((a, b) => a - b)
        .map(i => String.fromCharCode(65 + i))
        .join(', ');
    }
  },
  methods: {
    isSelected(idx) {
      return this.answer.includes(idx);
    },
    toggleCorrect(idx) {
      let newAnswer = [...this.answer];
      const foundIndex = newAnswer.indexOf(idx);
      
      if (foundIndex > -1) {
        // 如果已经选中，则移除（至少保留一个正确答案的逻辑可根据业务增加）
        newAnswer.splice(foundIndex, 1);
      } else {
        // 如果未选中，则添加
        newAnswer.push(idx);
      }
      this.$emit('update:answer', newAnswer);
    },
    addOption() {
      this.localQuestion.options.push('');
    },
    removeOption(idx) {
      // 1. 移除选项内容
      const newOptions = [...this.localQuestion.options];
      newOptions.splice(idx, 1);
      this.localQuestion.options = newOptions;

      // 2. 调整答案索引
      let newAnswer = this.answer
        .filter(item => item !== idx) // 移除已删除的项
        .map(item => (item > idx ? item - 1 : item)); // 后面的索引往前移
      
      this.$emit('update:answer', newAnswer);
    }
  }
};
</script>

<style scoped>
/* 继承大部分单选题样式，并增加多选特有样式 */
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
/* 多选题专属色调 */
.multiple-tag {
  background: #f9f0ff;
  color: #722ed1;
}

.question-header { display: flex; align-items: flex-start; margin-bottom: 16px; }
.q-index { font-size: 20px; font-weight: bold; line-height: 28px; margin-right: 8px; color: #722ed1; }
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
}

.options-container { display: flex; flex-direction: column; gap: 12px; }
.opt-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #f9f9f9;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.opt-card:hover { border-color: #d9d9d9; }
.opt-card.is-selected {
  border-color: #722ed1;
  background-color: #f9f0ff;
}

.opt-content { display: flex; align-items: center; flex: 1; }

/* 多选框 UI */
.checkbox-ui {
  width: 18px;
  height: 18px;
  border: 2px solid #d9d9d9;
  border-radius: 4px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: transparent;
  transition: all 0.2s;
  background: #fff;
}
.checkbox-ui.checked {
  background: #722ed1;
  border-color: #722ed1;
  color: #fff;
}

.opt-label { font-weight: 700; color: #722ed1; margin-right: 12px; font-size: 16px; }
.opt-text-input {
  flex: 1; border: none; outline: none; background: transparent;
  font-size: 15px; color: #434343;
}

.delete-btn { color: #bfbfbf; font-size: 20px; cursor: pointer; padding: 0 4px; }
.delete-btn:hover { color: #ff4d4f; }

.add-btn-card {
  border: 1px dashed #d9d9d9;
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  color: #8c8c8c;
  cursor: pointer;
}
.add-btn-card:hover { border-color: #722ed1; color: #722ed1; background: #f9f0ff; }

.feedback-section { margin-top: 24px; }
.section-divider { height: 1px; background: linear-gradient(to right, #eee 0%, #fff 100%); margin-bottom: 20px; }
.feedback-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.answer-tag { background: #f6ffed; color: #52c41a; border: 1px solid #d9f7be; }
.answer-indicator { font-size: 13px; color: #8c8c8c; margin-left: 10px; }
.answer-indicator strong { color: #52c41a; }

.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
}
.feedback-card:focus-within {
  background: #fff;
  border-color: #d3adf7;
  box-shadow: 0 0 0 2px rgba(114, 46, 209, 0.06);
}

.analysis-textarea {
  width: 100%; min-height: 90px; border: none; outline: none;
  background: transparent; font-size: 14px; line-height: 1.6; color: #595959; resize: vertical;
}
.card-footer { display: flex; justify-content: flex-end; margin-top: 8px; }
.char-count { font-size: 12px; color: #bfbfbf; }
</style>