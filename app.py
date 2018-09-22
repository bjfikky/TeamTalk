from flask import Flask, g, flash
from flask.ext.login import LoginManager

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


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Yay, you register!", "success")



if __name__ == '__main__':
    models.initialize()
    models.User.create_user(username='bjfikky', email='bjfikky@yahoo.com', password='fikky007')
    app.run()
