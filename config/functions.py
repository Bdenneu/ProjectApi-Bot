from werkzeug.security import generate_password_hash,check_password_hash

def func_check_password(password,name):
    return check_password_hash(aTry[1].password,password)

def func_need_password(author):
    return author.password != ""
