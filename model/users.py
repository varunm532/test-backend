from random import randrange
from datetime import date
import os, base64
import json
from sqlalchemy import func, case, select
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    # define the schema
    id = db.Column(db.Integer,primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.Integer, nullable=False)
    _price = db.Column(db.Integer, nullable=False)
    
    def _init_(uid,self,symbol,quantity,price):
        self._uid = uid
        self._symbol = symbol
        self._quantity = quantity
        self._price = price
    
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self,uid):
        self._uid = uid
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity
    @property
    def price(self):
        return self._price
    
    @price.setter
    def quantity(self,price):
        self._price = price
        
    def __str__(self):
        return json.dumps(self.read())
    
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    def update(self,uid="",symbol="",quantity="",price=""):
        """only updates values with length"""
        if len(uid) > 0:
            self.uid = uid
        if len(symbol) > 0:
            self.symbol = symbol
        if len(price) > 0:
            self.price = price
        if len(quantity) > 0:
            self.quantity = quantity          
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price": self.price
        }
    
    
class Stock_Transactions(db.Model):
    __tablename__ = 'stock_transactions'
   
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_type = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_amount = db.Column(db.Integer, nullable=False)
    # constructor of a User object, initializes the instance variables within object (self)

    def _init_(self,uid,symbol,transaction_type,quantity,transaction_amount):
        self._uid = uid
        self._symbol = symbol
        self._transaction_type = transaction_type
        self._quantity = quantity
        self._transaction_amount = transaction_amount
    
    # uid
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self,uid):
        self._uid = uid
        
    # symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
        
    # transaction type
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self,transaction_type):
        self._transaction_type = transaction_type
        
    #quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity
        
    #transaction amount
    @property
    def transaction_amount(self):
        return self._transaction_amount
    
    @transaction_amount.setter
    def transaction_amount(self,transaction_amount):
        self._transaction_amount = transaction_amount
        
        
     # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    
    # CRUD update: updates user name, password, phone
    # returns self

    def update(self,uid="",symbol="",transaction_type="",quantity="",transaction_amount=""):
        """only updates values with length"""
        if len(uid) > 0:
            self.uid = uid
        if len(symbol) > 0:
            self.symbol = symbol
        if len(transaction_type) > 0:
            self.transaction_type = transaction_type
        if len(quantity) > 0:
            self.quantity = quantity
        if len(transaction_amount) > 0:
            self.transaction_amount = transaction_amount           
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "symbol": self.symbol,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "transaction_amount": self.transaction_amount
        }

class Stocks(db.Model):
    _tablename_ = 'stocks'
    
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _company = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.Integer,unique=False,nullable=False)
    _sheesh = db.Column(db.Integer,unique=False,nullable=False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    def _init_(self,symbol,company,quantity,sheesh):
        self._symbol = symbol
        self._company = company
        self._quantity = quantity
        self._sheesh = sheesh
# symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
#company
    @property
    def company(self):
        return self._company
    
    @company.setter
    def company(self,company):
        self._company = company
#quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity

#cost
    @property
    def sheesh(self):
        return self._sheesh
    
    @sheesh.setter
    def sheesh(self,sheesh):
        self._sheesh = sheesh
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,symbol="",company="",quantity=None):
        """only updates values with length"""
        if len(symbol) > 0:
            self.symbol = symbol
        #if sheesh > 0:
           # self.sheesh = sheesh
        if len(company) > 0:
            self.company = company
        if quantity is not None and isinstance(quantity, int) and quantity > 0:
            self.quantity = quantity
        
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "company": self.company,
            "quantity": self.quantity,
            "sheesh": self.sheesh,
        }
    # Builds working data for testing
    def initUsers():
        with app.app_context():
            """Create database and tables"""
            db.create_all()

class House(db.Model):
    _tablename_ = 'houses'
    
    # define the house schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)

    _price = db.Column(db.Numeric, nullable=False)
    _beds = db.Column(db.Integer, nullable=False)
    _baths = db.Column(db.Integer, nullable=False)
    _address = db.Column(db.String(255), nullable=False)
    _lat = db.Column(db.String(255), nullable=False)
    _long = db.Column(db.String(255), nullable=False)
    _sqfeet = db.Column(db.Integer, nullable=False)
    _image = db.Column(db.String(255), nullable=False)
    
    
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self,price,beds,baths, address, lat, long, sqfeet, image="image"):
        self._price = price
        self._beds = beds
        self._baths = baths
        self._address = address
        self._lat = lat
        self._long = long
        self._sqfeet = sqfeet
        self._image = image
        #fill rest
# price
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self,price):
        self._price = price
#beds
    @property
    def beds(self):
        return self._beds
    
    @beds.setter
    def beds(self,beds):
        self._beds = beds
#baths
    @property
    def baths(self):
        return self._baths
    
    @baths.setter
    def baths(self,baths):
        self._baths = baths
