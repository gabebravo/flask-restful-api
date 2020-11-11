from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class Item(Resource):

    def get(self, name):
        return {'item': name}


api.add_resource(Item, '/item/<string:name>')  # localhost:5000/item/desk

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
