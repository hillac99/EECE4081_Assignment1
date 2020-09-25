# Imports
from flask import Flask                 
from flask import render_template       
from flask import request               
from flask import redirect              
import os 
from flask_sqlalchemy import SQLAlchemy

# Establish google cloud database
database = (
    #mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_connection_name>
    'mysql+pymysql://{name}:{password}@/{dbname}?unix_socket=/cloudsql/{connection}').format(
        name       = os.environ['DB_USER'], 
        password   = os.environ['DB_PASS'],
        dbname     = os.environ['DB_NAME'],
        connection = os.environ['DB_CONNECTION_NAME']
        )

# create the flask application object
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database
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

@app.route('/')
def init():    
    db.drop_all()
    db.create_all()
    return redirect('/read')

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
    return render_template("create.html", inventory = inventory, title = "Add Broken Laptop to Inventory")
    
@app.route('/read')
def read():
    # Display all broken laptops in inventory
    inventory = BrokenLaptop.query.all()
    return render_template("read.html", inventory = inventory, title = "Broken Laptop Inventory" )
    
@app.route('/update/<laptop_id>', methods=['GET','POST'])
def update(laptop_id):
    laptop = BrokenLaptop.query.get(laptop_id)
    if request.form:
        laptop.brand = request.form.get("brand")
        laptop.price = request.form.get("price")
        db.session.commit()
         
    return render_template("update.html", brokenlaptop = laptop, title = "Update Broken Laptop")


@app.route('/delete_request/<laptop_id>')
def delete_request(laptop_id):
    return render_template("delete_confirmation.html", title = "Are you sure you want to delete this laptop?", laptop_id = laptop_id)

@app.route('/delete/<laptop_id>')
def delete(laptop_id):
    laptop = BrokenLaptop.query.get(laptop_id)
    db.session.delete(laptop)
    db.session.commit()
    return redirect('/read')
    
if __name__ == '__main__':
    app.run(debug=True)
