/**
 * 留言管理前端交互脚本
 */

// 查看留言详情
function viewDetail(contactId) {
    fetch(`/admin/contacts/${contactId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const contact = data.data;
                const statusText = contact.status === 'unread' ? '未读' : '已处理';
                const statusClass = contact.status === 'unread' ? 'status-unread' : 'status-handled';

                let detailHTML = `
                    <div class="detail-row">
                        <div class="detail-label">ID:</div>
                        <div>${contact.id}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">姓名:</div>
                        <div>${contact.name}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">联系方式:</div>
                        <div>${contact.contact_info}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">留言内容:</div>
                        <div style="white-space: pre-wrap;">${contact.message_text}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">状态:</div>
                        <div><span class="status-badge ${statusClass}">${statusText}</span></div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">来源页面:</div>
                        <div>${contact.source_page_url || '未知'}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">创建时间:</div>
                        <div>${contact.created_at}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">处理时间:</div>
                        <div>${contact.handled_at || '未处理'}</div>
                    </div>
                `;

                document.getElementById('detailContent').innerHTML = detailHTML;
                document.getElementById('detailModal').style.display = 'block';
            } else {
                alert('获取详情失败');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('获取详情失败');
        });
}

// 关闭详情模态框
function closeDetailModal() {
    document.getElementById('detailModal').style.display = 'none';
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('detailModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// 标记为已处理
function markAsHandled(contactId) {
    updateStatus(contactId, 'handled');
}

// 标记为未读
function markAsUnread(contactId) {
    updateStatus(contactId, 'unread');
}

// 更新留言状态
function updateStatus(contactId, status) {
    fetch(`/admin/contacts/${contactId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('更新状态失败');
    });
}

// 删除留言
function deleteContact(contactId) {
    if (!confirm('确定删除这条留言吗？')) {
        return;
    }

    fetch(`/admin/contacts/${contactId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('删除失败');
    });
}

// 全选/取消全选
function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.contact-checkbox');

    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });

    updateBatchActions();
}

// 更新批量操作按钮状态
function updateBatchActions() {
    const checkboxes = document.querySelectorAll('.contact-checkbox:checked');
    const count = checkboxes.length;
    const batchActions = document.getElementById('batchActions');
    const selectedCount = document.getElementById('selectedCount');

    if (count > 0) {
        batchActions.style.display = 'block';
        selectedCount.textContent = count;
    } else {
        batchActions.style.display = 'none';
    }
}

// 批量标记为已处理
function batchMarkAsHandled() {
    batchUpdateStatus('handled');
}

// 批量标记为未读
function batchMarkAsUnread() {
    batchUpdateStatus('unread');
}

// 批量更新状态
function batchUpdateStatus(status) {
    const checkboxes = document.querySelectorAll('.contact-checkbox:checked');
    const ids = Array.from(checkboxes).map(cb => parseInt(cb.value));

    if (ids.length === 0) {
        alert('请先选择留言');
        return;
    }

    const statusText = status === 'handled' ? '已处理' : '未读';
    if (!confirm(`确定将选中的 ${ids.length} 条留言标记为${statusText}吗？`)) {
        return;
    }

    fetch('/admin/contacts/batch/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ids: ids,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('批量更新失败');
    });
}

// 清除选择
function clearSelection() {
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    document.getElementById('selectAll').checked = false;
    updateBatchActions();
}

// 导出 CSV
function exportCSV() {
    // 获取当前的筛选条件
    const urlParams = new URLSearchParams(window.location.search);
    const statusFilter = urlParams.get('status_filter') || '';
    const keyword = urlParams.get('keyword') || '';

    // 构建导出 URL
    let exportUrl = '/admin/contacts/export/csv?';
    if (statusFilter) {
        exportUrl += `status_filter=${statusFilter}&`;
    }
    if (keyword) {
        exportUrl += `keyword=${encodeURIComponent(keyword)}`;
    }

    // 下载文件
    window.location.href = exportUrl;
}
