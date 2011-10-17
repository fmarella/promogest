#-*- coding: utf-8 -*-
#
# Promogest -Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import hashlib
from core import Environment
from core.lib.utils import *
from core.dao.User import User
#from core.dao.Canone import Canone
#from core.dao.Servizio import Servizio
#from core.dao.UserModule import UserModule
#from core.dao.UserService import UserService
#from core.dao.ClientProfile import ClientProfile
#from core.session import Session
from core.lib.page import Page
import datetime


def userClientInfo(req, static=None, subdomain=None):

    user = getUserFromId(req)
    userservice = UserService().select(idUser = user.id, batchSize=None)
    usermodule = UserModule().select(idUser = user.id, batchSize=None)
    canoni = Canone().select(idUser = user.id, batchSize=None)
    clienteprofile = ClientProfile().select(idUser = user.id,batchSize=None)
    pageData = {'file' : 'userClientInfo',
            "subdomain": subdomain,
            "user":user,
            "canoni": canoni,
            'usermodule':usermodule,
            'userservice':userservice,
            "clienteprofile": clienteprofile
            }
    return Page(req).render(pageData)
