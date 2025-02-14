"use strict";
var before_player = null
const mutationObserver = new MutationObserver(() => {
    if (document.querySelectorAll('[data-name="video-content"]')[0] != before_player) {
        const player = document.querySelectorAll('[data-name="video-content"]')[0];
        if (player) {
            const video_id = window.location.pathname.split("/").pop();
            const beacon_headers = {type: "application/json"}

            function start_video() {
                navigator.sendBeacon("http://localhost:36201/api/v1/update_watch", new Blob([JSON.stringify({video_id: video_id, time: player.currentTime})], beacon_headers));
            };
            function stop_video() {
                navigator.sendBeacon("http://localhost:36201/api/v1/stop_watch");
            };

            player.addEventListener("play", start_video);
            player.addEventListener("pause", stop_video);
            player.addEventListener("waiting", stop_video);
            player.addEventListener("loadeddata", start_video);
            player.addEventListener("seeking", stop_video);
            player.addEventListener("error", stop_video);
            player.addEventListener("seeked", start_video);
            player.addEventListener("ended", stop_video);
            window.addEventListener("unload", stop_video);
            if (!player.paused) {start_video();};
        };
        before_player = player;
    };
});
mutationObserver.observe(document, {childList: true, subtree: true});
