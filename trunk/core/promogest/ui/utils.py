# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gobject, os, decimal
from decimal import *
import pygtk
pygtk.require('2.0')
import gtk
import time, datetime
from sqlalchemy.orm import *
from sqlalchemy import *
from promogest import Environment
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.Operazione import Operazione
from promogest.dao.Azienda import Azienda
from promogest.dao.RoleAction import RoleAction
from promogest.dao.Role import Role
from promogest.dao.Language import Language
import string, re
import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import *
import Login
from promogest.dao.Dao import Dao
from utilsCombobox import *
# Letture per recuperare velocemente dati da uno o piu' dao correlati


def articleType(dao):
    if dao and "PromoWear" in Environment.modulesList:
        if (dao.id) and (dao.id_articolo_taglia_colore is not None) and (dao.id_articolo_padre is None) and (dao.articoliTagliaColore):
            print "ARTICOLO FATHER"
            return "father"
        elif (dao.id) and (dao.id_articolo_taglia_colore is not None) and (dao.id_articolo_padre) and (not dao.articoliTagliaColore):
            print "ARTICOLO SON"
            return "son"
        elif (dao.id) and (dao.id_articolo_taglia_colore is not None) and (dao.id_articolo_padre is None) and (not dao.articoliTagliaColore):
            print "ARTICOLO PLUS"
            return "plus"
        elif (dao.id) and (dao.id_articolo_taglia_colore is None) and (dao.id_articolo_padre is None) and (not dao.articoliTagliaColore):
            print "ARTICOLO NORMAL"
            return "normal"
        elif not dao.id:
            print "ARTICOLO NEW NORMAL"
            return "new"


def leggiArticolo(id, full=False, idFornitore=False,data=None):
    """
    Restituisce un dizionario con le informazioni sull'articolo letto
    """
    from promogest.dao.AliquotaIva import AliquotaIva
    from promogest.dao.Articolo import Articolo
    _id = None
    _denominazione = ''
    _codice = ''
    _denominazioneBreveAliquotaIva = ''
    _percentualeAliquotaIva = 0
    _idUnitaBase = None
    _unitaBase = ''
    _quantita_minima = ''
    artiDict = {}
    print "ID IN LEGGI ARTICOLO ", id
    if id is not None:
        daoArticolo = Articolo(id=id).getRecord()
        print "daoArticoloooooooooooooooooo", daoArticolo
        variantiList = []
        if "PromoWear" in Environment.modulesList:
            if articleType(daoArticolo)=="father":
                varianti = daoArticolo.articoliVarianti
                from promogest.modules.PromoWear.ui.PromowearUtils import leggiArticoloPromoWear, leggiFornituraPromoWear
                for varia in varianti:
                    variante=leggiArticoloPromoWear(varia.id, full=True)
                    variante['fornitura'] = leggiFornituraPromoWear(idArticolo=varia.id,
                                                    idFornitore=idFornitore,
                                                    data=data)
                    variantiList.append(variante)
                artiDict = leggiArticoloPromoWear(id)
                artiDict["varianti"] = variantiList
                artiDict["fornitura"] = leggiFornituraPromoWear(idArticolo=varia.id,
                                                    idFornitore=idFornitore,
                                                    data=data)
                return artiDict
        if daoArticolo is not None:
            print "DENTRO L?IF DI DAO ARTICOLO", daoArticolo.codice
            _id = id
            _denominazione = daoArticolo.denominazione or ''
            _codice = daoArticolo.codice or ''
            _idUnitaBase = daoArticolo.id_unita_base
            _quantita_minima = ''
            if _idUnitaBase is not None:
                res = UnitaBase(id =_idUnitaBase).getRecord()
                if res is not None:
                    _unitaBase = res.denominazione
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = AliquotaIva(id=daoArticolo.id_aliquota_iva).getRecord()
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
                    _percentualeAliquotaIva = daoAliquotaIva.percentuale or 0

            artiDict = {"id": _id,
                    "denominazione": _denominazione, "codice": _codice,
                    "denominazioneBreveAliquotaIva": _denominazioneBreveAliquotaIva,
                    "percentualeAliquotaIva": _percentualeAliquotaIva,
                    "idUnitaBase": _idUnitaBase,
                    "unitaBase": _unitaBase,
                    "quantita_minima": _quantita_minima}
            return artiDict


def leggiCliente(id):
    from  promogest.dao.Cliente import Cliente
    """
    Restituisce un dizionario con le informazioni sul cliente letto
    """
    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''
    _id_pagamento = None
    _id_magazzino = None
    _id_listino = None
    _id_banca = None
    _email = None
    if id is not None:
        daoCliente = Cliente(id=id).getRecord()
        if daoCliente is not None:
            try:
                for i in range(0,len(daoCliente.recapiti)):
                    if daoCliente.recapiti[i].tipo_recapito == "E-Mail":
                        _email = daoCliente.recapiti[i].recapito
            except:
                _email = ""

            _id = id
            _ragioneSociale = daoCliente.ragione_sociale or ''
            _nome = daoCliente.nome or ''
            _cognome = daoCliente.cognome or ''
            _id_pagamento = daoCliente.id_pagamento
            _id_magazzino = daoCliente.id_magazzino
            _id_listino = daoCliente.id_listino
            _id_banca = daoCliente.id_banca

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,
            "id_pagamento": _id_pagamento,
            "id_magazzino": _id_magazzino,
            "id_listino": _id_listino,
            "id_banca": _id_banca,
            "email": _email or ""}


def leggiDestinazioneMerce(id):
    """
    Restituisce un dizionario con le informazioni sulla destinazione merce letta
    """
    from promogest.dao.DestinazioneMerce import DestinazioneMerce
    _id = None
    _denominazione = ''
    _indirizzo = ''
    _localita = ''
    _cap = ''
    _provincia = ''
    _email = ""

    if id is not None:
        daoDestinazioneMerce = DestinazioneMerce(id=id).getRecord()
        if daoDestinazioneMerce is not None:
            _id = id
            _denominazione = daoDestinazioneMerce.denominazione or ''
            _indirizzo = daoDestinazioneMerce.indirizzo or ''
            _localita = daoDestinazioneMerce.localita or ''
            _cap = daoDestinazioneMerce.cap or ''
            _provincia = daoDestinazioneMerce.provincia or ''

    return {"id": _id,
            "denominazione": _denominazione,
            "indirizzo": _indirizzo,
            "localita": _localita,
            "cap": _cap,
            "provincia": _provincia}


