import sqlite3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db, requires_roles, users
from users.forms import SearchForm

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin-home.html')


@admin_blueprint.route('/privileges', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def privileges():

    form = SearchForm()

    conn = sqlite3.connect('C:/Users/jacob/PycharmProjects/Capture/instance/ctf.db')
    c = conn.cursor()
    res = c.execute("SELECT * FROM users")

    if form.validate_on_submit():
        user_id = request.form.get('name')
        try:
            c.execute("UPDATE users SET role = 'admin' WHERE id=?", user_id)
        except sqlite3.ProgrammingError:
            return redirect(url_for('admin.privileges'))
        conn.commit()
        c.close()
        return redirect(url_for('admin.privileges'))

    return render_template('privileges.html', form=form, res=res)
