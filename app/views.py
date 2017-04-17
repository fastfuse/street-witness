
# -*- coding: utf-8 -*-

from app import app, admin, db
from flask import (request,
                   redirect,
                   render_template,
                   make_response,
                   url_for,
                   json)
from flask.views import MethodView
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
from flask_admin.contrib.pymongo import ModelView
from wtforms import form, fields

# sudo service mongod start
# sudo service mongod stop


# ===========================  Help functions   ==============================

def register_api(view, endpoint, url, pk='id', pk_type='any'):
    """Function to simplify registration of API views (based on MethodView)"""
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])

    app.add_url_rule('{url}<{pk_type}:{pk}>'.format(url=url,
                                                    pk_type=pk_type,
                                                    pk=pk),
                         view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


def jsonify_mongo_obj(obj):
    """Function to dump mongo objects (with safe convert ObectId)"""
    pass 

# ============================   Admin views   ================================

class IncidentForm(form.Form):
    title = fields.StringField('Title')
    description = fields.TextAreaField('Description')
    location = fields.StringField('Location')
    tag = fields.StringField('Tag')
    status = fields.SelectField('Status', choices=[('active', 'Активний'),
                                                   ('archived', 'Архівний')])
    date = fields.DateTimeField('Date')


class IncidentView(ModelView):
    column_list = ('title', 'description', 'location', 'status', 'tag', 'date')
    form = IncidentForm


admin.add_view(IncidentView(db['incidents']))

# =================================================================

@app.route('/')
def index():
    """Only renders index page"""
    return render_template('index.html')

# ==============================   API   ======================================

class IncidentsAPI(MethodView):

    def get(self, incident_id):
        """Get all incidents or single incident by ID"""

        # get status from query string?
        # e.g.: /api/incidents?status=all/status=active?
        # request.args.get('key', 'None') or request.query_string

        # add 404 error if no such item

        # refactor json load/dump/jsonify
        # jsonify returns response obj

        if incident_id:
            incidents = db.incidents.find_one({'_id': ObjectId(incident_id)})
            incidents = json.loads(json_util.dumps(incidents))

            return make_response(json.jsonify(incidents))

        else:
            status = request.args.get('status', '')
            if status:
                incidents = db.incidents.find({'status': status})
            else:
                incidents = db.incidents.find()

            response = {"data_count": incidents.count(),
                        "data": json.loads(json_util.dumps(incidents))}

            return make_response(json.jsonify(response))

    def post(self):
        """Add new incident"""

        new_incident = request.json
        new_incident['date'] = datetime.now()
        new_incident['status'] = 'active'
        # print(new_incident)
        created = db.incidents.insert_one(new_incident)

        return make_response(json_util.dumps(new_incident), 201)

    def delete(self):
        """Delete all incidents - for dev purposes only"""

        result = mongo.db.incidents.delete_many({'tag': 'test2'})

        return make_response(json.jsonify({'Deleted': result.deleted_count}))



register_api(IncidentsAPI, 'incidents_api', '/api/incidents/',
             pk='incident_id', pk_type='string')