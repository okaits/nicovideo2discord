function senddata() {
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({"status": "ranking"}),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    });
};
function close() {
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({"status": "closed"}),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        },
        keepalive: true
    });
};

senddata();
window.addEventListener("beforeunload", close);