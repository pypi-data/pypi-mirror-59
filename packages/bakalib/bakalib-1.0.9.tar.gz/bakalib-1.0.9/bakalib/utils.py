"""
util
====
"""

__all__ = (
    "BakalibError",
    "cache",
    "data_dir",
    "_logger",
    "request",
)

import datetime as _datetime
import inspect as _inspect
import logging as _logging
import pathlib as _pathlib
import sys as _sys

import cachetools as _cachetools
from gevent import monkey as _monkey

_monkey.patch_all(thread=False, select=False)

import requests as _requests
import urllib3 as _urllib3
import xmltodict as _xmltodict


_urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)

data_dir = _pathlib.Path(__file__).parent.joinpath("data")
_log_dir = _pathlib.Path(_pathlib.Path.home() / ".bakalib")
_log_file = _pathlib.Path(
    _log_dir / (_datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")
)

if not _log_dir.is_dir():
    _log_dir.mkdir()
else:
    _logs = [f for f in _log_dir.iterdir()]
    _logs.sort()
    while len(_logs) > 5:
        _logs[0].unlink()
        _logs.pop(0)

_log_file.touch()


def _setup_logger(name):
    formatter = _logging.Formatter(
        fmt="%(asctime)s — %(name)s — %(levelname)s — %(message)s — %(funcName)s:%(lineno)d"
    )
    handler = _logging.FileHandler(_log_file, mode="a")
    handler.setFormatter(formatter)
    logger = _logging.getLogger(name)
    logger.setLevel(_logging.DEBUG)
    logger.addHandler(handler)
    return logger


_logger = _setup_logger("default")

cache = _cachetools.TTLCache(32, 300)


@_cachetools.cached(cache)
def request(url: str, **kwargs: str) -> dict:
    """
    Make a GET request to school URL.\n
    Module names are available at `https://github.com/bakalari-api/bakalari-api/tree/master/moduly`.
    >>> # Valid types of requests
    >>> request("https://example.com/login.aspx", gethx="Username123")
    >>> request("https://example.com/login.aspx", hx="token1234=", pm="module_name", pmd="20191219") # pmd is optional
    """

    resp: _requests.Response = _requests.get(url=url, params=kwargs, verify=False)
    parsed: dict = _xmltodict.parse(resp.content)
    results: dict = parsed.get("results")

    try:
        res: dict = results.get("res")
        result: dict = results.get("result")
    except AttributeError as e:
        log_args: dict = kwargs.copy()
        log_args.pop(k="hx", d=None)
        _logger.error(log_args)

    comp: str = res if res else result

    if not comp == "01":
        raise BakalibError("Received response is invalid")

    return results


class BakalibError(Exception):
    pass
