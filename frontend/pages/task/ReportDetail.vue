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
        <view v-if="viewState === 'loading' || viewState === 'generating'" class="state-panel">
          <text class="state-text">{{ stateMessage }}</text>
        </view>
        <view v-else-if="viewState === 'empty' || viewState === 'error'" class="state-panel">
          <text class="state-text">{{ stateMessage }}</text>
          <text v-if="viewState === 'error'" class="retry-link" @click="loadReport">重新加载</text>
        </view>
        <view v-else class="feedback-list">
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
import { ref, onUnmounted } from 'vue';
import { onLoad } from '@dcloudio/uni-app';
import request from '@/utils/request.js';

const reportData = ref({
  title: '学情反馈报告',
  sections: []
});

const viewState = ref('loading');
const stateMessage = ref('报告加载中...');
let reportTimer = null;
let reportRequestId = 0;
let assignmentId = null;
let studentId = null;

const stopReportPolling = () => {
  if (reportTimer) {
    clearTimeout(reportTimer);
    reportTimer = null;
  }
};

const buildSections = (report) => {
  const sections = [];
  if (report.error_summary) {
    sections.push({
      type: 'error',
      title: '错误总结',
      color: '#ef4444',
      content: report.error_summary
    });
  }
  if (report.study_suggestions) {
    sections.push({
      type: 'suggest',
      title: '学习建议',
      color: '#10b981',
      content: report.study_suggestions
    });
  }
  return sections;
};

const fetchReport = async (requestId) => {
  if (requestId !== reportRequestId || !assignmentId || !studentId) return;

  try {
    const response = await request.get(`/api/submit/${assignmentId}/${studentId}`);
    if (requestId !== reportRequestId) return;

    if (!response.success || !response.data) {
      stopReportPolling();
      viewState.value = 'error';
      stateMessage.value = response.message || '未找到本次作业的提交记录';
      return;
    }

    if (response.data.status === 'grading') {
      viewState.value = 'generating';
      stateMessage.value = '报告生成中...';
      stopReportPolling();
      reportTimer = setTimeout(() => fetchReport(requestId), 1500);
      return;
    }

    stopReportPolling();
    const sections = buildSections(response.data.report || {});
    if (sections.length === 0) {
      viewState.value = 'empty';
      stateMessage.value = '本次批改已完成，暂无 AI 反馈内容';
      return;
    }

    reportData.value.sections = sections;
    viewState.value = 'ready';
  } catch (error) {
    if (requestId !== reportRequestId) return;
    console.error('获取个人学情反馈报告失败:', error);
    stopReportPolling();
    viewState.value = 'error';
    stateMessage.value = '获取报告失败，请稍后重试';
  }
};

const loadReport = () => {
  stopReportPolling();
  reportRequestId++;
  reportData.value.sections = [];
  viewState.value = 'loading';
  stateMessage.value = '报告加载中...';
  fetchReport(reportRequestId);
};

onLoad((options) => {
  assignmentId = Number(options.id);
  const userInfo = uni.getStorageSync('userInfo');

  if (!assignmentId) {
    viewState.value = 'error';
    stateMessage.value = '作业信息无效';
    return;
  }
  if (!userInfo || !userInfo.user_id) {
    viewState.value = 'error';
    stateMessage.value = '请先登录后查看报告';
    return;
  }

  studentId = userInfo.user_id;
  loadReport();
});

onUnmounted(() => {
  reportRequestId++;
  stopReportPolling();
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

.state-panel {
  min-height: 360rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 32rpx;
}

.state-text {
  font-size: 30rpx;
  color: #64748b;
}

.retry-link {
  font-size: 28rpx;
  color: #1677ff;
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
