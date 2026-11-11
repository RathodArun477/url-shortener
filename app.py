from flask import Flask,request,jsonify,redirect
# from markupsafe import escape
from utils import generate_code
from db import insert_db,init_db,get_original_url
MAX_ATTEMPTS = 5
app = Flask(__name__)
init_db()

@app.route("/")
def hello_world():
    return {"message":"URL Shortener is working"}

@app.route("/shorten",methods=['POST'])
def shorten():
    data = request.get_json(silent=True)
    
    if not isinstance(data,dict) or not data:
        return jsonify({"message":"no url received"}),400

    url = data.get("url")

    if not isinstance(url,str) or not url.strip():
        return jsonify({"message":"incorrect url received"}),400
    url = url.strip()
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


@app.route('/<code>',methods=['GET'])
def redirect_url(code):
    original = get_original_url(code)

    if not original:
        return jsonify({"message":"no url found, please try again"}),404

    return redirect(original)