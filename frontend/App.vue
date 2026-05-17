<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
			
			// #ifdef APP-PLUS
			// 1. 检查是否有从外部（浏览器/其他App）传过来的唤醒参数
			if (plus.runtime.arguments) {
				try {
					let args = plus.runtime.arguments;
					console.log("App被外部唤醒，携带的完整参数为:", args);
					
					// 2. 你的 scheme 是 smartcourse://share
					if (args.includes('smartcourse://')) {
						
						// 3. 检查参数里有没有包含去登录的指令（例如网页端传了 action=login）
						if (args.includes('action=login')) {
							
							// 延迟 500 毫秒执行跳转，防止 App 刚启动时页面还没渲染好导致跳转失败
							setTimeout(() => {
								uni.navigateTo({
									url: '/pages/login/login' // 🛠️ 注意：请确保这是你真实的登录页面路径
								});
							}, 500);
						}
					}
					
					// 4. 【核心】消费完参数后必须清空！否则以后每次 App 从后台切回前台，都会重复触发跳转
					plus.runtime.arguments = ""; 
					
				} catch (e) {
					console.error("解析唤醒参数失败:", e);
				}
			}
			// #endif
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/* 1. 强制所有元素使用怪异盒子模型，宽度包含 padding 和 border */
	view, scroll-view, text {
		box-sizing: border-box;
	}

	/* 2. 你原本的滚动条隐藏代码 */
	.mobile-page ::-webkit-scrollbar {
		display: none;
		width: 0 !important;
		height: 0 !important;
		background: transparent;
	}
    
	/* 3. 确保页面容器不会横向溢出 */
	page {
		width: 100%;
		overflow-x: hidden;
	}
</style>