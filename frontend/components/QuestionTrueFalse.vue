<template>
  <div class="match-ui-container">
    <div v-if="question.question_title" class="question-title-container">
      <div class="tag-row">
        <span class="tag">判断题</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ index }}.</span>
        <span class="question-text">{{ question.question_title }}</span>
      </div>
    </div>

    <div class="options-grid">
      <div 
        v-for="option in [true, false]" 
        :key="option"
        class="match-card" 
        :class="{ 
          'is-active': selectedAnswer === option && status === 'typing',
          'is-correct': status === 'result' && selectedAnswer === option && selectedAnswer === correctAnswer,
          'is-wrong': status === 'result' && selectedAnswer === option && selectedAnswer !== correctAnswer,
          'is-disabled': disabled || status === 'result'
        }"
        @click="selectAnswer(option)"
      >
        <div class="card-body">
          <span class="card-label">{{ option ? '正确' : '错误' }}</span>
        </div>

        <div class="status-box" v-if="status === 'result' && selectedAnswer === option">
          <div v-if="selectedAnswer === correctAnswer" class="checkmark"></div>
          <div v-else class="cross"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionTrueFalse',
  props: {
    index: { type: [Number, String], default: 1 },
    question: { type: Object, required: true },
    disabled: { type: Boolean, default: false },
    status: { type: String, default: 'typing' },
    correctAnswer: { type: Boolean, default: null },
    modelValue: { type: Boolean, default: null }
  },
  computed: {
    selectedAnswer() {
      return this.modelValue;
    }
  },
  methods: {
    selectAnswer(answer) {
      if (this.disabled || this.status === 'result') return;
      this.$emit('update:modelValue', answer);
      this.$emit('answer-change', answer);
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
  max-width: 800px;
}

.tag {
  background-color: #e6f4ff;
  color: #1677ff;
  font-size: 13px;
  padding: 2px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.title-row {
  display: flex;
  align-items: flex-start;
  font-size: 17px;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
}

.options-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 800px;
}

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
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* 1. 答题中：选中的蓝色样式 */
.match-card.is-active {
  border: 2px solid #3b82f6;
  background-color: #f0f7ff;
  transform: scale(1.02);
}

/* 2. 结果：正确时的绿色样式 */
.match-card.is-correct {
  border: 2px solid #49b972;
  background-color: #f2faf5;
  transform: scale(1.02);
}

/* 3. 结果：错误时的红色样式 */
.match-card.is-wrong {
  border: 2px solid #f56c6c;
  background-color: #fef0f0;
  transform: scale(1.02);
}

.match-card.is-disabled {
  cursor: not-allowed;
}

.card-label {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

/* 状态盒子容器 */
.status-box {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 绿色勾选图标背景 */
.is-correct .status-box {
  background-color: #49b972;
}

/* 红色叉号图标背景 */
.is-wrong .status-box {
  background-color: #f56c6c;
}

/* 勾图标 */
.checkmark {
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
  margin-bottom: 2px;
}

/* 叉图标 (用伪元素画两条线) */
.cross {
  position: relative;
  width: 12px;
  height: 12px;
}
.cross::before, .cross::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 12px;
  height: 2px;
  background-color: white;
}
.cross::before { transform: rotate(45deg); }
.cross::after { transform: rotate(-45deg); }

@media (max-width: 600px) {
  .title-row { font-size: 17px; }
  .match-card { min-height: 56px; }
}
</style>