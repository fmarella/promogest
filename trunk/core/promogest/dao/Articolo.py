#-*- coding: utf-8 -*-
#
"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 license: GPL see LICENSE file
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from promogest import Environment
from Immagine import Immagine
from UnitaBase import UnitaBase
from FamigliaArticolo import FamigliaArticolo
from AliquotaIva import AliquotaIva
from CategoriaArticolo import CategoriaArticolo
from CodiceABarreArticolo import CodiceABarreArticolo
from Imballaggio import Imballaggio
from StatoArticolo import StatoArticolo
from Fornitura import Fornitura
from Multiplo import Multiplo
from promogest.ui.utils import codeIncrement
#from promogest.modules.PromoWear.dao.ArticoloPromowear import Articolo


class Articolo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
        #self.codibar = None

    @reconstructor
    def init_on_load(self):
        self.codibar = None

    def cod_bar(self):
        if not self.codibar:
            self.codibar = params["session"].query(CodiceABarreArticolo).with_parent(self).filter(articolo.c.id==CodiceABarreArticolo.id_articolo)
        return self.codibar


    @property
    def codice_a_barre(self):
        """ esempio di funzione  unita alla property """
        que = self.cod_bar()
        try:
            # cerco la situazione ottimale, un articolo ha un codice ed è primario
            try:
                a =  que.filter(CodiceABarreArticolo.primario==True).one()
                return a.codice
            except:
                a =  que.one()
                return a.codice
        except:
            return ""

    @property
    def codice_articolo_fornitore(self):
        if self.fornitur: return self.fornitur.codice_articolo_fornitore or ""

    @property
    def imballaggio(self):
        if self.imba: return self.imba.denominazione
        else: return ""


    def _getImmagine(self):
        if self.image:
            self._url_immagine= self.image.filename
        else:
            self._url_immagine = ""
        return self._url_immagine

    def _setImmagine(self, value):
        self._url_immagine = value
    url_immagine= property(_getImmagine, _setImmagine)

    @property
    def denominazione_famiglia(self):
        if self.den_famiglia :return self.den_famiglia.denominazione
        else : return ""


    @property
    def denominazione_breve_famiglia(self):
        if self.den_famiglia:return self.den_famiglia.denominazione_breve
        else: return ""

    @property
    def denominazione_breve_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione_breve
        else: return ""

    @property
    def denominazione_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.denominazione
        else: return ""

    @property
    def percentuale_aliquota_iva(self):
        if self.ali_iva :return self.ali_iva.percentuale
        else: return ""

    @property
    def denominazione_breve_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione_breve
        else: return ""

    @property
    def denominazione_categoria(self):
        if self.den_categoria: return self.den_categoria.denominazione
        else: return ""

    @property
    def denominazione_breve_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione_breve
        else: return ""

    @property
    def denominazione_unita_base(self):
        if self.den_unita:return self.den_unita.denominazione
        else: return ""

    @property
    def stato_articolo(self):
        if self.sa: return self.sa.denominazione
        else: return ""

    if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":

        def getArticoloTagliaColore(self):
            """ Restituisce il Dao ArticoloTagliaColore collegato al Dao Articolo #"""
            #if self.__articoloTagliaColore is not None:
            #self.__articoloTagliaColore = None
            #try:
            self.__articoloTagliaColore = ArticoloTagliaColore().getRecord(id=self.id)
            return self.__articoloTagliaColore
            #except:
                #return False

        def setArticoloTagliaColore(self, value):
            """ Imposta il Dao ArticoloTagliaColore collegato al Dao Articolo
            """
            self.__articoloTagliaColore = value
        articoloTagliaColore = property(getArticoloTagliaColore, setArticoloTagliaColore)

        def getArticoliTagliaColore(self, idGruppoTaglia=None, idTaglia=None, idColore=None):
            """ Restituisce una lista di Dao ArticoloTagliaColore figli del Dao Articolo """
            #from promogest.modules.PromoWear.dao.ArticoloTagliaColore import select
            articoli = []
            try:
                articolo_relato = ArticoloTagliaColore().getRecord(id=self.id)
                if not articolo_relato.id_articolo_padre:
                    articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo,
                                                                idGruppoTaglia=idGruppoTaglia,
                                                                idTaglia=idTaglia,
                                                                idColore=idColore,
                                                                offset=None,
                                                                batchSize=None)
                else:
                    articoli = ArticoloTagliaColore().select(idArticoloPadre=articolo_relato.id_articolo_padre,
                                                                idGruppoTaglia=idGruppoTaglia,
                                                                idTaglia=idTaglia,
                                                                idColore=idColore,
                                                                offset=None,
                                                                batchSize=None)
            except:
                print "FOR DEBUG ONLY getArticoliTagliaColore FAILED"
            return articoli
        articoliTagliaColore = property(getArticoliTagliaColore)


        def getArticoliVarianti(self):
            """ Restituisce una lista di Dao Articolo Varianti """
            articoli = []
            for art in self.getArticoliTagliaColore():
                articoli.append(Articolo().getRecord(id=art.id_articolo))
            return articoli
        articoliVarianti = property(getArticoliVarianti)


        def _getTaglie(self):
            """ Restituisce una lista di Dao Taglia relativi alle taglie di tutti i Dao
                ArticoloTagliaColore figli del Dao Articolo  """
            idTaglie = set(a.id_taglia for a in self.articoliTagliaColore)
            return [Taglia().getRecord(id=idt) for idt in idTaglie]

        taglie = property(_getTaglie)


        def _getColori(self):
            """ Restituisce una lista di Dao Colore relativi ai colori di tutti i Dao
                ArticoloTagliaColore figli del Dao Articolo """
            idColori = set(a.id_colore for a in self.articoliTagliaColore)
            return [Colore().getRecord(id=idc) for idc in idColori]

        colori = property(_getColori)

        def _id_articolo_padre(self):
            if self.ATC: return self.ATC.id_articolo_padre or None
        id_articolo_padre_taglia_colore=property(_id_articolo_padre)
        id_articolo_padre = property(_id_articolo_padre)

        def _id_articolo(self):
            # we need it to see if this is ia tagliacolore simple article without father or variant
            if self.ATC: return self.ATC.id_articolo or None
        id_articolo_taglia_colore=property(_id_articolo)

        def _id_gruppo_taglia(self):
            if self.ATC: return self.ATC.id_gruppo_taglia or None
        id_gruppo_taglia=property(_id_gruppo_taglia)

        def _id_taglia(self):
            if self.ATC: return self.ATC.id_taglia or None
        id_taglia=property(_id_taglia)

        def _id_colore(self):
            if self.ATC: return self.ATC.id_colore or None
        id_colore=property(_id_colore)

        def _id_modello(self):
            if self.ATC: return self.ATC.id_modello or None
        id_modello=property(_id_modello)

        def _id_genere(self):
            if self.ATC: return self.ATC.id_genere or None
            #else: return ""
        id_genere = property(_id_genere)

        def _id_stagione(self):
            if self.ATC: return self.ATC.id_stagione or None
        id_stagione = property(_id_stagione)

        def _id_anno(self):
            if self.ATC: return self.ATC.id_anno or ""
        id_anno = property(_id_anno)

        @property
        def denominazione_gruppo_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_gruppo_taglia
                except:
                    return self.ATC.denominazione_gruppo_taglia

        @property
        def denominazione_taglia(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_taglia
                except:
                    return self.ATC.denominazione_taglia

        def _denominazione_colore(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_colore
                except:
                    return self.ATC.denominazione_colore
        denominazione_colore = property(_denominazione_colore)

        def _denominazione_modello(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].denominazione_modello
                except:
                    return self.ATC.denominazione_modello
        denominazione_modello = property(_denominazione_modello)

        @property
        def anno(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].anno
                except:
                    return self.ATC.anno

        @property
        def stagione(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].stagione
                except:
                    return self.ATC.stagione

        @property
        def genere(self):
            """ esempio di funzione  unita alla property """
            if self.ATC :
                try:
                    return self.ATC[0].genere
                except:
                    return self.ATC.genere

        def isArticoloPadre(self):
            """ Dice se l'articolo e' un articolo padre """

            articolo = self.getArticoloTagliaColore()
            if articolo is not None:
                return (articolo.id_articolo_padre is None)
            else:
                return False

    if "GestioneNoleggio" in Environment.modulesList:

        @property
        def divisore_noleggio(self):
            """ esempio di funzione  unita alla property """
            if self.APGN :return self.APGN.divisore_noleggio_value
            else: return ""


    if hasattr(conf, "DistintaBase") and getattr(conf.DistintaBase,'mod_enable')=="yes":
        """ necessario questo if"""
        @property
        def articoliAss(self):
            """ esempio di funzione  unita alla property """
            arts = AssociazioneArticolo().select(idPadre=self.id,
                                                offset=None,
                                                batchSize=None)
            return arts

    def persist(self):
        params["session"].add(self)
        self.saveToAppLog(self)
        #salvataggio , immagine ....per il momento viene gestita una immagine per articolo ...
        #in seguito sarà l'immagine a comandare non l'articolo
        try:
            if self._url_immagine and Immagine().getRecord(id=self.id_immagine):
                img = Immagine().getRecord(id=self.id_immagine)
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                self.saveToAppLog(img)
                params["session"].add(self)
                self.saveToAppLog(self)
            elif self._url_immagine:
                img = Immagine()
                img.id=self.id
                img.filename=self._url_immagine
                img.id_famiglia = self.id_famiglia_articolo
                self.id_immagine = self.id
                params["session"].add(img)
                self.saveToAppLog(img)
                params["session"].add(self)
                self.saveToAppLog(self)
            elif not self._url_immagine and Immagine().getRecord(id=self.id_immagine):
                img = Immagine().getRecord(id=self.id_immagine)
                self.id_immagine = None
                img.delete()
        except:
            pass
        if "GestioneNoleggio" in Environment.modulesList:
            if self.divisore_noleggio_value_set and self.id:
                div_nol = ArticoloPlusGN().getRecord(id=self.id)
                if div_nol:
                        div_nol.value = self.divisore_noleggio_value_set
                        params["session"].add(div_nol)
                else:
                    div_nol = ArticoloPlusGN()
                    div_nol.id_articolo = self.id
                    div_nol.divisore_noleggio_value = self.divisore_noleggio_value_set
                    params["session"].add(div_nol)
        if "PromoWear" in Environment.modulesList:
            try:
                if self.__articoloTagliaColore:
                    if ArticoloTagliaColore().getRecord(id=self.id):
                        a = ArticoloTagliaColore().getRecord(id=self.id)
                        a.delete()
                    self.__articoloTagliaColore.id_articolo=self.id
                    params["session"].add(self.__articoloTagliaColore)
                    self.saveToAppLog(self.__articoloTagliaColore)
                    if self.isArticoloPadre():
                        for var in self.getArticoliTagliaColore():
                            var.id_genere = self.__articoloTagliaColore.id_genere
                            var.id_anno = self.__articoloTagliaColore.id_anno
                            var.id_stagione = self.__articoloTagliaColore.id_stagione
                            var.id_modello = self.__articoloTagliaColore.id_modello
                            params["session"].add(var)
                        #self.saveToAppLog(var)
            except:
                print "ARTICOLO NORMALE SENZA TAGLIE O COLORI"
        params["session"].commit()

    def delete(self):
        # se l'articolo e' presente tra le righe di un movimento o documento
        # si esegue la cancellazione logica
        from Riga import Riga
        res = Riga().select(id_articolo=self.id)
        if res:
            daoArticolo = Articolo().getRecord(id=self.id)
            daoArticolo.cancellato = True
            params["session"].add(daoArticolo)
            self.saveToAppLog(daoArticolo)
        else:
            params["session"].delete(self)
            self.saveToAppLog(self)

    def filter_values(self,k,v):
        if k == "codice":
            dic = {k:articolo.c.codice.ilike("%"+v+"%")}
        elif k == "codicesatto" or k == "codiceEM":
            dic = {k:articolo.c.codice == v}
        elif k == 'denominazione':
            dic = {k:articolo.c.denominazione.ilike("%"+v+"%")}
        elif k == 'codiceABarre':
            dic = {k:and_(articolo.c.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice.ilike("%"+v+"%"))}
        elif k== 'codiceArticoloFornitore':
            dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore.ilike("%"+v+"%"))}
        elif k== 'codiceArticoloFornitoreEM':
            dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore == v)}
        elif k == 'produttore':
            dic = {k:articolo.c.produttore.ilike("%"+v+"%")}
        elif k=='idFamiglia':
            dic = {k:articolo.c.id_famiglia_articolo ==v}
        elif k == 'idCategoria':
            dic = {k:articolo.c.id_categoria_articolo ==v}
        elif k == 'idStato':
            dic= {k:articolo.c.id_stato_articolo == v}
        elif k == 'cancellato':
            dic = {k:or_(articolo.c.cancellato != v)}
        elif k == 'idArticolo':
            dic = {k:or_(articolo.c.id == v)}
        elif "PromoWear" in Environment.modulesList:
            if k == 'figliTagliaColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre==None)}
            elif k == 'idTaglia':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_taglia==v)}
            elif k == 'idModello':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_modello==v)}
            elif k == 'idGruppoTaglia':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_gruppo_taglia ==v)}
            elif k == 'padriTagliaColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre!=None)}
            elif k == 'idColore':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_colore ==v)}
            elif k == 'idStagione':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_stagione ==v)}
            elif k == 'idAnno':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_anno == v)}
            elif k == 'idGenere':
                dic = {k:and_(articolo.c.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_genere ==v)}
        elif "DistintaBase" in Environment.modulesList:
            print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
            if k =="nodo":
                dic = {}
        return  dic[k]

