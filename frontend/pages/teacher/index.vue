<template>
  <view class="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
    
    <aside class="w-20 lg:w-64 bg-white/70 backdrop-blur-xl border-r border-slate-200 flex flex-col py-8 z-10 transition-all">
      <view class="mb-12 font-bold text-xl text-indigo-600 tracking-tighter text-center">SmartCourse.</view>
      <nav class="flex-1 px-4 space-y-3">
        <view 
          @click="currentTab = 'design'" 
          :class="currentTab === 'design' ? 'bg-indigo-50 text-indigo-600 shadow-sm' : 'text-slate-400 hover:bg-slate-50'"
          class="w-full flex items-center justify-center lg:justify-start space-x-3 p-3 rounded-2xl transition-all cursor-pointer font-semibold"
        >
          <text class="text-xl">🏠</text>
          <text class="hidden lg:block">作业工作台</text>
        </view>
        <view 
          @click="currentTab = 'list'" 
          :class="currentTab === 'list' ? 'bg-indigo-50 text-indigo-600 shadow-sm' : 'text-slate-400 hover:bg-slate-50'"
          class="w-full flex items-center justify-center lg:justify-start space-x-3 p-3 rounded-2xl transition-all cursor-pointer font-semibold"
        >
          <text class="text-xl">📝</text>
          <text class="hidden lg:block">我的作业</text>
        </view>
      </nav>
    </aside>

    <main class="flex-1 overflow-y-auto p-4 lg:p-8 pb-64 relative no-scrollbar">
      <view v-if="currentTab === 'design'" class="animate-in fade-in duration-500">
        <header class="flex flex-col lg:flex-row lg:justify-between lg:items-end mb-10 gap-4">
          <view>
            <h1 class="text-3xl font-bold text-slate-900">我的作业流</h1>
            <p class="text-slate-500 mt-2">拖拽左侧题型至画布，已在画布的题型可直接拖动位置。</p>
          </view>
          <view class="flex gap-4">
            <button class="bg-white border border-slate-200 px-6 py-3 rounded-2xl font-semibold shadow-sm hover:bg-slate-50 transition-all">发布作业</button>
            <button @click="saveWorkflow" class="bg-indigo-600 text-white px-6 py-3 rounded-2xl font-semibold shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all">保存工作流</button>
          </view>
        </header>

        <h2 class="text-lg font-bold mb-6 flex items-center">
            <span class="w-2 h-2 bg-indigo-600 rounded-full mr-2"></span>
            可视化题型蓝图 (Node Editor)
        </h2>

        <view class="flex flex-col lg:flex-row gap-6">
          <view class="w-full lg:w-48 flex flex-row lg:flex-col gap-3 overflow-x-auto lg:overflow-x-visible pb-4 lg:pb-0">
            <view 
              v-for="item in toolset" :key="item.type"
              draggable="true"
              @dragstart="onDragStart($event, item)"
              class="flex-shrink-0 p-4 bg-white border border-slate-200 rounded-2xl cursor-move hover:border-indigo-400 hover:shadow-md transition-all flex items-center gap-3"
            >
              <view :class="item.color" class="w-3 h-3 rounded-full shadow-sm"></view>
              <text class="text-sm font-semibold text-slate-700">{{ item.type }}</text>
            </view>
          </view>

          <view 
            class="flex-1 min-h-[600px] rounded-[32px] node-canvas-bg border-2 border-dashed border-slate-200 relative overflow-hidden"
            @dragover.prevent
            @drop="onDrop"
          >
            <view 
              v-for="(node, index) in nodes" :key="node.id"
              class="node-element absolute glass-panel p-5 rounded-[24px] cursor-move z-10 border border-white shadow-lg select-none"
              :style="{ 
                left: node.x + 'px', 
                top: node.y + 'px', 
                minWidth: '200px',
                willChange: (isUpdating || draggingNodeIndex === index) ? 'auto' : 'left, top',
                transition: (isUpdating || draggingNodeIndex === index) ? 'none' : 'left 0.2s cubic-bezier(0.4, 0, 0.2, 1), top 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s, box-shadow 0.2s' 
              }"
              @mousedown.stop="onNodeMouseDown($event, index)"
              @click.stop="handleNodeClick(node, index)"
            >
              <view class="flex justify-between items-center mb-4 pointer-events-none">
                <text class="text-[10px] font-bold text-slate-400 tracking-widest uppercase">NODE_{{ index + 1 }}</text>
                <view 
                  @click.stop="removeNode(index)" 
                  :class="[node.color, 'pointer-events-auto']" 
                  class="w-5 h-5 rounded-full shadow-sm flex items-center justify-center cursor-pointer hover:scale-110 active:scale-90 transition-transform"
                >
                  <text class="text-white text-[12px] font-bold" style="line-height: 1;">×</text>
                </view>
              </view>
              <view class="font-bold text-slate-800 mb-3 pointer-events-none">{{ node.type }}</view>
              
              <view class="space-y-2 pointer-events-none">
                <view class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <view :class="node.color" class="w-1/2 h-full opacity-30"></view>
                </view>
                <view class="w-2/3 h-1.5 bg-slate-100 rounded-full"></view>
              </view>
              
              <view class="anchor-left absolute -left-2 top-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-slate-200 rounded-full transition-colors"></view>
              <view class="anchor-right absolute -right-2 top-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-indigo-400 rounded-full transition-colors"></view>
            </view>

            <view v-if="nodes.length === 0" class="absolute inset-0 flex flex-col items-center justify-center text-slate-400 pointer-events-none">
              <view class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                <text class="text-2xl">＋</text>
              </view>
              <text class="font-medium">将题型拖拽到此处开始设计</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else class="relative min-h-full">
        <view :class="currentView === 'list' ? 'view-active' : 'view-hidden'" class="view-transition absolute inset-0 p-4 lg:p-8">
          <header class="mb-10">
            <h1 class="text-3xl font-bold text-slate-900">作业管理中心</h1>
            <p class="text-slate-500 mt-2">在这里追踪所有已发布作业的收集情况与数据分析。</p>
          </header>

          <view class="space-y-12">
              <section>
                  <view class="flex items-center gap-3 mb-6">
                      <view class="w-1 h-6 bg-indigo-600 rounded-full"></view>
                      <text class="text-lg font-bold text-slate-800">今天发布</text>
                  </view>
                  <view class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      <AssignmentCard 
                        title="计算机网络周测 - TCP原理" 
                        deadline="截止: 05-10 18:00" 
                        status="进行中"
                        :participants="[
                          { initial: 'A', bgClass: 'bg-indigo-100 text-indigo-600' },
                          { initial: 'B', bgClass: 'bg-emerald-100 text-emerald-600' },
                          { initial: '+12', bgClass: 'bg-slate-100 text-slate-400' }
                        ]"
                        @detail-click="openAssignmentDetail('计算机网络周测 - TCP原理', '截止: 05-10 18:00', '进行中', [])"
                      />
                      <AssignmentCard 
                        title="软件工程作业 - UML建模" 
                        deadline="截止: 05-12 23:59" 
                        status="进行中"
                        :participants="[
                          { initial: 'C', bgClass: 'bg-purple-100 text-purple-600' },
                          { initial: 'D', bgClass: 'bg-pink-100 text-pink-600' },
                          { initial: '+8', bgClass: 'bg-slate-100 text-slate-400' }
                        ]"
                        @detail-click="openAssignmentDetail('软件工程作业 - UML建模', '截止: 05-12 23:59', '进行中', [])"
                      />
                      <AssignmentCard 
                        title="数据库系统设计报告" 
                        deadline="截止: 05-15 18:00" 
                        status="进行中"
                        :participants="[
                          { initial: 'E', bgClass: 'bg-orange-100 text-orange-600' },
                          { initial: 'F', bgClass: 'bg-cyan-100 text-cyan-600' },
                          { initial: '+15', bgClass: 'bg-slate-100 text-slate-400' }
                        ]"
                        @detail-click="openAssignmentDetail('数据库系统设计报告', '截止: 05-15 18:00', '进行中', [])"
                      />
                  </view>
              </section>

              <section>
                  <view class="flex items-center gap-3 mb-6">
                      <view class="w-1 h-6 bg-slate-300 rounded-full"></view>
                      <text class="text-lg font-bold text-slate-800">近七天</text>
                  </view>
                  <view class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 opacity-80 hover:opacity-100 transition-opacity">
                      <AssignmentCard 
                        title="操作系统同步互斥习题" 
                        deadline="截止: 04-15 23:59" 
                        status="已截止"
                        @ranking-click="openAssignmentDetail('操作系统同步互斥习题', '截止: 04-15 23:59', '已截止', [])"
                      />
                  </view>
              </section>
          </view>
        </view>

        <view :class="currentView === 'detail' ? 'view-active' : 'view-hidden'" class="view-transition p-4 lg:px-24 lg:py-4">
          <view @click="closeDetailView" class="flex items-center text-slate-400 hover:text-indigo-600 mb-6 cursor-pointer transition-colors">
            <text class="text-lg mr-2">←</text>
            <text class="font-semibold">返回列表</text>
          </view>

          <header class="flex justify-between items-end mb-8">
            <view>
              <h2 class="text-2xl font-bold text-slate-800 tracking-tight">{{ selectedAssignment.title }}</h2>
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
                <text class="text-3xl font-black text-slate-800">57</text>
                <text class="text-green-500 text-xs font-bold mb-1">+2% vs 均值</text>
              </view>
            </view>
            <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
              <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">平均得分</text>
              <view class="flex items-end justify-between">
                <text class="text-3xl font-black text-indigo-600">6.3</text>
                <view class="w-16 h-2 bg-slate-100 rounded-full overflow-hidden mb-2">
                  <view class="w-[78%] h-full bg-indigo-500"></view>
                </view>
              </view>
            </view>
            <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
              <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">优秀率 (A)</text>
              <view class="flex items-end justify-between">
                <text class="text-3xl font-black text-green-500">22%</text>
                <text class="text-slate-300 text-[10px] mb-1">目标: 15%</text>
              </view>
            </view>
            <view class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm border-l-4 border-l-rose-500">
              <text class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 block">高频错题</text>
              <view class="flex items-end justify-between">
                <text class="text-3xl font-black text-rose-500">Q7</text>
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
                >已提交 (57)</view>
                <view 
                  @click="currentSubmitTab = 'unsubmitted'"
                  :class="[
                    'px-3 py-1 text-xs font-bold rounded-md cursor-pointer transition-all',
                    currentSubmitTab === 'unsubmitted' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'
                  ]"
                >未提交 (3)</view>
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
        
        <view class="h-2"></view>
        </view>
      </view>
    </main>

    <view 
      v-show="drawer.show" 
      class="fixed inset-0 z-20"
      :class="drawer.show ? 'pointer-events-auto' : 'pointer-events-none'"
    >
      <view @click="drawer.show = false" class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"></view>
      <view 
        class="absolute top-0 right-0 h-full w-full md:w-[600px] bg-white shadow-2xl transition-transform duration-500 flex flex-col"
        :style="{ transform: drawer.show ? 'translateX(0)' : 'translateX(100%)' }"
      >
        <view class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <view class="flex-1">
            <h2 class="text-xl font-bold text-slate-900">{{ drawer.title }}</h2>
            <p class="text-slate-500 text-xs mt-1">SmartCourse 配置引擎</p>
          </view>
          <view @click="closeDrawer" class="ml-4 text-slate-300 hover:text-slate-500 transition-colors text-xl cursor-pointer">×</view>
        </view>

        <view class="flex-1 overflow-y-auto p-8">
          <view v-if="drawer.editingNode.type === '单选题'">
            <QuestionChoiceEditor 
              :index="drawer.currentIndex + 1"
              :modelValue="drawer.editingNode.data"
              :answer="drawer.editingNode.answer || 0"
              @update:modelValue="(val) => drawer.editingNode.data = val"
              @update:answer="(val) => drawer.editingNode.answer = val"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '多选题'">
            <QuestionMultipleChoiceEditor 
              :index="drawer.currentIndex + 1"
              :modelValue="drawer.editingNode.data"
              :answer="drawer.editingNode.answer || []"
              @update:modelValue="(val) => drawer.editingNode.data = val"
              @update:answer="(val) => drawer.editingNode.answer = val"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '判断题'">
            <QuestionTrueFalseEditor 
              :index="drawer.currentIndex + 1"
              v-model="drawer.editingNode.data"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '代码填空'">
            <QuestionCodeFillEditor 
              :index="drawer.currentIndex + 1"
              :modelValue="drawer.editingNode.data"
              @update:modelValue="(val) => drawer.editingNode.data = val"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '填空题'">
            <QuestionFillBlankEditor 
              :index="drawer.currentIndex + 1"
              v-model="drawer.editingNode.data"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '匹配题'">
            <QuestionMatchingEditor 
              :index="drawer.currentIndex + 1"
              :modelValue="drawer.editingNode.data"
              @update:modelValue="(val) => drawer.editingNode.data = val"
            />
          </view>

          <view v-else-if="drawer.editingNode.type === '简答题'">
            <QuestionShortAnswerEditor 
              :index="drawer.currentIndex + 1"
              v-model="drawer.editingNode.data"
            />
          </view>
        </view>

        <view class="p-8 border-t border-slate-100 flex gap-4">
          <button @click="saveNode" class="flex-1 bg-indigo-600 text-white py-4 rounded-2xl font-bold hover:shadow-lg transition-all">确认并保存</button>
          <button @click="deleteNode" class="px-8 py-4 bg-rose-50 text-rose-600 rounded-2xl font-bold hover:bg-rose-100 transition-all">删除</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue';
