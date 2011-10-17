#-*- coding: utf-8 -*-
#
#Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Servizio import Servizio
from core.lib.utils import *
from core.pages import *
from core.lib.page import Page
from core.lib.unipath.path import *


def serviceDetailByDenomination(req,subdomain=None, denomination=None):
    service = Servizio(req=req).select(permalink=denomination, active=True)
    if service:
        mo = service[0]
        mo.clicks = int(mo.clicks or 0)+1
        mo.persist()
        pageData = {'file' : 'service_detail',
                    "subdomain": subdomain,
                    'serviceD' : service[0],
}
        return Page(req).render(pageData)
    else:
        pageData = {'file' : 'not_found',
}
        return Page(req).render(pageData)


def services_list(req, static=None, subdomain=""):
    services = Servizio().select(batchSize=None, active=True)
    pageData = {'file' : 'serviziList',
                "subdomain": subdomain,
                "services" :services,
}
    return Page(req).render(pageData)