def leggiFornitore(id):
    """
    Restituisce un dizionario con le informazioni sul fornitore letto
    """
    from promogest.dao.Fornitore import Fornitore
    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''
    _id_pagamento = None
    _id_magazzino = None
    _email = None

    if id is not None:
        daoFornitore = Fornitore(id=id).getRecord()
        if daoFornitore is not None:
            try:
                for i in range(0,len(daoFornitore.recapiti)):
                    if daoFornitore.recapiti[i].tipo_recapito == "E-Mail":
                        _email = daoFornitore.recapiti[i].recapito
            except:
                _email = ""

            _id = id
            _ragioneSociale = daoFornitore.ragione_sociale or ''
            _nome = daoFornitore.nome or ''
            _cognome = daoFornitore.cognome or ''
            _id_pagamento = daoFornitore.id_pagamento
            _id_magazzino = daoFornitore.id_magazzino

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,
            "id_pagamento": _id_pagamento,
            "id_magazzino": _id_magazzino,
            "email":_email or ""}


def leggiVettore(id):
    """
    Restituisce un dizionario con le informazioni sul vettore letto
    """
    from promogest.dao.Vettore import Vettore
    _id = None
    _ragioneSociale = ''

    if id is not None:
        daoVettore = Vettore(id=id).getRecord()
        if daoVettore is not None:
            _id = id
            _ragioneSociale = daoVettore.ragione_sociale or ''

    return {"id": _id,
            "ragioneSociale": _ragioneSociale}


def leggiDestinazioneMerce(id):
    """
    Restituisce un dizionario con le informazioni sul vettore letto
    """
    from promogest.dao.DestinazioneMerce import DestinazioneMerce
    _id = None
    _denominazione = ''

    if id is not None:
        daoDestinazioneMerce = DestinazioneMerce(id=id).getRecord()
        if daoDestinazioneMerce is not None:
            _id = id
            _denominazione = daoDestinazioneMerce.denominazione or ''

    return {"id": _id,
            "denominazione": _denominazione}


def leggiContatto(id):
    """
    Restituisce un dizionario con le informazioni sul contatto letto
    """
    from promogest.dao.Contatto import Contatto
    _id = None
    _nome = ''
    _cognome = ''
    _email = ''

    if id is not None:
        daoContatto = Contatto(id=id).getRecord()
        if daoContatto is not None:
            try:
                for i in range(0,len(daoContatto.recapiti)):
                    if daoContatto.recapiti[i].tipo_recapito == "E-Mail":
                        _email = daoContatto.recapiti[i].recapito
            except:
                _email = ""


                daoContatto.recapiti[0].tipo_recapito
            _id = id
            _nome = daoContatto.nome or ''
            _cognome = daoContatto.cognome or ''
            _email = _email or ''

    return {"id": _id,
            "nome": _nome,
            "cognome": _cognome,
            "email": _email}

def leggiMagazzino(id):
    """
    Restituisce un dizionario con le informazioni sul magazzino letto
    """
    from promogest.dao.Magazzino import Magazzino
    _id = None
    _denominazione = ''
    _email = None

    if id is not None:
        daoMagazzino = Magazzino(id=id).getRecord()
        if daoMagazzino is not None:
            try:
                for i in range(0,len(daoMagazzino.recapiti)):
                    if daoMagazzino.recapiti[i].tipo_recapito == "E-Mail":
                        _email = daoMagazzino.recapiti[i].recapito
            except:
                _email = ""
            _id = id
            _denominazione = daoMagazzino.denominazione or ''

    return {"id": _id,
            "denominazione": _denominazione,
            "email": _email}

def leggiListino(idListino, idArticolo=None):
    """ Restituisce un dizionario con le informazioni sul listino letto """
    from promogest.dao.Listino import Listino
    from promogest.dao.ListinoArticolo import ListinoArticolo
    _denominazione = ''
    _prezzoIngrosso = 0
    _prezzoDettaglio = 0

    if idListino is not None:
        try:
            daoListino = Listino(isList=True).select(idListino=idListino,
                                                        batchSize=None)[0]
            if daoListino is not None:
                _denominazione = daoListino.denominazione
        except:
            print "leggiListino ha cannato qualcosa.....1"
            #pass
        try:
            if idArticolo is not None:
                daoListinoArticolo = ListinoArticolo(isList=True)\
                                            .select(idListino=idListino,
                                            idArticolo = idArticolo,
                                            batchSize=None, orderBy="id_listino")[0]
                if daoListinoArticolo is not None:
                    _prezzoIngrosso = daoListinoArticolo.prezzo_ingrosso
                    _prezzoDettaglio = daoListinoArticolo.prezzo_dettaglio
                    _scontiDettaglio = daoListinoArticolo.sconto_vendita_dettaglio
                    _scontiIngrosso = daoListinoArticolo.sconto_vendita_ingrosso
                    _applicazioneDettaglio = daoListinoArticolo.applicazione_sconti_dettaglio
                    _applicazioneIngrosso = daoListinoArticolo.applicazione_sconti_ingrosso

                return {"denominazione": _denominazione,
                        "prezzoIngrosso": _prezzoIngrosso,
                        "prezzoDettaglio": _prezzoDettaglio,
                        "scontiDettaglio":_scontiDettaglio,
                        "scontiIngrosso":_scontiIngrosso,
                        'applicazioneScontiDettaglio':_applicazioneDettaglio,
                        'applicazioneScontiIngrosso':_applicazioneIngrosso}
        except:
            print "leggiListino ha cannato qualcosa.....2"

    return {"denominazione": _denominazione,
            "prezzoIngrosso": _prezzoIngrosso,
            "prezzoDettaglio": _prezzoDettaglio}