import QuestionChoiceEditor from '@/components/QuestionChoiceEditor.vue';
import QuestionMultipleChoiceEditor from '@/components/QuestionMultipleChoiceEditor.vue';
import QuestionTrueFalseEditor from '@/components/QuestionTrueFalseEditor.vue';
import QuestionCodeFillEditor from '@/components/QuestionCodeFillEditor.vue';
import QuestionFillBlankEditor from '@/components/QuestionFillBlankEditor.vue';
import QuestionMatchingEditor from '@/components/QuestionMatchingEditor.vue';
import QuestionShortAnswerEditor from '@/components/QuestionShortAnswerEditor.vue';
import AssignmentCard from '@/components/AssignmentCard.vue';

const currentTab = ref('design');
const nodes = ref([]);
const isUpdating = ref(false); 
const currentView = ref('list');
const selectedAssignment = reactive({
  title: '',
  deadline: '',
  status: '',
  participants: []
});

const drawer = reactive({
  show: false,
  title: '',
  editingNode: { 
    type: '', 
    data: {}, 
    answer: null,
    id: '',
    x: 0,
    y: 0,
    color: ''
  },
  currentIndex: -1
});

const toolset = [
  { type: '单选题', color: 'bg-blue-500' },
  { type: '多选题', color: 'bg-purple-500' },
  { type: '代码填空', color: 'bg-emerald-500' },
  { type: '匹配题', color: 'bg-orange-500' },
  { type: '判断题', color: 'bg-rose-500' },
  { type: '填空题', color: 'bg-cyan-500' },
  { type: '简答题', color: 'bg-indigo-500' }
];

