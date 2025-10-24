from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Simple in-memory storage (use DB like SQLite/MySQL for production)
users = {}
assignments = {
    "Meghana": ["AI Assignment", "Python Project", "Web Services Notes"]
}

@app.route('/')
def home():
    return redirect(url_for('stu_login'))

@app.route('/stu_login', methods=['GET', 'POST'])
def stu_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username]['password'], password):
            session['user'] = username
            flash('Login Successful!', 'success')
            return redirect(url_for('stu_assignments'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('stu_login.html')

@app.route('/stu_reg', methods=['GET', 'POST'])
def stu_reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Try a new one.', 'danger')
        else:
            users[username] = {'password': generate_password_hash(password)}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('stu_login'))
    return render_template('stu_reg.html')

@app.route('/stu_assignments')
def stu_assignments():
    if 'user' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('stu_login'))
    
    user = session['user']
    user_assignments = assignments.get(user, ["No assignments yet."])
    return render_template('stu_assignments.html', user=user, assignments=user_assignments)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('stu_login'))

if __name__ == '__main__':
    app.run(debug=True)
