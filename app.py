from flask import Flask, request, jsonify, redirect, render_template
from urllib.parse import urlparse
from utils import generate_code
from db import insert_db, init_db, get_original_url, get_url_stats
MAX_ATTEMPTS = 5
app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten",methods=['POST'])
def shorten():
    data = request.get_json(silent=True)
    
    if not isinstance(data,dict) or not data:
        return jsonify({"message":"no url received"}),400

    url = data.get("url")

    if not isinstance(url,str) or not url.strip():
        return jsonify({"message":"incorrect url received"}),400
    url = url.strip()
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    elif parsed.scheme not in ("http","https"):
        return jsonify({"message":"invalid url scheme"}),400
    for attempt in range(MAX_ATTEMPTS):
        code = generate_code()

        if insert_db(code,url):
            short_url = request.host_url + code

            return jsonify({
                "message":"url shortened successfully",
                "code":code,
                "short_url":short_url
            }),201

    return jsonify({"message":"could not generate a unique code, please try again"}),500


@app.route('/stats/<code>', methods=['GET'])
def stats(code):
    data = get_url_stats(code)
    if not data:
        return jsonify({"message": "no url found"}), 404
    return jsonify(data), 200


@app.route('/<code>',methods=['GET'])
def redirect_url(code):
    original = get_original_url(code)

    if not original:
        return jsonify({"message":"no url found, please try again"}),404

    return redirect(original)