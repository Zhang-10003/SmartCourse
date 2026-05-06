<template>
  <div class="match-ui-container">
    <div class="tag-row">
      <span class="tag matching-tag">匹配题编辑</span>
    </div>

    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          v-model="localQuestion.title" 
          class="q-textarea" 
          placeholder="请输入匹配题的整体题目描述或指导语..."
          spellcheck="false"
        ></textarea>
      </div>
    </div>

    <div class="editor-main-layout">
      <div class="pairs-edit-container">
        <div class="pairs-header-row">
          <div class="header-label column-left">左侧条目 (Item A)</div>
          <div class="header-label column-right">右侧条目 (Item B - 默认正确答案)</div>
          <div class="header-label column-action"></div>
        </div>

        <div 
          v-for="(pair, idx) in localQuestion.pairs" 
          :key="idx"
          class="pair-edit-card"
        >
          <div class="pair-index-badge" :style="getBadgeColor(idx)">
            {{ idx + 1 }}
          </div>

          <div class="input-cell">
            <input 
              v-model="pair.left"
              type="text"
              class="pair-text-input"
              placeholder="输入左侧条目内容"
            />
          </div>

          <div class="link-indicator">
            <span class="link-arrow">⇌</span>
          </div>

          <div class="input-cell">
            <input 
              v-model="pair.right"
              type="text"
              class="pair-text-input"
              placeholder="输入正确配对的右侧内容"
            />
          </div>

          <div class="action-cell">
            <div 
              v-if="localQuestion.pairs.length > 2"
              class="delete-btn" 
              @click="removePair(idx)"
              title="删除此配对"
            >×</div>
          </div>
        </div>

        <div class="add-btn-card" @click="addPair">
          <span>+ 添加全新配对条目 (自动建立映射)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionMatchingEditor",
  props: {
    index: { 
      type: [Number, String], 
      default: 1 
    },
    modelValue: {
      type: Object,
      default: () => ({
        title: '',
        pairs: [
          { left: '', right: '' },
          { left: '', right: '' },
          { left: '', right: '' }
        ],
        analysis: ''
      })
    }
  },
  data() {
    return {
      // 匹配答题端的经典色彩矩阵（蓝、绿、橙、粉、紫）
      colorPalette: [
        { bg: '#f0f7ff', main: '#3b82f6' }, 
        { bg: '#f2faf5', main: '#49b972' }, 
        { bg: '#fff7ed', main: '#f97316' }, 
        { bg: '#fdf2f8', main: '#ec4899' }, 
        { bg: '#f5f3ff', main: '#8b5cf6' }  
      ]
    };
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue; },
      set(val) { this.$emit('update:modelValue', val); }
    }
  },
  methods: {
    // 依据行索引循环轮显色彩微章
    getBadgeColor(idx) {
      const color = this.colorPalette[idx % this.colorPalette.length];
      return {
        backgroundColor: color.bg,
        color: color.main,
        borderColor: color.main
      };
    },
    // 添加配对项
    addPair() {
      this.localQuestion.pairs.push({ left: '', right: '' });
    },
    // 删除配对项（执行视觉优先策略，瞬时锁死状态，剔除动画延迟）
    removePair(idx) {
      this.localQuestion.pairs.splice(idx, 1);
    }
  }
};
</script>

<style scoped>
/* 容器及通用题干基础 */
.match-ui-container {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  background: #fff;
  border-radius: 16px;
  box-sizing: border-box;
}

.tag-row {
  margin-bottom: 4px;
}
.tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}
.matching-tag {
  background: #e6fffb;
  color: #13c2c2; /* 标志性 SCI 学术风青色 */
}

.question-header {
  display: flex;
  align-items: flex-start;
  margin: 16px 0;
}
.q-index {
  font-size: 20px;
  font-weight: bold;
  line-height: 28px;
  margin-right: 8px;
  color: #13c2c2;
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

/* 主容器排版与表头 */
.editor-main-layout {
  background: #fdfdfd;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
}

.pairs-edit-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pairs-header-row {
  display: flex;
  align-items: center;
  padding: 0 14px 8px;
  border-bottom: 1px dashed #e8e8e8;
}

.header-label {
  font-size: 13px;
  color: #8c8c8c;
  font-weight: 500;
}
.column-left { flex: 1; padding-left: 36px; }
.column-right { flex: 1; padding-left: 20px; }
.column-action { width: 30px; }

/* 每一行配对卡片流 */
.pair-edit-card {
  display: flex;
  align-items: center;
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 10px;
  padding: 10px 14px;
  box-sizing: border-box;
}

.pair-edit-card:hover {
  border-color: #d9d9d9;
  background: #f5f5f5;
}

/* 映射色彩微章 */
.pair-index-badge {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
}

/* ⚙️ 输入框的父级单元格：提供充足的最小高度空间，防止挤压 */
.input-cell {
  flex: 1;
  display: flex;
  align-items: center;
  min-height: 36px;
}

/* ⚙️ 核心修复：单行输入框样式（通过放宽 line-height 与弹性 padding 彻底解决变音字符顶部被削问题） */
.pair-text-input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  color: #434343;
  box-sizing: border-box;
  display: block;
  height: auto;

  /* 使用规范中的核心无衬线字体栈，保证中西文混排时的字宽与字高饱满 */
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
  
  /* 1. 刚性放宽文字垂直轨道高度（从隐式小值拉大到 1.6），为 é, à 等顶部的拼音符号留出刚性的像素通道，拒绝碰顶削头 */
  line-height: 1.6; 
  
  /* 2. 用弹性 padding 微调将卡片内壁优雅撑开，放弃死卡高度的做法，使得高字身字符能完美舒展 */
  padding: 4px 8px; 
}

.pair-text-input:focus {
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 0 0 2px rgba(19, 194, 194, 0.1);
}

/* 映射方向指示器 */
.link-indicator {
  padding: 0 16px;
  color: #bfbfbf;
  font-size: 16px;
  user-select: none;
  font-weight: bold;
}

/* 极速移除按钮 */
.action-cell {
  width: 30px;
  display: flex;
  justify-content: flex-end;
}
.delete-btn {
  color: #bfbfbf;
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
  user-select: none;
  line-height: 1;
}
.delete-btn:hover {
  color: #ff4d4f;
}

/* Bento 风格虚线添加卡片 */
.add-btn-card {
  border: 1px dashed #d9d9d9;
  border-radius: 10px;
  padding: 14px;
  text-align: center;
  color: #595959;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.add-btn-card:hover {
  border-color: #13c2c2;
  color: #13c2c2;
  background: #e6fffb;
}

/* 底部题目解析区域 */
.feedback-section {
  margin-top: 24px;
}
.section-divider {
  height: 1px;
  background: linear-gradient(to right, #eee 0%, #fff 100%);
  margin-bottom: 20px;
}
.feedback-header {
  margin-bottom: 12px;
}
.answer-tag {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #d9f7be;
}
.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px 18px;
}
.analysis-textarea {
  width: 100%;
  min-height: 80px;
  border: none;
  outline: none;
  background: transparent;
  resize: vertical;
  font-size: 14px;
  color: #434343;
  line-height: 1.6;
}
</style>