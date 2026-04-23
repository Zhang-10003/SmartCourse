<template>
  <div class="match-ui-container">
    <div class="match-grid">
      <div class="match-column">
        <div 
          v-for="(item, index) in question.leftItems" 
          :key="'l-' + index"
          class="match-card"
          :class="{ 
            'is-active': selectedLeft === index,
            'is-matched': isLeftMatched(index) 
          }"
          :style="getMatchedStyle(index, 'left')"
          @click="selectLeft(index)"
        >
          <div class="card-body">
            <span class="card-label">{{ getItemLabel(item) }}</span>
          </div>
          <div 
            class="status-box" 
            v-if="isLeftMatched(index)" 
            :style="getIconStyle(index, 'left')"
          >
            <div class="checkmark"></div>
          </div>
        </div>
      </div>

      <div class="match-column">
        <div 
          v-for="(item, index) in question.rightItems" 
          :key="'r-' + index"
          class="match-card"
          :class="{ 
            'is-active': selectedRight === index,
            'is-matched': isRightMatched(index)
          }"
          :style="getMatchedStyle(index, 'right')"
          @click="selectRight(index)"
        >
          <div class="card-body">
            <span class="card-label">{{ getItemLabel(item) }}</span>
          </div>
          <div 
            class="status-box" 
            v-if="isRightMatched(index)" 
            :style="getIconStyle(index, 'right')"
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
  methods: {
    getItemLabel(item) {
      if (typeof item === 'string') return item;
      return item.label || '';
    },
    selectLeft(index) {
      // 如果点的是已经选中的，则取消选中
      this.selectedLeft = (this.selectedLeft === index) ? null : index;
      this.checkMatch();
    },
    selectRight(index) {
      this.selectedRight = (this.selectedRight === index) ? null : index;
      this.checkMatch();
    },
    checkMatch() {
      if (this.selectedLeft !== null && this.selectedRight !== null) {
        // 1. 先移除包含当前选中项的任何旧匹配（保持一对一）
        this.completedMatches = this.completedMatches.filter(
          m => m.l !== this.selectedLeft && m.r !== this.selectedRight
        );
    
        // 2. 添加新匹配
        this.completedMatches.push({
          l: this.selectedLeft,
          r: this.selectedRight,
          // 核心修复：基于左侧索引取色，确保同一行的初始色调一致，且不受数组长度变化影响
          colorIndex: this.selectedLeft % this.colorPalette.length 
        });
    
        this.$emit('answer-change', this.completedMatches);
        this.selectedLeft = null;
        this.selectedRight = null;
      }
    },
    getMatchedStyle(index, side) {
      const match = this.completedMatches.find(m => side === 'left' ? m.l === index : m.r === index);
      if (match) {
        const color = this.colorPalette[match.colorIndex];
        return {
          backgroundColor: color.bg,
          borderColor: color.main,
          borderWidth: '2px',
          transform: 'scale(1.02)'
        };
      }
      return {};
    },
    getIconStyle(index, side) {
      const match = this.completedMatches.find(m => side === 'left' ? m.l === index : m.r === index);
      return match ? { backgroundColor: this.colorPalette[match.colorIndex].main } : {};
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
.match-ui-container {
  padding: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
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
  min-height: 60px; /* 确保卡片有足够高度 */
  background: #ffffff;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
}

.match-card:hover {
  border-color: #49b972;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 选中状态 */
.match-card.is-active {
  border: 1.5px dashed #666; /* 改为灰色虚线，表示“准备中” */
  background-color: #fafafa;
  transform: translateY(-2px);
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
  word-break: break-word; /* 允许长文本换行 */
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

/* 响应式适配 */
@media (max-width: 600px) {
  .match-grid { gap: 12px; }
  .match-card { padding: 12px 14px; min-height: 50px; }
  .card-label { font-size: 14px; }
  .status-box { width: 20px; height: 20px; }
}
</style>