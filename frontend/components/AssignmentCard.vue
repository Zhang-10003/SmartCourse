<template>
  <view class="assignment-card">
    <view class="card-header">
      <view :class="statusClass" class="status-tag">
        <text>{{ status }}</text>
      </view>
      <view class="card-menu" @click="handleMenuClick">•••</view>
    </view>
    
    <view class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-due">{{ deadline }}</p>
    </view>
    
    <view class="card-footer">
      <view v-if="status === '进行中'" class="participants-wrapper">
        <view class="participants">
          <view 
            v-for="(participant, idx) in displayParticipants" 
            :key="idx"
            :class="participant.bgClass"
            class="participant-avatar"
          >
            <text>{{ participant.initial }}</text>
          </view>
        </view>
      </view>
      
      <view v-if="status === '进行中'" class="action-link" @click="handleDetailClick">
        <text>查看详情 →</text>
      </view>
      
      <view v-if="status === '已截止'" class="ranking-btn-wrap">
        <view class="ranking-btn" @click="handleRankingClick">
          <text>🏆</text>
          <text>查看排行</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'AssignmentCard',
  props: {
    title: {
      type: String,
      required: true
    },
    deadline: {
      type: String,
      required: true
    },
    status: {
      type: String,
      required: true,
      validator: (value) => ['进行中', '已截止'].includes(value)
    },
    participants: {
      type: Array,
      default: () => [
        { initial: 'A', bgClass: 'bg-indigo-100 text-indigo-600' },
        { initial: 'B', bgClass: 'bg-emerald-100 text-emerald-600' },
        { initial: '+12', bgClass: 'bg-slate-100 text-slate-400' }
      ]
    }
  },
  computed: {
    statusClass() {
      return this.status === '进行中' ? 'status-in-progress' : 'status-completed';
    },
    displayParticipants() {
      return this.participants.slice(0, 3);
    }
  },
  methods: {
    handleMenuClick() {
      this.$emit('menu-click');
    },
    handleDetailClick() {
      this.$emit('detail-click');
    },
    handleRankingClick() {
      this.$emit('ranking-click');
    }
  }
};
</script>

<style scoped>
.assignment-card {
  background: #fff;
  border-radius: 24px;
  border: 1px solid #f1f5f9;
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.assignment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.status-tag {
  font-size: 10px;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-in-progress {
  background: #dbeafe;
  color: #2563eb;
}

.status-completed {
  background: #f3f4f6;
  color: #6b7280;
}

.card-menu {
  color: #cbd5e1;
  cursor: pointer;
  font-size: 14px;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.2s;
}

.card-menu:hover {
  color: #64748b;
}

.card-body {
  margin-bottom: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.card-due {
  font-size: 14px;
  color: #94a3b8;
  margin: 0;
}

.card-footer {
  padding-top: 16px;
  border-top: 1px solid #f8fafc;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.participants-wrapper {
  flex: 1;
}

.participants {
  display: flex;
}

.participant-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  border: 2px solid #fff;
  margin-left: -8px;
}

.participant-avatar:first-child {
  margin-left: 0;
}

.action-link {
  color: #4f46e5;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.2s;
}

.action-link:hover {
  color: #4338ca;
}

.ranking-btn-wrap {
  display: flex;
  justify-content: flex-end;
}

.ranking-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #fffbeb;
  border: 1px solid #fef3c7;
  border-radius: 12px;
  color: #d97706;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.ranking-btn:hover {
  background: #fef3c7;
}
</style>