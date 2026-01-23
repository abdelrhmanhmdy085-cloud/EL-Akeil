#!/usr/bin/env python3
"""
Test script for Chef Location Map API
تجربة مسارات API الخريطة
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

# Test data
test_user_token = None
test_chef_id = 1

def test_api():
    print("=" * 60)
    print("🗺️  Chef Location Map - API Test")
    print("=" * 60)
    
    # Test 1: Get all chefs
    print("\n✅ Test 1: Get all chefs")
    try:
        response = requests.get(f"{API_BASE}/customer/chefs")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Chefs found: {len(data)}")
        if data:
            print(f"Sample chef: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get chefs with location filter
    print("\n✅ Test 2: Get chefs with location filter")
    try:
        response = requests.get(
            f"{API_BASE}/customer/chefs",
            params={
                "lat": 30.0444,
                "long": 31.2357,
                "max_distance": 50
            }
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Nearby chefs found: {len(data)}")
        if data:
            chef = data[0]
            print(f"Chef name: {chef.get('name')}")
            print(f"Distance: {chef.get('distance')} km")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get dishes
    print("\n✅ Test 3: Get available dishes")
    try:
        response = requests.get(f"{API_BASE}/customer/dishes")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Dishes found: {len(data)}")
        if data:
            dish = data[0]
            print(f"Dish: {dish.get('name')} - {dish.get('price')} EGP")
            print(f"Chef ID: {dish.get('user_id')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get heatmap data
    print("\n✅ Test 4: Get heatmap data")
    try:
        response = requests.get(f"{API_BASE}/customer/heatmap-data")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Heatmap points found: {len(data)}")
        if data:
            point = data[0]
            print(f"Sample point: Lat {point.get('lat')}, Lng {point.get('lng')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get chef analytics
    print("\n✅ Test 5: Get chef analytics")
    try:
        response = requests.get(f"{API_BASE}/customer/chef-analytics")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Get busy areas
    print("\n✅ Test 6: Get busy areas")
    try:
        response = requests.get(f"{API_BASE}/customer/busy-areas")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Busy areas found: {len(data)}")
        if data:
            area = data[0]
            print(f"Top busy area: Lat {area.get('lat')}, Status: {area.get('status')}")
            print(f"Order count: {area.get('order_count')}")
            print(f"Active chefs: {area.get('active_chefs')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    print("Starting API tests...")
    print(f"Base URL: {BASE_URL}")
    print("\nMake sure the server is running: python src/backend/app.py\n")
    
    try:
        test_api()
    except Exception as e:
        print(f"❌ Test failed: {e}")
