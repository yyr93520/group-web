# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import DataRequired
import util

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EntranceForm(Form):
    groupName = StringField('群体名称', validators=[DataRequired()])
    startTime = DateTimeField('开始时间', format='%Y-%m-%d %H:%M:%S')
    endTime = DateTimeField('结束时间', format='%Y-%m-%d %H:%M:%S')
    keyWord = StringField('关键词', validators=[DataRequired()])
    location = SelectField('地域', choices=util.loc_list())