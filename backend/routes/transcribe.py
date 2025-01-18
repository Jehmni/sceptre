from flask import Blueprint, request, jsonify
import speech_recognition as sr
from services.openai_service import get_bible_verses
from pydub import AudioSegment
import logging
import io

transcribe_bp = Blueprint('transcribe', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@transcribe_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        logging.error("No audio file provided")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    logging.debug(f"Received audio file: {audio_file.filename}, Content-Type: {audio_file.content_type}")
    recognizer = sr.Recognizer()

    try:
        # Convert webm to WAV
        if audio_file.content_type == 'audio/webm':
            audio_data = AudioSegment.from_file(io.BytesIO(audio_file.read()), format='webm')
            wav_io = io.BytesIO()
            audio_data.export(wav_io, format='wav')
            wav_io.seek(0)
            audio_file = wav_io

        # Process the audio file with speech_recognition
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        verses = get_bible_verses(text)
        return jsonify({"text": text, "verses": verses})
    except sr.UnknownValueError:
        logging.error("Could not understand audio")
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        logging.error(f"Could not request results; {e}")
        return jsonify({"error": f"Could not request results; {e}"}), 500
    except Exception as e:
        logging.error(f"An error occurred; {e}")
        return jsonify({"error": f"An error occurred; {e}"}), 500