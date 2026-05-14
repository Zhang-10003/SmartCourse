<template>
  <view class="assignment-detail">
    <view @click="close" class="flex items-center text-slate-400 hover:text-indigo-600 mb-6 cursor-pointer transition-colors">
      <text class="text-lg mr-2">←</text>
      <text class="font-semibold">返回列表</text>
    </view>

    <header class="flex justify-between items-end mb-8">
      <view>
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">{{ assignment.title }}</h2>
        <p class="text-indigo-500 mt-2 font-medium text-sm">数据统计与实时排行榜分析</p>
      </view>
      <view class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-slate-200 rounded-xl font-semibold text-slate-600 hover:bg-slate-50 transition-colors text-sm">导出报表</button>
        <button class="px-4 py-2 bg-indigo-600 rounded-xl font-semibold text-white shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-colors text-sm">提醒未交学生</button>
      </view>
    </header>

    <view class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">已提交人数</text>
        <view class="flex items-end justify-between">
          <text class="text-3xl font-black text-slate-800">{{ stats.submittedCount }}</text>
          <text class="text-green-500 text-xs font-bold mb-1">+2% vs 均值</text>
        </view>
      </view>
      <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">平均得分</text>
        <view class="flex items-end justify-between">
          <text class="text-3xl font-black text-indigo-600">{{ stats.avgScore }}</text>
          <view class="w-16 h-2 bg-slate-100 rounded-full overflow-hidden mb-2">
            <view class="w-[78%] h-full bg-indigo-500"></view>
          </view>
        </view>
      </view>
      <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">优秀率 (A)</text>
        <view class="flex items-end justify-between">
          <text class="text-3xl font-black text-green-500">{{ stats.excellentRate }}</text>
          <text class="text-slate-300 text-[10px] mb-1">目标: 15%</text>
        </view>
      </view>
      <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm border-l-4 border-l-rose-500">
        <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">高频错题</text>
        <view class="flex items-end justify-between">
          <text class="text-3xl font-black text-rose-500">{{ stats.hardestQuestion }}</text>
          <text class="text-rose-400 text-xs font-medium mb-1">错误率 42%</text>
        </view>
      </view>
    </view>

    <view class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
      <view class="lg:col-span-1 bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
        <h3 class="text-lg font-bold mb-6 text-slate-800">成绩分布概览</h3>
        <view class="h-[260px] flex flex-col items-center justify-center">
          <view class="relative w-40 h-40">
            <svg viewBox="0 0 100 100" class="w-full h-full">
              <circle cx="50" cy="50" r="40" fill="none" stroke="#f1f5f9" stroke-width="12"/>
              <circle cx="50" cy="50" r="40" fill="none" stroke="#4f46e5" stroke-width="12" stroke-dasharray="100.5 314" stroke-dashoffset="0" transform="rotate(-90 50 50)"/>
              <circle cx="50" cy="50" r="40" fill="none" stroke="#818cf8" stroke-width="12" stroke-dasharray="88 314" stroke-dashoffset="-100.5" transform="rotate(-90 50 50)"/>
              <circle cx="50" cy="50" r="40" fill="none" stroke="#c7d2fe" stroke-width="12" stroke-dasharray="78.5 314" stroke-dashoffset="-188.5" transform="rotate(-90 50 50)"/>
              <circle cx="50" cy="50" r="40" fill="none" stroke="#f8fafc" stroke-width="12" stroke-dasharray="47 314" stroke-dashoffset="-267" transform="rotate(-90 50 50)"/>
            </svg>
          </view>
          <view class="flex justify-center gap-4 mt-4">
            <view class="flex items-center">
              <view class="w-3 h-3 rounded-full bg-indigo-600 mr-1.5"></view>
              <text class="text-xs text-slate-500">优秀</text>
            </view>
            <view class="flex items-center">
              <view class="w-3 h-3 rounded-full bg-indigo-400 mr-1.5"></view>
              <text class="text-xs text-slate-500">良好</text>
            </view>
            <view class="flex items-center">
              <view class="w-3 h-3 rounded-full bg-indigo-200 mr-1.5"></view>
              <text class="text-xs text-slate-500">及格</text>
            </view>
            <view class="flex items-center">
              <view class="w-3 h-3 rounded-full bg-slate-100 border border-slate-200 mr-1.5"></view>
              <text class="text-xs text-slate-500">待加强</text>
            </view>
          </view>
        </view>
      </view>
      <view class="lg:col-span-2 bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
        <view class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-bold text-slate-800">各题目正确率 (%)</h3>
        </view>
        <view class="h-[260px] flex">
          <view class="flex flex-col justify-between py-1 mr-4 text-[10px] text-slate-400">
            <text>100</text>
            <text>80</text>
            <text>60</text>
            <text>40</text>
            <text>20</text>
            <text>0</text>
          </view>
          <view class="flex-1 flex items-end justify-around gap-2">
            <view class="flex flex-col items-center flex-1" v-for="(item, index) in questionScores" :key="index">
              <view 
                class="w-8 rounded-t-md transition-all duration-500"
                :style="{ 
                  height: item.score * 1.8 + 'px', 
                  backgroundColor: item.color
                }"
              ></view>
              <text class="text-xs font-bold text-slate-600 mt-2">{{ item.label }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
      <view class="flex justify-between items-center px-6 py-5 border-b border-slate-50">
        <view class="flex items-center">
          <text class="font-bold text-slate-800">学生提交排行</text>
        </view>
        <view class="flex bg-slate-100 p-1 rounded-lg">
          <view 
            @click="currentSubmitTab = 'submitted'"
            :class="[
              'px-3 py-1 text-xs font-bold rounded-md cursor-pointer transition-all',
              currentSubmitTab === 'submitted' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'
            ]"
          >已提交 ({{ submittedStudents.length }})</view>
          <view 
            @click="currentSubmitTab = 'unsubmitted'"
            :class="[
              'px-3 py-1 text-xs font-bold rounded-md cursor-pointer transition-all',
              currentSubmitTab === 'unsubmitted' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'
            ]"
          >未提交 ({{ unsubmittedStudents.length }})</view>
        </view>
      </view>
      
      <view class="px-6 py-4 border-b border-slate-50">
        <view class="flex text-slate-400 text-xs font-medium">
          <view class="flex-1">学生信息</view>
          <view v-if="currentSubmitTab === 'submitted'" class="flex-1 text-center">提交时间</view>
          <view v-if="currentSubmitTab === 'submitted'" class="flex-1 text-center">状态</view>
          <view v-if="currentSubmitTab === 'submitted'" class="flex-1 text-center">得分</view>
          <view class="flex-1 text-right">操作</view>
        </view>
      </view>
      
      <view v-if="currentSubmitTab === 'submitted'">
        <view 
          v-for="(student, index) in submittedStudents" 
          :key="index"
          :class="[
            'px-6 py-4 hover:bg-slate-50/50 transition-colors',
            index < submittedStudents.length - 1 ? 'border-b border-slate-50' : ''
          ]"
        >
          <view class="flex items-center">
            <view class="flex-1 flex items-center">
              <view class="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 text-white flex items-center justify-center font-bold text-xs mr-2.5">
                {{ student.name.charAt(0) }}
              </view>
              <view>
                <text class="text-sm font-bold text-slate-800">{{ student.name }}</text>
                <text class="text-xs text-slate-400 block">{{ student.className }} · {{ student.id }}</text>
              </view>
            </view>
            <view class="flex-1 text-center text-xs text-slate-500">{{ student.submitTime }}</view>
            <view class="flex-1 flex justify-center">
              <text class="px-2 py-0.5 bg-green-50 text-green-600 rounded-md text-xs font-medium">{{ student.status }}</text>
            </view>
            <view class="flex-1 text-center">
              <text class="text-sm font-bold text-slate-700">{{ student.score }}</text>
            </view>
            <view class="flex-1 flex justify-end">
              <text class="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-md cursor-pointer">查看答案</text>
            </view>
          </view>
        </view>
      </view>
      
      <view v-else>
        <view 
          v-for="(student, index) in unsubmittedStudents" 
          :key="index"
          :class="[
            'px-6 py-4 hover:bg-slate-50/50 transition-colors',
            index < unsubmittedStudents.length - 1 ? 'border-b border-slate-50' : ''
          ]"
        >
          <view class="flex items-center">
            <view class="flex-1 flex items-center">
              <view class="w-8 h-8 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center font-bold text-xs mr-2.5">
                {{ student.name.charAt(0) }}
              </view>
              <view>
                <text class="text-sm font-bold text-slate-800">{{ student.name }}</text>
                <text class="text-xs text-slate-400 block">{{ student.className }} · {{ student.id }}</text>
              </view>
            </view>
            <view class="flex-1"></view>
            <view class="flex-1"></view>
            <view class="flex-1"></view>
            <view class="flex-1 flex justify-end">
              <text class="text-xs font-bold text-orange-600 bg-orange-50 px-3 py-1 rounded-md cursor-pointer">提醒提交</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  assignment: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      deadline: '',
      status: '',
      participants: []
    })
  },
  stats: {
    type: Object,
    default: () => ({
      submittedCount: 57,
      avgScore: 6.3,
      excellentRate: '22%',
      hardestQuestion: 'Q7'
    })
  },
  questionScores: {
    type: Array,
    default: () => []
  },
  submittedStudents: {
    type: Array,
    default: () => []
  },
  unsubmittedStudents: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close']);

const currentSubmitTab = ref('submitted');

const close = () => {
  emit('close');
};
</script>

<style scoped>
.assignment-detail {
  width: 100%;
}
</style>
