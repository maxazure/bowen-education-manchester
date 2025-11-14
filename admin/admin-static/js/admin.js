// 管理后台基础JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('博文教育管理后台已加载');

    // TODO: 添加通用功能
    // - AJAX表单提交
    // - 确认对话框
    // - 提示消息
});

// 工具函数
const AdminUtils = {
    // 显示成功消息
    showSuccess: function(message) {
        alert('成功: ' + message);
    },

    // 显示错误消息
    showError: function(message) {
        alert('错误: ' + message);
    },

    // 确认对话框
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    }
};
