const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { exec, spawn } = require('child_process'); // 引入 spawn 方法

const app = express();
const port = 3000;

let items = [];

app.use(cors());
app.use(bodyParser.json());

app.get('/items', (req, res) => {
res.json(items);
});

app.post('/items', (req, res) => {
    const item = { ...req.body, output: '正在执行命令...' };
    items.push(item);
    const index = items.length - 1; // 获取新添加的 item's 索引

    console.log(`新增项目: ${JSON.stringify(item)}`);
    res.status(201).send();

    // 构建要执行的命令字符串
    const command = `sscma.cli`;
    const args = [
        'client',
        '--broker',
        '192.168.137.1',
        '--port',
        '1883',
        '--device',
        `xiao_esp32_s3_${item.title1}`,
        '--headless'
    ];

    console.log(`执行命令: ${command} ${args.join(' ')}`);

    // 使用 spawn 以便实时捕获输出
    const child = spawn(command, args);

    child.stdout.on('data', (data) => {
        const output = data.toString();
        console.log(`stdout: ${output}`);
        items[index].output += output;
    });

    child.stderr.on('data', (data) => {
        const errorOutput = data.toString();
        console.error(`stderr: ${errorOutput}`);
        items[index].output += errorOutput;
    });

    child.on('error', (error) => {
        console.error(`执行错误: ${error.message}`);
        items[index].output += `错误: ${error.message}`;
    });

    child.on('close', (code) => {
        console.log(`子进程退出码: ${code}`);
        items[index].output += `\n命令执行结束，退出码 ${code}`;
    });
});

app.listen(port, () => {
    console.log(`Server running at http://192.168.66.184:${port}/`);
});
