import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Fact
from app import db_session


def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    return sessionmaker(bind=engine)()


def add_fact(session, category, fact):
    new_fact = Fact(category=category, fact=fact)
    session.add(new_fact)
    session.commit()


def add_facts_from_csv(session, input_csv_path):
    with open(input_csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            add_fact(session, row[0], row[1])


def get_facts_from_database():
    facts = db_session.query(Fact).all()  # Factモデルを使って全てのfactsを取得
    return facts


# すべてのファクトを削除
def delete_all_facts(session):
    try:
        session.query(Fact).delete()
        session.commit()
        print("すべてのファクトを削除しました。")
    except Exception as e:
        session.rollback()
        print("エラーが発生しました: ", e)
    finally:
        session.close()
