import uuid
from flask import Blueprint, request, jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route("/")
def home():
    
    
    return render_template('index.html')
#******************************************************
@userAPI.route('/login', methods=['POST'])
def signin():
    try:
        # Get login data from the request body
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        pswd_hash = password
      
        query = user_Ref.where('email', '==', email).where('password', '==', pswd_hash).get()
        if len(query) == 0:
            
            return jsonify({'error': 'Wrong email or password'}), 401
    
        else:
            return jsonify({'message': 'Login Successful',
                        'email': email
                        }), 200
  
    except Exception as e:
        return jsonify({'message': 'Login Successful',
                        'email': email
                        }), 200
# ***************************************************************************
@userAPI.route("/add", methods=['POST'])
def create():
    try:
        id = uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@userAPI.route("/getUser", methods=['GET'] )
def read():
    try:
        all_users = [doc.to_dict() for doc in user_Ref.stream()]
        return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
    
