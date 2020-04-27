;
var user_reset_pwd_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        $("#save").click(function(){
            var btn_target = $(this)
            if (btn_target.hasClass("disabled")) {
                alert("请求正在进行，请稍后再试")
                return
            }
            var old_password = $("#old_password").val()
            var new_password = $("#new_password").val()

            if (!old_password || old_password.length < 6) {
                alert('请输入符合规范的原密码')
                return false
            }
            if (!new_password || new_password.length < 6) {
                alert('请输入符合规范的新密码')
                return false
            }
            
            btn_target.addClass("disabled")

            $.ajax({
                url: common_ops.buildUrl("/user/reset-pwd"),
                type:"POST",
                data:{"old_password":old_password,"new_password":new_password},
                dataType:"json",
                success:function(resp){
                    alert("重置密码成功")
                    console.log(resp.msg)
                    btn_target.removeClass("disabled")
                },
                error:function(error){
                    console.log(error)
                }
            })
        })
    }
}

$(document).ready(function(){
    user_reset_pwd_ops.init()
})