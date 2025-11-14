/**
 * 单页管理 JavaScript
 *
 * 功能:
 * - Markdown 编辑器初始化
 * - 实时预览
 * - 删除确认
 * - 发布/取消发布
 */

// Markdown 编辑器实例
let easyMDE = null;

/**
 * 初始化 Markdown 编辑器
 */
function initMarkdownEditor() {
    const textarea = document.getElementById('content_markdown');
    if (!textarea) return;

    easyMDE = new EasyMDE({
        element: textarea,
        autosave: {
            enabled: true,
            uniqueId: 'single-page-editor',
            delay: 1000,
        },
        spellChecker: false,
        toolbar: [
            'bold',
            'italic',
            'heading',
            '|',
            'quote',
            'unordered-list',
            'ordered-list',
            '|',
            'link',
            'image',
            '|',
            'preview',
            'side-by-side',
            'fullscreen',
            '|',
            'guide'
        ],
        placeholder: '在此输入 Markdown 内容...',
        renderingConfig: {
            codeSyntaxHighlighting: true,
        },
        previewRender: function(plainText) {
            // 实时预览功能
            return renderMarkdown(plainText);
        }
    });

    // 监听编辑器变化,更新预览
    easyMDE.codemirror.on('change', function() {
        updatePreview();
    });

    // 初始加载时更新一次预览
    updatePreview();
}

/**
 * 更新实时预览
 */
function updatePreview() {
    if (!easyMDE) return;

    const content = easyMDE.value();
    const previewContainer = document.getElementById('previewContainer');
    const previewContent = document.getElementById('previewContent');

    if (!previewContainer || !previewContent) return;

    if (content.trim()) {
        previewContainer.style.display = 'block';
        previewContent.innerHTML = renderMarkdown(content);
    } else {
        previewContainer.style.display = 'none';
    }
}

/**
 * 简单的 Markdown 渲染 (客户端预览)
 * 注意: 这只是预览,实际转换在服务器端进行
 */
function renderMarkdown(text) {
    if (!text) return '';

    // 简单的 Markdown 转换 (用于预览)
    let html = text;

    // 标题
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // 粗体和斜体
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // 链接
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

    // 图片
    html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');

    // 代码块
    html = html.replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code>$2</code></pre>');

    // 行内代码
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // 段落
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';

    return html;
}

/**
 * 删除单页
 */
function deletePage(pageId) {
    if (!confirm('确定要删除这个单页吗?此操作不可恢复!')) {
        return;
    }

    fetch(`/admin/pages/${pageId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || '删除成功');
            // 从 DOM 中移除该行
            const row = document.querySelector(`tr[data-page-id="${pageId}"]`);
            if (row) {
                row.remove();
            }
            // 如果没有更多页面,显示空状态
            checkEmptyState();
        } else {
            alert(data.message || '删除失败');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('删除失败: ' + error.message);
    });
}

/**
 * 发布/取消发布单页
 */
function togglePublish(pageId, currentStatus) {
    const action = currentStatus === 'published' ? '取消发布' : '发布';
    if (!confirm(`确定要${action}这个单页吗?`)) {
        return;
    }

    fetch(`/admin/pages/${pageId}/publish`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || `${action}成功`);
            // 刷新页面以更新状态
            location.reload();
        } else {
            alert(data.message || `${action}失败`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`${action}失败: ` + error.message);
    });
}

/**
 * 检查空状态
 */
function checkEmptyState() {
    const tbody = document.querySelector('.pages-table tbody');
    if (tbody && tbody.children.length === 0) {
        location.reload(); // 简单的方式:重新加载页面显示空状态
    }
}

/**
 * 自动生成 Slug
 */
function autoGenerateSlug() {
    const titleInput = document.getElementById('title');
    const slugInput = document.getElementById('slug');

    if (!titleInput || !slugInput) return;

    // 只在新建时自动生成
    if (slugInput.value.trim() !== '') return;

    titleInput.addEventListener('blur', function() {
        if (slugInput.value.trim() === '' && titleInput.value.trim() !== '') {
            // 简单的 slug 生成 (实际生成在服务器端)
            let slug = titleInput.value.toLowerCase()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');
            slugInput.value = slug;
        }
    });
}

/**
 * 页面加载完成后初始化
 */
document.addEventListener('DOMContentLoaded', function() {
    // 初始化 Markdown 编辑器 (仅在表单页面)
    initMarkdownEditor();

    // 自动生成 Slug
    autoGenerateSlug();

    // 绑定删除按钮
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const pageId = this.getAttribute('data-id');
            deletePage(pageId);
        });
    });

    // 绑定发布/取消发布按钮
    document.querySelectorAll('.btn-publish').forEach(button => {
        button.addEventListener('click', function() {
            const pageId = this.getAttribute('data-id');
            const status = this.getAttribute('data-status');
            togglePublish(pageId, status);
        });
    });

    // 表单提交验证
    const form = document.getElementById('pageForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            // 确保 Markdown 内容同步到 textarea
            if (easyMDE) {
                easyMDE.codemirror.save();
            }

            // 基本验证
            const title = document.getElementById('title').value.trim();
            const slug = document.getElementById('slug').value.trim();
            const content = document.getElementById('content_markdown').value.trim();

            if (!title) {
                alert('请输入标题');
                e.preventDefault();
                return false;
            }

            if (!slug) {
                alert('请输入 Slug');
                e.preventDefault();
                return false;
            }

            if (!content) {
                alert('请输入内容');
                e.preventDefault();
                return false;
            }

            return true;
        });
    }
});
