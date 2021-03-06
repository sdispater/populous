import sys

from builtins import range
from builtins import zip
from six import string_types as basestring


PY2 = sys.version_info[0] == 2


if PY2:
    import peloton_bloomfilters as bloomfilter
else:
    import pybloomfilter as bloomfilter


if PY2:
    from string import letters as ascii_letters
else:
    from string import ascii_letters


__all__ = [
    'ascii_letters',
    'basestring',
    'bloomfilter',
    'PY2',
    'range',
    'zip',
]
