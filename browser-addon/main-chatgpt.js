$.ajax({
  url: 'http://localhost:5000/login',
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({user: "user1", password: "password"}),
  success: function(data) {
    // 認証に成功したら、トークンを取得する
    var token = data.token;

    // ビデオの再生状態が変わった時にも送信する
    mainVideoPlayer.addEventListener('pause', function() {
      // 現在の再生状態を取得する
      var isPaused = mainVideoPlayer.paused;
      var currentTime = mainVideoPlayer.currentTime;
      var hour = Math.floor(currentTime / 3600);
      var min = Math.floor(currentTime / 60) % 60;
      var sec = Math.floor(currentTime % 60);

      // 送信するデータを作成する
      var videoData = {
        status: "opened",
        videoid: filename,
        playing: !isPaused,
        hour: hour,
        min: min,
        sec: sec
      };

      // データを送信する
      $.ajax({
        url: 'http://localhost:5000/video',
        type: 'POST',
        contentType: 'application/json',
        headers: {
          'Authorization': 'Bearer ' + token
        },
        data: JSON.stringify(videoData),
      });
      mainVideoPlayer.addEventListener('play', function() {
        // 現在の再生状態を取得する
        var isPaused = mainVideoPlayer.paused;
        var currentTime = mainVideoPlayer.currentTime;
        var hour = Math.floor(currentTime / 3600);
        var min = Math.floor(currentTime / 60) % 60;
        var sec = Math.floor(currentTime % 60);
      
        // 送信するデータを作成する
        var videoData = {
          status: "opened",
          videoid: filename,
          playing: !isPaused,
          hour: hour,
          min: min,
          sec: sec
        };
      
        // データを送信する
        $.ajax({
          url: 'http://localhost:5000/video',
          type: 'POST',
          contentType: 'application/json',
          headers: {
            'Authorization': 'Bearer ' + token
          },
          data: JSON.stringify(videoData),
        });
      });
      
      // ページを閉じる時に{"status": "closed"}を送信する
      $(window).on('beforeunload', function() {
        $.ajax({
          url: 'http://localhost:5000/video',
          type: 'POST',
          contentType: 'application/json',
          headers: {
            'Authorization': 'Bearer ' + token
          },
          data: JSON.stringify({status: "closed"}),
        });
      });
    });
  }
});