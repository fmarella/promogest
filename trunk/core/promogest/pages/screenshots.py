#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>



from sqlalchemy.orm import *
from core import Environment
from core.lib.page import Page


class ScreenShots(object):

    def __init__(self, req):
        self.path = req.environ['PATH_INFO'].split('/')
        self.req = req

    def show(self):
        """
        screenshots
        """
        pageData = {'file' : 'screenshots'}
        return Page(self.req).render(pageData)


