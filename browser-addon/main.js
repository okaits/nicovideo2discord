function senddata() {
    var player = document.querySelector("#MainVideoPlayer > video");
    var ispaused = player.paused;
    var time = player.currentTime;
    var speed = player.playbackRate;
    var hour = Math.floor(time / 3600);
    var min = Math.floor(time % 3600 / 60);
    var sec = time % 60;
    console.debug("Playing: " + !ispaused);
    var videoid = window.location.pathname.split("/").pop();
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({'status': 'opened', 'videoid': videoid, 'playing': !ispaused, 'ended': false, 'hour': hour, 'min': min, 'sec': sec, 'speed': speed}),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
};

function end() {
    var videoid = window.location.pathname.split("/").pop();
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({'status': 'opened', 'videoid': videoid, 'playing': false, 'ended': true}),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
};

function close() {
    fetch("http://localhost:5000/video", {
        method: 'POST',
        body: JSON.stringify({'status': 'closed'}),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        keepalive: true
    });
};

function onload() {
    var player = document.querySelector("#MainVideoPlayer > video")
    player.addEventListener("play", senddata);
    player.addEventListener("pause", senddata);
    player.addEventListener("waiting", senddata);
    player.addEventListener("seeking", senddata);
    player.addEventListener("seeked", senddata);
    player.addEventListener("ratechange", senddata);
    player.addEventListener("ended", end);
    senddata();
};

window.addEventListener("load", onload)
window.addEventListener("beforeunload", close);
