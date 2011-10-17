#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sha, time

from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao import *
from core.lib.utils import *
from core import Environment
from core.lib.page import Page
from core.pages import *
from core.lib.session import Session
#from sets import Set


class Search:
    """
    Classe preposta alla ricerca, rimanderà quando sarà pronta alla pagina
    centrale per la visualizzazione dei risultati di fatto il form è inserito
    nella spalla sx.
    """
    def __init__(self, req):
        self.req = req
        self.path = req.environ['PATH_INFO'].split('/')

    def index(self, articles=None):
        pageData = {'file' : 'article'}
        return Page(self.req).render(pageData)

    def searchText(self):
        """ search form page """
        results = []
        produttoreResult= []
        produttoreResultLimited = []
        codiceResult= []
        codiceResultLimited = []
        denominazioneResult = []
        denominazioneResultLimited=[]
        textResult = []
        textResultLimited = []
        myListinoId = getIdlistinoFromRole(self.req)
        if not myListinoId: myListinoId = Environment.params[self.path[1]]['listinoDefault']
        defaultLimit = Environment.params[self.path[1]]['defaultLimit']
        defaultOffset = 0
        produttore =''
        codice = ''
        denominazioneVar = ''
        prezzo = ''
        testo = ''
        defaultOffsetIndex = 0

        try:
            defaultOffsetIndex = int(self.req.args.get('pag'))-1
            if defaultOffsetIndex == 0:
                defaultOffset = 0
            else:
                defaultOffset = defaultOffsetIndex * defaultLimit
            produttore = self.req.args.get('produttore')
            codice = self.req.args.get('codice')
            denominazioneVar = self.req.args.get('descrizione')
            testo = self.req.args.get('testo')
            prezzo = self.req.args.get('prezzo')
            catId = self.req.args.get('catId')
        except:
            produttore = self.req.form.get('produttore')
            codice = self.req.form.get('codice')
            denominazioneVar = self.req.form.get('descrizione')
            testo = self.req.form.get('testo')
            prezzo = self.req.form.get('prezzo')
            catId = self.req.args.get('catId')
        try :
            if catId:
                catIdResult = ListinoArticoloSl(self.req).query().join('articolo')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.id_famiglia_articolo==catId)\
                                .filter(ListinoArticoloSl.id_listino == myListinoId)\
                                .all()
                catIdResultLimited = ListinoArticoloSl(self.req).query().join('articolo')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ListinoArticoloSl.id_listino == myListinoId)\
                                .filter(ArticleSl.c.id_famiglia_articolo==catId)\
                                .all()[defaultOffset:(defaultOffset+defaultLimit)]
                resultsLen= len(catIdResult)
                results = catIdResultLimited
        except:
            pass
        try:
            if len(testo)>2:
                testo = testo.replace(' ', '%')
                textResult = ListinoArticoloSl(self.req).query().join('articolo')\
                                .filter(ListinoArticoloSl.id_listino == myListinoId)\
                                .filter(FamilySl.visible == 1)\
                                .filter(ArticleSl.denominazione.like('%'+ testo +'%')|\
                                ArticleSl.c.produttore.like('%'+testo+'%')|\
                                ArticleSl.c.codice.like('%'+ testo +'%')).all()

                textResultLimited = ListinoArticoloSl(self.req).query().join('articolo')\
                                .filter(ListinoArticoloSl.id_listino == myListinoId)\
                                .filter(FamilySl.visible == 1)\
                                .filter(ArticleSl.denominazione.like('%'+ testo +'%')|\
                                ArticleSl.c.produttore.like('%'+ testo +'%')|\
                                ArticleSl.c.codice.like('%'+ testo +'%'))\
                                .all()[defaultOffset:(defaultOffset+defaultLimit)]
                resultsLen = len(textResult)
                results = textResultLimited
        except:
            print " HO FALLITO  NELLA FUNZIONE DI RICERCA "
        try:
            if len(produttore)>2:
                produttoreResult = ArticleSl(self.req).query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.produttore.like('%'+produttore+'%')).all()
                produttoreResultLimited = ArticleSl().query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.produttore.like('%'+produttore+'%')).limit(defaultLimit).offset(defaultOffset).all()
        except:
            pass
        try:
            if len(codice)>2:
                codiceResult = ArticleSl(self.req).query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.codice.like('%'+ codice +'%')).all()
                codiceResultLimited = ArticleSl().query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.codice.like('%'+ codice +'%')).limit(defaultLimit).offset(defaultOffset).all()
        except:
            pass
        try:
            if len(denominazioneVar)>2 :

                denominazioneResult = ArticleSl(req).query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.denominazione.like('%'+ denominazioneVar +'%')).all()
                denominazioneResultLimited = ArticleSl().query().join('famiglia').filter(FamilySl.c.visible == 1).filter( ArticleSl.c.denominazione.like('%'+ denominazioneVar +'%')).limit(defaultLimit).offset(defaultOffset).all()
        except:
            pass
        #a= Set(produttoreResultLimited)
        #b = Set(codiceResultLimited)
        #c = Set(denominazioneResultLimited)

        if results:
            #d= Set(produttoreResult)
            #e = Set(codiceResult)
            #f = Set(denominazioneResult)
            giacenze = {}
            for i in results:
                qt = calcoloGiacenza(self.req, i.id_articolo)
                giacenze[i.id_articolo] = qt

            if resultsLen % Environment.params[self.path[1]]['defaultLimit'] :
                item = resultsLen/Environment.params[self.path[1]]['defaultLimit'] +1
            else:
                item = resultsLen/Environment.params[self.path[1]]['defaultLimit']
            print len(results)
            pageData = {'file' : 'article',
                        'article' : results,
                        'catId' : catId,
                        'codice' : codice,
                        'denominazioneVar' : denominazioneVar,
                        'giacenze' : giacenze,
                        'item' : item,
                        'pag' : defaultOffsetIndex,
                        'prezzo' :  prezzo,
                        'produttore' : produttore,
                        'resultsLen' : resultsLen,
                        'siteAdmin' : 'no',
                        'testo' : testo,}
            return Page(self.req).render(pageData)
        else:
            pageData = {'file' : 'errorSearch'}
            return Page(self.req).render(pageData)

