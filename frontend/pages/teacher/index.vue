<template>
  <view class="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
    <view 
      class="fixed top-0 left-0 right-0 z-50 flex justify-center pointer-events-none"
      :class="toast.show ? 'opacity-100' : 'opacity-0'"
      style="transition: opacity 0.3s ease;"
    >
      <view 
        class="bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg mt-4 flex items-center gap-2"
        :style="toast.show ? 'transform: translateY(0);' : 'transform: translateY(-20px);'"
      >
        <svg v-if="toast.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
        <svg v-else-if="toast.type === 'error'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
        <span class="text-sm font-medium">{{ toast.message }}</span>
      </view>
    </view>
    
    <aside class="w-20 lg:w-64 bg-white/70 backdrop-blur-xl border-r border-slate-200 flex flex-col py-8 z-10 transition-all">
      <view class="mb-12 font-bold text-xl text-indigo-600 tracking-tighter text-center">SmartCourse</view>
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

    <main class="flex-1 overflow-y-auto p-4 lg:p-8 pb-4 relative no-scrollbar">
      <view v-if="currentTab === 'design'" class="animate-in fade-in duration-500 flex flex-col h-full">
        <header class="flex flex-col lg:flex-row lg:justify-between lg:items-end mb-6 gap-4 shrink-0">
          <view>
            <h1 class="text-3xl font-bold text-slate-900">我的作业流</h1>
            <p class="text-slate-500 mt-2">拖拽左侧题型至画布，已在画布的题型可直接拖动位置。</p>
          </view>
          <view class="flex gap-4">
            <button @click="openRAGModal" class="bg-white border border-slate-200 px-6 py-3 rounded-2xl font-semibold shadow-sm hover:bg-slate-50 transition-all">RAG知识库管理</button>
            <button @click="openShareModal" class="bg-white border border-slate-200 px-6 py-3 rounded-2xl font-semibold shadow-sm hover:bg-slate-50 transition-all">发布作业</button>
            <button @click="saveWorkflow" class="bg-indigo-600 text-white px-6 py-3 rounded-2xl font-semibold shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all">保存工作流</button>
          </view>
        </header>

        <h2 class="text-lg font-bold mb-4 flex items-center shrink-0">
            <span class="w-2 h-2 bg-indigo-600 rounded-full mr-2"></span>
            可视化题型蓝图 (Node Editor)
        </h2>

        <view class="flex flex-col lg:flex-row gap-6 flex-1 min-h-0">
          <view class="w-full lg:w-48 flex flex-row lg:flex-col gap-3 overflow-x-auto lg:overflow-x-visible pb-4 lg:pb-0 shrink-0">
            <view class="flex-shrink-0 w-full lg:w-auto">
              <text class="text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-2 block">Knowledge Source</text>
              <view 
                draggable="true"
                @dragstart="onDragStart($event, { type: '教材/课件', color: 'bg-amber-400' })"
                @click="showResourceLibrary = true"
                class="flex-shrink-0 p-4 bg-white border-2 border-amber-300 rounded-2xl cursor-pointer hover:border-amber-500 hover:shadow-md transition-all flex items-center gap-3"
              >
                <view class="w-3 h-3 rounded-full bg-amber-400 shadow-sm"></view>
                <text class="text-sm font-semibold text-amber-700">教材/课件</text>
              </view>
            </view>
            
            <text class="text-[10px] font-bold text-slate-400 tracking-widest uppercase mb-2 block w-full lg:w-auto mt-4 lg:mt-6">Question Types</text>
            
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
            class="flex-1 min-h-0 rounded-[32px] node-canvas-bg border-2 border-dashed border-slate-200 relative overflow-hidden"
            @dragover.prevent
            @drop="onDrop"
          >
            <view class="absolute top-6 left-1/2 -translate-x-1/2 px-6 py-3 bg-white/80 backdrop-blur-lg rounded-2xl border border-slate-100 shadow-lg flex items-center gap-3 pointer-events-none z-10">
              <view class="flex h-2 w-2 relative">
                <view class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></view>
                <view class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></view>
              </view>
              <text class="text-sm text-slate-600 font-medium">操作指引：拖拽左侧题型到画布 | 点击教材圆点→题型圆点连线 | 右键连线删除</text>
            </view>
            
            <view 
              v-for="(node, index) in nodes" :key="node.id"
              :class="[
                'node-element absolute glass-panel rounded-[24px] cursor-move select-none flex flex-col transition-all duration-300',
                node.isExpanded 
                  ? 'z-30 shadow-2xl border-indigo-200/60' 
                  : 'z-10 shadow-lg border border-white'
              ]"
              :style="{ 
                left: node.x + 'px', 
                top: node.y + 'px', 
                width: node.isExpanded ? '600px' : '240px',
                height: node.isExpanded ? 'auto' : '145px',
                willChange: (isUpdating || draggingNodeIndex === index) ? 'auto' : 'left, top',
                transition: (isUpdating || draggingNodeIndex === index) 
                  ? 'none' 
                  : 'left 0.2s cubic-bezier(0.4, 0, 0.2, 1), top 0.2s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1), height 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s, border-color 0.3s' 
              }"
              @mousedown.stop="onNodeMouseDown($event, index)"
              @click.stop="handleNodeClick(node, index)"
            >
              <view 
                v-if="node.type !== '教材/课件'" 
                class="port port-in" 
                :class="{ 'active': selectedPortId === node.id + '-in' }"
                :data-port-id="node.id" 
                data-port-type="in"
                @click.stop="handlePortClick(node.id, 'in')"
              ></view>
              <view v-if="!node.isExpanded" class="mini-view p-5 h-full flex flex-col justify-between">
                <view class="flex justify-between items-center">
                  <text class="text-[10px] font-bold text-slate-400 tracking-widest uppercase">{{ node.type === '教材/课件' ? '📁 教材' : 'Q' + getQuestionIndex(index) }}</text>
                  <view 
                    @click.stop="removeNode(index)" 
                    :class="[node.color, 'pointer-events-auto']" 
                    class="w-5 h-5 rounded-full shadow-sm flex items-center justify-center cursor-pointer hover:scale-110 active:scale-90 transition-transform"
                  >
                    <text class="text-white text-[12px] font-bold" style="line-height: 1;">×</text>
                  </view>
                </view>
                <view class="font-bold text-slate-800 mb-3">{{ node.type }}</view>
                
                <view class="space-y-2">
                  <view class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <view :class="node.color" class="w-1/2 h-full opacity-30"></view>
                  </view>
                  <view class="w-2/3 h-1.5 bg-slate-100 rounded-full"></view>
                </view>
              </view>

              <view v-else class="expanded-view flex flex-col">
                <view class="drag-handle-expanded p-4 cursor-move select-none flex items-center justify-between border-b border-dashed border-slate-100 bg-slate-50/40">
                  <view class="flex items-center gap-2">
                    <span :class="[node.color, 'px-2.5 py-1 text-xs font-bold rounded-lg text-white']">{{ node.type }}</span>
                    <span v-if="node.type !== '教材/课件'" class="text-xs font-bold text-slate-400">{{ String(getQuestionIndex(index)).padStart(2, '0') }}.</span>
                  </view>
                  <button 
                    @click.stop="shrinkNode(index)" 
                    class="px-6 py-2 bg-slate-700 text-white hover:bg-slate-800 text-sm font-bold rounded-xl transition-all"
                  >
                    收起
                  </button>
                  <view class="flex items-center gap-3">
                    <view 
                      @click.stop="generateQuestionWithAI(index)" 
                      class="text-indigo-600 hover:text-indigo-700 text-sm font-medium cursor-pointer transition-colors flex items-center gap-1"
                    >
                      <span>AI智能生成</span>
                    </view>
                    <view @click.stop="removeNode(index)" class="text-slate-400 hover:text-rose-500 text-lg cursor-pointer">×</view>
                  </view>
                </view>

                <view class="flex-1 overflow-y-auto p-4 scrollbar-hide">
                  <view v-if="node.type === '单选题'">
                    <QuestionChoiceEditor 
                      :index="getQuestionIndex(index)"
                      :modelValue="node.data"
                      :answer="node.answer || 0"
                      @update:modelValue="(val) => { node.data = val }"
                      @update:answer="(val) => { node.answer = val }"
                    />
                  </view>
                  <view v-else-if="node.type === '多选题'">
                    <QuestionMultipleChoiceEditor 
                      :index="getQuestionIndex(index)"
                      :modelValue="node.data"
                      :answer="node.answer || []"
                      @update:modelValue="(val) => { node.data = val }"
                      @update:answer="(val) => { node.answer = val }"
                    />
                  </view>
                  <view v-else-if="node.type === '判断题'">
                    <QuestionTrueFalseEditor 
                      :index="getQuestionIndex(index)"
                      v-model="node.data"
                    />
                  </view>
                  <view v-else-if="node.type === '代码填空'">
                    <QuestionCodeFillEditor 
                      :index="getQuestionIndex(index)"
                      :modelValue="node.data"
                      @update:modelValue="(val) => { node.data = val }"
                    />
                  </view>
                  <view v-else-if="node.type === '填空题'">
                    <QuestionFillBlankEditor 
                      :index="getQuestionIndex(index)"
                      v-model="node.data"
                    />
                  </view>
                  <view v-else-if="node.type === '匹配题'">
                    <QuestionMatchingEditor 
                      :index="getQuestionIndex(index)"
                      :modelValue="node.data"
                      @update:modelValue="(val) => { node.data = val }"
                    />
                  </view>
                  <view v-else-if="node.type === '简答题'">
                    <QuestionShortAnswerEditor 
                      :index="getQuestionIndex(index)"
                      v-model="node.data"
                    />
                  </view>
                </view>
              </view>
              <view 
                v-if="node.type === '教材/课件'" 
                class="port port-out" 
                :class="{ 'active': selectedPortId === node.id + '-out' }"
                :data-port-id="node.id" 
                data-port-type="out"
                @click.stop="handlePortClick(node.id, 'out')"
              ></view>
            </view>

            <svg id="svg-layer" class="absolute inset-0 w-full h-full pointer-events-none" style="z-index: 5; min-height: 1000px; min-width: 1000px;"></svg>

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
                  <view v-if="assignmentList.today.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      <AssignmentCard 
                        v-for="(assignment, index) in assignmentList.today" 
                        :key="assignment.assignment_id"
                        :title="assignment.title" 
                        :deadline="assignment.deadline" 
                        :status="assignment.status"
                        :participants="fixedParticipants"
                        :assignmentId="assignment.assignment_id"
                        @detail-click="openAssignmentDetail(assignment.title, assignment.deadline, assignment.status, [], assignment.share_code, assignment.deadline_ts, assignment.assignment_id)"
                        @report-click="handleReportClick(assignment)"
                        @close-click="handleCloseClick(assignment.assignment_id)"
                      />
                  </view>
                  <view v-else class="text-center py-10 text-slate-400">
                      <text class="text-lg">暂无作业</text>
                  </view>
              </section>

              <section>
                  <view class="flex items-center gap-3 mb-6">
                      <view class="w-1 h-6 bg-slate-300 rounded-full"></view>
                      <text class="text-lg font-bold text-slate-800">近七天</text>
                  </view>
                  <view v-if="assignmentList.recent.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 opacity-80 hover:opacity-100 transition-opacity">
                      <AssignmentCard 
                        v-for="(assignment, index) in assignmentList.recent" 
                        :key="assignment.assignment_id"
                        :title="assignment.title" 
                        :deadline="assignment.deadline" 
                        :status="assignment.status"
                        :assignmentId="assignment.assignment_id"
                        @detail-click="openAssignmentDetail(assignment.title, assignment.deadline, assignment.status, [], assignment.share_code, assignment.deadline_ts, assignment.assignment_id)"
                        @report-click="handleReportClick(assignment)"
                        @close-click="handleCloseClick(assignment.assignment_id)"
                      />
                  </view>
                  <view v-else class="text-center py-10 text-slate-400">
                      <text class="text-lg">暂无作业</text>
                  </view>
              </section>
          </view>
        </view>

        <view :class="currentView === 'detail' ? 'view-active' : 'view-hidden'" class="view-transition p-4 lg:px-24 lg:py-4">
          <AssignmentDetail
            :assignment="selectedAssignment"
            :stats="assignmentStats"
            :questionScores="questionScores"
            :submittedStudents="submittedStudents"
            :unsubmittedStudents="unsubmittedStudents"
            @close="closeDetailView"
            @deadline-click="handleCloseClick(selectedAssignment.assignment_id)"
          />
        </view>


      </view>
    </main>

    <view v-if="aiModal.show" class="fixed inset-0 z-30 flex items-center justify-center p-4">
      <view @click="closeAIModal" class="absolute inset-0 bg-black/40 backdrop-blur-sm"></view>
      <view class="ai-modal-card relative">
        <view class="ai-modal-header">
          <h3 class="flex items-center gap-2">
            <text>✨</text>
            <span>智能出题</span>
            <span class="rag-badge">已关联知识库</span>
          </h3>
        </view>

        <view class="ai-modal-body">
          <view class="form-group">
            <label class="form-label">你想要生成什么样的题目？</label>
            <textarea 
              v-model="aiModal.prompt"
              class="input-control" 
              rows="4" 
              placeholder="例如：出一道关于TCP特点的题目..."
            ></textarea>
          </view>

          <view class="options-row">
            <div class="option-item">
              <label class="form-label">题目类型</label>
              <select v-model="aiModal.questionType" class="input-control" disabled>
                <option v-for="type in questionTypes" :key="type.value" :value="type.value">
                  {{ type.label }}
                </option>
              </select>
            </div>
            <div class="option-item">
              <label class="form-label">难度设定</label>
              <select v-model="aiModal.difficulty" class="input-control">
                <option>简单</option>
                <option>中等</option>
                <option>困难</option>
              </select>
            </div>
          </view>
        </view>

        <view class="ai-modal-footer">
          <button class="btn btn-cancel" @click="closeAIModal">取消</button>
          <button class="btn btn-confirm" @click="generateQuestion">开始生成</button>
        </view>
      </view>
    </view>

    <!-- 加载动画 -->
    <view v-if="loadingState.show" class="fixed inset-0 z-40 flex items-center justify-center p-4">
      <view class="absolute inset-0 bg-black/30 backdrop-blur-sm"></view>
      <view class="bg-white rounded-2xl p-8 shadow-2xl flex flex-col items-center gap-4">
        <view class="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></view>
        <span class="text-indigo-900 font-medium text-lg">正在生成题目...</span>
      </view>
    </view>

    <!-- 学情分析报告弹窗 -->
    <view v-if="reportModal.show" class="fixed inset-0 z-30 flex items-center justify-center p-4">
      <view @click="closeReportModal" class="absolute inset-0" style="background-color: rgba(15, 23, 42, 0.3); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"></view>
      <view class="relative" style="background: rgba(255, 255, 255, 0.95); border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 32px; padding: 40px; width: 90vw; max-width: 1160px; box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.08);">
        <button class="modal-close-btn absolute top-6 right-6 w-9 h-9 rounded-full border-0 bg-black/5 text-gray-500 cursor-pointer flex items-center justify-center text-2xl leading-none transition-all hover:bg-black/8 hover:text-gray-900" @click="closeReportModal">×</button>

        <!-- 标题和分隔线 -->
        <view class="mb-6">
          <view class="text-2xl font-bold text-slate-900 mb-3" style="color: #3b82f6;">作业报告</view>
          <view style="height: 4px; width: 120px; background-color: #3b82f6; border-radius: 2px;"></view>
        </view>

        <view v-if="reportModal.state === 'generating'" class="report-grid" style="display: grid; grid-template-columns: 1.1fr 0.9fr; grid-template-rows: 1fr; gap: 40px; text-align: left;">
          <!-- 左侧面板加载状态 -->
          <view class="panel-left flex flex-col h-full">
            <view class="card-title text-lg font-semibold mb-6 flex items-center gap-2.5" style="color: #0f172a;">
              <text class="title-icon inline-block w-4.5 h-4.5 rounded" style="background-color: #3b82f6; clip-path: polygon(0 100%, 30% 40%, 60% 70%, 100% 0, 100% 100%);"></text>
              错误知识点分布
            </view>
            <view class="card-body flex-1 flex flex-col justify-between">
              <text class="text-lg text-slate-500 py-2">LLM生成中...</text>

              <!-- LLM 反馈文本框 -->
              <view class="llm-panel mt-8" style="background: rgba(59, 130, 246, 0.03); border-left: 4px solid #3b82f6; padding: 20px; border-radius: 0 16px 16px 0;">
                <view class="text-base mb-3 flex items-center gap-2" style="color: #3b82f6;">
                  <text class="title-icon icon-robot inline-block w-3 h-3 rounded-full" style="border: 3px solid #3b82f6; background: transparent;"></text>
                  LLM 智能化反馈总结
                </view>
                <text class="text-lg text-slate-500">LLM生成中...</text>
              </view>
            </view>
          </view>

          <!-- 右侧面板加载状态 -->
          <view class="panel-right flex flex-col h-full">
            <view class="card-title text-lg font-semibold mb-6 flex items-center gap-2.5" style="color: #0f172a;">
              <text class="title-icon icon-lightbulb inline-block w-4.5 h-4.5" style="background-color: #3b82f6; clip-path: polygon(50% 0%, 80% 30%, 50% 100%, 20% 30%);"></text>
              后续教学与强化建议
            </view>
            <text class="text-lg text-slate-500 py-2">LLM生成中...</text>
          </view>
        </view>
        <view v-else-if="reportModal.state === 'error'" class="flex items-center justify-center py-20 text-slate-400">
          <text>{{ reportModal.errorMessage || '报告生成失败，请稍后重试' }}</text>
        </view>
        <view v-else class="report-grid" style="display: grid; grid-template-columns: 1.1fr 0.9fr; grid-template-rows: 1fr; gap: 40px; text-align: left;">
          <!-- 左侧面板 -->
          <view class="panel-left flex flex-col h-full">
            <view class="card-title text-lg font-semibold mb-6 flex items-center gap-2.5" style="color: #0f172a;">
              <text class="title-icon inline-block w-4.5 h-4.5 rounded" style="background-color: #3b82f6; clip-path: polygon(0 100%, 30% 40%, 60% 70%, 100% 0, 100% 100%);"></text>
              错误知识点分布
            </view>
            <view class="card-body flex-1 flex flex-col justify-between">
              <view class="progress-group flex flex-col gap-5">
                <view v-for="(item, index) in getKnowledgeDistribution()" :key="index" class="progress-item flex flex-col gap-2">
                  <view class="progress-info flex justify-between text-sm font-medium" style="color: #0f172a;">
                    <text>{{ item.title }}</text>
                    <text :style="{ color: item.color }">{{ item.percentage }}%</text>
                  </view>
                  <view class="progress-track h-2 rounded" style="background: rgba(226, 232, 240, 0.8); overflow: hidden;">
                    <view class="progress-bar h-full rounded transition-all duration-800" :style="{ width: item.percentage + '%', backgroundColor: item.color }"></view>
                  </view>
                </view>
              </view>

              <view class="llm-panel mt-8" style="background: rgba(59, 130, 246, 0.03); border-left: 4px solid #3b82f6; padding: 20px; border-radius: 0 16px 16px 0;">
                <view class="text-base mb-3 flex items-center gap-2" style="color: #3b82f6;">
                  <text class="title-icon icon-robot inline-block w-3 h-3 rounded-full" style="border: 3px solid #3b82f6; background: transparent;"></text>
                  LLM 智能化反馈总结
                </view>
                <view class="llm-list list-none p-0 m-0 flex flex-col gap-3 text-sm leading-relaxed" style="color: #475569;">
                  <view v-if="reportModal.feedback_summary">
                    <text style="color: #0f172a; font-weight: bold;">整体总结：</text>{{ reportModal.feedback_summary }}
                  </view>
                </view>
              </view>
            </view>
          </view>

          <!-- 右侧面板 -->
          <view class="panel-right flex flex-col h-full">
            <view class="card-title text-lg font-semibold mb-6 flex items-center gap-2.5" style="color: #0f172a;">
              <text class="title-icon icon-lightbulb inline-block w-4.5 h-4.5" style="background-color: #3b82f6; clip-path: polygon(50% 0%, 80% 30%, 50% 100%, 20% 30%);"></text>
              后续教学与强化建议
            </view>
            <view class="card-body flex-1 flex flex-col justify-between">
              <view class="advice-stack flex flex-col gap-4 h-full">
                <view v-for="(advice, index) in reportModal.teaching_advice" :key="index" class="advice-item bg-white border border-gray-200 p-5 rounded-xl flex-1 flex flex-col justify-center">
                  <view class="text-base font-semibold mb-2" :style="{ color: getAdviceColor(index) }">{{ advice.keyword }}</view>
                  <text class="text-sm leading-relaxed" style="color: #475569;">{{ advice.text }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view v-if="ragModal.show" class="fixed inset-0 z-30 flex items-center justify-center p-4">
      <view @click="closeRAGModal" class="absolute inset-0 bg-black/40 backdrop-blur-sm"></view>
      <view class="rag-modal-card relative">
        <view class="rag-modal-header">
          <div class="modal-title">我的知识库</div>
          <view class="filter-tabs">
            <view 
              v-for="tab in ragTabs" 
              :key="tab"
              class="tab"
              :class="{ active: ragModal.activeTab === tab }"
              @click="handleRAGTabClick(tab)"
            >{{ tab }}</view>
          </view>
        </view>

        <view class="rag-modal-body">
          <span class="section-label">文件列表</span>
          
          <view v-if="uploadStatus.message" :class="['upload-status', uploadStatus.type]">
            {{ uploadStatus.message }}
          </view>
          
          <view v-if="ragFiles.length === 0" class="text-center py-10 text-slate-400">
            <text class="text-lg">暂无文件</text>
            <text class="text-sm block mt-2">请上传知识库文件</text>
          </view>
          
          <view 
            v-for="(file, index) in ragFiles" 
            :key="file.id"
            class="file-item"
            :data-type="file.type"
            :style="{ animationDelay: file.delay, display: ragModal.activeTab === '全部' || ragModal.activeTab === file.type ? 'flex' : 'none' }"
          >
            <view class="file-info">
              <view 
                class="file-icon"
                :style="{ 
                  background: file.type === 'pdf' ? '#fef2f2' : file.type === 'docx' ? '#eff6ff' : '#f8fafc',
                  color: file.type === 'pdf' ? '#ef4444' : file.type === 'docx' ? '#3b82f6' : '#64748b'
                }"
              >{{ file.type.toUpperCase() }}</view>
              <view class="file-details">
                <view class="name">{{ file.name }}</view>
                <view class="size">{{ file.size }}</view>
              </view>
            </view>
            <view class="status-badge">{{ file.status === 1 ? '已完成' : '上传中' }}</view>
          </view>
        </view>

        <view class="rag-modal-footer">
          <view 
            class="dropzone" 
            @dragover="handleDragOver" 
            @drop="handleDrop"
            @click="handleFileInput"
          >
            <view class="plus-icon-container">+</view>
            <view class="dropzone-text">将文件拖到此处，或<text style="color: #4f46e5;"> 点击浏览</text></view>
            <view class="dropzone-hint">支持 pdf, docx, txt 格式</view>
          </view>
        </view>
      </view>
    </view>

    <view class="share-modal-overlay" :class="{ active: shareModal.show }" @click="handleShareOverlayClick">
      <view class="share-modal">
        <button class="share-modal-close" @click="closeShareModal">&times;</button>
        
        <h2 class="share-modal-title">作业发布</h2>
        
        <view class="share-modal-form-group">
          <span class="share-modal-label">分享链接</span>
          <view class="share-modal-hint">学生点击链接即可打开 SmartCourse App 查看作业</view>
          <view class="share-modal-link-section">
            <input 
              v-if="shareModal.url" 
              type="text" 
              class="share-modal-url" 
              id="shareUrlInput" 
              :value="shareModal.url" 
              readonly 
            />
            <text 
              v-else 
              class="share-modal-url-placeholder"
            >点击「确定」后生成分享链接</text>
            <button 
              v-if="shareModal.url" 
              class="share-modal-btn share-modal-copy" 
              :class="{ copied: shareModal.copied }" 
              @click="copyShareLink"
            >
              {{ shareModal.copied ? '已复制' : '复制链接' }}
            </button>
          </view>
        </view>
        
        <view class="share-modal-form-group">
          <label for="task-title" class="share-modal-label">作业标题</label>
          <input type="text" id="task-title" class="share-modal-input" v-model="shareModal.assignmentTitle" placeholder="请输入作业标题" />
        </view>
        
        <view class="share-modal-form-group">
          <label for="due-date" class="share-modal-label">截止时间</label>
          <view class="datetime-row">
            <picker mode="date" :value="shareModal.deadline.slice(0, 10)" @change="onDateChange">
              <view class="share-modal-input date-picker">
                <text>{{ shareModal.deadline.slice(0, 10) || '选择日期' }}</text>
                <text class="date-picker-icon"></text>
              </view>
            </picker>
            <picker mode="time" :value="shareModal.deadline.slice(11, 16)" @change="onTimeChange">
              <view class="share-modal-input time-picker">
                <text>{{ shareModal.deadline.slice(11, 16) || '选择时间' }}</text>
                <text class="date-picker-icon"></text>
              </view>
            </picker>
          </view>
        </view>
        
        <view class="share-modal-footer">
          <button class="share-modal-btn share-modal-confirm" @click="confirmShare">确定</button>
        </view>
      </view>
    </view>

    <view class="resource-library-overlay" :class="{ active: showResourceLibrary }" @click="showResourceLibrary = false">
      <view class="resource-library-panel" @click.stop>
        <view class="resource-library-header">
          <view class="resource-header-top">
            <h3 class="resource-library-title">资料库</h3>
            <view class="resource-library-close" @click="showResourceLibrary = false">✕</view>
          </view>
          <view class="resource-search-container">
            <view class="search-box-inner">
              <view class="search-icon-left">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </view>
              
              <input 
                type="text" 
                class="resource-search-input-new" 
                placeholder="搜索已上传的课件..." 
                v-model="searchKeyword" 
                @focus="handleSearchFocus" 
                @blur="handleSearchBlur" 
                confirm-type="search" 
              />
              
              <view class="search-action-btn" @click="handleSearchConfirm">
                <text>搜索</text>
              </view>
            </view>
          </view>
        </view>
        
        <view class="resource-library-body">
          <view class="resource-list">
            <view v-if="resourceList.length === 0" class="text-center py-10 text-slate-400">
              <text class="text-lg">暂无资料</text>
              <text class="text-sm block mt-2">请上传教学资料</text>
            </view>
            
            <view 
              v-for="(resource, index) in resourceList" 
              :key="resource.id"
              class="resource-item" 
              :class="{ 'selected': selectedResources.includes(index) }"
              @click="toggleResourceSelect(index)"
            >
              <view class="resource-checkbox-wrapper" @click.stop="toggleResourceSelect(index)">
                <view class="resource-checkbox" :class="{ 'checked': selectedResources.includes(index) }">
                  <text v-if="selectedResources.includes(index)" class="check-icon">✓</text>
                </view>
              </view>
              <view 
                class="resource-icon" 
                :class="{
                  'pdf-icon': resource.type === 'PDF',
                  'doc-icon': resource.type === 'DOCX',
                  'txt-icon': resource.type === 'TXT',
                  'ppt-icon': resource.type === 'PPTX'
                }"
              >{{ resource.type }}</view>
              <view class="resource-info">
                <text class="resource-name">{{ resource.name }}</text>
                <text class="resource-meta">{{ resource.size }} · {{ resource.time }} 上传</text>
              </view>
            </view>
            
            <view 
              class="resource-upload-btn" 
              @click="handleResourceUploadClick"
              @dragover="handleResourceDragOver"
              @drop="handleResourceDrop"
            >
              <text class="upload-icon">+</text>
              <text>上传新资料</text>
            </view>
          </view>
        </view>
        
        <view class="resource-library-footer">
          <button class="resource-confirm-btn" @click="confirmResourceAssociation">确认关联并更新 AI</button>
        </view>
      </view>
    </view>

  </view>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick, watch } from 'vue';
