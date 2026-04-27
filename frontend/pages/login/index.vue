<template>
  <view class="page-wrapper">
    <view class="bg-decoration-top"></view>
    <view class="bg-decoration-bottom"></view>

    <view class="content-container">
      <view class="app-logo">
        <text class="app-name">课程助手</text>
      </view>

      <view class="login-card">
        <view class="header-section">
          <text class="main-title">欢迎登录</text>
          <view class="title-bar"></view>
        </view>

        <view class="form-content">
          <view class="input-item">
            <text class="iconfont icon-user"></text>
            <input 
              type="text" 
              v-model="form.username" 
              placeholder="用户名 / 邮箱" 
              placeholder-class="input-placeholder"
            />
          </view>
          
          <view class="input-item">
            <text class="iconfont icon-lock"></text>
            <input 
              type="password" 
              v-model="form.password" 
              placeholder="请输入密码" 
              placeholder-class="input-placeholder"
            />
          </view>

          <view class="action-bar">
            <label class="remember-me" @tap="toggleRemember">
              <checkbox :checked="form.remember" color="#2979ff" style="transform:scale(0.6)" />
              <text>记住我</text>
            </label>
            <text class="forget-pwd">忘记密码？</text>
          </view>

          <button 
            :loading="loading" 
            class="submit-btn" 
            @tap="handleLogin"
            hover-class="btn-hover"
          >
            <text v-if="!loading">立即登录</text>
          </button>
        </view>

        <view class="footer-section">
          <text>还没有账号？</text>
          <text class="register-text">立即注册</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      form: { username: '', password: '', remember: false },
      loading: false
    }
  },
  methods: {
    toggleRemember() {
      this.form.remember = !this.form.remember;
    },
    handleLogin() {
      if (!this.form.username || !this.form.password) {
        uni.showToast({ title: '请输入账号密码', icon: 'none' });
        return;
      }
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
        uni.showToast({ title: '登录成功' });
      }, 1500);
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-color: #2979ff;
$bg-light: #f0f3f8;
$text-main: #1d1e2c;
$text-grey: #94a3b8;

.page-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center; /* 基础居中 */
  min-height: 100vh;
  background-color: $bg-light;
  overflow: hidden;
}

/* 内容容器上移 */
.content-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 通过负的 margin-top 让整体内容（Logo+卡片）往上方挪 */
  margin-top: -120rpx; 
  z-index: 10;
}

.app-logo {
  margin-bottom: 60rpx; /* 压缩 Logo 与卡片间距 */
  .app-name {
    font-size: 52rpx;
    font-weight: 900;
    color: #1d1e2c;
    letter-spacing: 6rpx;
    text-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
  }
}

.login-card {
  /* 调小侧边距：增加宽度百分比 */
  width: 90%; 
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 48rpx;
  /* 调小内部左右边距 */
  padding: 60rpx 40rpx; 
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
}

.header-section {
  margin-bottom: 50rpx;
  .main-title {
    font-size: 42rpx;
    font-weight: 800;
    color: $text-main;
  }
  .title-bar {
    width: 44rpx;
    height: 6rpx;
    background: $primary-color;
    margin: 12rpx 0;
    border-radius: 10rpx;
  }
}

.input-item {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 2rpx solid #f1f5f9;
  border-radius: 24rpx;
  padding: 0 24rpx;
  margin-bottom: 24rpx;
  height: 96rpx;
  
  input {
    flex: 1;
    font-size: 28rpx;
    color: $text-main;
  }
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10rpx 0 50rpx;
  font-size: 24rpx;
  
  .remember-me {
    display: flex;
    align-items: center;
    color: $text-grey;
  }
  .forget-pwd { color: $primary-color; }
}

.submit-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: linear-gradient(135deg, $primary-color 0%, #0056e0 100%);
  color: #fff;
  border-radius: 24rpx;
  font-size: 30rpx;
  font-weight: 600;
  box-shadow: 0 10rpx 20rpx rgba(41, 121, 255, 0.2);
  &::after { border: none; }
}

.footer-section {
  margin-top: 50rpx;
  text-align: center;
  font-size: 26rpx;
  color: $text-grey;
  .register-text {
    color: $text-main;
    font-weight: bold;
    margin-left: 10rpx;
    text-decoration: underline;
  }
}

/* 装饰背景保持不变 */
.bg-decoration-top {
  position: absolute;
  top: -100rpx;
  right: -100rpx;
  width: 400rpx;
  height: 400rpx;
  background: radial-gradient(circle, rgba(41, 121, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}
</style>