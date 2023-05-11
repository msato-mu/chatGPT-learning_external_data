from flask import request, jsonify
from . import app, db_session
from .database.models import Fact
from app.database.db_utils import get_session
from .gpt3.gpt3_utils import ask_gpt3
from flask import render_template
from app.database.db_utils import get_facts_from_database


# 「/api/facts」にGETリクエストがあった場合に、カテゴリーに基づいてFactを取得する関数を定義する
@app.route('/api/facts', methods=['GET'])
def get_facts():
    # リクエストからカテゴリーを取得し、該当するカテゴリーのFactをデータベースから取得する
    category = request.args.get('category')
    facts = db_session.query(Fact).filter(Fact.category == category).all()

    # 取得したFactをJSON形式で返す
    return jsonify([fact.fact for fact in facts])


@app.route("/api/ask", methods=["GET"])
def api_ask():
    question = request.args.get('Q', None)

    if question is None:
        return jsonify({"error": "Missing 'Q' parameter."}), 400

    # 1. データベースからfactを取得する
    facts = get_facts_from_database()

    # 2. GPT-3 に質問を投げる
    facts_str = "\n".join(f"- {fact}" for fact in facts)
    prompt = f"以下の情報に基づいて質問に答えてください:\n{facts_str}\n\n質問: {question}"
    response = ask_gpt3(prompt)

    return jsonify({"response": response})


# 質問を入力として受け取り、GPT-3を使ってカテゴリを特定し、データベースからそのカテゴリに関する事実を取得して返すAPIエンドポイント
@app.route('/api/ask2', methods=['GET'])
def ask():
    category = request.args.get('question')
    # category = ask_gpt3(question)
    facts = db_session.query(Fact).filter(Fact.category == category).all()
    return jsonify([fact.fact for fact in facts])


@app.route('/')
def index():
    # ここで必要に応じてデータを取得し、テンプレートに渡すことができます
    # 例えば、データベースから facts を取得する場合：
    # facts = get_facts_from_database()

    # データがない場合は、空のリストを使用する
    facts = get_facts_from_database()

    return render_template('index.html', facts=facts)
