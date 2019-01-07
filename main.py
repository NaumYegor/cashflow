from flask import Flask, request
import sqlite3
import functions
import config
import secrets

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def sign_up():

    user = {
        "login": request.values.get("login"),
        "email": request.values.get("email"),
        "password": request.values.get("password"),
        "status": "inactive"
        #"token": secrets.token_hex(16)
    }

    if not user["login"] or not user["email"] or not user["password"]:
        return "Not filled field."

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

    if not functions.send_email(user["email"]):
        return "Wrong email, bro."

    user = functions.dict_to_tuple(user)
    print(user)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user)
    conn.commit()
    conn.close()

    return "Check an email."


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=config.PORT)
