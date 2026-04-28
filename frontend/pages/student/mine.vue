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
          <text class="user-name">张俊琛</text>
          <text class="user-id">学号: 20260101</text>
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

<script setup>
const handlePassword = () => {
  uni.navigateTo({ url: '/pages/login/forget' });
};

const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出当前账号吗？',
    success: (res) => {
      if (res.confirm) {
        // 退出逻辑
      }
    }
  });
};
</script>

<style lang="scss" scoped>
.page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 导航栏样式 */
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

/* 主内容区域 */
.main-content {
  padding-top: calc(var(--status-bar-height) + 44px);
}

/* 用户卡片：移除 margin-bottom 使其与下方内容对接 */
.user-profile-card {
  background: #ffffff;
  padding: 30px 20px;
  margin-bottom: 0; /* 彻底移除与下方的间隙 */
  display: flex;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  /* 增加底部细微分割线，区分头像区和功能区 */
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

/* 菜单组：移除 margin 且去掉顶部边框，实现无缝连接 */
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

    /* 内部按钮分割线 */
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