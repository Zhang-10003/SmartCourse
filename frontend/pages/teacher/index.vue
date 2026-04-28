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

    <main class="flex-1 overflow-y-auto p-4 lg:p-8 relative no-scrollbar">
      
      <view v-if="currentTab === 'design'" class="animate-in fade-in duration-500">
        <header class="flex flex-col lg:flex-row lg:justify-between lg:items-end mb-10 gap-4">
          <view>
            <h1 class="text-3xl font-bold text-slate-900">我的作业流</h1>
            <p class="text-slate-500 mt-2">拖拽左侧题型组件至画布，构建您的智能课件。</p>
          </view>
          <view class="flex gap-4">
            <button class="bg-white border border-slate-200 px-6 py-3 rounded-2xl font-semibold shadow-sm hover:bg-slate-50 transition-all">导出预览</button>
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
              class="node-element absolute glass-panel p-5 rounded-[24px] cursor-pointer hover:scale-105 transition-all duration-300 z-10 border border-white shadow-lg"
              :style="{ left: node.x + 'px', top: node.y + 'px', minWidth: '200px' }"
              @click.stop="openEditor(node, index)"
            >
              <view class="flex justify-between items-center mb-4">
                <text class="text-[10px] font-bold text-slate-400 tracking-widest uppercase">NODE_{{ index + 1 }}</text>
                <view :class="node.color" class="w-2.5 h-2.5 rounded-full shadow-sm"></view>
              </view>
              <view class="font-bold text-slate-800 mb-3">{{ node.type }}</view>
              
              <view class="space-y-2">
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

      <view v-else class="animate-in slide-in-from-right duration-500">
        <header class="mb-10">
          <h1 class="text-3xl font-bold text-slate-900">作业管理中心</h1>
          <p class="text-slate-500 mt-2">在这里追踪所有已发布作业的收集情况与数据分析。</p>
        </header>

        <view class="space-y-12">
            <section>
                <view class="flex items-center gap-3 mb-6">
                    <view class="w-1 h-6 bg-indigo-600 rounded-full"></view>
                    <text class="text-lg font-bold text-slate-800">今天发布</text>
                    <text class="text-xs bg-slate-100 text-slate-500 px-2 py-1 rounded-md">2 项任务</text>
                </view>
                <view class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <view class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm hover:shadow-md transition-all">
                        <view class="flex justify-between items-start mb-4">
                            <text class="px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg uppercase">进行中</text>
                            <text class="text-slate-300">•••</text>
                        </view>
                        <h3 class="text-lg font-bold text-slate-900 mb-2">计算机网络周测 - TCP原理</h3>
                        <p class="text-sm text-slate-400 mb-6">截止: 05-10 18:00</p>
                        <view class="pt-4 border-t border-slate-50 flex justify-between items-center">
                            <view class="flex -space-x-2">
                                <view class="w-7 h-7 rounded-full bg-indigo-100 border-2 border-white flex items-center justify-center text-[10px] text-indigo-600 font-bold">A</view>
                                <view class="w-7 h-7 rounded-full bg-emerald-100 border-2 border-white flex items-center justify-center text-[10px] text-emerald-600 font-bold">B</view>
                            </view>
                            <text class="text-xs font-bold text-indigo-600">查看详情 →</text>
                        </view>
                    </view>
                </view>
            </section>
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
        class="absolute top-0 right-0 h-full w-full md:w-[500px] bg-white shadow-2xl transition-transform duration-500 flex flex-col"
        :style="{ transform: drawer.show ? 'translateX(0)' : 'translateX(100%)' }"
      >
        <view class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <view>
            <h2 class="text-2xl font-bold text-slate-900">{{ drawer.title }}</h2>
            <p class="text-slate-500 text-sm mt-1">SmartCourse 配置引擎</p>
          </view>
          <button @click="drawer.show = false" class="p-2 hover:bg-white rounded-full shadow-sm text-slate-400">×</button>
        </view>

        <view class="flex-1 overflow-y-auto p-8 space-y-6">
          <view>
            <label class="block text-sm font-bold text-slate-700 uppercase mb-3">题目内容</label>
            <textarea 
              v-model="drawer.editingNode.content"
              class="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl outline-none focus:ring-2 focus:ring-indigo-500" 
              rows="4" 
              placeholder="在此输入题目描述..."
            ></textarea>
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
import { ref, reactive, onMounted, onUnmounted } from 'vue';

