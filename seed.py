from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, db
from flask_bcrypt import Bcrypt
from app import app

# Create the engine and session
engine = create_engine('postgres://gbroswfsxwhhlt:dafd05639763001ae2c29545b676bdb2d12499c8ac3b75339f30f646ff872139@ec2-54-208-11-146.compute-1.amazonaws.com:5432/deggralu1tkvvv')
Session = sessionmaker(bind=engine)
session = Session()

# Create and insert user data
bcrypt = Bcrypt()

with app.app_context():
    db.create_all()

user1 = User(Username='erniepad', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user2 = User(Username='norma', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user3 = User(Username='wicho', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))

session.add_all([user1, user2, user3])
session.commit()

# Close the session
session.close()
