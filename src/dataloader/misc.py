import json
import re
from pathlib import Path
from typing import Union, Dict, List, Tuple

import yaml


from dateutil import parser
from dateutil.parser import ParserError
from datetime import date, time, datetime


def parser_wrap(func):
    """ A wrap to unify error handling of parsers """

    def wrapper(*args, **kwargs):
        value = str(kwargs.get("v"))
        default = kwargs.get("d", None)

        # None values are universal
        if value.lower().replace(' ', '') in ('null', 'none', 'nan', '-', 'unknown'):
            return default

        try:
            return func(*args, **kwargs)
        except (ValueError, ParserError):
            return default

    return wrapper


class StrParser:
    """ A list of type parsers """

    @parser_wrap
    def str(self, *, v, d=""):
        return str(v).strip()

    @parser_wrap
    def bool(self, *, v, d=None) -> bool:
        if type(v) == bool:
            return v
        elif v.lower().replace(' ', '') in ('false', '0', 'f', 'n', 'no', 'nope', 'none', 'nan', 'not'):
            return False
        return True

    @parser_wrap
    def date(self, *, v: str, d=None) -> date:
        return parser.parse(v).date()

    @parser_wrap
    def time(self, *, v: str, d=None) -> time:
        return parser.parse(v).time()

    @parser_wrap
    def datetime(self, *, v: str, d=None) -> datetime:
        return parser.parse(v)

    @parser_wrap
    def float(self, *, v: str, d=None) -> float:
        return float(v)

    @parser_wrap
    def int(self, *, v: str, d=None) -> int:
        return int(v)

    @parser_wrap
    def doi(self, *, v: str, d=None) -> Tuple[str, str]:
        pattern = re.compile(r"^.+href=\"(.+)\"\s*id=\"(.+)\">.+$")
        res = pattern.match(v)
        if res:
            return res.group(1), res.group(2)
        return "", ""

    @parser_wrap
    def doi2(self, *, v: str, d=None) -> Tuple[str, str]:
        pattern = re.compile(r"^.+href=\"(.+)\"\s*>(.+)</a>$")
        res = pattern.match(v)
        if res:
            return res.group(1), res.group(2)
        return "", ""

    @parser_wrap
    def suid(self, *, v, d="") -> str:
        return Path(v).name

    @staticmethod
    def load(location: Path) -> Union[Dict, List]:
        """ Load a dict type file (json, yaml, toml)"""
        with location.open() as fp:
            if location.suffix == '.json':
                return json.load(fp)
            elif location.suffix in ('.yaml', 'yml'):
                return yaml.load(fp, Loader=yaml.SafeLoader)
            elif location.suffix in ('.txt', '.list'):
                return [line.strip() for line in fp.readlines()]
            else:
                raise ValueError('Not a known file type !!!')
