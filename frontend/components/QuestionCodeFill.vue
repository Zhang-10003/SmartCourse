<template>
  <div class="q-container">
    <div class="q-title" v-if="question.title" v-html="question.title"></div>

    <div class="code-editor">
      <div v-for="(line, idx) in parsedLines" :key="idx" class="line-wrapper">
        <div v-if="line.type === 'input'" class="input-block">
          <span class="input-label">{{ line.label }} = </span>
          <input
            v-model="userValues[line.index]"
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
</template>

<script>
export default {
  name: 'QuestionCodeFill',
  props: {
    question: { type: Object, required: true },
    value: { type: Array, default: () => [] }
  },
  computed: {
    userValues: {
      get() { return this.value },
      set(val) { this.$emit('input', val) }
    },
    parsedLines() {
      if (!this.question.code) return [];
      const lines = this.question.code.split('\n');
      let fieldIdx = 0;

      return lines.map(rawLine => {
        const trimmed = rawLine.trim();

        // 1. 判断是否为输入框行
        if (trimmed.match(/^(IP|SP|IP\d+|SP\d+)=\?\?\?\?/)) {
          const res = {
            type: 'input',
            label: this.question.fields[fieldIdx]?.label || trimmed.split('=')[0],
            index: fieldIdx
          };
          fieldIdx++;
          return res;
        }

        // 2. 词法解析代码行
        return {
          type: 'code',
          tokens: this.tokenize(rawLine)
        };
      });
    }
  },
  methods: {
    tokenize(text) {
      const tokens = [];
      // 匹配：注释、十六进制数(0100H)、寄存器、指令、标号、符号
      const regex = /(;.*)|(\b[0-9A-Fa-f]+[Hh]\b)|(\b(mov|call|ret|inc|dec|add|int|end|start)\b)|(\b(ax|bx|cx|dx|ah|al|sp|ip)\b)|([a-zA-Z0-9_]+:)|(\s+)|(.)/gi;
      
      let match;
      while ((match = regex.exec(text)) !== null) {
        let type = 'hl-default';
        if (match[1]) type = 'hl-comment';      // 注释
        else if (match[2]) type = 'hl-number';  // 0100H
        else if (match[3]) type = 'hl-keyword'; // mov/call
        else if (match[5]) type = 'hl-reg';     // ax/sp
        else if (match[7]) type = 'hl-label';   // start:
        else if (match[8]) type = 'hl-space';   // 空格
        
        tokens.push({ text: match[0], type });
      }
      return tokens;
    }
  }
}
</script>

<style scoped>
/* 容器 */
.q-container { padding: 20px; background: #fff; }
.q-title { margin-bottom: 15px; font-size: 16px; line-height: 1.6; color: #333; }

/* 代码编辑器风格 */
.code-editor {
  background-color: #f8f9fa;
  border: 1px solid #e1e4e8;
  border-radius: 6px;
  padding: 16px;
  font-family: "Consolas", "Monaco", monospace;
  font-size: 14px;
  line-height: 1.5;
}

.line-wrapper { min-height: 24px; white-space: pre; }

/* --- 强制高亮颜色 --- */
.hl-keyword { color: #d73a4a; font-weight: bold; } /* 指令：红色 */
.hl-reg { color: #005cc5; }                        /* 寄存器：蓝色 */
.hl-number { color: #032f62; }                     /* 数值：深蓝色 */
.hl-label { color: #6f42c1; }                      /* 标号：紫色 */
.hl-comment { color: #6a737d; font-style: italic; } /* 注释：灰色 */
.hl-default { color: #24292e; }                    /* 符号(逗号等)：黑色 */

/* --- 输入框行样式 (匹配截图) --- */
.input-block {
  display: inline-flex;
  align-items: center;
  background-color: #ebf5ff;
  border: 1px solid #cce5ff;
  border-radius: 8px;
  padding: 6px 15px;
  margin: 10px 0 10px 20px;
}
.input-label {
  color: #0066cc;
  font-weight: bold;
  margin-right: 12px;
  font-family: sans-serif;
}
.code-input {
  width: 90px;
  padding: 4px 8px;
  border: 1px solid #b8daff;
  border-radius: 4px;
  outline: none;
  text-align: center;
}
</style>