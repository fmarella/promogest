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
from core.dao.Cliente import Cliente
from core.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
from core.dao.Province import Province
from core.dao.Regioni import Regioni
#from core.session import Session
from core.lib.page import Page
import datetime


def userdetail(req, static=None, subdomain=None):
    forms = req.form.to_dict()
    args = req.args.to_dict()
    user = getUserFromId(req)
    pg = PersonaGiuridica().select(id_user=user.id)
    if not pg:
        print "Probabile cliente aggiunto da sito"
        cl = None
    else:
        cl = Cliente().getRecord(id=pg[0].id)
    province = Province().select(batchSize=None)
    regioni = Regioni().select(batchSize=None)
    if forms:
        if forms["password"] != "" and forms["password"] == forms["re_password"]:
            user.password = hashlib.md5(user.username + \
                                forms["password"]).hexdigest()

        user.pegi.nome = forms["nome"]
        user.pegi.cognome = forms["cognome"]
        user.pegi.ragione_sociale = forms["ragionesociale"]
        user.pegi.insegna = forms["insegna"]
        user.pegi.codice_fiscale = forms["codicefiscale"]
        user.pegi.partita_iva = forms["partitaiva"]
        user.pegi.id_sede_legale_provincia = int(forms["sedelegaleprovincia"])
        user.pegi.id_sede_legale_regione = int(forms["sedelegaleregione"])
        user.pegi.nazione = forms["sedelegalenazione"]
        if not cl:
            cl = Cliente()
        cl.id=pg[0].id
        cl.telefono = forms["telefono"]
        cl.fax = forms["fax"]
        cl.note = forms["note"]
        cl.persist()
        user.persist()

    pageData = {'file' : 'userDetail',
            "subdomain": subdomain,
            "forms":forms,
            "args":args,
            "user":user,
            "province": province,
            "regioni":regioni,
            "nazioni" :nationList,
            "cl":cl}
    return Page(req).render(pageData)
