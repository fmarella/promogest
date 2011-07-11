# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params, workingYear, conf
from Dao import Dao
from Articolo import Articolo
from Magazzino import Magazzino
from promogest.dao.Fornitura import Fornitura
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from DaoUtils import giacenzaSel
from promogest.ui.utils import mN, posso

if posso("PW"):
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore


class Stoccaggio(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _getTotaliOperazioniMovimento(self):
        self.__dbTotaliOperazioniMovimento = giacenzaSel(year=workingYear, idMagazzino= self.id_magazzino, idArticolo=self.id_articolo)
        self.__totaliOperazioniMovimento = self.__dbTotaliOperazioniMovimento[:]

        return self.__totaliOperazioniMovimento

    def _setTotaliOperazioniMovimento(self, value):
        self.__totaliOperazioniMovimento = value

    totaliOperazioniMovimento = property(_getTotaliOperazioniMovimento,
                                         _setTotaliOperazioniMovimento)

    def _getGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totGiacenza = 0

        for t in totaliOperazioniMovimento:
            totGiacenza += (mN(t['giacenza']) or 0)
            #totGiacenza += (t[4] or 0)
        return totGiacenza

    giacenza = property(_getGiacenza, )

    def _getValoreGiacenza(self):
        totaliOperazioniMovimento = self.totaliOperazioniMovimento
        totValoreGiacenza = 0

        for t in totaliOperazioniMovimento:
            totValoreGiacenza += (t['valore'] or 0)
            #totValoreGiacenza += (t[5] or 0)
        return totValoreGiacenza

    valoreGiacenza = property(_getValoreGiacenza, )

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo= property(_denoArticolo)

    def _magazzino(self):
        if self.arti: return self.maga.denominazione
        else: return ""
    magazzino= property(_magazzino)

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear, 'mod_enable')=="yes":
        def _denominazione_gruppo_taglia(self):
            #if self.ATC: return self.ATC.denominazione or ""
            if self.arti: return self.arti.denominazione_gruppo_taglia
            else: return ""
        denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

        def _id_articolo_padre(self):
            #if self.ATC: return self.ATC.id_articolo_padre or None
            if self.arti: return self.arti.id_articolo_padre
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_gruppo_taglia(self):
            #if self.ATC: return self.ATC.id_gruppo_taglia or None
            if self.arti: return self.arti.id_gruppo_taglia
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_genere(self):
            #if self.ATC: return self.ATC.id_genere or None
            if self.arti: return self.arti.id_genere
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.arti: return self.arti.id_stagione
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.arti: return self.arti.id_anno
        id_anno = property(_id_anno)

        def _denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.arti: return self.arti.denominazione_taglia
        denominazione_taglia = property(_denominazione_taglia)

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.arti: return self.arti.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _anno(self):
            """ esempio di funzione  unita alla property """
            if self.arti: return self.arti.anno
        anno = property(_anno)

        def _stagione(self):
            """ esempio di funzione  unita alla property """
            if self.arti: return self.arti.stagione
        stagione = property(_stagione)

        def _genere(self):
            """ esempio di funzione  unita alla property """
            if self.arti: return self.arti.genere
        genere = property(_genere)

    def filter_values(self, k, v):
        if k== 'idArticolo':
            dic= {k: stoc.c.id_articolo == v}
        elif k == "idArticoloList":
            dic = {k: stoc.c.id_articolo.in_(v)}
        elif k == 'idMagazzino':
            dic = {k: stoc.c.id_magazzino == v}
        elif k == 'articolo':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.denominazione.ilike("%"+v+"%"))}
        elif k == 'codice':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.codice.ilike("%"+v+"%"))}
        elif k == 'codiceABarre':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==CodiceABarreArticolo.id_articolo, CodiceABarreArticolo.codice.ilike("%"+v+"%"))}
        elif k == 'produttore':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.produttore.ilike("%"+v+"%"))}
        elif k== 'codiceArticoloFornitoreEM':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==Fornitura.id_articolo, Fornitura.codice_articolo_fornitore == v)}
        elif k== 'codiceArticoloFornitore':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==Fornitura.id_articolo, Fornitura.codice_articolo_fornitore.ilike("%"+v+"%"))}
        elif k=='idFamiglia':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id_famiglia_articolo ==v)}
        elif k == 'idCategoria':
            dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id_categoria_articolo ==v)}
        elif k == 'idStato':
            dic= {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id_stato_articolo == v)}
        elif k == 'cancellato':
            dic = {k: or_(and_(stoc.c.id_articolo==Articolo.id, Articolo.cancellato != v))}
        elif posso("PW"):
            if k == 'figliTagliaColore':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre==None)}
            elif k == 'idTaglia':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_taglia==v)}
            elif k == 'idModello':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_modello==v)}
            elif k == 'idGruppoTaglia':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_gruppo_taglia ==v)}
            elif k == 'padriTagliaColore':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre!=None)}
            elif k == 'idColore':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_colore ==v)}
            elif k == 'idStagione':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_stagione ==v)}
            elif k == 'idAnno':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_anno == v)}
            elif k == 'idGenere':
                dic = {k: and_(stoc.c.id_articolo==Articolo.id, Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_genere ==v)}
        return  dic[k]


articolo=Table('articolo', params['metadata'], schema = params['schema'], autoload=True)
stoc=Table('stoccaggio', params['metadata'], schema = params['schema'], autoload=True)

std_mapper = mapper(Stoccaggio, stoc, properties={
        "arti": relation(Articolo, primaryjoin=
                stoc.c.id_articolo==articolo.c.id, backref="stoccaggio"),
        "maga": relation(Magazzino, primaryjoin=
                stoc.c.id_magazzino==Magazzino.id, backref="stoccaggio"),
        }, order_by=stoc.c.id)
