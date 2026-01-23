from flask import request
from flask_socketio import join_room, leave_room
from backend.socket_instance import socketio
import jwt
import os

@socketio.on('connect')
def on_connect():
    print('Client connected:', request.sid)

@socketio.on('join')
def on_join(data):
    # data: { token: "..." }
    token = data.get('token')
    if not token: return
    
    try:
        # Decode to get User ID and Role
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "dev_secret"), algorithms=["HS256"])
        uid = payload['sub']
        role = payload.get('role') # We might need to ensure role is in JWT or query USER
        
        # Simple rooms: user_<id>, role_<role>
        # But per requirements: customer_<id>, chef_<id>, driver_<id>
        # Ideally we query user to get role if not in JWT, but let's assume valid ID
        
        # We need role to form the correct channel name.
        # Let's re-query user to be safe or update auth.py to include role in JWT
        # For now, let's trust the client provided role or better, just use user_<id> and broadcast carefully
        # Requirement: "role-based notification channels: customer_<id>..."
        
        # Let's perform a user lookup or trust a passed 'role' from client if authenticated
        # Simpler: update auth.py to include role in JWT payload.
        # Assuming we update auth.py next.
        pass
    except Exception as e:
        print(e)

@socketio.on('auth_join')
def on_auth_join(data):
    token = data.get('token')
    if not token: return
    try:
        # We need the secret key from app config, but here we can use os.getenv
        secret = os.getenv("SECRET_KEY", "dev_secret")
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        uid = payload['sub']
        # We need the role here. Let's create a room "user_<uid>" 
        # API will emit to "user_<uid>" and frontend will decide?
        # Requirement says: customer_<id>, chef_<id>
        # Let's fetch user role from DB is safer.
        from backend.models import User
        user = User.query.get(uid)
        if user:
            room_name = f"{user.role}_{user.id}"
            join_room(room_name)
            print(f"User {uid} joined room {room_name}")
            
            if user.role == 'driver':
                join_room('drivers_all') # For pool notifications
    except Exception as e:
        print("Socket Auth Fail:", e)

@socketio.on('update_location')
def on_location(data):
    # Driver sends { lat: x, lng: y }
    # verify token...
    pass
