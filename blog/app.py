# app.py
from flask import Flask
from extensions import db, login_manager
from config import Config
from routes import register_routes  # 新增导入

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# 注册路由
register_routes(app)  # 调用路由注册函数

# 初始化数据库
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)