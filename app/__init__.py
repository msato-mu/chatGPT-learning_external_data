from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Flaskをインポートし、アプリケーションのインスタンスを作成する
app = Flask(__name__)

# データベースの設定を行う
app.config['DATABASE_URL'] = 'sqlite:///my_database.db'

# SQLAlchemyを使用してデータベースに接続するためのエンジンと、セッションを作成する
engine = create_engine(app.config['DATABASE_URL'])
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


# アプリケーションコンテキストが終了した際に、データベースから切断するための処理を定義する
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def create_app():
    from . import routes
    return app
