"""Module for common file IO methods"""
import json
import logging
from attrdict import AttrDict

logger = logging.getLogger(__name__)


def read_json_to_attrdict(filepath):
    """Read json object into an attrdict

    Args:
        filepath (str): Absolute path to file

    Return (AttrDict): File contents
    """

    with open(filepath, 'r') as json_file:
        dict_ = json.load(json_file)
    return AttrDict(dict_)


def epa_data_from_xls(self):
    """Fulhack to get data from Johroge's excel sheet"""
