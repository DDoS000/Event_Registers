from users import schema as users_schema
from auth import schema as auth_schema
from utils.dbUtil import database

def update_user(request: users_schema.UserUpdate, current_user: auth_schema.UserResponse):
    query = 'UPDATE my_users SET fullname=:fullname WHERE email=:email'
    return database.execute(query, values={'fullname': request.fullname, 'email': current_user.email})


def deactivate_account(current_user: auth_schema.UserResponse):
    query = 'UPDATE my_users SET active=0 WHERE email=:email'
    return database.execute(query, values={'email': current_user.email})

def change_password(change_password_object: users_schema.ChangePassword, current_user: auth_schema.UserResponse):
    query = 'UPDATE my_users SET password=:password WHERE email=:email'
    return database.execute(query, values={'password': change_password_object.new_password, 'email': current_user.email})

def save_token_to_blacklist(tokem: str, current_user: auth_schema.UserResponse):
    query = 'INSERT INTO my_blacklists (token, email) VALUES (:token, :email)'
    return database.execute(query, values={'token': tokem, 'email': current_user.email})