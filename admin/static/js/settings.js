/**
 * 站点设置页面脚本
 *
 * 提供 Tab 切换、媒体库选择、AJAX 表单提交等功能
 */

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    initForm();
    loadMediaPreviews();
});

/**
 * 初始化 Tab 切换功能
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

/**
 * 切换 Tab
 */
function switchTab(tabName) {
    // 移除所有 active 类
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // 添加当前 Tab 的 active 类
    const activeButton = document.querySelector(`[data-tab="${tabName}"]`);
    const activeContent = document.getElementById(`tab-${tabName}`);

    if (activeButton) activeButton.classList.add('active');
    if (activeContent) activeContent.classList.add('active');
}

/**
 * 初始化表单提交
 */
function initForm() {
    const form = document.getElementById('settings-form');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // 显示加载状态
        const submitBtn = form.querySelector('.btn-save');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '保存中...';
        submitBtn.disabled = true;

        try {
            // 收集表单数据
            const formData = new FormData(form);

            // 提交数据
            const response = await fetch('/admin/settings', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                showAlert('success', result.message || '设置已保存');
            } else {
                showAlert('error', result.message || '保存失败');
            }
        } catch (error) {
            console.error('保存设置时出错:', error);
            showAlert('error', '保存失败，请稍后重试');
        } finally {
            // 恢复按钮状态
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}

/**
 * 显示提示信息
 */
function showAlert(type, message) {
    const container = document.getElementById('alert-container');
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';

    container.innerHTML = `
        <div class="alert ${alertClass}">
            ${message}
        </div>
    `;

    // 3秒后自动隐藏
    setTimeout(() => {
        container.innerHTML = '';
    }, 3000);

    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * 选择媒体（Logo 或 Favicon）
 */
function selectMedia(type) {
    // TODO: 集成媒体库选择器
    // 这里暂时使用简单的提示
    alert(`媒体库选择功能待集成\n\n当前选择: ${type}`);

    // 实际使用时应该打开媒体库弹窗，选择图片后：
    // 1. 更新隐藏字段的值（media ID）
    // 2. 更新预览图片

    // 示例代码（假设选中了 ID 为 123 的图片）：
    // document.getElementById(`${type}_id`).value = 123;
    // updateMediaPreview(type, '/path/to/image.jpg');
}

/**
 * 更新媒体预览
 */
function updateMediaPreview(type, imageUrl) {
    const preview = document.getElementById(`${type}-preview`);
    if (preview && imageUrl) {
        preview.innerHTML = `<img src="${imageUrl}" alt="${type}">`;
    }
}

/**
 * 加载已有的媒体预览
 */
function loadMediaPreviews() {
    // 检查是否有 Logo ID
    const logoId = document.getElementById('logo_id').value;
    if (logoId) {
        // TODO: 根据 media ID 获取图片 URL
        // updateMediaPreview('logo', imageUrl);
    }

    // 检查是否有 Favicon ID
    const faviconId = document.getElementById('favicon_id').value;
    if (faviconId) {
        // TODO: 根据 media ID 获取图片 URL
        // updateMediaPreview('favicon', imageUrl);
    }
}
