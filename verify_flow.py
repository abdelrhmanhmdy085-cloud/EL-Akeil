import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

def register(role, username, password, extra={}):
    url = f"{BASE_URL}/register/{role}"
    data = {"username": username, "password": password, "name": f"{role}_user"}
    data.update(extra)
    res = requests.post(url, json=data)
    if res.status_code == 201: return res.json()['token']
    if res.status_code == 409: 
        # login if exists
        return requests.post(f"{BASE_URL}/login", json={"username": username, "password": password}).json()['token']
    print(f"Failed to register {role}: {res.text}")
    return None

def run_flow():
    print("1. Registering Users...")
    chef_token = register("chef", "chef_v1", "pass", {"address": "Cairo"})
    cust_token = register("customer", "cust_v1", "pass", {"phone": "123", "lat": 30.0, "long": 31.0})
    driver_token = register("driver", "driver_v1", "pass", {"national_id": "999", "face_id_data": "base64xyz"})

    print("2. Chef adding dish...")
    dish = requests.post(
        f"{BASE_URL}/chef/dishes", 
        json={"name": "Koshary", "price": 50, "description": "Tasty"},
        headers={"Authorization": f"Bearer {chef_token}"}
    ).json()['dish']
    print(f"   Dish Added: {dish['id']}")

    print("3. Customer placing order...")
    order = requests.post(
        f"{BASE_URL}/order",
        json={"chef_id": dish['chef_id'], "items": [{"dish_id": dish['id'], "qty": 2, "price": 50, "name": "Koshary"}]},
        headers={"Authorization": f"Bearer {cust_token}"}
    ).json()['order']
    print(f"   Order Placed: {order['id']} - Status: {order['status']}")

    print("4. Chef processing order...")
    requests.post(f"{BASE_URL}/chef/order/{order['id']}/status", json={"status": "cooking"}, headers={"Authorization": f"Bearer {chef_token}"})
    requests.post(f"{BASE_URL}/chef/order/{order['id']}/status", json={"status": "ready"}, headers={"Authorization": f"Bearer {chef_token}"})
    print("   Order is READY")

    print("5. Driver accepting order...")
    requests.post(f"{BASE_URL}/driver/accept/{order['id']}", headers={"Authorization": f"Bearer {driver_token}"})
    requests.post(f"{BASE_URL}/driver/update/{order['id']}", json={"status": "delivered"}, headers={"Authorization": f"Bearer {driver_token}"})
    print("   Order DELIVERED")

    print("6. Customer reviewing...")
    res = requests.post(
        f"{BASE_URL}/review",
        json={"chef_id": dish['chef_id'], "rating": 5, "comment": "Great food!"},
        headers={"Authorization": f"Bearer {cust_token}"}
    )
    print(f"   Review Submitted: {res.json()['ok']}")

    print("Verification Complete!")

if __name__ == "__main__":
    try:
        run_flow()
    except Exception as e:
        print(f"Error: {e}")
