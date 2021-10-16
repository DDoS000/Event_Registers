from pydantic.schema import schema
from utils.dbUtil import database
from auth import schema

def find_exist_user(email: str):
    query = "SELECT * FROM my_users WHERE status='1' AND email=:email"
    return database.fetch_one(query, values={"email": email})

def find_blacklist_token(token: str):
    query = "SELECT * FROM my_blacklists WHERE token=:token"
    return database.fetch_one(query, values={'token': token})

def create_user(user: schema.UserCreate):
    query = "INSERT INTO my_users values(nextval('user_id_seq'), :email, :password, :fullname, now() AT TIME ZONE 'UTC', '1')"
    return database.execute(query, values={'email': user.email, 'password': user.password, 'fullname': user.fullname})

def create_reset_code(email: str, reset_code: str):
    query = "insert into my_codes values(nextval('code_id_seq'), :email, :reset_code, '1', now() AT TIME ZONE 'UTC')"
    return database.execute(query, values={'email': email, 'reset_code': reset_code})

def check_reset_password_token(reset_password_token: str):
    query = "SELECT * FROM my_codes WHERE status='1' AND reset_code=:reset_password_token " \
    "AND exprired_in >= now() AT TIME ZONE 'UTC' - INTERVAL '10 minutes'"
    return database.fetch_one(query, values={'reset_password_token': reset_password_token})

def reset_password(new_hashed_password: str, email: str):
    query = "UPDATE my_users SET password=:password WHERE email=:email"
    return database.execute(query, values={'password': new_hashed_password, 'email': email})

def disable_reset_code(reset_password_token: str, email: str):
    query = "UPDATE my_codes SET status='0' WHERE status='1' AND reset_code=:reset_password_token AND email=:email"
    return database.execute(query, values={'reset_password_token': reset_password_token, 'email': email})
    
