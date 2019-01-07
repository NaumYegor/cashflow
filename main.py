from flask import Flask, request
import sqlite3
import functions

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def sign_up():

    user = dict()
    user["login"] = request.values["login"]
    user["email"] = request.values["email"]
    user["password"] = request.values["password"]
    user["status"] = 'inactive'

    conn = sqlite3.connect("debt.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE login=?', (user["login"], ))
    if cursor.fetchone() is not None:
        return "Try another login."

    cursor.execute('SELECT * FROM users WHERE email=?', (user["email"],))
    if cursor.fetchone() is not None:
        return "Try another email."

    if not functions.log_pass_valid(user["login"], user["password"]):
        return functions.invalid_data_msg()

    user = functions.dict_to_tuple(user)
    print(user)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user)
    conn.commit()
    conn.close()

    return "Ok."


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5303)
