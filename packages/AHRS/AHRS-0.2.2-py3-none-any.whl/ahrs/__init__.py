# -*- coding: utf-8 -*-
"""
AHRS
====

The versioning follows the principles of Semantic Versioning as specified in
https://semver.org

"""

from . import common
from . import filters
from . import utils
from .common.quaternion import Quaternion
from .versioning import get_version

__version__ = get_version()
