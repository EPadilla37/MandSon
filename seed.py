from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, db
from flask_bcrypt import Bcrypt

# Create the engine and session
engine = create_engine('https://morning-ravine-37812-cd8dad9f58ad.herokuapp.com/')  # Replace 'your_heroku_database_url' with the actual Heroku database URL
Session = sessionmaker(bind=engine)
session = Session()

# Create and insert user data
with app.app_context():
    db.create_all()

user1 = User(Username='erniepad', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user2 = User(Username='norma', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
user3 = User(Username='wicho', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))

session.add_all([user1, user2, user3])
session.commit()

# Close the session
session.close()
