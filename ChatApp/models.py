from flask import abort # HTTPステータスコードをクライアント側へ表示させるライブラリ
import pymysql          # SQL操作のライブラリ
from util.DB import DB  # 作成したDBファイルをimport

# 初期起動時にコネクションプールを作成し接続を確立
# envファイルからユーザー名やDB等を取得や同時接続最大数の設定、DB空の戻り値を辞書型に設定などを定義している
db_pool = DB.init_db_pool()

# ユーザークラス
class User:

    # ログイン時に、emailからユーザー情報を検索し、ユーザー情報を辞書型で返している
    @classmethod
    def find_user(cls,email):
        # データベース接続プールからコネクションを取得する（DB.pyファイルのこと）
        conn = db_pool.get_conn()

        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email))
                user = cur.fetchone()   # 設定した辞書型で取得
            return user
        except pymysql.Error as e:
            print(f'エラーが発生してます：{e}') 
            abort(500)
        
        finally:
            db_pool.release(conn)

    # サインアップ処理
    @classmethod
    def create_user(cls,user_id,company_id,name,email,password):
        pass


    # 会社情報の取得と登録
    @classmethod
    def find_company(cls,company_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT company_id FROM companies WHERE name=%s;"
                cur.execute(sql,(company_name))
                company = cur.fetchone()
                #会社情報があれば返し、無ければ登録して返す
                if company is None:
                    sql = "INSERT INTO companies (company_name) VALUES (%s)"
                    cur.execute(sql, (company_name))
                    company = cur.fetchone()
                return company
            
        except pymysql.Error as e:
            print(f'エラーが発生してます：{e}') 
            abort(500)
        finally:
            db_pool.release(conn)