"use strict";
var before_player = null;
var lock = false;
var waiting = null;

const mutationObserver = new MutationObserver(() => {
    if (document.querySelectorAll('[data-name="video-content"]')[0] != before_player) {
        const player = document.querySelectorAll('[data-name="video-content"]')[0];
        if (player) {
            const video_id = window.location.pathname.split("/").pop();

            function start_video() {
                const start_xhr = new XMLHttpRequest();
                start_xhr.open("POST", "http://localhost:36201/api/v1/update_watch", false);
                start_xhr.setRequestHeader("Content-Type", "application/json");
                start_xhr.send(JSON.stringify({video_id: video_id, time: player.currentTime}));
            }
            function stop_video() {
                const stop_xhr = new XMLHttpRequest();
                stop_xhr.open("POST", "http://localhost:36201/api/v1/stop_watch", false);
                stop_xhr.send();
            };
            function page_close() {
                navigator.sendBeacon("http://localhost:36201/api/v1/stop_watch");
            }
            function wrapped_start_video() {
                waiting = start_video;
            };
            function wrapped_stop_video() {
                waiting = stop_video;
            };

            player.addEventListener("play", wrapped_start_video);
            player.addEventListener("pause", wrapped_stop_video);
            player.addEventListener("waiting", wrapped_stop_video);
            player.addEventListener("loadeddata", wrapped_start_video);
            player.addEventListener("seeking", wrapped_stop_video);
            player.addEventListener("error", wrapped_stop_video);
            player.addEventListener("seeked", wrapped_start_video);
            player.addEventListener("ended", wrapped_stop_video);
            window.addEventListener("unload", page_close);
            if (!player.paused) {start_video();};
        };
        before_player = player;
    };
});
mutationObserver.observe(document, {childList: true, subtree: true});

function send_data() {
    if (!lock) {
        if (waiting) {
            lock = true;
            waiting();
            waiting = null;
            lock = false;
        };
    };
};
setInterval(send_data, 100);
