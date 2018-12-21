# -*- coding: utf-8 -*-

from flask import render_template, redirect, session, request, url_for
from app import app
from form import LoginForm, EntranceForm
from app import execute
from werkzeug.utils import secure_filename
import util
import os
from group.groupOp import GroupOp

@app.route('/')
@app.route('/index')
def index():
    group_list = GroupOp.getGroupList()
    return render_template('index.html', group_list = group_list)

@app.route('/abstract')
@app.route('/abstract/<int:groupid>')
def abstract(groupid):
    session['groupid'] = groupid
    return render_template('abstract.html', groupid = groupid)

@app.route('/location/<int:groupid>')
def location(groupid):
    node_json, edge_json = GroupOp.getLocation(groupid)
    return render_template('location.html', node_json=node_json, edge_json=edge_json, groupid=groupid)

@app.route('/reduction/<int:groupid>')
def reduction(groupid):
    sms_info = GroupOp.getSMSList(groupid)

    return render_template('session.html', groupid = groupid, sms_info = sms_info)

@app.route('/network/<groupid>')
def network(groupid):
    return render_template('network.html', groupid = groupid)

@app.route('/management')
def management():
    return render_template('management.html')

@app.route('/group', methods = ['GET', 'POST'])
def group():
    form = EntranceForm()
    if form.validate_on_submit():
        filename = ''
        if request.files.has_key('file'):
            file = request.files['file']
            if file and util.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        groupid = execute.execute(form.groupName.data, form.keyWord.data, form.startTime.data, form.endTime.data, form.location.data, filename)
        session['groupid'] = groupid
        return redirect(url_for('location', groupid=groupid))
    group_list = GroupOp.getGroupList()

    if session.get('groupid') != None:
        return render_template('group.html', form=form, group_list=group_list, groupid=session['groupid'])
    else:
        return render_template('group.html', form=form, group_list=group_list)