def leggiFornitura(idArticolo, idFornitore=None, data=None, noPreferenziale=False):
    """ Restituisce un dizionario con le informazioni sulla fornitura letta """
    from promogest.dao.Fornitura import Fornitura
    from promogest.dao.ScontoFornitura import ScontoFornitura
    _prezzoLordo = 0
    _prezzoNetto = 0
    _sconti = []
    _applicazioneSconti = 'scalare'
    _codiceArticoloFornitore = ''

    if (idArticolo is not None):
        fors = Fornitura(isList=True).select(idArticolo=idArticolo,
                                              idFornitore=None,
                                              daDataFornitura=None,
                                              aDataFornitura=None,
                                              daDataPrezzo=None,
                                              aDataPrezzo=data,
                                              codiceArticoloFornitore=None,
                                              orderBy = 'data_prezzo DESC, fornitore_preferenziale DESC',
                                              offset = None,
                                              batchSize = None)

        fornitura = None
        if idFornitore is not None:
            # cerca tra tutti i fornitori quello utile, o in sua assenza, quello preferenziale
            for f in fors:
                if f.id_fornitore == idFornitore:
                    fornitura = f
                    break
                elif not(noPreferenziale) and f.fornitore_preferenziale:
                    fornitura = f
        else:
            if len(fors) > 0:
                fornitura = fors[0]

        if fornitura is not None:
            _codiceArticoloFornitore = fornitura.codice_articolo_fornitore or ''
            _prezzoLordo = fornitura.prezzo_lordo or 0
            _prezzoNetto = _prezzoLordo
            _applicazioneSconti = fornitura.applicazione_sconti

            idFornitura = fornitura.id
            if idFornitura is not None:
                scos = ScontoFornitura(isList=True).select(idFornitura=idFornitura)

                for s in scos:
                    _sconti.append({"valore": s.valore, "tipo": s.tipo_sconto})

                    if s.tipo_sconto == 'percentuale':
                        if _applicazioneSconti == 'scalare':
                            _prezzoNetto = float(_prezzoNetto) * (1 - float(s.valore) / 100)
                        elif _applicazioneSconti == 'non scalare':
                            _prezzoNetto = float(_prezzoNetto) - float(_prezzoLordo) * float(s.valore) / 100
                    elif s.tipo_sconto == 'valore':
                        _prezzoNetto = float(_prezzoNetto) - float(s.valore)
    return {"prezzoLordo": _prezzoLordo,
            "prezzoNetto": _prezzoNetto,
            "sconti": _sconti,
            "applicazioneSconti": _applicazioneSconti,
            "codiceArticoloFornitore": _codiceArticoloFornitore}


def leggiOperazione(id):
    """
    Restituisce un dizionario con le informazioni sulla operazione letta
    """
    from  promogest.dao.Operazione import Operazione
    _fonteValore = ''
    _segno = ''
    _tipoPersonaGiuridica = ''

    if id is not None:
        res = Operazione(isList=True).select(batchSize=None,
                                            offset=None,
                                            denominazione=id,
                                            orderBy="denominazione")
        #queryString = ("SELECT * FROM promogest.operazione WHERE denominazione = '" + id + "'")
        #argList = []
        #Environment.connection._cursor.execute(queryString, argList)
        #res = Environment.connection._cursor.fetchall()
        if len(res) > 0:
            _fonteValore = res[0].fonte_valore or ''
            _segno = res[0].segno or ''
            _tipoPersonaGiuridica = res[0].tipo_persona_giuridica or ''

    return {"fonteValore": _fonteValore,
            "segno": _segno,
            "tipoPersonaGiuridica": _tipoPersonaGiuridica}


def leggiMultiplo(idMultiplo):
    """
    Restituisce un dizionario con le informazioni sul multiplo letto
    """
    from promogest.dao.Multiplo import Multiplo
    _denominazioneBreve = ''
    _denominazione = ''
    _moltiplicatore = 0

    if idMultiplo is not None:
        daoMultiplo = Multiplo(id=idMultiplo).getRecord()
        if daoMultiplo is not None:
            _denominazioneBreve = daoMultiplo.denominazione_breve
            _denominazione = daoMultiplo.denominazione
            _moltiplicatore = daoMultiplo.moltiplicatore

    return {"denominazioneBreve": _denominazioneBreve,
            "denominazione": _denominazione,
            "moltiplicatore": _moltiplicatore}


def leggiAzienda(schema):
    """
    Restituisce un dizionario con le informazioni sull'azienda letta
    """
    from  promogest.dao.Azienda import Azienda
    _schema = None
    _denominazione = ''

    if schema is not None:
        daoAzienda = Azienda(id=schema).getRecord()
        if daoAzienda is not None:
            _schema = schema
            _denominazione = daoAzienda.denominazione or ''

    return {"schema": _schema,
            "denominazione": _denominazione}


def leggiAgente(id):
    """
    Restituisce un dizionario con le informazioni sul vettore letto
    """
    from  promogest.dao.Agente import Agente
    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''
    _email = None

    if id is not None:
        daoAgente = Agente(id=id).getRecord()
        if daoAgente is not None:
            try:
                for i in range(0,len(daoAgente.recapiti)):
                    if daoAgente.recapiti[i].tipo_recapito == "E-Mail":
                        _email = daoAgente.recapiti[i].recapito
            except:
                _email = ""

            _id = id
            _ragioneSociale = daoAgente.ragione_sociale or ''
            _nome = daoAgente.nome or ''
            _cognome = daoAgente.cognome or ''

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,
            "email":_email}

# ---

