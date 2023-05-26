function senddata() {
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({"status": "ranking"}),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    })
    .catch(error => {console.log("Couldn't communicate to the server.")});
};
function close() {
    fetch("http://localhost:5000/video", {
        method: "POST",
        body: JSON.stringify({"status": "closed"}),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        },
        keepalive: true
    })
    .catch(error => {console.log("Couldn't communicate to the server.")});
};

senddata();
window.addEventListener("beforeunload", close);