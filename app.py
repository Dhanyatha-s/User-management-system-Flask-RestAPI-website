from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from model import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize API
api = Api(app)

# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Define request parser for user registration
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
user_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

class RegisterUser(Resource):
    def post(self):
        try:
            args = user_parser.parse_args()
            username = args['username']
            password = args['password']

            # Check if the user already exists
            if User.query.filter_by(username=username).first():
                return {'message': 'User already exists!!'}, 400
            
            # Create a new user and add to the database
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            return {'message': 'New User Created'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'username': user.username} for user in users], 200
    
# Define the API resources and their routes
api.add_resource(RegisterUser, '/api/register')
api.add_resource(UserList, '/api/users')  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        # Send registration request to the API
        import requests
        response = requests.post('http://127.0.0.1:5000/api/register', json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 201:  # Check for successful registration
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the index page
        else:
            flash(response.json().get('message', 'Registration failed'), 'danger')
            return render_template('register.html')  # Render the form again on failure

    return render_template('register.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