const questionScores = [
  { label: 'Q1', score: 85, color: '#6366f1' },
  { label: 'Q2', score: 72, color: '#818cf8' },
  { label: 'Q3', score: 92, color: '#6366f1' },
  { label: 'Q4', score: 65, color: '#a5b4fc' },
  { label: 'Q5', score: 48, color: '#c7d2fe' },
  { label: 'Q6', score: 88, color: '#6366f1' },
  { label: 'Q7', score: 55, color: '#d4d4d8' }
];

const currentSubmitTab = ref('submitted');

const submittedStudents = [
  { name: '张敬有', className: '大数据2403', id: '2024001', submitTime: '今天 14:22', status: '已自动阅卷', score: '8.0' },
  { name: '符式乾', className: '大数据2404', id: '2024042', submitTime: '今天 12:05', status: '已自动阅卷', score: '8.0' }
];

const unsubmittedStudents = [
  { name: '李明', className: '大数据2403', id: '2024002' },
  { name: '王华', className: '大数据2403', id: '2024003' },
  { name: '刘洋', className: '大数据2404', id: '2024043' }
];

let draggingItem = null;
const mousePos = { x: 0, y: 0 };
const draggingNodeIndex = ref(-1);
let offset = { x: 0, y: 0 };
let canvasRect = null; 
let startPoint = { x: 0, y: 0 };
let hasMoved = false;