const currentTab = ref('design');
const nodes = ref([]);
const drawer = reactive({
  show: false,
  title: '',
  editingNode: { content: '' },
  currentIndex: -1
});

const toolset = [
  { type: '单选题', color: 'bg-blue-500' },
  { type: '多选题', color: 'bg-purple-500' },
  { type: '代码填空', color: 'bg-emerald-500' },
  { type: '匹配题', color: 'bg-orange-500' },
  { type: '判断题', color: 'bg-rose-500' }
];

// 【核心修复 1】：改用全局 mousePos 存储 page 坐标
let draggingItem = null;
const mousePos = { x: 0, y: 0 };

const updateMousePos = (e) => {
  // pageX 包含页面滚动偏移，在 H5 容器中计算最稳
  mousePos.x = e.pageX || e.clientX;
  mousePos.y = e.pageY || e.clientY;
};

onMounted(() => {
  // 使用 capture 模式确保在拖拽期间也能捕获到位置
  window.addEventListener('mousemove', updateMousePos, true);
  // 部分浏览器在拖拽时只触发 dragover，补充一层保障
  window.addEventListener('dragover', updateMousePos, true);
});

onUnmounted(() => {
  window.removeEventListener('mousemove', updateMousePos, true);
  window.removeEventListener('dragover', updateMousePos, true);
});

const onDragStart = (e, item) => {
  draggingItem = item;
  const nativeEvent = e.nativeEvent || e;
  if (nativeEvent.dataTransfer) {
    nativeEvent.dataTransfer.setData('text/plain', item.type);
    nativeEvent.dataTransfer.effectAllowed = "move";
  }
};

const onDrop = (e) => {
  e.preventDefault();
  if (!draggingItem) return;

  // 【核心修复 2】：同步强行获取画布真实位置
  const canvasElement = document.querySelector('.node-canvas-bg');
  if (!canvasElement) return;

  // 获取画布相对于文档的绝对偏移
  const rect = canvasElement.getBoundingClientRect();
  const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  // 画布在文档中的绝对坐标
  const canvasDocX = rect.left + scrollLeft;
  const canvasDocY = rect.top + scrollTop;

  /**
   * 【核心修复 3】：坐标逻辑对齐
   * 鼠标文档坐标 - 画布文档坐标 - 节点中心偏移
   */
  let x = mousePos.x - canvasDocX - 100;
  let y = mousePos.y - canvasDocY - 40;

  console.log('PagePos:', mousePos.x, mousePos.y, 'CanvasDoc:', canvasDocX, canvasDocY);

  // 极端防御：如果算出来还是挤在左边（说明 rect.left 拿到的不对）
  // 增加最小安全边距
  if (x < 0) x = 20; 
  if (y < 0) y = 20;

  nodes.value.push({
    id: Date.now(),
    type: draggingItem.type,
    color: draggingItem.color,
    x: x,
    y: y,
    content: ''
  });
  
  draggingItem = null;
};

// --- 其他 UI 逻辑保持不变 ---
const openEditor = (node, index) => {
  drawer.title = `编辑：${node.type} (#${index + 1})`;
  drawer.editingNode = { ...node };
  drawer.currentIndex = index;
  drawer.show = true;
};

const saveNode = () => {
  if (drawer.currentIndex !== -1) {
    nodes.value[drawer.currentIndex] = { ...drawer.editingNode };
    drawer.show = false;
  }
};

const deleteNode = () => {
  if (drawer.currentIndex !== -1) {
    nodes.value.splice(drawer.currentIndex, 1);
    drawer.show = false;
  }
};

const saveWorkflow = () => {
  uni.showToast({ title: '保存成功', icon: 'success' });
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
  -webkit-backdrop-filter: blur(16px);
}

/* 锚点交互：模仿 HTML 中的 group-hover */
.node-element:hover .anchor-left {
  border-color: #4f46e5;
}
.node-element:hover .anchor-right {
  background-color: #4f46e5;
}

.no-scrollbar::-webkit-scrollbar { display: none; }

.animate-in {
  animation: fadeIn 0.4s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>