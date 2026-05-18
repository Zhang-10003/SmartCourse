<script>
	export default {
		onLaunch: function() {
			console.log('App Launch');
			
			// #ifdef APP-PLUS
			// 也尝试在 onLaunch 中获取参数
			try {
				handleAppWakeup();
			} catch(e) {
				console.error('onLaunch 处理异常:', e);
			}
			// #endif
		},
		onShow: function() {
			console.log('App Show');
			
			// #ifdef APP-PLUS
			try {
				handleAppWakeup();
			} catch(e) {
				console.error('onShow 处理异常:', e);
			}
			// #endif
		},
		onHide: function() {
			console.log('App Hide');
		}
	}
	
	// ===== 处理 APP 唤醒的核心函数 =====
	function handleAppWakeup() {
		console.log('===== 开始检查唤醒参数 =====');
		
		let shareCode = null;
		
		// ===== 方式 1: plus.runtime.arguments =====
		try {
			if (plus && plus.runtime && plus.runtime.arguments) {
				let args = plus.runtime.arguments;
				console.log('方式 1 - plus.runtime.arguments:', args);
				if (args && args.length > 0) {
					shareCode = extractShareCode(args);
				}
			}
		} catch(e) {
			console.error('方式 1 异常:', e);
		}
		
		// ===== 方式 2: plus.runtime.argv =====
		if (!shareCode) {
			try {
				if (plus && plus.runtime && plus.runtime.argv) {
					let argv = plus.runtime.argv;
					console.log('方式 2 - plus.runtime.argv:', argv);
					if (argv && argv.length > 0) {
						for (let i = 0; i < argv.length; i++) {
							let code = extractShareCode(argv[i]);
							if (code) {
								shareCode = code;
								break;
							}
						}
					}
				}
			} catch(e) {
				console.error('方式 2 异常:', e);
			}
		}
		
		// ===== 方式 3: document.URL 或 window.location =====
		if (!shareCode) {
			try {
				let url = document.URL || window.location.href;
				console.log('方式 3 - URL:', url);
				shareCode = extractShareCode(url);
			} catch(e) {
				console.error('方式 3 异常:', e);
			}
		}
		
		// ===== 处理获取到的分享码 =====
		if (shareCode && shareCode.length > 0) {
			console.log('✅ 成功获取分享码:', shareCode);
			
			// 保存到 storage
			uni.setStorageSync('pendingShareCode', shareCode);
			console.log('✅ 已保存到 storage');
			
			// 清空参数，避免重复处理
			try {
				if (plus && plus.runtime) {
					plus.runtime.arguments = '';
				}
			} catch(e) {}
			
			// 跳转到学生页面
			setTimeout(function() {
				const userInfo = uni.getStorageSync('userInfo');
				if (userInfo && userInfo.user_id) {
					console.log('已登录，跳转到学生页');
					uni.switchTab({ url: '/pages/student/index' });
				} else {
					console.log('未登录，跳转到登录页');
					uni.navigateTo({ url: '/pages/login/index' });
				}
			}, 200);
			
		} else {
			console.log('❌ 没有找到分享码');
		}
	}
	
	// ===== 从任何字符串中提取分享码 =====
	function extractShareCode(text) {
		if (!text || typeof text !== 'string') {
			return null;
		}
		
		console.log('正在提取，源文本:', text);
		
		// 1. 找 smartcourse://share/xxx
		if (text.indexOf('share/') !== -1) {
			let parts = text.split('share/');
			if (parts.length > 1) {
				let code = parts[1].split('?')[0].split('#')[0].split('&')[0].split('/')[0].trim();
				if (code && code.length > 0) {
					console.log('从 share/ 提取到:', code);
					return code;
				}
			}
		}
		
		// 2. 找 code=xxx
		if (text.indexOf('code=') !== -1) {
			let parts = text.split('code=');
			if (parts.length > 1) {
				let code = parts[1].split('&')[0].split('#')[0].split('?')[0].trim();
				if (code && code.length > 0) {
					console.log('从 code= 提取到:', code);
					return code;
				}
			}
		}
		
		// 3. 正则匹配 item-xxx 格式
		let match = text.match(/item-[a-z0-9]+/i);
		if (match) {
			console.log('从正则提取到:', match[0]);
			return match[0];
		}
		
		return null;
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
