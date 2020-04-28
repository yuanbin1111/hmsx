;
var account_index_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        var that = this;
        $(".remove").click(function(){
            id = $(this).attr("data")
            that.myAjax(id,"remove")
        })

        $(".recover").click(function(){
            id = $(this).attr("data")
            that.myAjax(id,"recover")
        })
    },

    // 封装ajax操作
    myAjax:function(id,acts){
        $.ajax({
            url:common_ops.buildUrl("/account/remove-or-recover"),
            type:"POST",
            data:{
                "id":id,
                "acts":acts
            },
            dataType:"json",
            success:function(resp){
                console.log(resp.msg)
                if (resp.code == 200) {
                    window.location.href = common_ops.buildUrl("/account/index")
                }
            },
            error:function(error){
                console.log(error)
            }
        })
    }

}
$(document).ready(function(){
    account_index_ops.init()
})