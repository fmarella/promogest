# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from textwrap import TextWrapper
import os
from threading import Timer
import hashlib
from calendar import Calendar
from decimal import *

try:
    from promogest.ui.gtk_compat import *
except:
    pass
import threading
import time
import datetime
from sqlalchemy.orm import *
from sqlalchemy import *
from promogest import Environment

import string
import re
try:
    import pysvn
except:
    pysvn = None
    print 'Modulo pysvn non trovato: gli aggiornamenti non saranno disponibili!'
import xml.etree.ElementTree as ET
import unicodedata
import urllib
import urllib2
try:
    import json
except:
    None


try:  # necessario per gestire i custom widgts con glade3 e gtkBuilder
    import Login
except:
    pass

from promogest.ui.utilsCombobox import *

# Letture per recuperare velocemente dati da uno o piu' dao correlati

def articleType(dao):
    """
    Che tipo di articolo è? Necessaria principalmente per taglie e Colore
    @param dao: Dao articolo su cui fare le verifiche
    @type dao: object
    """
    if dao and posso("PW"):
        if (dao.id) and (dao.id_articolo_taglia_colore is not None) and \
            (dao.id_articolo_padre is None) and (dao.articoliTagliaColore):
#            print "ARTICOLO FATHER"
            return "father"
        elif (dao.id) and (dao.id_articolo_taglia_colore is not None) and \
                        (dao.id_articolo_padre_taglia_colore is not None):
#            print "ARTICOLO SON"
            return "son"
        elif (dao.id) and (dao.id_articolo_taglia_colore is not None) and\
         (dao.id_articolo_padre is None) and (not dao.articoliTagliaColore):
#            print "ARTICOLO PLUS"
            return "plus"
        elif (dao.id) and (dao.id_articolo_taglia_colore is None) and\
         (dao.id_articolo_padre is None) and (not dao.articoliTagliaColore):
#            print "ARTICOLO NORMAL"
            return "normal"
        elif not dao.id:
#            print "ARTICOLO NEW NORMAL"
            return "new"


def leggiArticolo(id, full=False, idFornitore=False, data=None):
    """
    Restituisce un dizionario con le informazioni sull'articolo letto
    """
    from promogest.dao.Articolo import Articolo
    _id = None
    _denominazione = ''
    _codice = ''
    _denominazioneBreveAliquotaIva = ''
    _percentualeAliquotaIva = 0
    _idAliquotaIva = None
    _idUnitaBase = None
    _unitaBase = ''
    _quantita_minima = ''
    artiDict = {}
    daoArticolo = None
    _codicearticolofornitore = ""
    if id is not None:
        if posso("PW"):
            from promogest.modules.PromoWear.ui.PromowearUtils import leggiArticoloPromoWear
            artiDict = leggiArticoloPromoWear(id)
            return artiDict
        daoArticolo = Articolo().getRecord(id=id)
        if daoArticolo is not None:
            _id = id
            _denominazione = daoArticolo.denominazione or ''
            _codice = daoArticolo.codice or ''
            _idUnitaBase = daoArticolo.id_unita_base
            _codicearticolofornitore = daoArticolo.codice_articolo_fornitore
            _denominazioneBreveAliquotaIva = daoArticolo.denominazione_breve_aliquota_iva
            _percentualeAliquotaIva = daoArticolo.percentuale_aliquota_iva
            _idAliquotaIva = daoArticolo.id_aliquota_iva
            _unitaBase = daoArticolo.denominazione_breve_unita_base
            try:
                _quantita_minima = daoArticolo.quantita_minima
            except:
                _quantita_minima = ""

    artiDict = {"id": _id,
                "denominazione": _denominazione,
                "codice": _codice,
                "denominazioneBreveAliquotaIva": _denominazioneBreveAliquotaIva,
                "percentualeAliquotaIva": _percentualeAliquotaIva,
                "idAliquotaIva":_idAliquotaIva,
                "idUnitaBase": _idUnitaBase,
                "unitaBase": _unitaBase,
                "quantita_minima": _quantita_minima,
                "codicearticolofornitore":_codicearticolofornitore,
                "daoArticolo":daoArticolo}
    return artiDict


def leggiCliente(id):
    """
    Legge un Dao restituisce un dizionario della tabella cliente con alcune
    property risolte
    """
    from promogest.dao.Cliente import Cliente

    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''
    _id_pagamento = None
    _id_magazzino = None
    _id_listino = None
    _id_banca = None
    _id_aliquota_iva = None
    _email = None
    _pagante = False
    if id is not None:
        daoCliente = Cliente().getRecord(id=id)
        if daoCliente:
            _id = id
            _ragioneSociale = daoCliente.ragione_sociale or ''
            _nome = daoCliente.nome or ''
            _cognome = daoCliente.cognome or ''
            _id_pagamento = daoCliente.id_pagamento
            _id_magazzino = daoCliente.id_magazzino
            _id_listino = daoCliente.id_listino
            _id_banca = daoCliente.id_banca
            _id_aliquota_iva = daoCliente.id_aliquota_iva
            _pagante = daoCliente.pagante
            _email = daoCliente.email_principale or ''

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,
            "id_pagamento": _id_pagamento,
            "id_magazzino": _id_magazzino,
            "id_listino": _id_listino,
            "id_banca": _id_banca,
            "id_aliquota_iva": _id_aliquota_iva,
            "email": _email,
            "pagante": _pagante}


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

    if id is not None:
        daoDestinazioneMerce = DestinazioneMerce().getRecord(id=id)
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
        daoFornitore = Fornitore().getRecord(id=id)
        if daoFornitore:

            _id = id
            _ragioneSociale = daoFornitore.ragione_sociale or ''
            _nome = daoFornitore.nome or ''
            _cognome = daoFornitore.cognome or ''
            _id_pagamento = daoFornitore.id_pagamento
            _id_magazzino = daoFornitore.id_magazzino
            _email = daoFornitore.email_principale or ''

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,
            "id_pagamento": _id_pagamento,
            "id_magazzino": _id_magazzino,
            "email":_email}


def leggiVettore(id):
    """
    Restituisce un dizionario con le informazioni sul vettore letto
    """
    from promogest.dao.Vettore import Vettore
    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''

    if id is not None:
        daoVettore = Vettore().getRecord(id=id)
        if daoVettore is not None:
            _id = id
            _ragioneSociale = daoVettore.ragione_sociale or ''
            _nome = daoVettore.nome or ''
            _cognome = daoVettore.cognome or ''

    return {"id": _id,
            "ragioneSociale": _ragioneSociale,
            "nome": _nome,
            "cognome": _cognome,}


def leggiContatto(id):
    """
    Restituisce un dizionario con le informazioni sul contatto letto
    """
    from promogest.dao.daoContatti.Contatto import Contatto
    _id = None
    _nome = ''
    _cognome = ''
    _email = ''

    if id is not None:
        daoContatto = Contatto().select(id=id)
        if daoContatto is not None:
            try:
                for i in range(0,len(daoContatto[0].recapiti)):
                    if daoContatto[0].recapiti[i].tipo_recapito == "E-Mail" or daoContatto[0].recapiti[i].tipo_recapito == "Email":
                        _email = daoContatto[0].recapiti[i].recapito
            except:
                _email = ""
                daoContatto[0].recapiti[0].tipo_recapito
            _id = id
            _nome = daoContatto[0].nome or ''
            _cognome = daoContatto[0].cognome or ''
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
        daoMagazzino = Magazzino().getRecord(id=id)
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


