<template>
  <div class="match-ui-container">
    <div v-if="question.question_title" class="question-title-container">
      <div class="tag-row">
        <span class="tag">匹配题</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ index }}.</span>
        <span class="question-text">{{ question.question_title }}</span>
      </div>
    </div>
    
    <div class="match-grid">
      <div class="match-column">
        <div 
          v-for="(item, idx) in question.leftItems" 
          :key="'l-' + idx"
          class="match-card"
          :class="{ 
            'is-active': !disabled && selectedLeft === idx,
            'is-matched': isLeftMatched(idx) && (disabled || isPairCorrect(idx, 'left')),
            'is-disabled': disabled
          }"
          :style="getMatchedStyle(idx, 'left')"
          @click="selectLeft(idx)"
        >
          <div class="card-body">
            <span class="card-label">{{ getItemLabel(item) }}</span>
          </div>
          <div 
            class="status-box" 
            v-if="isLeftMatched(idx) && isPairCorrect(idx, 'left')" 
            :style="getIconStyle(idx, 'left')"
          >
            <div class="checkmark"></div>
          </div>
        </div>
      </div>

      <div class="match-column">
        <div 
          v-for="(item, idx) in question.rightItems" 
          :key="'r-' + idx"
          class="match-card"
          :class="{ 
            'is-active': !disabled && selectedRight === idx,
            'is-matched': isRightMatched(idx) && (disabled || isPairCorrect(idx, 'right')),
            'is-disabled': disabled
          }"
          :style="getMatchedStyle(idx, 'right')"
          @click="selectRight(idx)"
        >
          <div class="card-body">
            <span class="card-label">{{ getItemLabel(item) }}</span>
          </div>
          <div 
            class="status-box" 
            v-if="isRightMatched(idx) && isPairCorrect(idx, 'right')" 
            :style="getIconStyle(idx, 'right')"
          >
            <div class="checkmark"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionMatching',
  props: {
    index: {
      type: [Number, String],
      default: 1
    },
    disabled: {
      type: Boolean,
      default: false
    },
    status: {
      type: String,
      default: 'typing'
    },
    correctAnswers: {
      type: Array,
      default: () => []
    },
    modelValue: {
      type: Array,
      default: () => []
    },
    question: {
      type: Object,
      required: true,
      default: () => ({
        leftItems: [],
        rightItems: []
      })
    }
  },
  data() {
    return {
      selectedLeft: null,
      selectedRight: null,
      completedMatches: [], 
      colorPalette: [
        { bg: '#f2faf5', main: '#49b972' }, // 绿色
        { bg: '#f0f7ff', main: '#3b82f6' }, // 蓝色
        { bg: '#fff7ed', main: '#f97316' }, // 橙色
        { bg: '#fdf2f8', main: '#ec4899' }, // 粉色
        { bg: '#f5f3ff', main: '#8b5cf6' }  // 紫色
      ]
    }
  },
  created() {
    if (this.modelValue && this.modelValue.length > 0) {
      this.completedMatches = this.modelValue.map((match, idx) => ({
        ...match,
        colorIndex: match.colorIndex !== undefined ? match.colorIndex : idx % this.colorPalette.length
      }));
    }
  },
  methods: {
    getItemLabel(item) {
      if (typeof item === 'string') return item;
      return item.label || '';
    },
    selectLeft(index) {
      if (this.disabled || this.status === 'result') return;
      this.selectedLeft = (this.selectedLeft === index) ? null : index;
      this.checkMatch();
    },
    selectRight(index) {
      if (this.disabled || this.status === 'result') return;
      this.selectedRight = (this.selectedRight === index) ? null : index;
      this.checkMatch();
    },
    checkMatch() {
      if (this.selectedLeft !== null && this.selectedRight !== null) {
        this.completedMatches = this.completedMatches.filter(
          m => m.l !== this.selectedLeft && m.r !== this.selectedRight
        );
    
        this.completedMatches.push({
          l: this.selectedLeft,
          r: this.selectedRight,
          colorIndex: this.selectedLeft % this.colorPalette.length 
        });
    
        this.$emit('answer-change', this.completedMatches);
        this.$emit('update:modelValue', this.completedMatches);
        this.selectedLeft = null;
        this.selectedRight = null;
      }
    },
    // 判断当前配对是否正确
    isPairCorrect(index, side) {
      if (this.status !== 'result') return true; // 答题模式默认显示颜色
      const match = this.completedMatches.find(m => side === 'left' ? m.l === index : m.r === index);
      if (!match) return false;
      return this.correctAnswers.some(ans => ans.l === match.l && ans.r === match.r);
    },
    getMatchedStyle(index, side) {
      const match = this.completedMatches.find(m => side === 'left' ? m.l === index : m.r === index);
      if (match) {
        if (this.status === 'result' && !this.isPairCorrect(index, side)) {
          return {};
        }
        const color = this.colorPalette[match.colorIndex];
        return {
          backgroundColor: color.bg,
          borderColor: color.main,
          borderWidth: '2px',
          transform: this.disabled ? 'none' : 'scale(1.02)'
        };
      }
      return {};
    },
    getIconStyle(index, side) {
      const match = this.completedMatches.find(m => side === 'left' ? m.l === index : m.r === index);
      return (match && this.isPairCorrect(index, side)) ? { backgroundColor: this.colorPalette[match.colorIndex].main } : {};
    },
    isLeftMatched(index) {
      return this.completedMatches.some(m => m.l === index);
    },
    isRightMatched(index) {
      return this.completedMatches.some(m => m.r === index);
    }
  }
}
</script>

<style scoped>
.question-title-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  text-align: left;
  width: 100%;
  max-width: 800px;
}

.tag-row {
  display: flex;
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

.question-text {
  word-break: break-all;
}

.match-ui-container {
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.match-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  width: 100%;
  max-width: 800px;
}

.match-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.match-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  min-height: 60px;
  background: #ffffff;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
}

.match-card:hover:not(.is-disabled) {
  border-color: #49b972;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.match-card.is-active {
  border: 1.5px dashed #666;
  background-color: #fafafa;
  transform: translateY(-2px);
}

.match-card.is-disabled {
  pointer-events: none;
}

.card-body {
  flex: 1;
  display: flex;
  align-items: center;
  margin-right: 12px;
  overflow: hidden;
}

.card-label {
  font-size: 16px;
  color: #333;
  font-weight: 500;
  line-height: 1.4;
  word-break: break-word;
  text-align: left;
}

.status-box {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.checkmark {
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
  margin-bottom: 2px;
}

.match-card.is-disabled {
  background-color: #fafafa;
  border-color: #d9d9d9;
  cursor: not-allowed;
}

.match-card.is-disabled .card-label {
  color: #999;
}

@media (max-width: 600px) {
  .match-grid { gap: 12px; }
  .match-card { padding: 12px 14px; min-height: 50px; }
  .card-label { font-size: 14px; }
  .status-box { width: 20px; height: 20px; }
}
</style>