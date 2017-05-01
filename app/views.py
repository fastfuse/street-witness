
# -*- coding: utf-8 -*-

import copy
from app import app, db, admin, models, bcrypt
from flask import (request,
                   redirect,
                   render_template,
                   make_response,
                   url_for,
                   jsonify)
from flask.views import MethodView
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from wtforms import fields
from collections import namedtuple


# ===========================  Help functions   ==============================

def register_api(view, endpoint, url, pk='id', pk_type='any'):
    """ Function to simplify registration
        of API Views (based on MethodView) """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('{url}<{pk_type}:{pk}>'.format(url=url,
                                                    pk_type=pk_type,
                                                    pk=pk),
                     view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


# namedtuple to simplify creation of response messages
Response = namedtuple('Response', ['status', 'message'])


@app.errorhandler(404)
def not_found(error):
    """ RESTful 404 error """
    return make_response(jsonify({'error': 'Not found'}), 404)


# ============================   Admin views   ================================

class IncidentsView(ModelView):
    form_choices = {'status': [('active', 'Активний'),
                               ('archived', 'Архів')]}

    form_overrides = {'description': fields.TextAreaField}

    form_widget_args = {'description': {'rows': 10},
                        'location': {'rows': 4}}


class UserView(ModelView):
    column_exclude_list = ['password', ]


admin.add_view(IncidentsView(models.Incident, db.session))
admin.add_view(UserView(models.User, db.session))
admin.add_view(ModelView(models.BlacklistToken, db.session))


# =============================   Index page   ==============================

@app.route('/')
def index():
    """ Only renders index page """
    return render_template('index.html')


# ==============================   API   ====================================

class IncidentsAPI(MethodView):
    """ Incidents Resourse """
    def get(self, incident_id):
        """ Get all incidents or single incident by ID """

        # add 404 error if no such item
        # jsonify returns response obj

        if incident_id:
            incident_query = models.Incident.query.get_or_404(incident_id)

            incident = incident_query.__dict__
            incident.pop('_sa_instance_state')

            return make_response(jsonify(incident))

        else:
            status = request.args.get('status', None)
            if status:
                incidents_query = models.Incident.query.\
                    filter_by(status=status).all()

            else:
                incidents_query = models.Incident.query.all()

            incidents = []
            for item in incidents_query:
                incident = item.__dict__
                incident.pop('_sa_instance_state')
                incidents.append(incident)

            return make_response(jsonify(incidents=incidents,
                                              count=len(incidents)))

    def post(self):
        """ Add new incident """
        post_data = request.get_json() # test it
        new_incident = models.Incident(request.json['title'],
                                       request.json['description'],
                                       request.json['location'])

        response = copy.deepcopy(new_incident.__dict__) # refactor as generic function
        response.pop('_sa_instance_state')

        db.session.add(new_incident)
        db.session.commit()

        return make_response(jsonify(response), 201)


class RegistrationAPI(MethodView):
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
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                response_object = {
                    'status': 'Success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                print(user.__dict__)
                return make_response(jsonify(response_object)), 201

            except Exception as e:
                response = Response('Fail',
                                    'Some error occurred. Please try again.')
                return make_response(jsonify(response._asdict())), 401

        else:
            response = Response('Fail', 'User already exists. Please Log in.')
            return make_response(jsonify(response._asdict())), 202


class LoginAPI(MethodView):
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
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response = {
                        'status': 'Success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200

            else:
                response = Response('Fail', 'User does not exist.')
                return make_response(jsonify(response._asdict())), 404

        except Exception as e:
            print(e)
            response = Response('Fail', 'Try again')
            return make_response(jsonify(response._asdict())), 500


class UserAPI(MethodView):
    """ User Resource """
    def get(self, id):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split()[1]
        else:
            auth_token = ''

        if auth_token:
            resp = models.User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = models.User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'Success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(response_object)), 200

            response = Response('Fail', resp)
            return make_response(jsonify(response._asdict())), 401

        else:
            response = Response('Fail', 'Provide a valid auth token')
            return make_response(jsonify(response._asdict())), 401


class LogoutAPI(MethodView):
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

                    response = Response('Success', 'Successfully logged out.')
                    return make_response(jsonify(response._asdict())), 200

                except Exception as e:
                    response = Response('Fail', e)
                    return make_response(jsonify(response._asdict())), 200

            else:
                response = Response('Fail', resp)
                return make_response(jsonify(response._asdict())), 401

        else:
            response = Response('Fail', 'Provide a valid auth token.')
            return make_response(jsonify(response._asdict())), 403


# =====================   Register API endpoints   ==========================

register_api(IncidentsAPI, 'incidents_api', '/api/incidents/',
             pk='incident_id', pk_type='int')
register_api(RegistrationAPI, 'registration_api', '/api/register')
register_api(LoginAPI, 'login_api', '/api/login')
register_api(UserAPI, 'user_api', '/api/user')
register_api(LogoutAPI, 'logout_api', '/api/logout')
