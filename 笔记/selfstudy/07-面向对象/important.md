导入一个模块，Python解释器对模块位置的搜索顺序是：

1.当前目录
2.如果不在当前目录，Python则搜索在shell变量PYTHONPATH的每一个目录。
3.如果都找不到，Python会查看默认路径。
4.模块搜索路径存储在sysytem模块的sys.path变量中