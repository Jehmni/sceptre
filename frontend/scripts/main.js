const microphoneIcon = document.getElementById('microphone-icon');
const micIcon = document.getElementById('mic-icon');
const transcriptDisplay = document.getElementById('transcript-display');
const versesDisplay = document.getElementById('verses-display');

let isRecording = false;
let mediaRecorder;
let audioChunks = [];

microphoneIcon.addEventListener('click', async () => {
    if (isRecording) {
        mediaRecorder.stop();
        microphoneIcon.classList.remove('recording');
    } else {
        await startRecording();
        microphoneIcon.classList.add('recording');
    }
    isRecording = !isRecording;
});

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

    mediaRecorder.ondataavailable = async event => {
        audioChunks.push(event.data);
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        audioChunks = [];
        const formData = new FormData();
        formData.append('audio', audioBlob);

        transcriptDisplay.textContent = 'Transcribing...';
        versesDisplay.innerHTML = '';

        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            transcriptDisplay.textContent = result.text;
            versesDisplay.innerHTML = result.verses.map(verse => `<li>${verse}</li>`).join('');
        } catch (error) {
            transcriptDisplay.textContent = 'An error occurred during transcription.';
        }
    };

    mediaRecorder.start(1000); // Send audio data every second
}