""" nicovideo2discord client program """
from __future__ import annotations

import datetime
import json
import time
import urllib.request

import pypresence
import xmltodict

genres = { #Genres list
    "entertainment": "エンターテインメント",
    "radio": "ラジオ",
    "music_sound": "音楽・サウンド",
    "dance": "ダンス",
    "animal": "動物",
    "nature": "自然",
    "cooking": "料理",
    "traveling_outdoor": "旅行・アウトドア",
    "vehicle": "乗り物",
    "sports": "スポーツ",
    "society_politics_news": "社会・政治・時事",
    "technology_craft": "技術・工作",
    "解説・講座": "commentary_lecture",
    "anime": "アニメ",
    "game": "ゲーム",
    "other": "その他"
}

def debug(message: str, content_type: str = "text/plain") -> urllib.response:
    """ Send debug message to server """
    headers = {"Content-Type": content_type}
    req = urllib.request.Request("http://localhost:5000/debug", message.encode(), headers)
    return urllib.request.urlopen(req)

with open("config.json", encoding="UTF-8") as configfile:
    config = json.load(configfile)
CLIENT_ID = config["client_id"]
RPC = pypresence.Presence(CLIENT_ID)
RPC.connect()

beforevideodata = {'status': 'closed'}
while True:
    videodata = json.loads(urllib.request.urlopen("http://localhost:5000/video").read().decode())
    if videodata != beforevideodata:
        debug("Data changed.")

        if videodata["status"] == "closed": # Page closed
            RPC.clear()
            beforevideodata = videodata
            continue

        elif videodata["status"] == "toppage": # Top page
            RPC.update(
                state="トップページ",
                large_image="niconico_tvchan",
                large_text="ニコニコテレビちゃん",
                buttons=[
                    {
                        "label": "ニコニコ動画トップページ",
                        "url": "https://www.nicovideo.jp/video_top"
                    }
                ]
            )
            beforevideodata = videodata
            continue

        elif videodata["status"] == "ranking": # Ranking Page
            RPC.update(
                state="ランキングを閲覧中",
                large_image="niconico_tvchan",
                large_text="ニコニコテレビちゃん",
                buttons=[
                    {
                        "label": "ニコニコ動画トップページ",
                        "url": "https://www.nicovideo.jp/video_top"
                    },
                    {
                        "label": "ニコニコ動画総合ランキング",
                        "url": "https://www.nicovideo.jp/ranking"
                    }
                ]
            )
            beforevideodata = videodata
            continue

        elif videodata["status"] == "genretoppages": # Genre-separated top pages
            RPC.update(
                state=f'ジャンル: {genres[videodata["genre"]]}',
                details="ジャンル別トップページを閲覧中",
                large_image="niconico_tvchan",
                large_text="ニコニコテレビちゃん",
                buttons=[
                    {
                        "label": "ニコニコ動画トップページ",
                        "url": "https://www.nicovideo.jp/video_top"
                    },
                    {
                        "label": "該当ジャンルトップページ",
                        "url": f'https://www.nicovideo.jp/video_top/genre/{videodata["genre"]}'
                    }
                ]
            )
            beforevideodata = videodata
            continue

        # Watching video
        video = xmltodict.parse(
            urllib.request.urlopen(
                f'http://localhost:5000/videoinfo?vid={videodata["id"]}'
            ).read().decode()
        )
        # Video metadata
        video = video["nicovideo_thumb_response"]["thumb"]
        title = video["title"]
        vid = video["video_id"]
        thumbnail_url = video["thumbnail_url"]
        url = video["watch_url"]
        videolength = video["length"].split(":")
        # Video length
        if len(videolength) == 1:
            videolength = datetime.timedelta(
                seconds=int(videolength[0])
            )
        elif len(videolength) == 2:
            videolength = datetime.timedelta(
                minutes=int(videolength[0]),
                seconds=int(videolength[1])
            )
        elif len(videolength) == 3:
            videolength = datetime.timedelta(
                hours=int(videolength[0]),
                minutes=int(videolength[1]),
                seconds=int(videolength[2])
            )

        # Video ended
        if videodata["ended"] is False:
            playingtime = datetime.timedelta(
                hours=int(videodata["hour"]),
                minutes=int(videodata["min"]),
                seconds=int(videodata["sec"])
            )
            startedtime = datetime.datetime.now().replace(microsecond=0) - playingtime

        # Get author name
        if "user_nickname" in video:
            author = video["user_nickname"]
        else:
            author = video["ch_name"]
        # Set state message
        detailmsg = f'{video["title"]}'
        if videodata["playing"] is False and videodata["ended"] is False:
            detailmsg = f'{detailmsg} (一時停止中)'
        elif videodata["ended"] is True:
            detailmsg = f'{detailmsg} (再生終了)'
        if "speed" in videodata and videodata["speed"] != 1:
            detailmsg = f'{detailmsg} ({videodata["speed"]}倍速)'
        # Set details message
        statemsg = f'投稿者: {author}, 動画長: {video["length"]}'

        # RICKROLL
        if video["video_id"] == "sm5904539":
            detailmsg="リックロールされています"
            statemsg="釣られた"

        # Post those informations into discord
        if videodata["playing"] is True:
            RPC.update(
                details=detailmsg,
                state=statemsg,
                large_image="niconico_tvchan",
                large_text="ニコニコテレビちゃん",
                start=startedtime.timestamp(),
                buttons=[
                    {"label": f'動画を視聴する [{videodata["id"]}]', "url": url},
                    {"label": "ニコニコ動画トップページ", "url": "https://www.nicovideo.jp/video_top/"}
                ],
                instance=True
            )
        else:
            RPC.update(
                details=detailmsg,
                state=statemsg,
                large_image="niconico_tvchan",
                large_text="ニコニコテレビちゃん",
                buttons=[
                    {"label": f'動画を視聴する [{videodata["id"]}]', "url": url},
                    {"label": "ニコニコ動画トップページ", "url": "https://www.nicovideo.jp/video_top/"}
                ]
            )
    beforevideodata = videodata
    time.sleep(1)
