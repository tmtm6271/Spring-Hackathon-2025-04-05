# DB.pyが実行される時、初期化処理で、以下の設定が実行される
import os
import pymysql
from pymysqlpool.pool import Pool


class DB:
   @classmethod
    # envファイルから、DBに関する情報を取得している
   def init_db_pool(cls):
       pool = Pool(
           # データベースホスト
           host=os.getenv('DB_HOST'),
           # データベースユーザー
           user=os.getenv('DB_USER'),
           # データベースパスワード  
           password=os.getenv('DB_PASSWORD'),
           # データベース名
           database=os.getenv('DB_DATABASE'),
           # 同時に接続できる最大数を設定
           max_size=5,
           # 文字コード
           charset="utf8mb4",
           # カーソルクラスを辞書型に指定（デフォルトはタプル型）
           cursorclass=pymysql.cursors.DictCursor
       )
       # コネクションプールの初期化
       pool.init()
       return pool