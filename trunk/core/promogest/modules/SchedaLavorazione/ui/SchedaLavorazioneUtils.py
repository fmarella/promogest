# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
#


import gobject, os
import pygtk
import gtk
import string, re, time, datetime, decimal
from decimal import *
from promogest import Environment
from  promogest.ui.utils import *
from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.modules.SchedaLavorazione.dao.CarattereStampa import CarattereStampa
from promogest.modules.DistintaBase.dao.AssociazioneArticolo import AssociazioneArticolo
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.modules.SchedaLavorazione.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.PromemoriaSchedaOrdinazione import PromemoriaSchedaOrdinazione
import promogest.modules.SchedaLavorazione.lib.PopReader
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.Articolo import Articolo

def fillComboboxColoreStampa(combobox, filter=False):
    """
    Crea l'elenco dei listini
    """
    model = gtk.ListStore(object, int, str)
    liss = ColoreStampa().select(denominazione=None,
                                        orderBy = None,
                                        offset = None,
                                        batchSize = None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for l in liss:
        model.append((l, l.id, (l.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCarattereStampa(combobox, filter=False):
    """
    Crea l'elenco dei listini
    """
    model = gtk.ListStore(object, int, str)
    liss = CarattereStampa().select(    denominazione=None,
                                        orderBy = None,
                                        offset = None,
                                        batchSize = None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for l in liss:
        model.append((l, l.id, (l.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxAssociazioneArticoli(combobox, search_string=None):
    """
    Riempie la combobox di selezione delle associazioni di articoli.
    Se la lista risultante ha un solo elemento, questo viene automaticamente selezionato.
    """
    model = gtk.ListStore(object,str,str)
    model.clear()
    liss = Articolo().select(node =True,
                            codice=search_string,
                            offset=None,
                            batchSize=None)

    # questa combobox mi sa che non puo' andare a finire in un filter widget
    emptyRow = ''
    model.append((None, None, emptyRow))
    for l in liss:
        model.append([l,l.codice, l.denominazione])
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 1)
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if len(liss) == 1 and search_string is not None:
        combobox.set_active(1)
    return True

def fetch_date(string):
    """
    This should return a string indicating a date in italian format (dd/mm/YYYY)
    or None if some of the parts of the input string cant be translated into number format
    """
    def fetch_day(str):
        if len(str) <= 2:
            try:
                number = int(str)
                if number <= 31 and number > 0:
                    return str(number)
            except:
                #questa espressione regolare continua a matchare con la stringa "0" e "00"
                # necessario risolvere (potrebbe creare problemi)
                re_str = re.compile('(^[0-2]?[0-9]$|^30$|^31$){1}')
                if re_str.match(str) and str != ('0'or '00'):
                    return str
        else:
            return None

    def fetch_month(str):
        monthList = ['gennaio','febraio','marzo','aprile','maggio',\
                                'giugno','luglio','agosto','settembre','ottobre',\
                                'novembre','dicembre']
        if len(str) <= 2:
            try:
                number = int(str)
                if number <= 12 and number > 0:
                    return str(number)
            except:
                #se fallisce quello sopra... questo ha poche speranze.
                re_str = re.compile('(^[0-1]?[0-9]$|^10$|^11$|^12$){1}')
                if re_str.match(str) and str != ('0'or '00'):
                    return str
                return None
        else:
            ind = 1
            for month in monthList:
                if str.lower() == month:
                    return ind
                    break
                ind += 1
            return None

    def fetch_year(str):
        if len(str) == 2:
            return '20'+str
        elif len(str) == 4:
            return str
        else:
            return None

    data = string.split(' ')
    if len (data) == 3:
        day = fetch_day(data[0])
        month = fetch_month(data[1])
        year = fetch_year(data[2])
    elif len(data) == 4:
        day = fetch_day(data[0]) or fetch_day(data[1])
        month = fetch_month(data[2])
        year = fetch_year(data[3])
        if (day is not None) and (month is not None) and (year is not None):
            return stringTodate (day+'/'+month+'/'+year)
        else:
            return None

def get_nomi_sposi(str1,str2, reverse = False):
    if not reverse:
        return str1.split(' ')[0]+' e '+str2.split(' ')[0]
    else:
        return str1.split(' ')[-1]+' - '+str2.split(' ')[-1]

def create_schede_ordinazioni(data):
    schede_saltate = []
    codice_contrassegno = 5
    codice_stampa = 6
    for form in data:
        data_matrimonio = fetch_date(form['Data_matrimonio'])
        citta_matrimonio = form["Citta_matrimonio"]
        carattere = form["carattere"]
        colore = form["colore"]
        referente = form["nome"]
        presso = form["Presso"]
        via_piazza = form["Via_e_num"]
        citta = form["Citta"]
        provincia = form["Provincia"]
        zip = form["CAP"]
        telefono = form["telefono"]
        cellulare = form["Cellulare"]
        prima_email = form["From"]
        pagamento = form["pagamento"]
        sconto = form["Percentuale di sconto"].replace("%","")
        articoli_scheda = form['articoli']
        lui_e_lei = get_nomi_sposi(form["Nome_sposo"],form["Nome_sposa"])
        nomi_sposi = get_nomi_sposi(form["Nome_sposo"],form["Nome_sposa"], reverse=True)
        dao = SchedaOrdinazione()
        if data_matrimonio is not None:
            dao.data_matrimonio = utils.stringToDate(data_matrimonio)
        else:
            schede_saltate.append(form)
            continue
        dao.data_presa_in_carico = datetime.date.today()
        dao.nomi_sposi = nomi_sposi
        dao.lui_e_lei = lui_e_lei
        dao.id_carattere_stampa = CarattereStampa().select(denominazione= carattere,
                                                            orderBy = None,
                                                            offset = None,
                                                            batchSize = None)[0].id

        dao.id_colore_stampa = ColoreStampa().select(denominazione= colore,
                                                        orderBy = None,
                                                        offset = None,
                                                        batchSize = None)[0].id

        dao.provenienza = citta_matrimonio
        dao.referente = referente
        dao.presso = presso
        dao.via_piazza = via_piazza
        dao.zip = zip
        dao.localita =  citta
        dao.provincia = provincia
        dao.stato = 'Italia'
        dao.prima_email = prima_email
        dao.telefono = telefono
        dao.cellulare = cellulare
        art = articoli_scheda.iteritems()[0]
        associazione = AssociazioneArticoli().select(nodo=True,
                                                    codice=art[0],
                                                    offset=None,
                                                    batchSize=None)
        quantita = []
        _produttore = associazione[0].produttore
        if _produttore.lower() in Environment.conf.SchedaLavorazione.aziende_cliche.lower().strip().split(', '):
            dao.bomba_in_cliche = True
        else:
            dao.bomba_in_cliche = False
        for ass in associazione:
            for art in articoli_scheda.iteritems():
                if ass.codice == int(art[0]):
                    quantita.append(art[1])
                    continue
            if ass.denominazione.lower() == 'stampa':
                quantita.append(1)
                continue
            elif ass.denominazione.lower() == 'contrassegno':
                if pagamento.lower() == 'contrassegno':
                    quantita.append(1)
                    continue
                else:
                    delete_contrassegno = True
                    continue
            listini = []
            listinoarticolo = ListinoArticolo(Environment.connection, 1, ass.id_articolo)
            listini.append(listinoarticolo)
        if delete_contrassegno:
            for ass in associazione:
                if ass.denominazione.lower() == 'contrassegno':
                    associazione.remove(ass)
                    del delete_contrassegno
        righe = []
        id_magazzino = 1
        id_listino = 1
        dao.righe = []
        _parzialeNetto = Decimal('0')
        for i in range(len(associazione)):
            daoRiga = RigaSchedaOrdinazione()
            daoRiga.id_scheda = dao.id or None
            daoRiga.id_articolo = associazione[i].id_articolo
            daoRiga.id_magazzino = id_magazzino
            daoRiga.descrizione = associazione[i].denominazione
            daoRiga.codiceArticoloFornitore = None
            daoRiga.id_listino = id_listino
            daoRiga.percentuale_iva = lettura_articolo['percentualeAliquotaIva']
            setScontiRiga(daoRiga)
            daoRiga.quantita = quantita[i]
            daoRiga.id_multiplo = None
            daoRiga.moltiplicatore = None
            daoRiga.valore_unitario_lordo = listinoarticolo[i].prezzo_dettaglio
            daoRiga, _parzialeNetto = getPrezzoNetto(daoRiga,_parzialeNetto)
            dao.righe.append(daoRiga)
        dao.totale_lordo = _parzialeNetto.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


def getPrezzoNetto(dao, parzialeNetto=None):
    """ calcola il prezzo netto dal prezzo lordo e dagli sconti  in una riga """

    prezzoLordo = Decimal(str(dao.valore_unitario_lordo))
    prezzoNetto = prezzoLordo
    applicazione = dao.applicazione_sconti
    sconti = dao.scontiRiga
    if sconti:
        for s in sconti:
            if s.tipo_sconto == 'percentuale':
                if applicazione == 'scalare':
                    prezzoNetto = prezzoNetto * Decimal(str(1 - float(s.valore) / 100))
                elif applicazione == 'non scalare':
                    prezzoNetto = prezzoNetto - prezzoLordo * Decimal(str(float(s.valore) / 100))
            elif s.tipo_sconto == 'valore':
                prezzoNetto = prezzoNetto - Decimal(str(float(s.valore)))
    dao.valore_unitario_netto = prezzoNetto
    if parzialeNetto:
        parzialeNetto += prezzoNetto
        return dao, parzialeNetto
    else:
        return dao

