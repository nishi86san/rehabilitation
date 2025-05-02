# ローカルにファイルを保存するFlaskアプリ（雛形）
# ローカルに保存したファイルを一覧表示させる
# image_gallery/
# ├── app.py
# ├── static/ flask は static配下に画像を入れる必要がある
# │   └── images/ 
# ├── templates/
# │   ├── upload.html
# │   └── gallery.html
#

from flask import Flask, request, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)
app.secret_key = "secret" # flash用

# 保存先フォルダを確保
# アプリ（Pythonファイル）と同じ階層にuploadフォルダが作成されます。
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

def alowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# アップロードページ
# GETリクエスト（ページを表示するとき）とPOSTリクエスト（ファイル送信時）の両方に対応。
@app.route("/upload", methods=["GET", "POST"])
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

        return redirect(url_for("gallery"))

    return render_template("upload.html")

# 画像一覧ページ
@app.route("/gallery")
def gallery():
    if config.USE_S3:
        # S3一覧取得処理（後ほど記述）
        image_urls = []
    else:
        files = os.listdir(config.UPLOAD_FOLDER)
        image_urls = [url_for('static', filename=f"images/{f}") for f in files if alowed_file(f)]
    return render_template("gallery.html", images=image_urls)

if __name__ == "__main__":
    app.run(debug=True)

