import datetime
import re
from flask import Flask, jsonify, request
from flask import abort
from werkzeug.security import generate_password_hash
import jwt
from app.dbmodel.dbmodels import users



# instantiating app object
app = Flask(__name__)

app.config['SECRET KEY'] = 'thisissecret'

NewUser = users()

# Login_


@app.route('/api/v1/Login', methods=['POST'])
def user_login():
    post_data = request.get_json()
    email = post_data('email')
    user_password = post_data('user_password')

    if not NewUser.login(email, user_password):
        return jsonify({'message': 'Invalid input data'}), 401

    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() +
                        datetime.timedelta(minutes=20)}, app.config['SECRET KEY'])
    return jsonify({'token': token.decode('UTF-8')}), 201

# signup endpoint


@app.route('/api/v1/Signup', methods=['POST'])
def Signup():

    signup_data = request.get_json()
    email = signup_data['email']
    username = signup_data['username']
    user_password = signup_data['user_password']
    confirm_password = signup_data['confirm_password']
    role = 'Normal user'
    if len(username) <= len('liver'):
        return jsonify({'message': 'Below acceptable character length.'})
    if len(email) <= len('liverpool'):
        return jsonify({'message': 'Invalid email character length.'})

    if len(email) <= len('mapp@gmail.com'):
        return jsonify({'message': 'Invalid email character length.'})

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return jsonify({'message': 'Invalid email address.'})

    if user_password != confirm_password:
        return jsonify({'message': 'Unmatching passwords. Please try again.'})
    user_password = generate_password_hash(signup_data['user_password'], method='sha256')
    confirm_password = generate_password_hash(signup_data['confirm_password'], method='sha256')

    NewUser.signup(email, username, user_password, confirm_password, role)
    return jsonify({'message': 'new user created'}), 201

# all users route


@app.route('/api/v1/users', methods=['GET'])
def allUsers():
    return jsonify(NewUser.all_users()), 200

# create request endpoint


@app.route('/api/v1/requests', methods=['POST'])
def add_requests():
    if not request.json or not 'request_type' in request.json:
        abort(400)

    NewRequest = request.get_json()
    request_type = NewRequest['request_type']
    desscription = NewRequest['desscription']

    if len(request_type) < len('liverpool'):
        return jsonify({'message': 'Minimum character length is 10'})

    if len(desscription) < len('liverpool'):
        return jsonify({'message': 'Minimum character length is 10'})
    if len(desscription) < len('manchester'):
        return jsonify({'message': 'Minimum character length is 10'})
    NewUser.create_request(request_type, desscription)
    return jsonify({'message': 'Your request has been successfully submitted'}), 200

# get all requests endpoint


@app.route('/api/v1/requests', methods=['GET'])
def requests():
    return jsonify(NewUser.get_all_requests()), 200

# update request endpoint


@app.route('/api/v1/requests/<int:requestid>', methods=['PUT'])
def r_edit():
    redit = request.get_json()
    requestid = redit['requestid']
    request_type = redit['request_type']
    desscription = redit['desscription']
    NewUser.edit_request(request_type, desscription, requestid)
    if requestid < 0:
        return jsonify({'message': 'invalid requestid'}), 405
    return jsonify({'message': 'Request successfully updated'}), 200

# get request by id

@app.route('/api/v1/requests/<requestid>', methods=['POST'])
def get_requestid():
    return jsonify(NewUser.getby_id()), 200


# starting the server
if __name__ == '__main__':
    app.run(debug=True)
