1.框架
    MVC架构
        M：模型  
        V：视图
        C：控制器  接收请求和数据进行处理

    Django MVT架构
        M：模型  读写数据库
        V：视图  接收请求，与M和T交互，再返回应答
        T：模板（Template） 提供HTML模板

    分模块目的：解耦  降低代码之间的关联


2.环境(虚拟环境)
    虚拟环境的作用：虚拟环境可以为每个项目搭建独立的python运行环境，使得每个项目依赖的python环境独立

    2.1 安装虚拟环境包
        sudo pip install virtualenv
        sudo pip install virtualenvwrapper

        virtualenv：是一个可以在同一计算机中隔离多个python版本的工具
        virtualenvwrapper：是virtualenv的扩展管理包，用于更方便管理虚拟环境
                          作用：
                            1.将所有虚拟环境整合在一个目录下
                            2.管理（新增，删除，复制）虚拟环境
                            3.切换虚拟环境

    2.2 设置虚拟环境默认生成地址
        编辑当前用户家目录下的.bashrc文件
        添加配置：
        export WORKON_HOME=$HOME/virtualenvs  -->设置虚拟环境存放目录
        source /usr/bin/virtualenvwrapper.sh  -->添加virtualenvwrapper路由。注意：用户不同，此路径需要变更

        使用source .bashrc使其生效

    
    2.3 创建虚拟环境
            python2: mkvirtualenv <虚拟环境名称>
            python3: mkvirtuallenv -p python3 <虚拟环境名称>
    
    2.4 虚拟环境操作命令：
        查看和使用虚拟环境： 
            workon 按两次tab  -->查看所有虚拟环境
            workon 虚拟环境名称(按tab键可以补齐) -->选择使用哪个虚拟环境

        退出虚拟环境： deactivate

        删除虚拟环境：先退出虚拟环境，然后再删除
            deactivate  退出虚拟环境
            rmvirtualenv py_django  删除虚拟环境

    2.5 虚拟环境下安装包
        pip install 包的名称
        安装Django包： pip install django==1.8.2
        显示所有的安装包：pip list







