from flask import Blueprint, make_response, request, jsonify
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from app.models.user_models import User
from app.models.black_list import BlacklistToken
from app import db

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """User Registration Resource"""

    def post(self):
        """Handles post requests to this url /auth/register"""
        #gets the post data
        post_data = request.get_json()

        #checks if user exist
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    post_data.get("firstname"), post_data.get("lastname"),
                    post_data.get("email"), post_data.get("password"))
                # insert the user
                db.session.add(user)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return make_response(jsonify(responseObject)), 201

            except Exception as e:

                responseObject = {'status': 'Failed', 'message': str(e)}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'Failed',
                'message': 'User already exist. Please Login'
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """User Login Resource"""

    def post(self):
        """Handles post requests to this url /auth/login"""

        post_data = request.get_json()

        user = User.query.filter_by(email=post_data.get("email")).first()
        try:
            login = bool(user and Bcrypt().check_password_hash(
                user.password, post_data.get("password")))
            if not login:
                raise ValueError
        except (AttributeError, ValueError):
            response = {"Message": "Incorrect Email or Password"}
            return make_response(jsonify(response)), 401
        else:
            access_token = User.generate_token(user.id)
            response = {
                'message': 'You have successfully logged in',
                "Access token": access_token.decode(),
                'email': user.email
            }
            return make_response(jsonify(response)), 200


class LogoutAPI(MethodView):
    """User Login Resource"""

    def post(self):
        """Handle post request to this url /auth/login"""
        access_token = request.headers.get('Authorization')

        if not access_token:
            return make_response(
                jsonify({
                    "message": "Please Provide an access token"
                })), 401
        revoked_token = BlacklistToken(revoked_token=access_token)
        revoked_token.save()
        response = {"message": "You have successfully logged out"}
        return make_response(jsonify(response)), 200


# define the API resources
registration_view = RegisterAPI.as_view('register_view')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_view')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule(
    '/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule(
    '/auth/logout', view_func=logout_view, methods=['POST'])
