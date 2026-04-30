<template>
  <div class="match-ui-container">
    <div class="tag-row">
      <span class="tag code-tag">代码填空题编辑</span>
    </div>

    <!-- 题干编辑 -->
    <div class="question-header">
      <span class="q-index">{{ index.toString().padStart(2, '0') }}.</span>
      <div class="q-input-wrapper">
        <textarea 
          v-model="localQuestion.title" 
          class="q-textarea" 
          placeholder="请输入题目描述（例如：请补全汇编指令使程序正常运行）"
          spellcheck="false"
        ></textarea>
      </div>
    </div>

    <div class="editor-main-layout">
      <!-- 左侧：源码编辑器 -->
      <div class="code-source-section">
        <div class="section-label">源码编辑 (输入 ???? 表示填空位)</div>
        <textarea
          v-model="localQuestion.code"
          class="raw-code-editor"
          placeholder="MOV AX, 4C00H
????
INT 21H"
          spellcheck="false"
          @input="syncFields"
        ></textarea>
      </div>

      <!-- 右侧：实时预览与标准答案 -->
      <div class="preview-section">
        <div class="section-label">实时预览与标准答案</div>
        <div class="code-preview-box">
          <div v-for="(line, idx) in parsedLines" :key="idx" class="line-wrapper">
            <!-- 只要这一行包含填空，就渲染成红色的 input-block -->
            <div v-if="line.hasInput" class="input-block">
              <template v-for="(part, pIdx) in line.segments" :key="pIdx">
                <!-- 填空位 -->
                <input
                  v-if="part.isInput"
                  v-model="localQuestion.fields[part.fieldIndex].answer"
                  class="answer-input"
                  placeholder=""
                  spellcheck="false"
                />
                <!-- 填空位之间的代码文本 -->
                <span v-else class="code-line">
                  <span v-for="(token, tIdx) in part.tokens" :key="tIdx" :class="token.type">
                    {{ token.text }}
                  </span>
                </span>
              </template>
            </div>

            <!-- 纯代码行 -->
            <div v-else class="code-line-standalone">
              <span v-for="(token, tIdx) in line.tokens" :key="tIdx" :class="token.type">
                {{ token.text }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 解析部分 -->
    <div class="feedback-section">
      <div class="section-divider"></div>
      <div class="feedback-header">
        <span class="tag answer-tag">题目解析</span>
      </div>
      <div class="feedback-card">
        <textarea 
          v-model="localQuestion.analysis"
          class="analysis-textarea"
          placeholder="请输入该代码段的逻辑说明..."
          spellcheck="false"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionCodeFillEditor",
  props: {
    index: { type: [Number, String], default: 1 },
    modelValue: {
      type: Object,
      default: () => ({
        title: '',
        code: '',
        fields: [],
        analysis: ''
      })
    }
  },
  computed: {
    localQuestion: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) }
    },
    parsedLines() {
      if (!this.localQuestion.code) return [];
      const lines = this.localQuestion.code.split('\n');
      let globalFieldIndex = 0;

      return lines.map(rawLine => {
        if (rawLine.includes('????')) {
          const segments = [];
          const parts = rawLine.split(/(\?\?\?\?)/g);
          
          parts.forEach(part => {
            if (part === '????') {
              segments.push({ isInput: true, fieldIndex: globalFieldIndex++ });
            } else {
              segments.push({ isInput: false, tokens: this.tokenize(part) });
            }
          });
          return { hasInput: true, segments };
        } else {
          return { hasInput: false, tokens: this.tokenize(rawLine) };
        }
      });
    }
  },
  methods: {
    syncFields() {
      const fillCount = (this.localQuestion.code.match(/\?\?\?\?/g) || []).length;
      const fields = this.localQuestion.fields;
      if (fields.length < fillCount) {
        for (let i = fields.length; i < fillCount; i++) {
          fields.push({ value: '', answer: '' });
        }
      } else if (fields.length > fillCount) {
        this.localQuestion.fields = fields.slice(0, fillCount);
      }
    },
    tokenize(text) {
      if (!text) return [];
      const tokens = [];
      const regex = /(\b(mov|call|ret|inc|dec|add|int|end|push|pop|start|sub|mul|div|jmp|jz|jnz)\b)|(\s+)|(.)/gi;
      let match;
      while ((match = regex.exec(text)) !== null) {
        let type = 'hl-default';
        if (match[1]) type = 'hl-keyword';
        tokens.push({ text: match[0], type });
      }
      return tokens;
    }
  },
  mounted() {
    this.syncFields();
  }
};
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

.tag {
  background: #e6f4ff;
  color: #1677ff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}
.code-tag { background: #fff7e6; color: #fa8c16; }

.question-header { display: flex; align-items: flex-start; margin: 16px 0; }
.q-index { font-size: 20px; font-weight: bold; color: #fa8c16; margin-right: 8px; line-height: 28px; }
.q-input-wrapper { flex: 1; }
.q-textarea {
  width: 100%; border: none; outline: none; font-size: 18px; font-weight: bold;
  background: transparent; resize: none; padding: 0; margin: 0; line-height: 28px; height: 56px; min-height: 56px;
}

/* 关键修改：严格平分宽度并强制对齐 */
.editor-main-layout {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 确保两个框框宽度一致 */
  gap: 20px;
  margin-top: 10px;
  align-items: stretch; 
}

.code-source-section, .preview-section {
  display: flex;
  flex-direction: column;
  width: 100%; /* 确保填满 grid 的列 */
}

.section-label {
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 8px;
  display: block;
}

.raw-code-editor {
  flex: 1; 
  width: 100%;
  min-height: 400px; 
  background: #ffffff;
  color: #333;
  font-family: 'Consolas', monospace;
  font-size: 14px;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #d9d9d9;
  line-height: 1.8; 
  resize: vertical;
  outline: none;
  box-sizing: border-box;
}

.code-preview-box {
  flex: 1; 
  width: 100%;
  min-height: 400px;
  background: #f8f9fa;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  padding: 16px;
  overflow-y: auto;
  font-family: 'Consolas', monospace;
  font-size: 14px;
  box-sizing: border-box;
}

.line-wrapper {
  margin-bottom: 8px;
}

.input-block {
  display: flex;
  align-items: center;
  background: #fff1f0;
  border: 1px solid #ffa39e;
  padding: 4px 10px;
  border-radius: 6px;
  width: fit-content; 
  min-width: 80px;
}

/* 关键修改：输入框宽度改为原来的一半 (90px -> 45px) */
.answer-input {
  width: 45px;
  border: 1px solid #ffccc7;
  border-radius: 4px;
  padding: 2px 4px; /* 略微减小左右内边距以适配窄宽度 */
  margin: 0 4px; 
  outline: none;
  font-family: 'Consolas', monospace;
  font-size: 13px;
  background: #fff;
  text-align: center;
}

.code-line {
  white-space: pre;
  line-height: 1.6;
}

.code-line-standalone {
  white-space: pre;
  line-height: 1.6;
  padding-left: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
}

.hl-keyword { color: #d73a4a; font-weight: bold; }
.hl-default { color: #333; }

.feedback-section { margin-top: 24px; }
.section-divider { height: 1px; background: #eee; margin-bottom: 20px; }
.answer-tag { background: #f6ffed; color: #52c41a; }
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