from flask import Flask, request
import sqlite3
import functions
import smtplib
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

    smtp_obj = smtplib.SMTP(config.smtp_host, config.smtp_port)
    smtp_obj.starttls()
    smtp_obj.login(config.email, config.password)
    confirm_message = config.CONFIRMATION_TEXT + functions.confirmation_link()
    smtp_obj.sendmail(config.email, user["email"], confirm_message)

    user = functions.dict_to_tuple(user)
    print(user)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", user)
    conn.commit()
    conn.close()

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=config.PORT)