fornitura=Table('fornitura',params['metadata'],schema = params['schema'],autoload=True)
articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Articolo,articolo,
            properties=dict(
                        cod_barre = relation(CodiceABarreArticolo,primaryjoin=
                                articolo.c.id==CodiceABarreArticolo.id_articolo, backref="arti", cascade="all, delete"),
                        imba = relation(Imballaggio,primaryjoin=
                                (articolo.c.id_imballaggio==Imballaggio.id), backref="arti"),
                        ali_iva =  relation(AliquotaIva,primaryjoin=
                                (articolo.c.id_aliquota_iva==AliquotaIva.id)),
                        den_famiglia = relation(FamigliaArticolo,primaryjoin= articolo.c.id_famiglia_articolo==FamigliaArticolo.id),
                        den_categoria = relation(CategoriaArticolo,primaryjoin=
                                    (articolo.c.id_categoria_articolo==CategoriaArticolo.id)),
                        den_unita = relation(UnitaBase,primaryjoin= (articolo.c.id_unita_base==UnitaBase.id)),
                        image = relation(Immagine,primaryjoin= (articolo.c.id_immagine==Immagine.id)),
                        sa = relation(StatoArticolo,primaryjoin=(articolo.c.id_stato_articolo==StatoArticolo.id)),
                        fornitur = relation(Fornitura,primaryjoin=(Fornitura.id_articolo==articolo.c.id), backref="arti",uselist=False),
                        multi = relation(Multiplo,primaryjoin=(Multiplo.id_articolo==articolo.c.id),backref="arti")
                        ), order_by=articolo.c.codice)