const updateMousePos = (e) => {
  mousePos.x = e.pageX || e.clientX;
  mousePos.y = e.pageY || e.clientY;

  if (draggingNodeIndex.value !== -1) {
    const moveX = Math.abs(mousePos.x - startPoint.x);
    const moveY = Math.abs(mousePos.y - startPoint.y);
    if (moveX > 5 || moveY > 5) {
      hasMoved = true;
    }

    if (!canvasRect) return;
    nodes.value[draggingNodeIndex.value].x = mousePos.x - canvasRect.left - offset.x;
    nodes.value[draggingNodeIndex.value].y = mousePos.y - canvasRect.top - offset.y;
  }
};

const stopInternalDrag = () => {
  setTimeout(() => {
    draggingNodeIndex.value = -1;
    canvasRect = null;
  }, 10);
};

onMounted(() => {
  window.addEventListener('mousemove', updateMousePos, true);
  window.addEventListener('dragover', updateMousePos, true);
  window.addEventListener('mouseup', stopInternalDrag);
});

onUnmounted(() => {
  window.removeEventListener('mousemove', updateMousePos, true);
  window.removeEventListener('dragover', updateMousePos, true);
  window.removeEventListener('mouseup', stopInternalDrag);
});

const onDragStart = (e, item) => {
  draggingItem = item;
};

