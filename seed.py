from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import bcrypt

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/mandson_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xuekxciwtingpp:179f85749e57cd32788e9fd5d0b77f23d0aef3e9e29536524365808583e0916b@ec2-52-6-117-96.compute-1.amazonaws.com:5432/dbk7trv20p96j'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tables created successfully.")

    hashed_password = bcrypt.hashpw('mandson7'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #create the user
    user = User(
        Username = 'erniepad',
        Password = hashed_password
    )

    db.session.add(user)
    db.session.commit()

    print("Tables created and user added")
