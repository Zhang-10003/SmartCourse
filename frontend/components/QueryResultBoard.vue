<template>
  <div class="result-container">
    <div class="result-card">
      <div class="header-section">
        <h2 class="main-title">查询结果</h2>
        <p class="sub-title">仅本人可见</p>
      </div>

      <div class="score-circle-wrapper">
        <div class="score-circle">
          <div class="score-number">{{ resultData.totalScore }}</div>
          <div class="score-label">总分</div>
        </div>
      </div>

      <div class="info-list">
        <div class="info-item">
          <span class="label">姓名</span>
          <span class="value bold">{{ resultData.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">班级排名</span>
          <span class="value bold">{{ resultData.rank }}</span>
        </div>
        <div class="info-item">
          <span class="label">击败人数占比</span>
          <span class="value bold">{{ resultData.percentage }}%</span>
        </div>
      </div>

      <div class="action-section">
        <button class="back-btn" @click="$emit('back')">返回查询</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QueryResultBoard',
  props: {
    resultData: {
      type: Object,
      default: () => ({
        totalScore: 8,
        name: '黄泓铭',
        rank: 4,
        percentage: 93.0
      })
    }
  },
  emits: ['back']
}
</script>

<style scoped>
.result-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  background-color: #f8f9fb; /* 调浅背景色以突出卡片 */
  min-height: 100vh;
  box-sizing: border-box;
}

.result-card {
  width: 100%;
  max-width: 340px; /* 固定最大宽度以还原窄长比例 */
  background: white;
  border-radius: 24px; /* 增加圆角弧度 */
  padding: 40px 28px;
  /* 调整阴影使其更轻盈且范围更大 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
}

.header-section {
  text-align: center;
  margin-bottom: 32px;
}

.main-title {
  color: #1677ff;
  font-size: 26px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}

.sub-title {
  color: #999;
  font-size: 15px;
  margin: 10px 0 0;
}

/* 分数圆环还原 */
.score-circle-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.score-circle {
  width: 130px;
  height: 130px;
  border: 5px solid #49b972; /* 绿色线条宽度微调 */
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #49b972;
  line-height: 1;
}

.score-label {
  font-size: 15px;
  color: #999;
  margin-top: 6px;
}

/* 列表样式优化 */
.info-list {
  margin-bottom: 40px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 0;
  border-bottom: 1px solid #f2f2f2;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-size: 17px;
}

.value {
  color: #333;
  font-size: 18px;
}

.value.bold {
  font-weight: 700;
}

/* 返回按钮：还原为截图中的带边框矩形样式 */
.action-section {
  text-align: center;
}

.back-btn {
  background: #fff;
  border: 1px solid #e0e0e0; /* 还原灰色细边框 */
  color: #888;
  padding: 10px 32px;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  width: auto;
  min-width: 140px;
}

.back-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
  background-color: #f0f7ff;
}
</style>