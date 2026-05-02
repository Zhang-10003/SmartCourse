<template>
  <div class="match-ui-container">
    <div v-if="question.question_title" class="question-title-container">
      <div class="tag-row">
        <span class="tag">{{ question.isMultiple ? '多选题' : '单选题' }}</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ index }}.</span>
        <span class="question-text">{{ question.question_title }}</span>
      </div>
    </div>

    <div class="options-grid">
      <div
        v-for="(option, idx) in question.options"
        :key="idx"
        class="match-card"
        :class="getOptionClass(idx)"
        @click="selectOption(idx)"
      >
        <div class="card-body">
          <span class="card-label">{{ option }}</span>
        </div>

        <div class="status-box" v-if="status === 'result' && selectedOptions.includes(idx)">
          <div v-if="correctAnswer.includes(idx)" class="checkmark"></div>
          <div v-else class="cross"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionMultipleChoice",
  props: {
    index: { type: [Number, String], default: 1 },
    question: { type: Object, required: true },
    disabled: { type: Boolean, default: false },
    status: { type: String, default: "typing" },
    correctAnswer: { type: Array, default: () => [] },
    // 1. 修改这里：Vue 3 默认 prop 名是 modelValue
    modelValue: { type: Array, default: () => [] }
  },
  computed: {
    selectedOptions() {
      // 2. 修改这里：指向 modelValue
      return this.modelValue
    }
  },
  methods: {
    selectOption(index) {
      if (this.disabled || this.status === "result") return;

      let newSelected = []
      if (!this.question.isMultiple) {
        newSelected = [index];
      } else {
        newSelected = [...this.selectedOptions]
        const i = newSelected.indexOf(index);
        if (i > -1) {
          newSelected.splice(i, 1);
        } else {
          newSelected.push(index);
        }
      }
      // 3. 修改这里：触发 Vue 3 的更新事件
      this.$emit("update:modelValue", newSelected);
      // 如果父组件还需要这个自定义事件，可以保留
      this.$emit("answer-change", newSelected);
    },

    getOptionClass(idx) {
      const classes = [];
      const isSelected = this.selectedOptions.includes(idx);
      const isRight = this.correctAnswer.includes(idx);
      const isResult = this.status === "result";
      
      // 注意：这里逻辑修正，判断是否有答案
      const hasAnswer = this.selectedOptions && this.selectedOptions.length > 0;

      if (!isResult) {
        if (isSelected) classes.push("is-active");
        return classes;
      }

      if (isSelected) {
        classes.push(isRight ? "my-correct" : "my-wrong");
      } else {
        if (this.question.isMultiple && isRight) {
          classes.push("miss-correct");
        }
      }

      if (this.disabled || isResult) classes.push("is-disabled");
      return classes;
    }
  }
};
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
.question-index {
  margin-right: 8px;
  flex-shrink: 0;
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
  background: #fff;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
}
.match-card.is-active {
  border-color: #3b82f6;
  background-color: #f0f7ff;
  transform: scale(1.02);
}
.match-card.my-correct {
  border-color: #49b972 !important;
  background-color: #f2faf5 !important;
}
.match-card.my-wrong {
  border-color: #f56c6c !important;
  background-color: #fef0f0 !important;
}
.match-card.miss-correct {
  border-color: #f56c6c !important;
  background-color: #fff0f0 !important;
}
.match-card.is-disabled {
  cursor: not-allowed;
}
.card-label {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}
.status-box {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.my-correct .status-box {
  background: #49b972;
}
.my-wrong .status-box {
  background: #f56c6c;
}
.checkmark {
  width: 5px;
  height: 10px;
  border: solid #fff;
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
}
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
  background-color: #fff;
}
.cross::before { transform: rotate(45deg); }
.cross::after { transform: rotate(-45deg); }
</style>