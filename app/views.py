
# -*- coding: utf-8 -*-

import copy
from app import app, db, admin, models, bcrypt, utils
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
admin.add_view(ModelView(models.File, db.session))
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

    decorators = [utils.login_required]

    def get(self, incident_id, **kwargs):
        """ Get all incidents or single incident by ID """
        if incident_id:
            incident_query = models.Incident.query.get_or_404(incident_id)
            incident = incident_query.__serialize__()

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
                incidents.append(item.__serialize__())

            return make_response(jsonify(incidents=incidents,
                                         count=len(incidents)))

    def post(self, **kwargs):
        """ Add new incident """
        post_data = request.get_json()
        new_incident = models.Incident(title=post_data['title'],
                                       description=post_data['description'],
                                       location=post_data['location'],
                                       reporter=kwargs['user'].id)
        db.session.add(new_incident)
        db.session.commit()

        if 'files' in post_data.keys():
            for path in post_data['files']:
                new_file = models.File(path=path, incident_id=new_incident.id)
                db.session.add(new_file)

        db.session.commit()   # avoid commit 2 times

        response = new_incident.__serialize__()

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


# =====================   Register API endpoints   ==========================

incidents_view = IncidentsAPI.as_view('incidents_api')

app.add_url_rule('/api/register',
                 view_func=RegistrationAPI.as_view('registration_api'),
                 methods=['POST'])

app.add_url_rule('/api/login',
                 view_func=LoginAPI.as_view('login_api'),
                 methods=['POST'])

app.add_url_rule('/api/logout',
                 view_func=LogoutAPI.as_view('logout_api'),
                 methods=['POST'])

app.add_url_rule('/api/incidents/',
                 defaults={'incident_id': None},
                 view_func=incidents_view,
                 methods=['GET'])

app.add_url_rule('/api/incidents/',
                 view_func=incidents_view,
                 methods=['POST'])

app.add_url_rule('/api/incidents/<int:incident_id>',
                 view_func=incidents_view,
                 methods=['GET', 'PUT', 'DELETE'])

