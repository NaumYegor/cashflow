import string
import constant
import config
import smtplib

available_symbols = string.ascii_letters + string.digits


def dict_to_tuple(dictionary):
    tup = tuple()
    for key in dictionary:
        value = str(dictionary[str(key)])
        tup += (value,)
    return tup


def log_pass_valid(login, password):
    login_len = len(login)
    pass_len = len(password)
    if login_len < constant.MIN_LOGIN_LENGTH \
            or login_len > constant.MAX_LOGIN_LENGTH \
            or pass_len < constant.MIN_PASS_LENGTH \
            or pass_len > constant.MAX_PASS_LENGTH:
        return False

    for symbol in login:
        if symbol not in available_symbols:
            return False

    for symbol in password:
        if symbol not in available_symbols:
            return False

    return True


def invalid_data_msg():
    return ("Length of login has to be between " +
            str(constant.MIN_LOGIN_LENGTH) + " and " +
            str(constant.MAX_LOGIN_LENGTH) + "\n" +
            "Password length between " + str(constant.MIN_PASS_LENGTH) +
            " and " + str(constant.MAX_PASS_LENGTH) + "\n" +
            "Available symbols are: " + available_symbols
            )


def confirmation_link(token):
    return 'http://' + config.IP + ':' + str(config.PORT) + "/confirm?token=" + token


def send_email(recipient, token):
    try:
        smtp_obj = smtplib.SMTP(config.smtp_host, config.smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(config.email, config.password)
        confirm_message = config.CONFIRMATION_TEXT + confirmation_link(token)
        smtp_obj.sendmail(config.email, recipient, confirm_message)
        return True
    except smtplib.SMTPRecipientsRefused:
        return False
