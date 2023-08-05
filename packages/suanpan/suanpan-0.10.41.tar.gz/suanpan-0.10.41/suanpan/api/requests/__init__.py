# coding=utf-8
from __future__ import absolute_import, print_function

import base64
import hashlib
import hmac

import requests

from suanpan import error, g, utils
from suanpan.log import logger


def signatureV1(secret, data):
    h = hmac.new(utils.encode(secret), utils.encode(data), hashlib.sha1)
    return utils.decode(base64.b64encode(utils.encode(h.digest())))


def defaultHeaders():
    if not g.userIdHeaderField:
        raise error.ApiError("UserIdHeaderField not set")
    return {
        g.userIdHeaderField: g.userId,
        g.userSignatureHeaderField: signatureV1(g.accessSecret, g.userId),
        g.userSignVersionHeaderField: "v1",
    }


def session():
    sess = requests.Session()
    sess.headers.update(defaultHeaders())
    return sess


def request(method, url, *args, **kwargs):
    sess = session()
    func = getattr(sess, method)
    rep = func(url, *args, **kwargs)
    rep.raise_for_status()
    logger.debug(f"{method.upper()} - {url} - {rep.content}")
    result = rep.json()
    if not result.get("success", True):
        raise error.ApiError(f"Request failed {result}")
    return result


def get(url, *args, **kwargs):
    return request("get", url, *args, **kwargs)


def post(url, *args, **kwargs):
    return request("post", url, *args, **kwargs)


def put(url, *args, **kwargs):
    return request("put", url, *args, **kwargs)


def delete(url, *args, **kwargs):
    return request("delete", url, *args, **kwargs)
