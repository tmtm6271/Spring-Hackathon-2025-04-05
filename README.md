# Spring-Hackathon-2025-04-05

**起動方法**
```
docker compose up
```

**ブラウザで確認**
```
http://localhost:55000
```

**ディレクトリ構成図**

Desktop/
└── work_space/ 　　#←親ディレクトリ（ここでgit initと git clone初回のみ）
    ├── .git
    └── Spring-Hackathon-2025-04-05/　# 作業ディレクトリ（修正作業やpushを行う）
        ├── __init__.py
        ├── app.py
        ├── models.py
        ├── static /                  # 画像などの静的ファイル用ディレクトリ
        ├── templates /               # Template(HTML)用ディレクトリ
        │   ├──auth /                 # ログイン関係
        │   ├──error /                # エラー関係
        │   ├──model /                # チャットルーム関係
        │   └──util /                 # ヘッダーやサイドバー
        ├── util/                     
        ├── Docker/
        │   ├── Flask/
        │   │   └── Dockerfile           # Flask(Python)用Dockerファイル
        │   └── MySQL /
        │       ├── Dockerfile           # MySQL用Dockerファイル
        │       ├── init.sql             # MySQL初期設定ファイル
        │       └── my.cnf
        ├── .env
        ├── docker-compose.yml         # Spring-Hackathon用Docker-composeファイル
        └── requirements.txt           # Spring-Hackathon用requirements.txt
