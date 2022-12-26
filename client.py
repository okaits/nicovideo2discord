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
        print("Data changed.")
        if videodata["status"] == "closed":
            RPC.clear()
            beforevideodata = videodata
            continue
        elif videodata["status"] == "videointro":
            RPC.update(
                state="トップページ: いきなり！動画紹介を視聴中",
                large_image="https://nicovideo.cdn.nimg.jp/web/images/favicon/144.png",
                large_text="ニコニコテレビちゃん",
                buttons=[{"label": "ニコニコ動画トップページ", "url": "https://www.nicovideo.jp/video_top"}]
            )
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
        statemsg = f'{video["title"]}'
        if videodata["playing"] is False:
            statemsg = f'{statemsg} (一時停止中)'
        if "speed" in videodata and videodata["speed"] != 1:
            statemsg = f'{statemsg} ({videodata["speed"]}倍速)'
        if videodata["ended"] is True:
            statemsg = f'{statemsg} (再生終了)'
        detailsmsg = f'投稿者: {author}'
        if videodata["playing"] is True:
            RPC.update(
                state=statemsg,
                details=detailsmsg,
                large_image=thumbnail_url,
                large_text=vid,
                small_image="https://nicovideo.cdn.nimg.jp/web/images/favicon/144.png",
                small_text="ニコニコテレビちゃん",
                start=startedtime.timestamp(),
                buttons=[
                    {"label": "動画を視聴する", "url": url},
                    {"label": "ニコニコ動画トップページ", "url": "https://www.nicovideo.jp/video_top/"}
                ],
                instance=True
            )
        else:
            RPC.update(
                state=statemsg,
                details=detailsmsg,
                large_image=thumbnail_url,
                small_image="https://nicovideo.cdn.nimg.jp/web/images/favicon/144.png",
                small_text="ニコニコテレビちゃん",
                large_text="Thumbnail",
                buttons=[
                    {"label": "動画を視聴する", "url": url},
                    {"label": "ニコニコ動画トップページ", "url": "https://www.nicovideo.jp/video_top/"}
                ]
            )
    beforevideodata = videodata
    time.sleep(1)
