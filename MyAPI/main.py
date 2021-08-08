from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
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
    #'id': fields.Integer,
    'date': fields.Integer,
    'price': fields.Integer,
    'volume': fields.Integer,
    'trade': fields.String
}


class PostPutShare(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = share_args.parse_args()
        share = ShareModel(args['date'], args['price'], args['volume'], args['trade'])
        db.session.add(share)
        db.session.commit()
        return share, 201

class GetDeleteShare(Resource):

    @marshal_with(resource_fields)
    def get(self, date, trade):
        #result = ShareModel.query.filter_by(trade=trade)
        result = db.session.query(ShareModel).filter(ShareModel.date == date, ShareModel.trade == trade).first()
        #for res in result:
        #    print(res.price)
        #    return res, 200
        print("date equals : {}".format(date))
        print("trade equals : {}".format(trade))
        if result is not None:
            print(result)
            return result, 200
        abort(404, message="No share found !")
api.add_resource(PostPutShare, "/share")
api.add_resource(GetDeleteShare, "/<int:date>/<string:trade>")

if __name__ == "__main__":
    app.run(debug=True)