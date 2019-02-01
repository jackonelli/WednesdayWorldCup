"""Module for common file IO methods"""
import os
import json
import logging
from attrdict import AttrDict
from collections import OrderedDict
from xlrd import open_workbook

logger = logging.getLogger(__name__)


def read_json_to_attrdict(filepath):
    """Read JSON file into an attrdict

    TODO: Remove ordered, do not remember why it's there

    Args:
        filepath (str): Absolute path to file

    Returns:
        (AttrDict): File contents
    """

    if os.path.exists(filepath):
        _, ext = os.path.splitext(filepath)
        if ext == '.json':
            print(filepath)
            with open(filepath, 'r') as json_file:
                dict_ = json.load(json_file, object_pairs_hook=OrderedDict)
            return AttrDict(dict_)
        else:
            logger.error('Not JSON file: {}'.format(filepath))
    else:
        logger.error('Could not open path: {}'.format(filepath))


def write_dict_to_json(dict_, filepath, sort_keys=True, indent=2):
    """Write dict to JSON file

    Args:

        filepath (str): Absolute path to file
        dict_ (dict): data
    """
    _, ext = os.path.splitext(filepath)
    if ext == '.json':
        dir_ = os.path.basename(filepath)
        if not os.path.exists(dir_):
            os.makedirs(dir_)

        if os.path.exists(filepath):
            os.remove(filepath)
            logger.warning('Overwriting file {}'.format(filepath))
        with open(filepath, 'w') as json_file:
            json.dump(dict_, json_file, sort_keys=sort_keys, indent=indent)

    else:
        logger.error('Not JSON file: {}'.format(filepath))


def read_xls_to_class(filepath):
    """Read Excel to python workbook object

    Args:
        filepath (str): Absolute path to file

    Returns:
        (Workbook): File contents
    """
    if os.path.exists(filepath):
        _, ext = os.path.splitext(filepath)
        if ext == '.xls':
            return open_workbook(filepath)
        else:
            logger.error('Not excel file: {}'.format(filepath))
    else:
        logger.error('Could not open path: {}'.format(filepath))
