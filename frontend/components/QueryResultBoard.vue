<template>
  <view v-if="resultData" class="result-wrapper">
    <view class="result-card">
      <view class="header-section">
        <text class="main-title">查询结果</text>
        <text class="sub-title">仅本人可见</text>
      </view>

      <view class="score-circle-wrapper">
        <view class="score-circle">
          <text class="score-number">{{ resultData.totalScore }}</text>
          <text class="score-label">总分</text>
        </view>
      </view>

      <view class="info-list">
        <view class="info-item">
          <text class="label">姓名</text>
          <text class="value bold">{{ resultData.name }}</text>
        </view>
        <view class="info-item">
          <text class="label">班级排名</text>
          <text class="value bold">{{ resultData.rank }}</text>
        </view>
        <view class="info-item">
          <text class="label">击败人数占比</text>
          <text class="value bold">{{ resultData.percentage }}%</text>
        </view>
      </view>
      
      <view class="congrats-box">
        <text class="congrats-text">🎉 太棒了！你的表现非常优异，荣登排行榜前列！继续保持这份热情！</text>
      </view>

      <view class="action-section">
        <text class="back-link" @tap="$emit('back')">返回查询</text>
      </view>
    </view>
  </view>
</template>

<script setup>
// 使用 defineProps 明确声明接收的数据
const props = defineProps({
  resultData: {
    type: Object,
    required: true,
    default: () => ({
      totalScore: 0,
      name: '',
      rank: 0,
      percentage: 0
    })
  }
});

defineEmits(['back']);
</script>

<style lang="scss" scoped>
.result-wrapper {
  width: 100%;
  /* 如果背景需要灰色，可以在这里设置，或者在页面设置 */
  background-color: #f8f9fb; 
}

.result-card {
  width: 100%; /* 占满屏幕 */
  background: #ffffff;
  border-radius: 0 0 32rpx 32rpx; /* 仅底部圆角，更贴合顶部导航 */
  padding: 60rpx 40rpx;
  box-sizing: border-box;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.02);
}

.congrats-box {
  background-color: #e6f7ff;
  border: 1rpx solid #bae7ff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-top: 40rpx;
  .congrats-text {
    font-size: 26rpx;
    color: #1890ff;
    line-height: 1.6;
  }
}

.header-section {
  text-align: center;
  margin-bottom: 40rpx;
  .main-title {
    color: #1677ff;
    font-size: 52rpx;
    font-weight: bold;
    display: block;
  }
  .sub-title {
    color: #999;
    font-size: 28rpx;
    margin-top: 10rpx;
  }
}

.score-circle-wrapper {
  display: flex;
  justify-content: center;
  margin: 40rpx 0;
}

.score-circle {
  width: 260rpx;
  height: 260rpx;
  border: 10rpx solid #49b972;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .score-number {
    font-size: 90rpx;
    font-weight: bold;
    color: #49b972;
  }
  .score-label {
    font-size: 28rpx;
    color: #666;
  }
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 36rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
  &:last-child { border-bottom: none; }
  .label { color: #666; font-size: 32rpx; }
  .value { color: #333; font-size: 34rpx; &.bold { font-weight: bold; } }
}

.action-section {
  margin-top: 60rpx;
  text-align: center;
  padding-bottom: 20rpx;
  .back-link {
    color: #888;
    font-size: 30rpx;
  }
}
</style>