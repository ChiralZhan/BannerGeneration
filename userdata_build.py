from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login_time = Column(DateTime)
    role = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}', last_login_time='{self.last_login_time}')>"

# Replace 'postgresql://postgres:password@localhost/mydatabase' with your actual database URL
# If you're not using a password, it might look like 'postgresql://postgres@localhost/mydatabase'

engine = create_engine('postgresql://postgres@localhost/mydatabase', echo=True)

Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example to add a new user
new_user = User(
    username='johndoe',
    password='securepassword123',  # In real applications, passwords should be hashed
    last_login_time=datetime.now(),
    role='admin'
)

session.add(new_user)
session.commit()

# Close the session
session.close()