if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    std_mapper.add_property("ATC",relation(ArticoloTagliaColore,primaryjoin=(articolo.c.id==ArticoloTagliaColore.id_articolo),backref="ARTI",uselist=False))
if hasattr(conf, "DistintaBase") and getattr(conf.DistintaBase,'mod_enable')=="yes":
    from promogest.modules.DistintaBase.dao.AssociazioneArticolo import AssociazioneArticolo
    std_mapper.add_property("AAPadre",relation(AssociazioneArticolo,primaryjoin=(articolo.c.id==AssociazioneArticolo.id_padre),backref="ARTIPADRE"))
    std_mapper.add_property("AAFiglio",relation(AssociazioneArticolo,primaryjoin=(articolo.c.id==AssociazioneArticolo.id_figlio),backref="ARTIFIGLIO"))
if hasattr(conf, "GestioneNoleggio") and getattr(conf.GestioneNoleggio,'mod_enable')=="yes":
    from promogest.modules.GestioneNoleggio.dao.ArticoloPlusGN import ArticoloPlusGN
    std_mapper.add_property("APGN",relation(ArticoloPlusGN,primaryjoin=(articolo.c.id==ArticoloPlusGN.id_articolo),backref="ARTI"))


def isNuovoCodiceByFamiglia():
    """ Indica se un nuovo codice articolo dipende dalla famiglia o meno """
    dependsOn = False

    if hasattr(conf,'Articoli'):
        if hasattr(conf.Articoli,'numero_famiglie'):
            if hasattr(conf.Articoli,'lunghezza_codice_famiglia'):
                dependsOn = ((int(conf.Articoli.lunghezza_codice_famiglia) > 0) and
                            (int(conf.Articoli.numero_famiglie) > 0))
    return dependsOn