import CONFIG from '@/utils/config.js';
import QuestionChoiceEditor from '@/components/QuestionChoiceEditor.vue';
import QuestionMultipleChoiceEditor from '@/components/QuestionMultipleChoiceEditor.vue';
import QuestionTrueFalseEditor from '@/components/QuestionTrueFalseEditor.vue';
import QuestionCodeFillEditor from '@/components/QuestionCodeFillEditor.vue';
import QuestionFillBlankEditor from '@/components/QuestionFillBlankEditor.vue';
import QuestionMatchingEditor from '@/components/QuestionMatchingEditor.vue';
import QuestionShortAnswerEditor from '@/components/QuestionShortAnswerEditor.vue';
import AssignmentCard from '@/components/AssignmentCard.vue';
import AssignmentDetail from '@/components/AssignmentDetail.vue';

const savedTab = localStorage.getItem('teacherCurrentTab') || 'design';
const currentTab = ref(savedTab);
const nodes = ref([]);
const isUpdating = ref(false); 
const currentView = ref('list');
const showResourceLibrary = ref(false);
const selectedResources = ref([]);
const searchKeyword = ref('');
const searchFocused = ref(false);
const hasSearchFocus = ref(false);
const resourceList = ref([]);

const fetchResourceList = async () => {
  try {
    const response = await fetch(CONFIG.baseUrl + '/api/rag/knowledge-base', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const result = await response.json();
    if (result.code === 200) {
      resourceList.value = result.data.map((file, index) => ({
        id: file.id,
        name: file.file_name,
        type: file.file_type.toUpperCase(),
        size: formatFileSize(file.file_size),
        time: file.upload_time
      }));
    }
  } catch (error) {
    console.error('获取资源列表失败:', error);
  }
};

const handleResourceUpload = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch(CONFIG.baseUrl + '/api/rag/knowledge-base', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    });
    const result = await response.json();
    if (result.code === 200) {
      uni.showToast({ title: '上传成功', icon: 'success' });
      fetchResourceList();
    } else {
      uni.showToast({ title: result.message || '上传失败', icon: 'none' });
    }
  } catch (error) {
    console.error('上传失败:', error);
    uni.showToast({ title: '上传失败', icon: 'none' });
  }
};

