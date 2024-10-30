from flask import Flask, render_template, request, jsonify
import io
import os
from pydub import AudioSegment
import requests

app = Flask(__name__)

# HTMLページをレンダリング
@app.route('/')
def index():
    return render_template('index.html')

# WAVファイル保存ディレクトリ
SAVE_DIR = "saved_wavs"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    file = request.files['file']
    
    # ファイルをWAVに変換
    audio = AudioSegment.from_file(file)
    audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)
    wav_filename = os.path.join(SAVE_DIR, "converted_audio.wav")
    audio.export(wav_filename, format="wav")  # ファイルを保存
    
    # FastAPIサーバーに送信するためにメモリ上のデータとして準備
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    # FastAPIサーバーへ送信
    files = {"file": ("recorded_audio.wav", wav_io, "audio/wav")}
    response = requests.post("http://fastapi-app:8000/upload-audio/", files=files)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get transcription"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)