<template>
  <div class="match-ui-container">
    <div v-if="data.question" class="question-title-container">
      <div class="tag-row">
        <span class="tag">代码填空题</span>
      </div>
      <div class="title-row">
        <span class="question-index">{{ data.index }}.</span>
        <span class="question-text" v-html="data.question.question_title"></span>
      </div>
    </div>

    <div class="code-editor-container">
      <div class="code-editor">
        <div v-for="(line, idx) in parsedLines" :key="idx" class="line-wrapper">
          <div v-if="line.isInput" class="input-block">
            <span class="input-label" v-html="line.prefix"></span>
            <input
              v-model="data.question.fields[line.fieldIndex].value"
              class="code-input"
              placeholder="????"
            />
          </div>

          <div v-else class="code-line">
            <span v-for="(token, tIdx) in line.tokens" :key="tIdx" :class="token.type">
              {{ token.text }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionCodeFill',
  props: {
    // 接收你提供的那种完整数据结构
    data: {
      type: Object,
      required: true,
      default: () => ({ index: 1, question: { title: '', code: '', fields: [] } })
    }
  },
  computed: {
    parsedLines() {
      if (!this.data.question || !this.data.question.code) return [];
      const lines = this.data.question.code.split('\n');
      let fieldCounter = 0;

      return lines.map(rawLine => {
        // 检测是否包含 ????
        if (rawLine.includes('????')) {
          const prefix = rawLine.replace('????', '').trim();
          const currentIdx = fieldCounter;
          fieldCounter++;
          return {
            isInput: true,
            prefix: prefix, // 例如 "IP1="
            fieldIndex: currentIdx
          };
        }
        // 普通代码行进行词法解析
        return {
          isInput: false,
          tokens: this.tokenize(rawLine)
        };
      });
    }
  },
  methods: {
    tokenize(text) {
      const tokens = [];
      const regex = /(;.*)|(\b[0-9A-Fa-f]+[Hh]\b)|(\b(mov|call|ret|inc|dec|add|int|end|push|pop|start)\b)|(\b(ax|bx|cx|dx|ds|es|ss|sp|ip)\b)|([a-zA-Z0-9_]+:)|(\s+)|(.)/gi;
      let match;
      while ((match = regex.exec(text)) !== null) {
        let type = 'hl-default';
        if (match[1]) type = 'hl-comment';
        else if (match[2]) type = 'hl-number';
        else if (match[3]) type = 'hl-keyword';
        else if (match[5]) type = 'hl-reg';
        else if (match[7]) type = 'hl-label';
        else if (match[8]) type = 'hl-space';
        tokens.push({ text: match[0], type });
      }
      return tokens;
    }
  }
}
</script>

<style scoped>
/* 保持你要求的 UI 风格 */
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
}

.title-row {
  display: flex;
  font-size: 17px;
  font-weight: 600;
  color: #333;
}

.code-editor-container {
  width: 100%;
  max-width: 800px;
}

.code-editor {
  background-color: #f8f9fa;
  border: 1.5px solid #e8e8e8;
  border-radius: 14px;
  padding: 24px;
  font-family: "Consolas", monospace;
  font-size: 14px;
  line-height: 1.6;
}

/* 高亮配色 */
.hl-keyword { color: #d73a4a; font-weight: bold; }
.hl-reg { color: #005cc5; }
.hl-number { color: #032f62; }
.hl-label { color: #6f42c1; }
.hl-comment { color: #6a737d; font-style: italic; }
.hl-default { color: #333; }

/* 输入框行样式 */
.input-block {
  display: inline-flex;
  align-items: center;
  background-color: #f0f7ff;
  border: 1px solid #cce4ff;
  border-radius: 8px;
  padding: 4px 12px;
  margin: 6px 0 6px 20px;
}

.input-label {
  color: #1677ff;
  font-weight: bold;
  margin-right: 8px;
}

.code-input {
  width: 80px;
  padding: 4px 8px;
  border: 1px solid #b8daff;
  border-radius: 4px;
  outline: none;
}
</style>