from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, date
import os

#initialise app
app = Flask(__name__)
 

basedir = os.path.abspath(os.path.dirname(__file__))

# database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#db init
db = SQLAlchemy(app)
# marshmallow init
ma = Marshmallow(app)

# wishlist model
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    wish = db.Column(db.String(200))
    wish_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    

    def __init__(self,name,wish,wish_date):
        self.name =  name
        self.wish = wish 
        self.wish_date = wish_date 
  
        

## wish schema
class WishlistSchema(ma.Schema):
     class Meta:
         fields = ('id','name','wish','wish_date')

#initialize schema
wishlist_schema = WishlistSchema()
wishlists_schema = WishlistSchema(many=True)


## creaate a wish
@app.route('/wish',methods=['POST'])
def add_wish():
    name = request.json['name']
    wish = request.json['wish']
    wish_date = request.json['wish_date']
    year,month,day = wish_date.split("-")
    wish_date = datetime(int(year),int(month),int(day))

    new_wish = Wishlist(name,wish,wish_date)

    db.session.add(new_wish)
    db.session.commit()
    return wishlist_schema.jsonify(new_wish)


# get all wishes
@app.route('/')
def index():
    all_wishes = Wishlist.query.order_by(Wishlist.wish_date).all()
    result = wishlists_schema.dump(all_wishes)
    return jsonify({"data":result, "status":200})

# get a wish
@app.route('/wishes/<id>',methods=['GET'])
def show(id):
    wish = Wishlist.query.get_or_404(id)
    try:
        result =  wishlist_schema.jsonify(wish)
    except:
        return 'Wish not found'
    return result

@app.route('/wishes/<id>',methods=['PATCH'])
def update(id):
    try:
        one_wish = Wishlist.query.get_or_404(id)
        name = request.json['name']
        wish = request.json['wish']
        wish_date = request.json['wish_date']
        wish_date = request.json['wish_date']
        year,month,day = wish_date.split("-")
        wish_date = datetime(int(year),int(month),int(day))

        one_wish.name = name
        one_wish.wish = wish
        one_wish.wish_date = wish_date

        db.session.commit()
        return wishlist_schema.jsonify(one_wish)
    except Exception as e:
        # return 'Wish does not exist in db'
        print(e)


if __name__ == '__main__':
    app.run(debug=True)