const onDrop = (e) => {
  e.preventDefault();
  if (!draggingItem) return;
  const canvasElement = document.querySelector('.node-canvas-bg');
  const rect = canvasElement.getBoundingClientRect();
  const uniqueId = `node_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  const defaultData = getDefaultQuestionData(draggingItem.type);
  
  nodes.value.push({
    id: uniqueId,
    type: draggingItem.type,
    color: draggingItem.color,
    x: Math.max(0, mousePos.x - rect.left - 100),
    y: Math.max(0, mousePos.y - rect.top - 40),
    data: defaultData,
    answer: null
  });
  draggingItem = null;
};

const getDefaultQuestionData = (type) => {
  const templates = {
    '单选题': {
      title: '请输入单选题题目内容...',
      options: ['选项 A', '选项 B', '选项 C', '选项 D'],
      isMultiple: false
    },
    '多选题': {
      title: '请输入多选题题目内容...',
      options: ['选项 A', '选项 B', '选项 C', '选项 D'],
      isMultiple: true
    },
    '判断题': {
      title: '请输入判断题题目内容...'
    },
    '代码填空': {
      title: '请输入代码填空题题目内容...',
      code: 'MOV AX, ????\nADD BX, ????\nINT 21H',
      fields: [{ value: '' }, { value: '' }]
    },
    '填空题': {
      title: '计算机基础知识填空',
      content: '在计算机中，CPU由 ???? 和 ???? 两部分组成。内存的主要作用是 ????。',
      correctAnswers: ['运算器', '控制器', '临时存储数据']
    },
    '匹配题': {
      title: '请输入匹配题的整体题目描述或指导语...',
      pairs: [
        { left: '', right: '' },
        { left: '', right: '' },
        { left: '', right: '' }
      ],
      analysis: ''
    },
    '简答题': {
      title: '请输入简答题题目内容...'
    }
  };
  return templates[type] || {};
};

const onNodeMouseDown = (e, index) => {
  startPoint = { x: e.pageX || e.clientX, y: e.pageY || e.clientY };
  hasMoved = false;

  const node = nodes.value[index];
  const canvasElement = document.querySelector('.node-canvas-bg');
  canvasRect = canvasElement.getBoundingClientRect();
  
  offset.x = (e.clientX - canvasRect.left) - node.x;
  offset.y = (e.clientY - canvasRect.top) - node.y;
  
  draggingNodeIndex.value = index;
};

const handleNodeClick = (node, index) => {
  if (hasMoved) {
    hasMoved = false;
    return;
  }
  openEditor(node, index);
};

const removeNode = (index) => {
  isUpdating.value = true;
  
  requestAnimationFrame(() => {
    nodes.value.splice(index, 1);
    
    nextTick(() => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          isUpdating.value = false;
        });
      });
    });
  });
};

const openEditor = (node, index) => {
  drawer.title = `编辑：${node.type} (#${index + 1})`;
  drawer.editingNode = { ...node };
  drawer.currentIndex = index;
  drawer.show = true;
};

const saveNode = () => {
  if (drawer.currentIndex !== -1) {
    nodes.value[drawer.currentIndex] = { ...drawer.editingNode };
    closeDrawer();
  }
};

const deleteNode = () => {
  if (drawer.currentIndex !== -1) {
    removeNode(drawer.currentIndex);
    closeDrawer();
  }
};

const closeDrawer = () => {
  drawer.show = false;
  drawer.currentIndex = -1;
};

const saveWorkflow = () => {
  uni.showToast({ title: '保存成功', icon: 'success' });
};

const openAssignmentDetail = (title, deadline, status, participants) => {
  selectedAssignment.title = title;
  selectedAssignment.deadline = deadline;
  selectedAssignment.status = status;
  selectedAssignment.participants = participants;
  currentView.value = 'detail';
};

const closeDetailView = () => {
  currentView.value = 'list';
};
</script>

<style scoped>
.node-canvas-bg {
  background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
  background-size: 24px 24px;
}
.glass-panel {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px);
}
.node-element {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s;
}
.node-element:active { cursor: grabbing; }
.no-scrollbar::-webkit-scrollbar { display: none; }
.animate-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.select-none { user-select: none; }

.view-transition {
  transition: all 0.5s ease-in-out;
}
.view-hidden {
  opacity: 0;
  transform: translateY(20px);
  pointer-events: none;
  height: 0;
  overflow: hidden;
}
.view-active {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
</style>