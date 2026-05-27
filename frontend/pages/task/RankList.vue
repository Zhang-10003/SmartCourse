<template>
  <view class="rank-page">
    <view v-if="loading" class="rank-state">
      <text class="state-text">查询中...</text>
    </view>
    <RankListBoard
      v-else-if="rankInfo"
      :result-data="rankInfo" 
      @back="goBack" 
    />
    <view v-else class="rank-state">
      <text class="state-text">{{ stateMessage }}</text>
      <text class="back-link" @tap="goBack">返回作业列表</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';
import { onLoad } from '@dcloudio/uni-app';
import RankListBoard from '../../components/QueryResultBoard.vue';
import request from '../../utils/request.js';

const loading = ref(true);
const stateMessage = ref('');
const rankInfo = ref(null);

onLoad(async (options) => {
  const assignmentId = Number(options.id);
  const userInfo = uni.getStorageSync('userInfo');

  if (!assignmentId) {
    loading.value = false;
    stateMessage.value = '作业信息无效';
    return;
  }
  if (!userInfo || !userInfo.user_id) {
    loading.value = false;
    stateMessage.value = '请先登录后查看排行';
    return;
  }

  try {
    const response = await request.get(`/api/assignments/${assignmentId}/rank/${userInfo.user_id}`);
    if (!response.success || response.status !== 'ready' || !response.data) {
      stateMessage.value = response.message || '暂时无法查看排行';
      return;
    }

    const data = response.data;
    rankInfo.value = {
      totalScore: data.score,
      name: data.name,
      rank: data.rank,
      percentage: data.beat_percentage
    };
  } catch (error) {
    console.error('获取学生排行失败:', error);
    stateMessage.value = '获取排行失败，请稍后重试';
  } finally {
    loading.value = false;
  }
});

const goBack = () => uni.navigateBack();
</script>

<style>
.rank-page {
  background-color: #f8f9fb;
  min-height: 100vh;
}

.rank-state {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 32rpx;
  background: #ffffff;
}

.state-text {
  color: #64748b;
  font-size: 32rpx;
}

.back-link {
  color: #1677ff;
  font-size: 28rpx;
}
</style>
