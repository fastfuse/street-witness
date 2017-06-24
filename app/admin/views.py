# -*- coding: utf-8 -*-

from flask import Blueprint
from app import db, admin, models
from flask_admin.contrib.sqla import ModelView
from wtforms import fields


class IncidentsView(ModelView):
    """Overwrites model view to make admin more useful"""
    form_choices = {'status': [('pending', 'Очікує'),
                               ('active', 'Активний'),
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
