import CONFIG from './config.js'

const request = {
    get(url, data = {}, header = {}) {
        return this.request(url, 'GET', data, header)
    },
    
    post(url, data = {}, header = {}) {
        return this.request(url, 'POST', data, header)
    },
    
    put(url, data = {}, header = {}) {
        return this.request(url, 'PUT', data, header)
    },
    
    delete(url, data = {}, header = {}) {
        return this.request(url, 'DELETE', data, header)
    },
    
    async request(url, method = 'GET', data = {}, header = {}) {
        const defaultHeader = {
            'Content-Type': 'application/json',
            ...header
        }
        
        return new Promise((resolve, reject) => {
            uni.request({
                url: CONFIG.baseUrl + url,
                method: method,
                data: method === 'GET' ? data : JSON.stringify(data),
                header: defaultHeader,
                timeout: CONFIG.timeout,
                success: (response) => {
                    const responseData = response.data || response
                    
                    if (response.statusCode === 200) {
                        resolve(responseData)
                    } else {
                        const errorMessage = responseData.message || responseData.detail || '请求失败'
                        uni.showToast({ title: errorMessage, icon: 'none' })
                        reject(new Error(errorMessage))
                    }
                },
                fail: (error) => {
                    console.error('网络请求失败:', error)
                    uni.showToast({ title: '网络错误', icon: 'none' })
                    reject(error)
                }
            })
        })
    }
}

export default request