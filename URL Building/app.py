from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('home'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
