#encoding=utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from ihome import create_app,db

# 创建flask工程应用对象
app = create_app("develop")

# 启动命令扩展
manager = Manager(app)

# 初始化迁移工具
Migrate(app,db)

# 添加数据库迁移命令
manager.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manager.run()
    
