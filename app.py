from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def _find_item(self, name):
        return next(filter(lambda i: i["name"] == name, items), None)

    def get(self, name):
        item = self._find_item(name)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        existing_item = self._find_item(name)
        if existing_item is not None:
            return {"message": "Item already created"}, 409
        data = request.get_json()
        new_item = {"name": name, "price":data["price"]}

        items.append(new_item)
        return {"item": new_item}, 201

    def put(self, name):
        data = request.get_json()
        existing_item = self._find_item(name)
        if existing_item is not None:
            existing_item["price"]=data["price"]
            return {"item": existing_item}, 201
        else:
            new_item = {"name": name, "price": data["price"]}
            items.append(new_item)
            return {"item": new_item}, 201

api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)
