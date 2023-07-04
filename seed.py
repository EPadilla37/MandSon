from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, db
from flask_bcrypt import Bcrypt
import os

# Create the engine and session
engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

# Create and insert user data
bcrypt = Bcrypt()

user1 = User(Username='erniepad', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user2 = User(Username='norma', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user3 = User(Username='wicho', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))

session.add_all([user1, user2, user3])
session.commit()

# Close the session
session.close()
