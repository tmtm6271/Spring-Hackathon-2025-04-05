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
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)
# ここにzip関数をJinja2のグローバル変数として追加
app.jinja_env.globals.update(zip=zip)

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
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))  # ←セッションがない場合login_page関数からログイン画面に戻る
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



#------------------------------チャットルーム関連--------------------------------------
# ログイン or ルーム作成後の初回ページ
@app.route('/room/message', methods=['GET'])
def home_page():
    user_id = session.get('user_id')
    room_name = []
    room_id = []
    member_id = []
    user_name = []
    message_list = []
    message_id = []
    room_title = ''
    if user_id is None:
        return redirect(url_for('login_page'))
    else:
        my_list = Room.get_all(user_id)   # room_id,room_name,owner_id一覧情報を降順で取得
        if my_list:     # my_listが空じゃなければ
            messages = Message.get_all(my_list[0]['room_id'])
            print(my_list[0]['room_id'])
            # ルーム名、ルームid、メンバーidをそれぞれ取得
            for itm in my_list:  
                room_name .append(itm['room_name'])     # ルーム名一覧（List）
                room_id .append(itm['room_id'])         # ルームid一覧（List）
                member_id.append(itm['room_member_id']) # メンバーid一覧（List）                
            room_title = room_name[0]                   # 選択したルームのタイトル（String）

            # メッセージ情報取得
            if messages:
                for ms in messages:
                    user_name.append(ms['user_name'])                           # ユーザー名一覧（List）
                    message_list.append(ms['original_message'])                 # メッセージ一覧（List）
                    message_id.append(ms['message_id'])                         # メッセージid一覧（List）
            print(message_list)
        # フロント側で扱えるようレンダリング
        # ルーム名、ルームID、メンバーID、ルームのタイトル、ユーザー名、メッセージ、メッセージID、翻訳メッセージ
        return render_template('room.html', room_name=room_name, room_id=room_id, member_id=member_id, room_title=room_title, user_name=user_name,message_list=message_list,message_id=message_id)
    

# チャットルーム作成画面表示
@app.route('/room/create', methods=['GET'])
def room_create_page():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))  # ←セッションがない場合login_page関数からログイン画面に戻る
    
    return render_template('room_create.html')


# チャットルーム作成処理
@app.route('/room/create', methods=['POST'])
def room_create():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))  # ←セッションがない場合login_page関数からログイン画面に戻る

    new_room_name = request.form.get('room-name')
    user_email = request.form.get('user_email')

    print(f'新規ルーム名：{new_room_name}')
    if new_room_name == '':
        print('ルーム名を入力してください')
        flash('ルーム名を入力してください')
    else: 
        room_name = Room.find_by_name(new_room_name)
        if room_name != None:
            print(f'{room_name}は既に存在します')
            flash(f'{room_name}は既に存在します')
        else:
            Room.create(user_id,new_room_name)
            if user_email != '':
                #メンバー追加に渡すuser_idとroom_idを取得
                users = User.find_user(user_email)
                rooms = Room.find_by_name(new_room_name)
                # userが存在していれば登録
                if users is None:
                    print('ユーザーがいません')
                    flash('ユーザーがいません')
                    return redirect(url_for('room_create_page'))
                else:
                    Room.add_member(users['user_id'],rooms['room_id'])

            # 作成後は、作成したルームへ移動
            return redirect(url_for('home_page'))
    return redirect(url_for('room_create_page'))
    

# チャットルーム編集処理
@app.route('/room/update', methods=['GET'])
def room_update_page():
    return render_template('room_page')


# チャットルーム削除処理
@app.route('/room/delete', methods=['POST'])
def room_delete(room_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))

    Room.delete(room_id)
    rooms = Room.find_by_id(room_id)
    if rooms is None:
        print('削除しました')
        flash('削除しました')
    return redirect(url_for('home_page'))

# ルーム間の遷移(サンプルアプリのメッセージの詳細画面表示に該当)
# なくてよさそう
@app.route('/room/message', methods=['POST'])
def room_page():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page')) 
    room_id = Room.get_all(user_id)
    return redirect(url_for('home_page'))


#------------------------------メッセージ関連--------------------------------------
# メッセージ送信処理
@app.route('/room/message', methods=['POST'])
def message_create():
    print(f'-------開始------')
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))
    message = request.form.get('message')
    room_list = Room.get_all(user_id)
    room_id = room_list[0]['room_id']
    print(f'メッセージ：{message}')
    if message != '':
        Message.create(user_id, room_id, message)
    return redirect(url_for('home_page'))
    


# メッセージ編集処理
@app.route('/room/message/<message_id>/update', methods=['POST'])
def message_update(message_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))

    message = request.form.get('message')

    if message:
        Message.update(message_id, message)
    

# メッセージ削除処理
@app.route('/room/message/<message_id>', methods=['POST'])
def message_delete(message_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))

    Message.delete(message_id)
    


# メッセージ翻訳処理
@app.route('/room/message/translation', methods=['POST'])
def message_translation(message_id, translated_message):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_page'))

    Message.translate(message_id, translated_message)
    



# mainメソッド
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)