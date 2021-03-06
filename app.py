from flask import Flask, g, flash, redirect, url_for, render_template
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import forms
import models

app = Flask(__name__)
app.secret_key = "hisudsu9d9jjsojos%dfjiwjfpwfpw"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    posts = models.Post.get_all_posts()
    for post in posts:
        print(post.content)
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(), content=form.content.data.strip())
        flash("Message posted", "success")
        print("was here")
        return redirect(url_for('index'))
    return render_template('index.html', form=form, posts=posts)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "danger")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for('login'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Yay, you register!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    print("in main")
    models.initialize()
    try:
        models.User.create_user(username='bjfikky', email='bjfikky@yahoo.com', password='fikky007')
    except ValueError:
        pass
    app.run(debug=True)
