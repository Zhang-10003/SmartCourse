<template>
  <view class="detail-container">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="back-icon" @click="goBack"></text>
        <text class="nav-title">{{ taskInfo.title }}</text>
        <view class="nav-right"></view>
      </view>
    </view>

    <view class="info-banner">
      <view class="progress-box">
        <text class="label">当前进度：</text>
        <text class="value">{{ currentIndex + 1 }} / {{ questions.length }}</text>
      </view>
      <view class="timer-box" v-if="taskInfo.status !== 'finished'">
        <text class="time-left" :class="{ 'expired': taskInfo.status === 'expired' }">
          {{ taskInfo.status === 'expired' ? '已截止' : taskInfo.status === 'submitted' ? '已提交' : countdownText }}
        </text>
      </view>
    </view>



    <swiper 
      class="question-swiper" 
      :current="currentIndex" 
      @change="e => currentIndex = e.detail.current"
    >
      <swiper-item v-for="(q, index) in questions" :key="index">
        <scroll-view scroll-y class="scroll-v">
          <QuestionMultipleChoice
            v-if="q.type === 'choice'"
            :index="index + 1"
            :question="q"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
            :status="taskInfo.status === 'expired' ? 'result' : 'typing'"
            :correct-answer="q.correctAnswers"
            :model-value="q.userAnswer"
            @update:model-value="(val) => q.userAnswer = val"
          />
          
          <QuestionTrueFalse
            v-else-if="q.type === 'true_false'"
            :index="index + 1"
            :question="q"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
            :status="taskInfo.status === 'expired' ? 'result' : 'typing'"
            :correct-answer="q.correctAnswers"
            :model-value="q.userAnswer"
            @update:model-value="(val) => q.userAnswer = val"
          />
          
          <QuestionFillBlank
            v-else-if="q.type === 'fill_blank'"
            :index="index + 1"
            :question="q"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
            :status="taskInfo.status === 'expired' ? 'result' : 'typing'"
            :correct-answers="q.correctAnswers"
            :model-value="q.userAnswer"
            @update:model-value="(val) => q.userAnswer = val"
            @answer-change="(val) => q.userAnswer = val"
          />
          
          <QuestionShortAnswer
            v-else-if="q.type === 'short_answer'"
            :index="index + 1"
            :question="q"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
            :status="taskInfo.status === 'expired' ? 'result' : 'typing'"
            :correct-answer="q.correctAnswers"
            :model-value="q.userAnswer"
            @update:model-value="(val) => q.userAnswer = val"
          />
          
          <QuestionMatching
            v-else-if="q.type === 'matching'"
            :index="index + 1"
            :question="q"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
            :status="taskInfo.status === 'expired' ? 'result' : 'typing'"
            :correct-answers="q.correctAnswers"
            :model-value="q.userAnswer"
            @update:model-value="(val) => q.userAnswer = val"
          />
          
          <QuestionCodeFill
            v-else-if="q.type === 'code_fill'"
            :data="{ index: index + 1, question: q }"
            :disabled="taskInfo.status === 'submitted' || taskInfo.status === 'expired'"
          />
        </scroll-view>
      </swiper-item>
    </swiper>

    <view class="footer">
      <button class="btn-action prev" :class="{ disabled: currentIndex === 0 }" @click="prev">上一题</button>
      <view class="sheet-entry">
        <text class="iconfont"></text>
      </view>
      <button v-if="currentIndex < questions.length - 1" class="btn-action next" @click="next">下一题</button>
      <button v-else class="btn-action submit" @click="handleSubmit">
            {{ taskInfo.status === 'finished' || taskInfo.status === 'submitted' ? '返回' : '提交' }}
          </button>
    </view>
  </view>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { onLoad } from '@dcloudio/uni-app';
import request from '@/utils/request.js';
import QuestionMultipleChoice from '../../components/QuestionMultipleChoice.vue';
import QuestionTrueFalse from '../../components/QuestionTrueFalse.vue';
import QuestionFillBlank from '../../components/QuestionFillBlank.vue';
import QuestionShortAnswer from '../../components/QuestionShortAnswer.vue';
import QuestionMatching from '../../components/QuestionMatching.vue';
import QuestionCodeFill from '../../components/QuestionCodeFill.vue';