#address

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self,address):
        self._address = address
#lat
    @property
    def lat(self):
        return self._lat
    
    @lat.setter
    def lat(self,lat):
        self._lat = lat
#long
    
    @property
    def long(self):
        return self._long
    
    @long.setter
    def long(self,long):
        self._long = long
#sqfeet
        
    @property
    def sqfeet(self):
        return self._sqfeet
    
    @sqfeet.setter
    def sqfeet(self,sqfeet):
        self._sqfeet = sqfeet

#image
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self,image):
        self._image = image

    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,price="",beds="", baths="", sqft="", address="", image=""):
        """only updates values with length"""
        if price != "":
            self.price = price
        if beds != "":
            self.beds = beds
        if baths != "":
            self.baths = baths
        if sqft != "":
            self.sqfeet = sqft
        if address != "":
            self.address = address
        if image != "":
            self.image = image
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
        "price": "$"+str(int(self.price)),
        "beds": self.beds,
        "baths": self.baths,
        "address": self.address,
        "lat": self.lat,
        "long": self.long,
        "sqfeet":self.sqfeet,
        "image":self.image
    }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    # Builds working data for testing
    def initUsers():
        with app.app_context():
            """Create database and tables"""
            db.create_all()


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _pnum = db.Column(db.String(255), unique=False, nullable=True)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _stockmoney = db.Column(db.Integer, unique=False, nullable=False)

    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, pnum, stockmoney, password="123qwerty", dob=date.today(), role="User"): #role="User"
        self._name = name
        self._uid = uid
        self._stockmoney = stockmoney
        self.set_password(password)
        self._dob = dob
        self._pnum = pnum
        self._role = role

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def stockmoney(self):
        return self._stockmoney
    
    # a setter function, allows name to be updated after initial object creation
    @stockmoney.setter
    def stockmoney(self, stockmoney):
        self._stockmoney = stockmoney
    
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role

    def is_admin(self):
        return self._role == "Admin"
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))

    @property
    def pnum(self):
        return self._pnum
    
    @pnum.setter
    def pnum(self, pnum):
        self._pnum = pnum
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            print(IntegrityError)
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "stockmoney": self.stockmoney,
            "dob": self.dob,
            "age": self.age,
            "pnum": self.pnum,
            "role": self.role, 
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", pnum="", stockmoney=None):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(pnum) > 0:
            self.pnum = pnum
        if stockmoney is not None and isinstance(stockmoney, int) and stockmoney > 0:
            self.stockmoney = stockmoney
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
def NewTransactractionlog(body,transactionamount,isbuy):
    # creates transaction log
    quantitytobuy = body.get('buyquantity')
    uid = body.get('uid')
    symbol = body.get('symbol')
    # checks if it is a log for buy
    if isbuy == True:
        transactiontype= 'buy'
        Inst_table = Stock_Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantitytobuy, transaction_amount=transactionamount)
        print(Inst_table)
        Inst_table.create()   
        db.session.commit()
        return print("transaction logged")
    # checks if it is a log for sell
    elif isbuy == False:
        transactiontype= 'sell'
        quantity = body.get('quantity')
        Inst_table = Stock_Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantity, transaction_amount=transactionamount)
        print(Inst_table)
        Inst_table.create()   
        db.session.commit()
        return print("transaction logged")
    else:
        return {'message': f'no buy boolean'}, 400
def currentprice(body, currentsymbol=None):
    # Gets current price of stock from db
    try:
        # Used for buy/sell classes
        symbol = body.get('symbol')
        if symbol:
            result = Stocks.query.filter(Stocks._symbol == symbol).value(Stocks._sheesh)
            if result is not None:
                return result
        else:
            raise ValueError("No symbol provided in body")
    except Exception as e:
        # used for portfolio class
        if not currentsymbol:
            return {'message': f"Invalid usage of function: {str(e)}"}, 400
        result = Stocks.query.filter(Stocks._symbol == currentsymbol).value(Stocks._sheesh)
        if result is not None:
            return result
        return {'message': f"Symbol {currentsymbol} not found"}, 404
def updatemoney(body,newbal):
    # updates account bal
        uid = body.get('uid')
        userid = User.query.filter(User._uid == uid).value(User.id)
        x = User.query.get(userid)
        print("this is second x" + str(x))
        x.stockmoney = newbal
        db.session.commit()
        return print("account balance updated")
