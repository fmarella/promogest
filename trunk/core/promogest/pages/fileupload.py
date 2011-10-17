#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from core.lib.page import Page
from core.lib.utils import *

def fileupload(req, subdomain=None, action=None):
    """
    Home page Elinux
    """
    ids = req.args.get("id")
    part = req.args.get("part")
    pageData = {'file' : 'fileupload',
                "subdomain": addSlash(subdomain),
                "part":part,
                "id" :ids
}
    return Page(req).render(pageData)