def leggiListino(idListino=None, idArticolo=None, tiny=False):
    """
    Restituisce un dizionario con le informazioni sul listino letto
    """
    from promogest.dao.Listino import Listino
    from promogest.dao.ListinoArticolo import ListinoArticolo
    from promogest.dao.ListinoComplessoArticoloPrevalente import ListinoComplessoArticoloPrevalente
    from promogest.dao.Articolo import Articolo
    daoListinoArticolo = None

    #liss = Listino().select(batchSize=None)

    listinoDict = {"denominazione": "",
                    "prezzoIngrosso": 0,
                    "prezzoDettaglio": 0,
                    "ultimoCosto":0,
                    "complesso": False,
                    "sottoListiniID": [],
                    "scontiDettaglio":[],
                    "scontiIngrosso":[],
                    'applicazioneScontiDettaglio':None,
                    'applicazioneScontiIngrosso':[]}

    if idListino:
        daoListinoo = Listino().select(idListino=idListino, listinoAttuale=True)
        if daoListinoo:
            daoListino = daoListinoo[0]
            _denominazione = daoListino.denominazione
            _complesso = daoListino._isComplex()  #verifico se il listino è complesso
            listinoDict["denominazione"] = _denominazione
            listinoDict["complesso"] = _complesso
            if _complesso:
                _sottoListiniID = daoListino._sottoListiniIDD()
                listinoDict["sottoListiniID"] = _sottoListiniID

            if idArticolo:       #abbiamo anche un id Articolo daoListinoArticolo = None
                if _complesso:
                    #se il listino è complesso gestisco il suo listino articolo
                    daoListinoArticolo1 = ListinoArticolo().select(
                        idListino=_sottoListiniID,
                        idArticolo = idArticolo,
                        listinoAttuale = True,
                        batchSize=None,
                        orderBy=ListinoArticolo.id_listino)
                    if len(daoListinoArticolo1)>1:
                        daoListinoArticolo2 = ListinoComplessoArticoloPrevalente()\
                                .select(idListinoComplesso = idListino,
                                idArticolo = idArticolo,
                                batchSize = None)
                        if daoListinoArticolo2:
                            daoListinoArticolo = ListinoArticolo().select(
                                idListino=daoListinoArticolo2[0].id_listino,
                                idArticolo = idArticolo,
                                listinoAttuale = True,
                                batchSize = None,
                                orderBy=ListinoArticolo.id_listino)[0]
                        else:
                            daoListinoArticolo3 = ListinoArticolo().select(
                                idListino=_sottoListiniID,
                                idArticolo = idArticolo,
                                listinoAttuale = True,
                                batchSize=None,
                                orderBy=ListinoArticolo.data_listino_articolo)
                            if daoListinoArticolo3:
                                daoListinoArticolo = daoListinoArticolo1[-1]

                    elif daoListinoArticolo1:
                        daoListinoArticolo = daoListinoArticolo1[0]
                    else:
                        daoListinoArticolo = None

                else:  #listino normale
                    daoListinoArticolo1 = ListinoArticolo().select(join=Articolo,idListino=idListino,
                                                            idArticolo = idArticolo,
                                                            listinoAttuale = True,
                                                            batchSize=None,
                                                            #orderBy=ListinoArticolo.id_listino
                                                            )
                    if not daoListinoArticolo1 and posso("PW"):

                        father = Articolo().getRecord(id=idArticolo)
                        idArticolo = father.id_articolo_padre
                        #riprovo la query con l'id del padre, potrebbe essere un figlio
                        daoListinoArticolo1 = ListinoArticolo().select(idListino=idListino,
                                                            idArticolo = idArticolo,
                                                            listinoAttuale = True,
                                                            batchSize=None,
                                                            orderBy=ListinoArticolo.id_listino)
                    if len(daoListinoArticolo1) >= 1:
                        #PIÙ DI UN LISTINO ARTICOLO ATTUALE" prendo il primo
                        daoListinoArticolo= daoListinoArticolo1[0]
                    else:
                        daoListinoArticolo = None

                if daoListinoArticolo:
                    if tiny:
                        listinoDict["prezzoIngrosso"] = daoListinoArticolo.prezzo_ingrosso or 0
                        listinoDict["prezzoDettaglio"] = daoListinoArticolo.prezzo_dettaglio or 0
                        return listinoDict
                    _prezzoIngrosso = daoListinoArticolo.prezzo_ingrosso
                    _prezzoDettaglio = daoListinoArticolo.prezzo_dettaglio
                    _ultimoCosto = daoListinoArticolo.ultimo_costo
                    _scontiDettaglio = daoListinoArticolo.sconto_vendita_dettaglio
                    _scontiIngrosso = daoListinoArticolo.sconto_vendita_ingrosso
                    _applicazioneDettaglio = daoListinoArticolo.applicazione_sconti_dettaglio
                    _applicazioneIngrosso = daoListinoArticolo.applicazione_sconti_ingrosso

                    listinoDict["prezzoIngrosso"] = _prezzoIngrosso or 0
                    listinoDict["prezzoDettaglio"] = _prezzoDettaglio or 0
                    listinoDict["ultimoCosto"] = _ultimoCosto or 0
                    listinoDict["scontiDettaglio"] = _scontiDettaglio
                    listinoDict["scontiIngrosso"] = _scontiIngrosso
                    listinoDict['applicazioneScontiDettaglio'] = _applicazioneDettaglio
                    listinoDict['applicazioneScontiIngrosso'] = _applicazioneIngrosso

    return listinoDict


def leggiFornitura(idArticolo, idFornitore=None, data=None, noPreferenziale=False):
    """
    Restituisce un dizionario con le informazioni sulla fornitura letta
    """
    from promogest.dao.Fornitura import Fornitura
    from promogest.dao.ScontoFornitura import ScontoFornitura
    _prezzoLordo = 0
    _prezzoNetto = 0
    _sconti = []
    _applicazioneSconti = 'scalare'
    _codiceArticoloFornitore = ''
    _numeroLottoArticoloFornitura = None
    _dataScadenzaArticoloFornitura = None
    _dataProduzioneArticoloFornitura = None
    _dataPrezzoFornitura = None
    _ordineMinimoFornitura = None
    _tempoArrivoFornitura = None

    if (idArticolo is not None):
        fors = Fornitura().select(idArticolo=idArticolo,
                                    idFornitore=idFornitore,
                                    #daDataFornitura=None,
                                    aDataFornitura=data,
                                    #daDataPrezzo=None,
                                    #aDataPrezzo=data,
                                    #codiceArticoloFornitore=None,
                                    orderBy = 'data_fornitura',
                                    #offset = None,
                                    batchSize = None)
        if not fors:
            fors = Fornitura().select(idArticolo=idArticolo,
                            idFornitore=idFornitore,
                            #daDataFornitura=None,
                            #aDataFornitura=None,
                            #daDataPrezzo=None,
                            aDataPrezzo=data,
                            #codiceArticoloFornitore=None,
                            orderBy = 'data_prezzo',
                            #offset = None,
                            batchSize = None)
        if not fors:
            fors = Fornitura().select(idArticolo=idArticolo,
                            idFornitore=idFornitore,
                            #daDataFornitura=None,
                            #aDataFornitura=None,
                            #daDataPrezzo=None,
                            #aDataPrezzo=data,
                            #codiceArticoloFornitore=None,
                            orderBy = 'data_prezzo',
                            #offset = None,
                            batchSize = None)
        fornitura = None
        if idFornitore:
#            print "FOOOOOOOOOOOOOOOOOOOOORSA2", fors
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
            _numeroLottoArticoloFornitura = fornitura.numero_lotto or None
            _dataScadenzaArticoloFornitura = dateToString(fornitura.data_scadenza) or None
            _dataProduzioneArticoloFornitura = dateToString(fornitura.data_produzione) or None
            _dataPrezzoFornitura = dateToString(fornitura.data_prezzo) or None
            _ordineMinimoFornitura = fornitura.scorta_minima or None
            _tempoArrivoFornitura = fornitura.tempo_arrivo_merce or None

            idFornitura = fornitura.id
            if idFornitura is not None:
                scos = ScontoFornitura().select(join= ScontoFornitura.fornitura,
                                                            idFornitura=idFornitura,
                                                            batchSize=None)

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
            "codiceArticoloFornitore": _codiceArticoloFornitore,
            "numeroLottoArticoloFornitura": _numeroLottoArticoloFornitura,
            "dataScadenzaArticoloFornitura": _dataScadenzaArticoloFornitura,
            "dataProduzioneArticoloFornitura": _dataProduzioneArticoloFornitura,
            "dataPrezzoFornitura": _dataPrezzoFornitura,
            "ordineMinimoFornitura": _ordineMinimoFornitura,
            "tempoArrivoFornitura": _tempoArrivoFornitura

            }


def leggiOperazione(id):
    """
    Restituisce un dizionario con le informazioni sulla operazione letta
    """
    from promogest.dao.Operazione import Operazione
    _denominazione = id
    _fonteValore = ''
    _segno = ''
    _tipoPersonaGiuridica = ''
    _tipoOperazione = ""

    if id is not None:
        res = Operazione().getRecord(id=(id).strip())
        if res:
            _fonteValore = res.fonte_valore or ''
            _segno = res.segno or ''
            _tipoPersonaGiuridica = res.tipo_persona_giuridica or ''
            _tipoOperazione = res.tipo_operazione or ''

    return {"denominazione":_denominazione,
            "fonteValore": _fonteValore,
            "segno": _segno,
            "tipoPersonaGiuridica": _tipoPersonaGiuridica,
            "tipoOperazione": _tipoOperazione}


def leggiMultiplo(idMultiplo):
    """
    Restituisce un dizionario con le informazioni sul multiplo letto
    """
    from promogest.dao.Multiplo import Multiplo
    _denominazioneBreve = ''
    _denominazione = ''
    _moltiplicatore = 0

    if idMultiplo is not None:
        daoMultiplo = Multiplo().getRecord(id=idMultiplo)
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
    _codice_fiscale = ''
    _iban = ''
    _numero_conto = ''
    _abi = ''
    _cab = ''

    if schema is not None:
        daoAzienda = Azienda().getRecord(id=schema)
        if daoAzienda is not None:
            _schema = schema
            _denominazione = daoAzienda.denominazione or ''
            _codice_fiscale = daoAzienda.codice_fiscale or ''
            _iban = daoAzienda.iban or ''
            _abi = daoAzienda.abi or ''
            _cab = daoAzienda.cab or ''
            _numero_conto = daoAzienda.numero_conto or ''

    return {"schema": _schema,
            "denominazione": _denominazione,
            "codice_fiscale": _codice_fiscale,
            "iban": _iban,
            "abi": _abi,
            "cab": _cab,
            "numero_conto": _numero_conto
            }


def leggiAgente(id):
    """
    Restituisce un dizionario con le informazioni sul vettore letto
    """
    from  promogest.dao.daoAgenti.Agente import Agente
    _id = None
    _ragioneSociale = ''
    _nome = ''
    _cognome = ''
    _email = None

    if id is not None:
        daoAgente = Agente().getRecord(id=id)
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
        """
        FIXME
        """
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
        from promogest.ui.SimpleSearch.RicercaAgenti import RicercaAgenti
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
        """
        FIXME
        """
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
        from promogest.ui.SimpleSearch.RicercaVettori import RicercaVettori
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
        """
        FIXME
        """
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
        from promogest.ui.SimpleSearch.RicercaMagazzini import RicercaMagazzini
        anag = RicercaMagazzini()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide", refresh_combobox_magazzino)
    elif callName is not None:
        callName()


