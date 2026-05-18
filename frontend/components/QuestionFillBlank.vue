<template>
  <div class="match-ui-container">
    <div v-if="question && question.content" class="question-title-container">
      <div class="tag-row">
        <span class="tag">填空题</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ index }}.</span>
        <div class="question-text">
          <span v-for="(part, i) in parsedData.parts" :key="'part-' + i">
            {{ part }}
            <span v-if="i < parsedData.blanksCount" class="inline-placeholder">
              ( {{ i + 1 }} )
            </span>
          </span>
        </div>
      </div>
    </div>

    <div class="options-grid">
      <div 
        v-for="(_, idx) in parsedData.blanksCount" 
        :key="'blank-' + idx"
        class="match-card"
        :class="{ 
          'is-correct': status === 'result' && isCorrect(idx),
          'is-wrong': status === 'result' && !isCorrect(idx),
          'is-disabled': status === 'result'
        }"
      >
        <div class="card-body">
          <span class="card-label">空格 {{ idx + 1 }}</span>
          <input
            type="text"
            class="code-input"
            placeholder="请输入答案"
            v-model="localAnswers[idx]"
            @input="handleInput"
            :disabled="disabled || status === 'result'"
          />
        </div>

        <div class="status-box-wrapper" v-if="status === 'result'">
          <div :class="['status-box', isCorrect(idx) ? 'bg-correct' : 'bg-wrong']">
            <div v-if="isCorrect(idx)" class="checkmark"></div>
            <div v-else class="cross"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionFillBlank',
  props: {
    index: { type: [Number, String], default: 1 },
    question: { 
      type: Object, 
      required: true,
      default: () => ({ content: '' }) 
    },
    disabled: { type: Boolean, default: false },
    status: { type: String, default: 'typing' },
    correctAnswers: { type: Array, default: () => [] },
    modelValue: { type: Array, default: () => [] }
  },
  emits: ['answer-change', 'update:modelValue'],
  data() {
    return {
      localAnswers: []
    }
  },
  computed: {
    parsedData() {
      const content = this.question.content || '';
      const parts = content.split('????');
      return {
        parts,
        blanksCount: parts.length - 1
      };
    }
  },
  methods: {
    handleInput() {
      this.$emit('answer-change', [...this.localAnswers]);
      this.$emit('update:modelValue', [...this.localAnswers]);
    },
    isCorrect(idx) {
      if (!this.correctAnswers || this.correctAnswers.length === 0) return false;
      const userAns = (this.localAnswers[idx] || '').toString().trim();
      const correctAns = (this.correctAnswers[idx] || '').toString().trim();
      return userAns !== '' && userAns === correctAns;
    }
  },
  watch: {
    'question.content': {
      immediate: true,
      handler(newContent) {
        const count = this.parsedData.blanksCount;
        const arr = new Array(count).fill('');
        this.localAnswers = this.modelValue && this.modelValue.length === count ? [...this.modelValue] : arr;
      }
    },
    modelValue: {
      handler(val) {
        if (val && val.length > 0) this.localAnswers = [...val];
      }
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
  width: 100%;
  max-width: 800px;
}
.tag {
  background-color: #e6f4ff;
  color: #1677ff;
  font-size: 13px;
  padding: 2px 10px;
  border-radius: 4px;
  font-weight: 500;
  width: fit-content;
}
.title-row {
  display: flex;
  font-size: 17px;
  font-weight: 600;
  color: #333;
  line-height: 1.6;
}
.question-index { margin-right: 8px; }
.inline-placeholder { color: #1677ff; margin: 0 4px; font-weight: 600; }
.options-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 800px;
}

/* 默认卡片样式 */
.match-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  min-height: 64px;
  background: #ffffff;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* 仅保留结果状态的样式 */
.match-card.is-correct {
  border: 2px solid #49b972;
  background-color: #f2faf5;
}
.match-card.is-wrong {
  border: 2px solid #f56c6c;
  background-color: #fef0f0;
}

.card-body { display: flex; align-items: center; flex: 1; }
.card-label { font-size: 14px; color: #8c8c8c; margin-right: 20px; font-weight: 500; white-space: nowrap; }
.code-input { flex: 1; border: none; background: transparent; font-size: 16px; color: #333; font-weight: 500; outline: none; }

.status-box {
  width: 24px; height: 24px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center; margin-left: 12px;
}
.bg-correct { background-color: #49b972; }
.bg-wrong { background-color: #f56c6c; }
.checkmark {
  width: 5px; height: 10px; border: solid white;
  border-width: 0 2.5px 2.5px 0; transform: rotate(45deg); margin-bottom: 2px;
}
.cross { position: relative; width: 12px; height: 12px; }
.cross::before, .cross::after {
  content: ''; position: absolute; top: 50%; left: 0; width: 12px; height: 2px; background-color: white;
}
.cross::before { transform: rotate(45deg); }
.cross::after { transform: rotate(-45deg); }
.is-disabled { 
  cursor: not-allowed; 
  background-color: #fafafa;
  border-color: #d9d9d9;
}

.is-disabled .code-input {
  background-color: #f5f5f5;
  border-color: #d9d9d9;
  color: #999;
  cursor: not-allowed;
}

.is-disabled .card-label {
  color: #999;
}
</style>