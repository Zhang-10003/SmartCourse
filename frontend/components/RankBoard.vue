<template>
  <div class="rank-board">
    <header class="board-header">
      <div class="main-title">
        <h1>排行榜</h1>
      </div>
      <p class="sub-title">{{ data.subtitle || '汇编语言 - 指令学习优秀名单' }}</p>
    </header>

    <div class="list-container">
      <div 
        v-for="(item, index) in data.list" 
        :key="index" 
        class="rank-row"
      >
        <div class="rank-num-box">
          <div :class="['rank-circle', getRankClass(index + 1)]">
            {{ index + 1 }}
          </div>
        </div>

        <div class="name-box">
          <span class="user-name">{{ item.name }}</span>
        </div>

        <div class="value-box">
          <div class="score-pill">{{ item.score }}分</div>
          <div class="medal-slot">
            <span v-if="index === 0" class="medal medal-gold">🥇</span>
            <span v-else-if="index === 1" class="medal medal-silver">🥈</span>
            <span v-else-if="index === 2" class="medal medal-bronze">🥉</span>
          </div>
        </div>
      </div>
    </div>

    <footer class="board-footer">
      <p class="motto">
        <span class="motto-icon">✨</span>
        每一份努力都值得被看见！继续加油！
      </p>
    </footer>
  </div>
</template>

<script setup>
/**
 * JSON 接口说明：
 * data: {
 * subtitle: String, // 副标题
 * list: [
 * { name: String, score: Number } // 数据项
 * ]
 * }
 */
const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({
      subtitle: '',
      list: []
    })
  }
});

// 获取排名背景类名
const getRankClass = (rank) => {
  if (rank === 1) return 'top-1';
  if (rank === 2) return 'top-2';
  if (rank === 3) return 'top-3';
  return 'top-other';
};
</script>

<style scoped>
.rank-board {
  max-width: 450px;
  margin: 0 auto;
  background-color: #ffffff;
  min-height: 100vh;
  font-family: -apple-system, system-ui, sans-serif;
  color: #333;
}

/* 头部样式 */
.board-header {
  padding: 32px 20px 16px;
  text-align: center;
}

.main-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.main-title h1 {
  font-size: 22px;
  color: #1a73e8;
  font-weight: 800;
  margin: 0;
  letter-spacing: 1px;
}

.emoji { font-size: 24px; }

.sub-title {
  font-size: 14px;
  color: #888;
  margin: 0;
}

/* 列表样式 */
.list-container {
  padding: 0 20px;
}

.rank-row {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f2f2f2;
}

.rank-num-box {
  width: 44px;
}

.rank-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 15px;
}

/* 排名色值 */
.top-1 { background-color: #ffde00; color: #fff; }
.top-2 { background-color: #ccd1d1; color: #fff; }
.top-3 { background-color: #e59866; color: #fff; }
.top-other { background-color: #f0f3f4; color: #99a3a4; }

.name-box {
  flex: 1;
  padding-left: 12px;
}

.user-name {
  font-size: 17px;
  font-weight: 600;
  color: #2c3e50;
}

/* 分数区域 */
.value-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.score-pill {
  background-color: #eafaf1;
  color: #27ae60;
  padding: 4px 14px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 15px;
  border: 1px solid #d5f5e3;
}

.medal-slot {
  width: 24px;
  text-align: center;
  font-size: 20px;
}

/* 底部 */
.board-footer {
  padding: 40px 20px;
  text-align: center;
}

.motto {
  font-size: 12px;
  color: #bdc3c7;
  margin: 0;
}

.motto-icon { font-size: 14px; margin-right: 4px; }
</style>