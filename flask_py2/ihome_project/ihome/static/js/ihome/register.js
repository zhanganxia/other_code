function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 向后端请求图片验证码
    // 生成验证码图片的编号
    imageCodeId = generateUUID();
    // 拼接验证码图片的路径(即，后端的额请求路径)
    var url = "/api/v1.0/image_codes/" + imageCodeId;

    // 设置到前端页面
    $(".image-code img").attr("src", url);
}

function sendSMSCode() {
    // 防止用户连击
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    var reqData = {
        image_code_id: imageCodeId,
        image_code_text: imageCode
    };
    $.get("/api/v1.0/sms_codes/" + mobile, reqData, function(resp) {
        // 因为后端返回的响应数据是json格式的字符串，并且包含了响应头Content-Type指明是application/json
        // 所以ajax将收到的响应数据自动转换为js中的对象(字典)，我们可以直接按照对象属性的操作获取返回数据
        // resp.errcode
        // resp.errmsg
        // 根据后端返回的不同错误编号,做不同的处理
        if (resp.errcode == "0") {
            // 表示发送成功
            // 显示倒计时
            var num = 60;
            var timer = setInterval(function() {
                num--;
                if (num > 0) {
                    $(".phonecode-a").html(num + "秒");
                } else {
                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    clearInterval(timer)
                }

            }, 1000, 60)
        } else {
            // alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    });

    // $.get("/api/smscode", { mobile: mobile, code: imageCode, codeId: imageCodeId },
    //     function(data) {
    //         if (0 != data.errno) {
    //             $("#image-code-err span").html(data.errmsg);
    //             $("#image-code-err").show();
    //             if (2 == data.errno || 3 == data.errno) {
    //                 generateImageCode();
    //             }
    //             $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //         } else {
    //             var $time = $(".phonecode-a");
    //             var duration = 60;
    //             var intervalid = setInterval(function() {
    //                 $time.html(duration + "秒");
    //                 if (duration === 1) {
    //                     clearInterval(intervalid);
    //                     $time.html('获取验证码');
    //                     $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //                 }
    //                 duration = duration - 1;
    //             }, 1000, 60);
    //         }
    //     }, 'json');
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function() {
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function() {
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function() {
        $("#phone-code-err").hide();
    });
    $("#password").focus(function() {
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function() {
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e) {
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
    });
});