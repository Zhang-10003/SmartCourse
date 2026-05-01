<template>
  <div class="match-ui-container">
    <div class="tag-row">
      <span class="tag">简答题</span>
    </div>

    <!-- 题干部分：严格对齐单选题 1 行起步 -->
    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          ref="titleRef"
          v-model="localQuestion.title" 
          class="q-textarea auto-height" 
          placeholder="请输入简答题题干内容..."
          :rows="1"
          @input="handleInput"
        ></textarea>
      </div>
    </div>

    <!-- 答案解析/标准答案编辑区 -->
    <div class="feedback-section">
      <div class="section-divider"></div>
      
      <div class="feedback-header">
        <div class="left-labels">
          <span class="tag answer-tag">参考答案</span>
        </div>
      </div>

      <div class="feedback-card">
        <textarea
          ref="answerRef"
          v-model="localQuestion.standardAnswer"
          class="analysis-textarea auto-height"
          placeholder="请输入标准参考答案..."
          :rows="1"
          @input="handleInput"
        ></textarea>
        <div class="card-footer">
          <span class="char-count">{{ localQuestion.standardAnswer?.length || 0 }} 字</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionShortAnswerEditor",
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: { 
      type: Object, 
      default: () => ({ title: '', standardAnswer: '', analysis: '' })
    }
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    }
  },
  mounted() {
    // 页面加载完成后，根据内容初始撑开高度
    this.$nextTick(() => {
      this.initAllHeights();
    });
  },
  methods: {
    // 初始化所有输入框高度
    initAllHeights() {
      const refs = [this.$refs.titleRef, this.$refs.answerRef, this.$refs.analysisRef];
      refs.forEach(el => {
        if (el) this.updateElementHeight(el);
      });
    },
    // 处理输入事件
    handleInput(e) {
      this.updateElementHeight(e.target);
    },
    // 核心高度计算函数（带空值保护）
    updateElementHeight(el) {
      if (!el || !el.style) return;
      
      el.style.height = 'auto'; // 先缩回最小
      const newHeight = el.scrollHeight;
      if (newHeight > 0) {
        el.style.height = newHeight + 'px'; // 撑开
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
  box-sizing: border-box;
}

.tag-row { margin-bottom: 4px; }
.tag {
  background: #e6f4ff;
  color: #1677ff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

/* 题干样式：严格对齐单选题截图 */
.question-header {
  display: flex;
  align-items: flex-start;
  margin-top: 8px;
}
.q-index {
  font-size: 20px;
  font-weight: bold;
  line-height: 28px;
  color: #1677ff;
  margin-right: 8px;
}
.q-input-wrapper { flex: 1; }

.auto-height {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  resize: none;
  display: block;
  padding: 0;
  margin: 0;
  overflow: hidden; /* 必须隐藏，否则撑开瞬间会有滚动条闪烁 */
}

/* 题干：文字加粗，行高 28px */
.q-textarea {
  font-size: 18px;
  font-weight: bold;
  color: #262626;
  line-height: 28px;
  min-height: 28px; /* 初始 1 行高度 */
}

/* 卡片容器 */
.section-divider {
  height: 1px;
  background: linear-gradient(to right, #eee, #fff);
  margin: 24px 0 20px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.answer-tag { background: #f6ffed; color: #52c41a; border: 1px solid #d9f7be; }
.analysis-tag { background: #fff7e6; color: #fa8c16; border: 1px solid #ffd591; }

.ai-gen-btn {
  font-size: 13px;
  color: #722ed1;
  background: #f9f0ff;
  padding: 4px 12px;
  border-radius: 6px;
  border: 1px solid #efdbff;
  cursor: pointer;
}

.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
}

.feedback-card:focus-within {
  background: #fff;
  border-color: #1677ff;
}

.analysis-textarea {
  font-size: 14px;
  line-height: 1.6;
  color: #595959;
  min-height: 22px; /* 1.6 * 14px ≈ 22px，即 1 行高度 */
}

.card-footer { display: flex; justify-content: flex-end; margin-top: 8px; }
.char-count { font-size: 12px; color: #bfbfbf; }
</style>