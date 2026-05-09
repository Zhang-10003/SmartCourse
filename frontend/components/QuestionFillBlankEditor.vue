<template>
  <div class="match-ui-container">
    <!-- 顶部标签和分数设置 -->
    <div class="tag-score-row">
      <span class="tag edit-tag">填空题编辑</span>
      <div class="score-input-wrapper">
        <span class="score-label">题目分数</span>
        <button class="score-btn" @click="decreaseScore">-</button>
        <input 
          type="number" 
          v-model.number="localScore" 
          class="score-input" 
          min="1" 
          max="100"
        />
        <button class="score-btn" @click="increaseScore">+</button>
        <span class="score-unit">分</span>
      </div>
    </div>

    <!-- 题干编辑区：参考代码二样式 -->
    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          v-model="localQuestion.title" 
          class="q-textarea" 
          placeholder="请输入题目描述（例如：请根据语境在空格处填入正确的词汇）"
          spellcheck="false"
        ></textarea>
      </div>
    </div>

    <div class="editor-main-layout">
      <!-- 左侧：题干源码编辑 -->
      <div class="code-source-section">
        <div class="section-label">题干内容编辑 (???? 表示填空位)</div>
        <textarea
          v-model="localQuestion.content"
          class="raw-content-editor"
          placeholder="示例：锄禾日当午，????，谁知盘中餐，粒粒皆辛苦。"
          spellcheck="false"
          @input="syncBlanks"
        ></textarea>
      </div>

      <!-- 右侧：填空位预览与答案配置 -->
      <div class="preview-section">
        <div class="section-label">实时预览与标准答案</div>
        <div class="blanks-preview-box">
          <!-- 题干预览流 -->
          <div class="content-preview">
             <span v-for="(part, i) in parsedData.parts" :key="'part-' + i">
              {{ part }}
              <span v-if="i < parsedData.blanksCount" class="inline-placeholder">
                ( {{ i + 1 }} )
              </span>
            </span>
          </div>

          <div class="options-divider"></div>

          <!-- 答案输入列表 -->
          <div class="answers-list">
            <div 
              v-for="(_, idx) in parsedData.blanksCount" 
              :key="'blank-' + idx"
              class="answer-item-card"
            >
              <span class="answer-label">空格 {{ idx + 1 }}</span>
              <input
                type="text"
                class="answer-input-field"
                placeholder="设置标准答案"
                v-model="localQuestion.correctAnswers[idx]"
              />
            </div>
            <div v-if="parsedData.blanksCount === 0" class="empty-tip">
              请在左侧输入 ???? 创建填空位
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionFillBlankEditor',
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: {
      type: Object,
      default: () => ({
        title: '',
        content: '',
        correctAnswers: [],
        analysis: '',
        score: 10
      })
    }
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    },
    localScore: {
      get() { return this.localQuestion.score || 10 },
      set(val) { 
        this.localQuestion.score = Math.max(1, Math.min(100, val || 1));
      }
    },
    parsedData() {
      const content = this.localQuestion.content || '';
      const parts = content.split('????');
      return {
        parts,
        blanksCount: parts.length - 1
      };
    }
  },
  methods: {
    increaseScore() {
      if (this.localScore < 100) {
        this.localScore++;
      }
    },
    decreaseScore() {
      if (this.localScore > 1) {
        this.localScore--;
      }
    },
    syncBlanks() {
      const count = this.parsedData.blanksCount;
      const answers = this.localQuestion.correctAnswers;
      if (answers.length < count) {
        for (let i = answers.length; i < count; i++) {
          answers.push('');
        }
      } else if (answers.length > count) {
        this.localQuestion.correctAnswers = answers.slice(0, count);
      }
    }
  },
  mounted() {
    this.syncBlanks();
  }
}
</script>

<style scoped>
.match-ui-container {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  background: #fff;
  border-radius: 16px;
  box-sizing: border-box;
}

/* 标签样式 */
.tag-score-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}
.edit-tag { background: #e6f4ff; color: #1677ff; }
.score-input-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
}
.score-label {
  font-size: 13px;
  color: #8c8c8c;
}
.score-btn {
  width: 24px;
  height: 24px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.score-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
  background: #f0f7ff;
}
.score-input {
  width: 50px;
  height: 24px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #333;
  outline: none;
  transition: all 0.2s;
}
.score-input:focus {
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}
.score-unit {
  font-size: 12px;
  color: #8c8c8c;
  margin-left: 2px;
}

/* 题干样式：参考代码二 */
.question-header { display: flex; align-items: flex-start; margin: 16px 0; }
.q-index { font-size: 20px; font-weight: bold; color: #fa8c16; margin-right: 8px; line-height: 28px; }
.q-input-wrapper { flex: 1; }
.q-textarea {
  width: 100%; border: none; outline: none; font-size: 18px; font-weight: bold;
  background: transparent; resize: none; padding: 0; margin: 0; 
  line-height: 28px; 
  height: 56px; /* 默认2行高度 (28px * 2) */
  min-height: 56px;
  color: #333;
}

/* 布局：双栏对齐 */
.editor-main-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 10px;
  align-items: stretch;
}

.section-label {
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 8px;
  display: block;
}

/* 左侧编辑器 */
.raw-content-editor {
  width: 100%;
  min-height: 350px;
  background: #ffffff;
  color: #333;
  font-size: 15px;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #d9d9d9;
  line-height: 1.8;
  resize: vertical;
  outline: none;
  box-sizing: border-box;
}

/* 右侧预览区 */
.blanks-preview-box {
  background: #f8f9fa;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.content-preview {
  font-size: 15px;
  line-height: 1.8;
  color: #444;
  margin-bottom: 16px;
  word-break: break-all;
}

.inline-placeholder {
  color: #1677ff;
  font-weight: bold;
  margin: 0 4px;
}

.options-divider {
  height: 1px;
  background: #e8e8e8;
  margin-bottom: 16px;
}

/* 答案卡片样式 */
.answers-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.answer-item-card {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #eee;
  padding: 8px 12px;
  border-radius: 8px;
}

.answer-label {
  font-size: 13px;
  color: #8c8c8c;
  width: 80px;
  flex-shrink: 0;
}

.answer-input-field {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1677ff;
  font-weight: 500;
}

.empty-tip {
  text-align: center;
  color: #bfbfbf;
  font-size: 13px;
  padding: 20px 0;
}

/* 解析部分 */
.feedback-section { margin-top: 24px; }
.section-divider { height: 1px; background: #eee; margin-bottom: 20px; }
.analysis-tag { background: #f6ffed; color: #52c41a; }
.feedback-card {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 14px;
}
.analysis-textarea {
  width: 100%; min-height: 80px; border: none; outline: none;
  background: transparent; font-size: 14px; color: #595959; resize: vertical;
}
</style>