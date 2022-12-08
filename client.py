""" niconico2discord client program """
from __future__ import annotations

import datetime
import hashlib
import json
import time
import urllib.request

import pypresence
import xmltodict

CLIENT_ID = "DISCORD_CLIENT_ID_HERE"
RPC = pypresence.Presence(CLIENT_ID)
RPC.connect()

class Auth():
    """ Class about Auth information """
    class User():
        """ Class about user information """
        def __init__(self, username: str, password: str):
            self.username = username
            self.password = hashlib.sha256()
            self.password.update(password.encode())
            self.password = self.password.hexdigest()
    class Token():
        """ JMT class """
        def __init__(self):
            self.token = ""
        def get(self, user: Auth.User):
            """ Get JMT from server """
            tokenrequest = urllib.request.Request("http://localhost:5000/login", headers={"Content-type": "application/json"}, data=json.dumps({"user": user.username, "password": user.password}).encode())
            self.token = json.load(urllib.request.urlopen(tokenrequest))["token"]

token = Auth.Token()
token.get(Auth.User("user1", "password"))

videodata_request = urllib.request.Request("http://localhost:5000/video", headers={"Authorization": f"Bearer {token.token}"})
beforevideodata = {}
beforeestimatedendtime = datetime.timedelta(seconds=0)
while True:
    try:
        videodata = json.loads(urllib.request.urlopen(videodata_request).read().decode())
    except urllib.error.HTTPError:
        token.get(Auth.User("user1", "password"))
        videodata_request = urllib.request.Request("http://localhost:5000/video", headers={"Authorization": f"Bearer {token.token}"})
        continue
    if videodata != beforevideodata:
        print(videodata)
        if videodata["status"] == "closed":
            RPC.clear()
            beforevideodata = videodata
            continue
        video = xmltodict.parse(urllib.request.urlopen(f'http://localhost:5000/videoinfo?vid={videodata["id"]}').read().decode())
        video = video["nicovideo_thumb_response"]["thumb"]
        title = video["title"]
        vid = video["video_id"]
        thumbnail_url = video["thumbnail_url"]
        url = video["watch_url"]
        videolength = video["length"].split(":")
        if len(videolength) == 1:
            videolength = datetime.timedelta(seconds=int(videolength[0]))
        elif len(videolength) == 2:
            videolength = datetime.timedelta(minutes=int(videolength[0]), seconds=int(videolength[1]))
        elif len(videolength) == 3:
            videolength = datetime.timedelta(hours=int(videolength[0]), minutes=int(videolength[1]), seconds=int(videolength[2]))
        playingtime = datetime.timedelta(hours=int(videodata["hour"]), minutes=int(videodata["min"]), seconds=int(videodata["sec"]))
        startedtime = datetime.datetime.now().replace(microsecond=0) - playingtime
        estimatedendtime = datetime.datetime.now().replace(microsecond=0) + videolength - playingtime
        if estimatedendtime == beforeestimatedendtime and videodata["sec"] == beforevideodata["sec"]:
            beforevideodata = videodata
            time.sleep(1)
            continue
        try:
            author = video["user_nickname"]
        except KeyError:
            author = video["ch_name"]
        if videodata["playing"] is True:
            statemsg = f'{video["title"]}'
        else:
            statemsg = f'{video["title"]} (一時停止中)'
        detailsmsg = f'投稿者: {author}'
        if videodata["playing"] is True:
            RPC.update(
                state=statemsg,
                details=detailsmsg,
                large_image=thumbnail_url,
                large_text=vid,
                start=startedtime.timestamp(),
                end=estimatedendtime.timestamp(),
                buttons=[{"label": "動画を視聴する", "url": url}],
                instance=True
            )
        else:
            RPC.update(
                state=statemsg,
                details=detailsmsg,
                large_image=thumbnail_url,
                large_text="Thumbnail",
                buttons=[{"label": "動画を視聴する", "url": url}]
            )
    beforevideodata = videodata
    time.sleep(1)
