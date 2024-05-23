import argparse
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

# 设置数据库连接
DATABASE_URL = 'postgresql:///mydatabase'
DATABASE_URL = 'postgresql://postgres@localhost/mydatabase'
# 创建数据库引擎
engine = create_engine(DATABASE_URL)

def add_user_to_db(username, password, role,department):
    hashed_password = generate_password_hash(password)
    with engine.connect() as conn:
        insert_statement = text("""
            INSERT INTO users (username, password, role, department) VALUES (:username, :password, :role, department)
        """)
        conn.execute(insert_statement, username=username, password=hashed_password, role=role, department=department)
        print(f"User {username} added successfully with role {role}.")
def add_user_to_db(username, password, role,department):
    hashed_password = generate_password_hash(password)
    with engine.connect() as conn:
        transaction = conn.begin()  # 开始一个新的事务
        try:
            insert_statement = text("""
                INSERT INTO users (username, password, role, department) VALUES (:username, :password, :role, :department)
            """)
            params = {'username': username, 'password': hashed_password, 'role': role, 'department':department}
            conn.execute(insert_statement, params)
            transaction.commit()  # 提交事务
            print(f"{department} User {username} added successfully with role {role}.")
        except:
            transaction.rollback()  # 如果出错则回滚
            raise
if __name__== '__main__':
    parser = argparse.ArgumentParser(description='Add a new user to the database.')
    parser.add_argument('-user', required=True, help='Username of the new user')
    parser.add_argument('-password', required=True, help='Password for the new user')
    parser.add_argument('-role', required=True, help='Role of the new user')
    parser.add_argument('-department', required=True, help='Department of the new user')
    args = parser.parse_args()

    add_user_to_db(args.user, args.password, args.role,args.department)
