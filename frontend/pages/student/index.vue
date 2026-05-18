<template>
  <view class="page mobile-page">
    <view class="fixed-header">
      <view class="status-bar"></view>
      
      <view class="header-top">
        <view class="avatar-box">
          <image class="avatar-img" src="/static/logo.png" mode="aspectFill"></image>
        </view>
        <view class="search-wrapper">
          <input class="search-input" type="text" placeholder="搜索作业题目" placeholder-style="color:#bbb" />
          <text class="search-icon">🔍</text>
        </view>
        <view class="action-icons">
          <view class="icon-item">
            <text>🔔</text>
            <view class="dot"></view>
          </view>
        </view>
      </view>
    </view>

    <scroll-view class="main-content" scroll-y>
      <view class="filter-bar">
        <text class="time-label">七天内</text>
        <view class="share-entry" @click="showShareInput">
          <text>🔗</text>
          <text class="share-text">输入分享码</text>
        </view>
      </view>
      
      <!-- 分享码输入弹窗 -->
      <view v-if="showShareDialog" class="share-dialog-mask" @click="closeShareDialog">
        <view class="share-dialog" @click.stop>
          <view class="dialog-header">
            <text class="dialog-title">输入分享码</text>
          </view>
          <view class="dialog-body">
            <input 
              class="share-input" 
              v-model="inputShareCode" 
              placeholder="请输入分享码" 
              placeholder-style="color:#999"
            />
          </view>
          <view class="dialog-footer">
            <button class="dialog-btn dialog-btn-cancel" @click="closeShareDialog">取消</button>
            <button class="dialog-btn dialog-btn-confirm" @click="submitShareCode">确定</button>
          </view>
        </view>
      </view>

      <view v-if="tasks.length === 0" class="empty-state">
        <text class="empty-text">暂无作业</text>
      </view>
      <view class="card" v-for="(item, index) in tasks" :key="index" @click="goToAssignmentDetail(index)">
        <view class="card-header">
          <text :class="['tag', item.statusType]">{{ item.statusText }}</text>
        </view>
        <view class="card-title">{{ item.title }}</view>
        <view class="card-footer">
          <text class="deadline">截止: {{ item.deadline }}</text>
          
          <view 
            v-if="item.statusType === 'expired'" 
            class="report-link" 
            @click.stop="goToReport(index)"
          >
            <text class="report-icon">📊</text>
            <text class="report-text">查看报告</text>
          </view>
          <view 
            v-if="item.statusType === 'expired'" 
            class="rank-link" 
            @click.stop="goToRank(index)"
          >
            <text class="rank-icon">🏆</text>
            <text class="rank-text">查看排行</text>
          </view>
        </view>
      </view>
      
      <view class="safe-bottom"></view>
    </scroll-view>
  </view>
</template>

<script>
import request from '@/utils/request.js';

