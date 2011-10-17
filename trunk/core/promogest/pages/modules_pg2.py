#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Modulo import Modulo
from core.dao.ModuliAbbinati import ModuliAbbinati
from core.dao.VideoModulo import VideoModulo
from core.lib.utils import *
from core.pages import *
from core.lib.page import Page
from core.lib.unipath.path import *


def moduleDetailByDenomination(req,subdomain=None, denomination=None):
    module = Modulo(req=req).select(permalink=denomination, active=True)
    if module:
        modulia = ModuliAbbinati().select(idModulo = module[0].id)
        moduliassociati = []
        for modd in modulia:
            moduliassociati.append(Modulo().getRecord(id=modd.id_modulo_abbinato))
        mo = module[0]
        mo.clicks = int(mo.clicks or 0)+1
        mo.persist()
        mediaAbbinati = VideoModulo().select(idModulo=module[0].id)
        pageData = {'file' : 'module_detail',
                    "subdomain": subdomain,
                    "mediaAbbinati": mediaAbbinati,
                    'moduleD' : module[0],
                    'moduliassociati' :moduliassociati,
}
        return Page(req).render(pageData)
    else:
        pageData = {'file' : 'not_found',
}
        return Page(req).render(pageData)

def modules_list(req, static=None, subdomain=""):
    modules = Modulo().select(batchSize=None, active=True)
    pageData = {'file' : 'moduliList',
                "subdomain": subdomain,
                "modules" :modules}
    return Page(req).render(pageData)
