# -*- coding: utf-8 -*-

from flask import Blueprint


dashboard_blueprint = Blueprint('dasboard_blueprint', __name__)
                                # template_folder='app/templates')

from . import views
