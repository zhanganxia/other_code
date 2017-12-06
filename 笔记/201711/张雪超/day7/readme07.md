全局和局部变量
--------------------------------------------
在开发中尽量不要出现局部和全局变量名

局部变量的优先级比全局的高，如果函数内出现和全局变量同名时，
在局部变量定义的函数内去屏蔽掉全局变量，此时如果提前使用变量
会提示undefined类型


封闭函数
---------------------------------------------
解决同名函数或同名变量覆盖问题
!function(){

}()

~function(){

}()


jQuery
------------------------------------------
$()-->万能函数
jQuery获取标签对象 用jQuery获取的标签对象 变量前面以$开头 就是为了和原生的js标签对象区分
1. jQuery 和原生js对比
        1) 原生js只能回去到标签的行内式属性的值

            jQuery获取标签对象 用Query获取的标签对象 变量前面以$开头
            就是为了和原生js的标签对象进行区分

            jQuery获取样式属性值时，只要它有 不管他是怎么有的都能取到


        2) $(document).ready(function(){ }) -->html文档准备好了
        window.onload = function(){}  -->浏览器加载完成    

        3) jQuery的执行优先于原生js

2.  jQuery操作css属性

    1) jQuery 操作css数字属性可以不加单位,如果添加单位需要加引号
    2) 属性必须用单引号引起来，否则会认为成变量
    3) 多个属性间用逗号连接，类似于JSON格式
    4) 属性名可以用原生js写法，也可以用css写法

3.  jQuery选择器
    1) 标签选择器
        var $div = $('div');
        $div.css({'color': 'green'});

    2) 类选择器
        var $div = $('.box1');
        $div.css({'color': 'green'});
    
    3) id选择器
        var $div = $('#box2');
        $div.css({'color': 'green'});

    4) 层级后代选择器
        var $div = $('.con .box2');
        $div.css({'color': 'green'});

    5) 并集/组选择器
        var $div = $('.box2,.a1');
        $div.css({'color': 'green'});

    6) 属性选择器

        <!-- *=表示类名里只要包含xxx   ^=开头是否包含xxx  $=结束包含xxx -->
        var $div = $('div[class*=o]');
        $div.css({'color': 'green'});

4.  jQuery选择集的过滤
    1) has('') 选中后代包含xxx标签的div
        has中穿的参数只能是子集 后级
       例： $divs.has('p').css({'xxx':'xxx'});

    2) not('') 里面不能传后代 和子集无关 找的是叫什么类名/id名以外的标签
       例： $divs.not('p')

    3) eq() 通过角标的方式去找指定的标签，和嵌套层次无关，都是从0开始
       例：$li.eq(6).css({'xxx'：'xxx'});


5.  jQuery选择器的转移
    1) prev (previous) 选中平级上面的一个标签
        例：$div3.prev().css({});

    2) prevAll  选中平级上面的所有标签

    3) next 选中平级下面的一个标签

    4) nextAll 选中平级下面的所有标签

    5) siblings 选中除了自己以外的所有平级兄弟

    6) children() 选中所有直接子级，不会找到孙子及后代

    7) find() 查找后代

    8) 转移到子集的直接父级
        $('p').parent().class({'xxx':'xxx'});

        $('p').parent()-->找上面的所有父元素

6.  判断选择器是否选择到标签
    1) length 如果length为0说明没有选到标签
    $li.length

7.  jQuery中的事件
    click
    this (在事件函数中使用)在事件中它表示谁触发的事件就表示谁，默认是js对象
        把js对象那个转成jQuery中的对象 用$()包装就可以了

    index() 获取当前标签在它的直接父级中他是第几个儿子，从每一个嵌套关系中，都是从0开始

8.  jQuery操作样式类
    $div.addClass('') -->给标签添加类
    $div.removeClass('') -->删除标签中的类

9.  动画函数 animate
    第一个参数： {} 动画属性 css属性
    第二个参数： 动画持续时间  毫秒
    第三个参数： swing linear 默认不传就是用swing
    第四个参数： 动画执行完成后的回调函数

10.  jQuery 获得内容
    text() : 设置或返回所选元素的文本内容
    html() : 设置或返回所选元素的内容(包括HTML标记)
    val() : 设置或返回表单字段的值
    attr() : 获取属性值



其他：
opacity: 设置透明度  0表示透明  1表示不透明






    
