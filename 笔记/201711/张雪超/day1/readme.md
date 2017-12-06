01 - HTML
超文本编辑语言:超-指超链接，是一种标记语言(标记视频、音频...)

快捷创建HTML：将输入发调整到英文模式-->回车

谷歌浏览器字体默认值是16号


css 指层叠样式表
-----------------------------------------------------------
行内式：在div标签后添加style属性，属性间用";"隔开
嵌入式：在head标签中  一般用在网站首页
外链式：<link rel="stylesheet" href="">

css选择器
    1.标签选择器：做真实网页时 做标签样式重置时使用此选择器

    2.类选择器：使用最多  前面不要少了小点
        选中类名叫box的那个标签
        .box{
            xxx
        }

        <div class="box"> 我是一个div标签 </div>
    3.层级/后代
        对div标签中的p标签起作用
        .box2 p{
            xxx
        }
        <div class = "box2" >
            <p>xxxx</>
        </div>

css常用样式属性
    color：                文字颜色
    font-size:字体大小      像素
    background-color:      背景颜色
    font-family:           字体
    font-weight:           字体加粗  bold/normal
    line-height:           行高

    width: 200px -->设置元素、内容的宽度
    height:200px -->设置高度

    设置元素边框：第一个值是边框粗细；第二个值是样式(solid-->实线)；第三个是颜色
        border_left：1px solid red
        border_head：
	
	solid-->实线
	dashed-->虚线
	dotted-->点线

    外边距：margin
        一般只设置左和顶部的外边距 它不会影响元素的真实大小，只会影响它的位置
        margin-left:20px
        margin-righ:20px
        margin-head:20px
        margin-bottom:20px
        
        实现水平居中
        margin: 0px auto

    内边距：padding
        内边距就是让里面的内容和元素的边框/边界有一定距离
        padding:20px    四边都是20px
        padding:20px 40px   上下 左右
        padding:20px 30px 40px 上  左右  下
        padding:20px 30px 40px 50px   上  左 右  下()

    浮动:float
        只有左、右浮动
        float:left/right

    清除下划线：text-decoration: none

    设置下划线：text-decoration: underline






