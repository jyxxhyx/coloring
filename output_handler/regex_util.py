"""
Code borrowed from grblogtools
"""

import datetime
import re

int_regex = re.compile(r"[-+]?\d+$")
float_regex = re.compile(r"[-+]?((\d*\.\d+)|(\d+\.?))([Ee][+-]?\d+)?$")
percentage_regex = re.compile(r"[-+]?((\d*\.\d+)|(\d+\.?))([Ee][+-]?\d+)?%$")
date_time_regex = re.compile(r"\D+\s\D+\s\d+\s\d+:\d+:\d+\s\d{4}")


def convert_data_types(value):
    """Convert the given value string to the type it matches."""
    if value is None or value == "-":
        # Commonly used sentinel for a missing value in log tables
        return None
    elif int_regex.match(value):
        return int(value)
    elif float_regex.match(value):
        return float(value)
    elif percentage_regex.match(value):
        return float(value.rstrip("%")) / 100
    elif date_time_regex.match(value):
        return datetime.datetime.strptime(value, "%a %b %d %H:%M:%S %Y")
    else:
        return value


def typeconvert_groupdict(match):
    """Return the groupdict of a regex match with type converted values."""
    return {k: convert_data_types(v) for k, v in match.groupdict().items()}
