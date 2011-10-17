# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from core import Environment
from core.pages.modules.sla2pdf.sla2pdf import *
from core.lib.utils import *
from core.pages import views

#MODULES_NAME = "sla2pdf"
#MODULES_FOR_EXPORT = []
#GUI_DIR = getattr(Environment.conf.Project, 'cartella_moduli', 'core/pages/modules')+'/sla2pdf/gui/'
#START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
#START_CALL = None                              # of this call in a separated Thread

#@expose("/sla2pdf")
#def sla2pdd(req, subdomain=""):
#    return sla2pdff(req, static="sla2pdf", subdomain=subdomain)
#setattr(views, "sla2pdd",sla2pdd )
