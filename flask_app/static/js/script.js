let mediaRecorder;
let mediaStream;
let audioChunks = [];
let isRecording = false;

// Rキーを押している間に録音を開始
document.addEventListener("keydown", async (event) => {
  if (event.key.toLowerCase() === "r" && !isRecording) { // Rキーが押されており、録音中でない場合
    console.log("Rキー押下 - 録音開始");
    isRecording = true;
    audioChunks = [];
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(mediaStream);

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    mediaRecorder.start();
    console.log("Recording started...");
  }
});

// Rキーを離したときに録音を停止
document.addEventListener("keyup", async (event) => {
  if (event.key.toLowerCase() === "r" && isRecording) { // Rキーが離されたとき
    console.log("Rキー解放 - 録音停止");
    isRecording = false;
    mediaRecorder.stop();
    console.log("Recording stopped...");

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const formData = new FormData();
      formData.append("file", audioBlob, "recorded_audio.wav");

      // サーバーに音声データを送信
      const response = await fetch('/upload-audio', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Server response:", data);
        document.getElementById("transcriptionDisplay").innerText = data.transcript;

        // サーバーから返ってきた音声データを再生
        const audioData = data.audio_data;
        const audioBlob = new Blob([Uint8Array.from(atob(audioData), c => c.charCodeAt(0))], { type: 'audio/mp3' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = audioUrl;
        audioPlayer.play();

        // Blob URLを解放
        audioPlayer.onended = () => URL.revokeObjectURL(audioUrl);
      } else {
        console.error("Error uploading file:", response.statusText);
      }

      // 録音が停止したらマイクアクセスを解放
      mediaStream.getTracks().forEach(track => track.stop());
    };
  }
});