def on_combobox_azienda_search_clicked(combobox, callName=None):
    """
    Richiama la ricerca delle aziende
    """

    def refresh_combobox_azienda(anagWindow):
        """
        FIXME
        """
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
    richiama la ricerca dei clienti per esempio nel form contatti
    """

    def refresh_combobox_cliente(anagWindow):
        """ """
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
        from promogest.ui.SimpleSearch.RicercaClienti import RicercaClienti
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
        """
        """
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
        from promogest.ui.SimpleSearch.RicercaFornitori import RicercaFornitori
        anag = RicercaFornitori()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_fornitore)
    elif callName is not None:
        callName()


def permalinkaTitle(string):
    try:
        string = unicodedata.normalize("NFKD",string).encode('ascii','ignore').strip().lower()
    except:
        string = string.replace(" ","_").strip().lower()
    test = "_".join(string.split())
    badchar = []
    for char in test:
        if char not in "qwertyuiopasdfghjklzxcvbnm1234567890-_":
            badchar.append(char)
    if badchar:
        for ch in badchar:
            test = test.replace(str(ch),"")
    return test


def calcolaSaldoGeneralePrimaNota():
    from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
    #TODO Aggiungere una opzione in setconf con una data ed un saldo di partenza
#        valore = 0

    data_riporto_cassa = setconf("PrimaNota", "data_saldo_parziale_cassa_primanota")
    riporto_cassa = 0
    if data_riporto_cassa:
        tpn_cassa = TestataPrimaNota().select(daDataInizio=stringToDate(data_riporto_cassa), batchSize=None)
        riporto_cassa = setconf("PrimaNota", "valore_saldo_parziale_cassa_primanota")
        tot_cassa = calcolaTotaliPrimeNote(tpn_cassa, tipo='CASSA')

    data_riporto_banca = setconf("PrimaNota", "data_saldo_parziale_banca_primanota")
    riporto_banca = 0
    if data_riporto_banca:
        tpn_banca = TestataPrimaNota().select(daDataInizio=stringToDate(data_riporto_banca), batchSize=None)
        riporto_banca = setconf("PrimaNota", "valore_saldo_parziale_banca_primanota")
        tot_banca = calcolaTotaliPrimeNote(tpn_banca, tipo='BANCA')

    if data_riporto_cassa and data_riporto_banca:
        tot_banca['saldo_cassa'] = tot_cassa['saldo_cassa']
        tot_banca['tot_entrate_cassa'] = tot_cassa['tot_entrate_cassa']
        tot_banca['tot_uscite_cassa'] = tot_cassa['tot_uscite_cassa']
        return tot_banca
    if data_riporto_cassa:
        return tot_cassa
    if data_riporto_banca:
        return tot_banca
    tpn = TestataPrimaNota().select(batchSize=None)
    return calcolaTotaliPrimeNote(tpn, tipo='ALL')


def calcolaSaldoPeriodoPrimaNota():
    from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota

    a = Environment.a_data_inizio_primanota
    if not a:
        return None

    tpn = TestataPrimaNota().select(daDataInizio=stringToDate('01/01/' + Environment.workingYear), aDataInizio=stringToDate(a), batchSize=None)
    return calcolaTotaliPrimeNote(tpn, tipo='ALL')

def getDataFiltroPrimaNota():
    return Environment.a_data_inizio_primanota

def getRiportoBanca():
    return str(setconf("PrimaNota", "valore_saldo_parziale_banca_primanota"))

def getRiportoCassa():
    return str(setconf("PrimaNota", "valore_saldo_parziale_cassa_primanota"))

def getDenominazioneBanca(id_banca):
    from promogest.dao.Banca import Banca
    bn = Banca().getRecord(id=id_banca)
    if bn:
        return bn.denominazione
    else:
        return "Banca generica"

def leggiBanca(id_banca):
    from promogest.dao.Banca import Banca
    bn = Banca().getRecord(id=id_banca)
    if bn:
        return {"denominazione": bn.denominazione,
                "agenzia": bn.agenzia,
                "iban": bn.iban,
                "abi": bn.abi,
                "cab": bn.cab
                }
    else:
        return None

def calcolaTotaliBanche(dao, banche_entrate, banche_uscite):
    """
    Ritorna i totali entrate e uscite divisi per banca
    """
    for r in dao.righeprimanota:
        if r.tipo == 'cassa' or not r.id_banca:
            continue
        idx = str(r.id_banca)

        if r.segno == "uscita":
            if idx in banche_uscite.keys():
                banche_uscite[idx] += -1*Decimal(r.valore)
            else:
                banche_uscite[idx] = -1*Decimal(r.valore)
        elif r.segno == 'entrata':
            if idx in banche_entrate.keys():
                banche_entrate[idx] += Decimal(r.valore)
            else:
                banche_entrate[idx] = Decimal(r.valore)
        else:
            pass

    return (banche_entrate, banche_uscite)

def calcolaTotaliPrimeNote(tpn, tipo='ALL'):
    """
    """
    riporto_cassa = setconf("PrimaNota", "valore_saldo_parziale_cassa_primanota") or 0
    riporto_banca = setconf("PrimaNota", "valore_saldo_parziale_banca_primanota") or 0

    entrate_cassa = Decimal(0)
    uscite_cassa = Decimal(0)
    entrate_banca = Decimal(0)
    uscite_banca = Decimal(0)

    dict_be = {}
    dict_bu = {}

    for dao in tpn:
        t = dao.totali

        if tipo == "ALL" or tipo == 'CASSA':
            entrate_cassa += t["tot_entrate_cassa"]
            uscite_cassa += t["tot_uscite_cassa"]
        if tipo == "ALL" or tipo == 'BANCA':
            entrate_banca += t['tot_entrate_banca']
            uscite_banca += t['tot_uscite_banca']
            dict_be, dict_bu = calcolaTotaliBanche(dao, dict_be, dict_bu)

    saldo_cassa = entrate_cassa + uscite_cassa + Decimal(str(riporto_cassa))
    saldo_banca = entrate_banca + uscite_banca + Decimal(str(riporto_banca))

    return {
        'saldo_cassa': saldo_cassa,
        'saldo_banca': saldo_banca,
        'tot_entrate_cassa': entrate_cassa,
        'tot_uscite_cassa': uscite_cassa,
        'tot_entrate_banca': entrate_banca,
        'tot_uscite_banca': uscite_banca,
        'tot_entrate_per_banche': dict_be,
        'tot_uscite_per_banche': dict_bu,
        }

def findIdFromCombobox(combobox):
    """
    Restituisce l' id relativo alla riga selezionata in un elenco a discesa
    """

    model = combobox.get_model()
    iterator = combobox.get_active_iter()
    if iterator is not None:
        id = model.get_value(iterator, 1)
        if id == 0 :
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
        All'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        """
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxAliquoteIva(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from promogest.ui.AnagraficaAliquoteIva import AnagraficaAliquoteIva
    anag = AnagraficaAliquoteIva()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_aliquote_iva_destroyed)


def on_id_categoria_articolo_customcombobox_clicked(widget, button):
    """
    Richiama l'anagrafica delle categorie articoli
    """
    def on_anagrafica_categorie_articoli_destroyed(window):
        """
        """
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxCategorieArticoli(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.ui.AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
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

    from promogest.ui.AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
    anag = AnagraficaFamiglieArticoli()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_famiglie_articoli_destroyed)

def on_stadio_commessa_combobox_clicked(widget, button):
    """Richiama l'anagrafica delle categorie articoli """

    def on_anagrafica_stadio_commessa_destroyed(window):
        """    """
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxStadioCommessa(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)

    if widget.button.get_property('active') is False:
        return

    from promogest.modules.GestioneCommesse.ui.AnagraficaStadioCommessa import AnagraficaStadioCommessa
    anag = AnagraficaStadioCommessa()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_stadio_commessa_destroyed)


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

    from promogest.ui.AnagraficaImballaggi import AnagraficaImballaggi
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

    from promogest.ui.AnagraficaCategorieClienti import AnagraficaCategorieClienti
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

    from promogest.ui.AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
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

    from promogest.ui.Contatti.AnagraficaCategorieContatti import AnagraficaCategorieContatti
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

    from promogest.ui.AnagraficaMagazzini import AnagraficaMagazzini
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

    from promogest.ui.AnagraficaMultipli import AnagraficaMultipli
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
        from promogest.ui.AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(idArticolo, idListino)
    else:
        from promogest.ui.AnagraficaListini import AnagraficaListini
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
        """
        FIXME
        @param window:
        @type window:
        """
        widget.button.set_active(False)


    if widget.button.get_property('active') is False:
        return

    from promogest.ui.anagForniture.AnagraficaForniture import AnagraficaForniture
    anag = AnagraficaForniture(idArticolo, idFornitore)

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy", on_anagrafica_forniture_destroyed)


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

    from promogest.ui.AnagraficaPagamenti import AnagraficaPagamenti
    anag = AnagraficaPagamenti()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy", on_anagrafica_pagamenti_destroyed)


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

    from promogest.ui.AnagraficaBanche import AnagraficaBanche
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

    from promogest.ui.AnagraficaDestinazioniMerce import AnagraficaDestinazioniMerce
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
    """    """
    res = leggiArticolo(idArticolo)
    combobox.refresh(idArticolo, res["denominazione"], res, clear, filter)


