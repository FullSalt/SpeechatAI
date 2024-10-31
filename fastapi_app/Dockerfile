FROM python:3.11 AS base

# rootのパスワード設定
RUN echo 'root:rootpw' | chpasswd

RUN apt-get update && apt-get install -y \
    sudo \
    # 音声を扱うためのライブラリ
    pulseaudio ffmpeg alsa-utils libsdl2-dev \
    # Azure Speech SDKの依存ライブラリ
    build-essential ca-certificates libasound2-dev libssl-dev  libbz2-dev wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ユーザー作成
RUN useradd -m -s /bin/bash appuser && \
    echo 'appuser:appuserpw' | chpasswd && \
    usermod -aG sudo appuser

# アプリのディレクトリをコピー
COPY . /home/appuser/fastapi_app
# 作業ディレクトリ
WORKDIR /home/appuser/fastapi_app
# ユーザーの権限を変更
RUN chown appuser:appuser /home/appuser/fastapi_app

# ユーザー切り替え
USER appuser

ARG SPEECH_KEY
ARG SPEECH_REGION
ENV SPEECH_KEY=${SPEECH_KEY}
ENV SPEECH_REGION=${SPEECH_REGION}

# ライブラリのインストール
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /home/appuser/fastapi_app/requirements.txt

# # ファイルが存在しない場合にのみダウンロード
# RUN wget -nc https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
# # ファイルの解凍
# RUN unzip ./vosk-model-ja-0.22.zip

# ポートの公開
EXPOSE 8000

# 開発環境
FROM base AS development

# コンテナ起動時に実行されるコマンド
CMD ["python", "/home/appuser/fastapi_app/app.py"]

# 本番環境
FROM base AS production

# コンテナ起動時に実行されるコマンド
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]