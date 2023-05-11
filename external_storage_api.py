import sqlite3
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)


conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE data (id INT PRIMARY KEY, name TEXT, value INT)')
print("Table created successfully")

conn.close()


@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    cursor = conn.execute('SELECT id, name, value from data')
    data = []
    for row in cursor:
        data.append({'id': row[0], 'name': row[1], 'value': row[2]})

    conn.close()

    return {'data': data}


@app.route('/data', methods=['POST'])
def create_data():
    data = request.get_json()
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO data (id, name, value) VALUES ({data['id']}, '{data['name']}', {data['value']})")

    conn.commit()
    print("Records created successfully")
    conn.close()

    return {'message': 'Data created successfully'}


@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE data set name = '{data['name']}', value = {data['value']} where id = {id}")

    conn.commit()
    print("Records updated successfully")
    conn.close()

    return {'message': 'Data updated successfully'}


@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    cursor = conn.cursor()

    cursor.execute(f"DELETE from data where id = {id}")

    conn.commit()
    print("Records deleted successfully")
    conn.close()

    return {'message': 'Data deleted successfully'}
