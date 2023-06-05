from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from models import User, TestCase
from datetime import datetime
from flask import jsonify



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('tests'))
    flash('Invalid username or password')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('index'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tests')
@login_required
def tests():
    tests = TestCase.query.all()

    return render_template('tests.html', tests=tests)


@app.route('/tests/add', methods=['GET', 'POST'])
@login_required
def add_test():
    if request.method == 'POST':
        test_name = request.form.get('test_name')
        scenario = request.form.get('scenario')
        suite = request.form.get('suite')
        version = request.form.get('version')
        format_date=datetime.utcnow()
        date_added=format_date.strftime('%Y-%m-%d')

        if not test_name:
            flash('Test name is required!')
            return redirect(url_for('add_test'))
        
        test = TestCase(name=test_name, scenario=scenario, suite=suite, version=version, date_added=date_added, added_by=current_user.id)
        db.session.add(test)
        db.session.commit()
        
        flash('Test added successfully')
        return redirect(url_for('tests'))
    return render_template('add_test.html')

@app.route('/tests/set_status/<int:test_id>/<status>', methods=['POST'])
@login_required
def set_test_status(test_id, status):
    test = TestCase.query.get(test_id)
    if test:
        test.status = status
        db.session.commit()
        flash('Test status updated successfully')
    else:
        flash('Test not found')
    return redirect(url_for('tests'))


@app.route('/tests/set_failed/<int:test_id>', methods=['POST'])
@login_required
def set_failed(test_id):
    test = TestCase.query.get_or_404(test_id)
    if test:
        test.status = 'failed'
        db.session.commit()
    return redirect(url_for('tests'))

@app.route('/tests/set_in_progress/<int:test_id>', methods=['POST'])
@login_required
def set_in_progress(test_id):
    test = TestCase.query.get_or_404(test_id)
    if test:
        test.status = 'in_progress'
        db.session.commit()
    return redirect(url_for('tests'))

@app.route('/tests/set_passed/<int:test_id>', methods=['POST'])
@login_required
def set_passed(test_id):
    test = TestCase.query.get_or_404(test_id)
    if test:
        test.status = 'passed'
        db.session.commit()
    return redirect(url_for('tests'))

@app.route('/tests/clear/<int:test_id>', methods=['POST'])
@login_required
def clear(test_id):
    test = TestCase.query.get_or_404(test_id)
    if test:
        test.status = 'not_set'
        db.session.commit()
    return redirect(url_for('tests'))


@app.route('/tests/<int:test_id>', methods=['GET'])
def get_test_details(test_id):
    test = TestCase.query.get_or_404(test_id)
    test_details = {
        'id': test.id,
        'name': test.name,
        'scenario': test.scenario,
        'suite': test.suite,
        'version': test.version,
        'status': test.status,
        'dateAdded': str(test.date_added),
        'lastModified': str(test.last_modified),
        'addedBy': test.added_by
    }
    return jsonify(test_details)



