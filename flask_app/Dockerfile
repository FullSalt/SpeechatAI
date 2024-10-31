FROM python:3.11 AS base

# rootのパスワード設定
RUN echo 'root:rootpw' | chpasswd

RUN apt-get update && apt-get install -y \
    sudo \
    pulseaudio ffmpeg socat alsa-utils libsdl2-dev portaudio19-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# MacOSの場合、
# RUN { echo "pcm.default pulse"; echo "ctl.default pulse"; }  | tee /.asoundrc

# ユーザー作成
RUN useradd -m -s /bin/bash appuser && \
    echo 'appuser:appuserpw' | chpasswd && \
    usermod -aG sudo appuser

# ユーザー切り替え
USER appuser

ARG PULSE_SERVER
ENV PULSE_SERVER=${PULSE_SERVER}

# アプリのディレクトリをコピー
COPY . /home/appuser/flask_app
# 作業ディレクトリ
WORKDIR /home/appuser/flask_app

# ライブラリのインストール
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /home/appuser/flask_app/requirements.txt

# ポートの公開
EXPOSE 5000

# 開発環境
FROM base AS development

# コンテナ起動時に実行されるコマンド
CMD ["python", "/home/appuser/flask_app/app.py"]

# 本番環境
FROM base AS production

# コンテナ起動時に実行されるコマンド
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]