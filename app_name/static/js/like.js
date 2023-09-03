$(function () {            
    $(".like").click(function () {
        var url = 'http://localhost:8123/articles/' + id + '/like?username=' + username; // 构造URL

        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                // 点赞成功，改变组件颜色
                $(this).toggleClass('cs');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // 点赞失败，弹出错误原因
                var error = jqXHR.responseJSON.error || textStatus;
                alert('点赞失败：' + error);
            },
            context: this // 设置上下文为当前元素，确保在成功回调函数中可以正确引用该元素
        });

        $(this).off('click'); // 将单击事件从元素上删除，防止再次触发
    });
});
