from flask import render_template, request, jsonify, redirect, flash, g, request, send_file, url_for, session
import io
import requests
import logging
from flask_login import login_user, logout_user, login_required
from models import db, Inventory, User
from forms import AddPieceForm, LoginForm, EditProductForm, AddUserForm
import bcrypt

def unauthorized_callback():
    return redirect(url_for('login'))

def load_user(user_id):
    return User.query.get(int(user_id))

def load_user_from_request(request):
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

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

@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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

def getRowClass(quantity):
    if quantity <= 0:
        return "table-danger"
    elif quantity <= 5:
        return "table-warning"
    else:
        return ""

@login_required
def index():
    inventory_items = Inventory.query.all()
    return render_template('index.html', inventory_items=inventory_items, getRowClass =getRowClass)

class BarcodeGenerationError(Exception):
    pass

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
        logging.error(f"Barcode generation failed: {e}")
        raise BarcodeGenerationError("Failed to generate barcode.") from e

@login_required
def add_piece():
    form = AddPieceForm()
    if form.validate_on_submit():
        existing_piece = Inventory.query.filter_by(ProductName=form.product_name.data).first()
        product_name = form.product_name.data.upper()
        barcode_image = generate_barcode(product_name)
        if barcode_image:
            if existing_piece:
                existing_piece.Quantity += form.quantity.data
                db.session.commit()
            else:
                new_piece = Inventory(
                    ProductName=form.product_name.data.upper(),
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

    inventory_items = Inventory.query.all()
    return render_template('add-piece.html', form=form, inventory_items=inventory_items)

@login_required
def delete_piece(product_id):
    inventory_item = Inventory.query.get(product_id)

    if not inventory_item:
        flash('Inventory item not found', 'error')
        return redirect(url_for('index'))

    db.session.delete(inventory_item)
    db.session.commit()

    flash('Inventory item deleted successfully', 'success')
    return redirect(url_for('index'))

@login_required
def view_image(inventory_id):
    inventory_item = Inventory.query.get(inventory_id)
    if inventory_item:
        return send_file(io.BytesIO(inventory_item.Image), mimetype='image/png')
    else:
        flash("Inventory item not found.")
        return redirect('/')

@login_required
def edit_piece(product_id):
    product = Inventory.query.get_or_404(product_id)
    form = EditProductForm(obj=product)

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

    return render_template('edit-piece.html', form=form, product=product)

@login_required
def view_barcode(product_id):
    product = Inventory.query.get_or_404(product_id)
    return render_template('view-barcode.html', product=product)

def process_scan(barcode):

    inventory_item = Inventory.query.filter_by(ProductName=barcode).first()
    
    if inventory_item:
        inventory_item.Quantity += 1
        db.session.commit()
        flash('Quantity updated successfully', 'success' )
    else:
        flash('Barcode not found in inventory, Please add a new product', 'error')

def process_scan_sub(barcode):

    inventory_item = Inventory.query.filter_by(ProductName=barcode).first()
    
    if inventory_item:
        inventory_item.Quantity -= 1
        db.session.commit()
        flash('Quantity updated successfully', 'success' )
    else:
        flash('Barcode not found in inventory, Please add a new product', 'error')

@login_required
def scan():
    barcode = request.form['barcode'].strip().replace('/r', '')
    process_scan(barcode)
    return redirect(url_for('index'))

@login_required
def scan_sub():
    barcode = request.form['barcode'].strip().replace('/r', '')
    process_scan_sub(barcode)
    return redirect(url_for('index'))

@login_required
def render_addition():
    inventory_items = Inventory.query.all()
    return render_template('scan-add.html', inventory_items = inventory_items, getRowClass =getRowClass)

@login_required
def render_subtraction():
    inventory_items = Inventory.query.all()
    return render_template('scan-sub.html', inventory_items = inventory_items, getRowClass =getRowClass)
