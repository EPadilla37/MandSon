from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import BYTEA

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.Password, password)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Numeric, nullable=False)
    AddedBy = db.Column(db.Integer, db.ForeignKey('users.UserID'), default = None)
    RemovedBy = db.Column(db.Integer, db.ForeignKey('users.UserID'), default = None)
    Image = db.Column(db.LargeBinary, nullable=True)


class DamagedPieces(db.Model):
    __tablename__ = 'damaged'

    DamagedID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('inventory.ProductID'))
    Description = db.Column(db.Text, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)


class AddedPieces(db.Model):
    __tablename__ = 'added'

    AddedID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('inventory.ProductID'))
    Description = db.Column(db.Text, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)