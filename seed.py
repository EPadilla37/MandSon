from models import User, db, connect_db
from flask_bcrypt import Bcrypt
import os

# Call connect_db function to initialize the database connection
connect_db(app)

# Create and insert user data
bcrypt = Bcrypt()

with app.app_context():
    user1 = User(Username='erniepad', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
    user2 = User(Username='norma', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))
    user3 = User(Username='wicho', Password=bcrypt.generate_password_hash('mandson7').decode('utf-8'))

    db.session.add_all([user1, user2, user3])
    db.session.commit()