def getNuovoCodiceArticolo(idFamiglia=None):
    """ Restituisce il codice progressivo per un nuovo articolo """

    lunghezzaProgressivo = 0
    lunghezzaCodiceFamiglia = 0
    numeroFamiglie = 0
    codice = ''
    if hasattr(conf,'Articoli'):
        if hasattr(conf.Articoli,'lunghezza_progressivo'):
            if isNuovoCodiceByFamiglia():
                print "passi qui,isNuovoCodiceByFamiglia() "
                lunghezzaCodiceFamiglia = int(conf.Articoli.lunghezza_codice_famiglia)
                numeroFamiglie = int(conf.Articoli.numero_famiglie)
            #codicesel  =params['session'].query(Articolo.codice).order_by("id").all()
            if Environment.lastCode:
                codice = codeIncrement(Environment.lastCode)
                Environment.lastCode = codice
            else:
                codice = codeIncrement(conf.Articoli.struttura_codice)
                while params['session'].query(Articolo.codice).filter(codice==Articolo.codice).order_by("id").all():
                    codice = codeIncrement(codice)
                else:
                    codice = codice
    if params['session'].query(Articolo.codice).filter(codice==Articolo.codice).order_by("id").all():
        while params['session'].query(Articolo.codice).filter(codice==Articolo.codice).order_by("id").all():
            codice = codeIncrement(codice)
            Environment.lastCode = codice
        else:
            codice = codice
    else:
        Environment.lastCode = codice
    return codice

    def getArticoliAssociati(connection, id):
        res = connection.execStoredProcedure('ArticoliAssociatiGet',(codice,))
        if len(res) > 0:
            article_list =[]
            for r in res:
                article_list.append(Articolo(connection,r['id']))
            print 'Done. Found '+str(len(res))+' associated articles in databse.'
            return (len(res))

    def setArticoliAssociati(connection, article, data):
        if len (data) > 0:
            for article2 in data:
                connection.execStoredProcedure('ArticoliAssociatiSet', (article1.id, article2.id))
            return true
        else:
            return None

    def delArticoliAssociati(connection, articolo1, articolo2):
        connection.execStoredProcedure('ArticoliAssociatiDel', (article1.id,article2.id))