# -*- coding: utf-8 -*-

import hashlib


def get_md5(url):
    if isinstance(url, unicode):
        url = url.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(url)
    return md5.hexdigest()
