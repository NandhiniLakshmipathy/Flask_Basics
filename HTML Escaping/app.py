from flask import Flask 
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "Route to /your_name"
  
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
