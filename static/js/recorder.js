const mic_btn = document.getElementById('mic-btn')

var can_record = false;
var is_recording = false;

var recorder = null;

var chunks = [];

function SetupAudio() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then(SetupStream)
        .catch((err) => {
            console.error(err);
        })
    }
}

function SetupStream(stream) {
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => {
        chunks.push(e.data);
    }

    recorder.onstop = async () => {
        const blob = new Blob(chunks);
        chunks = [];
        var mode = document.getElementById('mode').value;
        src_lang = mode.split('-')[0];
        tgt_lang = mode.split('-')[1];
        socket.emit('audio', {
            room: room_id,
            audio: blob,
            src_lang: src_lang,
            tgt_lang: tgt_lang
        });
    }
    can_record = true;
}

mic_btn.addEventListener('click', ToggleMic)
function ToggleMic(){
    if (!can_record) {
        return;
    }

    is_recording = !is_recording;

    if (is_recording) {
        recorder.start();
        mic_btn.classList.add('recording');
        mic_btn.classList.add('bg-red-500');
        mic_btn.classList.remove('hover:bg-slate-200');
        mic_btn.classList.add('hover:bg-red-600');
    } else {
        recorder.stop()
        mic_btn.classList.remove('recording');
        mic_btn.classList.remove('bg-red-500');
        mic_btn.classList.add('hover:bg-slate-200');
        mic_btn.classList.remove('hover:bg-red-600');
    }
}

SetupAudio();