from flask import Flask, request, render_template
import sqlite3
import functions
import config
import secrets
import bcrypt

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def sign_up():

    user = {
        "login": request.values.get("login"),
        "email": request.values.get("email"),
        "password": request.values.get("password"),
        "token": secrets.token_hex(16),
        "status": "inactive",
        "balance": 0
    }

    if not user["login"] or not user["email"] or not user["password"]:
        return "Not filled fields."

    conn = sqlite3.connect("debt.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE login=?', (user["login"], ))
    if cursor.fetchone() is not None:
        return "Try another login."

    cursor.execute('SELECT * FROM users WHERE email=?', (user["email"], ))
    if cursor.fetchone() is not None:
        return "Try another email."

    if not functions.log_pass_valid(user["login"], user["password"]):
        return functions.invalid_data_msg()

    try:
        if not functions.send_email(user["email"], user["token"]):
            return "Wrong email, bro."
    except UnicodeEncodeError:
        return "UnicodeEncodeError"

    user["password"] = bcrypt.hashpw(user["password"].encode('utf-8'),
                                     bcrypt.gensalt())
    user = functions.dict_to_tuple(user)
    print(user)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", user)
    conn.commit()
    conn.close()

    return "Check an email."


@app.route('/confirm', methods=['GET'])
def confirm():
    token = request.values.get('token')

    if not token:
        return "Bad request."

    conn = sqlite3.connect('debt.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE token = ?", (token, ))
    user = cursor.fetchone()

    if user is None:
        return "Wrong token."

    if user[4] == "active":
        return "Activated already."

    cursor.execute("UPDATE users SET status = 'active' WHERE token = ?",
                   (token, ))
    cursor.execute("INSERT INTO spending VALUES (0, 0, 'Initial.', ?, ?)",
                   (user[0], functions.current_date(), ))

    conn.commit()
    conn.close()

    return "Activated."


@app.route('/signin', methods=['POST'])
def sign_in():

    user = {
        "login": request.values.get("login"),
        "password": request.values.get("password")
    }

    if not user["login"] or not user["password"]:
        return "Not filled fields."

    conn = sqlite3.connect("debt.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE login = ?', (user["login"], ))
    user_data = cursor.fetchone()

    if user_data is None:
        return "This login does not exist."

    if user_data[4] == "inactive":
        return "Activate your account."

    expected_password = user_data[2]
    if not bcrypt.checkpw(user["password"].encode('utf-8'), expected_password):
        return "Wrong password."

    new_token = secrets.token_hex(16)
    cursor.execute("UPDATE users SET token = ? WHERE login = ?",
                   (new_token, user_data[0], ))
    conn.commit()
    conn.close()

    return new_token


@app.route('/transaction', methods=['POST'])
def activity():

    token = request.values.get("token")
    if token is None:
        return "Bad request."

    conn = sqlite3.connect("debt.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE token = ?', (token, ))
    user = cursor.fetchone()
    if user is None:
        return "Wrong token."

    if user[4] == "inactive":
        return "Activate your account."

    try:
        transaction = float(request.values.get("transaction"))
    except ValueError:
        return "Value Error. Transaction field should contain Float value."

    new_balance = float(user[5]) + transaction
    cursor.execute('UPDATE users SET balance = ? WHERE token = ?',
                   (new_balance, token, ))

    transaction = {
        "balance": new_balance,
        "transaction": transaction,
        "title": request.values.get("title"),
        "username": user[0],
        "date": functions.current_date()
    }

    transaction = functions.dict_to_tuple(transaction)
    print(transaction)
    cursor.execute("INSERT INTO spending VALUES (?, ?, ?, ?, ?)", transaction)

    conn.commit()
    conn.close()
    return "Transactions added."


@app.route('/list', methods=['GET'])
def get_transactions():

    token = request.values.get("token")

    if token is None:
        return "token is None..."

    conn = sqlite3.connect("debt.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE token = ?', (token, ))
    user = cursor.fetchone()

    if user is None:
        return "user is None..."

    user_login = user[0]
    cursor.execute('SELECT * FROM spending WHERE username = ?', (user_login, ))
    transactions = cursor.fetchall()

    return render_template("list.html", transactions=transactions[::-1])


@app.route('/register', methods=['GET'])
def sign_up_template():
    return render_template("sign_up.html")


@app.route('/login', methods=['GET'])
def sign_in_template():
    return render_template("sign_in.html")


@app.route('/add', methods=['GET'])
def add_page():
    return render_template("adding.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=config.PORT)
