from flask import Blueprint, request,jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from datetime import timedelta
auth_bp=Blueprint("auth",__name__)

# Regiester Route

@auth_bp.route('/register',methods=['POST'])

def register():
    data=request.get_json()
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')

    # check required fields 
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}),400
    

    # check for existing user email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}),400
    
    # check for existing user email
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 400
    

    # create new user 
    new_user=User(username=username,email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user registered successfully"}),201


# Login Route

@auth_bp.route('/login',methods=['POST'])

def login():
    data=request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "All input fields are required"}),400
    
    # find user 
    user=User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # create token for 1 day 
    access_token =create_access_token(identity=user.id,expires_delta=timedelta(hours=1)) # creating session token for logging in 
    refresh_token=create_refresh_token(identity=user.id,expires_delta=timedelta(days=7))
    return jsonify({
        "message":"login successful",
        "access_token":access_token,
        "refresh_token":refresh_token,
        "user_id":user.id
    }),200


#Refresh token route

@auth_bp.route('/refresh',methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id=get_jwt_identity()
    new_access_token=create_access_token(identity=user_id,expires_delta=timedelta(hours=1))

    return jsonify({
        "access_token":new_access_token
    }),200
# protected profile route 

@auth_bp.route('/profile',methods=["GET"])
@jwt_required()
def profile():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)

    if not user:
        return jsonify({"error":"User not found"}),404
    
    return jsonify({
        "username":user.username,
        "email":user.email,
        "created_at":user.created_at
    }),200

