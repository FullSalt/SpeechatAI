# SpeechatAI


ログイン
```bash
az login
```

レジストリの作成
```bash
az acr create --resource-group リソースグループ名 --name レジストリ名 --sku Basic
```

レジストリの一覧を表示する
```bash
az acr list --output table
```

レジストリにログイン
```bash
az acr login --name レジストリ名
```
Login Succeeded と表示されればログイン成功

イメージをビルド
```bash
./start_prod.sh
```

下記の2つのイメージが作成される
- speechatai-kikagaku-flask-app
- speechatai-kikagaku-fastapi-app

イメージをタグ付け
```bash
docker tag speechatai-kikagaku-flask-app:latest レジストリ名.azurecr.io/speechatai-kikagaku-flask-app:latest
```
```bash
docker tag speechatai-kikagaku-flask-app:latest レジストリ名.azurecr.io/speechatai-kikagaku-fastapi-app:latest
```

ACR にプッシュ
```bash
docker push レジストリ名.azurecr.io/speechatai-kikagaku-flask-app:latest
```

```bash
docker push レジストリ名.azurecr.io/speechatai-kikagaku-fastapi-app:latest
```

ACR にプッシュしたイメージを確認
```bash
az acr repository list --name レジストリ名 --output table
```

docer-compose.webapp.yml の下記の imeges のレジストリ名を変更する。
```yml
  flaskapp:
    image: レジストリ名.azurecr.io/speechatai-kikagaku-flask-app:latest
```

```yml
  fastapiapp:
    image: レジストリ名.azurecr.io/speechatai-kikagaku-fastapi-app:latest
```

Web App 上の compose ファイルの指定でdocer-compose.webapp.yml を指定する。
