from flask import Flask, render_template, request, jsonify, redirect, flash, g, request, send_file, url_for, session
import io
from flask_sqlalchemy import SQLAlchemy
from models import db, Inventory, User
from forms import AddPieceForm, LoginForm, EditProductForm, AddUserForm
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import bcrypt
from base64 import b64decode
import requests
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/mandson_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'


db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()


###################################################################################################
#User login/logout raoutes
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@app.route('/login', methods = ["GET", "POST"])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.Password.encode('utf-8')):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(Username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                Username=form.username.data,
                Password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('New user added successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('add-user.html', form=form)

###################################################################################################
# Route to render the index.html page
@app.route('/')
@login_required
def index():
    inventory_items = Inventory.query.all()
    return render_template('index.html', inventory_items=inventory_items)
#Add/Edit/Inventory Routes 

def generate_barcode(product_name):
    url = 'https://barcodeapi.org/{}'
    params = {
        'text': product_name,
        'type': 'code128',
        'scale': 1,
        'height': 100,
        'width': 2,
        'format': 'png'
    }

    try:
        response = requests.get(url.format(params['text']), params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.content
    except requests.exceptions.RequestException as e:
        # Handle the error condition
        print(f"Barcode generation failed: {e}")
        return None

@app.route('/add-piece', methods=['GET', 'POST'])
def add_piece_form():
    form = AddPieceForm()
    if form.validate_on_submit():
        existing_piece = Inventory.query.filter_by(ProductName=form.product_name.data).first()
        product_name = form.product_name.data
        barcode_image = generate_barcode(product_name)
        if barcode_image:
            if existing_piece:
                existing_piece.Quantity += form.quantity.data
                db.session.commit()
            else:
                new_piece = Inventory(
                    ProductName=form.product_name.data,
                    Quantity=form.quantity.data,
                    Price=form.price.data,
                    Image=barcode_image
                )
                db.session.add(new_piece)
                db.session.commit()
                return redirect('/')
        else:
            # Handle the error condition where barcode generation failed
            flash("Failed to generate barcode. Please try again.")
            return redirect('/add-piece')

        return redirect('/')

    inventory_items = Inventory.query.all()
    print(form.errors)
    return render_template('add-piece.html', form=form, inventory_items=inventory_items)

@app.route('/view-image/<int:inventory_id>')
def view_image(inventory_id):
    inventory_item = Inventory.query.get(inventory_id)
    if inventory_item:
        return send_file(io.BytesIO(inventory_item.Image), mimetype='image/png')
    else:
        flash("Inventory item not found.")
        return redirect('/')


@app.route('/edit/<int:product_id>', methods=["GET", "POST"])
def edit_piece(product_id):
    product = Inventory.query.get_or_404(product_id)
    form = EditProductForm(obj = product)

    if form.validate_on_submit():
        product.ProductName = form.product_name.data
        product.Quantity = form.quantity.data
        product.Price = form.price.data
        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect('/')
    elif request.method == "GET": 
        form.product_name.data = product.ProductName
        form.quantity.data = product.Quantity
        form.price.data = product.Price
    
    return render_template('edit-piece.html', form= form, product=product)

@app.route('/view-barcode/<int:product_id>')
def view_barcode(product_id):
    product = Inventory.query.get_or_404(product_id)
    return render_template('view-barcode.html', product=product)

###################################################################################################

if __name__ == '__main__':
    app.run()

