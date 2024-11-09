from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from crontab import CronTab
import os
import json
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Path to the JSON file for storing user data
USER_DATA_FILE = 'users.json'


# Load existing users from JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


# Save users to JSON file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)


# Load users initially
users = load_users()


@app.route('/')
def home():
    if 'username' in session:
        # Load user's schedule
        username = session['username']
        user_data = users.get(username, {})
        schedule = user_data.get('schedule', {})
        # Pass schedule data to the dashboard
        return render_template('dashboard.html', username=username, schedule=schedule)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username in users and users[username]['password'] == hashed_password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials", 403

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username in users:
            return "Username already exists", 409

        users[username] = {'password': hashed_password}
        save_users(users)

        session['username'] = username
        return redirect(url_for('home'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_data = users.get(username, {})
    current_schedule = user_data.get('schedule', {})

    if request.method == 'POST':
        days = request.form.getlist('days')  # Get list of selected days
        time = request.form['time']  # Time in HH:MM format
        user_schedule = {'days': days, 'time': time}

        # Save schedule to user data and update JSON file
        users[username]['schedule'] = user_schedule
        save_users(users)

        # Update cron job with the new schedule
        # setup_cron_jobs(username, days, time)
        return redirect(url_for('home'))

    return render_template('schedule.html', schedule=current_schedule)


def setup_cron_jobs(username, days, time):
    hour, minute = map(int, time.split(':'))

    # Create cron job specific to this user
    cron = CronTab(user=True)
    command = f'docker run -e USERNAME="{username}" -e PASSWORD="{users[username]["password"]}" food_order_container'

    # Remove existing jobs for this user
    cron.remove_all(comment=username)

    # Add new job for each selected day
    for day in days:
        job = cron.new(command=command, comment=username)
        job.setall(minute, hour, f"* * {day}")

    cron.write()


@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    """API to retrieve the user's schedule for display on the calendar."""
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403

    username = session['username']
    user_data = users.get(username, {})
    schedule = user_data.get('schedule', {})
    scheduled_dates = calculate_scheduled_dates(schedule)

    return jsonify(scheduled_dates)


def calculate_scheduled_dates(schedule):
    """Calculate the scheduled dates based on user's selected days and time."""
    days = schedule.get('days', [])
    time = schedule.get('time', '00:00')
    scheduled_dates = []
    now = datetime.now()

    for day in days:
        day_diff = (int(day) - now.weekday()) % 7
        scheduled_date = now + timedelta(days=day_diff)
        scheduled_date_str = scheduled_date.strftime(f"%Y-%m-%d {time}")
        scheduled_dates.append(scheduled_date_str)

    return scheduled_dates


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
