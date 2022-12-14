from flask import Blueprint, url_for, render_template, redirect
from .models import User
from .forms import RegisterForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user
from flask_.extensions import db

blueprint = Blueprint('auth_blue', __name__, static_folder='../static',
                        template_folder='../templates', static_url_path='')

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        user = User(name=name, email=email)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth_blue.login'))
    return render_template('auth_module/register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('app_blue.index'))
        return redirect(url_for('auth_blue.login'))
    return render_template('auth_module/login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blue.login'))