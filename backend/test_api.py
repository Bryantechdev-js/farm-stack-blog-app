#!/usr/bin/env python3
"""
Test the API endpoints
"""
import asyncio
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    print("\n[TEST] Health endpoint")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200

def test_signup():
    print("\n[TEST] Signup endpoint")
    payload = {
        "email": f"test_{asyncio.get_event_loop().time()}@test.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/signup", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200

def test_login():
    print("\n[TEST] Login endpoint")
    # First create a user
    email = f"test_{asyncio.get_event_loop().time()}@test.com"
    payload = {
        "email": email,
        "password": "testpassword123"
    }
    signup_response = client.post("/auth/signup", json=payload)
    print(f"Signup Status: {signup_response.status_code}")
    
    # Then login
    login_response = client.post("/auth/login", json=payload)
    print(f"Login Status: {login_response.status_code}")
    print(f"Login Response: {login_response.json()}")
    print(f"Cookies: {login_response.cookies}")
    assert login_response.status_code == 200

if __name__ == "__main__":
    print("=" * 50)
    print("Testing API Endpoints")
    print("=" * 50)
    
    try:
        test_health()
        test_signup()
        test_login()
        print("\n" + "=" * 50)
        print("All tests passed!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