def newquantity(body,isbuy):
    # updates stock quantity after purchase
    # logic for updating quantity incase of buy
    if isbuy == True:
        newquantity = body.get('newquantity')
        symbol = body.get('symbol')
        idnum = Stocks.query.filter(Stocks._symbol==symbol).value(Stocks.id)
        x= Stocks.query.get(idnum)
        print("this is x" + str(x))
        x.update(quantity = newquantity)
        return print("updated quanity")
    # logic for updating quantity incase of sell
    elif isbuy == False:
        symbol = body.get('symbol')
        quantity = body.get('quantity')
        totalquant = Stocks.query.filter(Stocks._symbol == symbol).value(Stocks._quantity)
        newquantity = totalquant + quantity
        idnum = Stocks.query.filter(Stocks._symbol==symbol).value(Stocks.id)
        x= Stocks.query.get(idnum)
        print("this is x" + str(x))
        x.update(quantity = newquantity)
        return print("updated quanity")
    else:
        return {'message': f'no buy boolean'},400
def usermoney(body):
    # Gets account balance
    uid = body.get('uid')
    return User.query.filter(User._uid == uid).value(User._stockmoney)
def numstockowned(body,for_portfolio = None,symbol = None):
    # calculates the amount of stocks owned
    uid = body.get('uid')
    # used for sell class
    if for_portfolio == None:
        symbol = body.get('symbol')
        
        result = db.session.query(
                    Stock_Transactions._symbol.label("SYMBOL"),
                    (func.sum(case([(Stock_Transactions._transaction_type == 'buy', Stock_Transactions._quantity)], else_=0)) -
                    func.sum(case([(Stock_Transactions._transaction_type == 'sell', Stock_Transactions._quantity)], else_=0))
                    ).label("TOTAL_QNTY"),
                    (func.sum(Stock_Transactions._quantity * Stocks._sheesh)).label("VALUE"),
                ).join(Stocks, Stocks._symbol == Stock_Transactions._symbol) \
        .filter(Stock_Transactions._uid == uid, Stock_Transactions._symbol == symbol) \
        .group_by(Stock_Transactions._symbol) \
        .all()
        #print(result[0][1])
        ownedstock = result[0][1]
        return ownedstock
    else:
        # used for portfolio class
        result = db.session.query(
                    Stock_Transactions._symbol.label("SYMBOL"),
                    (func.sum(case([(Stock_Transactions._transaction_type == 'buy', Stock_Transactions._quantity)], else_=0)) -
                    func.sum(case([(Stock_Transactions._transaction_type == 'sell', Stock_Transactions._quantity)], else_=0))
                    ).label("TOTAL_QNTY"),
                    (func.sum(Stock_Transactions._quantity * Stocks._sheesh)).label("VALUE"),
                ).join(Stocks, Stocks._symbol == Stock_Transactions._symbol) \
        .filter(Stock_Transactions._uid == uid, Stock_Transactions._symbol == symbol) \
        .group_by(Stock_Transactions._symbol) \
        .all()
        #print(result[0][1])
        ownedstock = result[0][1]
        return ownedstock
        
def display(body= None,for_portfolio = None,display= None):
    
    if for_portfolio == None and display == None:
        # Displays a transactions made by user
        uid = body.get('uid')
        data = Stock_Transactions.query.filter(Stock_Transactions._uid == uid)
        print("this is data" +str(data))
        json_ready = [data.read() for data in data]
        print("this is data" +str(json_ready))
        return json_ready
    elif for_portfolio == True:
        # used inpart display and calculate data about stocks owned in portfolio class
        uid = body.get('uid')
        list1 = Stock_Transactions.query.filter(Stock_Transactions._uid == uid).distinct(Stock_Transactions._symbol).all()
        symbols_list = list(set(row._symbol for row in list1))
        # Extracting _symbol values from the query result
        
        #print(str(listofstock))
        return symbols_list
    else:
        # used to display stocks
        return [stock.read() for stock in display]
def updatestockprice(body = None,isloop = None,latest_price = None,stock = None, topstock = None):
    #symbol = body.get('symbol')
    # updates stock price 
    if topstock == True:
        return Stocks.query.offset(0).limit(26).all()
    if isloop == False:
        return Stocks.query.all()
    elif isloop == True:
        stock.sheesh = latest_price
        price = stock.sheesh
        db.session.commit()
        return price
def querytables(body,type,table):
    if table == Stocks:
        
            #sym = body.get('symbol')
            return Stocks.query.filter_by(_symbol=type).all()
        
    else:
        if type == '_uid':
            uid = body.get('uid')
            return Stock_Transactions.query.filter_by(_uid=uid).all()
        else:
            return {'message': f'invalid type for table'},400
        
    
    


"""Database Creation and Testing """

def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11), pnum=123401293,stockmoney=10000, role="Admin")
        u2 = User(name='Nicholas Tesla', uid='niko', password='123niko', dob=date(1856, 7, 10), pnum=123404293,stockmoney=10000,)
        u3 = User(name='Alexander Graham Bell', uid='lex', pnum=123401293,stockmoney=10000,)
        u4 = User(name='Grace Hopper', uid='hop', password='123hop', dob=date(1906, 12, 9), pnum=123405293,stockmoney=10000,)
        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
            