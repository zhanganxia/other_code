html列表标签

一、选择器2 -->主要为js服务

   1. id选择器("#"标记)
        id 名称应该是唯一的
        每一个标签的id名称最好不要一样
        id 主要是运用在js中很少用在CSS上

        一个标签可以有多个类名，类名之间用空格隔开
        但一个标签只能有一个个id名称

  2.  组/并集选择器 ---->有相同的样式设置时使用，可以简化代码
        .box1,.box2{
            width:200px;
        }
        #单独设置需重新写：
        .box1{
            color:red;
        }
        .box2{
            color:blank;
        }

  3.  伪类选择器，作用在标签上，主要对元素起作用(类似于js的鼠标事件)
       1)hover:当鼠标悬浮到元素身上时此时选择器中的样式才会生效
        注意：类选择器和伪元素之间用两个":"隔开
        .box::hover{
            color:red;
            background-color:green
        }

        2)befor:在元素内容的前面，主要用来调试Bug

        3)after:在元素内容的后面


二、css中文本常用属性
    1. text-align:文字水平对齐  此属性主要用在块属性，父元素上
            left 默认值/缺省值
            center 居中
            right 居右
    行内标签设置文本水平对其没有效果 因为它的大小和文字一样大

    2.text-indent:文字首行缩进
        1) 如果用px单位 缩进几个字就用字体大小*N
        2) 如果用em单位 缩进几个字就写几

    3.font-xxxx
        font-style: italic; -->斜体
        font-weight:bold; -->加粗用

    4.元素溢出：
        子元素的尺寸超出了父元素就会元素溢出，溢出的区域默认显示
        overflow
        visible 默认超出区域可见
        hidden -->超出区域不显示
        scroll 超出的区域可以滚动查看，但在有些浏览器中没有超相互也会显示滚动条的信息
        auto 如果有超出

三、盒子模型
    1.元素在网页中显示的真实大小由：width height birder padding属性控制

    2.margin-top: 负值   合并边框

    3.垂直外边距默认会合并，取上下边距中的较大值，不会累加

    4.margin-top的塌陷：
        父元素没有边界时，设置子元素的margin-top,子元素相对父元素的顶部间距没有变化
        反而是父元素整体下移 子元素的margin-top这个作用到父元素身上了

        在HTML中如果界面出现问题，一般都去找父元素，设置也一般都设置父元素

        解决方法：
            方法一：加边框 -->border：1px solid white;
            方法二：overflow: hidden;  -->设置元素溢出
                  float：left;  -->float的浮动尽量不要随便乱用
            方法三：使用伪元素   -->推荐做法  对此元素没有什么影响，而且解决塌陷问题
                .clearfix::before{
                    content:'';
                    display：table;
                }





    
