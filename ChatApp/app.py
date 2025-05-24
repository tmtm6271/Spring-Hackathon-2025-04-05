from flask import Flask, redirect, render_template, session, flash, abort, url_for, request
from datetime import timedelta
import hashlib
import uuid
import re
import os

# DB操作（models）のファイルから、Userメソッドなどを取得
# importで、DB情報を取ってくる
from models import User, Room, Message, File

# FlaskやDjangoでは、デフォルトでtemplatesを認識するので、パス指定はtemplates以降を記載で問題ない
# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key= os.getenv('SECRET_KEY', uuid.uuid4().hex) # .envファイルからシークレットキーを取得

# 起動時にセッションがあれば、channel.htmlへ遷移し、なければlogin.htmlへ遷移する
# 初回起動時のリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))  # ←セッションがない場合login_page関数からログイン画面に戻る
    return redirect(url_for('room_page'))


# ログイン画面表示
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    # Formから入力内容の取得
    email = request.form.get('email')
    password = request.form.get('pass')
    if email == '' or password == '':
        flash('未入力の項目があります')
    else:
        user = User.find_user(email) # find_userメソッドへ、emailを引数で渡し、SELECT文でユーザー情報を辞書型で全て取得
        if user is None:
            flash('ユーザーが存在しません')
        else:
            # ログイン画面で入力したpasswordをutf-8でバイト形式に変換
            # hashlibで、バイト形式に変化かんされた入力データをハッシュ値に変換（sha256は256ビットのハッシュ値を生成する関数）
            # hexdigestはハッシュ関数で生成されたハッシュ値を16進数に変換
            # ユーザーが入力した内容をバイト形式に変換→ハッシュ値に変換→16進数に変換して変数に格納している
            user_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            if user_password != user["pass"]:   # DBのカラム名をキーに値を取得
                flash('パスワードが間違っています')
            else:
                session['user_id'] = user['user_id']
                return redirect(url_for('home_page'))

    return redirect(url_for('login_page'))


# ログアウト処理
@app.route('/login', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


# サインアップ画面表示
@app.route('/signup',methods=['GET'])
def signup_page():
    return render_template('auth/signup.html')


# サインアップ処理
@app.route('/signup',methods=['POST'])
def signup_process():
    # htmlのname=の値を取得
    name = request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('pass')
    company_name= request.form.get('company-name')

    # 会社情報の取得
    # 会社名からcompany_idを取得、ない場合0
    company_id= User.find_company(company_name) # company_idをキー値で値の取得
    
    # flash(***)：Flaskの機能の一つで、ユーザーへ一時的にメッセージを表示する
    if name == '' or email == '' or password == '' or company_name == '':
        flash('未入力の項目があります')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('入力したメールアドレスの形式が正しくありません')
    else:
        user_id = uuid.uuid4() #uuidを使い、user_idの生成
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_user(email)

        # 作成されたアカウントが存在するか確認
        if registered_user != None:
            flash('既に登録されたメールアドレスです')
        else:
            User.create_user(user_id,company_id,name,email,password)
            return redirect(url_for('home_page'))
    return redirect(url_for('signup_page'))


'''# ログイン後の初回ページ
@app.route('/room/message', methods=['GET'])
def home_page():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))
    else:
        my_rooms = Room.get_all(user_id)
        messages = Message.get_all()
        # room情報と
        return render_template('room.html', my_rooms, messages)
'''

#★ログイン後の初回ページ
@app.route('/room/message', methods=['GET'])
def home_page():
    return render_template('room.html')



# チャットルーム作成処理
@app.route('/room/create', methods=['POST'])
def room_create():
    return render_template('room_create.html')


# チャットルーム編集処理
@app.route('/room/update/<cid>', methods=['POST'])
def room_update():
    pass


# チャットルーム削除処理
@app.route('/room/delete/<cid>', methods=['POST'])
def room_delete():
    pass


# ルーム間の遷移
@app.route('/room/<cid>/message', methods=['GET'])
def room_page():
    return render_template('message.html')


# メッセージ送信処理
@app.route('/room/<cid>/message', methods=['POST'])
def message_create():
    pass


# メッセージ編集処理
@app.route('/room/<cid>/message/<message_id>', methods=['POST'])
def message_update():
    pass


# メッセージ削除処理
@app.route('/room/<cid>/message/<message_id>', methods=['POST'])
def message_delete():
    pass


# メッセージ翻訳処理
@app.route('/room/<cid>/message/<message_id>', methods=['POST'])
def message_translation():
    pass


# mainメソッド
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)




