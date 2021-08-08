from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/tosanapi'
db = SQLAlchemy(app)

class ShareModel(db.Model):
    __tablename__='Shares'
    id      = db.Column(db.Integer, primary_key=True)
    date    = db.Column(db.Integer)
    price   = db.Column(db.Integer)
    volume  = db.Column(db.Integer)
    trade   = db.Column(db.String(40))

    #def __repr__(self):
	#    return f"Share(date = {date}, price = {price}, volume = {volume} )"

    def __init__(self, date, price, volume, trade):
        self.date = date
        self.price = price
        self.volume = volume
        self.trade = trade

share_args  =   reqparse.RequestParser()
share_args.add_argument("date", type=int, help="Date is required")
share_args.add_argument("price", type=int, help="Price is required")
share_args.add_argument("volume", type=int, help="Volume is required")
share_args.add_argument("trade", type=str, help="Trade is required")

resource_fields = {
    'id': fields.Integer,
    'date': fields.Integer,
    'price': fields.Integer,
    'volume': fields.Integer,
    'trade': fields.String
}


class Share(Resource):
    @marshal_with(resource_fields)
    def get(self, ):
        return

    @marshal_with(resource_fields)
    def post(self):
        args = share_args.parse_args()
        share = ShareModel(args['date'], args['price'], args['volume'], args['trade'])
        db.session.add(share)
        db.session.commit()
        return share, 201

api.add_resource(Share, "/share")

if __name__ == "__main__":
    app.run(debug=True)