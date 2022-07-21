from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

#create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)
api=Api(app)
#@app.route('/test',methods=['GET'])
@app.route('/user', methods=['GET', 'POST'])
#test
#def test():
	#if request.method == "GET":
		#return jsonify({"response":"Get Request Called"})

#User resource
class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String(100))
	password=db.Column(db.String(100))
	username=db.Column(db.String(100))
	created_at=db.Column(db.DateTime())
	updated_at=db.Column(db.DateTime())
	def __repr__(self):
		return '<Station %s>' % self.name

#Marshmallow schema class
class UserSchema(ma.Schema):
	class Meta:
		fields=('id', 'email', 'password', 'username', 'created_at', 'updated_at')

#create a schema for one user and one for a list of users
user_schema=UserSchema()
users_schema=UserSchema(many=True)

#get lists of all user resource and post a new 
class UserListResource(Resource):
	def get(self):
		users=User.query.all()
		return users_schema.dump(users)

	def post(self):
		new_user=User(
			email=request.json['email'],
			password=request.json['password'],
			username=request.json['username'],
			created_at=request.json['created_at'],
			updated_at=request.json['updated_at'],
		)
		db.session.add(new_user)
		db.session.commit()
		return user_schema.dump(new_user)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    def patch(self, user_id):
        user = Station.query.get_or_404(user_id)
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.password = request.json['password']
        if 'username' in request.json:
            user.username = request.json['username']
        if 'created_at' in request.json:
            user.created_at = request.json['created_at']
        if 'updated_at' in request.json:
            user.updated_at = request.json['updated_at'] 
        db.session.commit()
        return station_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204		

api.add_resource(UserListResource, '/users/')
api.add_resource(UserResource, '/users/<int:user_id>/')

if __name__=="__main__":
	app.run(debug=True)