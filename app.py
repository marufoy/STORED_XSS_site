from flask import Flask, request, render_template_string, session, redirect

app = Flask(__name__)
# セッションを暗号化するための秘密鍵（適当でOK）
app.secret_key = 'ryo_secret_key'
app.config.update(SESSION_COOKIE_HTTPONLY=False) 

# メモリ上の掲示板
comments = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerable Login Board</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <main class="container">
        <section class="board-card">
            <h1>掲示板システム</h1>
            <p class="lead">入力内容はそのまま表示されます。挙動確認用のローカル環境として利用してください。</p>

            {% if 'user' in session %}
                <div class="user-row">
                    <p>ログイン中: <b>{{ session['user'] }}</b></p>
                    <a href="/logout" class="ghost-link">ログアウト</a>
                </div>
                <form method="POST" action="/post" class="comment-form">
                    <label for="comment">コメントを投稿</label>
                    <textarea id="comment" name="comment" placeholder="スクリプトを仕込む場所"></textarea>
                    <button type="submit">投稿する</button>
                </form>
            {% else %}
                <h2>ログインしてください</h2>
                <form method="POST" action="/login" class="auth-form">
                    <label for="username">ユーザー名</label>
                    <input id="username" type="text" name="username" placeholder="ユーザー名">
                    <button type="submit">ログイン</button>
                </form>
            {% endif %}
        </section>

        <section class="comments-card">
            <h2>投稿一覧</h2>
            <ul class="comment-list">
                {% if comments %}
                    {% for c in comments %}
                        <li>{{ c | safe }}</li>
                    {% endfor %}
                {% else %}
                    <li class="empty">まだ投稿はありません。</li>
                {% endif %}
            </ul>
        </section>
    </main>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, comments=comments)

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form.get('username', 'Guest')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/post', methods=['POST'])
def post():
    comment = request.form.get('comment', '')
    comments.append(comment)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)