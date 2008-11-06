# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Multiplo import Multiplo
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.dao.Fornitore import Fornitore
from promogest.dao.Articolo import Articolo
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento

class Fornitura(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def _getScontiFornitura(self):
        self.__dbScontiFornitura = params['session'].query(ScontoFornitura).with_parent(self).filter_by(id_fornitura=fornitura.c.id).all()
        self.__scontiFornitura = self.__dbScontiFornitura[:]
        return self.__scontiFornitura

    def _setScontiFornitura(self, value):
        self.__scontiFornitura = value

    sconti = property(_getScontiFornitura, _setScontiFornitura)

    def _fornitore(self):
        if self.forni: return self.forni.ragione_sociale or ""
        #else: return ""
    fornitore= property(_fornitore)

    def _codice_fornitore(self):
        if self.forni: return self.forni.codice or ""
        #else: return ""
    codice_fornitore= property(_codice_fornitore)

    def _codiceArticolo(self):
        if self.arti: return self.arti.codice or ""
        #else: return ""
    codice_articolo= property(_codiceArticolo)

    def _denoArticolo(self):
        if self.arti: return self.arti.denominazione or ""
        #else: return ""
    articolo= property(_denoArticolo)

    def _multiplo(self):
        if self.multi: return self.multi.denominazione_breve or ""
        #else: return ""
    multiplo= property(_multiplo)





    def _denominazione_gruppo_taglia(self):
        #if self.ATC: return self.ATC.denominazione or ""
        if self.arti:return self.arti.denominazione_gruppo_taglia
        #else: return ""
    denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

    def _id_articolo_padre(self):
        #if self.ATC: return self.ATC.id_articolo_padre or None
        if self.arti:return self.arti.id_articolo_padre
    id_articolo_padre_taglia_colore=property(_id_articolo_padre)
    id_articolo_padre = property(_id_articolo_padre)

    def _id_gruppo_taglia(self):
        #if self.ATC: return self.ATC.id_gruppo_taglia or None
        if self.arti:return self.arti.id_gruppo_taglia
    id_gruppo_taglia=property(_id_gruppo_taglia)

    def _id_genere(self):
        #if self.ATC: return self.ATC.id_genere or None
        if self.arti:return self.arti.id_genere
        #else: return ""
    id_genere = property(_id_genere)

    def _id_stagione(self):
        if self.arti:return self.arti.id_stagione
    id_stagione = property(_id_stagione)

    def _id_anno(self):
        if self.arti:return self.arti.id_anno
    id_anno = property(_id_anno)

    def _denominazione_taglia(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Fornitura)\
                                #.filter(and_( ArticoloTagliaColore.id_taglia==Taglia.id)).all()
        #if not a: return a
        #else: return a[0].denominazione
        if self.arti:return self.arti.denominazione_taglia
    denominazione_taglia = property(_denominazione_taglia)

    def _denominazione_colore(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Fornitura)\
                                #.filter(and_( ArticoloTagliaColore.id_colore==Colore.id)).all()
        #if not a: return a
        #else: return a[0].denominazione
        if self.arti:return self.arti.denominazione_colore
    denominazione_colore = property(_denominazione_colore)

    def _anno(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Fornitura)\
                                #.filter(and_(ArticoloTagliaColore.id_anno==AnnoAbbigliamento.id)).all()
        #if not a: return a
        #else: return a[0].denominazione
        if self.arti:return self.arti.anno
    anno = property(_anno)

    def _stagione(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Fornitura)\
                                #.filter(and_(ArticoloTagliaColore.id_stagione==StagioneAbbigliamento.id)).all()
        #if not a: return a
        #else: return a[0].denominazione
        if self.arti:return self.arti.stagione
    stagione = property(_stagione)

    def _genere(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Fornitura)\
                                #.filter(and_( ArticoloTagliaColore.id_genere==GenereAbbigliamento.id)).all()
        #if not a: return a
        #else: return a[0].denominazione
        if self.arti:return self.arti.genere
    genere = property(_genere)


    def filter_values(self,k,v):
        if k == 'codiceArticoloFornitore':
            dic = {k:fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%")}
        elif k== 'idFornitore':
            dic= {k:fornitura.c.id_fornitore ==v}
        elif k== 'idFornitoreList':
            dic= {k:fornitura.c.id_fornitore.in_(v)}
        elif k == 'idArticolo':
            dic = {k:fornitura.c.id_articolo==v}
        elif k == 'idArticoloList':
            dic = {k:fornitura.c.id_articolo.in_(v)}
        elif k == 'daDataPrezzo':
            dic = {k:fornitura.c.data_prezzo >= v}
        elif k == 'aDataPrezzo':
            dic = {k:fornitura.c.data_prezzo <= v}
        elif k == 'daDataFornitura':
            dic= {k:fornitura.c.data_fornitura >= v}
        elif k == 'aDataFornitura':
            dic = {k:fornitura.c.data_fornitura <= v}
        return  dic[k]

        #,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        #,GT.denominazione AS denominazione_gruppo_taglia
        #,T.denominazione_breve AS denominazione_breve_taglia
        #,T.denominazione AS denominazione_taglia
        #,C.denominazione_breve AS denominazione_breve_colore
        #,C.denominazione AS denominazione_colore
        #,AAB.denominazione AS anno
        #,SAB.denominazione AS stagione
        #,GAB.denominazione AS genere
    #FROM fornitura F
    #LEFT OUTER JOIN persona_giuridica P ON F.id_fornitore = P.id
    #LEFT OUTER JOIN articolo A ON F.id_articolo = A.id
    #LEFT OUTER JOIN multiplo M ON F.id_multiplo = M.id
    #LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    #LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    #LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    #LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    #LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    #LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    #LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id
    #WHERE A.cancellato = False;
    #def persist(self, conn=None):

    """FIXME:
            ##cancellazione sconti associati alla fornitura
            #conn.execStoredProcedure('ScontiFornituraDel',
                                     #(self.id, ))

            #if self.__scontiFornitura is not None:
                #for i in range(0, len(self.__scontiFornitura)):
                    ##annullamento id dello sconto
                    #self.__scontiFornitura[i]._resetId()
                    ##associazione allo sconto della fornitura
                    #self.__scontiFornitura[i].id_fornitura = self.id
                    ##salvataggio sconto
                    #self.__scontiFornitura[i].persist(conn)
                    """

fornitura=Table('fornitura',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(Fornitura,fornitura, properties={
        "multi": relation(Multiplo,primaryjoin=fornitura.c.id_multiplo==Multiplo.id),
        "sconto_fornitura": relation(ScontoFornitura, backref="fornitura"),
        "forni" : relation(Fornitore,primaryjoin=fornitura.c.id_fornitore==Fornitore.id),
        "arti" : relation(Articolo,primaryjoin=fornitura.c.id_articolo==Articolo.id, backref=backref("artic", uselist=False)),
        #"ATC":relation(ArticoloTagliaColore,primaryjoin=(Articolo.id==ArticoloTagliaColore.id_articolo)),
        #"GT":relation(GruppoTaglia,primaryjoin=
                    #(GruppoTaglia.id==articolotagliacolore.c.id_gruppo_taglia), backref="ATCGT"),
        #"TA":relation(Taglia,primaryjoin=
                    #(Taglia.id==articolotagliacolore.c.id_taglia), backref="ATCTA"),
        #"CO":relation(Colore,primaryjoin=
                    #(Colore.id==articolotagliacolore.c.id_colore), backref="ATCCO"),
        #"AA":relation(AnnoAbbigliamento,primaryjoin=
                    #(AnnoAbbigliamento.id==articolotagliacolore.c.id_anno), backref="ATCAA"),
        #"SA":relation(StagioneAbbigliamento,primaryjoin=
                    #(StagioneAbbigliamento.id==articolotagliacolore.c.id_stagione), backref="ATCSA"),
        #"GA":relation(GenereAbbigliamento,primaryjoin=
                    #(GenereAbbigliamento.id==articolotagliacolore.c.id_genere), backref="ATCGA"),
                }, order_by=fornitura.c.id)