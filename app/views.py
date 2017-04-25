
# -*- coding: utf-8 -*-

import copy
from app import app, db, admin, models
from flask import (request,
                   redirect,
                   render_template,
                   make_response,
                   url_for,
                   json)
from flask.views import MethodView
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from wtforms import fields


# ===========================  Help functions   ==============================

def register_api(view, endpoint, url, pk='id', pk_type='any'):
    """ Function to simplify registration of API views (based on MethodView) """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])

    app.add_url_rule('{url}<{pk_type}:{pk}>'.format(url=url,
                                                    pk_type=pk_type,
                                                    pk=pk),
                     view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


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


# =============================   Index page   ==============================

@app.route('/')
def index():
    """ Only renders index page """
    return render_template('index.html')


# ==============================   API   ====================================

class IncidentsAPI(MethodView):

    def get(self, incident_id):
        """ Get all incidents or single incident by ID """

        # add 404 error if no such item
        # jsonify returns response obj

        if incident_id:
            incident_query = models.Incident.query.get_or_404(incident_id)

            incident = {}
            incident['id'] = incident_query.id
            incident['title'] = incident_query.title
            incident['description'] = incident_query.description
            incident['location'] = incident_query.location
            incident['timestamp'] = incident_query.timestamp
            incident['status'] = incident_query.status

            return make_response(json.jsonify(incident))

        else:
            status = request.args.get('status', None)
            if status:
                incidents_query = models.Incident.query.\
                    filter_by(status=status).all()

            else:
                incidents_query = models.Incident.query.all()

            incidents = []
            for item in incidents_query:
                incident = {}
                incident['id'] = item.id
                incident['title'] = item.title
                incident['description'] = item.description
                incident['location'] = item.location
                incident['timestamp'] = item.timestamp
                incident['status'] = item.status
                incidents.append(incident)

            return make_response(json.jsonify(incidents=incidents,
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

        return make_response(json.jsonify(response), 201)


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
                return make_response(json.jsonify(response_object)), 201

            except Exception as e:
                response_object = {
                    'status': 'Fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(json.jsonify(response_object)), 401

        else:
            response_object = {
                'status': 'Fail',
                'message': 'User already exists. Please Log in.',
            }

            return make_response(json.jsonify(response_object)), 202





# =====================   Register API endpoints   ==========================

register_api(IncidentsAPI, 'incidents_api', '/api/incidents/',
             pk='incident_id', pk_type='int')

register_api(RegistrationAPI, 'registration_api', '/api/register') # /api/auth ?
