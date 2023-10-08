# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/productdb'  # Replace with your MySQL credentials
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), unique=True)
    stock_on_hand = db.Column(db.Integer)

# Create the database tables
db.create_all()

# Helper function to generate a random alphanumeric product name
def generate_product_name():
    while True:
        product_name = 'Item ' + ''.join(random.choices(string.digits, k=3))
        # Check if the generated name already exists
        if not Product.query.filter_by(product_name=product_name).first():
            return product_name


# Helper function to generate a random stock_on_hand value between 20 and 50
def generate_stock_on_hand():
    return random.randint(20, 50)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    products = Product.query.paginate(page=page, per_page=per_page)
    return render_template('index.html', products=products)

@app.route('/generate_products', methods=['POST'])
def generate_products():
    for _ in range(50):
        product_name = generate_product_name()
        stock_on_hand = generate_stock_on_hand()
        product = Product(product_name=product_name, stock_on_hand=stock_on_hand)
        db.session.add(product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sort_product_name_asc')
def sort_product_name_asc():
    products = Product.query.order_by(Product.product_name.asc()).all()
    return render_template('index.html', products=products)


@app.route('/sort_stock_desc')
def sort_stock_desc():
    products = Product.query.order_by(Product.stock_on_hand.desc()).paginate(page=1, per_page=20)
    return render_template('index.html', products=products)


@app.route('/reduce_stock_by_2')
def reduce_stock_by_2():
    Product.query.update({Product.stock_on_hand: Product.stock_on_hand - 2})
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/increase_stock_even')
def increase_stock_even():
    # Query even products based on their IDs
    even_products = Product.query.filter(Product.id % 2 == 0).all()
    
    # Check if even_products contains any products
    if even_products:
        for product in even_products:
            product.stock_on_hand += 2
        db.session.commit()
    else:
        print("No even products found.")
    
    return redirect(url_for('index'))

@app.route('/generate_and_add_products', methods=['POST'])
def generate_and_add_products():
    for _ in range(50):
        product_name = generate_product_name()
        stock_on_hand = generate_stock_on_hand()
        product = Product(product_name=product_name, stock_on_hand=stock_on_hand)
        db.session.add(product)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
