from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
#  from typing import Any, Generic, Optional, TypeVar

app = Flask(__name__)
app.secret_key = 'yowzers'  # in produciton make this an env var - DO NOT EXPOSE
api = Api(app)
jwt = JWT(app, authenticate, identity)  # this will forward to the /auth route
# first calls authenticate, gets JWT, and then forwards it to identity

items = []


class ItemList(Resource):
    def get(self):
        return {'items': items} if len(items) else ({'items': None}, 400)


class Item(Resource):
    @jwt_required()  # decorator will do the auth check before accessing the GET
    def get(self, name: str):
        item_by_name = {'item': next(  # next returns first value on the filter function
            filter(lambda x: x['name'] == name, items), None)}
        # ternary returns 400 status code if item not found
        return item_by_name if item_by_name['item'] else (item_by_name, 400)

    def post(self):
        data = request.get_json()

        if next(filter(lambda x: x['name'] == data['name'], items), None) is not None:
            return {'message': f"An item with name {data['name']} already exists."}, 400

        item = {'name': data['name'], 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self):
        global items
        data = request.get_json()
        print(data)
        items = list(
            filter(lambda item: item['name'] != data['name'], items))

        return {'message': f"Items deleted"}, 200


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item', '/item/<string:name>')

if __name__ == '__main__':
    # important to mention debug=True, defaults to port:5000
    app.run(debug=True)
