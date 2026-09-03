const API_BASE = '/api/v1';

let threadId = null;
let uploadedImageUrl = null;
let isStreaming = false;

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImg = document.getElementById('removeImg');
const newChatBtn = document.getElementById('newChatBtn');
const clearBtn = document.getElementById('clearBtn');

// 生成 thread_id
function generateThreadId() {
    return 'thread_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// 滚动到底部
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 添加用户消息
function addUserMessage(text, imageUrl) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user';

    let content = '';
    if (imageUrl) {
        content += `<img src="${imageUrl}" alt="上传的图片">`;
    }
    content += text;

    msgDiv.innerHTML = `<div class="message-content">${content}</div>`;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
}

// 添加助手消息
function addAssistantMessage() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message assistant';
    msgDiv.innerHTML = `
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
    return msgDiv;
}

// 更新助手消息内容
function updateAssistantMessage(msgDiv, text) {
    msgDiv.innerHTML = `<div class="message-content">${text}</div>`;
    scrollToBottom();
}

// 上传图片到 OSS
async function uploadImage(file) {
    const filename = `${Date.now()}_${file.name}`;

    // 获取预签名上传 URL
    const presignRes = await fetch(`${API_BASE}/oss/presign?filename=${encodeURIComponent(filename)}`);
    const presignData = await presignRes.json();

    // 上传文件到 OSS
    await fetch(presignData.uploadUrl, {
        method: 'PUT',
        headers: { 'Content-Type': presignData.contentType },
        body: file
    });

    return presignData.accessUrl;
}

// 发送消息
async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text && !uploadedImageUrl) return;
    if (isStreaming) return;

    if (!threadId) {
        threadId = generateThreadId();
    }

    // 显示用户消息
    addUserMessage(text, uploadedImageUrl);

    // 清空输入
    messageInput.value = '';
    messageInput.style.height = 'auto';
    const imageUrl = uploadedImageUrl;
    uploadedImageUrl = null;
    imagePreview.style.display = 'none';

    // 显示加载动画
    const assistantMsg = addAssistantMessage();
    isStreaming = true;
    sendBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                thread_id: threadId,
                image_url: imageUrl
            })
        });

        if (response.ok) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullReply = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value);
                fullReply += chunk;
                updateAssistantMessage(assistantMsg, fullReply);
            }

            if (!fullReply) {
                updateAssistantMessage(assistantMsg, 'AI 没有返回内容，请稍后重试。');
            }
        } else {
            const errorText = await response.text();
            updateAssistantMessage(assistantMsg, `请求失败 (${response.status})：${errorText}`);
        }
    } catch (error) {
        updateAssistantMessage(assistantMsg, `网络错误：${error.message}`);
    }

    isStreaming = false;
    sendBtn.disabled = false;
}

// 清空当前对话
async function clearMessages() {
    if (!threadId) return;

    await fetch(`${API_BASE}/chat/messages?thread_id=${threadId}`, {
        method: 'DELETE'
    });

    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon"></div>
            <h3>对话已清空</h3>
            <p>上传你的饭菜照片，我会帮你分析营养成分。</p>
        </div>
    `;
    threadId = null;
}

// 新建对话
function newChat() {
    threadId = null;
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon"></div>
            <h3>你好！我是你的健康饮食助手</h3>
            <p>上传你的饭菜照片，我会帮你分析营养成分，并给出运动建议。</p>
            <div class="quick-actions">
                <button class="quick-btn" data-text="帮我分析这份午餐的营养">分析午餐营养</button>
                <button class="quick-btn" data-text="我吃了红烧肉和米饭，帮我算算热量">计算红烧肉热量</button>
                <button class="quick-btn" data-text="今天吃了沙拉，需要运动多久消耗？">沙拉运动建议</button>
            </div>
        </div>
    `;
    bindQuickButtons();
}

// 绑定快捷按钮
function bindQuickButtons() {
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            messageInput.value = btn.dataset.text;
            sendMessage();
        });
    });
}

// 事件绑定
sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 自动调整 textarea 高度
messageInput.addEventListener('input', () => {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
});

// 图片上传
uploadBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 本地预览
    const reader = new FileReader();
    reader.onload = (ev) => {
        previewImg.src = ev.target.result;
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    // 上传到 OSS
    try {
        uploadedImageUrl = await uploadImage(file);
    } catch (error) {
        console.error('图片上传失败:', error);
        alert('图片上传失败，请重试。');
    }

    fileInput.value = '';
});

removeImg.addEventListener('click', () => {
    uploadedImageUrl = null;
    imagePreview.style.display = 'none';
    previewImg.src = '';
});

newChatBtn.addEventListener('click', newChat);
clearBtn.addEventListener('click', clearMessages);

// 初始化
bindQuickButtons();
