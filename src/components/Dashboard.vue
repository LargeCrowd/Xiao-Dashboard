<!-- Filename: Dashboard.vue -->
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
            <h2>XIAO{{ item.title1 }}: Scenario{{ item.title2 }}</h2>
            <pre :ref="'preOutput_' + item.id">{{ item.output }}</pre>
            </div>
        </div>
    </div>
</template>
  
<script>
    import axios from 'axios';
    
    export default {
        data() {
        return {
            items: [],
            newItem: {
            title1: '',
            title2: ''
            }
        };
        },
        methods: {
        async addItem() {
            try {
            const response = await axios.post('http://192.168.66.184:3000/items', this.newItem);
            const createdItem = response.data;
            this.items.push(createdItem);
            this.newItem.title1 = '';
            this.newItem.title2 = '';
            } catch (error) {
            console.error('Error adding item:', error);
            }
        },
        async fetchItems() {
            try {
            const response = await axios.get('http://192.168.66.184:3000/items');
            this.items = response.data;
            } catch (error) {
            console.error('Error fetching items:', error);
            }
        },
        handleCommandOutput({ id, output }) {
            const item = this.items.find(item => item.id === id);
            if (item) {
                this.$set(item, 'output', item.output + output);
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
        this.socket = io('http://192.168.66.184:3000');
        this.socket.on('commandOutput', this.handleCommandOutput);
        },
        beforeUnmount() {
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
  