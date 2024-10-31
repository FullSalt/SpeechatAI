from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from vosk import Model, KaldiRecognizer
import wave
import os
import uvicorn
import json
import base64
from gtts import gTTS
import azure.cognitiveservices.speech as speechsdk

# FastAPIアプリケーションの初期化
app = FastAPI()

# Vosk モデルの読み込み
# model = Model("/home/appuser/fastapi_app/vosk-model-ja-0.22")

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_recognition_language="ja-JP"

# WAVファイル保存ディレクトリ
SAVE_DIR = "uploads"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.get("/test/")
async def read_root():
    return {"message": "FastAPI server is running!"}

@app.post("/recognize-by-azurespeech/")
async def upload_audio(file: UploadFile = File(...)):
    file_location = f"./uploads/{file.filename}"
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)  # ファイルの内容を保存

    # VoskでWAVファイルを使って音声認識
    try:
            audio_config = speechsdk.audio.AudioConfig(filename=file_location)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            text_result = speech_recognizer.recognize_once_async().get().text
    except Exception as e:
        print(e)

    finally:
        # 一時ファイルを削除
        # os.remove(file_location)
        # if os.path.exists(wav_location):
        #     os.remove(wav_location)
        print("Transcript: ", text_result)

    tts = gTTS(text=text_result, lang="ja")
    output_audio_path = "synthesized_outut.mp3"
    tts.save(output_audio_path)

    # 合成された音声をBase64エンコードしてJSONレスポンスに含める
    with open(output_audio_path, "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

    # 音声認識結果とBase64エンコードされた音声ファイルを返す
    return JSONResponse(content={"transcript": text_result, "audio_data": encoded_audio})

# @app.post("/recognize-by-vosk/")
# async def upload_audio(file: UploadFile = File(...)):
#     file_location = f"./uploads/{file.filename}"
#     wav_location = f"./uploads/{file.filename}"
#     with open(file_location, "wb") as f:
#         content = await file.read()
#         f.write(content)  # ファイルの内容を保存

#     # VoskでWAVファイルを使って音声認識
#     try:
#         with wave.open(wav_location, "rb") as wf:
#             params = wf.getparams()
#             print("Audio Parameters:", params)
#             # WAVファイル形式が正しいか確認
#             if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#                 raise HTTPException(status_code=400, detail="Audio file must be WAV format mono PCM.")

#             rec = KaldiRecognizer(model, wf.getframerate())
#             text_result = ""
            
#             while True:
#                 data = wf.readframes(4000)
#                 if len(data) == 0:
#                     break
#                 if rec.AcceptWaveform(data):
#                     result = json.loads(rec.Result())
#                     text_result += result.get("text", "")

#             # 最終結果の取得
#             final_result = json.loads(rec.FinalResult())
#             text_result += final_result.get("text", "")

#     finally:
#         wf.close()
#         # 一時ファイルを削除
#         # os.remove(file_location)
#         # if os.path.exists(wav_location):
#         #     os.remove(wav_location)
#         print("Transcript: ", text_result)

#     tts = gTTS(text=text_result, lang="ja")
#     output_audio_path = "synthesized_outut.mp3"
#     tts.save(output_audio_path)

#     # 合成された音声をBase64エンコードしてJSONレスポンスに含める
#     with open(output_audio_path, "rb") as audio_file:
#         encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

#     # 音声認識結果とBase64エンコードされた音声ファイルを返す
#     return JSONResponse(content={"transcript": text_result, "audio_data": encoded_audio})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)