const handleResourceUploadClick = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.pdf,.docx,.txt,.pptx';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await handleResourceUpload(file);
    }
  };
  input.click();
};

const handleResourceDrop = (e) => {
  e.preventDefault();
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleResourceUpload(files[0]);
  }
};

const handleResourceDragOver = (e) => {
  e.preventDefault();
};
const selectedAssignment = reactive({
  title: '',
  deadline: '',
  deadline_ts: 0,
  status: '',
  participants: [],
  share_code: ''
});

const assignmentStats = reactive({
  submittedCount: 0,
  totalStudents: 0,
  avgScore: 0,
  totalScore: 0,
  excellentRate: '0%',
  hardestQuestion: '—',
  hardestErrorRate: 0,
  scoreDistribution: { excellent: 0, good: 0, pass: 0, fail: 0 }
});

const questionScores = ref([]);
const submittedStudents = ref([]);
const unsubmittedStudents = ref([]);
const detailAssignmentId = ref(null);
let statsTimer = null;
let eventSource = null;
let isClosing = false;

const selectedPortId = ref(null);
const connections = ref([]);
const portRefs = {};

const now = new Date();
const defaultDeadline = now.toISOString().slice(0, 16);

const shareModal = reactive({
  show: false,
  url: '',
  copied: false,
  assignmentTitle: '新建作业',
  deadline: defaultDeadline
});

