import sqlite3
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from wtforms import ValidationError

from app import users, db
from users.flags import flag_recon1, flag_recon2, flag_cred1
from users.forms import RegisterForm, LoginForm, SearchForm, BlogForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already in use', 'error')
            return render_template('register.html', form=form)

        new_user = users(role='user',
                         email=form.email.data,
                         password=form.password.data,
                         flag_recon=0)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            return render_template('login.html', form=form)

        login_user(user)
        if current_user.role == 'admin':
            return redirect(url_for('admin.privileges'))
        else:
            return redirect(url_for('users.tasks'))

    return render_template('login.html', form=form)


@users_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    conn = sqlite3.connect('instance/ctf.db')
    c = conn.cursor()
    res = c.execute("SELECT * FROM products")

    if form.validate_on_submit():
        name = request.form.get('name')
        conn = sqlite3.connect('instance/ctf.db')
        c = conn.cursor()
        try:
            sql = c.execute("SELECT * FROM products WHERE name LIKE '"'%' + name + '%'"';")
            res = sql.fetchall()
            c.close()
        except TypeError:
            return render_template('search.html', form=form)
        except sqlite3.OperationalError:
            return render_template('search.html', form=form)

        return render_template('search.html', name=name, form=form, res=res)

    return render_template('search.html', form=form, res=res)


@users_blueprint.route('/reconnaissance')
def reconnaissance():
    return render_template('reconnaissance.html')


@users_blueprint.route('/tasks')
def tasks():
    return render_template('tasks.html')


@users_blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SearchForm()

    conn = sqlite3.connect('instance/ctf.db')
    c = conn.cursor()

    sql = c.execute("SELECT flag_recon1 FROM users WHERE id=?", (current_user.id,))
    flag_value_rec1 = sql.fetchone()

    sql = c.execute("SELECT flag_recon2 FROM users WHERE id=?", (current_user.id,))
    flag_value_rec2 = sql.fetchone()

    sql = c.execute("SELECT flag_recon2 FROM users WHERE id=?", (current_user.id,))
    flag_value_cred1 = sql.fetchone()

    if form.validate_on_submit():
        name = request.form.get('name')

        if name == flag_recon1:
            c.execute("UPDATE users SET flag_recon1 = 1 WHERE id=?", (current_user.id,))
            conn.commit()
            flash('Correct flag, well done!', 'success')

        if name == flag_recon2:
            c.execute("UPDATE users SET flag_recon2 = 1 WHERE id=?", (current_user.id,))
            conn.commit()
            flash('Correct flag, well done!', 'success')

        if name == flag_cred1:
            c.execute("UPDATE users SET flag_cred1 = 1 WHERE id=?", (current_user.id,))
            conn.commit()
            flash('Correct flag, well done!', 'success')

        sql = c.execute("SELECT flag_recon1 FROM users WHERE id=?", (current_user.id,))
        flag_value_rec1 = sql.fetchone()

        sql = c.execute("SELECT flag_recon2 FROM users WHERE id=?", (current_user.id,))
        flag_value_rec2 = sql.fetchone()

        sql = c.execute("SELECT flag_recon2 FROM users WHERE id=?", (current_user.id,))
        flag_value_cred1 = sql.fetchone()

        return render_template('submit.html', form=form, flag_value_rec1=flag_value_rec1,
                               flag_value_rec2=flag_value_rec2, flag_value_cred1=flag_value_cred1)

    c.close()
    return render_template('submit.html', form=form, flag_value_rec1=flag_value_rec1,
                           flag_value_rec2=flag_value_rec2, flag_value_cred1=flag_value_cred1)


@users_blueprint.route('/blogs', methods=['GET', 'POST'])
def blogs():
    conn = sqlite3.connect('instance/ctf.db')
    c = conn.cursor()

    sql = c.execute("SELECT * FROM comments")
    all_posts = sql.fetchall()

    form = BlogForm()
    if form.validate_on_submit():
        post = request.form.get('content')
        c.execute("INSERT INTO comments(comment) VALUES (?)", (post,))
        conn.commit()
        c.close()
        return redirect(url_for('users.blogs'))

    return render_template('blogs.html', form=form, all_posts=all_posts)


@users_blueprint.route('/delete', methods=['GET', 'POST'])
def delete():
    conn = sqlite3.connect('instance/ctf.db')
    c = conn.cursor()
    c.execute("DELETE FROM comments")
    conn.commit()
    c.close()
    return blogs()


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
