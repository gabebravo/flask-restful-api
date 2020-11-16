from flask import Flask, request
from flask_restful import Resource, Api
#  from typing import Any, Generic, Optional, TypeVar

app = Flask(__name__)
api = Api(app)

items = []


class ItemList(Resource):
    def get(self):
        return {'items': items} if len(items) else ({'items': None}, 400)


class Item(Resource):

    def get(self, name: str):
        item_by_name = {'item': next(  # next is an iterator helper
            filter(lambda x: x['name'] == name, items), None)}
        # ternary returns 400 status code if item not found
        return item_by_name if item_by_name['item'] else (item_by_name, 400)

    def post(self):
        data = request.get_json()

        if next(filter(lambda x: x['name'] == data['name'], items), None) is not None:
            return {'message': f"An item with name {data['name']} already exists."}

        item = {'name': data['name'], 'price': data['price']}
        items.append(item)
        return item, 201


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item', '/item/<string:name>')

if __name__ == '__main__':
    # important to mention debug=True, defaults to port:5000
    app.run(debug=True)
