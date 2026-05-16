<template>
  <view class="page mobile-page">
    <view class="fixed-header">
      <view class="status-bar"></view>
      
      <view class="header-top">
        <view class="avatar-box">
          <image class="avatar-img" src="/static/logo.png" mode="aspectFill"></image>
        </view>
        <view class="search-wrapper">
          <input class="search-input" type="text" placeholder="搜索作业题目" placeholder-style="color:#bbb" />
          <text class="search-icon">🔍</text>
        </view>
        <view class="action-icons">
          <view class="icon-item">
            <text>🔔</text>
            <view class="dot"></view>
          </view>
        </view>
      </view>
    </view>

    <scroll-view class="main-content" scroll-y>
      <view class="filter-bar">
        <text class="time-label">七天内</text>
        <view class="filter-icons">
          <text>⏳</text>
          <text>⊞</text>
          <text>☑</text>
        </view>
      </view>

      <view class="card" v-for="(item, index) in tasks" :key="index" @click="goToAssignmentDetail(index)">
        <view class="card-header">
          <text :class="['tag', item.statusType]">{{ item.statusText }}</text>
        </view>
        <view class="card-title">{{ item.title }}</view>
        <view class="card-footer">
          <text class="deadline">截止: {{ item.deadline }}</text>
          
          <view 
            v-if="item.statusType === 'expired'" 
            class="report-link" 
            @click.stop="goToReport(index)"
          >
            <text class="report-icon">📊</text>
            <text class="report-text">查看报告</text>
          </view>
          <view 
            v-if="item.statusType === 'expired'" 
            class="rank-link" 
            @click.stop="goToRank(index)"
          >
            <text class="rank-icon">🏆</text>
            <text class="rank-text">查看排行</text>
          </view>
        </view>
      </view>
      
      <view class="safe-bottom"></view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const tasks = ref([
  { title: '计算机网络周测 - TCP原理', deadline: '05-10 18:00', statusText: '进行中', statusType: 'processing' },
  { title: '数据结构：链表专题', deadline: '04-20 12:00', statusText: '已提交', statusType: 'submitted' },
  { title: '操作系统同步互斥习题', deadline: '04-15 23:59', statusText: '已截止', statusType: 'expired' }
]);

const goToAssignmentDetail = (index) => {
  const task = tasks.value[index];
  uni.navigateTo({
    url: `/pages/task/AssignmentDetail?id=${index + 1}&status=${task.statusType}`
  });
};
const goToReport = (index) => {
  uni.navigateTo({
    url: `/pages/task/ReportDetail?id=${index + 1}`
  });
};
const goToRank = (index) => {
  uni.navigateTo({
    url: `/pages/task/RankList?id=${index + 1}`
  });
};
</script>

<style lang="scss" scoped>
.page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #ffffff;
  z-index: 999;
  
  .status-bar { height: var(--status-bar-height); }

  .header-top {
    display: flex;
    align-items: center;
    padding: 8px 15px;
    
    .avatar-box {
      width: 34px;
      height: 34px;
      background: #f0f0f0;
      border-radius: 50%;
      overflow: hidden;
      margin-right: 12px;
      .avatar-img { width: 100%; height: 100%; }
    }
    
    .search-wrapper {
      flex: 1;
      height: 36px;
      background: #f2f3f5;
      border-radius: 18px;
      display: flex;
      align-items: center;
      padding: 0 12px;
      .search-icon { font-size: 14px; margin-right: 6px; }
      .search-input { flex: 1; font-size: 14px; }
    }

    .action-icons {
      margin-left: 15px;
      display: flex;
      .icon-item {
        position: relative;
        font-size: 22px;
        .dot {
          position: absolute;
          top: 2px; right: 0;
          width: 8px; height: 8px;
          background: #ff4d4f;
          border: 1px solid #fff;
          border-radius: 50%;
        }
      }
    }
  }
}

.main-content {
  padding-top: calc(var(--status-bar-height) + 52px);
  padding-left: 15px;
  padding-right: 15px;

  .filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    .time-label { font-size: 13px; color: #999; }
    .filter-icons text { margin-left: 15px; color: #666; font-size: 18px; }
  }
}

.card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-sizing: border-box;
  width: auto;
  margin-left: 0;
  margin-right: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); 
  border: 1rpx solid #f0f0f0; 

  .card-header { 
    margin-bottom: 10px; 
    .tag { 
      font-size: 12px; 
      padding: 2px 8px; 
      border-radius: 4px; 
      display: inline-block;
      &.processing { background: #e8f2ff; color: #007aff; } 
      &.submitted { background: #e7f7ef; color: #07c160; } 
      &.expired { background: #f2f2f2; color: #999; } 
    } 
  }
  
  .card-title { 
    font-size: 18px; 
    font-weight: bold; 
    color: #333; 
    margin-bottom: 12px;
    word-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    line-height: 1.4;
  }
  
  .deadline { font-size: 14px; color: #999; }
  
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;

    .deadline {
      font-size: 13px;
      color: #999;
    }

    .report-link {
      display: flex;
      align-items: center;
      background-color: #e6f7ff;
      padding: 4px 10px;
      border-radius: 100px;
      border: 1px solid #91d5ff;
      margin-right: 8px;

      .report-icon {
        font-size: 12px;
        margin-right: 4px;
      }

      .report-text {
        font-size: 12px;
        color: #1890ff;
        font-weight: 500;
      }
    }

    .rank-link {
      display: flex;
      align-items: center;
      background-color: #fff7e6;
      padding: 4px 10px;
      border-radius: 100px;
      border: 1px solid #ffe58f;

      .rank-icon {
        font-size: 12px;
        margin-right: 4px;
      }

      .rank-text {
        font-size: 12px;
        color: #d48806;
        font-weight: 500;
      }
    }
  }
}
.safe-bottom { height: 20px; }
</style>