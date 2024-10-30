FROM python:3.11

# rootのパスワード設定
RUN echo 'root:rootpw' | chpasswd

RUN apt-get update && apt-get install -y \
    sudo \
    pulseaudio ffmpeg socat alsa-utils libsdl2-dev portaudio19-dev \
    && apt-get clean
# MacOSの場合、
# RUN { echo "pcm.default pulse"; echo "ctl.default pulse"; }  | tee /.asoundrc

# ユーザー作成
RUN useradd -m -s /bin/bash appuser && \
    echo 'appuser:appuserpw' | chpasswd && \
    usermod -aG sudo appuser

# ユーザー切り替え
USER appuser

# アプリのディレクトリをコピー
COPY . /home/appuser/flask_app
# 作業ディレクトリ
WORKDIR /home/appuser/flask_app

# ライブラリのインストール
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /home/appuser/flask_app/requirements.txt

# ポートの公開
EXPOSE 5000

# コンテナ起動時に実行されるコマンド
CMD ["python", "/home/appuser/flask_app/app.py"]