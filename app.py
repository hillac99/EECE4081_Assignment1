# Imports
from flask import Flask                 # general web development
from flask import render_template       # render html5 templates
from flask import request               #
from flask import redirect              #
from flask_sqlalchemy import SQLAlchemy # create sqlite databases using python3

# create the flask application object
app = Flask(__name__)

# create a database and link it to the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brokenlaptop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# create a table of broken laptops
class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    
#################################################################
# Create basic CRUD API                                         #
#                                                               #
# Create - will add new broken laptop to inventory              #
# Read - will list all the existing broken laptops in inventory #
# Update - will modify the attributes of a broken laptop        #
# Delete - will delete a single entry of a broken laptop        #
#################################################################

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        new_laptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(new_laptop)
        db.session.commit()
    
    # display inventory    
    inventory = BrokenLaptop.query.all()    
    return render_template("create.html", inventory = inventory)
    
@app.route('/')
def read():
    # Display all broken laptops in inventory
    inventory = BrokenLaptop.query.all()
    return render_template("read.html", inventory = inventory )
    
@app.route('/update/<laptop_id>', methods=['GET','POST'])
def update(laptop_id):
    laptop = BrokenLaptop.query.get(laptop_id)
    if request.form:
        laptop.brand = request.form.get("brand")
        laptop.price = request.form.get("price")
        db.session.commit()
         
    return render_template("update.html", brokenlaptop = laptop)

@app.route('/delete/<laptop_id>')
def delete(laptop_id):
    db.session.delete(BrokenLaptop.query.get(laptop_id))
    db.session.commit()
    return redirect("/")
    
if __name__ == '__main__':
    app.run(debug=True)
