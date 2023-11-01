from errno import EIDRM
import requests
import json

BASE_URL = "http://127.0.0.1:5000"
current_user=0
admin_token="invalid"

def register_user():
    global current_user
    address = input("Enter your address: ")
    url = f"{BASE_URL}/register"
    data = {"address": address}
    response = requests.post(url, json=data)
    current_user = (response.json())["user_id"]
    print(response.json())

def list_menu():
    url = f"{BASE_URL}/menu"
    response = requests.get(url)
    data=response.json()
    print("======================")
    print("   Tastiest Menu:")
    print("======================")
    for entry in data:
        eid = entry["id"]
        ename = entry["name"]
        eprice = entry["price"]
        print(f"||{eid}, {ename} , |{eprice}$ ||")

def create_order():
    global current_user
    if current_user==0:
        print("You need to register first.")
        return
    user_id = current_user
    pizza_id = int(input("Enter pizza ID from the menu: "))
    quantity = int(input("Enter quantity: "))
    order_data = {"user_id": user_id, "pizza_id": pizza_id, "quantity": quantity}
    url = f"{BASE_URL}/order"
    response = requests.post(url, json=order_data)
    if (response.json())["message"]=="error":
        print("User not found, please register first.")
        return
    data=(response.json())["order"]
    print("===========================")
    print("Successfully placed order")
    print("===========================")
    did = data["id"]
    dadd = data["address"]
    print(f"Order ID: {did} to be delivered to {dadd}")

def check_order_status():
    global current_user
    user_id = current_user
    order_id = int(input("Enter order ID: "))
    url = f"{BASE_URL}/order/{user_id}/{order_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            order_status = response.json()
            orst =  order_status["status"]
            print(f"Your order is {orst}")
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON in response.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def cancel_order():
    order_id = int(input("Enter order ID to cancel: "))
    url = f"{BASE_URL}/order/{order_id}"
    response = requests.delete(url)
    print(response.json()["message"])

def admin_action():
    global admin_token
    admin_token = input("Enter admin token: ")
    url = f"{BASE_URL}/admin"
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(url, headers=headers)
    print((response.json())["message"])

def add_pizza():
    global admin_token
    name = input("Enter pizza name: ")
    price = float(input("Enter pizza price: "))
    pizza_data = {"name": name, "price": price}
    url = f"{BASE_URL}/admin/add_pizza"
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(url, json=pizza_data, headers=headers)
    print((response.json())["message"])

def delete_pizza():
    global admin_token
    pizza_id = int(input("Enter pizza ID to delete: "))
    url = f"{BASE_URL}/admin/delete_pizza/{pizza_id}"
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.delete(url, headers=headers)
    print((response.json())["message"])

def main():
    while True:
        print("^~~~~~~~~~~~~~~~~~~~~~~~~~~~^")
        print("Super Cool Pizza Store")
        print("1. Register User")
        print("2. List Menu")
        print("3. Create Order")
        print("4. Check Order Status")
        print("5. Cancel Order")
        print("6. Admin Action")
        print("7. Add Pizza to Menu")
        print("8. Delete Pizza from Menu")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            list_menu()
        elif choice == "3":
            create_order()
        elif choice == "4":
            check_order_status()
        elif choice == "5":
            cancel_order()
        elif choice == "6":
            admin_action()
        elif choice == "7":
            add_pizza()
        elif choice == "8":
            delete_pizza()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
