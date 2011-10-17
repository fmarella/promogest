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

from sqlalchemy.orm import *
from core.lib.utils import Response, Request , RedirectResponse
from core import Environment
from core.pages import *
from core.lib.session import Session
#from sets import Set


class SearchAdvanced(object):
    """
    CLasse preposta alla ricerca, rimanderà quando sarà pronta alla pagina
    centrale per la visualizzazione dei risultati di fatto il form è inserito
    nella spalla sx.
    """
    def __init__(self, req):
        loader = TemplateLoader([Environment.templates_dir])
        self.path = req.environ['PATH_INFO'].split('/')
        self.tmpl = loader.load( self.path[1] + '/index.html')
        self.auth = Session().control(req)
        self.itemsStaticMenu = StaticMenuAction(req).index(req, embedded=True)
        self.rowsCompany= Login(req).index(req, embedded=True)


    def index(self,req, level=None, embedded=None, articles=None):
        if embedded:
            return ('ok')
        else:
            stream = self.tmpl.generate(
                    file='searchAdvancedForm',
                    rowsFamily=Environment.rowsFamily,
                    rowsCompany = self.rowsCompany,
                    itemsStaticMenu = self.itemsStaticMenu,
                    subdomainUrl=Environment.subdomainUrl,
                    path =self.path,
                    level=level)
            return Response(stream.render('xhtml'))

    def searchText(self,req, level=None):
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

        defaultLimit = Environment.defaultLimit
        defaultOffset = 0
        produttore =''
        codice = ''
        denominazioneVar = ''
        prezzo = ''
        testo = ''
        resultsLen = 0

        try:
            defaultOffsetIndex = int(req.args.get('defaultOffset'))
            if defaultOffsetIndex == 0:
                defaultOffset = 0
            else:
                defaultOffset = defaultOffsetIndex * defaultLimit
            produttore =req.args.get('produttore')
            codice = req.args.get('codice')
            denominazioneVar = req.args.get('descrizione')
            testo = req.args.get('testo')
            prezzo = req.args.get('prezzo')
            catId = req.args.get('catId')
        except:
            produttore =req.form.get('produttore')
            codice = req.form.get('codice')
            denominazioneVar = req.form.get('descrizione')
            testo = req.form.get('testo')
            prezzo = req.form.get('prezzo')
            catId = req.args.get('catId')

        try :
            if catId:
                catIdResult = ArticleSl().query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.id_famiglia_articolo==catId).all()
                catIdResultLimited = ArticleSl().query().join('famiglia').filter(FamilySl.c.visible == 1).filter(ArticleSl.c.id_famiglia_articolo==catId).limit(defaultLimit).offset(defaultOffset).all()
                resultsLen= len(catIdResult)
                results = catIdResultLimited
        except:
            pass
        try:
            if len(testo)>2:
                testo = testo.replace(' ', '%')
                textResult = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.denominazione.like('%'+ testo +'%')|\
                                ArticleSl.c.produttore.like('%'+testo+'%')|\
                                ArticleSl.c.codice.like('%'+ testo +'%')).all()
                textResultLimited = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.denominazione.like('%'+ testo +'%')|\
                                ArticleSl.c.produttore.like('%'+ testo +'%')| \
                                ArticleSl.c.codice.like('%'+ testo +'%'))\
                                .limit(defaultLimit)\
                                .offset(defaultOffset)\
                                .all()
                resultsLen = len(textResult)
                results = textResultLimited
        except:
            pass
        try:
            if len(produttore)>2:
                produttoreResult = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.produttore.like('%'+produttore+'%'))\
                                .all()
                produttoreResultLimited = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.produttore.like('%'+produttore+'%'))\
                                .limit(defaultLimit)\
                                .offset(defaultOffset)\
                                .all()
                resultsLen = resultsLen + len(produttoreResult)
                results = results + produttoreResultLimited

        except:
            pass
        try:
            if len(codice)>2:
                codiceResult = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.codice.like('%'+ codice +'%'))\
                                .all()
                codiceResultLimited = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.codice.like('%'+ codice +'%'))\
                                .limit(defaultLimit)\
                                .offset(defaultOffset)\
                                .all()
                resultsLen = resultsLen + len(codiceResultesult)
                results = results + codiceResultLimited
        except:
            pass
        try:
            if len(denominazioneVar)>2 :
                denominazioneResult = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter(ArticleSl.c.denominazione.like('%'+ denominazioneVar +'%'))\
                                .all()
                denominazioneResultLimited = ArticleSl().query().join('famiglia')\
                                .filter(FamilySl.c.visible == 1)\
                                .filter( ArticleSl.c.denominazione.like('%'+ denominazioneVar +'%'))\
                                .limit(defaultLimit)\
                                .offset(defaultOffset)\
                                .all()
                resultsLen = resultsLen + len(denominazioneResult)
                results = results + denominazioneResultLimited
        except:
            pass
        #a= Set(produttoreResultLimited)
        #b = Set(codiceResultLimited)
        #c = Set(denominazioneResultLimited)

        if results:
            #d= Set(produttoreResult)
            #e = Set(codiceResult)
            #f = Set(denominazioneResult)

            if resultsLen % Environment.defaultLimit :
                item = resultsLen/Environment.defaultLimit +1
            else:
                item = resultsLen/Environment.defaultLimit
            stream = self.tmpl.generate(file='article',
                    auth=self.auth,
                    article = results,
                    path = self.path,
                    item=item,
                    itemsStaticMenu = self.itemsStaticMenu,
                    rowsFamily=Environment.rowsFamily,
                    rowsCompany = self.rowsCompany,
                    resultsLen=resultsLen,
                    produttore =produttore,
                    codice = codice,
                    denominazioneVar = denominazioneVar,
                    testo = testo,
                    catId=catId,
                    prezzo = prezzo,
                    subdomainUrl=Environment.subdomainUrl,
                    level=level)
            return Response(stream.render('xhtml'))
        else:
            stream = self.tmpl.generate(file='errorSearch',
                        auth=self.auth,
                        path = self.path,
                        rowsFamily=Environment.rowsFamily,
                        rowsCompany = self.rowsCompany,
                        itemsStaticMenu = self.itemsStaticMenu,
                        subdomainUrl=Environment.subdomainUrl,
                        level=level)
            return Response(stream.render('xhtml'))

