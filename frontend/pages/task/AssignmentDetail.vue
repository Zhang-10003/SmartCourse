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
          {{ taskInfo.status === 'expired' ? '已截止' : taskInfo.status === 'submitted' ? '已提交' : '剩余 20:12' }}
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
          
          <AIFeedback 
            v-if="(taskInfo.status === 'expired') && questionFeedbacks[index]" 
            :res-json="questionFeedbacks[index]" 
            style="display:block;"
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
import { ref } from 'vue';
import QuestionMultipleChoice from '../../components/QuestionMultipleChoice.vue';
import QuestionTrueFalse from '../../components/QuestionTrueFalse.vue';
import QuestionFillBlank from '../../components/QuestionFillBlank.vue';
import QuestionShortAnswer from '../../components/QuestionShortAnswer.vue';
import QuestionMatching from '../../components/QuestionMatching.vue';
import QuestionCodeFill from '../../components/QuestionCodeFill.vue';
import AIFeedback from '../../components/AIFeedback.vue';

const currentIndex = ref(0);
const taskInfo = ref({
  title: '计算机网络周测 - TCP原理',
  status: 'submitted' 
});

const questionFeedbacks = ref([
  { score: '20/20', feedback: '回答正确！TCP是传输层协议，负责端到端的可靠数据传输。' },
  { score: '15/20', feedback: '回答基本正确，但漏选了UDP。UDP也是传输层协议。' },
  { score: '10/10', feedback: '回答正确！TCP是面向连接的可靠协议。' },
  { score: '10/15', feedback: '第一空正确！第二空回答不够准确，网络层的主要功能是路由选择和分组转发。' },
  { score: '5/20', feedback: '回答过于简略，需要详细描述三次握手的每个阶段及其目的。' },
  { score: '3/10', feedback: '匹配完全错误，请重新学习OSI模型各层协议。' },
  { score: '2/5', feedback: '堆栈操作理解有误，请复习汇编语言中push和call指令对SP的影响。' }
]);

import { onLoad } from '@dcloudio/uni-app';

onLoad((options) => {
  if (options?.status) {
    taskInfo.value.status = options.status;
  }
});

const questions = ref([
  { 
    type: 'choice',
    question_title: '以下哪个协议属于传输层？',
    options: ['TCP', 'IP', 'HTTP', 'DNS'],
    isMultiple: false,
    userAnswer: [0],
    correctAnswers: [0]
  },
  { 
    type: 'choice',
    question_title: '哪些是网络层协议？',
    options: ['IP', 'ICMP', 'UDP', 'ARP'],
    isMultiple: true,
    userAnswer: [0, 1],
    correctAnswers: [0, 1, 3]
  },
  { 
    type: 'true_false',
    question_title: 'TCP是一种无连接的协议。',
    userAnswer: false,
    correctAnswers: false
  },
  { 
    type: 'fill_blank',
    content: 'OSI模型分为????层，其中网络层的主要功能是????。',
    userAnswer: ['7', '数据传输'],
    correctAnswers: ['7', '路由选择']
  },
  { 
    type: 'short_answer',
    question_title: '简述TCP三次握手的过程。',
    userAnswer: 'TCP三次握手就是客户端和服务器之间交换三个报文。',
    correctAnswers: 'TCP三次握手过程：1. 客户端发送SYN包；2. 服务器发送SYN+ACK包；3. 客户端发送ACK包。'
  },
  { 
    type: 'matching',
    question_title: '将协议与其对应的层次匹配',
    leftItems: ['TCP', 'IP', 'HTTP', 'ARP'],
    rightItems: ['传输层', '网络层', '应用层', '网络层'],
    userAnswer: [{ l: 0, r: 1 }, { l: 1, r: 0 }, { l: 2, r: 2 }, { l: 3, r: 3 }],
    correctAnswers: [{ l: 0, r: 0 }, { l: 1, r: 1 }, { l: 2, r: 2 }, { l: 3, r: 1 }]
  },
  { 
    type: 'code_fill',
    question_title: '程序跟踪分析',
    code: `start: 
    mov ax, 1000h ; 设置起始段地址
    mov ss, ax    ; 设置堆栈段
    mov sp, 0020h ; 初始 SP = 0020H
    
    push ax        ; 将 AX 压栈
      SP1=????
      
    call sub_proc ; 调用子程序 (当前 IP=0108H)
      IP1=????
      SP2=????
  
  sub_proc:
    add ax, 05h   ; 执行加法
    ret           ; 子程序返回
      IP2=????
      SP3=????
  end start`,
    fields: [
      { label: "SP1", value: "001Eh" },
      { label: "IP1", value: "010Bh" },
      { label: "SP2", value: "001Ch" },
      { label: "IP2", value: "" },
      { label: "SP3", value: "" }
    ],
    userAnswer: [],
    correctAnswers: ['001Eh', '010BH', '001Ch', '010BH', '0020H']
  }
]);

const prev = () => { 
  if (currentIndex.value > 0) currentIndex.value--; 
};

const next = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++; 
  }
};

const handleSubmit = () => {
  console.log('用户答案汇总：', questions.value.map(q => q.userAnswer));
  
  if (taskInfo.value.status === 'finished' || taskInfo.value.status === 'submitted') {
    uni.navigateBack();
  } else {
    uni.showModal({
      title: '提示',
      content: '确定提交本次测试吗？',
      success: (res) => {
        if (res.confirm) {
          taskInfo.value.status = 'finished';
        }
      }
    });
  }
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