<template>
    <view class="page-wrapper">
        <view class="bg-decoration-top"></view>
        <view class="bg-decoration-bottom"></view>

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
.app-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 80rpx; /* 与下方登录卡片的间距 */
    z-index: 10;
}

.app-name {
    font-size: 52rpx;        /* 字体大小 */
    font-weight: 900;       /* 加粗 */
    color: #1d1e2c;         /* 深色文字，也可改为 $primary-color 变成蓝色 */
    letter-spacing: 6rpx;   /* 字间距，增加高级感 */
    text-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05); /* 微弱阴影 */
}
.page-wrapper {
	display: flex;
	flex-direction: column; /* 改为纵向排列，让 logo 在卡片上方 */
	justify-content: center;
	align-items: center;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: $bg-light;
    padding: 0 40rpx; // 强制增加左右外边距保护，防止贴边
    overflow: hidden;
}

.bg-decoration-top {
    position: absolute;
    top: -100rpx;
    right: -100rpx;
    width: 400rpx;
    height: 400rpx;
    background: radial-gradient(circle, rgba(41, 121, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.login-card {
    position: relative;
    z-index: 10;
    /* 关键修改：调整宽度比例并限制最大宽度 */
    width: 82%; 
    max-width: 380px; 
    
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 48rpx; // 稍微增加圆角，配合留白更显高级
    padding: 70rpx 50rpx;
    box-shadow: 
        0 20px 40px -10px rgba(0, 0, 0, 0.05),
        0 30px 60px -15px rgba(0, 0, 0, 0.1);
}

.header-section {
    margin-bottom: 60rpx;
    .main-title {
        font-size: 44rpx; // 稍微缩小一点，更精致
        font-weight: 800;
        color: $text-main;
        letter-spacing: 2rpx;
    }
    .title-bar {
        width: 50rpx;
        height: 6rpx;
        background: $primary-color;
        margin: 16rpx 0;
        border-radius: 10rpx;
    }
    .sub-title {
        font-size: 24rpx;
        color: $text-grey;
    }
}

.input-item {
    display: flex;
    align-items: center;
    background: #f8fafc;
    border: 2rpx solid #f1f5f9;
    border-radius: 28rpx;
    padding: 0 30rpx;
    margin-bottom: 30rpx;
    height: 100rpx;
    transition: all 0.2s ease-in-out;

    &:focus-within {
        background: #fff;
        border-color: $primary-color;
        box-shadow: 0 0 0 6rpx rgba(41, 121, 255, 0.08);
    }

    input {
        flex: 1;
        font-size: 28rpx;
        color: $text-main;
    }
}

.input-placeholder {
    color: #cbd5e1;
    font-size: 28rpx;
}

.action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10rpx 0 60rpx;
    
    .remember-me {
        display: flex;
        align-items: center;
        font-size: 24rpx;
        color: $text-grey;
    }
    
    .forget-pwd {
        font-size: 24rpx;
        color: $primary-color;
    }
}

.submit-btn {
    width: 100%;
    height: 100rpx;
    line-height: 100rpx;
    background: linear-gradient(135deg, $primary-color 0%, #0056e0 100%);
    color: #fff;
    border-radius: 28rpx;
    font-size: 30rpx;
    font-weight: 600;
    border: none;
    box-shadow: 0 10rpx 20rpx rgba(41, 121, 255, 0.25);
    display: flex;
    justify-content: center;
    align-items: center;
    
    &::after { border: none; }
}

.btn-hover {
    transform: translateY(2rpx);
    filter: brightness(1.1);
}

.footer-section {
    margin-top: 60rpx;
    text-align: center;
    font-size: 26rpx;
    color: $text-grey;
    
    .register-text {
        color: $text-main;
        font-weight: bold;
        margin-left: 10rpx;
        position: relative;
        
        // 增加一个小下划线效果
        &::after {
            content: '';
            position: absolute;
            bottom: -4rpx;
            left: 0;
            width: 100%;
            height: 2rpx;
            background: $text-main;
        }
    }
}

// 适配超窄屏幕，比如极小的 Android 手机
@media screen and (max-width: 320px) {
    .login-card {
        width: 85%;
        padding: 40rpx 30rpx;
    }
}
</style>