# ローカルにファイルを保存するFlaskアプリ（雛形）

from flask import Flask, request, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)
app.secret_key = "secret" # flash用

# 保存先フォルダを確保
# アプリ（Pythonファイル）と同じ階層にuploadフォルダが作成されます。
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# ブラウザで / （トップページ）にアクセスしたとき、この関数が動きます。
# GETリクエスト（ページを表示するとき）とPOSTリクエスト（ファイル送信時）の両方に対応。
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("ファイルが見つかりません")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("ファイルが選ばれてません")
            return redirect(request.url)
    
        filename = secure_filename(file.filename)

        if config.USE_S3:
            # S3保存処理（後ほど記述）
            pass
        else:
            save_path = os.path.join(config.UPLOAD_FOLDER, filename)
            file.save(save_path)
            flash(f"{filename}をローカルに保存しました")

        return redirect(url_for("upload_file"))

    return render_template("upload.html")

