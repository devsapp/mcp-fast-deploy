// 添加实时名称验证
const nameInput = document.querySelector('input[name="name"]');
const nameCounter = nameInput.nextElementSibling;

// 验证正则表达式
const nameRegex = /^[a-zA-Z_][a-zA-Z0-9_-]*$/;

nameInput.addEventListener('input', function() {
    const isValid = nameRegex.test(this.value);
    const length = this.value.length;
    
    // 更新字符计数器
    nameCounter.innerHTML = `${length}/32 ${
        isValid ? '' : '<span class="text-danger">(包含非法字符)</span>'
    }`;
    
    // 视觉反馈
    if (this.value && !isValid) {
        this.classList.add('is-invalid');
    } else {
        this.classList.remove('is-invalid');
    }
});

// 安装方式切换逻辑
document.body.addEventListener('click', function(e) {
    const btn = e.target.closest('[data-install-method]');
    if (!btn) return;

    // 原有切换逻辑
    document.querySelectorAll('[data-install-method]').forEach(b => {
        b.classList.remove('active');
    });
    btn.classList.add('active');
    document.querySelector('input[name="install_method"]').value = btn.dataset.installMethod;
    
    const jsonEditor = document.getElementById('jsonConfig');
    jsonEditor.placeholder = JSON.stringify(
        JSON.parse(btn.dataset.configTemplate),
        null, 4
    );
});

// 初始化配置模板
document.getElementById('jsonConfig').placeholder = JSON.stringify(
    JSON.parse(document.querySelector('[data-install-method].active').dataset.configTemplate),
    null, 4
);

// JSON校验逻辑
function validateJson(textarea) {
    const feedback = document.getElementById('jsonError');
    try {
        JSON.parse(textarea.value);
        textarea.classList.remove('is-invalid');
        feedback.textContent = "";
        return true;
    } catch (e) {
        textarea.classList.add('is-invalid');
        feedback.textContent = `JSON格式错误：${e.message}`;
        return false;
    }
}

function validateForm() {
    const nameValid = nameRegex.test(nameInput.value);
    const jsonValid = validateJson(document.getElementById('jsonConfig'));

    // 名称验证反馈
    if (!nameValid) {
        nameInput.classList.add('is-invalid');
        nameInput.scrollIntoView({ behavior: 'smooth' });
    }
    
    return nameValid && jsonValid;
}

// 在表单提交事件处理中添加状态控制
document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault(); // 必须添加在函数开头
    
    const submitBtn = document.getElementById('submitBtn');
    const spinner = submitBtn.querySelector('.spinner-border');
    const submitText = submitBtn.querySelector('.submit-text');
    
    try {
        submitBtn.disabled = true;
        submitText.textContent = '部署中...';
        spinner.style.display = 'inline-block';
        
        const formData = new FormData(e.target);
        const jsonValid = validateJson(document.getElementById('jsonConfig'));
        
        if (!jsonValid) {
            submitBtn.disabled = false;
            submitText.textContent = '提交部署';
            spinner.style.display = 'none';
            return;
        }

        const response = await fetch(e.target.action, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (response.ok) {
            const container = document.getElementById('resultContainer');
            container.style.display = 'block';
            document.getElementById('resultContent').innerHTML = JSON.stringify(result.data, null, 4);
            
            const linksDiv = document.getElementById('links');
            linksDiv.innerHTML = '';
            if (result.data.endpoint) {
            }
            container.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert(`部署失败: ${result.detail}`);
        }
        
    } catch (error) {
        console.error('请求失败:', error);
        alert('网络请求异常');
    } finally {
        // 恢复按钮状态
        submitBtn.disabled = false;
        submitText.textContent = '提交部署';
        spinner.style.display = 'none';
    }
});