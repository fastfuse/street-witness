
from app import app, models
from flask import request, make_response, jsonify, url_for
from collections import namedtuple


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


def login_required(func):
    """ Login required decorator.
        Additionally gives access to User object inside decorated view """
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split()[1]
        else:
            auth_token = ''

        if auth_token:
            resp = models.User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = models.User.query.filter_by(id=resp['user']).first()
                kwargs['user'] = user
                return func(*args, **kwargs)

            response = Response('Fail', resp)
            return make_response(jsonify(response._asdict())), 401

        else:
            response = Response('Fail', 'Provide a valid auth token')
            return make_response(jsonify(response._asdict())), 401

    return wrapper


def object_to_json(object):
    """ Convert DB object to RESTful json format (without unnecessary stuff) """
    object = object.__dict__
    object.pop('_sa_instance_state')
    object['url'] = url_for('incidents_api',
                            incident_id=object.pop('id'),
                            _external=True)
    if 'reporter' in object.keys():
        user = models.User.query.get(object['reporter'])
        object['reporter'] = user.username

    return object
