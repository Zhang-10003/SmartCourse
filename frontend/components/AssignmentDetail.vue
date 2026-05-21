<template>
  <view class="assignment-detail">
    <view class="back-btn" @click="close">
      <text class="back-arrow">←</text>
      <text class="back-text">返回列表</text>
    </view>

    <header class="detail-header">
      <view class="header-left">
        <view class="title-row">
          <h2 class="detail-title">{{ assignment.title }}</h2>
          
          <view class="share-wrapper">
            <view 
              class="share-trigger-btn" 
              :class="{ 'is-active': showSharePopover }"
              @click="toggleSharePopover"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
              </svg>
            </view>
            
            <view 
              class="share-popover"
              :class="{ 'show': showSharePopover }"
              @click.stop
            >
              <view class="popover-content">
                <h3 class="popover-title">作业分享入口</h3>
        <p class="popover-desc">学生点击链接即可打开 SmartCourse App 查看作业</p>
                <view class="link-group">
                  <input 
                    type="text" 
                    readonly 
                    :value="shareLink" 
                    class="share-input"
                  >
                  <view 
                    class="copy-btn" 
                    :class="{ 'success': copySuccess }"
                    @click="copyShareLink"
                  >
                    <text>{{ copySuccess ? '已复制' : '复制' }}</text>
                  </view>
                </view>
              </view>
            </view>
          </view>
        </view>
        <p class="detail-subtitle">数据统计与实时排行榜分析</p>
      </view>
      <view class="header-actions">
        <view class="time-display">
          <text class="time-label-text">剩余时间</text>
          <text class="time-countdown">{{ remainingTimeText }}</text>
        </view>
        <view class="btn-deadline">
          <text>立即截止</text>
        </view>
        <view class="btn-secondary">
          <text>导出报表</text>
        </view>
        <view class="btn-primary">
          <text>提醒未交学生</text>
        </view>
      </view>
    </header>

    <view class="metrics-grid">
      <view class="metric-card">
        <text class="metric-label">已提交人数</text>
        <view class="metric-value-row">
          <view class="score-display">
            <text class="metric-number">{{ stats.submittedCount || 0 }}</text>
            <text class="metric-divider"> / </text>
            <text class="metric-number small">{{ stats.totalStudents || 0 }}</text>
          </view>
        </view>
      </view>
      <view class="metric-card">
        <text class="metric-label">平均得分</text>
        <view class="metric-value-row">
          <view class="score-display">
            <text class="metric-number purple">{{ stats.avgScore || 0 }}</text>
            <text class="metric-divider"> / </text>
            <text class="metric-number small purple">{{ stats.totalScore || 0 }}</text>
          </view>
        </view>
      </view>
      <view class="metric-card">
        <text class="metric-label">优秀率</text>
        <view class="metric-value-row">
          <text class="metric-number green">{{ stats.excellentRate }}</text>
        </view>
      </view>
      <view class="metric-card alert-border">
        <text class="metric-label">高频错题</text>
        <view class="metric-value-row">
          <text class="metric-number red">{{ stats.hardestQuestion }}</text>
          <text class="metric-badge red-text">错误率 {{ stats.hardestErrorRate }}</text>
        </view>
      </view>
    </view>

    <view class="charts-row">
      <view class="chart-card pie-card">
        <h3 class="chart-title">成绩分布概览</h3>
        <view class="pie-container">
          <view class="css-donut-chart"></view>
          <view class="chart-legends">
            <view class="legend-item">
              <view class="legend-dot legend-dot-indigo"></view>
              <text>优秀</text>
            </view>
            <view class="legend-item">
              <view class="legend-dot legend-dot-light-indigo"></view>
              <text>良好</text>
            </view>
            <view class="legend-item">
              <view class="legend-dot legend-dot-pale-indigo"></view>
              <text>及格</text>
            </view>
            <view class="legend-item">
              <view class="legend-dot legend-dot-slate"></view>
              <text>待加强</text>
            </view>
          </view>
        </view>
      </view>
      
      <view class="chart-card bar-card">
        <view class="chart-header">
          <h3 class="chart-title">各题目正确率 (%)</h3>
        </view>
        <view class="bar-chart-wrapper">
          <view class="chart-y-axis">
            <text>100</text>
            <text>80</text>
            <text>60</text>
            <text>40</text>
            <text>20</text>
            <text>0</text>
          </view>
          <view 
            class="bar-scroll-area"
            @mousedown="startDrag"
            @mousemove="onDrag"
            @mouseup="stopDrag"
            @mouseleave="stopDrag"
          >
            <view 
              class="bar-columns" 
              :class="{ 'bar-columns-evenly': questionScores.length <= 8, 'bar-columns-scrollable': questionScores.length > 8 }"
            >
              <view class="bar-column" v-for="(item, index) in questionScores" :key="index">
                <view 
                  class="bar-active-fill"
                  :style="{ 
                    height: item.score * 1.8 + 'px', 
                    backgroundColor: item.color
                  }"
                ></view>
                <text class="bar-label">{{ item.label }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="table-card">
      <view class="table-header">
        <view class="table-title-row">
          <text class="table-title">学生提交排行</text>
        </view>
        <view class="tab-group">
          <view 
            class="tab-item" 
            :class="{ 'active': currentSubmitTab === 'submitted' }"
            @click="currentSubmitTab = 'submitted'"
          >
            <text>已提交 ({{ submittedStudents.length }})</text>
          </view>
          <view 
            class="tab-item" 
            :class="{ 'active': currentSubmitTab === 'unsubmitted' }"
            @click="currentSubmitTab = 'unsubmitted'"
          >
            <text>未提交 ({{ unsubmittedStudents.length }})</text>
          </view>
        </view>
      </view>
      
      <view class="table-labels">
        <view class="label-cell student-info-label">学生信息</view>
        <view v-if="currentSubmitTab === 'submitted'" class="label-cell time-label">提交时间</view>
        <view v-if="currentSubmitTab === 'submitted'" class="label-cell status-label">状态</view>
        <view v-if="currentSubmitTab === 'submitted'" class="label-cell score-label">得分</view>
        <view class="label-cell action-label">操作</view>
      </view>
      
      <view v-if="currentSubmitTab === 'submitted'" class="table-body">
        <view 
          class="table-row"
          v-for="(student, index) in submittedStudents" 
          :key="index"
          :class="{ 'has-border': index < submittedStudents.length - 1 }"
        >
          <view class="row-cell student-info">
            <view class="avatar-icon">
              <text>{{ student.name.charAt(0) }}</text>
            </view>
            <view class="student-details">
              <text class="student-name">{{ student.name }}</text>
              <text class="student-meta">{{ student.className }} · {{ student.id }}</text>
            </view>
          </view>
          <view class="row-cell time-cell">
            <text>{{ student.submitTime }}</text>
          </view>
          <view class="row-cell status-cell">
            <view class="status-badge">
              <text>{{ student.status }}</text>
            </view>
          </view>
          <view class="row-cell score-cell">
            <text class="score-text">{{ student.score }}</text>
          </view>
          <view class="row-cell action-cell">
            <view class="text-link">
              <text>查看答案</text>
            </view>
          </view>
        </view>
      </view>
      
      <view v-else class="table-body">
        <view 
          class="table-row"
          v-for="(student, index) in unsubmittedStudents" 
          :key="index"
          :class="{ 'has-border': index < unsubmittedStudents.length - 1 }"
        >
          <view class="row-cell student-info">
            <view class="avatar-icon avatar-slate">
              <text>{{ student.name.charAt(0) }}</text>
            </view>
            <view class="student-details">
              <text class="student-name">{{ student.name }}</text>
              <text class="student-meta">{{ student.className }} · {{ student.id }}</text>
            </view>
          </view>
          <view class="row-cell empty-cell"></view>
          <view class="row-cell empty-cell"></view>
          <view class="row-cell empty-cell"></view>
          <view class="row-cell action-cell">
            <view class="text-link orange-link">
              <text>提醒提交</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'AssignmentDetail',
  props: {
    assignment: {
      type: Object,
      required: true,
      default: () => ({
        title: '',
        deadline: '',
        deadline_ts: 0,
        status: '',
        participants: [],
        share_code: ''
      })
    },
    stats: {
      type: Object,
      default: () => ({
        submittedCount: 0,
        totalStudents: 0,
        avgScore: 0,
        totalScore: 0,
        excellentRate: '0%',
        hardestQuestion: '—',
        hardestErrorRate: '0%'
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
  },
  data() {
    return {
      currentSubmitTab: 'submitted',
      showSharePopover: false,
      copySuccess: false,
      isDragging: false,
      startX: 0,
      scrollLeftStart: 0,
      remainingSeconds: 0,
      timer: null
    };
  },
  computed: {
    shareLink() {
      if (this.assignment.share_code) {
        // 使用 HTTP 格式，浏览器可以访问，页面中会尝试唤醒 app
        return 'http://192.168.1.39:8000/share/' + this.assignment.share_code;
      }
      // 备用格式
      return 'http://192.168.1.39:8000/share/';
    },
    remainingTimeText() {
      let seconds = this.remainingSeconds;
      if (seconds <= 0) return '已截止';
      
      const days = Math.floor(seconds / (24 * 60 * 60));
      seconds %= (24 * 60 * 60);
      
      const hours = Math.floor(seconds / (60 * 60));
      seconds %= (60 * 60);
      
      const minutes = Math.floor(seconds / 60);
      seconds %= 60;
      
      const pad = (num) => num.toString().padStart(2, '0');
      
      if (days > 0) {
        return `${days}:${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
      } else {
        return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
      }
    }
  },
  methods: {
    close() {
      this.$emit('close');
    },
    toggleSharePopover(e) {
      e.stopPropagation();
      this.showSharePopover = !this.showSharePopover;
    },
    async copyShareLink(e) {
      e.stopPropagation();
      try {
        await navigator.clipboard.writeText(this.shareLink);
        this.copySuccess = true;
        setTimeout(() => {
          this.copySuccess = false;
        }, 1800);
      } catch (err) {
        console.error('复制失败', err);
      }
    },
    closePopover(e) {
      if (this.showSharePopover && !e.target.closest('.share-wrapper')) {
        this.showSharePopover = false;
      }
    },
    startDrag(e) {
      this.isDragging = true;
      this.startX = e.pageX;
      const scrollArea = this.$el.querySelector('.bar-scroll-area');
      if (scrollArea) {
        this.scrollLeftStart = scrollArea.scrollLeft;
      }
    },
    onDrag(e) {
      if (!this.isDragging) return;
      const scrollArea = this.$el.querySelector('.bar-scroll-area');
      if (scrollArea) {
        const walk = e.pageX - this.startX;
        scrollArea.scrollLeft = this.scrollLeftStart - walk;
      }
    },
    stopDrag() {
      this.isDragging = false;
    },
    startCountdown() {
      this.timer = setInterval(() => {
        if (this.remainingSeconds > 0) {
          this.remainingSeconds--;
        }
      }, 1000);
    },
    stopCountdown() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.closePopover);
    this.startCountdown();
  },
  watch: {
    'assignment.deadline_ts': {
      immediate: true,
      handler(ts) {
        if (ts) {
          this.remainingSeconds = Math.max(0, Math.floor(ts - Date.now() / 1000));
        }
      }
    }
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closePopover);
    this.stopCountdown();
  }
};
</script>

<style scoped>
.assignment-detail {
  width: 100%;
}

.back-btn {
  display: flex;
  align-items: center;
  color: #94a3b8;
  margin-bottom: 24px;
  cursor: pointer;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #4f46e5;
}

.back-arrow {
  font-size: 18px;
  margin-right: 8px;
}

.back-text {
  font-weight: 600;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}

.header-left {
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.detail-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.share-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.share-trigger-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.15s ease;
}

.share-trigger-btn:hover {
  background: #f1f5f9;
  color: #4f46e5;
}

.share-trigger-btn.is-active {
  background: #4f46e5;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.share-popover {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 12px;
  z-index: 50;
  width: 380px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(26, 29, 44, 0.08), 0 4px 12px rgba(79, 70, 229, 0.04);
  border: 1px solid rgba(226, 231, 240, 0.6);
  display: none;
}

.share-popover.show {
  display: block;
  animation: popoverFade 0.15s ease;
}

@keyframes popoverFade {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.popover-content {
  padding: 24px;
}

.popover-title {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px 0;
}

.popover-desc {
  font-size: 12px;
  color: #94a3b8;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.link-group {
  display: flex;
  gap: 8px;
}

.share-input {
  flex: 1;
  height: 34px;
  padding: 0 10px;
  font-size: 12px;
  color: #475569;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  outline: none;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}

.copy-btn {
  height: 34px;
  padding: 0 14px;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
  background: #4f46e5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-btn.success {
  background: #22c55e;
}

.detail-subtitle {
  font-size: 14px;
  color: #4f46e5;
  font-weight: 500;
  margin: 8px 0 0 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.time-display {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  padding: 0;
  background: transparent;
  border: none;
  margin-right: 32px;
}

.time-label-text {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 500;
  margin-bottom: 0;
  margin-right: 12px;
}

.time-countdown {
  font-size: 28px;
  font-weight: 800;
  color: #4f46e5;
  letter-spacing: 2px;
  font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
}

.btn-deadline {
  background: #fff;
  border: 1px solid #f87171;
  color: #f87171;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.btn-deadline:hover {
  background: #fef2f2;
}

.btn-secondary {
  background: #fff;
  border: 1px solid #e2e8f0;
  color: #475569;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.btn-primary {
  background: #4f46e5;
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.metric-card {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(138, 149, 229, 0.04);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 140px;
  position: relative;
}

.metric-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
  display: block;
}

.metric-value-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
}

.metric-value-row.left {
  justify-content: flex-start;
}

.score-display {
  display: flex;
  align-items: flex-end;
}


.metric-number {
  font-size: 36px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.metric-number.purple {
  color: #4f46e5;
}

.metric-number.green {
  color: #22c55e;
}

.metric-number.red {
  color: #f87171;
}

.metric-number.small {
  font-size: 24px;
  font-weight: 600;
  color: #94a3b8;
}

.metric-divider {
  font-size: 24px;
  font-weight: 600;
  color: #cbd5e1;
  margin: 0 4px;
}

.metric-badge {
  font-size: 12px;
  font-weight: 700;
  color: #22c55e;
}

.metric-badge.red-text {
  color: #fb7185;
  opacity: 0.7;
}

.metric-target {
  font-size: 10px;
  color: #cbd5e1;
  margin-bottom: 4px;
}

.mini-progress-bar {
  width: 64px;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
  margin-bottom: 8px;
}

.mini-progress-fill {
  width: 78%;
  height: 100%;
  background: #4f46e5;
  border-radius: 4px;
}

.metric-card.alert-border {
  border-left: 4px solid #fb7185;
}

.charts-row {
  display: grid;
  grid-template-columns: 34% 64%;
  gap: 2%;
  margin-bottom: 32px;
}

.chart-card {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(138, 149, 229, 0.04);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.pie-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 240px;
}

.css-donut-chart {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: conic-gradient(
    #4f46e5 0% 45%, 
    #818cf8 45% 75%, 
    #c7d2fe 75% 90%, 
    #f1f5f9 90% 100%
  );
  position: relative;
  margin-bottom: 24px;
}

.css-donut-chart::before {
  content: '';
  position: absolute;
  top: 25px;
  left: 25px;
  width: 110px;
  height: 110px;
  background: #fff;
  border-radius: 50%;
}

.chart-legends {
  display: flex;
  justify-content: center;
  gap: 16px;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 6px;
}

.legend-dot-indigo {
  background: #4f46e5;
}

.legend-dot-light-indigo {
  background: #818cf8;
}

.legend-dot-pale-indigo {
  background: #c7d2fe;
}

.legend-dot-slate {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
}

.bar-chart-wrapper {
  display: flex;
  height: 200px;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.chart-y-axis {
  flex-shrink: 0;
  width: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: 8px;
}

.chart-y-axis text {
  font-size: 10px;
  color: #94a3b8;
  text-align: right;
}

.bar-scroll-area {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  cursor: grab;
  position: relative;
  scroll-behavior: smooth;
}

.bar-scroll-area:active {
  cursor: grabbing;
}

.bar-scroll-area::-webkit-scrollbar {
  display: none;
}

.bar-columns {
  display: flex;
  align-items: flex-end;
  height: 100%;
  padding: 0 20px;
}

.bar-columns-evenly {
  justify-content: space-around;
  width: 100%;
}

.bar-columns-scrollable {
  gap: 24px;
  width: auto;
  min-width: max-content;
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  min-width: 60px;
  flex-shrink: 0;
}

.bar-active-fill {
  width: 32px;
  border-radius: 6px 6px 0 0;
  transition: transform 0.3s ease;
}

.bar-label {
  font-size: 12px;
  font-weight: 700;
  color: #1e293b;
  margin-top: 12px;
  white-space: nowrap;
}

.table-card {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(138, 149, 229, 0.04);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.table-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.tab-group {
  background: #f8fafc;
  padding: 4px;
  border-radius: 10px;
  display: flex;
}

.tab-item {
  padding: 6px 16px;
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.15s;
}

.tab-item.active {
  background: #fff;
  color: #4f46e5;
  box-shadow: 0 2px 6px rgba(79, 70, 229, 0.06);
}

.table-labels {
  display: flex;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 500;
  padding: 16px 0;
  border-bottom: 1px solid #f8fafc;
}

.label-cell {
  flex: 1;
}

.student-info-label {
  flex: 1;
}

.time-label {
  flex: 1;
  text-align: center;
}

.status-label {
  flex: 1;
  text-align: center;
}

.score-label {
  flex: 1;
  text-align: center;
}

.action-label {
  flex: 1;
  text-align: right;
}

.table-body {
  display: block;
}

.table-row {
  display: flex;
  align-items: center;
  padding: 18px 0;
  transition: background 0.2s;
}

.table-row:hover {
  background: rgba(248, 250, 252, 0.5);
}

.table-row.has-border {
  border-bottom: 1px solid #f8fafc;
}

.row-cell {
  flex: 1;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.avatar-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5, #a855f7);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.avatar-slate {
  background: #e2e8f0;
  color: #64748b;
}

.student-details {
  display: flex;
  flex-direction: column;
}

.student-name {
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.student-meta {
  font-size: 12px;
  color: #94a3b8;
}

.time-cell {
  text-align: center;
  font-size: 12px;
  color: #64748b;
}

.status-cell {
  display: flex;
  justify-content: center;
}

.status-badge {
  background: #f0fdf4;
  color: #22c55e;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.score-cell {
  text-align: center;
}

.score-text {
  font-weight: 700;
  color: #1e293b;
  font-size: 16px;
}

.action-cell {
  display: flex;
  justify-content: flex-end;
}

.text-link {
  color: #4f46e5;
  font-weight: 600;
  text-decoration: none;
  background: #eef2ff;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
}

.orange-link {
  color: #ea580c;
  background: #fff7ed;
}

.empty-cell {
  flex: 1;
}
</style>
