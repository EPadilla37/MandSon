from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Inventory
from forms import AddPieceForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:padilla@localhost/mandson_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

db.init_app(app)

with app.app_context():
    db.create_all()

# Route to render the index.html page
@app.route('/')
def index():
    inventory_items = Inventory.query.all()
    return render_template('index.html', inventory_items=inventory_items)

# @app.route('/process-scan', methods=["POST"])
# def process_scan():
#     data = request.get_json()
#     scanned_value = data.get('value')

#     return jsonify({'message': 'Scan successful!'})

@app.route('/add-piece', methods =['GET', 'POST'])
def add_piece_form():
    form = AddPieceForm()
    if form.validate_on_submit():
        new_piece = Inventory(
            ProductName = form.product_name.data,
            Quantity = form.quantity.data,
            Price = form.price.data
            )
        db.session.add(new_piece)
        db.session.commit()
        return redirect('/')
    
    inventory_items = Inventory.query.all()
    print(form.errors)
    return render_template('add-piece.html', form=form, inventory_items=inventory_items)

if __name__ == '__main__':
    app.run()

