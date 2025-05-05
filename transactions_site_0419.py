import os
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Key for Forms

app.config['SECRET_KEY'] = 'mysecretkey'

############################################

        # SQL DATABASE AND MODELS  

##########################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Transaction(db.Model):

    __tablename__ = 'transactions'
    id = db.Column(db.Integer,primary_key = True)
    amount = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    def __init__(self,id):
        self.id = id

    def __init__(self,date):
        self.date = date

    def __init__(self,category):
        self.category = category

    def __init__(self,description):
        self.description = description

    def __init__(self,amount):
        self.amount = amount

    def __repr__(self):
        return f"Id: {self.id}"

    def __repr__(self):
        return f"Date: {self.date}"

    def __repr__(self):
        return f"Category: {self.category}"
    
    def __repr__(self):
        return f"Description: {self.description}"
    
    def __repr__(self):
        return f"Amount: {self.amount}"
    
############################################

        # VIEWS WITH FORMS

##########################################

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_trans():
    form = AddForm()

    if form.validate_on_submit():
        category = form.category.data

        # Add new transaction to database
        new_trans = Transaction(category)
        db.session.add(new_trans)
        db.session.commit()

        return redirect(url_for('list_trans'))

    return render_template('add.html',form=form)

@app.route('/list')
def list_trans():
    # Grab a list of transactions from database.
    transactions = Transaction.query.all()
    return render_template('list.html')   
                           

@app.route('/delete', methods=['GET', 'POST'])
def del_trans():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        trans = Transaction.query.get(id)
        db.session.delete(trans)
        db.session.commit()

        return redirect(url_for('list_trans'))
    return render_template('delete.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
