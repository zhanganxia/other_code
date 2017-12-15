git版本控制

1. 安装git：sudo apt-get install git (Ubantu安装方式)

2. git操作基本命令：

    2.1 将文件夹设置为工作区：git init

        .git文件夹-->版本库，里面包含暂存区和仓库区

    2.2 版本创建及查看状态：git status：查看最近的提示

    2.3 代码提交：
        提交文件到暂存区：git add 
        将暂存区的记录提交仓库区：git commit -m '<版本说明>'

3. 版本查看和回退

    3.1 查看当前版本：git log

    3.2 回退到上一个版本： git reset --hard HEAD^ 或  git reset --hard HEAD~1
        HEAD : 当前版本

    3.3 查看任何创建过的版本：git reset --hard <版本号>

    3.4 查看所有版本号：git reflog


4. git管理修改

    4.1 git只提交暂存区的修改，在工作区的修改，不会提交到仓库区
    4.2 在工作区反悔：git checkout -- <文件名> 
    
    4.3 在暂存区反悔：
        a.从暂存区重新放回工作区：git reset HEAD <文件名>
        b.在工作区再进行回退：git checkout --<文件名> 

    4.4 撤销提交到仓库区的修改：git reset --hard HEAD^  版本回退

5. 文件对比
    5.1 比较工作区和版本库的区别： git diff HEAD --<文件>
    5.2 查看当前版本和上一个版本的区别：git diff HEAD HEAD^

6. 删除文件
    6.1 使用git命名删除文件：git rm <文件名>
        删除的修改行为已经提交到暂存区，如果确认删除，需要提交到仓库区
    
    6.2 直接在文件夹中删除文件，只是影响了工作区，需要提交到暂存区

7. git分支

    7.1 分支基本操作
        a. 查看当前分支 git branch
                * 星号表示当前在哪个分支
                master：主分支
                dev: 开发分支

        b. 创建分支：git branch dev

        c. 切换分支：git checkout dev

        d. 切换并创建分支：git checkout -b <要创建的分支名>

        e. 删除分支：git branch -d <分支名>

        f. 合并分支：
            方式一：快速合并
            git merge <分支名>
            fast-forword：快速合并，指针重新指向要合并的分支

            方式二：递归合并
            git merge --no-ff -m'' <分支名>
            'recursive':递归方式合并分支

             查看分支合并信息：git log --graph --pretty=online

    7.2 解决冲突

        冲突产生原因：两个分支同时对同一个文件都做了修改，然后合并
        解决方法：双方协商解决，保留代码中需要的部分，然后提交到暂存区、仓库区

    7.3 Bug分支
        在工作区暂存：git stash 
        创建Bug分支：git branch bug001
        修改Bug并提交暂存区-->仓库区-->然后切换到dev分支，使用递归方式合并Bug001分支
        删除Bug分支：git branch -b <bug分支名>

        查看暂存工作区：git stash list
        恢复工作区，继续编辑：git stash pop
    
8. git远程操作
        从远程拉取分支：git pull <分支名>

        





