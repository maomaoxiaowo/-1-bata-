# routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Post
from forms import RegistrationForm, LoginForm, PostForm
from extensions import db

def register_routes(app):
    @app.route('/')
    def index():
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            # 实际注册逻辑（需补充密码哈希处理）
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='注册', form=form)

    # 其他路由需完整实现（登录、退出、文章发布等）
# routes.py（续）
def register_routes(app):
    # 已有路由...

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:  # 实际应使用密码哈希验证
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('登录失败，请检查邮箱和密码', 'danger')
        return render_template('login.html', title='登录', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/post/new', methods=['GET', 'POST'])
    @login_required
    def new_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('文章已发布！', 'success')
            return redirect(url_for('index'))
        return render_template('create_post.html', title='新文章', form=form)