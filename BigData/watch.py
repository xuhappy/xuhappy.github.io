from bottle import route, run, template, get, post
import sh
import logging

import os
from os import path

CWD = path.dirname(path.abspath(__file__))
os.chdir(CWD)
LOGFILE = path.join(CWD, 'update.log')
logging.basicConfig(level=logging.DEBUG, filename=LOGFILE)

def refresh_website():
    ret = '\n---\n'.join([
        str(sh.git('pull')),
        str(sh.bash('sync.sh'))
    ])
    logging.info('%s', ret)
    return ret

@get('/')
def index():
    ret = refresh_website()
    return template('OK\n' + str(ret))

@post('/')
def index():
    ret = refresh_website()
    return template('OK\n' + str(ret))

logging.info('start to watch')
run(host='0.0.0.0', port=1943)