const currentIndex = ref(0);
const taskInfo = ref({ title: '', status: '' });
const questions = ref([]);
const submissionData = ref(null);
const loading = ref(true);
const countdownText = ref('');

let countdownTimer = null;
let assignmentId = null;

onLoad((options) => {
  if (options?.status) taskInfo.value.status = options.status;
  if (options?.title) taskInfo.value.title = decodeURIComponent(options.title);
  if (options?.id) {
    assignmentId = parseInt(options.id, 10);
    fetchQuestions(assignmentId);
  }
  if (options?.deadline_ts && options.status === 'processing') {
    const ts = parseInt(options.deadline_ts, 10) * 1000;
    if (ts > 0) startCountdown(ts);
  }
});

function startCountdown(deadlineMs) {
  const deadline = new Date(deadlineMs);
  function tick() {
    const now = new Date();
    const diff = deadline - now;
    if (diff <= 0) {
      countdownText.value = '已截止';
      taskInfo.value.status = 'expired';
      if (countdownTimer) clearInterval(countdownTimer);
      return;
    }
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    countdownText.value = `剩余 ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }
  tick();
  countdownTimer = setInterval(tick, 1000);
}

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer);
});

async function fetchQuestions(assignmentId) {
  try {
    const [qRes, subRes] = await Promise.all([
      request.get(`/api/questions?assignment_id=${assignmentId}`),
      taskInfo.value.status === 'submitted' || taskInfo.value.status === 'expired'
        ? request.get(`/api/submit/${assignmentId}/${uni.getStorageSync('userInfo')?.user_id}`).catch(() => null)
        : null
    ]);

    if (qRes && qRes.success) {
      questions.value = (qRes.data || []).map(mapBackendQuestion);

      if (subRes && subRes.success) {
        submissionData.value = subRes.data;
        const answerMap = {};
        for (const a of subRes.data.answers) {
          answerMap[a.question_id] = a;
        }
        for (const q of questions.value) {
          const saved = answerMap[q.question_id];
          if (saved) {
            q.userAnswer = JSON.parse(saved.answer);
            if (q.type === 'code_fill' && q.fields && Array.isArray(q.userAnswer)) {
              q.fields.forEach((f, i) => { f.value = q.userAnswer[i] || ''; });
            }
          }
        }
      }
    } else {
      uni.showToast({ title: qRes?.message || '获取题目失败', icon: 'none' });
    }
  } catch (e) {
    console.error('获取题目失败:', e);
    uni.showToast({ title: '获取题目失败', icon: 'none' });
  } finally {
    loading.value = false;
  }
}

function mapBackendQuestion(q) {
  let type = q.type;
  const isMultiple = type === 'multiple_choice' || q.is_multiple;
  if (type === 'multiple_choice') type = 'choice';

  const mapped = {
    question_id: q.question_id,
    type,
    question_title: q.question_title || '',
    isMultiple,
    analysis: q.analysis || '',
    score: q.score || 0,
    userAnswer: initUserAnswer(type),
    correctAnswers: parseField(q.correct_answers),
  };

  if (q.options) mapped.options = parseField(q.options);
  if (q.content) mapped.content = q.content;
  if (q.code) mapped.code = q.code;
  if (q.fields) mapped.fields = parseField(q.fields);
  if (q.left_items) mapped.leftItems = parseField(q.left_items);
  if (q.right_items) mapped.rightItems = parseField(q.right_items);

  return mapped;
}

function parseField(val) {
  if (!val) return null;
  try { return JSON.parse(val); } catch { return val; }
}

function initUserAnswer(type) {
  switch (type) {
    case 'choice': return [];
    case 'true_false': return null;
    case 'short_answer': return '';
    case 'fill_blank': return [];
    case 'matching': return [];
    default: return null;
  }
}

const prev = () => { 
  if (currentIndex.value > 0) currentIndex.value--; 
};

const next = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++; 
  }
};

const handleSubmit = () => {
  if (taskInfo.value.status === 'finished' || taskInfo.value.status === 'submitted') {
    uni.navigateBack();
    return;
  }

  uni.showModal({
    title: '提示',
    content: '确定提交本次测试吗？',
    success: async (modalRes) => {
      if (!modalRes.confirm) return;

      const userInfo = uni.getStorageSync('userInfo');
      if (!userInfo || !userInfo.user_id) {
        uni.showToast({ title: '请先登录', icon: 'none' });
        return;
      }

      const answers = questions.value.map(q => {
        let answer = q.userAnswer;
        // code_fill: 从 fields 中提取答案
        if (q.type === 'code_fill' && q.fields) {
          answer = q.fields.map(f => f.value || '');
        }
        return {
          question_id: q.question_id,
          answer: JSON.stringify(answer ?? '')
        };
      });

      uni.showLoading({ title: '提交中...' });

      try {
        const res = await request.post('/api/submit', {
          assignment_id: assignmentId,
          student_id: userInfo.user_id,
          answers
        });

        uni.hideLoading();

        if (res && res.success) {
          taskInfo.value.status = 'submitted';
          uni.showToast({ title: '提交成功', icon: 'success' });
        } else {
          uni.showToast({ title: res?.message || '提交失败', icon: 'none' });
        }
      } catch (e) {
        uni.hideLoading();
        console.error('提交异常:', e);
        uni.showModal({ title: '提交失败', content: e.message || JSON.stringify(e), showCancel: false });
      }
    }
  });
};

const goBack = () => uni.navigateBack();
</script>

<style lang="scss" scoped>
.detail-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
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

.info-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 40rpx 0rpx;
  background-color: #ffffff;
  
  .progress-box {
    .label { color: #999; font-size: 26rpx; }
    .value { color: #333; font-weight: bold; font-size: 30rpx; }
  }
  .time-left { 
    color: #ff5e5e; 
    font-size: 28rpx; 
    font-weight: 500; 
    &.expired {
      color: #ff5e5e;
      font-weight: 600;
    }
  }
}

.question-swiper { 
  flex: 1; 
  background-color: #ffffff;
}

.scroll-v { 
  height: 100%; 
  padding: 0rpx 30rpx 30rpx;
  box-sizing: border-box; 
  background-color: #ffffff;
}

/* 作业得分和反馈区域 */
.summary-box {
  margin: 20rpx 30rpx;
  padding: 30rpx;
  background: linear-gradient(135deg, #fff7f0 0%, #fef7ff 100%);
  border-radius: 20rpx;
  border: 2rpx solid #f0e6ff;
}

.summary-title {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 16rpx;
}

.score-display {
  display: flex;
  align-items: baseline;
  margin-bottom: 24rpx;
}

.score-value {
  font-size: 72rpx;
  font-weight: 800;
  color: #ff6b6b;
}

.score-slash {
  font-size: 36rpx;
  color: #999;
  margin: 0 8rpx;
}

.score-max {
  font-size: 36rpx;
  color: #999;
}

.feedback-summary {
  border-top: 1rpx dashed #e8d5ff;
  padding-top: 24rpx;
}

.feedback-label {
  font-size: 26rpx;
  color: #ff6b6b;
  font-weight: 600;
  margin-bottom: 12rpx;
}

.feedback-text {
  font-size: 26rpx;
  color: #333;
  line-height: 1.7;
  white-space: pre-wrap;
}

.footer {
  background: #fff;
  padding: 20rpx 40rpx calc(20rpx + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.05);

  .btn-action {
    flex: 1;
    height: 88rpx;
    line-height: 88rpx;
    border-radius: 44rpx;
    font-size: 30rpx;
    font-weight: 500;
    margin: 0;
    &::after { border: none; }
    
    &.prev {
      background-color: #f2f3f5;
      color: #666;
      &.disabled { opacity: 0.5; }
    }
    &.next {
      background-color: #3578ff;
      color: #fff;
    }
    &.submit {
      background-color: #49b972;
      color: #fff;
    }
  }

  .sheet-entry {
    padding: 0 40rpx;
    .iconfont { font-size: 44rpx; color: #333; }
  }
}
</style>