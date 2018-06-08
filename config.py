import os
from util.io import read_json_to_attrdict

basedir = os.path.abspath(os.path.dirname(__file__))
META_SETTINGS = 'settings/meta.json'


class Config(object):
    SETTINGS = read_json_to_attrdict(os.path.join(basedir, META_SETTINGS))
    ROOT = basedir