const formatDeadline = (deadline) => {
  if (!deadline) return '请选择日期时间';
  const date = new Date(deadline.replace('T', ' '));
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${year}/${month}/${day} ${hours}:${minutes}`;
};

const onDateChange = (e) => {
  const date = e.detail.value;
  const time = shareModal.deadline ? shareModal.deadline.slice(11, 16) : '23:59';
  shareModal.deadline = `${date}T${time}`;
};

const onTimeChange = (e) => {
  const time = e.detail.value;
  const date = shareModal.deadline ? shareModal.deadline.slice(0, 10) : new Date().toISOString().slice(0, 10);
  shareModal.deadline = `${date}T${time}`;
};

const pendingQuestions = ref([]);

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
});

const aiModal = reactive({
  show: false,
  prompt: '',
  difficulty: '中等',
  questionType: ''
});

const loadingState = reactive({
  show: false
});

const reportModal = reactive({
  show: false,
  state: 'generating',
  errorMessage: '',
  title: '',
  error_points: [],
  feedback_summary: '',
  teaching_advice: []
});

const deadlineTimerRef = ref(null);
let reportPollTimer = null;
let reportRequestId = 0;

// 作业列表数据
const assignmentList = reactive({
  today: [],
  recent: []
});

// 写死的 participants 数据
const fixedParticipants = [
  { initial: 'A', bgClass: 'bg-indigo-100 text-indigo-600' },
  { initial: 'B', bgClass: 'bg-emerald-100 text-emerald-600' },
  { initial: '+12', bgClass: 'bg-slate-100 text-slate-400' }
];

// 加载教师作业列表
const loadTeacherAssignments = async () => {
  try {
    console.log('=== 开始加载作业列表 ===');
    
    const userInfo = uni.getStorageSync('userInfo') || localStorage.getItem('userInfo');
    let userId = 1;
    if (userInfo) {
      const parsedInfo = typeof userInfo === 'string' ? JSON.parse(userInfo) : userInfo;
      userId = parsedInfo?.user_id || parsedInfo?.userId || 1;
    }
    
    console.log('使用的userId:', userId);
    
    const url = CONFIG.baseUrl + `/api/teacher/${userId}/assignments`;
    console.log('请求URL:', url);
    
    const response = await fetch(url);
    const result = await response.json();
    
    console.log('接口返回结果:', result);
    
    if (result.success) {
      assignmentList.today = result.data.today || [];
      assignmentList.recent = result.data.recent || [];
      console.log('作业列表已更新 - today:', assignmentList.today.length, '个作业');
    }
    scheduleDeadlineCheck();
  } catch (error) {
    console.error('加载作业列表失败:', error);
  }
};

// 监听标签切换，切换到作业列表时加载数据，同时保存状态
watch(currentTab, (newTab) => {
  localStorage.setItem('teacherCurrentTab', newTab);
  if (newTab === 'list') {
    loadTeacherAssignments();
  }
});

// 组件加载时也尝试加载一次
onMounted(() => {
  if (currentTab.value === 'list') {
    loadTeacherAssignments();
  }
});

const ragModal = reactive({
  show: false,
  activeTab: '全部'
});

const uploadStatus = reactive({
  message: '',
  type: ''
});

const ragFiles = ref([]);
const ragTabs = ['全部', 'pdf', 'docx', 'txt'];

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

const fetchKnowledgeBase = async () => {
  try {
    const type = ragModal.activeTab === '全部' ? '' : ragModal.activeTab;
    const url = type ? CONFIG.baseUrl + '/api/rag/knowledge-base?file_type=' + type : CONFIG.baseUrl + '/api/rag/knowledge-base';
    console.log('获取知识库列表URL:', url);
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const result = await response.json();
    if (result.code === 200) {
      ragFiles.value = result.data.map((file, index) => ({
        id: file.id,
        type: file.file_type,
        name: file.file_name,
        size: formatFileSize(file.file_size),
        status: file.status,
        delay: `${index * 0.2}s`
      }));
    }
  } catch (error) {
    console.error('获取知识库列表失败:', error);
  }
};

const handleRAGTabClick = (tab) => {
  ragModal.activeTab = tab;
  fetchKnowledgeBase();
};

const handleDragOver = (e) => {
  e.preventDefault();
};

const handleDrop = async (e) => {
  e.preventDefault();
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    await uploadFile(files[0]);
  }
};

const uploadFile = async (file) => {
  console.log('========== 开始上传文件 ==========');
  console.log('文件名:', file.name);
  console.log('文件类型:', file.type);
  console.log('文件大小:', file.size, 'bytes');
  console.log('文件大小(MB):', (file.size / (1024 * 1024)).toFixed(2));
  
  uploadStatus.message = '上传中...';
  uploadStatus.type = 'loading';
  
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    console.log('开始发送请求...');
    const startTime = Date.now();
    
    const url = CONFIG.baseUrl + '/api/rag/knowledge-base';
    console.log('请求URL:', url);
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    });
    
    const endTime = Date.now();
    console.log(`请求完成，耗时: ${endTime - startTime}ms`);
    console.log('响应状态码:', response.status);
    console.log('响应状态文本:', response.statusText);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`请求失败，状态码: ${response.status}`);
      console.error('响应内容:', errorText);
      uploadStatus.message = `请求失败: ${response.status}`;
      uploadStatus.type = 'error';
      setTimeout(() => {
        uploadStatus.message = '';
      }, 3000);
      return;
    }
    
    const result = await response.json();
    console.log('响应JSON:', result);
    
    if (result.code === 200) {
      console.log('上传成功！');
      uploadStatus.message = '上传成功';
      uploadStatus.type = 'success';
      setTimeout(() => {
        uploadStatus.message = '';
      }, 3000);
      fetchKnowledgeBase();
    } else {
      console.error('上传失败:', result.message);
      uploadStatus.message = result.message || '上传失败';
      uploadStatus.type = 'error';
      setTimeout(() => {
        uploadStatus.message = '';
      }, 3000);
    }
  } catch (error) {
    console.error('文件上传异常:', error);
    console.error('异常类型:', error.name);
    console.error('异常消息:', error.message);
    if (error.stack) {
      console.error('异常堆栈:', error.stack);
    }
    
    // 判断错误类型
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      console.error('网络请求失败，可能是后端服务未启动或跨域问题');
      uploadStatus.message = '网络连接失败，请检查后端服务';
    } else if (error.name === 'AbortError') {
      uploadStatus.message = '请求已取消';
    } else {
      uploadStatus.message = `上传异常: ${error.message}`;
    }
    uploadStatus.type = 'error';
    setTimeout(() => {
      uploadStatus.message = '';
    }, 3000);
  }
};

const handleFileInput = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.pdf,.docx,.txt';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await uploadFile(file);
    }
  };
  input.click();
};

const questionTypes = [
  { value: '', label: '自动' },
  { value: '单选题', label: '单选题' },
  { value: '多选题', label: '多选题' },
  { value: '判断题', label: '判断题' },
  { value: '填空题', label: '填空题' },
  { value: '代码填空', label: '代码填空' },
  { value: '匹配题', label: '匹配题' },
  { value: '简答题', label: '简答题' }
];

const toolset = [
  { type: '单选题', color: 'bg-blue-500' },
  { type: '多选题', color: 'bg-purple-500' },
  { type: '代码填空', color: 'bg-emerald-500' },
  { type: '匹配题', color: 'bg-orange-500' },
  { type: '判断题', color: 'bg-rose-500' },
  { type: '填空题', color: 'bg-cyan-500' },
  { type: '简答题', color: 'bg-indigo-500' }
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
    updateLines();
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
  if (deadlineTimerRef.value) {
    clearTimeout(deadlineTimerRef.value);
    deadlineTimerRef.value = null;
  }
  if (eventSource) { eventSource.close(); eventSource = null; }
  stopStatsPolling();
  stopReportPolling();
  reportRequestId++;
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
    '教材/课件': {
      title: '教材/课件'
    },
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
  
  if (node.type === '教材/课件') {
    showResourceLibrary.value = true;
    fetchResourceList();
    return;
  }
  
  if (!node.isExpanded) {
    expandNode(index);
  }
};

const expandNode = (index) => {
  const canvasElement = document.querySelector('.node-canvas-bg');
  const rect = canvasElement.getBoundingClientRect();
  const node = nodes.value[index];
  
  let currentLeft = node.x || 0;
  if (currentLeft + 600 > rect.width) {
    currentLeft = Math.max(0, rect.width - 600);
    node.x = currentLeft;
  }
  
  node.isExpanded = true;
  
  nextTick(() => {
    updateLines();
  });
};

const shrinkNode = (index) => {
  const canvasElement = document.querySelector('.node-canvas-bg');
  const rect = canvasElement.getBoundingClientRect();
  const node = nodes.value[index];
  
  let currentLeft = node.x || 0;
  let currentTop = node.y || 0;
  currentLeft = Math.min(currentLeft, rect.width - 240);
  currentTop = Math.min(currentTop, rect.height - 145);
  
  node.x = currentLeft;
  node.y = currentTop;
  node.isExpanded = false;
  
  nextTick(() => {
    updateLines();
  });
};

const getQuestionIndex = (nodeIndex) => {
  let count = 0;
  for (let i = 0; i < nodes.value.length; i++) {
    if (nodes.value[i].type !== '教材/课件') {
      count++;
      if (i === nodeIndex) return count;
    }
  }
  return 0;
};

const removeNode = (index) => {
  isUpdating.value = true;
  
  const node = nodes.value[index];
  if (node) {
    connections.value = connections.value.filter(c => 
      c.startPortId !== node.id && c.endPortId !== node.id
    );
    updateLines();
  }
  
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

const generateQuestionWithAI = (nodeIndex) => {
  if (nodeIndex !== undefined && nodeIndex >= 0 && nodeIndex < nodes.value.length) {
    const currentNode = nodes.value[nodeIndex];
    aiModal.questionType = currentNode.type;
    aiModal.currentNodeIndex = nodeIndex;
  } else {
    aiModal.questionType = '';
    aiModal.currentNodeIndex = -1;
  }
  aiModal.show = true;
};

const closeAIModal = () => {
  aiModal.show = false;
  aiModal.prompt = '';
  aiModal.difficulty = '中等';
};

const openRAGModal = () => {
  ragModal.show = true;
  ragModal.activeTab = '全部';
  fetchKnowledgeBase();
};

const closeRAGModal = () => {
  ragModal.show = false;
};

const generateQuestion = async () => {
  const promptText = aiModal.prompt.trim();
  if (!promptText) {
    showToast('请输入题目描述', 'error');
    return;
  }
  const diffText = aiModal.difficulty;
  const typeText = aiModal.questionType || undefined;
  
  // 立即关闭弹窗，显示加载动画
  closeAIModal();
  loadingState.show = true;
  
  try {
    const response = await fetch(CONFIG.baseUrl + '/api/ai/generate-question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt: promptText,
        difficulty: diffText,
        question_type: typeText
      })
    });
    
    const result = await response.json();
    
    if (result.success && result.data) {
      const questionData = result.data;
      
      const typeMap = {
        'choice': '单选题',
        'multiple_choice': '多选题',
        'true_false': '判断题',
        'fill_blank': '填空题',
        'code_fill': '代码填空',
        'matching': '匹配题',
        'short_answer': '简答题'
      };
      
      const questionType = typeMap[questionData.type] || '单选题';
      
      const data = {
        title: questionData.title || '',
        options: questionData.options || ['', '', '', ''],
        analysis: questionData.analysis || '',
        answer: questionData.answer || 0,
        score: questionData.score || 10,
        correctAnswers: questionData.correctAnswers || [],
        content: questionData.content || '',
        code: questionData.code || '',
        fields: questionData.fields || [],
        pairs: questionData.pairs || [
          { left: '', right: '' },
          { left: '', right: '' },
          { left: '', right: '' }
        ],
        standardAnswer: questionData.standardAnswer || ''
      };
      
      // 检查是否正在编辑某个node
      if (aiModal.currentNodeIndex !== undefined && aiModal.currentNodeIndex >= 0 && aiModal.currentNodeIndex < nodes.value.length) {
        // 更新当前正在编辑的node，保持原有的题型
        const currentNode = nodes.value[aiModal.currentNodeIndex];
        const finalQuestionType = currentNode.type;
        nodes.value[aiModal.currentNodeIndex] = {
          ...currentNode,
          type: finalQuestionType,
          data: data,
          answer: questionData.answer || (finalQuestionType === '多选题' ? [] : 0),
          color: getQuestionColor(finalQuestionType)
        };
      } else {
        // 创建新node
        const canvasElement = document.querySelector('.node-canvas-bg');
        const rect = canvasElement.getBoundingClientRect();
        nodes.value.push({
          type: questionType,
          data: data,
          answer: questionData.answer || (questionType === '多选题' ? [] : 0),
          id: Date.now().toString(),
          x: rect.width / 2 - 120,
          y: rect.height / 2 - 72,
          color: getQuestionColor(questionType)
        });
      }
      
      loadingState.show = false;
      showToast('题目生成成功！', 'success');
    } else {
      loadingState.show = false;
      showToast(result.message || '生成失败，请重试', 'error');
    }
  } catch (error) {
    console.error('生成题目失败:', error);
    loadingState.show = false;
    showToast('生成失败，请检查网络连接', 'error');
  }
};

const getQuestionColor = (type) => {
  const colorMap = {
    '单选题': 'bg-blue-500',
    '多选题': 'bg-purple-500',
    '判断题': 'bg-rose-500',
    '填空题': 'bg-cyan-500',
    '代码填空': 'bg-emerald-500',
    '匹配题': 'bg-orange-500',
    '简答题': 'bg-indigo-500'
  };
  return colorMap[type] || 'bg-blue-500';
};

const showToast = (message, type = 'success') => {
  toast.message = message;
  toast.type = type;
  toast.show = true;
  setTimeout(() => {
    toast.show = false;
  }, 2000);
};

const saveWorkflow = () => {
  showToast('保存成功');
};

const openShareModal = () => {
  if (nodes.value.length === 0) {
    showToast('请先添加题目', 'error');
    return;
  }
  
  const typeMapping = {
    '单选题': 'choice',
    '多选题': 'multiple_choice',
    '判断题': 'true_false',
    '代码填空': 'code_fill',
    '填空题': 'fill_blank',
    '匹配题': 'matching',
    '简答题': 'short_answer'
  };

  const questionNodes = nodes.value.filter((node) => typeMapping[node.type]);
  if (questionNodes.length === 0) {
    showToast('请先添加题目', 'error');
    return;
  }
  
  const questions = questionNodes.map((node, index) => {
    const data = node.data;
    const question = {
      type: typeMapping[node.type],
      question_title: data.title || data.question_title || '',
      options: null,
      content: null,
      code: null,
      fields: null,
      left_items: null,
      right_items: null,
      correct_answers: null,
      is_multiple: node.type === '多选题' ? true : false,
      analysis: data.analysis || '',
      score: data.score || 10,
      sort_order: index
    };
    
    if (node.type === '单选题') {
      question.options = JSON.stringify(data.options || []);
      const answer = data.answer !== undefined && data.answer !== null ? data.answer : (node.answer !== undefined && node.answer !== null ? node.answer : [0]);
      question.correct_answers = JSON.stringify(Array.isArray(answer) ? answer : [answer]);
    } else if (node.type === '多选题') {
      question.options = JSON.stringify(data.options || []);
      const answer = data.answer !== undefined && data.answer !== null ? data.answer : (node.answer !== undefined && node.answer !== null ? node.answer : []);
      question.correct_answers = JSON.stringify(Array.isArray(answer) ? answer : []);
    } else if (node.type === '判断题') {
      const answer = data.answer !== undefined && data.answer !== null ? data.answer : (node.answer !== undefined && node.answer !== null ? node.answer : false);
      question.correct_answers = answer ? 'true' : 'false';
    } else if (node.type === '代码填空') {
      question.code = data.code || '';
      const fields = data.fields || [];
      const processedFields = fields.map(f => ({
        value: f.value || '',
        answer: f.answer || ''
      }));
      const answers = processedFields.map(f => f.answer);
      question.fields = JSON.stringify(processedFields);
      question.correct_answers = JSON.stringify(answers);
    } else if (node.type === '填空题') {
      question.content = data.content || '';
      const blanks = (data.content || '').split('????').length - 1;
      const existingAnswers = data.correctAnswers || [];
      const answers = Array.from({ length: blanks }, (_, i) => existingAnswers[i] || '');
      question.correct_answers = JSON.stringify(answers);
    } else if (node.type === '匹配题') {
      const pairs = data.pairs || [];
      question.left_items = JSON.stringify(pairs.map(p => p.left || ''));
      question.right_items = JSON.stringify(pairs.map(p => p.right || ''));
      const correctAnswers = pairs.map((_, idx) => ({ l: idx, r: idx }));
      question.correct_answers = JSON.stringify(correctAnswers);
    } else if (node.type === '简答题') {
      const answer = data.standardAnswer || data.answer || '';
      question.correct_answers = JSON.stringify({ standardAnswer: answer });
    }
    
    return question;
  });
  
  console.log('========== 作业题目数据 ==========');
  console.log(JSON.stringify(questions, null, 2));
  console.log('==================================');
  
  pendingQuestions.value = questions;
  
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const currentDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
  
  shareModal.deadline = currentDateTime;
  
  // 初始时不显示假链接，而是显示提示
  shareModal.url = '';
  shareModal.show = true;
};

const submitAssignment = async (questions) => {
  try {
    const deadline = shareModal.deadline ? shareModal.deadline.replace('T', ' ') + ':00' : new Date().toISOString().slice(0, 19).replace('T', ' ');
    
    const assignmentData = {
      assignment_title: shareModal.assignmentTitle || '新建作业',
      deadline: deadline,
      status: 'ongoing'
    };
    
    console.log('提交的数据:', assignmentData);
    console.log('Token:', localStorage.getItem('token'));
    
    const assignmentResponse = await fetch(CONFIG.baseUrl + '/api/assignments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(assignmentData)
    });
    
    console.log('响应状态:', assignmentResponse.status);
    const assignmentResult = await assignmentResponse.json();
    console.log('创建作业结果:', assignmentResult);
    
    if (!assignmentResult.success) {
      showToast('创建作业失败: ' + (assignmentResult.message || '未知错误'), 'error');
      return;
    }
    
    const assignmentId = assignmentResult.data.assignment_id;
    console.log('创建的作业ID:', assignmentId);
    
    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];
      question.assignment_id = assignmentId;
      console.log(`正在创建题目 ${i + 1}:`, question);
      
      const questionResponse = await fetch(CONFIG.baseUrl + '/api/questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(question)
      });
      
      const questionResult = await questionResponse.json();
      console.log(`题目 ${i + 1} 创建结果:`, questionResult);
      
      if (!questionResult.success) {
        showToast('创建题目失败: ' + (questionResult.message || '未知错误'), 'error');
        return;
      }
    }
    
    const shareResponse = await fetch(CONFIG.baseUrl + '/api/shares', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ assignment_id: assignmentId, access_type: 'submit' })
    });
    
    const shareResult = await shareResponse.json();
    console.log('分享链接创建结果:', shareResult);
    
    if (shareResult.success) {
      shareModal.url = CONFIG.shareUrl + '/' + shareResult.data.share_code;
      shareModal.copied = false;
      shareModal.show = true;
      // 刷新作业列表
      await loadTeacherAssignments();
    } else {
      showToast('生成分享链接失败: ' + (shareResult.message || '未知错误'), 'error');
    }
    
  } catch (error) {
    console.error('发布作业失败:', error);
    showToast('发布失败，请重试: ' + error.message, 'error');
  }
};

const generateShareCode = () => {
  return 'item-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
};

const closeShareModal = () => {
  shareModal.show = false;
};

const handleShareOverlayClick = (e) => {
  if (e.target === e.currentTarget) {
    closeShareModal();
  }
};

const copyShareLink = async () => {
  try {
    await navigator.clipboard.writeText(shareModal.url);
    shareModal.copied = true;
    setTimeout(() => {
      shareModal.copied = false;
    }, 1500);
  } catch (err) {
    uni.showToast({ title: '复制失败', icon: 'none' });
  }
};

const confirmShare = async () => {
  // 1. 先关闭之前的弹窗
  closeShareModal();
  
  // 2. 显示加载状态
  uni.showLoading({ title: '发布中...' });
  
  try {
    const deadline = shareModal.deadline ? shareModal.deadline.replace('T', ' ') + ':00' : new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 19).replace('T', ' ');
    
    const assignmentData = {
      assignment_title: shareModal.assignmentTitle || '新建作业',
      deadline: deadline,
      status: 'ongoing'
    };
    
    console.log('提交的数据:', assignmentData);
    
    const assignmentResponse = await fetch(CONFIG.baseUrl + '/api/assignments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(assignmentData)
    });
    
    console.log('响应状态:', assignmentResponse.status);
    const assignmentResult = await assignmentResponse.json();
    console.log('创建作业结果:', assignmentResult);
    
    if (!assignmentResult.success) {
      uni.hideLoading();
      showToast('创建作业失败: ' + (assignmentResult.message || '未知错误'), 'error');
      return;
    }
    
    const assignmentId = assignmentResult.data.assignment_id;
    console.log('创建的作业ID:', assignmentId);
    
    for (let i = 0; i < pendingQuestions.value.length; i++) {
      const question = { ...pendingQuestions.value[i], assignment_id: assignmentId };
      console.log(`正在创建题目 ${i + 1}:`, question);
      
      const questionResponse = await fetch(CONFIG.baseUrl + '/api/questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(question)
      });
      
      const questionResult = await questionResponse.json();
      console.log(`题目 ${i + 1} 创建结果:`, questionResult);
      
      if (!questionResult.success) {
        uni.hideLoading();
        showToast('创建题目失败: ' + (questionResult.message || '未知错误'), 'error');
        return;
      }
    }
    
    const shareResponse = await fetch(CONFIG.baseUrl + '/api/shares', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ assignment_id: assignmentId, access_type: 'submit' })
    });
    
    const shareResult = await shareResponse.json();
    console.log('分享链接创建结果:', shareResult);
    
    uni.hideLoading();
    
    if (shareResult.success) {
      // 使用 HTTP 格式的分享链接
      shareModal.url = CONFIG.shareUrl + '/' + shareResult.data.share_code;
      shareModal.copied = false;
      // 关键：重新打开弹窗，让教师看到真链接！
      shareModal.show = true;
      showToast('发布成功');
      // 刷新作业列表，更新最新的 share_code
      await loadTeacherAssignments();
    } else {
      showToast('生成分享链接失败: ' + (shareResult.message || '未知错误'), 'error');
    }
    
  } catch (error) {
    uni.hideLoading();
    console.error('发布作业失败:', error);
    showToast('发布失败，请重试: ' + error.message, 'error');
  }
};

const openAssignmentDetail = (title, deadline, status, participants, shareCode, deadlineTs, assignmentId) => {
  console.log('打开作业详情:', { title, deadline, status, shareCode, deadlineTs, assignmentId });
  selectedAssignment.title = title;
  selectedAssignment.deadline = deadline;
  selectedAssignment.deadline_ts = deadlineTs || 0;
  selectedAssignment.status = status;
  selectedAssignment.participants = participants || [];
  selectedAssignment.share_code = shareCode || '';
  selectedAssignment.assignment_id = assignmentId || null;
  currentView.value = 'detail';

  detailAssignmentId.value = assignmentId || null;
  fetchAssignmentStats();

  // 建立 SSE 连接，批改完成后自动刷新
  stopStatsPolling();
  if (eventSource) { eventSource.close(); eventSource = null; }
  if (assignmentId && status === '进行中') {
    if (typeof EventSource === 'undefined') {
      startStatsPolling();
      return;
    }
    const source = new EventSource(CONFIG.baseUrl + `/api/assignments/${assignmentId}/events`);
    eventSource = source;
    source.onopen = () => {
      if (eventSource !== source || currentView.value !== 'detail') return;
      stopStatsPolling();
      fetchAssignmentStats();
    };
    source.onmessage = () => {
      if (eventSource !== source || currentView.value !== 'detail') return;
      stopStatsPolling();
      fetchAssignmentStats();
    };
    source.onerror = () => {
      if (eventSource !== source) return;
      source.close();
      eventSource = null;
      if (currentView.value === 'detail' && detailAssignmentId.value === assignmentId) {
        startStatsPolling();
      }
    };
  }
};

async function fetchAssignmentStats() {
  const id = detailAssignmentId.value;
  if (!id) return;
  try {
    const res = await fetch(CONFIG.baseUrl + `/api/assignments/${id}/stats`);
    const data = await res.json();
    if (data.success && data.data) {
      const d = data.data;
      assignmentStats.submittedCount = d.submitted_count || 0;
      assignmentStats.totalStudents = d.total_students || 0;
      assignmentStats.avgScore = d.avg_score || 0;
      assignmentStats.totalScore = d.total_score || 0;
      assignmentStats.excellentRate = d.excellent_rate || '0%';
      // 处理高频错题：只有在有数据时才显示
      if (d.hardest_question && d.hardest_question.error_rate >= 0) {
        assignmentStats.hardestQuestion = d.hardest_question.label || '—';
        assignmentStats.hardestErrorRate = (d.hardest_question.error_rate * 100).toFixed(0) + '%';
      } else {
        assignmentStats.hardestQuestion = '—';
        assignmentStats.hardestErrorRate = '—';
      }
      // 处理题目分数：error_rate为-1时表示没有数据，score设为null
      questionScores.value = (d.question_scores || []).map(q => ({
        label: q.label, 
        score: q.error_rate >= 0 ? Math.round((1 - q.error_rate) * 100) : null, 
        color: q.color
      }));
      assignmentStats.scoreDistribution = d.score_distribution || { excellent: 0, good: 0, pass: 0, fail: 0 };
      submittedStudents.value = (d.submitted_students || []).map(s => ({
        name: s.name, className: s.className || '', id: s.id,
        submitTime: s.submit_time || '', score: s.score || '0',
        status: s.status || '已提交'
      }));
      unsubmittedStudents.value = (d.unsubmitted_students || []).map(s => ({
        name: s.name, className: s.className || '', id: s.id
      }));
    }
  } catch (e) {
    console.error('获取统计数据失败:', e);
  }
}

function startStatsPolling() {
  stopStatsPolling();
  statsTimer = setTimeout(() => {
    fetchAssignmentStats();
    startStatsPolling();
  }, 10000);
}

function stopStatsPolling() {
  if (statsTimer) { clearTimeout(statsTimer); statsTimer = null; }
}

const closeDetailView = () => {
  if (eventSource) { eventSource.close(); eventSource = null; }
  stopStatsPolling();
  currentView.value = 'list';
};

const clearReportContent = () => {
  reportModal.error_points = [];
  reportModal.feedback_summary = '';
  reportModal.teaching_advice = [];
};

const stopReportPolling = () => {
  if (reportPollTimer) {
    clearTimeout(reportPollTimer);
    reportPollTimer = null;
  }
};

const fetchReportUntilReady = async (assignmentId, requestId) => {
  if (!reportModal.show || requestId !== reportRequestId) return;

  try {
    const res = await fetch(CONFIG.baseUrl + `/api/assignments/${assignmentId}/report`);
    const data = await res.json();
    if (!reportModal.show || requestId !== reportRequestId) return;

    if (data.success && data.data && data.data.report_data) {
      const rd = data.data.report_data;
      reportModal.error_points = rd.error_points || [];
      reportModal.feedback_summary = rd.feedback_summary || '';
      reportModal.teaching_advice = rd.teaching_advice || [];
      reportModal.state = 'ready';
      stopReportPolling();
      return;
    }

    if (data.status === 'generating') {
      reportModal.state = 'generating';
      reportPollTimer = setTimeout(() => fetchReportUntilReady(assignmentId, requestId), 1500);
      return;
    }

    reportModal.state = 'error';
    reportModal.errorMessage = data.message || '报告生成失败，请稍后重试';
    stopReportPolling();
  } catch (e) {
    if (!reportModal.show || requestId !== reportRequestId) return;
    console.error('获取报告失败:', e);
    reportModal.state = 'error';
    reportModal.errorMessage = '获取报告失败，请稍后重试';
    stopReportPolling();
  }
};

const handleReportClick = (assignment) => {
  stopReportPolling();
  reportRequestId++;
  reportModal.show = true;
  reportModal.state = 'generating';
  reportModal.errorMessage = '';
  reportModal.title = assignment.title;
  clearReportContent();
  fetchReportUntilReady(assignment.assignment_id, reportRequestId);
};

const closeReportModal = () => {
  reportModal.show = false;
  reportRequestId++;
  stopReportPolling();
};

const getKnowledgeDistribution = () => {
  return reportModal.error_points.map((ep, index) => {
    const colors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'];
    const rate = Math.max(0, Math.min(1, Number(ep.error_rate) || 0));
    const percentage = Math.round(rate * 100);
    return {
      title: ep.name,
      percentage: percentage,
      color: colors[index % colors.length]
    };
  });
};

const getAdviceColor = (index) => {
  const colors = ['#10b981', '#3b82f6', '#f59e0b'];
  return colors[index % colors.length];
};

const handleCloseClick = async (assignmentId) => {
  if (isClosing) return;
  isClosing = true;
  selectedAssignment.status = '已截止';
  selectedAssignment.deadline_ts = Math.floor(Date.now() / 1000);
  try {
    await fetch(CONFIG.baseUrl + `/api/assignments/${assignmentId}/close`, { method: 'POST' });
    showToast('作业已截止，报告生成中', 'success');
    await loadTeacherAssignments();
    scheduleDeadlineCheck();
  } catch (e) {
    console.error('截止作业失败:', e);
    showToast('截止失败', 'error');
  } finally {
    isClosing = false;
  }
};

function scheduleDeadlineCheck() {
  if (deadlineTimerRef.value) {
    clearTimeout(deadlineTimerRef.value);
    deadlineTimerRef.value = null;
  }
  const now = Date.now() / 1000;
  const allAssignments = [...assignmentList.today, ...assignmentList.recent];
  const processing = allAssignments.filter(a => a.status === '进行中' && a.deadline_ts);
  if (processing.length === 0) return;
  const nearest = Math.min(...processing.map(a => a.deadline_ts));
  const diffMs = (nearest - now) * 1000 + 500;
  if (diffMs <= 0) {
    autoCloseExpired(processing.filter(a => a.deadline_ts <= now));
    return;
  }
  deadlineTimerRef.value = setTimeout(() => {
    autoCloseExpired(processing.filter(a => a.deadline_ts <= Date.now() / 1000));
  }, diffMs);
}

async function autoCloseExpired(list) {
  if (!list || list.length === 0) return;
  for (const a of list) {
    try {
      await fetch(CONFIG.baseUrl + `/api/assignments/${a.assignment_id}/close`, { method: 'POST' });
    } catch (e) {
      console.error('自动截止失败:', a.assignment_id, e);
    }
  }
  await loadTeacherAssignments();
  scheduleDeadlineCheck();
}

const handleUploadResource = () => {
  showToast('功能开发中', 'info');
};

const toggleResourceSelect = (index) => {
  const idx = selectedResources.value.indexOf(index);
  if (idx > -1) {
    selectedResources.value.splice(idx, 1);
  } else {
    selectedResources.value.push(index);
  }
};

const focusSearch = () => {
  searchFocused.value = true;
};

const handleSearchFocus = () => {
  hasSearchFocus.value = true;
};

const handleSearchBlur = () => {
  hasSearchFocus.value = false;
};

const handleSearchConfirm = () => {
  console.log("执行搜索:", searchKeyword.value);
};

const handlePortClick = (nodeId, type) => {
  const currentId = nodeId + '-' + type;
  
  if (type === 'out') {
    selectedPortId.value = (selectedPortId.value === currentId) ? null : currentId;
    console.log('选中源点:', selectedPortId.value);
  } else if (type === 'in' && selectedPortId.value) {
    const [startNodeId] = selectedPortId.value.split('-');
    const lineId = `line-${startNodeId}-${nodeId}`;
    
    if (!connections.value.some(c => c.lineId === lineId)) {
      connections.value.push({
        lineId,
        startPortId: startNodeId,
        endPortId: nodeId
      });
      console.log('连线成功:', lineId);
    }
    
    selectedPortId.value = null;
    nextTick(() => {
      updateLines();
    });
  }
};

const updateLines = () => {
  const svgLayer = document.getElementById('svg-layer');
  const canvas = document.querySelector('.node-canvas-bg');
  
  if (!svgLayer || !canvas) return;

  const canvasRect = canvas.getBoundingClientRect();
  svgLayer.innerHTML = '';

  connections.value.forEach(conn => {
    const startEl = document.querySelector(`[data-port-id="${conn.startPortId}"][data-port-type="out"]`);
    const endEl = document.querySelector(`[data-port-id="${conn.endPortId}"][data-port-type="in"]`);

    if (startEl && endEl) {
      const sRect = startEl.getBoundingClientRect();
      const eRect = endEl.getBoundingClientRect();

      const x1 = sRect.left - canvasRect.left + (sRect.width / 2);
      const y1 = sRect.top - canvasRect.top + (sRect.height / 2);
      const x2 = eRect.left - canvasRect.left + (eRect.width / 2);
      const y2 = eRect.top - canvasRect.top + (eRect.height / 2);

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const cp1x = x1 + (x2 - x1) / 2;
      const d = `M ${x1} ${y1} C ${cp1x} ${y1}, ${cp1x} ${y2}, ${x2} ${y2}`;
      
      path.setAttribute('d', d);
      path.setAttribute('stroke', '#6366f1');
      path.setAttribute('stroke-width', '3');
      path.setAttribute('fill', 'none');
      path.setAttribute('style', 'pointer-events: visibleStroke; cursor: pointer;');
      
      path.oncontextmenu = (e) => {
        e.preventDefault();
        connections.value = connections.value.filter(c => c.lineId !== conn.lineId);
        updateLines();
      };
      
      svgLayer.appendChild(path);
    }
  });
};



const confirmResourceAssociation = () => {
  showToast('资料关联成功', 'success');
  showResourceLibrary.value = false;
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

.port {
  width: 14px;
  height: 14px;
  background: #fff;
  border: 2px solid #6366f1;
  border-radius: 50%;
  cursor: crosshair;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 50;
  transition: all 0.2s;
  pointer-events: auto;
}
.port:hover {
  transform: translateY(-50%) scale(1.3);
  background: #6366f1;
}
.port.active {
  background: #6366f1;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}
.port-in {
  left: -7px;
}
.port-out {
  right: -7px;
}

.flow-line {
  fill: none;
  stroke: #6366f1;
  stroke-width: 3;
  stroke-linecap: round;
  pointer-events: stroke;
  cursor: pointer;
  transition: stroke 0.2s;
}
.flow-line:hover {
  stroke: #ef4444;
  stroke-width: 4;
  filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.3));
}
.no-scrollbar::-webkit-scrollbar { display: none; }
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
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

/* AI智能出题弹窗样式 */
.ai-modal-card {
  width: 430px;
  background: white;
  border-radius: 22px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  padding: 32px;
  box-sizing: border-box;
}

.ai-modal-header {
  margin-bottom: 26px;
}

.ai-modal-header h3 {
  margin: 0;
  font-size: 1.45rem;
  font-weight: 600;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 12px;
}

.rag-badge {
  font-size: 13px;
  font-weight: normal;
  background: #eef2ff;
  color: #4f46e5;
  padding: 4px 11px;
  border-radius: 14px;
  margin-left: auto;
}

.ai-modal-body {
  margin-bottom: 26px;
}

.form-group {
  margin-bottom: 26px;
}

.form-label {
  display: block;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 11px;
  color: #111827;
}

.input-control {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  font-size: 16px;
  line-height: 1.6;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  background: #f9fafb;
  resize: none;
  color: #111827;
}

.input-control:focus {
  outline: none;
  border-color: rgba(79, 70, 229, 0.3);
  background: white;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.05);
}

.options-row {
  display: flex;
  gap: 22px;
  margin-bottom: 26px;
}

.option-item {
  flex: 1;
}

.option-item select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236b7280'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 17px;
}

.option-item select:disabled {
  cursor: not-allowed;
  background-image: none;
  opacity: 0.7;
}

.ai-modal-footer {
  display: flex;
  gap: 14px;
}

.btn {
  flex: 1;
  padding: 14px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-confirm {
  background: #4f46e5;
  color: white;
  flex: 2;
}

.btn-confirm:hover {
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.btn-cancel {
  background: #f9fafb;
  color: #6b7280;
}

.btn:active {
  transform: translateY(0);
}

.share-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
  z-index: 100;
}

.share-modal-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.share-modal {
  background: #ffffff;
  width: 560px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  padding: 24px;
  position: relative;
}

.share-modal-close {
  position: absolute;
  top: 24px;
  right: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #999;
  font-size: 22px;
  line-height: 1;
  transition: color 0.2s;
}

.share-modal-close:hover {
  color: #666;
}

.share-modal-title {
  font-size: 22px;
  font-weight: bold;
  color: #222222;
  text-align: center;
  margin-bottom: 24px;
  margin-top: 10px;
}

.share-modal-form-group {
  margin-bottom: 20px;
}

.share-modal-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #444;
  margin-bottom: 8px;
}

.share-modal-hint {
  font-size: 13px;
  color: #909399;
  margin-bottom: 12px;
}

.share-modal-link-section {
  display: flex;
  gap: 10px;
}

.share-modal-url {
  flex: 1;
  background-color: #fff;
  height: 40px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: border-color 0.2s;
}

.share-modal-url:focus {
  border-color: #007bff;
}

.share-modal-url-placeholder {
  flex: 1;
  background-color: #f5f7fa;
  height: 40px;
  border: 1px dashed #c0c4cc;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
}

.share-modal-input {
  width: 100%;
  height: 40px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 0 12px;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: border-color 0.2s;
}

.share-modal-input:focus {
  border-color: #007bff;
}

.share-modal-btn {
  height: 40px;
  padding: 0 24px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.share-modal-btn:hover {
  opacity: 0.9;
}

.share-modal-copy {
  background-color: #28a745;
  color: white;
  white-space: nowrap;
}

.share-modal-footer {
  margin-top: 32px;
  margin-bottom: 8px;
  display: flex;
  justify-content: center;
}

.share-modal-confirm {
  background-color: #007bff;
  color: white;
  min-width: 120px;
}

.share-modal-copy.copied {
  background-color: #17a2b8;
}

.datetime-row {
  display: flex;
  gap: 10px;
}

.date-picker,
.time-picker {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-picker-icon {
  font-size: 16px;
}

.share-modal-confirm {
  background-color: #007bff;
  color: white;
}

.share-modal-confirm:hover {
  background-color: #0056b3;
}

.resource-library-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  z-index: 50;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.resource-library-overlay.active {
  opacity: 1;
  pointer-events: auto;
  background-color: rgba(0, 0, 0, 0.5);
}

.resource-library-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100%;
  background-color: #ffffff;
  box-shadow: -20px 0 25px -5px rgba(0, 0, 0, 0.05), -10px 0 10px -5px rgba(0, 0, 0, 0.02);
  transform: translateX(100%);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  border-left: 1px solid #f0f0f0;
}

.resource-library-overlay.active .resource-library-panel {
  transform: translateX(0);
}

.resource-library-header {
  padding: 32px;
  border-bottom: 1px solid #f0f0f0;
}

.resource-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.resource-library-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.resource-library-close {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: transparent !important;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  font-size: 20px;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resource-library-close:hover {
  color: #6b7280;
  background-color: #f3f4f6 !important;
  background: #f3f4f6 !important;
}

.resource-library-body {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.resource-search-container {
  width: 100%;
  margin-top: 8px;
}

.search-box-inner {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #f1f5f9;
  border-radius: 16px;
  height: 48px;
  padding: 0 6px 0 16px;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.search-box-inner:focus-within {
  background: #ffffff;
  border-color: #6366f1;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
}

.search-icon-left {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  flex-shrink: 0;
}

.resource-search-input-new {
  flex: 1;
  height: 100%;
  background: transparent;
  border: none;
  font-size: 14px;
  color: #1f2937;
  outline: none;
  padding: 0;
}

.search-action-btn {
  background: #6366f1;
  color: white;
  padding: 0 16px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.1s;
  margin-left: 8px;
}

.search-action-btn:active {
  transform: scale(0.96);
  background: #4f46e5;
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resource-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.resource-item:hover {
  border-color: #c4b5fd;
  background: rgba(139, 92, 246, 0.03);
}

.resource-item.selected {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.08);
}

.resource-checkbox-wrapper {
  margin-right: 14px;
}

.resource-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: #ffffff;
}

.resource-checkbox:hover {
  border-color: #8b5cf6;
}

.resource-checkbox.checked {
  background: #8b5cf6;
  border-color: #8b5cf6;
}

.check-icon {
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
}

.resource-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
  margin-right: 16px;
}

.pdf-icon {
  background: #fef2f2;
  color: #ef4444;
}

.doc-icon {
  background: #eff6ff;
  color: #3b82f6;
}

.ppt-icon {
  background: #fff7ed;
  color: #f97316;
}

.resource-info {
  flex: 1;
  min-width: 0;
}

.resource-name {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resource-meta {
  display: block;
  font-size: 10px;
  color: #9ca3af;
}

.resource-checkbox {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #d1d5db;
  color: #6366f1;
  cursor: pointer;
  flex-shrink: 0;
}

.resource-checkbox:checked {
  background-color: #6366f1;
  border-color: #6366f1;
}

.resource-upload-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  border: 2px dashed #e5e7eb;
  border-radius: 32px;
  cursor: pointer;
  color: #9ca3af;
  transition: all 0.2s;
  margin-top: 24px;
}

.resource-upload-btn:hover {
  border-color: #e0e7ff;
  color: #6366f1;
  background: #faf5ff;
}

.upload-icon {
  font-size: 32px;
  font-weight: 300;
  margin-bottom: 8px;
}

.resource-library-footer {
  padding: 32px;
  border-top: 1px solid #f0f0f0;
}

.resource-confirm-btn {
  width: 100%;
  padding: 16px;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 20px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.2);
}

.resource-confirm-btn:hover {
  background: #531dab;
  box-shadow: 0 4px 12px rgba(114, 46, 209, 0.3);
}

.rag-modal-card {
  width: 560px;
  height: 680px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 20px 50px rgba(148, 163, 184, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s ease;
}

.rag-modal-card:hover {
  box-shadow: 0 25px 60px rgba(148, 163, 184, 0.35);
}

.rag-modal-header {
  flex-shrink: 0;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 22px;
  color: #0f172a;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 0.5px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  background: rgba(241, 245, 249, 0.7);
  padding: 6px;
  border-radius: 14px;
  margin-bottom: 20px;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 8px 0;
  font-size: 13px;
  color: #64748b;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  text-transform: uppercase;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab:hover {
  color: #334155;
  background: rgba(255, 255, 255, 0.6);
}

.tab.active {
  color: #4f46e5;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12);
}

.rag-modal-body {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 24px;
  padding-right: 4px;
}

.rag-modal-body::-webkit-scrollbar {
  width: 0px;
}

.section-label {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 12px;
  display: block;
  font-weight: 500;
}

.upload-status {
  font-size: 14px;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 16px;
  text-align: center;
  font-weight: 500;
}

.upload-status.success {
  background: #ecfdf5;
  color: #10b981;
}

.upload-status.error {
  background: #fef2f2;
  color: #ef4444;
}

.upload-status.loading {
  background: #eff6ff;
  color: #3b82f6;
}

.file-item {
  font-size: 14px;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 16px;
  text-align: center;
  font-weight: 500;
}

.upload-status.success {
  background: #ecfdf5;
  color: #10b981;
}

.upload-status.error {
  background: #fef2f2;
  color: #ef4444;
}

.upload-status.loading {
  background: #eff6ff;
  color: #3b82f6;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 16px 20px;
  border-radius: 18px;
  margin-bottom: 12px;
  animation: listBreathe 4s ease-in-out infinite;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.file-icon {
  width: 42px;
  height: 42px;
  background: #eef2ff;
  color: #4f46e5;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 11px;
}

.file-details .name {
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
  margin-bottom: 3px;
}

.file-details .size {
  font-size: 12px;
  color: #94a3b8;
  width: 80px;
  text-align: left;
}

.status-badge {
  font-size: 12px;
  color: #10b981;
  background: #ecfdf5;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 500;
}

.rag-modal-footer {
  flex-shrink: 0;
}

.dropzone {
  border: 2px dashed #cbd5e1;
  border-radius: 18px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  background: rgba(248, 250, 252, 0.6);
  transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

.dropzone:hover {
  border-color: #6366f1;
  background: rgba(99, 102, 241, 0.03);
  transform: scale(1.01);
}

.plus-icon-container {
  width: 48px;
  height: 48px;
  background: #4f46e5;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px auto;
  font-size: 26px;
  font-weight: 300;
  position: relative;
  transition: transform 0.3s ease, background 0.3s ease;
}

.plus-icon-container::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4);
  animation: iconPulse 2.5s infinite cubic-bezier(0.25, 0, 0, 1);
}

.dropzone:hover .plus-icon-container {
  transform: scale(1.08);
  background: #4338ca;
}

.dropzone-text {
  font-size: 14px;
  color: #475569;
  font-weight: 500;
}

.dropzone-hint {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 6px;
}

@keyframes listBreathe {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);
  }
  50% {
    transform: scale(1.008);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.04);
    border-color: rgba(99, 102, 241, 0.15);
  }
}

@keyframes iconPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.5);
  }
  70% {
    box-shadow: 0 0 0 12px rgba(79, 70, 229, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(79, 70, 229, 0);
  }
}
</style>
