    window.onload = function() {
        var socket = io.connect('https://' + document.domain + ':' + location.port);
        var videoElement = document.getElementById('video-stream');
        var stopButton = document.getElementById('stop-stream');
        var stream;
        var mediaRecorder;
        var chunks = [];

        var s_id = document.getElementById("feed_id").getAttribute("data-s-id");
        socket.emit('start_stream', { s_id: s_id });

        navigator.mediaDevices.getUserMedia({ video: { mimeType: 'video/mpeg' } }) 
        .then(function(userStream) {
                videoElement.srcObject = userStream;
                stream = userStream;
                mediaRecorder = new MediaRecorder(userStream);

                
                mediaRecorder.ondataavailable = function(event) {
                    if (event.data.size > 0) {
                        chunks.push(event.data);
                        socket.emit('stream_data', { data: event.data });
                    }
                };

                mediaRecorder.onstop = function() {
                    var blob = new Blob(chunks, { type: 'video/mpeg' }); 
                    var formData = new FormData();
                    formData.append('video', blob);
                
                    fetch('https://192.168.1.21:5000/save_video', {
                        method: 'POST',
                        body: formData,
                    }).then(function(response) {
                        if (response.ok) {
                            console.log('Video saved successfully on the server.');
                        } else {
                            console.error('Failed to save video on the server.');
                        }
                    }).catch(function(error) {
                        console.error('Error saving video:', error);
                    });
                };
                

                mediaRecorder.start();

                stopButton.addEventListener('click', function() {
                    if (stream) {
                        stream.getTracks().forEach(function(track) {
                            track.stop();
                        });
                    }
                    mediaRecorder.stop();
                    window.location.href = '/homepage';
                });
            })
            .catch(function(error) {
                console.error('Error accessing camera:', error);
            });
    };
