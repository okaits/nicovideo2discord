function beforeunload() {
    // navigator.sendBeacon("http://localhost:5000/video", JSON.stringify({"status": "closed"}));
    body = JSON.stringify({"status": "closed"});
    fetch("http://localhost:5000/video", {
        method: 'POST',
        body: JSON.stringify({"status": "closed"}),
        headers: {
            "Content-type": "application/json"
        },
        keepalive: true
    });
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};

async function loop() {
    var beforepaused = true;
    while (true) {
        await sleep(500);
        var player = document.getElementById("MainVideoPlayer").firstElementChild;
        var ispaused = player.paused;
        var time = player.currentTime;
        var hour = Math.floor(time / 3600);
        var min = Math.floor(time % 3600 / 60);
        var sec = time % 60;
        if (ispaused == beforepaused) {
            continue;
        };
        console.debug("Playing: " + !ispaused);
        var videoid = window.location.pathname.split("/").pop();
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/video",
            data: JSON.stringify({'status': 'opened', 'videoid': videoid, 'playing': !ispaused, 'hour': hour, 'min': min, 'sec': sec}),
            contentType: "application/json; charset=UTF-8"
        });
        beforepaused = ispaused;
    };
};
console.debug("start")
loop();
