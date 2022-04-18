from flask import Flask, jsonify, render_template, redirect, request, Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///self_dict.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# データベースの作成(登録したコンテンツ)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    pseudonym = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(600), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))



# トップページを表示
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        # データベースの全てのデータの取得
        posts = db.session.query(Post).order_by(Post.pseudonym).all()
        post = Post.query.get(1)
        div1 = Markup('<div class="meaning">')
        h1_1 = Markup('<h1>')
        h1_2 = Markup('</h1>')
        p1 = Markup('<p>')
        p2 = Markup('</p>')
        div2 = Markup('</div>')
        return render_template('index.html', posts=posts, post=post, div1=div1, div2=div2, h1_1=h1_1, h1_2=h1_2, p1=p1, p2=p2)



# 新規登録
@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        # get()の()内に書かれた、呼び出し元のnameの内容を取得
        title = request.form.get('title')
        meaning = request.form.get('meaning')
        pseudonym = request.form.get('pseudonym')
        
        # インスタンス化（コード上で追加）
        post = Post(title=title, meaning=meaning, pseudonym=pseudonym)
        
        # 実際のデータベースに追加
        db.session.add(post)
        db.session.commit()
        
        # トップに遷移
        return redirect('/')
    else:
        page_title = '新規作成'
        page = 'create'
        work = '登録'
        
        # インスタンス化（コード上で追加）
        post = Post(title='', meaning='', pseudonym='')
        return render_template('create_update.html', page_title=page_title, post=post, page=page, work=work)



# 編集・更新
@app.route('/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    # カラム（変数）idの値をもつレコードを取得
    post = Post.query.get(id)
    
    if request.method == 'POST':
        # POST送信された時（更新ボタンを押された時）
        post.title = request.form.get('title')
        post.meaning = request.form.get('meaning')
        
        db.session.commit()
        return redirect('/')
    else:
        # GET送信された時（編集ボタンを押された時）
        page_title = '編集'
        page =  str(id)+'/update'
        work = '更新'
        return render_template('create_update.html', post=post, page_title=page_title, page=page, work=work)



# 削除
@app.route('/<int:id>/delete', methods=['POST', 'GET'])
def delete(id):
    post = Post.query.get(id)
    
    # idで指定されたレコードを削除＆実行
    db.session.delete(post)
    db.session.commit()
    return redirect('/')



# 意味
@app.route('/<int:id>/meaning', methods=['POST'])
def meaning(id):
    posts = Post.query.all()
    post = Post.query.get(id)
    return render_template('index.html', posts=posts, post=post)



# 検索
@app.route('/result', methods=['POST'])
def search():
    search_item = request.form.get('search')
    posts = Post.query.all()
    post = []
    for value in posts:
        if search_item in value.title:
            post.append(value)
        else:
            continue
    if len(post) > 0:
        return render_template('result.html', posts=post, search=search_item)
    else:
        return render_template('notFound.html', search=search_item)