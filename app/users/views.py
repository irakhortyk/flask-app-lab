from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

users_bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')

VALID_USERS = {
    "user1": "12345",
    "admin": "password"
}

@users_bp.route('/hi/<string:name>')
def greetings(name):
    age = request.args.get('age')
    return render_template('users/hi.html', name=name.upper(), age=age)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in VALID_USERS and VALID_USERS[username] == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/hi.html', page='login')


@users_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему для доступу до профілю!', 'danger')
        return redirect(url_for('users.login'))

    username = session['username']
    theme = request.cookies.get('theme', 'light')

    if request.method == 'POST':
        action = request.form.get('action')
        response = make_response(redirect(url_for('users.profile')))

        if action == 'add_cookie':
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            max_age = request.form.get('cookie_max_age')

            if key and value:
                try:
                    max_age_val = int(max_age) if max_age else None
                    response.set_cookie(key, value, max_age=max_age_val)
                    flash(f'Кукі "{key}" успішно додано!', 'success')
                except ValueError:
                    flash('Термін дії має бути числом!', 'warning')
            else:
                flash('Заповніть ключ та значення кукі!', 'warning')
            return response

        elif action == 'delete_cookie':
            key = request.form.get('delete_key')
            if key in request.cookies:
                response.delete_cookie(key)
                flash(f'Кукі "{key}" успішно видалено!', 'info')
            else:
                flash(f'Кукі "{key}" не знайдено!', 'warning')
            return response

        elif action == 'delete_all_cookies':
            for key in request.cookies.keys():
                if key != 'session':
                    response.delete_cookie(key)
            flash('Усі кукі успішно видалено!', 'info')
            return response

    return render_template(
        'users/hi.html',
        page='profile',
        username=username,
        cookies=request.cookies,
        theme=theme
    )


@users_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи!', 'info')
    return redirect(url_for('users.login'))


@users_bp.route('/set-theme/<theme_name>')
def set_theme(theme_name):
    if theme_name not in ['light', 'dark']:
        theme_name = 'light'
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme_name, max_age=2592000)
    flash(f'Тему змінено на {"темну" if theme_name == "dark" else "світлу"}!', 'success')
    return response