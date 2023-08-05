# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os


def polyaxon_user_path():
    base_path = os.path.expanduser('~')
    if not os.access(base_path, os.W_OK):
        base_path = '/tmp'

    return os.path.join(base_path, '.polyaxon')
