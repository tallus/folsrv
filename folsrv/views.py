from flask import render_template, flash, redirect
from flask import Markup 
from folsrv import app
import datetime
import sys
import glob
from  json import JSONEncoder as jenc


@app.route("/")
@app.route('/index')
def index():
        topics = [
                {
                    'title' : 'Training Material', 
                    'body' : '''Useful reference and other training materials for new tech support interns.<br />
                    <dl><dt class=sans"><a href="/downloads/command-line.pdf">Introduction to the Command Line</a> (PDF)</dt><dd class="sans">A Free manual published by <a href="http://flossmanuals.net/">flossmanuals.net</a>. It is also available online, in HTML format at<br /> <a href="http://flossmanuals.net/command-line/">http://flossmanuals.net/command-line</a></dd></dl></dd>'''
                },
                {
                    'title' : 'upgrade-ubuntu.sh',
                    'url' : 'upgrade-ubuntu.sh',
                    'body' : '''Use this to upgrade form 10.04 to 12.04. <br>N.B. 
        This script performs a backup, so you should not do one first as it will complain. You can force it to overwrite it with the -f option. 
        <p>Steps to upgrade the script. 
        <strong> Note the following carefully:</strong>
        </p>
        <ol>
            <li>Run the script, carefully noting any instructions given</li>
            <li><strong>When prompted to reboot. DO NOT REBOOT</strong></li>
            <li>Press x, then type reboot on the command line.</li>
            <li> Rerun the script a second time to finish the process</li>
        </ol>'''
            },
            {
                'title' : 'whoopsie-disable.sh',
                'url' : 'whoopsie-disable.sh',
                'body' : 'A small shell script that will disable the annoying crash reports on 12.04'
            }
            ]
        current_version = '0.1.13'
        versions = [
                { 
                    'number' : '0.1.13',
                    'content' : ''' &laquo;Lucky Thirteen&raquo;<br />
                                <del><a href ="http://todo.freegeek.org/Ticket/Display.html?id=34487">#34487</a></del> <del><a href="http://todo.freegeek.org/Ticket/Display.html?id=32908">#32908</a></del> Hopefully fixed the bug which prevented backups when there was a space in the directory name (for reals this time).<br>
                                            Added a long list of temporary files that will be excluded from backups.<br>
                                                        Fixed a bug with adding an addendum that left off the ticket number. (Also closing <del><a href="http://todo.freegeek.org/Ticket/Display.html?id=33225">#33225</a></del>) <br>
                                                                    
                                                                                Added a -R option for read only file systems e.g. dd images.'''
            }
        ]
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
        return ''
    else:
        return jenc.encode(backups)


def get_backup_list(ticket):
    backups = gob.gob('/srv/tsbackup/*-' + ticket)
    return backups


def get_recycle_date():
    today = datetime.date.today()
    timedelta = datetime.timedelta(45)
    recycledate = today + timedelta
    return recycledate



