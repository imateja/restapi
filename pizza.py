import random
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

menu = [
    {"id": 1, "name": "Margherita", "price": 10.99},
    {"id": 2, "name": "Pepperoni", "price": 12.99},
]

orders = []
admin_token = "supersecret"
user_data = {}

class Register(Resource):
    def post(self):
        user_id = len(user_data) + 1
        user_address = request.json.get("address")
        user_data[user_id] = {"address": user_address}
        return {"user_id": user_id, "message": "Registration successful", "address": user_address}

class Menu(Resource):
    def get(self):
        return jsonify(menu)

class CreateOrder(Resource):
    def post(self):
        user_id = request.json.get("user_id")
        if user_id in user_data:
            order_data = request.json
            order_data["user_id"] = user_id
            order_data["address"] = user_data[user_id]["address"]
            order_data["id"] = len(orders) +1
            order_data["status"] = random.choice(["ready", "not ready"])
            orders.append(order_data)
            return {"message": "Order placed successfully", "order": order_data}
        else:
            return {"message": "error"}, 400

class OrderStatus(Resource):
    def get(self, user_id, order_id):
        for order in orders:
            if order["id"] == order_id and order.get("user_id") == user_id:
                return {"status": order["status"]}
        return {"message": "Order not found or unauthorized"}, 404

class CancelOrder(Resource):
    def delete(self, order_id):
        for order in orders:
            if order["id"] == order_id and order["status"] != "ready":
                orders.remove(order)
                return {"message": "Order canceled successfully"}
            elif order["id"] == order_id and order["status"] == "ready":
                return {"message": "Cannot cancel, order is ready for delivery"}
        return {"message": "Order not found"}, 404

class Admin(Resource):
    def post(self):
        token = request.headers.get("Authorization")
        if token == f"Bearer {admin_token}":
            return {"message": "Admin authorization successful"}
        return {"message": "Unauthorized"}, 401

class AddPizza(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name cannot be blank")
        parser.add_argument("price", type=float, required=True, help="Price cannot be blank")
        args = parser.parse_args()

        token = request.headers.get("Authorization")
        if token == f"Bearer {admin_token}":
            pizza = {"id": len(menu) + 1, "name": args["name"], "price": args["price"]}
            menu.append(pizza)
            return {"message": "Pizza added to the menu", "pizza": pizza}
        return {"message": "Unauthorized"}, 401

class DeletePizza(Resource):
    def delete(self, pizza_id):
        token = request.headers.get("Authorization")
        if token == f"Bearer {admin_token}":
            for pizza in menu:
                if pizza["id"] == pizza_id:
                    menu.remove(pizza)
                    return {"message": "Pizza deleted from the menu"}
            return {"message": "Pizza not found"}, 404
        return {"message": "Unauthorized"}, 401

api.add_resource(Register, "/register")
api.add_resource(Menu, "/menu")
api.add_resource(CreateOrder, "/order")
api.add_resource(OrderStatus, "/order/<int:user_id>/<int:order_id>")
api.add_resource(CancelOrder, "/order/<int:order_id>")
api.add_resource(Admin, "/admin")
api.add_resource(AddPizza, "/admin/add_pizza")
api.add_resource(DeletePizza, "/admin/delete_pizza/<int:pizza_id>")

if __name__ == "__main__":
    app.run(debug=True)
