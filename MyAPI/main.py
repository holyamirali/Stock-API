from flask import Flask, jsonify, json
from flask_restful import Api, Resource, marshal, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import response

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
share_args_update  =   reqparse.RequestParser()


share_args.add_argument("date", type=int, help="Date is required", required=True)
share_args.add_argument("price", type=int, help="Price is required", required=True)
share_args.add_argument("volume", type=int, help="Volume is required", required=True)
share_args.add_argument("trade", type=str, help="Trade type is required", required=True)

share_args_update.add_argument("date", type=int)
share_args_update.add_argument("price", type=int)
share_args_update.add_argument("volume", type=int)
share_args_update.add_argument("trade", type=str)

resource_fields = {
    'date': fields.Integer,
    'price': fields.Integer,
    'volume': fields.Integer,
    'trade': fields.String,
}


class PostPutShare(Resource):

    @marshal_with(resource_fields)
    def post(self):
        args = share_args.parse_args()
        share = ShareModel(args['date'], args['price'], args['volume'], args['trade'])
        db.session.add(share)
        db.session.commit()
        return share, 201

    @marshal_with(resource_fields)
    def put(self):
        args = share_args_update.parse_args()
        askedShare = db.session.query(ShareModel).filter(ShareModel.date == args['date'], ShareModel.trade == args['trade']).first()
        if askedShare is not None:
            if args['price']:
                askedShare.price = args['price']
            if args['volume']:
                askedShare.volume = args['volume']
            db.session.commit()
            return askedShare, 200
        abort(404, message="Share with given date and trade type is not found !")

class GetDeleteShare(Resource):

    @marshal_with(resource_fields)
    def get(self, date, trade):
        result = db.session.query(ShareModel).filter(ShareModel.date == date, ShareModel.trade == trade).first()
        if result is not None:
            return result, 200
        abort(404, message="Share with given date and trade type is not found !")

    def delete(self, date, trade):
        askedShare = db.session.query(ShareModel).filter(ShareModel.date == date, ShareModel.trade == trade).first()
        if askedShare is not None:
            db.session.delete(askedShare)
            db.session.commit()
            resp = {'message': 'Share deleted successfully!'}
            return resp, 200
        abort(404, message="Share with given date and trade type is not found !")
        

api.add_resource(PostPutShare, "/share")
api.add_resource(GetDeleteShare, "/<int:date>/<string:trade>")

if __name__ == "__main__":
    app.run(debug=True)