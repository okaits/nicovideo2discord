""" nicovideo2discord client program """
from __future__ import annotations

import datetime
import json
import time
import urllib.request

import pypresence
import xmltodict

with open("config.json", encoding="UTF-8") as configfile:
    config = json.load(configfile)
CLIENT_ID = config["client_id"]
RPC = pypresence.Presence(CLIENT_ID)
RPC.connect()

beforevideodata = {'status': 'closed'}
while True:
    videodata = json.loads(urllib.request.urlopen("http://localhost:5000/video").read().decode())
    if videodata != beforevideodata:
        print(videodata)
        if videodata["status"] != "opened":
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
        if videodata["ended"] is False:
            playingtime = datetime.timedelta(hours=int(videodata["hour"]), minutes=int(videodata["min"]), seconds=int(videodata["sec"]))
            startedtime = datetime.datetime.now().replace(microsecond=0) - playingtime
        try:
            author = video["user_nickname"]
        except KeyError:
            author = video["ch_name"]
        if videodata["playing"] is True:
            statemsg = f'{video["title"]}'
        elif videodata["ended"] is True:
            statemsg = f'{video["title"]} (再生終了)'
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
