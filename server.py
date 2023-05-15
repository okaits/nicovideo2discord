"""
nicovideo2discord
このプログラムを使うと、ニコニコ動画で視聴している動画をDiscordのアクティビティに登録できます。
"""

import json
import math
import urllib.request
import xmltodict
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
class Data():
    """ Data class """
    status = {"status": "closed"}
    cache = {}

@app.route("/video", methods=["POST", "GET"])
def video():
    """ API /video """
    if request.method == "POST":
        # Check Content-Type
        if request.content_type.split(";")[0] == "application/json":
            data = request.json
        elif request.content_type.split(";")[0] == "text/plain":
            data = json.loads(request.data)
        else:
            return jsonify({"msg": "bad content-type"}), "415 Unsupported media type"

        try:
            if data["status"] == "closed": # Page closed
                Data.status = {
                    "status": data["status"]
                }
                return jsonify({"msg": "success"}), "201 Created"

            elif data["status"] == "toppage" or data["status"] == "ranking": # Main top page or Ranking page
                Data.status = {
                    "status": data["status"]
                }
                return jsonify({"msg": "success"}), "201 Created"

            elif data["status"] == "genretoppages": # Genre-separated top page
                Data.status = {
                    "status": data["status"],
                    "genre": data["genre"]
                }
                return jsonify({"msg": "success"}), "201 Created"

            elif data["ended"] is True: # Video ended
                Data.status = {
                    "status": data["status"],
                    "id": data["videoid"],
                    "ended": data["ended"],
                    "playing": data["playing"]
                }
                return jsonify({"msg": "success"}), "201 Created"

            Data.status = { # Watching video
                "status": data["status"],
                "id": data["videoid"],
                "ended": data["ended"],
                "playing": data["playing"],
                "hour": data["hour"],
                "min": data["min"],
                "sec": str(math.floor(int(data["sec"]))),
                "speed": data["speed"]
            }

        except KeyError:
            return jsonify({"msg": "missing value"}), "400 Bad Request"

        return jsonify({"msg": "success"}), "201 Created"

    elif request.method == "GET":
        return jsonify(Data.status), "200 OK"

@app.route("/videoinfo", methods=["GET"])
def videoinfo():
    """ API /videoinfo """
    vid = request.args.get("vid")

    if vid is None:
        return jsonify({"msg": "missing vid."}), "400 Bad Request"
    if vid in Data.cache:
        app.logger.debug("Using cache.") # pylint: disable=E1101
        return Response(Data.cache[vid], status="200 OK", mimetype="application/xml")

    url = f"https://ext.nicovideo.jp/api/getthumbinfo/{vid}"
    app.logger.info("Not found in cache. Getting from nicovideo server.") # pylint: disable=E1101
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
