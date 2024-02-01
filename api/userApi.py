import uuid,os
from flask import Blueprint, request, jsonify, render_template
from firebase_admin import firestore, storage

db = firestore.client()
user_Ref = db.collection('user')
group_Ref = db.collection('group')
member_Ref = db.collection('member')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route("/")
def home():
    
    
    return render_template('index.html')
#******************************************************
def get_user_id(email):
    # Query the Firestore collection for the email field
    query = user_Ref.where('email', '==', email).limit(1)

    # Execute the query and retrieve the user ID
    results = query.get()
    for doc in results:
        # Assuming the document ID is the user ID
        return doc.id
    return None

    
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
        
@userAPI.route("/aImage", methods=['POST'] )
def addImage():
    mail = request.form.get('email')
    image = request.files.get('image')
    
    # Check if the uploaded file is an image
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    if image.filename.split('.')[-1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file format. Only JPEG and PNG images are allowed.'}), 400

    try:
        q = user_Ref.where('email', '==', mail).get()
        
        if len(q) == 0:
            userID = get_user_id(mail)
            
            # Store the image in Firebase Storage nkap-4181f.appspot.com
            bucket = storage.bucket(name="nkap-4181f.appspot.com")
            image_name = f'profile/{mail}.jpg'
            blob = bucket.blob(image_name)
            blob.upload_from_file(image, content_type='image/jpeg')
            
            # Get the public URL of the uploaded image
            blob.make_public()
            image_url = blob.public_url
            
            return jsonify({'message': 'image saved as', 'image': image_name, 'public url': image_url }), 200
        else:
            return jsonify({'message': 'User does not exit' }), 401
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
# ***************************************************************************
@userAPI.route("/add", methods=['POST'])
def create():
    try:
        id = uuid.uuid4()
        # request of json type{ address: "Buea", email: "JonesD@gmail.com", frist name: "Dave", last name: "Jones", password: "JoneS123", pin: "", roll: ""}
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
    
@userAPI.route("/addGroup", methods=['POST'])
def createG():
    try:
        id = uuid.uuid4()
        group_Ref.document(id.hex).set(request.json)
        # request of json type{ groupHead:"", name: "exampleGroup"}
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@userAPI.route("/getGroups", methods=['GET'] )
def readG():
    try:
        all_groups = [doc.to_dict() for doc in group_Ref.stream()]
        return jsonify(all_groups), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
# ****************************************************
@userAPI.route("/addMember", methods=['POST'])
def createM():
    try:
        id = uuid.uuid4()
        # request of json type{ groupName: "exampleGroup", role: "", userEmail: "example@gmail.com", userName: "Exname"}
        member_Ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@userAPI.route("/getMembers", methods=['GET'] )
def readM():
    try:
        all_members = [doc.to_dict() for doc in member_Ref.stream()]
        return jsonify(all_members), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
