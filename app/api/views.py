# -*- coding: utf-8 -*-

from . import api_blueprint
from app import db, models, bcrypt, utils
from flask import request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime


class IncidentsAPI(MethodView):
    """ Incidents Resourse """

    decorators = [utils.login_required]

    def get(self, incident_id, **kwargs):
        """ Get all incidents or single incident by ID """
        if incident_id:
            incident_query = models.Incident.query.get_or_404(incident_id)
            incident = incident_query.serialize()

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
                incidents.append(item.serialize())

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

        db.session.commit()   # avoid commiting 2 times

        response = new_incident.serialize()

        return make_response(jsonify(response)), 201


# =====================   Register API endpoints   ==========================

incidents_view = IncidentsAPI.as_view('incidents_api')

api_blueprint.add_url_rule('/incidents/',
                           defaults={'incident_id': None},
                           view_func=incidents_view,
                           methods=['GET'])

api_blueprint.add_url_rule('/incidents/',
                           view_func=incidents_view,
                           methods=['POST'])

api_blueprint.add_url_rule('/incidents/<int:incident_id>',
                           view_func=incidents_view,
                           methods=['GET', 'PUT', 'DELETE'])
