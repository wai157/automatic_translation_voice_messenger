const mic_btn = document.getElementById('mic-btn')

mic_btn.addEventListener('click', ToggleMic)

var can_record = false
var is_recording = false

var recorder = null

var chunks = []
var audio_src = null
var audio_blob = null

function SetupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then(SetupStream)
        .catch((err) => {
            console.error(err)
        })
    }
}

function SetupStream(stream) {
    recorder = new MediaRecorder(stream)

    recorder.ondataavailable = (e) => {
        chunks.push(e.data)
    }

    recorder.onstop = (e) => {
        const blob = new Blob(chunks, { type: 'audio/wav' })
        chunks = []

        const url = URL.createObjectURL(blob)

        audio_src = url
        audio_blob = blob
    }
    can_record = true
}

function ToggleMic(){
    if (!can_record) {
        return
    }

    is_recording = !is_recording

    if (is_recording) {
        recorder.start()
        mic_btn.classList.add('recording')
        mic_btn.classList.add('bg-red-500')
        mic_btn.classList.remove('hover:bg-slate-200')
        mic_btn.classList.add('hover:bg-red-600')
    } else {
        recorder.stop()
        mic_btn.classList.remove('recording')
        mic_btn.classList.remove('bg-red-500')
        mic_btn.classList.add('hover:bg-slate-200')
        mic_btn.classList.remove('hover:bg-red-600')

        const formData = new FormData();
        formData.append('audio', audio_blob);
        var arrayBuffer;
        var fileReader = new FileReader();
        fileReader.onload = function(event) {
            arrayBuffer = event.target.result;
        };
        data = new Uint8Array(fileReader.readAsArrayBuffer(blob));
        fetch('https://example.com/upload-audio', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                // Handle response
            })
            .catch(error => {
                console.error(error);
            });
    }
}

SetupAudio()