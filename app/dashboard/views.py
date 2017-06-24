# -*- coding: utf-8 -*-

from . import dashboard_blueprint
from flask import request, render_template, make_response, jsonify
from app import db, models, bcrypt, utils


@dashboard_blueprint.route('/')
@dashboard_blueprint.route('/dashboard')
def index():
    """ Only renders dashboard (index) page """
    return render_template('index.html')
