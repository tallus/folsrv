from flask import render_template, flash, redirect, jsonify, Markup
from folsrv import app
import datetime
import glob
import os.path
from ast import literal_eval as ast_eval


@app.route("/")
@app.route('/index')
def index():
        # for our index page read in files containing  python lists of dicts
        # for parsing by jinja2 per templates/index.html
        # note this allows embedded html(+js etc) i.e. passed to jinja2
        # by being piped through safe, so only good for static files

        f = open('folsrv/src/topics', 'r')
        topic_txt = f.read()
        topics = ast_eval(topic_txt)
        f.close()
        
        f = open('folsrv/src/fg_tstools', 'r')
        ver_txt = f.read()
        versions = ast_eval(ver_txt)
        f.close()
        
        # get current version no
        latest = versions[0]
        current_version = latest['number']

        recycle_date = get_recycle_date()

        return render_template("index.html", recycle_date = recycle_date, topics = topics, current_version = current_version, versions = versions)


# for urls of form /ticket/[ticket_no] return space separated list 
@app.route("/ticket/<path:ticket_no>")
def show_ticket(ticket_no):
    backups = get_backup_list(ticket_no)
    if not backups:
        return ''
    else:
        return ' '.join(backups)


# for urls of form /json/[ticket_no] return json encoded list 
@app.route("/json/<path:ticket_no>")
def json_ticket(ticket_no):
    backups = get_backup_list(ticket_no)
    if not backups:
        return jsonify(backups=[])
    else:
        return jsonify(backups=backups)


def get_backup_list(ticket):
    backups = []
    for f in glob.glob('/srv/tsbackup/*-' + ticket + '*'):
            backups.append(os.path.basename(f))
    return backups


def get_recycle_date():
    today = datetime.date.today()
    timedelta = datetime.timedelta(45)
    recycledate = today + timedelta
    return recycledate
