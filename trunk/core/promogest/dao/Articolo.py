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
from promogest.ui.utils import idArticoloFromFornitura, codeIncrement

if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
        from promogest.modules.PromoWear.dao.ArticoloPromowear import Articolo
else:
    class Articolo(Dao):

        def __init__(self, arg=None,isList=False, id=None):
            Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

        def _codice_a_barre(self):
            """ esempio di funzione  unita alla property """
            try:
                # cerco la situazione ottimale, un articolo ha un codice ed è primario
                try:
                    a =  params["session"].query(CodiceABarreArticolo.codice).with_parent(self).filter(and_(articolo.c.id==CodiceABarreArticolo.id_articolo,
                                CodiceABarreArticolo.primario==True)).one()
                    return a[0]
                except:
                    a =  params["session"].query(CodiceABarreArticolo.codice).with_parent(self).filter(articolo.c.id==CodiceABarreArticolo.id_articolo).one()
                    return a[0]
            except:
                return ""
        codice_a_barre = property(_codice_a_barre)

        def _codice_articolo_fornitore(self):
            if self.fornitur: return self.fornitur.codice_articolo_fornitore or ""
        codice_articolo_fornitore= property(_codice_articolo_fornitore)

        def _codice_a_barre_all(self):
            """ esempio di funzione  unita alla property """
            a =  params["session"].query(CodiceABarreArticolo).with_parent(self).filter(and_(articolo.c.id==CodiceABarreArticolo.id_articolo)).all()
            if not a:
                return a
            else:
                return a[0].codice
        codice_a_barre_all = property(_codice_a_barre_all)

        def _imballaggio(self):
            if self.imba: return self.imba.denominazione
            else: return ""
        imballaggio= property(_imballaggio)

        def _getImmagine(self):
            if self.image:
                self._url_immagine= self.image.filename
            else:
                self._url_immagine = ""
            return self._url_immagine

        def _setImmagine(self, value):
            self._url_immagine = value
        url_immagine= property(_getImmagine, _setImmagine)

        def _denominazione_famiglia(self):
            if self.den_famiglia :return self.den_famiglia.denominazione
            else : return ""
        denominazione_famiglia= property(_denominazione_famiglia)

        def _denominazione_breve_famiglia(self):
            if self.den_famiglia:return self.den_famiglia.denominazione_breve
            else: return ""
        denominazione_breve_famiglia= property(_denominazione_breve_famiglia)

        def _denominazione_breve_aliquota_iva(self):
            if self.ali_iva :return self.ali_iva.denominazione_breve
            else: return ""
        denominazione_breve_aliquota_iva= property(_denominazione_breve_aliquota_iva)

        def _denominazione_aliquota_iva(self):
            if self.ali_iva :return self.ali_iva.denominazione
            else: return ""
        denominazione_aliquota_iva= property(_denominazione_aliquota_iva)

        def _percentuale_aliquota_iva(self):
            if self.ali_iva :return self.ali_iva.percentuale
            else: return ""
        percentuale_aliquota_iva= property(_percentuale_aliquota_iva)

        def _denominazione_breve_categoria(self):
            if self.den_categoria: return self.den_categoria.denominazione_breve
            else: return ""
        denominazione_breve_categoria = property(_denominazione_breve_categoria)

        def _denominazione_categoria(self):
            if self.den_categoria: return self.den_categoria.denominazione
            else: return ""
        denominazione_categoria = property(_denominazione_categoria)

        def _denominazione_breve_unita_base(self):
            if self.den_unita:return self.den_unita.denominazione_breve
            else: return ""
        denominazione_breve_unita_base= property(_denominazione_breve_unita_base)

        def _denominazione_unita_base(self):
            if self.den_unita:return self.den_unita.denominazione
            else: return ""
        denominazione_unita_base= property(_denominazione_unita_base)

        def _stato_articolo(self):
            if self.sa: return self.sa.denominazione
            else: return ""
        stato_articolo= property(_stato_articolo)

        def persist(self):
            params["session"].add(self)
            params["session"].commit()
            #salvataggio , immagine ....per il momento viene gestita una immagine per articolo ...
            #in seguito sarà l'immagine a comandare non l'articolo
            try:
                if self._url_immagine and Immagine(id=self.id_immagine).getRecord():
                    img = Immagine(id=self.id_immagine).getRecord()
                    img.filename=self._url_immagine
                    img.id_famiglia = self.id_famiglia_articolo
                    self.id_immagine = self.id
                    params["session"].add(img)
                    params["session"].add(self)
                    params["session"].commit()
                elif self._url_immagine:
                    img = Immagine().getRecord()
                    img.id=self.id
                    img.filename=self._url_immagine
                    img.id_famiglia = self.id_famiglia_articolo
                    self.id_immagine = self.id
                    params["session"].add(img)
                    params["session"].add(self)
                    params["session"].commit()
                elif not self._url_immagine and Immagine(id=self.id_immagine).getRecord():
                    img = Immagine(id=self.id_immagine).getRecord()
                    self.id_immagine = None
                    img.delete()
            except:
                pass
                #print "nessuna immagine associata all'articolo"
            params["session"].flush()

        def delete(self):
            # se l'articolo e' presente tra le righe di un movimento o documento
            # si esegue la cancellazione logica
            from Riga import Riga
            res = Riga(isList=True).select(id_articolo=self.id)
            if res:
                daoArticolo = Articolo(id=self.id).getRecord()
                daoArticolo.cancellato = True
                params["session"].add(daoArticolo)
                params["session"].commit()
            else:
                params["session"].delete(self)
                params["session"].commit()

        def filter_values(self,k,v):
            if k == "codice":
                dic = {k:articolo.c.codice.ilike("%"+v+"%")}
            elif k == "codicesatto":
                dic = {k:articolo.c.codice == v}
            elif k == 'denominazione':
                dic = {k:articolo.c.denominazione.ilike("%"+v+"%")}
            elif k == 'codiceABarre':
                dic = {k:and_(articolo.c.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice.like("%"+v+"%"))}
            elif k== 'codiceArticoloFornitore':
                dic = {k:and_(articolo.c.id==fornitura.c.id_articolo,fornitura.c.codice_articolo_fornitore.like("%"+v+"%"))}
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
            return  dic[k]

    #def getByCodice(connection, codice):
        #""" Restituisce il risultato di una ricerca per codice """
        #res = connection.execStoredProcedure('ArticoloGetByCodice', (codice,))
        #if len(res) > 0:
            #return Articolo(connection, res[0]['id'])
            #else:
                #return None
    fornitura=Table('fornitura',params['metadata'],schema = params['schema'],autoload=True)
    articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)

    std_mapper = mapper(Articolo,articolo,
                properties={
                "cod_barre":relation(CodiceABarreArticolo,primaryjoin=
                    and_(articolo.c.id==CodiceABarreArticolo.id_articolo)),
                "imba":relation(Imballaggio,primaryjoin=
                    and_(articolo.c.id_imballaggio==Imballaggio.id), backref="articolo"),
                #"stato_articolo":relation(StatoArticolo, backref="articolo"),
                "ali_iva" : relation(AliquotaIva,primaryjoin=
                    and_(articolo.c.id_aliquota_iva==AliquotaIva.id)),
                "den_famiglia":relation(FamigliaArticolo,primaryjoin= articolo.c.id_famiglia_articolo==FamigliaArticolo.id),
                "den_categoria":relation(CategoriaArticolo,primaryjoin=
                    and_(articolo.c.id_categoria_articolo==CategoriaArticolo.id)),
                "den_unita":relation(UnitaBase,primaryjoin= (articolo.c.id_unita_base==UnitaBase.id)),
                "image":relation(Immagine,primaryjoin= (articolo.c.id_immagine==Immagine.id)),
                "sa":relation(StatoArticolo,primaryjoin=(articolo.c.id_stato_articolo==StatoArticolo.id)),
                "fornitur" : relation(Fornitura,primaryjoin=Fornitura.id_articolo==articolo.c.id, backref=backref("arti"),uselist=False),
                "multi":relation(Multiplo,primaryjoin=Multiplo.id_articolo==articolo.c.id,backref=backref("arti"))
                }, order_by=articolo.c.id)


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