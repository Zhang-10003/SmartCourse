<template>
  <view class="detail-container">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="back-icon" @click="goBack"></text>
        <text class="nav-title">{{ taskInfo.title }}</text>
        <view class="nav-right"></view> </view>
    </view>

    <view class="info-banner">
      <view class="progress-box">
        <text class="label">当前进度：</text>
        <text class="value">{{ currentIndex + 1 }} / {{ questions.length }}</text>
      </view>
      <view class="timer-box" v-if="taskInfo.status !== 'finished'">
        <text class="time-left">剩余 23:51</text>
      </view>
    </view>

    <swiper 
      class="question-swiper" 
      :current="currentIndex" 
      @change="e => currentIndex = e.detail.current"
    >
      <swiper-item v-for="(q, index) in questions" :key="index">
        <scroll-view scroll-y class="scroll-v">
          <component 
            :is="getComponent(q.type)" 
            v-if="q.type !== 'code_fill'"
            :question="q" 
            :index="index + 1"
            :status="taskInfo.status === 'finished' ? 'result' : 'typing'"
            :correctAnswer="q.correctAnswer"
            :correctAnswers="q.correctAnswers"
            v-model="q.userAnswer" 
          />
          <component 
            :is="getComponent(q.type)" 
            v-else
            :data="{ index: index + 1, question: q }"
            :status="taskInfo.status === 'finished' ? 'result' : 'typing'"
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
        {{ taskInfo.status === 'finished' ? '返回' : '提交' }}
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

const currentIndex = ref(0);
const taskInfo = ref({
  title: '计算机网络周测 - TCP原理',
  status: 'ongoing' 
});

const questions = ref([
  { 
    type: 'choice', 
    isMultiple: false, // 单选题
    title: '以下哪个协议属于传输层？', 
    options: ['TCP', 'IP', 'HTTP', 'DNS'], 
    userAnswer: [],    // 初始值必须是数组，否则子组件的 includes 会报错
    correctAnswer: [0] // 正确答案是 TCP
  },
  { 
    type: 'choice', 
    isMultiple: true,  // 多选题
    title: '哪些是网络层协议？', 
    options: ['IP', 'ICMP', 'UDP', 'ARP'], 
    userAnswer: [], 
    correctAnswer: [0, 1, 3] // 正确答案是 IP, ICMP, ARP
  },
  { 
    type: 'true_false', 
    title: 'TCP是一种无连接的协议。', 
    userAnswer: null, 
    correctAnswer: false // 正确答案是错误
  },
  { 
    type: 'fill_blank', 
    content: 'OSI模型分为????层，其中网络层的主要功能是????。', 
    userAnswer: [], 
    correctAnswers: ['7', '路由选择'] // 正确答案
  },
  { 
    type: 'short_answer', 
    title: '简述TCP三次握手的过程。', 
    userAnswer: '', 
    correctAnswer: 'TCP三次握手过程：1. 客户端发送SYN包；2. 服务器发送SYN+ACK包；3. 客户端发送ACK包。' // 正确答案
  },
  { 
    type: 'matching', 
    title: '将协议与其对应的层次匹配', 
    leftItems: ['TCP', 'IP', 'HTTP', 'ARP'], 
    rightItems: ['传输层', '网络层', '应用层', '网络层'], 
    userAnswer: [], 
    correctAnswers: [{ l: 0, r: 0 }, { l: 1, r: 1 }, { l: 2, r: 2 }, { l: 3, r: 3 }] // 正确答案
  },
  { 
      type: 'code_fill', 
      title: '程序跟踪分析：<br>假设初始 <b>SP = 2000H</b>。请分析下方汇编片段，填写指令执行后对应的寄存器状态。', 
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
        { label: "SP1", value: "" },
        { label: "IP1", value: "" },
        { label: "SP2", value: "" },
        { label: "IP2", value: "" },
        { label: "SP3", value: "" }
      ],
      userAnswer: [], // 用于存储最终答案
      correctAnswers: ['001Eh', '010BH', '001Ch', '010BH', '0020H'] // 示例正确答案
    }
]);

const getComponent = (type) => {
  const map = {
    'choice': QuestionMultipleChoice,
    'true_false': QuestionTrueFalse,
    'fill_blank': QuestionFillBlank,
    'short_answer': QuestionShortAnswer,
    'matching': QuestionMatching,
    'code_fill': QuestionCodeFill
  };
  return map[type];
};

const prev = () => { if (currentIndex.value > 0) currentIndex.value--; };
const next = () => {
  // 必须加 .value，否则变量不会响应式更新
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++; 
  }
};

const handleSubmit = () => {
  // 打印数据检查 v-model 是否生效
  console.log('用户答案汇总：', questions.value.map(q => q.userAnswer));
  
  if (taskInfo.value.status === 'finished') {
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
  background-color: #ffffff; // 改为白色，确保缝隙不可见
}

/* 1. 模拟图二样式的导航栏 */
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

/* 进度显示区 */
.info-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 40rpx 0rpx; // 底部 padding 设为 0
  background-color: #ffffff;
  
  .progress-box {
    .label { color: #999; font-size: 26rpx; }
    .value { color: #333; font-weight: bold; font-size: 30rpx; }
  }
  .time-left { color: #ff5e5e; font-size: 28rpx; font-weight: 500; }
}
.question-swiper { 
  flex: 1; 
  background-color: #ffffff;
}
.scroll-v { 
  height: 100%; 
  padding: 0rpx 30rpx 30rpx; // 顶部 padding 设为 0
  box-sizing: border-box; 
  background-color: #ffffff;
}

/* 底部按钮样式优化 */
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