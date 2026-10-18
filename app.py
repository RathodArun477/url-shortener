from flask import Flask
from markupsafe import escape
app = Flask(__name__)

@app.route("/")
def hell_world():
    return {"message":"URL Shortener is working"}
