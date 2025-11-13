/**
 * 栏目管理前端脚本
 *
 * 功能：
 * - 树形结构拖拽排序
 * - 删除栏目确认
 * - 批量更新排序
 */

document.addEventListener('DOMContentLoaded', function() {
    initSortable();
    initDeleteButtons();
});

/**
 * 初始化拖拽排序
 */
function initSortable() {
    const treeContainer = document.getElementById('column-tree');
    if (!treeContainer) return;

    // 为主容器创建 Sortable 实例
    Sortable.create(treeContainer, {
        animation: 150,
        handle: '.drag-handle',
        ghostClass: 'dragging',
        onEnd: function(evt) {
            updateSortOrder();
        }
    });

    // 为每个子容器创建 Sortable 实例
    const childContainers = document.querySelectorAll('.column-children');
    childContainers.forEach(container => {
        Sortable.create(container, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'dragging',
            onEnd: function(evt) {
                updateSortOrder();
            }
        });
    });
}

/**
 * 更新排序顺序
 */
function updateSortOrder() {
    const columnItems = document.querySelectorAll('.column-item');
    const orderData = [];

    columnItems.forEach((item, index) => {
        const columnId = parseInt(item.getAttribute('data-id'));
        orderData.push({
            id: columnId,
            sort_order: index + 1
        });
    });

    // 发送排序数据到后端
    fetch('/admin/columns/reorder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            order: orderData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification('排序已更新', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('排序更新失败', 'error');
    });
}

/**
 * 初始化删除按钮
 */
function initDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-column');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const columnId = this.getAttribute('data-id');
            deleteColumn(columnId);
        });
    });
}

/**
 * 删除栏目
 */
function deleteColumn(columnId) {
    if (!confirm('确定要删除这个栏目吗？如果栏目包含子栏目或关联内容，将无法删除。')) {
        return;
    }

    fetch(`/admin/columns/${columnId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification(data.message, 'success');
            // 重新加载页面
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else if (data.error) {
            showNotification(data.error + '\n' + (data.message || ''), 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('删除失败，请稍后重试', 'error');
    });
}

/**
 * 显示通知消息
 */
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        color: white;
        font-size: 14px;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;

    // 根据类型设置背景色
    if (type === 'success') {
        notification.style.background = '#28a745';
    } else if (type === 'error') {
        notification.style.background = '#dc3545';
    } else if (type === 'warning') {
        notification.style.background = '#ffc107';
        notification.style.color = '#000';
    } else {
        notification.style.background = '#17a2b8';
    }

    // 添加到页面
    document.body.appendChild(notification);

    // 3秒后自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
