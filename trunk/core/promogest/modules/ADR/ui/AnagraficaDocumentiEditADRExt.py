# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest import Environment
from promogest.lib.utils import *

from promogest.modules.ADR.dao.ArticoloADR import ArticoloADR

T_SUM_ADR=_("### RIEPILOGO ADR ###")

T_PG = _("P.G")

T_CODICE_UN = _("Cod.UN")

T_QTA = _("Q.tà")

T_QTA_VIRT = _("Q.tà Virt. ADR")

T_GRUPPO_SUM_ADR=_("Tot. Gruppo")

T_DOC_SUM_ADR=_("Tot. Documento")

def setLabels(anaedit):
    """Inizializza i campi per l'anagrafica documenti relativi al modulo ADR.

    Arguments:
    - `anaedit`: l'anagrafica articolo edit
    """
    anaedit.summary_adr_label.set_text('')

def azzeraRiga(anaedit, numero):
    pass

def getADRArticolo(id):
    """Restituisce le informazioni ADR per un articolo

    Arguments:
    - `id`: l'id dell'articolo
    """
    _articoloADR = ArticoloADR().select(id_articolo=id)
    if _articoloADR:
        _articoloADR = _articoloADR[0]
    return _articoloADR


MSG_ADR = "\nTrasporto non superante i limiti liberi\nprescritti al 1.1.3.6"

def calcolaLimiteTrasportoADR(anagrafica, artADR, **kwargs):
    """Calcola se viene superato il limite massimo di esenzione
    virtuale di 1000 kg

    Arguments:
    - `anagrafica` : anagrafica articoli edit
    - `artADR` : l'articolo ADR
    """
    # Sanitizza i valori in kwargs
    azione = 'add'
    if 'azione' in kwargs:
        azione = kwargs['azione']

    qta = 0.0
    if 'qta' in kwargs:
        qta = kwargs['qta']

    if artADR.numero_un == '' or isinstance(artADR.coefficiente_moltiplicazione_virtuale, str):
        return

    # il gruppo imballaggio non esiste, inseriamo direttamente il numero un & co
    if not artADR.gruppo_imballaggio in anagrafica.dati_adr:
        anagrafica.dati_adr[artADR.gruppo_imballaggio] = [
            { artADR.numero_un: [
                anagrafica._righe[0]["quantita"],
                anagrafica._righe[0]["quantita"] * artADR.coefficiente_moltiplicazione_virtuale
                ]
            }
        ]
    else:
        # esiste già un gruppo imballaggio, cerchiamo il numero un & co per aggiornare i dati
        t = False
        i = 0
        for o in anagrafica.dati_adr[artADR.gruppo_imballaggio]:
            if artADR.numero_un in o:
                if azione == 'rm':
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][0] -= anagrafica._righe[0]["quantita"]
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][1] -= anagrafica._righe[0]["quantita"] * artADR.coefficiente_moltiplicazione_virtuale
                elif azione == 'agg':
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][0] -= qta
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][1] -= qta * artADR.coefficiente_moltiplicazione_virtuale
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][0] += anagrafica._righe[0]["quantita"]
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][1] += anagrafica._righe[0]["quantita"] * artADR.coefficiente_moltiplicazione_virtuale
                else:
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][0] += anagrafica._righe[0]["quantita"]
                    anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][1] += anagrafica._righe[0]["quantita"] * artADR.coefficiente_moltiplicazione_virtuale
                if anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un][0] == 0:
                    del(anagrafica.dati_adr[artADR.gruppo_imballaggio][i][artADR.numero_un])  # rimuovi il codice UN
                t = True
                break
            i += 1
        # esito ricerca negativo, aggiungiamo il numero un & co
        if not t:
            anagrafica.dati_adr[artADR.gruppo_imballaggio].append({artADR.numero_un: [anagrafica._righe[0]["quantita"], anagrafica._righe[0]["quantita"] * artADR.coefficiente_moltiplicazione_virtuale]})

    # Calcolo dei totali, superamento dei limiti
    sup = False
    tt1=0
    tt2=0
    _buf = T_SUM_ADR.center(70)
    _buf += "\n %-5s %-15s %-20s %-20s" % (T_PG, T_CODICE_UN, T_QTA, T_QTA_VIRT)
    for k,o in anagrafica.dati_adr.iteritems():
        t1=0
        t2=0
        for j in o:
            for kk,z in j.iteritems():
                _buf += "\n %-8s %-17s %-18s %-20s" % (str(k), str(kk), str(z[0]), str(z[1]))
                t1+=z[0]
                t2+=z[1]
        _buf += "\n\n %-22s %-18s %-10s" % (T_GRUPPO_SUM_ADR, str(t1), str(t2))
        if t2 > 1000:
            sup = True
        tt1+=t1
        tt2+=t2
    _buf += "\n %-20s %-18s %-10s" % (T_DOC_SUM_ADR, str(tt1), str(tt2))

    if not sup:
        _buf += MSG_ADR

    anagrafica.summary_adr_label.set_text(_buf)

def sposta_sommario_in_tabella(anagrafica):
    """Sposta le righe descrittive del documento ADR nella tabella

    Arguments:
    - `anagrafica`: l'anagrafica documento
    """
    _buffer = anagrafica.summary_adr_label.get_text()
    for linea in _buffer.splitlines():
        anagrafica.azzeraRiga()
        anagrafica._righe[0]['descrizione'] = linea
        anagrafica._righe[0]['quantita'] = 0
        anagrafica._righe.append(anagrafica._righe[0])

def docCompatibileADR(denominazione):
    """Ritorna vero se il tipo di documento Ãš appropriato per il modulo ADR

    Arguments:
    - `denominazione`: la denominazione del tipo di documento
    """
    tipi_consentiti = ['Fattura accompagnatoria',
                       'DDT vendita',
                       'DDT acquisto',
                       'DDT reso a fornitore',
                       'DDT reso da cliente']
    if denominazione in tipi_consentiti:
        return True
    else:
        return False
