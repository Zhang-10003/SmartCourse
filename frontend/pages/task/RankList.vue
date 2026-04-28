<template>
  <view class="rank-page">
    <RankListBoard 
      :result-data="rankInfo" 
      @back="goBack" 
    />
  </view>
</template>

<script setup>
import { ref } from 'vue';
import { onLoad } from '@dcloudio/uni-app';
import RankListBoard from '../../components/QueryResultBoard.vue';

// 给初始值，防止加载瞬间的报错
const rankInfo = ref({
  totalScore: 0,
  name: '',
  rank: 0,
  percentage: 0
});

onLoad((options) => {
  // 模拟 API 请求
  setTimeout(() => {
    rankInfo.value = {
      totalScore: 8,
      name: '黄泓铭',
      rank: 4,
      percentage: 93.0
    };
  }, 200);
});

const goBack = () => uni.navigateBack();
</script>

<style>
.rank-page {
  background-color: #f8f9fb;
  min-height: 100vh;
}
</style>