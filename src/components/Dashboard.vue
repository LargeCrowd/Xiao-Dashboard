<template>
	<div class="dashboard">
		<div class="header">
			<h1>仪表盘</h1>
			<form @submit.prevent="addItem" class="input-form">
			<input v-model="newItem.title1" placeholder="输入标题1" required />
			<input v-model="newItem.title2" placeholder="输入标题2" required />
			<button type="submit">发送</button>
			</form>
		</div>

		<div class="grid">
			<div v-for="(item, index) in items" :key="item.id" class="grid-item">
				<ViewBox 
					:device-name="`XIAO ${item.title1}`"
					:device-id="item.id"
					:place-holder="item.img || defaultPlaceholder" 
				/>
			</div>
		</div>

		<MQTTHandler />
	</div>
</template>
  
<script>
import axios from 'axios';
import MQTTHandler from './MQTTHandler.vue';
import ViewBox from './ViewBox.vue';
import placeholderImage from '../google-image.png'
import { io } from 'socket.io-client';


export default {
	components: {
		ViewBox,
		MQTTHandler
	},
	data() {
		return {
			items: [],
			newItem: {
				title1: '',
				title2: ''
			},
			defaultPlaceholder: placeholderImage,
			socket: null
		};
	},
	methods: {
		async addItem() {
			try {
				// 发送 POST 请求并获取新创建的 item
				const response = await axios.post('http://192.168.137.1:9001/items'	, this.newItem);
				const createdItem = response.data;
        console.log('新建的项目:', createdItem); // 调试日志
        // 将新创建的 item 添加到 items 数组中
        this.items.push(createdItem);
        // 清空输入框
        this.newItem.title1 = '';
        this.newItem.title2 = '';
      } catch (error) {
        console.error('添加项目失败:', error);
      }
    },

		async fetchItems() {
			try {
			const response = await axios.get('http://192.168.137.1:9001/items');
			this.items = response.data;
      } catch (error) {
        console.error('获取项目失败:', error);
      }
		},
		handleCommandOutput({ id, output }) {
      console.log(`接收到命令输出 - ID: ${id}, 输出: ${output}`); // 调试日志
      const item = this.items.find(item => item.id === id);
      if (item) {
        // 使用 Vue.set 确保响应式更新
        this.$set(item, 'output', item.output + output);
        
        // 等待 DOM 更新后自动滚动
        this.$nextTick(() => {
          const preElement = this.$refs['preOutput_' + id];
          if (preElement) {
            preElement.scrollTop = preElement.scrollHeight;
          }
        });
      }
    }
  },
	mounted() {
		this.fetchItems();

    // 建立 Socket.IO 连接
		this.socket = io('http://192.168.137.1:9001');
		this.socket.on('connect', () => {
      console.log('已连接到服务器');
    });
    this.socket.on('commandOutput', this.handleCommandOutput);
    
    // 如果使用 Socket.IO 实时更新，则不需要定时轮询
    // 否则可以保留以下定时器进行数据轮询
    // this.interval = setInterval(this.fetchItems, 5000);
  },
	beforeUnmount() { // Vue 3 使用 beforeUnmount，Vue 2 则使用 beforeDestroy
    // 移除定时器（如果有）
    // clearInterval(this.interval);
    if (this.socket) {
      this.socket.disconnect();
    }
  }
};
</script>
  
<style scoped>
.dashboard {
	max-width: 1200px;
	margin: auto;
	display: flex;
	flex-direction: column;
	padding: 20px;
}
.header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-bottom: 20px;
}
.input-form {
	display: flex;
	align-items: center;
}
.input-form input {
	margin-right: 10px;
	padding: 8px;
}
.input-form button {
	padding: 8px 16px;
	cursor: pointer;
}
.grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 20px;
}
.grid-item {
	border: 1px solid #ccc;
	padding: 10px;
	box-shadow: 0 2px 5px rgba(0,0,0,0.1);
	background-color: #fff;
}
pre {
	max-height: 7.2em;
	overflow-y: auto;
	background-color: #f5f5f5;
	padding: 10px;
	white-space: pre-wrap;
	border: 1px solid #e0e0e0;
	font-family: monospace;
}
</style>
  