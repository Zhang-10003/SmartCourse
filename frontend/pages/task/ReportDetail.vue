<template>
  <view class="page-container">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="back-icon" @click="goBack"></text>
        <text class="nav-title">{{ reportData.title }}</text>
        <view class="nav-right"></view>
      </view>
    </view>
    
    <scroll-view class="main-content" scroll-y>
      <view class="phone-canvas">
        <view class="feedback-list">
          <view 
            v-for="(section, index) in reportData.sections" 
            :key="index" 
            class="feedback-card"
            :class="section.type"
          >
            <view class="card-title" :style="{ '--theme-color': section.color }">
              <text class="title-text">{{ section.title }}</text>
            </view>
            <view class="content-text">{{ section.content }}</view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const reportData = ref({
  title: '学情反馈报告',
  sections: [
    {
      type: 'error',
      title: '错误总结',
      color: '#ef4444',
      content: '本次作业的核心问题在于条件循环语句的概念混淆，具体表现为逻辑上的死循环以及临界点拦截失效导致的数组越界隐患，这些问题直接暴露了在编写边界逻辑时缺乏严谨的数据自增与极限值校验意识。'
    },
    {
      type: 'suggest',
      title: '学习建议',
      color: '#10b981',
      content: '后续应将重心放在重温循环控制结构的基础例题上，通过模拟数据盲推来培养自检习惯，并结合针对性的边界值专项微练，在实际动手调试中快速攻克并理清代码的逻辑临界点。'
    }
  ]
});

const goBack = () => uni.navigateBack();
</script>

<style lang="scss" scoped>
.page-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.custom-navbar {
  background-color: #ffffff;
  .status-bar { height: var(--status-bar-height); }
  .nav-content {
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 30rpx;
    
    .back-icon { font-size: 40rpx; color: #333; }
    .nav-title {
      font-size: 32rpx;
      font-weight: 600;
      color: #1a1a1a;
    }
    .nav-right { width: 40rpx; }
  }
}

.main-content {
  height: calc(100vh - var(--status-bar-height) - 44px);
  padding: 30rpx;
}

.phone-canvas {
  width: 100%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 36rpx;
  padding: 32rpx 24rpx;
  box-shadow: 0 20px 50px rgba(148, 163, 184, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.feedback-card {
  background: #ffffff;
  border-radius: 20rpx;
  padding: 22rpx;
  box-shadow: 0 4px 16px rgba(148, 163, 184, 0.05);
  border: 1px solid rgba(241, 245, 249, 0.9);
  
  &:active {
    transform: scale(0.98);
  }
}

.card-title {
  font-size: 32rpx;
  font-weight: 600;
  margin-bottom: 16rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
  position: relative;
  
  &::before {
    content: '';
    display: block;
    width: 6rpx;
    height: 32rpx;
    background: var(--theme-color);
    border-radius: 4rpx;
  }
  
  .title-text {
    color: var(--theme-color);
  }
}

.content-text {
  color: #1e293b;
  font-size: 28rpx;
  line-height: 1.8;
  text-align: justify;
}
</style>