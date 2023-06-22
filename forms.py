from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class AddPieceForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
