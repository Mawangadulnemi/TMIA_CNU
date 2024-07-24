document.addEventListener('DOMContentLoaded', async () => {
    const questionList = document.getElementById('question-list');
    const apiBaseUrl = '/api/conversation';
    const remoteVideo = document.getElementById('remoteVideo');
    const remoteVideo2 = document.getElementById('remoteVideo2');
    const localVideo = document.getElementById('localVideo');
    const baseVideoUrl = './assets/videos/baseVideo.mp4';

    // 기본 비디오 설정
    remoteVideo.src = baseVideoUrl;
    remoteVideo.autoplay = true;
    remoteVideo.loop = false; // 루프를 끄고 비디오가 끝날 때마다 효과 적용

    const response = await fetch('/question.txt');
    const text = await response.text();
    const questions = text.split('\n').filter((question) => question.trim().length > 0);

    questions.forEach((question, index) => {
        const listItem = document.createElement('li');
        const button = document.createElement('button');
        button.textContent = question;
        button.classList.add(`question${index + 1}`);
        listItem.appendChild(button);
        questionList.appendChild(listItem);
    });

    questionList.querySelectorAll('button').forEach((button, index) => {
        button.addEventListener('click', () => {
            const q = index + 1;
            const id = '34343';
            fetchVideo(id, q, apiBaseUrl, baseVideoUrl);
        });
    });

    const muteButton = document.getElementById('muteButton');
    const cameraButton = document.getElementById('cameraButton');
    const fullscreenButton = document.getElementById('fullscreenButton');
    const endCallButton = document.getElementById('endCallButton');

    let isMuted = true;
    let isCameraOn = true;

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = stream;

        muteButton.addEventListener('click', () => {
            isMuted = !isMuted;
            stream.getAudioTracks()[0].enabled = !isMuted;
            muteButton.innerHTML = isMuted
                ? '<i class="fa-solid fa-microphone-slash"></i>'
                : '<i class="fa-solid fa-microphone"></i>';
        });

        cameraButton.addEventListener('click', () => {
            isCameraOn = !isCameraOn;
            stream.getVideoTracks()[0].enabled = isCameraOn;
            cameraButton.innerHTML = isCameraOn
                ? '<i class="fa-solid fa-video"></i>'
                : '<i class="fa-solid fa-video-slash"></i>';
        });

        fullscreenButton.addEventListener('click', () => {
            const videoContainer = document.getElementById('video-container');
            if (!document.fullscreenElement) {
                videoContainer.requestFullscreen();
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        });

        endCallButton.addEventListener('click', () => {
            window.location.href = 'select.html';
        });

        let mediaRecorder;
        let audioChunks = [];

        document.addEventListener('keydown', (event) => {
            if (event.code === 'Space' && stream) {
                stream.getAudioTracks()[0].enabled = true;
                muteButton.innerHTML = '<i class="fa-solid fa-microphone"></i>';

                if (!mediaRecorder || mediaRecorder.state === 'inactive') {
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.ondataavailable = (e) => {
                        audioChunks.push(e.data);
                    };
                    mediaRecorder.onstop = () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        audioChunks = [];
                        sendAudio(audioBlob, apiBaseUrl, baseVideoUrl);
                    };
                    mediaRecorder.start();
                }
            }
        });

        document.addEventListener('keyup', (event) => {
            if (event.code === 'Space' && mediaRecorder && mediaRecorder.state === 'recording') {
                stream.getAudioTracks()[0].enabled = false;
                muteButton.innerHTML = '<i class="fa-solid fa-microphone-slash"></i>';
                mediaRecorder.stop();
            }
        });

        // 기본 비디오가 끝날 때마다 크로스페이드 효과 적용
        remoteVideo.onended = () => {
            crossfade(remoteVideo, remoteVideo2, baseVideoUrl, () => {
                remoteVideo.loop = false; // Disable looping for the fetched video
            });
        };

        remoteVideo2.onended = () => {
            crossfade(remoteVideo2, remoteVideo, baseVideoUrl, () => {
                remoteVideo2.loop = false; // Disable looping for the fetched video
            });
        };
    } catch (error) {
        console.error('미디어 장치 접근 오류.', error);
    }
});

async function fetchVideo(id, q, apiBaseUrl, baseVideoUrl) {
    const currentVideo = document.getElementById('remoteVideo').classList.contains('hidden')
        ? document.getElementById('remoteVideo2')
        : document.getElementById('remoteVideo');
    const nextVideo =
        currentVideo.id === 'remoteVideo'
            ? document.getElementById('remoteVideo2')
            : document.getElementById('remoteVideo');
    const apiUrl = `${apiBaseUrl}/${id}?q=${q}`;
    const token = 'BEARER_TOKEN';

    try {
        const response = await fetch(apiUrl, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const videoBlob = await response.blob();
        const videoUrl = URL.createObjectURL(videoBlob);

        crossfade(currentVideo, nextVideo, videoUrl, () => {
            nextVideo.loop = false; // Disable looping for the fetched video
            nextVideo.onended = () => {
                crossfade(nextVideo, currentVideo, baseVideoUrl, () => {
                    currentVideo.loop = true; // Re-enable looping for the base video
                });
            };
        });
    } catch (error) {
        console.error('비디오 가져오기 오류:', error);
    }
}

async function sendAudio(audioBlob, apiBaseUrl, baseVideoUrl) {
    const currentVideo = document.getElementById('remoteVideo').classList.contains('hidden')
        ? document.getElementById('remoteVideo2')
        : document.getElementById('remoteVideo');
    const nextVideo =
        currentVideo.id === 'remoteVideo'
            ? document.getElementById('remoteVideo2')
            : document.getElementById('remoteVideo');
    const conversationId = '33';
    const apiUrl = `${apiBaseUrl}/${conversationId}`;
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('네트워크 응답이 올바르지 않습니다 ' + response.statusText);
        }

        const videoBlob = await response.blob();
        const videoUrl = URL.createObjectURL(videoBlob);

        crossfade(currentVideo, nextVideo, videoUrl, () => {
            nextVideo.loop = false; // Disable looping for the fetched video
            nextVideo.onended = () => {
                crossfade(nextVideo, currentVideo, baseVideoUrl, () => {
                    currentVideo.loop = true; // Re-enable looping for the base video
                });
            };
        });
    } catch (error) {
        console.error('오류:', error);
    }
}

function crossfade(currentVideo, nextVideo, newSource, callback) {
    // Pause the current video and disable its audio track
    currentVideo.pause();
    currentVideo.muted = true;

    // Load the next video source
    nextVideo.src = newSource;
    nextVideo.muted = false; // Ensure the next video is unmuted
    nextVideo.onloadeddata = () => {
        currentVideo.classList.add('hidden');
        nextVideo.classList.remove('hidden');
        nextVideo.play();
        if (callback) callback();
    };
}

document.addEventListener('DOMContentLoaded', () => {
    function updateTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        document.getElementById('current-time').textContent = `${hours}:${minutes}`;
    }

    updateTime();
    setInterval(updateTime, 60000); // Update every minute
});
