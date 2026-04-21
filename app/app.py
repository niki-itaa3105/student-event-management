from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devops-secret-key')

ADMIN_EMAIL = "admin@eventhub.com"
ADMIN_PASSWORD = "admin123"

def get_db():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'db'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'root123'),
        database=os.environ.get('MYSQL_DB', 'eventdb')
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            db  = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                        (name, email, password))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already registered.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            session['user_name'] = 'Admin'
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome, {user['name']}!", 'success')
            return redirect(url_for('events'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM events ORDER BY event_date ASC")
    all_events = cur.fetchall()
    cur.execute("SELECT event_id FROM registrations WHERE user_id = %s", (session['user_id'],))
    registered = {row['event_id'] for row in cur.fetchall()}
    return render_template('events.html', events=all_events, registered=registered)

@app.route('/register_event/<int:event_id>', methods=['GET', 'POST'])
def register_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor(dictionary=True)
    if request.method == 'POST':
        phone      = request.form['phone']
        college    = request.form['college']
        department = request.form['department']
        year       = request.form['year']
        food_pref  = request.form['food_pref']
        try:
            cur.execute("""
                INSERT INTO registrations (user_id, event_id, phone, college, department, year, food_pref)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], event_id, phone, college, department, year, food_pref))
            db.commit()
            flash('Successfully registered for the event!', 'success')
            return redirect(url_for('events'))
        except mysql.connector.IntegrityError:
            flash('You already registered for this event.', 'warning')
            return redirect(url_for('events'))
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    return render_template('event_register_form.html', event=event)

@app.route('/cancel_event/<int:event_id>')
def cancel_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM registrations WHERE user_id = %s AND event_id = %s",
                (session['user_id'], event_id))
    db.commit()
    flash('Registration cancelled successfully.', 'info')
    return redirect(url_for('my_events'))

@app.route('/my_events')
def my_events():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT e.*, r.id as reg_id, r.phone, r.college, r.department, r.year, r.food_pref
        FROM events e
        JOIN registrations r ON e.id = r.event_id
        WHERE r.user_id = %s
        ORDER BY e.event_date ASC
    """, (session['user_id'],))
    my_registered = cur.fetchall()
    return render_template('my_events.html', events=my_registered)

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) as total FROM users")
    total_users = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM registrations")
    total_regs = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM events")
    total_events = cur.fetchone()['total']
    cur.execute("""
        SELECT e.id, e.title, e.category, e.event_date, e.location, e.seats,
               COUNT(r.id) as reg_count
        FROM events e
        LEFT JOIN registrations r ON e.id = r.event_id
        GROUP BY e.id
        ORDER BY e.event_date ASC
    """)
    event_stats = cur.fetchall()
    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_regs=total_regs,
                           total_events=total_events,
                           event_stats=event_stats)

@app.route('/admin/event/<int:event_id>')
def admin_event_detail(event_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    cur.execute("""
        SELECT u.name, u.email, r.phone, r.college, r.department, r.year, r.food_pref, r.registered_at
        FROM registrations r
        JOIN users u ON r.user_id = u.id
        WHERE r.event_id = %s
        ORDER BY r.registered_at DESC
    """, (event_id,))
    registrations = cur.fetchall()
    return render_template('admin_event_detail.html', event=event, registrations=registrations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