export default {
  data() {
    return {
      tasks: [],
      loading: false,
      showShareDialog: false,
      inputShareCode: ''
    };
  },
  onLoad(options) {
    console.log('学生页面 onLoad, options:', options);
    if (options.share_code) {
      this.handleShareCode(options.share_code);
    } else {
      this.loadAssignments();
    }
  },
  onShow() {
    console.log('=== 学生页面 onShow ===');
    console.log('当前页面路径:', getCurrentPages()[0]?.route);
    console.log('当前页面参数:', getCurrentPages()[0]?.options);
    
    // 先检查页面参数中是否有 share_code
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    if (currentPage && currentPage.options && currentPage.options.share_code) {
      const shareCode = currentPage.options.share_code;
      console.log('✅ 从页面参数获取到 share_code:', shareCode);
      this.handleShareCode(shareCode);
      return;
    }
    
    // 检查是否有待处理的share_code（如果从App.vue直接跳转过来）
    const pendingShareCode = uni.getStorageSync('pendingShareCode');
    console.log('从 Storage 获取到 pendingShareCode:', pendingShareCode);
    console.log('pendingShareCode 类型:', typeof pendingShareCode);
    console.log('pendingShareCode 长度:', pendingShareCode ? pendingShareCode.length : 0);
    
    if (pendingShareCode && pendingShareCode.length > 0) {
      console.log('✅ 找到待处理的分享码，准备处理:', pendingShareCode);
      // 先移除再处理，避免重复处理
      uni.removeStorageSync('pendingShareCode');
      this.handleShareCode(pendingShareCode);
    } else {
      console.log('没有待处理的分享码，加载作业列表');
      this.loadAssignments();
    }
  },
  methods: {
    async loadAssignments() {
      try {
        const userInfo = uni.getStorageSync('userInfo');
        console.log('用户信息:', userInfo);
        
        if (!userInfo || !userInfo.user_id) {
          console.log('用户未登录或user_id不存在');
          return;
        }
        
        this.loading = true;
        console.log('正在请求作业列表...');
        const res = await request.get(`/api/student/${userInfo.user_id}/assignments`);
        console.log('作业列表响应:', res);
        
        if (res && res.success) {
          this.tasks = res.data || [];
          console.log('加载了', this.tasks.length, '个作业');
        } else {
          console.log('请求失败:', res);
          uni.showToast({ title: res.message || '加载失败', icon: 'none' });
        }
      } catch (error) {
        console.error('加载作业列表失败:', error);
        uni.showToast({ title: '加载失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    async handleShareCode(shareCode) {
      try {
        console.log('='.repeat(60));
        console.log('===== 开始处理分享码 =====');
        console.log('传入的 shareCode:', JSON.stringify(shareCode));
        console.log('shareCode 类型:', typeof shareCode);
        console.log('shareCode 长度:', shareCode ? shareCode.length : 0);
        
        // 空值检查
        if (!shareCode || String(shareCode).trim() === '') {
          console.log('❌ shareCode 为空或无效');
          uni.showToast({ title: '分享码无效', icon: 'none' });
          return;
        }
        
        // 转换为字符串并清洗
        const shareCodeStr = String(shareCode);
        const cleanShareCode = shareCodeStr.trim();
        console.log('清洗后的 shareCode:', JSON.stringify(cleanShareCode));
        console.log('清洗后的长度:', cleanShareCode.length);
        
        const userInfo = uni.getStorageSync('userInfo');
        console.log('用户信息:', JSON.stringify(userInfo));
        
        if (!userInfo || !userInfo.user_id) {
          console.log('❌ 用户未登录或user_id不存在');
          uni.showToast({ title: '请先登录', icon: 'none' });
          return;
        }
        
        // 直接用 uni.request 发送，绕过封装，方便调试！
        uni.showLoading({ title: '加载作业中...' });
        
        // 关键！student_id 作为 Query 参数放在 URL 后面！
        const requestUrl = 'http://192.168.1.39:8000/api/student/share/' + cleanShareCode + '?student_id=' + userInfo.user_id;
        
        console.log('🚀 发送请求详情:');
        console.log('  完整 URL:', requestUrl);
        console.log('  请求方式: POST');
        console.log('  Query 参数 (student_id):', userInfo.user_id);
        
        // 直接使用 uni.request，不通过封装
        uni.request({
          url: requestUrl,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          success: (response) => {
            console.log('📦 收到响应:');
            console.log('  状态码:', response.statusCode);
            console.log('  响应头:', JSON.stringify(response.header));
            console.log('  响应数据:', JSON.stringify(response.data));
            
            uni.hideLoading();
            
            const res = response.data;
            if (res && res.success) {
              uni.showToast({ title: '作业获取成功', icon: 'success' });
              console.log('✅ 成功！准备重新加载作业列表');
              this.loadAssignments();
            } else {
              console.log('❌ 业务失败，响应:', JSON.stringify(res));
              uni.showToast({ 
                title: res?.message || '获取作业失败', 
                icon: 'none',
                duration: 2000
              });
            }
          },
          fail: (error) => {
            uni.hideLoading();
            console.log('❌ 网络请求失败:');
            console.log('  错误信息:', JSON.stringify(error));
            uni.showModal({
              title: '网络错误',
              content: '请求失败: ' + JSON.stringify(error),
              showCancel: false
            });
          }
        });
        
      } catch (error) {
        uni.hideLoading();
        console.log('❌ 异常捕获:');
        console.log('  错误对象:', JSON.stringify(error));
        console.log('  错误堆栈:', error.stack);
        uni.showToast({ title: '处理失败', icon: 'none' });
      }
    },
    goToAssignmentDetail(index) {
      const task = this.tasks[index];
      uni.navigateTo({
        url: `/pages/task/AssignmentDetail?id=${task.assignment_id}&status=${task.statusType}`
      });
    },
    goToReport(index) {
      const task = this.tasks[index];
      uni.navigateTo({
        url: `/pages/task/ReportDetail?id=${task.assignment_id}`
      });
    },
    goToRank(index) {
      const task = this.tasks[index];
      uni.navigateTo({
        url: `/pages/task/RankList?id=${task.assignment_id}`
      });
    },
    // 显示分享码输入弹窗
    showShareInput() {
      this.inputShareCode = '';
      this.showShareDialog = true;
    },
    // 关闭分享码输入弹窗
    closeShareDialog() {
      this.showShareDialog = false;
      this.inputShareCode = '';
    },
    // 提交分享码
    async submitShareCode() {
      const code = this.inputShareCode.trim();
      if (!code) {
        uni.showToast({ title: '请输入分享码', icon: 'none' });
        return;
      }
      
      this.closeShareDialog();
      await this.handleShareCode(code);
    }
  }
};
</script>

<style lang="scss" scoped>
.page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  .empty-text {
    color: #999;
    font-size: 14px;
  }
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #ffffff;
  z-index: 999;
  
  .status-bar { height: var(--status-bar-height); }

  .header-top {
    display: flex;
    align-items: center;
    padding: 8px 15px;
    
    .avatar-box {
      width: 34px;
      height: 34px;
      background: #f0f0f0;
      border-radius: 50%;
      overflow: hidden;
      margin-right: 12px;
      .avatar-img { width: 100%; height: 100%; }
    }
    
    .search-wrapper {
      flex: 1;
      height: 36px;
      background: #f2f3f5;
      border-radius: 18px;
      display: flex;
      align-items: center;
      padding: 0 12px;
      .search-icon { font-size: 14px; margin-right: 6px; }
      .search-input { flex: 1; font-size: 14px; }
    }

    .action-icons {
      margin-left: 15px;
      display: flex;
      .icon-item {
        position: relative;
        font-size: 22px;
        .dot {
          position: absolute;
          top: 2px; right: 0;
          width: 8px; height: 8px;
          background: #ff4d4f;
          border: 1px solid #fff;
          border-radius: 50%;
        }
      }
    }
  }
}

.main-content {
  padding-top: calc(var(--status-bar-height) + 52px);
  padding-left: 15px;
  padding-right: 15px;

  .filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    .time-label { font-size: 13px; color: #999; }
    .filter-icons text { margin-left: 15px; color: #666; font-size: 18px; }
    .share-entry {
      display: flex;
      align-items: center;
      padding: 6px 12px;
      background: #f0f2f5;
      border-radius: 16px;
      .share-text {
        font-size: 13px;
        color: #667eea;
        margin-left: 4px;
      }
    }
  }
  
  /* 分享码弹窗样式 */
  .share-dialog-mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }
  
  .share-dialog {
    width: 80%;
    max-width: 300px;
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
  }
  
  .dialog-header {
    padding: 16px 20px;
    text-align: center;
    border-bottom: 1px solid #f0f0f0;
    .dialog-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }
  }
  
  .dialog-body {
    padding: 20px;
    .share-input {
      width: 100%;
      height: 44px;
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 0 12px;
      font-size: 14px;
    }
  }
  
  .dialog-footer {
    display: flex;
    border-top: 1px solid #f0f0f0;
    .dialog-btn {
      flex: 1;
      height: 48px;
      line-height: 48px;
      text-align: center;
      font-size: 15px;
      border: none;
      background: none;
    }
    .dialog-btn-cancel {
      color: #666;
      border-right: 1px solid #f0f0f0;
    }
    .dialog-btn-confirm {
      color: #667eea;
      font-weight: 600;
    }
  }
}

.card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-sizing: border-box;
  width: auto;
  margin-left: 0;
  margin-right: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); 
  border: 1rpx solid #f0f0f0; 

  .card-header { 
    margin-bottom: 10px; 
    .tag { 
      font-size: 12px; 
      padding: 2px 8px; 
      border-radius: 4px; 
      display: inline-block;
      &.processing { background: #e8f2ff; color: #007aff; } 
      &.submitted { background: #e7f7ef; color: #07c160; } 
      &.expired { background: #f2f2f2; color: #999; } 
    } 
  }
  
  .card-title { 
    font-size: 18px; 
    font-weight: bold; 
    color: #333; 
    margin-bottom: 12px;
    word-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    line-height: 1.4;
  }
  
  .deadline { font-size: 14px; color: #999; }
  
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;

    .deadline {
      font-size: 13px;
      color: #999;
    }

    .report-link {
      display: flex;
      align-items: center;
      background-color: #e6f7ff;
      padding: 4px 10px;
      border-radius: 100px;
      border: 1px solid #91d5ff;
      margin-right: 8px;

      .report-icon {
        font-size: 12px;
        margin-right: 4px;
      }

      .report-text {
        font-size: 12px;
        color: #1890ff;
        font-weight: 500;
      }
    }

    .rank-link {
      display: flex;
      align-items: center;
      background-color: #fff7e6;
      padding: 4px 10px;
      border-radius: 100px;
      border: 1px solid #ffe58f;

      .rank-icon {
        font-size: 12px;
        margin-right: 4px;
      }

      .rank-text {
        font-size: 12px;
        color: #d48806;
        font-weight: 500;
      }
    }
  }
}
.safe-bottom { height: 20px; }
</style>