def insertComboboxSearchFornitore(combobox, idFornitore, clear=False, filter=True):
    """    """
    res = leggiFornitore(idFornitore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idFornitore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idFornitore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchCliente(combobox, idCliente, clear=False, filter=True):
    """    """
    res = leggiCliente(idCliente)
    if res["ragioneSociale"] != '':
        combobox.refresh(idCliente, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idCliente, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchVettore(combobox, idVettore, clear=False, filter=True):
    """    """
    res = leggiVettore(idVettore)
    if res["ragioneSociale"] != '':
        combobox.refresh(idVettore, res["ragioneSociale"], res, clear, filter)
    else:
        combobox.refresh(idVettore, res["cognome"] + ' ' + res["nome"], res, clear, filter)


def insertComboboxSearchMagazzino(combobox, idMagazzino, clear=False, filter=True):
    """     """
    res = leggiMagazzino(idMagazzino)
    combobox.refresh(idMagazzino, res["denominazione"], res, clear, filter)


def insertComboboxSearchAzienda(combobox, schemaAzienda, clear=False, filter=True):
    """    """
    res = leggiAzienda(schemaAzienda)
    combobox.refresh(schemaAzienda, res["denominazione"], res, clear, filter)



def insertComboboxSearchAgente(combobox, idAgente, clear=False, filter=True):
    """    """
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
    if type(costo)==type("stringa") or costo is None:
        costo = Decimal(sanitizer(costo) or 0)
    if type(ricarico)==type("stringa") or ricarico is None:
        ricarico = Decimal(sanitizer(ricarico) or 0)
    if type(iva)==type("stringa") or iva is None:
        iva = Decimal(sanitizer(iva) or 0)
    if costo.__class__ == Decimal and ricarico.__class__ == Decimal and iva.__class__ == Decimal:
        return costo * (1 + (ricarico / 100)) * (1 + (iva / 100))
    else:
        return float(costo * (1 + (ricarico / 100)) * (1 + (iva / 100)))


def calcolaRicarico(costo=0, listino=0, iva=0):
    """
    Calcola il ricarico a partire dal costo, dal prezzo di vendita e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if type(costo)==type("stringa") or costo is None:
        costo = Decimal(sanitizer(costo) or 0)
    if type(listino)==type("stringa") or listino is None:
        listino = Decimal(sanitizer(listino) or 0)
    if type(iva)==type("stringa") or iva is None:
        iva = Decimal(sanitizer(iva) or 0)
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
    TODO: C'è da verificare la coerenza in caso di iva a zero o margine a zero
    """
    if type(costo)==type("stringa") or costo is None:
        costo = Decimal(sanitizer(costo) or 0)
    if type(margine)==type("stringa") or margine is None:
        margine = Decimal(sanitizer(margine) or 0)
    if type(iva)==type("stringa") or iva is None:
        iva = Decimal(sanitizer(iva) or 0)

    if costo.__class__ == Decimal and margine.__class__ == Decimal and iva.__class__ == Decimal:
        return (costo / (1 - (margine / 100))) * (1 + (iva / 100))
    else:
        return float((costo / (1 - (margine / 100))) * (1 + (iva / 100)))


def calcolaMargine(costo=0, listino=0, iva=0):
    """
    Calcola il margine a partire dal costo, dal prezzo di vendita e dall'iva
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if type(costo)==type("stringa") or costo is None:
        costo = Decimal(sanitizer(costo) or 0)
    if type(listino)==type("stringa") or listino is None:
        listino = Decimal(sanitizer(listino) or 1)
    if type(iva)==type("stringa") or iva is None:
        iva = Decimal(sanitizer(iva) or 0)
    if costo.__class__ == Decimal and listino.__class__ == Decimal and iva.__class__ == Decimal:
        if listino == 0:
            return Decimal('0')
        return (100 - ((costo * 100) / ((listino * 100) / (iva + 100))))
    else:
        if listino == 0:
            return 0
        return float(100 - ((costo * 100) / ((listino * 100) / (iva + 100))))


def calcolaCostoUltimodaDettaglio(dettaglio=0, ricarico=0, iva=0):
    #prima scorporo
    imponibile = float(dettaglio)/(1+float(iva)/100)
    #poi calcolo il costo ultimo
    costo_ultimo = float(imponibile)/(1+float(ricarico)/100)
    return costo_ultimo

def calcolaCostoUltimodaIngrosso(ingrosso=0, ricarico=0):
    costo_ultimo = float(ingrosso)/(1+float(ricarico)/100)
    return costo_ultimo

def calcolaMargineDaRicarico(ricarico=0):
    """
    Calcola il margine dal ricarico
    sel l'argomento è un oggetto Decimal, lo è anche il valore di ritorno
    """
    if type(ricarico)==type("stringa") or ricarico is None:
        ricarico = Decimal(sanitizer(ricarico) or 0)
    if ricarico.__class__ == Decimal:
        return ricarico / (1 + (ricarico / 100))
    return float(ricarico / (1 + (ricarico / 100)))


def calcolaRicaricoDaMargine(margine=0):
    """
    Calcola il ricarico dal margine
    sel l'argomento è un oggetto Decimal, lo è anche il valore di ritorno
    """
    if type(margine)==type("stringa") or margine is None:
        margine = Decimal(sanitizer(margine) or 0)
    if margine.__class__ == Decimal:
        return margine / (1 - (margine / 100))
    else:
        return float(margine / (1 - (margine / 100)))


def calcolaPrezzoIva(prezzo=0, iva=0):
    """
    Calcola un prezzo ivato (iva > 0) o scorpora l'iva da un prezzo (iva < 0)
    sel gli argomenti sono tutti oggetti Decimal, lo è anche il valore di ritorno
    """
    if type(prezzo)==type("stringa") or prezzo is None:
        prezzo = Decimal(sanitizer(prezzo) or 0)
    if type(iva)==type("stringa") or iva is None:
        iva = Decimal(sanitizer(iva) or 0)
    if prezzo.__class__ == Decimal and iva.__class__ == Decimal:
        if iva and iva <0:
            return (100*prezzo)/(abs(iva)+100)
        else:
            return prezzo*(1+(iva/100))
    else:
        if iva  and iva < 0:
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
    Converte una data in stringa con formato GG/MM/AAAA
    """
    if data is None:
        return ''
    elif type(data) == str:
        return data
    else:
        try:
            s = string.zfill(str(data.day),2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4)
        except Exception:
            s = ''
        return s


def stringToDate(stringa):
    """
    Converte una stringa con formato GG/MM/AAAA in data
    """
    if not stringa:
        return None
    else:
        try:
            d = time.strptime(stringa, "%d/%m/%Y")
        except ValueError:
            return None
        else:
            return datetime.date(d[0], d[1], d[2])


def stringToDateBumped(stringa, giorni=1):
    """
    Ritorna la data aumentata di uno o più giorni

    Arguments:
    - `stringa`: una data
    - `giorni`: il numero di giorni da aggiungere
    """
    stringa = stringToDate(stringa)
    if stringa:
        return stringa + datetime.timedelta(days=giorni)
    else:
        return None

def dateTimeToString(data):
    """
    Converte una data + ora in stringa
    """
    if data is None:
        return ''
    elif type(data) == str:
        return data
    else:
        try:
            if string.zfill(str(data.month),2) and string.zfill(str(data.minute),2) != "00":
                s = string.zfill(str(data.day), 2) +\
                '/' + string.zfill(str(data.month),2) +\
                '/' + string.zfill(str(data.year),4) + \
                ' ' + string.zfill(str(data.hour),2) + \
                ':' + string.zfill(str(data.minute),2)
            else:
                s = string.zfill(str(data.day), 2) +\
                '/' + string.zfill(str(data.month),2) +\
                '/' + string.zfill(str(data.year),4)
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
        except:
            try:
                d = time.strptime(stringa, "%d/%m/%Y")
                data = datetime.datetime(d[0], d[1], d[2])
#            messageInfo(msg= "LA DATA E' IN QUALCHE MODO ERRATA O INCOMPLETA")
            except:
                data=None
        return data

def controllaDateFestivi(data):
    """Controlla se una data è festiva

    Arguments:
    - `stringa`: la data da controllare
    """
    festivi = ['1508', '3112']
    if type (data) != str:
        data = data.strftime('%d%m')
    else:
        data = data[:4]
    return data in festivi


def dataInizioFineMese(data):
    import calendar
    mese = data.month
    anno = data.year
    giorni = calendar.monthrange(anno, mese)
    return (datetime.date(anno, mese, 1), datetime.date(anno, mese, giorni[1]))

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
    """
    FIXME
    @param daoSconti:
    @type daoSconti:
    @param daoApplicazione:
    @type daoApplicazione:
    """
    applicazione = 'scalare'
    sconti = []

    if daoApplicazione == 'scalare' or daoApplicazione == 'non scalare':
        applicazione = daoApplicazione
    if daoSconti:
        for s in daoSconti:
            sconti.append({"valore": s.valore, "tipo": s.tipo_sconto})
    return (sconti, applicazione)

def getMisureFromRiga(daoMisura = []):
    """
    FIXME
    @param daoMisura:
    @type daoMisura:
    """
    misura = []

    for s in daoMisura:
        misura.append({"altezza": s.altezza, "larghezza": s.larghezza, "pezzi_moltiplicatore": s.moltiplicatore})

    return (misura)

def getDato(dictMisura, dato):
    """
    FIXME
    @param dictMisura:
    @type dictMisura:
    @param dato:
    @type dato:
    """
    returned = ''
    for s in dictMisura:
        returned = s[dato]
    return returned

def getStringaSconti(listSconti):
    """
    FIXME
    @param listSconti:
    @type listSconti:
    """
    stringaSconti = ''
    for s in listSconti:
        decimals = '1'
        tipo = s["tipo"]
        if tipo == 'percentuale':
            tipo = '%'
        elif tipo == 'valore':
            tipo = ''
            decimals = int(setconf(key="decimals", section="Numbers"))
        if tipo =="%" and (float(s["valore"]) - float(int(float(s["valore"])))) == 0:
            valore = str(int(float(s["valore"])))
        else:
            valore = ('%.' + str(decimals) + 'f') % float(s["valore"])
        stringaSconti = stringaSconti + valore + tipo + ';'
    return stringaSconti




def scontiTipo(stringa):
    if stringa =="valore":
        return " €"
    else:
        return " %"


def getDynamicStrListStore(length):
    """
    return a gtk.ListStore of the specified lenght
    """
    string1 = 'list = gtk.ListStore(str'
    string2 = ', str' * (length -1)
    string3 = ')'
    string4 = string1+string2+string3
    exec string4
    return list


def setFileName(filename, ext, returnName = False):
    """
    Verify that the filename have the extension "ext"
    If not, it will append the extension to the end of the filename.
    """
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
    """
    """
    def on_anagrafica_richiamata_destroy(anagWindow):
        """ """
        if anagWindow in Environment.windowGroup:
            Environment.windowGroup.remove(anagWindow)
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
    if anagWindow not in Environment.windowGroup:
        Environment.windowGroup.append(anagWindow)
    anagWindow.show_all()

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


def obligatoryField(window, widget=None, msg=None):
    """
    Gestisce un dialog di segnalazione campo obbligatorio
    """
    if msg is None:
        msg = 'Campo obbligatorio !'
    dialog = gtk.MessageDialog(window, GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                               GTK_DIALOG_MESSAGE_INFO, GTK_BUTTON_OK, msg)
    dialog.run()
    dialog.destroy()
    if widget is not None:
        if widget.get_property("can-focus"):
            widget.grab_focus()
    raise Exception, 'Operation aborted campo obbligatorio'


def showComplexQuestion(parentWindow, message):
    """
    MessageBox alla quale si puo' rispondere con Si/No/Tutti/Nessuno
    """
    dialog = gtk.Dialog('Attenzione',
                        parentWindow,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        None)
    hbox = gtk.HBox()
    image = GTK_IMAGE_NEW_FROM_STOCK(gtk.STOCK_DIALOG_QUESTION, GTK_ICON_SIZE_DIALOG)
    image.set_padding(10,10)
    label = gtk.Label(message)
    label.set_justify(GTK_JUSTIFICATION_LEFT)
    label.set_alignment(0,0)
    label.set_padding(15,10)
    hbox.pack_start(image, False, False, 0)
    hbox.pack_start(label, True, True, 0)
    dialog.get_content_area().pack_start(hbox, True, True, 0)

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
    dialog.add_action_widget(buttonYes, GTK_RESPONSE_YES)
    dialog.add_action_widget(buttonNo, GTK_RESPONSE_NO)
    dialog.add_action_widget(buttonAll, GTK_RESPONSE_APPLY)
    dialog.add_action_widget(buttonNone, GTK_RESPONSE_REJECT)

    dialog.show_all()
    result = dialog.run()
    dialog.destroy()
    return result


def destroy_event(window):
    """
    Send a 'destroy-event' to the specified gtk.Window
    """
    event = GDK_EVENT(GDK_EVENT_DESTROY)

    event.send_event = True
    event.window = window.window

    gtk.main_do_event(event)

def insertFileTypeChooser(filechooser,typeList):
    """
    FIXME
    @param filechooser:
    @type filechooser:
    @param typeList:
    @type typeList:
    """
    fc_vbox = gtk.VBox(True, spacing=5)
    hbox1 = gtk.HBox()
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
    filechooser.get_content_area().pack_end(fc_vbox, False, False, 10)
    return combobox


def modificaLottiScadenze(riga):
    ll = riga["descrizione"]
    if 'id' in riga:
        from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
        aa = RigaMovimentoFornitura().select(idRigaMovimentoVendita = riga["id"], batchSize=None)
        if aa:
            l = ""
            lotti= []
            for a in aa:
                lotto = a.forni.numero_lotto
                if lotto in lotti:
                    continue
                else:
                    lotti.append(lotto)
                l += _("\n Lotto %s Data sc %s ") %(lotto,dateToString(a.forni.data_scadenza))
            ll += l
        else:
            from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
            aa = NumeroLottoTemp().select(idRigaMovimentoVenditaTemp=riga["id"])
            if aa:
                ll+=_("\n Lotto %s") %(aa[0].lotto_temp)
    return ll


def listaComponentiArticoloKit(riga):
    """
    Ritorna la lista dei componenti articolo kit

    @param riga: riga dell'articolo
    @return: descrizione completa articolo kit
    """
    descr = riga['descrizione']
    from promogest.dao.Articolo import Articolo
    if setconf('Documenti', 'lista_componenti_articolokit'):
        if 'id_articolo' in riga:
            articolo = Articolo().getRecord(id=riga['id_articolo'])
            if articolo:
                for articolokit in articolo.articoli_kit:
                    _subarticolo = leggiArticolo(articolokit.id_articolo_filler)
                    if _subarticolo:
                        descr += "\n %s" % _subarticolo['denominazione']
    return descr

def multilinedirtywork(param):
    """
    Funzione che gestisce la suddivisione in multirighe
    """
    caratteri_singola_linea = int(setconf("Multilinea","multilinealimite"))

    operazione = ""
    if 'operazione' in param[0]:
        operazione = param[0]['operazione'].strip()

    costi_ddt_riga = True
    costi_ddt_totale = True
    if 'DDT' in operazione:
        costi_ddt_riga = setconf("Documenti","costi_ddt_riga")
        if costi_ddt_riga == '':
            costi_ddt_riga = True
        costi_ddt_totale = setconf("Documenti","costi_ddt_totale")
        if costi_ddt_totale == '':
            costi_ddt_totale = True

    strippa = True
    if operazione:
        if operazione == 'Fattura accompagnatoria' or 'DDT' in operazione:
            strippa = False

    for i in param:
        if not costi_ddt_totale:
            for k in ['_totaleOggetti', '_totaleImponibile',
                      '_totaleScontato', '_totaleImpostaScontata',
                      '_totaleNonScontato', '_totaleNonBaseImponibile',
                      '_totaleImposta', '_totaleImponibileScontato']:
                i[k] = ''
            i['_castellettoIva'] = []
        if 'righe' in i:
            skip = False
            for z in i["righe"]:
                z["descrizione"] = modificaLottiScadenze(z)
                z["descrizione"] = listaComponentiArticoloKit(z)
                if strippa:
                    if 'Rif. DDT vendita' in z["descrizione"]:
                        skip = False
                    if skip or 'RIEPILOGO ADR' in z["descrizione"]:
                        skip = True
                        z["descrizione"] = ''
                        continue
                if not costi_ddt_riga:
                    for k in ['valore_unitario_lordo', 'totaleRiga', 'valore_unitario_netto']:
                        z[k] = ''

            lista = []
            for riga in i['righe']:
                if riga['descrizione'] != '':
                    lista.append(riga)
            i['righe'] = lista

            for x in i['righe']:
                if len(x["descrizione"]) > caratteri_singola_linea \
                and "\n" not in x["descrizione"]:
                    wrapper = TextWrapper()
                    wrapper.width = caratteri_singola_linea
                    x["descrizione"] = "\n".join(wrapper.wrap(x["descrizione"]))

                if '\n' in x["descrizione"]:
                    desc= x["descrizione"].split("\n")
                    o = lista.index(x) # posizione della righa fra le righe
                    x["descrizione"] = desc[0]
                    lung = len(desc)-1
                    for d in desc[1:]:
                        p = desc.index(d)
                        c = x.copy()
                        for k,v in c.iteritems():
                            c[k] = ""
                        c["descrizione"] = str(d).strip()
                        lista.insert(o+p,c)
    return param


def on_status_activate(status, windowGroup, visible, blink, screens):
    """
    on press systray icon widget hide or show
    """
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



def checkCodFisc(codfis):
    """
    Funzione di verifica e controllo del codice fiscale
    """
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
        msg = _('Attenzione Codice Fiscale formalmente scorretto\nInserire comunque?!!!')
        messageInfo(msg=msg)
        return True

def checkPartIva(partitaIVA):
    """
    FIXME
    @param partitaIVA:
    @type partitaIVA:
    """

    n_Val = 0
    n_Som1 = 0
    n_Som2 = 0
    lcv = 0
    if len(partitaIVA) !=11:
        msg = _('Attenzione Partita Iva formalmente scorretto\nInserire comunque?!!!')
        messageInfo(msg=msg)
        return True
    l_ret = 0
    try:
        l_ret = int(partitaIVA)
    except:
        msg = _('Attenzione Partita Iva formalmente scorretto\nInserire comunque?!!!')
        messageInfo(msg=msg)
        return True
    if l_ret < 0:
        msg = _('Attenzione Partita Iva formalmente scorretto\nInserire comunque?!!!')
        messageInfo(msg=msg)
        return True
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
        msg = _('Attenzione Partita Iva formalmente scorretto\nInserire comunque?!!!')
        messageInfo(msg=msg)
        return True

def omogeneousCode(section=None, string = None):
    """
    """
    if section == "Clienti":
        if setconf("Clienti", "cliente_codice_upper"):
            return string.upper()
    elif section == "Fornitori":
        if setconf("Fornitori", "fornitore_codice_upper"):
            return string.upper()
    elif section == "Articoli":
        if setconf("Articoli", "articolo_codice_upper"):
            return string.upper()
    elif section == "Vettori":
        if setconf("Vettori", "vettore_codice_upper"):
            return string.upper()
    return string

def hasAction(actionID=None):
    """
    La modularizzazione richiede che
    quando il modulo non è presente o non è attivato
    la risposta sia sempre true perchè essendoci solo
    admin ha de facto tutti i privilegi
    """
    from promogest.modules.RuoliAzioni.dao.RoleAction import RoleAction
    idRole = Environment.params['usernameLoggedList'][2]
    if Environment.idACT == []:
        aa= RoleAction().select(id_role=idRole, batchSize=None)
        Environment.idACT = [x.id_action for x in aa]

    #roleActions = RoleAction().select(id_role=idRole,
                                            #id_action=actionID,
                                            #)
    if actionID in Environment.idACT: #roleActions:
        return True
    else:
        dialog = gtk.MessageDialog( None,
                                GTK_DIALOG_MODAL |
                                GTK_DIALOG_DESTROY_WITH_PARENT,
                                GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTON_OK,
                                _("Permesso negato! L'azione richiesta non è tra quelle che ti son consentite"))
        dialog.run()
        dialog.destroy()
        return False

def idArticoloFromFornitura(k,v):
    """
    """
    from promogest.dao.Fornitura import Fornitura
    codiciArtForFiltered =  Environment.params["session"]\
        .query(Fornitura)\
        .filter(and_(Fornitura.codice_articolo_fornitore.ilike("%"+v+"%")))\
        .all()
    return codiciArtForFiltered

def getCategorieContatto(id=None):
    """
    """
    from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto
    dbCategorieContatto = ContattoCategoriaContatto().select(id=id,
                                                            batchSize=None)
    return dbCategorieContatto

def getRecapitiContatto(id=None):
    """
    """
    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    if id:
        dbRecapitiContatto = RecapitoContatto().select(idContatto=id)
    else:
        dbRecapitiContatto = []
    return dbRecapitiContatto

def checkCodiceDuplicato(codice=None,id=None,tipo=None):
    """
    """
    if tipo =="Articolo":
        from promogest.dao.Articolo import Articolo
        if not id:
            a = Articolo().select(codicesatto=codice, idArticolo=id)
        else:
            a = False
    elif tipo =="Clienti":
        a = Cliente().select(codicesatto=codice)
    if a:
        msg = """Attenzione!
    Codice %s : %s  è già presente
    Inserirne un altro o premere il bottone "G"enera""" %(tipo,codice)
        dialog = gtk.MessageDialog(None,
                                GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                GTK_DIALOG_MESSAGE_INFO,
                                GTK_BUTTON_OK,
                                msg)
        dialog.run()
        dialog.destroy()
        return False
    else:
        return True


def sanitizer(value):
    if value:
        value = value.strip()
        value = value.replace("€", "")
        value = value.replace("%", "")
        value = value.replace(",", ".")
    return value


def dividi_in_rate(totale, nrate):
    """Divide un importo in rate
    """
    totale = Decimal(str(totale))
    somma = Decimal(0)
    rate = []
    for i in range(nrate):
        rate.append(mN(totale / nrate, 2))
        somma += mN(rate[i], 2)
    rate[nrate - 1] = rate[0] - mN(somma - totale, 2)
    return rate


def mN(value, decimal=None):
    """
    funzione importante perchè normalizza le valute, mettendo i decimali così
    come settato nel configure e restituisce un arrotondamento corretto
    RICORDA: Per un valore TOTALE quindi con due decimali si deve forzare il 2
    UPDATE: adesso supporta anche lo zero
    """
    if not value or value == '' or value == "None":
        return Decimal(0)
    value = deItalianizza(value)
    if decimal >= 0:
        precisione = decimal
    else:
        precisione = int(setconf(key="decimals", section="Numbers"))
    if precisione == 0:
        decimals = 0
    else:
        decimals = Decimal(10) ** - (precisione)
    newvalue= Decimal(str(value).strip()).quantize(Decimal(decimals), rounding=ROUND_HALF_UP)
    return newvalue


def mNLC(value,decimal=None, curr="€ "):
    """
    Per il momento ritorna mN, da implementare la localizzazione
    anche solo di valuta
    """
    value = mN(value, decimal=decimal)
    curr = setconf("Valuta", "valuta_curr")
    dp =","
    sep="."
    if curr =="$" or curr=="£":
        dp="."
        sep=","
    elif curr =="€":
        dp=","
        sep="."

    return italianizza(value, decimal=decimal,curr=curr+" ", dp=dp, sep=sep)


def mNL(value,decimal=None):
    """
    Per il momento ritorna mN, da implementare la localizzazione
    anche solo di valuta
    """
    value = mN(value, decimal=decimal)
    return italianizza(value, decimal=decimal)


def deItalianizza(value):
    if type("stringa") == type(value):
        if "€" in str(value):
            value = value.replace("€","")
        if "," in str(value) and "." in str(value):
            value = value.replace(".", "")
            value = value.replace(",", ".")
        elif "," in str(value):
            value = value.replace(",", ".")
    return value


def italianizza(value, decimal=0, curr='', sep='.', dp=',',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'
    ATTENZIONE: se si vuole che arrotondi si deve mettere
    un due ma si deve dare anche
    un valore con soli due decimali
    """
#    qq = Decimal(10) ** -places      # 2 places --> '0.01'
    precisione = int(decimal) or int(setconf(key="decimals", section="Numbers"))
    sign, digits, exp = Decimal(value).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(precisione):
        build(next() if digits else '0')
    if not precisione:
        build("0")
        build("0")
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def generateRandomBarCode(ean=13):
    """
    funzione di generazione codice ean13 random
    utile per quei prodotti che non hanno un codice
    chiaramente solo per uso interno
    """
    import random
    from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
    codice = ''

    def create(ean):
        """
        crea un codice di tipo ean
        @param ean: tipo di codice ( al momento gestisce  ean8 ed ean13)
        @type ean: int ( 8 o 13 )
        """
        code = [8, 0]
        if ean == 13:
            for a in xrange(10):
                code.append(random.sample(
                                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 1)[0])
            dispari = (code[1] \
                        + code[3] \
                        + code[5] \
                        + code[7] \
                        + code[9] \
                        + code[11]) * 3
            pari = code[0] + code[2] + code[4] + code[6] + code[8] + code[10]
        elif ean == 8:
            for a in xrange(5):
                code.append(random.sample(
                                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 1)[0])
            dispari = (code[0] + code[2] + code[4] + code[6]) * 3
            pari = code[1] + code[3] + code[5]
        tot = 10 - ((dispari + pari) % 10)
        if tot == 10:
            tot = 0
        code.append(tot)
        b = ''
        for d in code:
            b = b + str(d)
        return b
    correct = False
    while correct is False:
        codice = create(ean)
        there = CodiceABarreArticolo().select(codice=codice)
        if not there:
            return codice
        else:
            create(ean)


def removeCodBarorphan():
    """
    FIXME
    @param :
    @type :
    """
    from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
    bc = CodiceABarreArticolo().select(idArticoloNone=True, batchSize=None)
    if bc:
        for a in bc:
            print "CODICE A BARRE ORFANO DI ARTICOLO, VERRA' ELIMINATO", a.codice
            a.delete()


def calcolaTotali(daos, pbarr=None, onlypag=True):
    """
    Preleva i dati del totale del dao e ne fa un dizionario
    """

    plus = ["Fattura vendita", "DDT vendita", "Preventivo", "Vendita dettaglio",
    "Preventivo dettaglio","Ordine a magazzino","Vendita dettaglio CORSO", "Vendita dettaglio SANTIAGO",
"Ordine beni strumentali","Fattura pro-forma","Fattura differita vendita",
    "Fattura accompagnatoria","Scarico venduto da cassa","Ordine da cliente",
    "Ordine a fornitore","DDT acquisto",
    "Fattura acquisto","Fattura differita acquisto",]

    minus =["Nota di credito a cliente",
            "Nota di credito da fornitore",
            "DDT reso da cliente",
            "DDT reso a fornitore",]

#"Scarico per uso interno",
#"Scarico per deterioramento o rottura",
#"Scarico per omaggio",
#"Carico per inventario",

    totale_imponibile_non_scontato = 0
    totale_imponibile_scontato = 0
    totale_non_base_imponibile = 0
    totale_imposta_non_scontata = 0
    totale_imposta_scontata = 0
    totale_non_scontato = 0
    totale_scontato = 0
    totale_sospeso = 0
    totale_pagato = 0
    numero_documenti = 0

    _cast_imponibile = {}
    _cast_imposta = {}

    for tot in daos:
        if onlypag:
            if tot.operazione not in Environment.hapag:
                continue
        numero_documenti += 1
        if pbarr:
            pbar(pbarr,parziale=daos.index(tot), totale=len(daos),text=tot.intestatario[0:15], noeta=True)
        tot.totali
        for u in tot._castellettoIva:
            if str(u['aliquota']) not in _cast_imponibile:
                _cast_imponibile[str(u['aliquota'])] = Decimal(0)
                _cast_imposta[str(u['aliquota'])] = Decimal(0)
            if tot.operazione in minus:
                _cast_imposta[str(u['aliquota'])] -= u['imposta']
                _cast_imponibile[str(u['aliquota'])] -= u['imponibile']
            elif tot.operazione in plus:
                _cast_imposta[str(u['aliquota'])] += u['imposta']
                _cast_imponibile[str(u['aliquota'])] += u['imponibile']
        try:
            if tot.operazione in minus:
                totale_imponibile_non_scontato -= tot._totaleImponibile
            elif tot.operazione in plus:
                totale_imponibile_non_scontato += tot._totaleImponibile
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_imposta_non_scontata -= tot._totaleImposta
            elif tot.operazione in plus:
                totale_imposta_non_scontata += tot._totaleImposta
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_non_base_imponibile -= tot._totaleNonBaseImponibile
            elif tot.operazione in plus:
                totale_non_base_imponibile += tot._totaleNonBaseImponibile
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_non_scontato -= tot._totaleNonScontato
            elif tot.operazione in plus:
                totale_non_scontato += tot._totaleNonScontato
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_scontato -= tot._totaleScontato
            elif tot.operazione in plus:
                totale_scontato += tot._totaleScontato
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_imponibile_scontato -= tot._totaleImponibileScontato
            elif tot.operazione in plus:
                totale_imponibile_scontato += tot._totaleImponibileScontato
        except:
            pass
        try:
            if tot.operazione in minus:
                totale_imposta_scontata -= tot._totaleImpostaScontata
            elif tot.operazione in plus:
                totale_imposta_scontata += tot._totaleImpostaScontata
        except:
            pass
        try:
            if tot.operazione in minus:
                if tot.documento_saldato:
                    totale_sospeso -= 0
                else:
                    totale_sospeso -= tot.totale_sospeso
            elif tot.operazione in plus:
                if tot.documento_saldato:
                    totale_sospeso += 0
                else:
                    totale_sospeso += tot.totale_sospeso
        except:
            pass
        try:
            if tot.operazione in minus:
                if tot.documento_saldato:
                    totale_pagato -= tot._totaleScontato
                else:
                    totale_pagato -= tot.totale_pagato
            elif tot.operazione in plus:
                if tot.documento_saldato:
                    totale_pagato += tot._totaleScontato
                else:
                    totale_pagato += tot.totale_pagato
        except:
            pass
    if pbarr:
        pbar(pbarr,stop=True)
    totaliGenerali = {
        "totale_imponibile_non_scontato": totale_imponibile_non_scontato,
        "totale_imponibile_scontato": totale_imponibile_scontato,
        "totale_imposta_scontata": totale_imposta_scontata,
        "totale_non_base_imponibile": totale_non_base_imponibile,
        "totale_imposta_non_scontata": totale_imposta_non_scontata,
        "totale_non_scontato": totale_non_scontato,
        "totale_scontato": totale_scontato,
        "totale_pagato": totale_pagato,
        "totale_sospeso": totale_sospeso,
        "imponibile_aliquote": _cast_imponibile,
        "imposta_aliquote": _cast_imposta,
        "numero_documenti": numero_documenti
                        }
    return totaliGenerali


def fenceDialog():
    """
    FIXME
    """
    def on_button_clicked(button):
        """
        FIXME
        """
        from promogest.ui.SendEmail import SendEmail
        SendEmail()

    dialog = gtk.MessageDialog(None,
                                GTK_DIALOG_MODAL
                                | GTK_DIALOG_DESTROY_WITH_PARENT,
                                GTK_DIALOG_MESSAGE_INFO, GTK_BUTTON_OK)
    image = gtk.Image()
    image.set_from_file("./gui/messaggio_avviso.png")
    image.show()
    button = gtk.Button()
    button.add(image)
    button.show()
    button.connect('clicked', on_button_clicked)
    dialog.set_image(button)
    dialog.run()
    dialog.destroy()

def leggiRevisioni():
    """ controllo se il pg2 è da aggiornare o no"""
    def fetch():
        try:
            client = pysvn.Client()
            if not Environment.rev_locale:
                Environment.rev_locale = client.info(".").revision.number
            if not Environment.rev_remota:
                Environment.rev_remota = pysvn.Client().info2(
                    "http://svn.promotux.it/svn/promogest2/trunk/",
                            recurse=False)[0][1]["rev"].number
        except pysvn.ClientError:
            pass
        Environment.pg2log.info("VERSIONE IN USO LOCALE E REMOTA "+str(Environment.rev_locale)+" "+str(Environment.rev_remota))
    if pysvn:
        thread = threading.Thread(target=fetch)
        thread.start()

def messageInfo(msg="Messaggio generico", transient=None):
    """generic msg dialog """
    dialoggg = gtk.MessageDialog(transient,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        GTK_DIALOG_MESSAGE_INFO,
                        GTK_BUTTON_OK)
    dialoggg.set_markup(msg)
    response = dialoggg.run()
    dialoggg.destroy()
    return response

def messageError(msg="Messaggio generico", transient=None):
    """generic msg dialog """
    dialoggg = gtk.MessageDialog(transient,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        gtk.MESSAGE_ERROR,
                        gtk.BUTTONS_CANCEL)
    dialoggg.set_markup(msg)
    response = dialoggg.run()
    dialoggg.destroy()
    return response

def messageWarning(msg="Messaggio generico", transient=None):
    """generic msg dialog """
    dialoggg = gtk.MessageDialog(transient,
                        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                        GTK_DIALOG_MESSAGE_WARNING,
                        GTK_BUTTON_OK)
    dialoggg.set_markup(msg)
    response = dialoggg.run()
    dialoggg.destroy()
    return response


def YesNoDialog(msg="MESSAGGIO", transient=None,show_entry=False ):
    dialog = gtk.MessageDialog(transient,
                           GTK_DIALOG_MODAL
                           | GTK_DIALOG_DESTROY_WITH_PARENT,
                           GTK_DIALOG_MESSAGE_QUESTION, GTK_BUTTON_YES_NO,
                           msg)
    __entry_codi = gtk.Entry()
    dialog.get_content_area().pack_start(__entry_codi, False, False, 0)
    if show_entry:
        __entry_codi.show()
    response = dialog.run()
    entry_text = __entry_codi.get_text()
    dialog.destroy()
    if response == -8:
        if show_entry:
            return (True, entry_text)
        return True
    else:
        return False
    return response

def textview_insert_at_cursor(textview, string):
    _buffer = textview.get_buffer()
    return _buffer.insert_at_cursor(string)

def textview_get_modified(textview):
    _buffer = textview.get_buffer()
    return _buffer.get_modified()

def textview_get_char_count(textview):
    _buffer = textview.get_buffer()
    return _buffer.get_char_count()

def textview_get_line_count(textview):
    _buffer = textview.get_buffer()
    return _buffer.get_line_count()

def textview_get_text(textview):
    _buffer = textview.get_buffer()
    return _buffer.get_text(_buffer.get_start_iter(), _buffer.get_end_iter(), True) or ""

def textview_set_text(textview, text):
    _buffer = textview.get_buffer()
    _buffer.set_text(text or "")
    textview.set_buffer(_buffer)

def notebook_tabs_show(notebook, pages):
    for page in pages:
        _page = notebook.get_nth_page(page)
        _page.set_property('visible', True)

def notebook_tabs_hide(notebook, pages):
    for page in pages:
        _page = notebook.get_nth_page(page)
        _page.set_property('visible', False)

def notebook_tab_hide(notebook, page):
    _page = notebook.get_nth_page(page)
    _page.set_property('visible', False)

def notebook_tab_show(notebook, page):
    _page = notebook.get_nth_page(page)
    _page.set_property('visible', True)

def deaccenta(riga=None):
    """ questa funzione elimina gli accenti magari non graditi in alcuni casi"""
    nkfd_form = unicodedata.normalize('NFKD', unicode(riga))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def setconf(section, key, value=False):
    """ Importante funzione che "semplifica" la lettura dei dati dalla tabella
    di configurazione setconf
    Tentativo abbastanza rudimentale per gestire le liste attraverso i ; ma
    forse si potrebbero gestire più semplicemente con le virgole
    """
    if Environment.tipo_eng =="postgresql" or Environment.tipo_eng =="postgres" :
        if not hasattr(Environment.conf, "Documenti"):
            Environment.conf.add_section("Documenti")
            Environment.conf.save()
        if  hasattr(Environment.conf, "Documenti") and not hasattr(Environment.conf.Documenti, "cartella_predefinita"):
            setattr(Environment.conf.Documenti,"cartella_predefinita",Environment.documentsDir)
            Environment.conf.save()
        if key == "cartella_predefinita":
            return Environment.conf.Documenti.cartella_predefinita
    from promogest.dao.Setconf import SetConf
    #confList = Environment.confList
    if not Environment.confDict:
        confList = SetConf().select(batchSize=None)
        for d in confList:
            Environment.confDict[(d.key,d.section)] = d
        #Environment.confList = confList

    #confff = None
    #for d in confList:
        #if not value:
            #if d.key==key and d.section==section:
                #confff = d
                #break
        #else:
            #if d.key==key and d.section==section and d.value == value:
                #confff = d
                #break
    if (key,section) not in Environment.confDict:
        if not value:
            confff = SetConf().select(key=key, section=section)
        elif value:
            confff = SetConf().select(key=key, section=section, value=value)
        if confff:
            confff = confff[0]
    else:
        confff = Environment.confDict[(key, section)]
    c = []
    if confff:
        valore = confff.value
        if ";" in str(valore):
            val = str(valore).split(";")
            for a in val:
                c.append(a.strip())
            return c
        else:
            if valore == "":
                return None
            elif valore and len(valore.split("/"))>=2:
                return str(valore)
            else:
                try:
                    return eval(valore)
                except:
                    return str(valore)

    else:
        return ""

def number_format():
    stringa = str('%-14.'+ str(setconf("Numbers", "decimals")) +'f')
    return stringa

def orda(name):
     a = "".join([str(ord(x)) for x in list(name)])
     return a

def checkInstallation():
    """ TODO: Aggiungere una funzione che tenga conto delle volte in cui
    fallisce il check """
    from promogest.dao.Setconf import SetConf
    try:
#        url = "http://localhost:8080/check"
        url = "http://www.promogest.me/check"
        data = {"masterkey" : SetConf().select(key="install_code",
                                            section="Master")[0].value,
                "icode":SetConf().select(key="icode",
                                            section="Master")[0].value}
        values = urllib.urlencode(data)
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
        t = Timer(5.0, response.close)
        t.start()
        content = response.read()
        conte = json.loads(content)
        if conte == {}:
            print "CODICE NON PRESENTE DARE UN MESSAGGIO"
        #elif conte and conte["codice"] == None and conte["tipo"] == None:
            #print "CODICE VUOTO RESETTO I DATI"
            #confy = SetConf().select(key="install_code",section="Master")
            #if confy:
                #con = confy[0]
            #else:
                #con = SetConf()
            #con.key = "install_code"
            #con.value =str(hashlib.sha224("aziendapromo"+orda("aziendapromo")).hexdigest())
            #con.section = "Master"
            #con.description = "codice identificativo della propria installazione"
            #con.tipo_section = "General"
            #con.tipo = "ONE BASIC"
            #con.active = True
            #con.date = datetime.datetime.now()
            #con.persist()
        else:
            print " CODICE TROVATO",conte
            confy = SetConf().select(key="tipo",section="Master")
            if confy:
                if confy[0].value != conte["tipo"]:
                    confy[0].value = conte["tipo"]
                    confy[0].tipo = conte["tipo"]
                    confy[0].persist()
            else:
                k = SetConf()
                k.key = "tipo"
                k.value =conte["tipo"]
                k.section = "Master"
                k.description = "tipo"
                k.tipo_section = "General"
                k.tipo = conte["tipo"]
                k.active = True
                k.date = datetime.datetime.now()
                k.persist()
            Environment.modulesList.append(str(conte["tipo"]))
            Environment.tipo_pg= str(conte["tipo"])
    except:
        print "ERRORE NEL COLLEGAMENTO AL CHECK INSTALLAZIONE"
        data = SetConf().select(key="tipo",section="Master")
        if data:
            Environment.modulesList.append(str(data[0].tipo))
            Environment.tipo_pg= str(data[0].tipo)
            a = SetConf().select(key="errcheck",section="Master")
            if a :
                a[0].value = str(int(a[0].value)+1)
                a[0].persist()
            else:
                k = SetConf()
                k.key = "errcheck"
                k.value ="1"
                k.section = "Master"
                k.description = "errcheck"
                k.tipo_section = "General"
                k.tipo = ""
                k.active = True
                k.date = datetime.datetime.now()
                k.persist()




def last_day_of_month(y, m):
    """Return day (1..31) which is last day of month m in year y
    """
    _dim = (None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def _leap(y):
        if y % 4: return 0
        if y % 100: return 1
        if y % 400: return 0
        return 1

    if m == 2:
        return 28 + _leap(y)
    if not (1 <= m <= 12):
        raise Exception("month not in 1..12")
    return _dim[m]

def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]

def dateToOrdinal(anno):
    dd = []
    ccccc = Calendar().yeardatescalendar(int(Environment.workingYear))
    for cccc in ccccc:
        for ccc in cccc:
            for cc in ccc:
                for c in cc:
                    if c.year==int(Environment.workingYear) and c.toordinal() not in dd:
                        dd.append((c.toordinal(),c))
    return dd


def format_sec(sec):
    sec = int(sec)
    min_, sec = divmod(sec, 60)
    hour, min_ = divmod(min_, 60)
    return '%d:%02d:%02d' % (hour, min_, sec)

def pbar(pbar, parziale=1, totale=1, pulse=False, stop=False, text="", noeta= False):
    if stop:
        pbar.grab_add()
        pbar.set_fraction(0)
        pbar.set_text("Finito")
        while gtk.events_pending():
            gtk.main_iteration_do(False)
        pbar.grab_remove()
        return
    if not pulse:
        x = (parziale*100)/totale
        if not Environment.puntoA:
            Environment.puntoA = time.time()
            delta = 0
        else:
            puntoA = Environment.puntoA
            puntoB = time.time()
            Environment.puntoA = puntoB
            Environment.puntoB = time.time()
            delta = puntoB-puntoA
        if not Environment.puntoP:
            Environment.puntoP = x
            eta = Environment.eta
        else:
            if x != Environment.puntoP:
                Environment.puntoP = x
                if delta:
                    eta = format_sec((totale*delta)-(parziale*delta))
                    Environment.eta = eta
                else:
                    eta= 0
            else:
                eta = Environment.eta
        pbar.grab_add()
        if text:
            if noeta:
                pbar.set_text(text+" "+str(x)+"%")
            else:
                pbar.set_text(text+" "+str(x)+"% ETA: "+str(eta))
        else:
            if noeta:
                pbar.set_text(str(x)+"%")
            else:
                pbar.set_text(str(x)+"% ETA: "+str(eta))
        if parziale == 0: parziale=1
        if totale ==0 :totale =1
        if totale - 1.0 >0:
            pbar.set_fraction(parziale/(totale - 1.0))  # genera un warning, perc >= 0 and perc <= 1.0, infatti vale 1.33 all'ultimo passaggio...
        while gtk.events_pending():
             gtk.main_iteration_do(False)
        pbar.grab_remove()
    else:
        pbar.grab_add()
        if text:
            pbar.set_text(text)
        pbar.pulse()
        while gtk.events_pending():
             gtk.main_iteration_do(False)
        pbar.grab_remove()


def b(stringa):
    if stringa:
        stringa = "<b>"+stringa+"</b>"
    else:
        stringa = ""
    return stringa


def c(stringa, color):
    if stringa:
        stringa = "<span foreground='%s' >" %(color) +stringa+"</span>"
    else:
        stringa = ""
    return stringa

def scribusVersion(slafile):
    Environment.pg2log.info( "QUESTO E' IL FILE SLA"+ slafile)
    try:
        doc = ET.parse(slafile)
    except:
        Environment.new_print_enjine=False
        return False
    root = doc.getroot()
    doc.findall('DOCUMENT')[0]
    slaversion = root.get('Version')
    Environment.pg2log.info( "FILE SLA DA VERIFICARE PRIMA DLLA STAMPA "+ slafile)
    Environment.pg2log.info("VERSIONE SLA  "+ str(slaversion))
    if slaversion in ("1.3.6", "1.3.7", "1.3.8", "1.3.9","1.4.0","1.4.0.rc2","1.4.0.rc3","1.4.0.rc4"):
        Environment.new_print_enjine=True
        return True
    elif slaversion in ("1.3.5.1", "1.3.5svn"):
#        messageInfo(msg="ATTENZIONE FORMATO TEMPLATE SLA DA CORREGGERE 1.3.5")
        print "ATTENZIONE FORMATO TEMPLATE SLA DA CORREGGERE 1.3.5"
        Environment.pg2log.info("ATTENZIONE FORMATO TEMPLATE SLA DA CORREGGERE 1.3.5")
        return True
    elif "1.3.4" in slaversion:
        Environment.new_print_enjine=False
        return False
    elif slaversion in ("1.3.3","1.3.3.6cvs"):
        Environment.new_print_enjine = False
        return False
    else:
        Environment.new_print_enjine=True
        return True

def posso(mod=None):
    modulis = Environment.modulesList
    if mod == "RA":
        if "RuoliAzioni"in modulis: return True
        if "FULL" in modulis :return True
        if "STANDARD" in modulis: return True
        return False
    if mod == "PW" or mod=="PromoWear":
        if "PromoWear" in modulis:return True
        if "+W" in modulis:return True
        return False
    if mod == "AG":
        if "Agenti" in modulis: return True
        if "FULL" in modulis :return True
        if "STANDARD" in modulis: return True
        return False
    if mod == "GN":
        if "GestioneNoleggio" in modulis: return True
        return False
    if mod == "VD" or mod=="VenditaDettaglio":
        if "VenditaDettaglio" in modulis:return True
        if "+S" in modulis:return True
        return False
    if mod == "DB":
        if "DistintaBase" in modulis: return True
        return False
    if mod == "ADR":
        if "ADR" in modulis: return True
        return False
    if mod == "CN" or mod=="Contatti":
        if "Contatti" in modulis:return True
        if "BASIC" in modulis : return True
        if "STANDARD" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "PR" or mod=="Promemoria":
        if "Promemoria" in modulis:return True
        if "BASIC" in modulis : return True
        if "STANDARD" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "IN":
        if "Inventario"  in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "IPL":
        if "ImportPriceList" in modulis:return True
        if "FULL" in modulis: return True
        return False
    if mod == "LA":
        if "Label" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "GRB":
        if "FULL" in modulis: return True
        return False
    if mod == "SM":
        if "SuMisura" in modulis: return True
        return False
    if mod == "IP":
        if "InfoPeso" in modulis: return True
        return False
    if mod == "PA" or mod=="Pagamenti":
        if "Pagamenti" in modulis: return True
        if "BASIC" in modulis: return True
        if "STANDARD" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "PN" or mod=="PrimaNota":
        if "PrimaNota" in modulis: return True
        if "BASIC" in modulis: return True
        if "STANDARD" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "STA":
        if "STA" in modulis: return True
        if "FULL" in modulis: return True
        return False
    if mod == "STA_DETT":
        if "STA_DETT" in modulis: return True
        if "FULL" in modulis: return True
    if mod == "SD":
        if "SincroDB" in modulis :return True
        return False
    if mod == "SL":
        if "SchedaLavorazione" in modulis :
            return True
        return False
    if mod == "GC" or mod =="GestioneCommesse":
        if "GestioneCommesse" in modulis :return True
        if "BASIC" in modulis: return True
        if "STANDARD" in modulis: return True
        if "FULL" in modulis: return True
        return False
    d = setconf(mod,"mod_enable", value="yes")
    if d:
        return True
    return False

def installId():
    from promogest.dao.Setconf import SetConf
    from random import randint as rint
    a = setconf(section="Master", key ="icode")
    if not a:
        string = ""
        values = "23456789QWERTYUPASDFGHJKLZXCVBNMabcdefghmnpqrstuvz"
        for a in range(15):
            b =  rint(0,35)
            string += values[b]
        kdd = SetConf()
        kdd.key = "icode"
        kdd.value = string
        kdd.section = "Master"
        kdd.tipo_section = "Master"
        kdd.description = ""
        kdd.active = True
        kdd.date = datetime.datetime.now()
        kdd.persist()

def getListiniArticolo(idArticolo=None):
    from promogest.dao.ListinoArticolo import ListinoArticolo
    listi = ListinoArticolo().select(idArticolo = idArticolo,
                            listinoAttuale=True, batchSize=None)
    return listi

def fencemsg():
    msg = """OPERAZIONE NON CONSENTITA CON IL PACCHETTO
CHE STAI USANDO, PASSA ALLA "ONE STANDARD"
O ALLA "ONE FULL" OPPURE ACQUISTA IL MODULO
DI CUI HAI BISOGNO
   GRAZIE"""
    return messageInfo(msg=msg)

def daoTestDocu(dao):
    if dao.id_fornitore and dao.id_testata_documento:
        from promogest.dao.TestataDocumento import TestataDocumento
        return TestataDocumento().getRecord(id=dao.id_testata_documento)
    else:
        return None

def getLottoeScadenze(daoRigaMovimento, testataMovimento):
    from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
    from promogest.dao.Fornitura import Fornitura

    idFornitura = RigaMovimentoFornitura().select(
                        idRigaMovimentoAcquisto = daoRigaMovimento.id,
                        idArticolo = daoRigaMovimento.id_articolo,
                        batchSize=None)
    if idFornitura:
        idFornitura = idFornitura[0]
        return Fornitura().getRecord(id=idFornitura)
    else:
        return None

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed


def start_viewer(filename):
    '''
    Apre un documento con il visualizzatore predefinito in modo
    cross-platform.
    '''
    import subprocess
    from sys import platform
    if platform == 'darwin':
        os.system('open "%s"' % filename)
    elif platform == 'win32':
        os.startfile(filename)
    elif platform.startswith('linux'):
        subprocess.Popen(['xdg-open', filename])
    else:
        pass
