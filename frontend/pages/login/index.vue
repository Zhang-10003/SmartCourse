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
            <view class="remember-me" @tap="handleRememberClick">
              <checkbox 
                :checked="rememberChecked" 
                color="#2979ff" 
                style="transform:scale(0.6); pointer-events: none;" 
              />
              <text>记住我</text>
            </view>
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
import request from '@/utils/request.js'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rememberChecked: false,
      loading: false
    }
  },
  onLoad() {
    console.log('登录页面 onLoad');
    this.loadRememberedPassword();
  },
  methods: {
    // 统一处理点击“记住我”区域的逻辑
    handleRememberClick() {
      this.rememberChecked = !this.rememberChecked;
      console.log('记住我状态切换至:', this.rememberChecked);
    },
    
    // 加载存储的信息
    loadRememberedPassword() {
      try {
        const remembered = uni.getStorageSync('rememberedUser');
        if (remembered && remembered.username) {
          const now = Date.now();
          // 检查是否在有效期内
          if (remembered.expireTime && remembered.expireTime > now) {
            this.form.username = remembered.username;
            this.form.password = remembered.password;
            this.rememberChecked = true;
            console.log('已成功填充记住的信息');
          } else {
            uni.removeStorageSync('rememberedUser');
            console.log('信息已过期，已清除');
          }
        }
      } catch (e) {
        console.error('读取存储失败', e);
      }
    },
    
    // 保存信息逻辑
    saveRememberedPassword() {
      if (this.rememberChecked) {
        const threeDays = 3 * 24 * 60 * 60 * 1000;
        const data = {
          username: this.form.username,
          password: this.form.password,
          expireTime: Date.now() + threeDays
        };
        uni.setStorageSync('rememberedUser', data);
        console.log('已执行保存逻辑');
      } else {
        uni.removeStorageSync('rememberedUser');
        console.log('已执行清除逻辑');
      }
    },
    
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        uni.showToast({ title: '请输入账号密码', icon: 'none' });
        return;
      }
      
      this.loading = true;
      
      try {
        const responseData = await request.post('/auth/login', {
          username: this.form.username,
          password: this.form.password
        });
        
        // 判断登录成功的条件（根据你的接口返回结构，这里假设有 user_id 或 access_token）
        if (responseData && (responseData.user_id || responseData.access_token)) {
          
          // 1. 处理记住密码逻辑
          this.saveRememberedPassword();
          
          // 2. 存储用户信息
          uni.setStorageSync('userInfo', responseData);
          
          // 3. 成功时不弹窗，直接跳转
          const userType = String(responseData.user_type);
          if (userType === '1') {
            uni.switchTab({ url: '/pages/student/index' });
          } else {
            uni.switchTab({ url: '/pages/teacher/index' });
          }
          
        } else {
          // 4. 业务逻辑上的失败（例如：密码错误，responseData 里带着错误信息）
          const msg = responseData.message || responseData.error || '登录失败，请检查账号密码';
          uni.showModal({
            title: '登录失败',
            content: msg,
            showCancel: false,
            confirmColor: '#2979ff'
          });
        }
      } catch (error) {
        // 5. 网络请求失败或服务器宕机
        console.error('登录请求异常:', error);
        uni.showModal({
          title: '网络异常',
          content: '无法连接到服务器，请检查网络设置',
          showCancel: false
        });
      } finally {
        this.loading = false;
      }
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
  align-items: center;
  min-height: 100vh;
  background-color: $bg-light;
}

.content-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: -120rpx;
  z-index: 10;
}

.app-logo {
  margin-bottom: 60rpx;
  .app-name {
    font-size: 52rpx;
    font-weight: 900;
    color: $text-main;
    letter-spacing: 6rpx;
  }
}

.login-card {
  width: 90%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 60rpx 40rpx;
  box-sizing: border-box;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.05);
}

.header-section {
  margin-bottom: 50rpx;
  .main-title {
    font-size: 42rpx;
    font-weight: 800;
  }
  .title-bar {
    width: 44rpx;
    height: 6rpx;
    background: $primary-color;
    margin: 12rpx 0;
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
  }
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10rpx 0 50rpx;
  font-size: 26rpx;
  
  .remember-me {
    display: flex;
    align-items: center;
    color: $text-grey;
    /* 增加点击区域，提升体验 */
    padding: 10rpx 0; 
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
  font-weight: 600;
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
  }
}

.bg-decoration-top {
  position: absolute;
  top: -100rpx;
  right: -100rpx;
  width: 400rpx;
  height: 400rpx;
  background: radial-gradient(circle, rgba(41, 121, 255, 0.1) 0%, transparent 70%);
}
</style>