from flask import Flask, render_template, request, jsonify, redirect, flash, g, request, send_file
import io
from flask_sqlalchemy import SQLAlchemy
from models import db, Inventory
from forms import AddPieceForm, LoginForm, EditProductForm
from flask_migrate import Migrate
from base64 import b64decode
import base64
import requests
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/mandson_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'


db.init_app(app)

migrate = Migrate(app,db)

with app.app_context():
    db.create_all()

# Route to render the index.html page
@app.route('/')
def index():
    inventory_items = Inventory.query.all()
    return render_template('index.html', inventory_items=inventory_items)

############################################################################################
#Add/Edit inventory Routes 

def generate_barcode(product_name):
    url = 'https://barcodeapi.org/{}'
    params = {
        'text': product_name,
        'type': product_name,
        'scale': 1,
        'height': 100,
        'width': 2,
        'format': 'png'
    }

    try:
        response = requests.get(url.format(params['type']), params=params)
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



if __name__ == '__main__':
    app.run()

