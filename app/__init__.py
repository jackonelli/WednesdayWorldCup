import os
from flask import Flask
import logging
from datetime import datetime
from util.log import setup_logger
from config import Config

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object(Config)
settings = app.config['SETTINGS']

logger = logging.getLogger(__name__)
log_file = '{}.log'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
setup_logger(log_path=os.path.join(basedir, settings.logdir,  log_file))

from app import routes
