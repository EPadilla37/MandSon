from flask import Flask, render_template, request, jsonify, redirect, flash, g, request, send_file, url_for, session
from functions import getRowClass, unauthorized_callback,render_addition, render_subtraction, load_user, load_user_from_request, generate_barcode, add_piece, delete_piece, scan, process_scan, scan_sub, process_scan_sub,view_image, edit_piece, view_barcode, login, logout, add_user, index
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import AddPieceForm, LoginForm, EditProductForm, AddUserForm
from flask_sqlalchemy import SQLAlchemy
from models import db, Inventory, User
from flask_migrate import Migrate
from base64 import b64decode
import requests
import bcrypt
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/mandson_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# User login/logout routes
login_manager.unauthorized_handler(unauthorized_callback)
login_manager.user_loader(load_user)
login_manager.request_loader(load_user_from_request)

# Routes
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/logout')(logout)
app.route('/add-user', methods=['GET', 'POST'])(add_user)

app.route('/')(index)

app.route('/add-piece', methods=['GET', 'POST'])(add_piece)
app.route('/delete/<int:product_id>', methods=["POST"])(delete_piece)

app.route('/view-image/<int:inventory_id>')(view_image)
app.route('/edit/<int:product_id>', methods=['GET', 'POST'])(edit_piece)
app.route('/view-barcode/<int:product_id>')(view_barcode)

app.route('/render_add')(render_addition)
app.route('/render_sub')(render_subtraction)
app.route('/scan', methods=['POST'])(scan)
app.route('/scan_sub', methods=['POST'])(scan_sub)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run()
