# -*- coding: utf-8 -*-

from . import auth_blueprint
from app import db, models, bcrypt, utils
from flask import request, make_response, jsonify
from flask.views import MethodView


class RegistrationView(MethodView):
    """ User Registration Resource """
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = models.User.query.\
            filter_by(username=post_data.get('username')).first()

        if not user:
            try:
                user = models.User(username=post_data.get('username'),
                                   password=post_data.get('password'))

                db.session.add(user)
                db.session.commit()

                role = 'Admin' if user.admin else 'User'
                # generate the auth token
                auth_token = user.encode_auth_token(user.id, role)

                response = utils.Response('Success',
                                          'Successfully registered.')._asdict()
                response['auth_token'] = auth_token.decode()
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = utils.Response(
                    'Fail', 'Some error occurred. Please try again.')
                return make_response(jsonify(response._asdict())), 401

        else:
            response = utils.Response('Fail',
                                      'User already exists. Please Log in.')
            return make_response(jsonify(response._asdict())), 202


class LoginView(MethodView):
    """ User Login Resource """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = models.User.query.filter_by(
                username=post_data.get('username')).first()

            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                role = 'Admin' if user.admin else 'User'
                auth_token = user.encode_auth_token(user.id, role)
                if auth_token:
                    response = {
                        'status': 'Success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200

            else:
                response = utils.Response('Fail', 'User does not exist.')
                return make_response(jsonify(response._asdict())), 404

        except Exception as e:
            print(e)
            response = utils.Response('Fail', 'Try again')
            return make_response(jsonify(response._asdict())), 500


class LogoutView(MethodView):
    """ Logout Resource """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = models.User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = models.BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()

                    response = utils.Response('Success',
                                              'Successfully logged out.')
                    return make_response(jsonify(response._asdict())), 200

                except Exception as e:
                    response = utils.Response('Fail', e)
                    return make_response(jsonify(response._asdict())), 200

            else:
                response = utils.Response('Fail', resp)
                return make_response(jsonify(response._asdict())), 401

        else:
            response = utils.Response('Fail', 'Provide a valid auth token.')
            return make_response(jsonify(response._asdict())), 403


# =====================   Register endpoints   ==============================

auth_blueprint.add_url_rule('/register',
                            view_func=RegistrationView.as_view('registration'),
                            methods=['POST'])

auth_blueprint.add_url_rule('/login',
                            view_func=LoginView.as_view('login'),
                            methods=['POST'])

auth_blueprint.add_url_rule('/logout',
                            view_func=LogoutView.as_view('logout'),
                            methods=['POST'])