# Usate nel custom widget CustomComboBoxModify
def on_combobox_agente_search_clicked(combobox, callName=None):
    """
    Richiama la ricerca degli agenti
    """

    def refresh_combobox_agente(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiAgente(id)
        if res["ragioneSociale"] != '':
            combobox.refresh(id, res["ragioneSociale"], res)
        else:
            combobox.refresh(id, res["cognome"] + ' ' + res["nome"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaAgenti import RicercaAgenti
        anag = RicercaAgenti()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_agente)
    elif callName is not None:
        callName()

def on_combobox_vettore_search_clicked(combobox, callName=None):
    """
    richiama la ricerca dei vettori
    """

    def refresh_combobox_vettore(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiVettore(id)
        if res["ragioneSociale"] != '':
            combobox.refresh(id, res["ragioneSociale"], res)
        else:
            combobox.refresh(id, res["cognome"] + ' ' + res["nome"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaVettori import RicercaVettori
        anag = RicercaVettori()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_vettore)
    elif callName is not None:
        callName()


def on_combobox_magazzino_search_clicked(combobox, callName=None):
    """
    richiama la ricerca dei magazzini
    """

    def refresh_combobox_magazzino(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiMagazzino(id)
        combobox.refresh(id, res["denominazione"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaMagazzini import RicercaMagazzini
        anag = RicercaMagazzini()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_magazzino)
    elif callName is not None:
        callName()


def on_combobox_azienda_search_clicked(combobox, callName=None):
    """
    Richiama la ricerca delle aziende
    """

    def refresh_combobox_azienda(anagWindow):
        if anag.dao is None:
            schema = None
        else:
            schema = anag.dao.schemaa
        res = leggiAzienda(schema)
        combobox.refresh(schema, res["denominazione"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaAziende import RicercaAziende
        anag = RicercaAziende()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_azienda)
    elif callName is not None:
        callName()

def on_combobox_cliente_search_clicked(combobox, callName=None):
    """
    richiama la ricerca dei clienti
    """

    def refresh_combobox_cliente(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiCliente(id)
        if res["ragioneSociale"] != '':
            combobox.refresh(id, res["ragioneSociale"], res)
        else:
            combobox.refresh(id, res["cognome"] + ' ' + res["nome"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaClienti import RicercaClienti
        anag = RicercaClienti()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_cliente)
    elif callName is not None:
        callName()


def on_combobox_fornitore_search_clicked(combobox, callName=None):
    """
    richiama la ricerca dei fornitore
    """

    def refresh_combobox_fornitore(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiFornitore(id)
        if res["ragioneSociale"] != '':
            combobox.refresh(id, res["ragioneSociale"], res)
        else:
            combobox.refresh(id, res["cognome"] + ' ' + res["nome"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaFornitori import RicercaFornitori
        anag = RicercaFornitori()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_fornitore)
    elif callName is not None:
        callName()




def findIdFromCombobox(combobox):
    """
    Restituisce l' id relativo alla riga selezionata in un elenco a discesa
    """

    model = combobox.get_model()
    iterator = combobox.get_active_iter()
    if iterator is not None:
        id = model.get_value(iterator, 1)
        if id == 0:
            return None
        else:
            return id
    else:
        return None

def on_id_aliquota_iva_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle aliquote iva
    """

    def on_anagrafica_aliquote_iva_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxAliquoteIva(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaAliquoteIva import AnagraficaAliquoteIva
    anag = AnagraficaAliquoteIva()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_aliquote_iva_destroyed)


def on_id_categoria_articolo_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle categorie articoli
    """

    def on_anagrafica_categorie_articoli_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategorieArticoli(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
    anag = AnagraficaCategorieArticoli()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_categorie_articoli_destroyed)


def on_id_famiglia_articolo_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica delle famiglie articoli
    """

    def on_anagrafica_famiglie_articoli_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxFamiglieArticoli(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
    anag = AnagraficaFamiglieArticoli()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_famiglie_articoli_destroyed)


def on_id_imballaggio_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica degli imballaggi
    """

    def on_anagrafica_imballaggi_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxImballaggi(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaImballaggi import AnagraficaImballaggi
    anag = AnagraficaImballaggi()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_imballaggi_destroyed)


def on_id_categoria_cliente_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle categorie clienti
    """

    def on_anagrafica_categorie_clienti_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategorieClienti(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaCategorieClienti import AnagraficaCategorieClienti
    anag = AnagraficaCategorieClienti()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_categorie_clienti_destroyed)


def on_id_categoria_fornitore_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle categorie fornitori
    """

    def on_anagrafica_categorie_fornitori_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategorieFornitori(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
    anag = AnagraficaCategorieFornitori()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_categorie_fornitori_destroyed)


def on_id_categoria_contatto_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle categorie contatti
    """

    def on_anagrafica_categorie_contatti_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategorieContatti(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaCategorieContatti import AnagraficaCategorieContatti
    anag = AnagraficaCategorieContatti()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_categorie_contatti_destroyed)


def on_id_magazzino_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica dei magazzini
    """

    def on_anagrafica_magazzini_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxMagazzini(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaMagazzini import AnagraficaMagazzini
    anag = AnagraficaMagazzini()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_magazzini_destroyed)


def on_id_multiplo_customcombobox_clicked(widget, button, idArticolo):
    """
    richiama l'anagrafica dei multipli
    """

    def on_anagrafica_multipli_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxMultipli(widget.combobox, idArticolo)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaMultipli import AnagraficaMultipli
    anag = AnagraficaMultipli(idArticolo)

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_multipli_destroyed)


def on_id_listino_customcombobox_clicked(widget, button, idArticolo=None, idListino=None):
    """
    richiama l'anagrafica dei listini
    """

    def on_anagrafica_listini_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        id = findIdFromCombobox(widget.combobox)
        fillComboboxListini(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)
        widget.button.set_active(False)


    if widget.button.get_property('active') is False:
        return

    if idArticolo is not None:
        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(idArticolo, idListino)
    else:
        from AnagraficaListini import AnagraficaListini
        anag = AnagraficaListini()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_listini_destroyed)


def on_id_fornitura_customcombobox_clicked(widget, button, idArticolo, idFornitore):
    """
    richiama l'anagrafica delle forniture
    """

    def on_anagrafica_forniture_destroyed(window):
        widget.button.set_active(False)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaForniture import AnagraficaForniture
    anag = AnagraficaForniture(idArticolo, idFornitore)

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_forniture_destroyed)


def on_id_pagamento_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica dei pagamenti
    """

    def on_anagrafica_pagamenti_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxPagamenti(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaPagamenti import AnagraficaPagamenti
    anag = AnagraficaPagamenti()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_pagamenti_destroyed)


def on_id_banca_customcombobox_clicked(widget, button):
    """
    richiama l'anagrafica delle banche
    """

    def on_anagrafica_banche_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxBanche(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaBanche import AnagraficaBanche
    anag = AnagraficaBanche()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_banche_destroyed)


def on_id_destinazione_merce_customcombobox_clicked(widget, button, idCliente):
    """
    richiama l'anagrafica delle destinazioni merce
    """

    def on_anagrafica_destinazioni_merce_destroyed(window):
        """
        all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxDestinazioniMerce(widget.combobox, idCliente)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaDestinazioniMerce import AnagraficaDestinazioniMerce
    anag = AnagraficaDestinazioniMerce(idCliente)

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_destinazioni_merce_destroyed)

#


# Usate nel custom widget CustomComboBoxSearch


def insertComboboxSearchArticolo(combobox, idArticolo, clear=False, filter=True):
    res = leggiArticolo(idArticolo)
    combobox.refresh(idArticolo, res["denominazione"], res, clear, filter)


def insertComboboxSearchFornitore(combobox, idFornitore, clear=False, filter=True):
    res = leggiFornitore(idFornitore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idFornitore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idFornitore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchCliente(combobox, idCliente, clear=False, filter=True):
    res = leggiCliente(idCliente)
    if res["ragioneSociale"] != '':
        combobox.refresh(idCliente, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idCliente, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchVettore(combobox, idVettore, clear=False, filter=True):
    res = leggiVettore(idVettore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idVettore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idVettore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchMagazzino(combobox, idMagazzino, clear=False, filter=True):
    res = leggiMagazzino(idMagazzino)
    combobox.refresh(idMagazzino, res["denominazione"], res, clear, filter)


def insertComboboxSearchAzienda(combobox, schemaAzienda, clear=False, filter=True):
    res = leggiAzienda(schemaAzienda)
    combobox.refresh(schemaAzienda, res["denominazione"], res, clear, filter)


def insertComboboxSearchAgente(combobox, idAgente, clear=False, filter=True):
    res = leggiAgente(idAgente)
    if res["ragioneSociale"] != '':
        combobox.refresh(idAgente, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idAgente, res["cognome"] + ' ' + res["nome"], res, clear, filter)



def insertComboboxSearchArticolo(combobox, idArticolo, clear=False, filter=True):
    res = leggiArticolo(idArticolo)
    combobox.refresh(idArticolo, res["denominazione"], res, clear, filter)


def insertComboboxSearchFornitore(combobox, idFornitore, clear=False, filter=True):
    res = leggiFornitore(idFornitore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idFornitore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idFornitore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchCliente(combobox, idCliente, clear=False, filter=True):
    res = leggiCliente(idCliente)
    if res["ragioneSociale"] != '':
        combobox.refresh(idCliente, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idCliente, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchVettore(combobox, idVettore, clear=False, filter=True):
    res = leggiVettore(idVettore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idVettore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idVettore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchMagazzino(combobox, idMagazzino, clear=False, filter=True):
    res = leggiMagazzino(idMagazzino)
    combobox.refresh(idMagazzino, res["denominazione"], res, clear, filter)


def insertComboboxSearchAzienda(combobox, schemaAzienda, clear=False, filter=True):
    res = leggiAzienda(schemaAzienda)
    combobox.refresh(schemaAzienda, res["denominazione"], res, clear, filter)


def insertComboboxSearchAgente(combobox, idAgente, clear=False, filter=True):
    res = leggiAgente(idAgente)
    if res["ragioneSociale"] != '':
        combobox.refresh(idAgente, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idAgente, res["cognome"] + ' ' + res["nome"], res, clear, filter)

# Routines di calcolo e conversione


def calcolaListinoDaRicarico(costo=0, ricarico=0, iva=0):
    """
    Calcola il prezzo di vendita a partire dal costo, dal ricarico e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo � anche il valore di ritorno
    """
    if costo is None:
        costo = 0
    if ricarico is None:
        ricarico = 0
    if iva is None:
        iva = 0
    if costo.__class__ == Decimal and ricarico.__class__ == Decimal and iva.__class__ == Decimal:
        return costo * (1 + (ricarico / 100)) * (1 + (iva / 100))
    else:
        return float(costo * (1 + (ricarico / 100)) * (1 + (iva / 100)))


def calcolaRicarico(costo=0, listino=0, iva=0):
    """
    Calcola il ricarico a partire dal costo, dal prezzo di vendita e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo � anche il valore di ritorno
    """
    if costo is None:
        costo = 0
    if listino is None:
        listino = 0
    if iva is None:
        iva = 0
    if costo.__class__ == Decimal and listino.__class__ == Decimal and iva.__class__ == Decimal:
        if costo == 0:
            return Decimal('0')
        else:
            return (((100 * 100) * listino) / (costo * (iva + 100))) - 100
    else:
        if costo == 0:
            return 0
        return float((((100 * 100) * listino) / (costo * (iva + 100))) - 100)


def calcolaListinoDaMargine(costo=0, margine=0, iva=0):
    """
    Calcola il prezzo di vendita a partire dal costo, dal margine e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if costo is None:
        costo = 0
    if margine is None:
        margine = 0
    if iva is None:
        iva = 0
    if costo.__class__ == Decimal and margine.__class__ == Decimal and iva.__class__ == Decimal:
        return (costo / (1 - (margine / 100))) * (1 + (iva / 100))
    else:
        return float((costo / (1 - (margine / 100))) * (1 + (iva / 100)))


def calcolaMargine(costo=0, listino=0, iva=0):
    """
    Calcola il margine a partire dal costo, dal prezzo di vendita e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if costo is None:
        costo = 0
    if listino is None:
        listino = 1
    if iva is None:
        iva = 0
    if costo.__class__ == Decimal and listino.__class__ == Decimal and iva.__class__ == Decimal:
        if listino == 0:
            return Decimal('0')
        return (100 - ((costo * 100) / ((listino * 100) / (iva + 100))))
    else:
        if listino == 0:
            return 0
        return float(100 - ((costo * 100) / ((listino * 100) / (iva + 100))))


def calcolaMargineDaRicarico(ricarico=0):
    """
    Calcola il margine dal ricarico
    sel l'argomento è un oggetto Decimal, lo è anche il valore di ritorno
    """
    if ricarico is None:
        ricarico = 0
    if ricarico.__class__ == Decimal:
        return ricarico / (1 + (ricarico / 100))
    return float(ricarico / (1 + (ricarico / 100)))


def calcolaRicaricoDaMargine(margine=0):
    """
    Calcola il ricarico dal margine
    sel l'argomento è un oggetto Decimal, lo è anche il valore di ritorno
    """
    if margine is None:
        margine = 0
    if margine.__class__ == Decimal:
        return margine / (1 - (margine / 100))
    else:
        return float(margine / (1 - (margine / 100)))


def calcolaPrezzoIva(prezzo=0, iva=0):
    """
    Calcola un prezzo ivato (iva > 0) o scorpora l'iva da un prezzo (iva < 0)
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if prezzo is None:
        prezzo = 0
    if iva is None:
        iva = 0
    if prezzo.__class__ == Decimal and iva.__class__ == Decimal:
        if iva <0:
            return (100*prezzo)/(abs(iva)+100)
        else:
            return prezzo*(1+(iva/100))
    else:
        if iva < 0:
            return float((int(100) * float(prezzo)) / float((abs(iva) + int(100))))
        else:
            return float(prezzo * (1 + (iva / 100)))


def emptyStringToNone(string):
    """
    Restituisce None se la stringa e' nulla
    """
    if string == '':
        return None
    else:
        return string


def prepareFilterString(string=None):
    """
    Tratta una stringa prima di essere passata come parametro in un filtro:
    Restituisce None se la stringa e' nulla e sostituisce un apice con la relativa sequenza di escape
    """
    if (string or '') == '':
        return ""
    else:
        return string.replace('\'', '\\\'')


def dateToString(data):
    """
    Converte una data in stringa
    """
    if data is None:
        return ''
    else:
        try:
            s = string.zfill(str(data.day),2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4)
        except Exception:
            s = ''
        return s


def stringToDate(stringa):
    """
    Converte una stringa in data
    """
    if stringa is None or stringa == '':
        return None
    else:
        try:
            d = time.strptime(stringa, "%d/%m/%Y")
            data = datetime.date(d[0], d[1], d[2])
        except Exception:
            data=None
        return data

def stringToDateBumped(stringa):
    """
    Converte una stringa in data
    """
    if stringa is None or stringa == '':
        return None
    else:
        try:
            d = time.strptime(stringa, "%d/%m/%Y")
            data = datetime.date(d[0], d[1], d[2]+1)
        except Exception:
            data=None
        return data



def dateTimeToString(data):
    """
    Converte una data + ora in stringa
    """
    if data is None:
        return ''
    else:
        try:
            s = string.zfill(str(data.day), 2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4) + ' ' + string.zfill(str(data.hour),2) + ':' + string.zfill(str(data.minute),2)
        except Exception:
            s = ''
        return s


def stringToDateTime(stringa):
    """
    Converte una stringa in data + ora
    """
    if stringa is None or stringa == '':
        return None
    else:
        try:
            d = time.strptime(stringa, "%d/%m/%Y %H:%M")
            data = datetime.datetime(d[0], d[1], d[2], d[3], d[4])
        except Exception:
            data=None
        return data

def getScadenza(data_documento, ngiorniscad, FM = True):
    """
    Ritorna la data di scadenza in base alla data del documento, al numero di giorni
    della scadenza e se la scadenza e` da considerarsi fine mese.
    """
    if FM:
        import calendar
        # Spiegazione algoritmo per eventuali modifiche:
        # Salvo a parte il mese e l'anno della scadenza presunta;
        # Salvo a parte il numero di giorni del mese presunto della scadenza, e lo converto in data;
        # Cosi` facendo ottengo la fine del mese.
        data_scadenza_provvisoria = data_documento + datetime.timedelta(ngiorniscad)
        mese_scadenza = data_scadenza_provvisoria.month
        anno_scadenza = data_scadenza_provvisoria.year
        giornimesescadenza = calendar.monthrange(anno_scadenza, mese_scadenza)
        data_ultimo_del_mese = datetime.date(anno_scadenza, mese_scadenza, giornimesescadenza[1])
        return data_ultimo_del_mese
    else:
        data_scadenza = data_documento + datetime.timedelta(ngiorniscad)
        return data_scadenza

def getScontiFromDao(daoSconti = [], daoApplicazione = 'scalare'):
    applicazione = 'scalare'
    sconti = []

    if daoApplicazione == 'scalare' or daoApplicazione == 'non scalare':
        applicazione = daoApplicazione
    if daoSconti:
        for s in daoSconti:
            sconti.append({"valore": s.valore, "tipo": s.tipo_sconto})

    return (sconti, applicazione)

def getMisureFromRiga(daoMisura = []):
    misura = []

    for s in daoMisura:
        misura.append({"altezza": s.altezza, "larghezza": s.larghezza, "pezzi_moltiplicatore": s.moltiplicatore})

    return (misura)

def getDato(dictMisura, dato):
    returned = ''
    for s in dictMisura:
        returned = s[dato]
    return returned

def getStringaSconti(listSconti):
    stringaSconti = ''
    for s in listSconti:
        decimals = '2'
        tipo = s["tipo"]
        if tipo == 'percentuale':
            tipo = '%'
        elif tipo == 'valore':
            tipo = ''
            decimals = Environment.conf.decimals
        valore = ('%.' + str(decimals) + 'f') % float(s["valore"])
        stringaSconti = stringaSconti + valore + tipo + '; '
    return stringaSconti

def getDynamicStrListStore(length):
    """return a gtk.ListStore of the specified lenght"""
    string1 = 'list = gtk.ListStore(str'
    string2 = ', str' * (length -1)
    string3 = ')'
    string4 = string1+string2+string3
    exec string4
    return list


def setFileName(filename, ext, returnName = False):
    """Verify that the filename have the extension "ext"

    If not, it will append the extension to the end of the filename."""
    name = os.path.split(filename)
    _filename = os.path.splitext(name[1])
    _ext = _filename[1].upper()[1:]

    if _ext == ext.upper():
        if returnName:
            return name[1]
        else:
            return filename

    else:
        if returnName:
            return _filename[0]+'.'+ext.lower()
        else:
            _name = name[0]+os.path.sep+_filename[0]+'.'+ext.lower()
            return _name



def showAnagraficaRichiamata(returnWindow, anagWindow, button=None, callName=None):

    def on_anagrafica_richiamata_destroy(anagWindow):
        if anagWindow in Login.windowGroup:
            Login.windowGroup.remove(anagWindow)
##        Login.windowGroup.append(anagReturn)
        if button is not None:
            if isinstance(button, gtk.ToggleButton):
                button.set_active(False)
        if callName is not None:
            callName()

    anagReturn = returnWindow
    anagWindow.connect("destroy",
                       on_anagrafica_richiamata_destroy)
    anagWindow.set_transient_for(anagReturn)
##    Login.windowGroup.remove(anagReturn)
    if anagWindow not in Login.windowGroup:
        Login.windowGroup.append(anagWindow)
    anagWindow.show_all()


def obligatoryField(window, widget=None, msg=None):
    if msg is None:
        msg = 'Campo obbligatorio !'
    dialog = gtk.MessageDialog(window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
    dialog.run()
    dialog.destroy()
    if widget is not None:
        if widget.get_property("can-focus"):
            widget.grab_focus()
    raise Exception, 'Operation aborted'


def showComplexQuestion(parentWindow, message):
    """
    MessageBox alla quale si puo' rispondere con Si/No/Tutti/Nessuno
    """
    dialog = gtk.Dialog('Attenzione',
                        parentWindow,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        None)
    hbox = gtk.HBox()
    image = gtk.image_new_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    image.set_padding(10,10)
    label = gtk.Label(message)
    label.set_justify(gtk.JUSTIFY_LEFT)
    label.set_alignment(0,0)
    label.set_padding(15,10)
    hbox.pack_start(image, False, False, 0)
    hbox.pack_start(label, True, True, 0)
    dialog.vbox.pack_start(hbox, True, True, 0)

    buttonYes = gtk.Button(stock=gtk.STOCK_YES)
    buttonNo = gtk.Button(stock=gtk.STOCK_NO)
    buttonAll = gtk.Button(stock=gtk.STOCK_MEDIA_NEXT)
    alignmentAll = buttonAll.get_children()[0]
    hboxAll = alignmentAll.get_children()[0]
    imageAll, labelAll = hboxAll.get_children()
    labelAll.set_text('S_i a tutti')
    labelAll.set_use_underline(True)
    buttonNone = gtk.Button(stock=gtk.STOCK_MEDIA_FORWARD)
    alignmentNone = buttonNone.get_children()[0]
    hboxNone = alignmentNone.get_children()[0]
    imageNone, labelNone = hboxNone.get_children()
    labelNone.set_text('N_o a tutti')
    labelNone.set_use_underline(True)
    dialog.add_action_widget(buttonYes, gtk.RESPONSE_YES)
    dialog.add_action_widget(buttonNo, gtk.RESPONSE_NO)
    dialog.add_action_widget(buttonAll, gtk.RESPONSE_APPLY)
    dialog.add_action_widget(buttonNone, gtk.RESPONSE_REJECT)

    dialog.show_all()
    result = dialog.run()
    dialog.destroy()
    return result


def destroy_event(window):
    """
    Send a 'destroy-event' to the specified gtk.Window
    """
    event = gtk.gdk.Event(gtk.gdk.DESTROY)

    event.send_event = True
    event.window = window.window

    gtk.main_do_event(event)

def insertFileTypeChooser(filechooser,typeList):
    fc_vbox = gtk.VBox(True, spacing=5)
    hbox1 = gtk.HBox(False,10)
    label = gtk.Label()
    label.set_markup(str='<b><u>Salva in formato</u></b>')
    hbox1.pack_start(label, False, False, 5)
    fc_vbox.pack_start(hbox1, False, False)
    cb_model = gtk.ListStore(str,str)
    for type in typeList:
        cb_model.append(type)
    renderer = gtk.CellRendererText()
    combobox = gtk.ComboBox(model=cb_model)
    combobox.clear()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 1)
    combobox.set_model(cb_model)
    hbox1.pack_start(combobox, False, False, 5)
##    fc_vbox.pack_start(hbox2)
    filechooser.vbox.pack_end(fc_vbox, False, False, 10)
    return combobox

def multilinedirtywork( param):
    for i in param:
        try:
            lista = i['righe']
            for x in lista:
                try:
                    if '\n' in x["descrizione"]:
                        desc= x["descrizione"].split("\n")
                        o = lista.index(x)
                        lista.remove(x)
                        lung = len(desc)-1
                        for d in desc:
                            p = desc.index(d)
                            c = x.copy()
                            if p < lung:
                                for k,v in c.iteritems():
                                    c[k] = ""
                            c["descrizione"] = str(d).strip()
                            lista.insert(o+p,c)
                except:
                    pass
        except:
            pass
    return param


def on_status_activate(status, windowGroup, visible, blink, screens):
    """ on press systray icon widget hide or show """
    if visible == 1:
        visible = 0
        screens = []
        for window in windowGroup:
                screens.append(window.get_screen())
                window.hide_all()
        return (visible,blink, screens)
    else:
        visible = 1
        ind = 0
        for window in windowGroup:
            window.set_screen(screens[ind])
            ind += 1
            window.show_all()
        screens = []
        return (visible,blink,screens)

def getDateRange(string):
    """
    returns a set of two timestamps one at beginning and at the end of
    the year indicated by string (it must be placed on the last 4 characters of the string) (01/01/YEAR, 31/12/YEAR)
    """
    capodanno = '01/01/'+string[-4:]
    san_silvestro = '31/12/'+string[-4:]
    begin_date = stringToDate(capodanno)
    end_date = stringToDate(san_silvestro)
    return (begin_date, end_date)

def checkCodFisc(codfis):
    codfis.upper()
    a = re.compile('^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$')
    t = a.match(codfis)
    if t:
        return True
    else:
        c = checkPartIva(codfis)
    if  c:
        return True
    else:

        msg = 'Attenzione Codice Fiscale formalmente scorretto\nricontrolla!!!'
        dialog = gtk.MessageDialog(None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK,
                                msg)
        dialog.run()
        dialog.destroy()
        return False

def checkPartIva(partitaIVA):
    def dialog():
        msg = 'Attenzione Partita Iva formalmente scorretto\nricontrolla!!!'
        dialog = gtk.MessageDialog(None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK,
                                msg)
        dialog.run()
        dialog.destroy()
    n_Val = 0
    n_Som1 = 0
    n_Som2 = 0
    lcv = 0
    if len(partitaIVA) !=11:
        dialog()
        return False
    l_ret = 0
    try:
        l_ret = int(partitaIVA)
    except:
        dialog()
        return False
    if l_ret < 0:
        dialog()
        return False
    for lcv in [0, 2, 4, 6, 8]:
        n_Val = int(partitaIVA[lcv])
        n_Som1 += n_Val
        n_Val = int(partitaIVA[lcv+1])
        n_Som1 += int((n_Val/5.0) + (n_Val<<1) % 10)
    n_Som2 = 10 - (n_Som1 % 10)
    if n_Som2==10:
        n_Som2=0
    n_Val=int(partitaIVA[10])
    if (n_Som2==n_Val):
        return True
    else:
        dialog()
        return False

def omogeneousCode(section=None, string = None):
    if section == "Clienti":
        try:
            function = Environment.conf.Clienti.omogeneus_codice
        except:
            return string
    elif section == "Fornitori":
        try:
            function = Environment.conf.Fornitori.omogeneus_codice
        except:
            return string
    elif section == "Articoli":
        try:
            function = Environment.conf.Articoli.omogeneus_codice
        except:
            return string
    elif section == "Agenti":
        try:
            function = Environment.conf.Agenti.omogeneus_codice
        except:
            return string
    elif section == "Famiglie":
        try:
            function = Environment.conf.Famiglie.omogeneus_codice
        except:
            return string
    elif section == "Vettori":
        try:
            function = Environment.conf.Vettori.omogeneus_codice
        except:
            return string
    if function =="upper":
        return string.upper()
    elif function == "capitalize":
        return string.capitalize()
    elif function == "lower":
        return string.lower()
    else:
        return string

def hasAction(actionID=None):
    idRole = Environment.usernameLoggedList[2]
    roleActions = RoleAction(isList=True).select(id_role=idRole,id_action = actionID,orderBy="id_role")
    for p in roleActions:
        if int(p.id_action) == int(actionID):
            return True
    dialog = gtk.MessageDialog( None,
                                gtk.DIALOG_MODAL |
                                gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                "Permesso negato! L'azione richiesta non è tra quelle che ti son consentite")
    response = dialog.run()
    dialog.destroy()
    return False

def numeroRegistroGet(tipo=None, date=None):
    """ Attenzione, funzione improvvisata, controllare meglio ed
        aggiungere i check sui diversi tipi di rotazione """
    from promogest.dao.TestataMovimento import TestataMovimento
    from promogest.dao.TestataDocumento import TestataDocumento
    from promogest.dao.Setting import Setting
    date = time.strftime("%Y")
    numeri = []
    #datepart= string.split(date, "/")

    _key= str(tipo+".registro").strip()
    registro = Setting(id=_key).getRecord()
    if not registro :
        raise "ATTENZIONE , Registro numerazione non trovato"

    registrovalue = registro.value
    registrovalueforrotazione = registrovalue+".rotazione"
    rotazione = Setting(isList=True).select(keys=registrovalueforrotazione)
    if not rotazione:
        print "ATTENZIONE , Registro numerazione non trovato"

    rotazione_temporale_dict = {'annuale':"year",
                                "mensile":"month",
                                "giornaliera":"day"}

    if tipo == "Movimento":
        numeroSEL = TestataMovimento(isList=True).select(complexFilter=(and_(func.date_part("year", TestataMovimento.data_movimento)==date ,
                            TestataMovimento.registro_numerazione==registrovalue)), batchSize=None, orderBy="id")

    else:
        numeroSEL = TestataDocumento(isList=True).select(complexFilter=(and_(func.date_part("year", TestataDocumento.data_documento)==date ,
                        TestataDocumento.registro_numerazione==registrovalue)), batchSize=None, orderBy="id")

    if numeroSEL:
        for num in numeroSEL:
            numeri.append(num.numero)
        numero = int(max(numeri))+1
    else:
        numero = 1
    return (numero, registrovalue)

def idArticoloFromFornitura(k,v):
    from promogest.dao.Fornitura import Fornitura
    codiciArtForFiltered =  Environment.params["session"]\
                                        .query(Fornitura)\
                                        .filter(and_(Fornitura.codice_articolo_fornitore.ilike("%"+v+"%")))\
                                        .all()
    return codiciArtForFiltered

def getCategorieContatto(id=None):
    from promogest.dao.ContattoCategoriaContatto import ContattoCategoriaContatto
    dbCategorieContatto = ContattoCategoriaContatto(isList=True).select(id=id,
                                                                    batchSize=None,
                                                                    orderBy="id_contatto")
    return dbCategorieContatto

def getRecapitiContatto(id=None):
    from promogest.dao.RecapitoContatto import RecapitoContatto
    dbRecapitiContatto = RecapitoContatto(isList=True).select(idContatto=id)
    return dbRecapitiContatto

def codeIncrement(value):

    lastNum = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

    def increment(s):
        """ look for the last sequence of number(s) in a string and increment """
        m = lastNum.search(s)
        if m:
            next = str(int(m.group(1))+1)
            start, end = m.span(1)
            s = s[:max(end-len(next), start)] + next + s[end:]
            return s

    return increment(value)

def checkCodiceDuplicato(codice=None,tipo=None):
    if tipo =="Articolo":
        from promogest.dao.Articolo import Articolo
        a = Articolo(isList=True).select(codicesatto=codice)
    elif tipo =="Clienti":
        a = Cliente(isList=True).select(codicesatto=codice)
    if a:
        msg = """Attenzione!
    Codice %s : %s  è già presente
    Inserirne un altro""" %(tipo,codice)
        dialog = gtk.MessageDialog(None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK,
                                msg)
        dialog.run()
        dialog.destroy()
        return False
    else:
        return True

