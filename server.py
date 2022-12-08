"""
nicovideo2discord
このプログラムを使うと、ニコニコ動画で視聴している動画をDiscordのアクティビティに登録できます。
"""

import hashlib
import json
import math
import urllib.request

import xmltodict
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-password"
jwt = JWTManager(app)
CORS(app)
id_dict = {"user1": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"}
class Data():
    """ Data class """
    status = {"user1": {"status": "closed"}}
    cache = {}


def jwt_unauthorized_loader_handler(_):
    return jsonify({"msg": "unauthorized"}), "401 Unauthorized"
jwt.unauthorized_loader(jwt_unauthorized_loader_handler)

@app.route("/login", methods=["POST"])
def login():
    if request.content_type.split(";")[0] == "application/json":
        data = request.json
    elif request.content_type.split(";")[0] == "text/plain":
        data = json.loads(request.data)
    else:
        return jsonify({"msg": "bad content-type"}), "415 Unsupported media type"
    try:
        if data["user"] in id_dict:
            if data["password"] == id_dict[data["user"]]:
                user = data["user"]
            else:
                pwhash = hashlib.sha256()
                pwhash.update(data["password"].encode())
                if pwhash.hexdigest() == id_dict[data["user"]]:
                    user = data["user"]
                else:
                    return jsonify({"msg": "Unauthorized"}), "401 Unauthorized"
    except KeyError:
        return jsonify({"msg": "Unprocessable json"}), "400 Bad request"
    token = create_access_token(identity=user)
    return jsonify({"msg": "ok", "token": token}), "200 OK"

@app.route("/video", methods=["POST", "GET"])
@jwt_required()
def video():
    """ API /video """
    if request.method == "POST":
        if request.content_type.split(";")[0] == "application/json":
            data = request.json
        elif request.content_type.split(";")[0] == "text/plain":
            data = json.loads(request.data)
        else:
            return jsonify({"msg": "bad content-type"}), "415 Unsupported media type"
        print(data)
        try:
            if data["status"] == "closed":
                Data.status[get_jwt_identity()] = {"status": data["status"]}
                return jsonify({"msg": "success"}), "201 Created"
            Data.status[get_jwt_identity()] = {"status": data["status"],"id": data["videoid"], "playing": data["playing"], "hour": data["hour"], "min": data["min"], "sec": str(math.floor(int(data["sec"])))}
        except KeyError:
            print(data)
            return jsonify({"msg": "missing value"}), "400 Bad Request"
        return jsonify({"msg": "success"}), "201 Created"
    elif request.method == "GET":
        return jsonify(Data.status[get_jwt_identity()]), "200 OK"

@app.route("/videoinfo", methods=["GET"])
def videoinfo():
    """ API /videoinfo """
    vid = request.args.get("vid")
    if vid is None:
        return jsonify({"msg": "missing vid."}), "400 Bad Request"
    if vid in Data.cache:
        app.logger.debug("Using cache.") # pylint: disable E1101
        return Response(Data.cache[vid], status="200 OK", mimetype="application/xml")
    url = f"https://ext.nicovideo.jp/api/getthumbinfo/{vid}"
    app.logger.info("Not found in cache. Getting from nicovideo server.") # pylint: disable E1101
    with urllib.request.urlopen(url) as thumbinfo:
        thumbinfo_orig = thumbinfo.read()
        thumbinfo = xmltodict.parse(thumbinfo_orig)
    if thumbinfo["nicovideo_thumb_response"]["@status"] == "fail":
        if thumbinfo["nicovideo_thumb_response"]["error"]["code"] == "NOT_FOUND":
            return Response(thumbinfo_orig, status='404 Not found', mimetype="application/xml")
        elif thumbinfo["nicovideo_thumb_response"]["error"]["code"] == "DELETED":
            return Response(thumbinfo_orig, status="410 Gone", mimetype="application/xml")
        else:
            return Response(thumbinfo_orig, status="400 Bad Request", mimetype="application/xml")
    Data.cache[vid] = thumbinfo_orig
    return thumbinfo_orig


if __name__ == "__main__":
    app.run(debug=True)
