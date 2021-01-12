from flask import Flask, render_template
from flask_cors import CORS

# Flaskの設定
app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
app.config.from_object('backend.config.BaseConfig')

from .models import db
db.drop_all()
db.create_all()

from .seeding import seed
seed()


# api.pyで記述したapiへのリクエストURLを登録
from .api import api
app.register_blueprint(api, url_prefix="/api")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# 全てのリクエストをVueに投げる。
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
