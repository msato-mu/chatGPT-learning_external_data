from app.database.db_utils import init_db, get_session, add_fact, add_facts_from_csv, delete_all_facts

database_url = 'sqlite:///my_database.db'
input_csv_path = 'data/facts_err_code.csv'

engine = init_db(database_url)
session = get_session(engine)

add_facts_from_csv(session, input_csv_path)
