<template>
  <view class="container mobile-page">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="nav-title">消息通知</text>
        <text class="nav-action">全部已读</text>
      </view>
    </view>

    <view class="notice-list">
      <view 
        class="notice-card" 
        v-for="(msg, index) in notices" 
        :key="index"
        @click="handleDetail(msg)"
      >
        <view class="card-header">
          <view class="title-section">
            <view class="unread-dot" v-if="index === 0"></view>
            <text class="notice-title">{{ msg.title }}</text>
          </view>
          <text class="notice-time">{{ msg.time }}</text>
        </view>
        
        <view class="notice-content">{{ msg.content }}</view>
        
        <view class="card-footer">
          <text class="detail-btn">查看详情</text>
          <text class="cuIcon-right icon"></text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const notices = ref([
  { title: '课程变动通知', content: '明天的计算机网络课程改至 302 教室，请同学们带好教材准时参加。', time: '10:30' },
  { title: '作业提醒', content: '数据结构链表专题作业即将截止，请在今晚 23:59 前完成提交。', time: '昨天' },
  { title: '系统更新', content: '智能课程助手 V1.2 版本已发布，修复了已知的问题。', time: '3天前' }
]);

const handleDetail = (msg) => {
  console.log('跳转详情', msg.title);
};
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f8f9fa; // 使用浅灰色背景，衬托白色卡片
}

/* 导航栏优化 */
.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px); // 毛玻璃效果
  border-bottom: 1rpx solid #eee;

  .status-bar {
    height: var(--status-bar-height);
    width: 100%;
  }

  .nav-content {
    height: 44px;
    padding: 0 15px;
    display: flex;
    align-items: center;
    justify-content: space-between; // 标题居中，右侧放功能键
    
    .nav-title {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      font-size: 18px;
      font-weight: 700;
      color: #2d3436;
    }
    
    .nav-action {
      font-size: 14px;
      color: #007aff; // 品牌色
      margin-left: auto;
    }
  }
}

/* 列表区域优化 */
.notice-list {
  padding: calc(var(--status-bar-height) + 60px) 15px 30px;
}

.notice-card {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 18px;
  margin-bottom: 15px;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.03); // 极轻微的阴影
  transition: transform 0.2s;

  &:active {
    transform: scale(0.98); // 点击反馈
    background: #fafafa;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .title-section {
      display: flex;
      align-items: center;
      
      .unread-dot {
        width: 8px;
        height: 8px;
        background: #ff4d4f;
        border-radius: 50%;
        margin-right: 8px;
      }
      
      .notice-title {
        font-weight: 600;
        font-size: 16px;
        color: #2d3436;
      }
    }

    .notice-time {
      color: #b2bec3;
      font-size: 12px;
    }
  }

  .notice-content {
    color: #636e72;
    font-size: 14px;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2; // 最多显示两行，超出省略
    overflow: hidden;
  }

  .card-footer {
    margin-top: 15px;
    padding-top: 12px;
    border-top: 1rpx solid #f1f2f6;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .detail-btn {
      font-size: 13px;
      color: #007aff;
      font-weight: 500;
    }
    
    .icon {
      color: #dfe6e9;
      font-size: 12px;
    }
  }
}
</style>