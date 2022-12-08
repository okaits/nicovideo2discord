token = ""
function beforeunload(token) {
    // navigator.sendBeacon("http://localhost:5000/video", JSON.stringify({"status": "closed"}));
    body = JSON.stringify({"status": "closed"});
    fetch("http://localhost:5000/video", {
        method: 'POST',
        body: JSON.stringify({"status": "closed"}),
        headers: {
            "Content-type": "application/json",
            "Authorization": "Bearer " + this.token
        },
        keepalive: true
    });
};

function ajaxerror(xhr, testStatus, errorThrown) {
    if (xhr.status == 401) {
        console.log("Reloading token...")
        token = gettoken("password")
    };
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};

async function gettoken(password) {
    tokenrecv = $.ajax(
        {
            type: "POST",
            url: "http://localhost:5000/login",
            data: JSON.stringify({"user": "user1", "password": password}),
            contentType: "application/json; charset=UTF-8"
        }
    );
    while (true) {
        await sleep(50);
        if (tokenrecv.responseJSON == undefined) {
            continue;
        } else {
            token = tokenrecv.responseJSON["token"];
            window.addEventListener('beforeunload', {token: token, handleEvent: beforeunload});
            return token
        };
    };
};

token = gettoken("password");

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
            headers: {"Authorization": "Bearer " + token},
            contentType: "application/json; charset=UTF-8",
            error: ajaxerror});
        beforepaused = ispaused;
    };
};
console.debug("start")
loop();
