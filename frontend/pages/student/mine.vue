<template>
  <view class="page mobile-page">
    <view class="custom-navbar">
      <view class="status-bar"></view>
      <view class="nav-content">
        <text class="nav-title">个人中心</text>
      </view>
    </view>

    <scroll-view class="main-content" scroll-y>
      <view class="user-profile-card">
        <view class="avatar-box">
          <image class="avatar-img" src="/static/logo.png" mode="aspectFill"></image>
        </view>
        <view class="info-content">
          <text class="user-name">{{ studentName || '未登录' }}</text>
          <text class="user-id">学号: {{ studentNo || '' }}</text>
        </view>
      </view>

      <view class="menu-group">
        <view class="menu-cell" hover-class="cell-hover" @click="handlePassword">
          <view class="cell-left">
            <text class="cell-title">修改登录密码</text>
          </view>
          <text class="arrow">></text>
        </view>

        <view class="menu-cell" hover-class="cell-hover" @click="handleLogout">
          <view class="cell-left">
            <text class="cell-title logout-text">退出当前账号</text>
          </view>
          <text class="arrow">></text>
        </view>
      </view>
      
      <view class="safe-bottom"></view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      studentName: '',
      studentNo: ''
    };
  },
  onLoad() {
    this.loadUserInfo();
  },
  onShow() {
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
      const userInfo = uni.getStorageSync('userInfo');
      console.log('用户信息:', userInfo);
      console.log('userInfo.student_name:', userInfo?.student_name);
      console.log('userInfo.student_no:', userInfo?.student_no);
      
      if (userInfo) {
        this.studentName = userInfo.student_name || userInfo.name || userInfo.username || '';
        this.studentNo = userInfo.student_no || userInfo.user_no || '';
      }
      console.log('设置后的 studentName:', this.studentName);
      console.log('设置后的 studentNo:', this.studentNo);
    },
    
    handlePassword() {
      uni.navigateTo({ url: '/pages/login/forget' });
    },

    handleLogout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出当前账号吗？',
        success: (res) => {
          if (res.confirm) {
            uni.removeStorageSync('userInfo');
            uni.redirectTo({ url: '/pages/login/index' });
          }
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.custom-navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 999;
  background-color: #ffffff;
  border-bottom: 1rpx solid #f0f0f0;

  .status-bar { height: var(--status-bar-height); }
  .nav-content {
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    .nav-title { font-size: 17px; font-weight: 700; color: #333; }
  }
}

.main-content {
  padding-top: calc(var(--status-bar-height) + 44px);
}

.user-profile-card {
  background: #ffffff;
  padding: 30px 20px;
  margin-bottom: 0;
  display: flex;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  border-bottom: 1rpx solid #f8f8f8; 

  .avatar-box {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    overflow: hidden;
    background: #f8f9fa;
    margin-right: 15px;
    border: 2px solid #fff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    .avatar-img { width: 100%; height: 100%; }
  }

  .info-content {
    .user-name { font-size: 22px; font-weight: bold; color: #1a1a1a; display: block; }
    .user-id { font-size: 14px; color: #999; margin-top: 4px; display: block; }
  }
}

.menu-group {
  background: #ffffff;
  margin: 0; 
  width: 100%;
  border-bottom: 1rpx solid #f0f0f0;
  box-sizing: border-box;

  .menu-cell {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 20px;
    background: #ffffff;
    transition: background 0.2s;

    &:not(:last-child) {
      border-bottom: 1rpx solid #f8f8f8;
    }

    &.cell-hover { background: #fafafa; }

    .cell-left {
      display: flex;
      align-items: center;
      .cell-title { font-size: 16px; color: #333; font-weight: 500; }
      .logout-text { color: #ff4d4f; }
    }

    .arrow { color: #d1d1d1; font-size: 14px; }
  }
}

.safe-bottom { height: 40px; }
</style>
