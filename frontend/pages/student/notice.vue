<template>
  <view class="container mobile-page">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="nav-title">消息通知</text>
        <text class="nav-action" @click="markAllAsRead">全部已读</text>
      </view>
    </view>

    <view class="notice-list">
      <view 
        class="notice-card" 
        v-for="msg in notices" 
        :key="msg.message_id"
        @click="handleDetail(msg)"
      >
        <view class="card-header">
          <view class="title-section">
            <view class="unread-dot" v-if="!msg.is_read"></view>
            <text class="notice-title">{{ msg.title }}</text>
          </view>
          <text class="notice-time">{{ formatTime(msg.created_at) }}</text>
        </view>
        
        <view class="notice-content">{{ msg.content }}</view>
        
        <view class="card-footer">
          <text class="detail-btn">查看详情</text>
          <text class="cuIcon-right icon"></text>
        </view>
      </view>
      
      <view v-if="notices.length === 0" class="empty-state">
        <text class="empty-text">暂无消息</text>
      </view>
    </view>
  </view>
</template>

<script>
import request from '@/utils/request.js';

export default {
  data() {
    return {
      notices: []
    };
  },
  onLoad() {
    this.loadMessages();
  },
  methods: {
    formatTime(timeStr) {
      if (!timeStr) return '';
      
      try {
        const now = new Date();
        const messageTime = new Date(timeStr);
        const diff = now - messageTime;
        
        const minutes = Math.floor(diff / (1000 * 60));
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        
        if (minutes < 1) {
          return '刚刚';
        } else if (minutes < 60) {
          return `${minutes}分钟前`;
        } else if (hours < 24) {
          return `${hours}小时前`;
        } else if (days < 7) {
          return `${days}天前`;
        } else {
          const month = String(messageTime.getMonth() + 1).padStart(2, '0');
          const day = String(messageTime.getDate()).padStart(2, '0');
          const hour = String(messageTime.getHours()).padStart(2, '0');
          const minute = String(messageTime.getMinutes()).padStart(2, '0');
          return `${month}-${day} ${hour}:${minute}`;
        }
      } catch (e) {
        console.error('时间格式化失败:', e);
        return '';
      }
    },
    
    async loadMessages() {
      try {
        const userInfo = uni.getStorageSync('userInfo');
        console.log('用户信息:', userInfo);
        
        if (!userInfo || !userInfo.user_id) {
          console.log('用户未登录或user_id不存在');
          return;
        }
        
        const res = await request.get(`/api/students/${userInfo.user_id}/messages`);
        console.log('消息列表响应:', res);
        
        if (res && res.success) {
          this.notices = res.data || [];
          console.log('加载了', this.notices.length, '条消息');
        } else {
          console.log('请求失败:', res);
          uni.showToast({ title: res.message || '加载失败', icon: 'none' });
        }
      } catch (error) {
        console.error('加载消息列表失败:', error);
        uni.showToast({ title: '加载失败', icon: 'none' });
      }
    },
    
    async markAsRead(messageId) {
      try {
        const res = await request.put(`/api/messages/${messageId}/read`);
        console.log('标记已读响应:', res);
        
        if (res && res.success) {
          const msg = this.notices.find(m => m.message_id === messageId);
          if (msg) {
            msg.is_read = true;
          }
        }
      } catch (error) {
        console.error('标记已读失败:', error);
      }
    },
    
    async markAllAsRead() {
      try {
        const userInfo = uni.getStorageSync('userInfo');
        if (!userInfo || !userInfo.user_id) {
          return;
        }
        
        const res = await request.put(`/api/students/${userInfo.user_id}/messages/read-all`);
        console.log('全部已读响应:', res);
        
        if (res && res.success) {
          this.notices.forEach(msg => {
            msg.is_read = true;
          });
          uni.showToast({ title: '已全部标记为已读', icon: 'success' });
        }
      } catch (error) {
        console.error('全部已读失败:', error);
      }
    },
    
    handleDetail(msg) {
      console.log('查看消息详情:', msg);
      
      if (!msg.is_read) {
        this.markAsRead(msg.message_id);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: #f8f9fa;
}

.custom-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1rpx solid #eee;

  .status-bar {
    height: var(--status-bar-height);
    width: 100%;
  }

  .nav-content {
    height: 44px;
    padding: 0 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    .nav-title {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      font-size: 18px;
      font-weight: 700;
      color: #2d3436;
    }
    
    .nav-action {
      font-size: 14px;
      color: #007aff;
      margin-left: auto;
    }
  }
}

.notice-list {
  padding: calc(var(--status-bar-height) + 60px) 15px 30px;
}

.notice-card {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 18px;
  margin-bottom: 15px;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.03);
  transition: transform 0.2s;

  &:active {
    transform: scale(0.98);
    background: #fafafa;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .title-section {
      display: flex;
      align-items: center;
      
      .unread-dot {
        width: 8px;
        height: 8px;
        background: #ff4d4f;
        border-radius: 50%;
        margin-right: 8px;
        flex-shrink: 0;
      }
      
      .notice-title {
        font-weight: 600;
        font-size: 16px;
        color: #2d3436;
      }
    }

    .notice-time {
      color: #b2bec3;
      font-size: 12px;
      flex-shrink: 0;
      margin-left: 10px;
    }
  }

  .notice-content {
    color: #636e72;
    font-size: 14px;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
  }

  .card-footer {
    margin-top: 15px;
    padding-top: 12px;
    border-top: 1rpx solid #f1f2f6;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .detail-btn {
      font-size: 13px;
      color: #007aff;
      font-weight: 500;
    }
    
    .icon {
      color: #dfe6e9;
      font-size: 12px;
    }
  }
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 100rpx 0;
  
  .empty-text {
    color: #b2bec3;
    font-size: 14px;
  }
}
</style>
