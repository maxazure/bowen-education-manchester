/**
 * 产品管理前端脚本
 */

// 删除产品
function deleteProduct(id) {
    if (!confirm('确定要删除这个产品吗?')) {
        return;
    }

    fetch(`/products/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('删除失败: ' + data.message);
        }
    })
    .catch(error => {
        alert('删除失败: ' + error);
    });
}

// 初始化产品表单
document.addEventListener('DOMContentLoaded', function() {
    const productForm = document.getElementById('productForm');
    if (!productForm) return;

    // 初始化 Markdown 编辑器
    const markdownEditor = document.getElementById('markdown-editor');
    if (markdownEditor && typeof EasyMDE !== 'undefined') {
        const easyMDE = new EasyMDE({
            element: markdownEditor,
            spellChecker: false,
            autosave: {enabled: true, uniqueId: 'product-description'}
        });
    }

    // AJAX 提交表单
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        // 处理复选框
        formData.set('is_recommended', document.querySelector('[name=is_recommended]').checked);

        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(r => r.json())
        .then(d => {
            alert(d.message);
            if (d.success) window.location.href = '/products';
        })
        .catch(e => alert('提交失败: ' + e));
    });
});
