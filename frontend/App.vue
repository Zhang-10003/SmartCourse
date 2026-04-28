<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
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
