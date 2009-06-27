# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author:M3nt0r3  <m3nt0r3@gmail.com>
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
                            codiceEM=search_string,
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

def fillSchedaLavorazioneFromEmail(ui):
    text = []
    try:
        email = file("/home/stampalux/Form ordine partecipazioni.eml","r")
        text = email.readlines()

        email.close()
    except:
        print "ATTENZIONEEEEEEEEEEEE!!!! FILE EMAIL NON PRESENTE"
    for line in text:
        line = line.decode('iso-8859-1', 'replace').encode('utf8')
        lista = line.split(":")
        campo = lista[0].strip()
        #print "CAMPOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",campo
        #valore = lista[1].strip()
        if campo == "Subject":
            if lista[1].strip() != "Form ordine partecipazioni":
                raise Exception,"errore email di tipo errato"
        if campo == "From":
            ui.prima_email_entry.set_text(lista[1].strip())
        elif campo == "Date":
            #Tue, 3 Mar 2009 22:03:38 +0100
            a = lista[1].strip().split(",")[1][0:-2].strip()
            a = a.replace("May", "Mag")
            a = a.replace("Jun", "Giu")
            a = a.replace("Jul", "Lug")
            a = a.replace("Aug", "Ago")
            a = a.replace("Sep", "Set")
            a = a.replace("Oct", "Ott")
            a = a.replace("Dec", "Dic")
            a = a.replace("Jan", "Gen")
            ui.data_presa_in_carico_entry.set_text(dateToString(time.strptime(a, "%d %b %Y")))
        elif campo == "Nome_sposo":
            ui.nome_sposo_entry.set_text(lista[1].strip().upper())
        elif campo == "Cognome_sposo":
            cognome_sposo = lista[1].strip().upper()
            ui.cognome_sposo_entry.set_text(cognome_sposo)
        elif campo == "Nome_sposa":
            ui.nome_sposa_entry.set_text(lista[1].strip())
        elif campo == "Cognome_sposa":
            cognome_sposa = lista[1].strip().upper()
            ui.cognome_sposa_entry.set_text(cognome_sposa)
        elif campo == "messaggio alternativo a annunciano...":
            messaggio_alternativo  = lista[1].strip().upper()
        elif campo == "cerimonia":
            cerimonia  = lista[1].strip().upper()
        elif campo == "nome_luogo_cerimonia":
            nome_luogo_cerimonia  = lista[1].strip().upper()
        elif campo == "localita_matrimonio":
            localita_matrimonio  = lista[1].strip().upper()
        elif campo == "Citta_matrimonio":
            ui.provenienza_entry.set_text(lista[1].strip().upper())
        elif campo == "Data_matrimonio":
            print lista[1].strip()
            datamat=lista[1].strip()
            datamat=datamat[0:-2]+"20"+datamat[-2:]
            ui.data_matrimonio_entry.set_text(datamat)
        elif campo == "Ora_matrimonio":
            ora_matrimonio  = lista[1].strip().upper()
        elif campo == "Citta_sposo":
            citta_sposo  = lista[1].strip().upper()
        elif campo == "Via_e_num_sposo":
            via_e_num_sposo  = lista[1].strip().upper()
        elif campo == "num_sposo":
            num_sposo  = lista[1].strip().upper()
        elif campo == "Citta_sposa":
            citta_sposa  = lista[1].strip().upper()
        elif campo == "Via_e_num_sposa":
            via_e_num_sposa  = lista[1].strip().upper()
        elif campo == "Num_sposa":
            num_sposa  = lista[1].strip()
        elif campo == "Indirizzo_coniugale":
            indirizzo_coniugale  = lista[1].strip().upper()
        elif campo == "Luogo_ricevimento":
            luogo_ricevimento  = lista[1].strip()
        elif campo == "biglietto_bomboniera":
            biglietto_bomboniera  = lista[1].strip().upper()
            if biglietto_bomboniera:
                ui.bomba_si_checkbutton.set_active(True)
            else:
                ui.bomba_no_checkbutton.set_active(True)
        elif campo == "gradita_conferma":
            gradita_conferma  = lista[1].strip().upper()
        elif campo == "Commenti":
            commenti  = lista[1].strip().upper()
        elif campo == "carattere":
            carattere_stampa  = lista[1].strip().upper()
        elif campo == "colore":
            colore_stampa  = lista[1].strip().upper()
        elif campo == "sito_omaggio":
            sito_omaggio  = lista[1].strip().upper()
        elif campo == "Luogo_spedizione":
            luogo_spedizione  = lista[1].strip().upper()
        elif campo == "nome":
            ui.referente_entry.set_text(lista[1].strip().upper())
        elif campo == "Presso":
            ui.presso_entry.set_text(lista[1].strip().upper())
        elif campo == "Via_e_num":
            ui.via_piazza_entry.set_text(lista[1].strip().upper())
            #dao.num_civ = ""
        elif campo == "Citta":
            ui.localita_entry.set_text(lista[1].strip().upper())
        elif campo == "Provincia":
            ui.provincia_entry.set_text(lista[1].strip().upper())
        elif campo == "CAP":
            ui.zip_entry.set_text(lista[1].strip().upper())
        elif campo == "telefono":
            ui.telefono_entry.set_text(lista[1].strip().upper())
        elif campo == "Cellulare":
            ui.cellulare_entry.set_text(lista[1].strip().upper())
        elif campo == "codicefiscale":
            codicefiscale  = lista[1].strip().upper()
        elif campo == "Note_aggiuntive":
            ui.note_final_entry.set_text(lista[1].strip().upper())
        elif campo == "pagamento":
            pagamento  = lista[1].strip().upper()
        elif campo == "documento":
            if lista[1].strip() == "ricevuta":
                ui.ricevuta_checkbutton.set_active(True)
                #dao.fattura  = False
            #else:
                #dao.fattura = True
        elif campo == "autorizzo_si":
            autorizzo_si  = lista[1].strip().upper()
        elif campo == "privacy":
            privacy  = lista[1].strip().upper()
        elif campo == "pagina":
            pagina  = lista[1].strip().upper()
        elif campo == "spesa":
            pagina  = lista[1].strip().upper()
        elif campo == "PRODOTTO":
            prodotto  = lista[1].strip().upper()
        elif campo == "CODICE PARTECIPAZIONE":
            codParte = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')[1:-1]
            quantitaParte = lista[2].strip().split("-")[0].strip()[1:-1]
            print "CODICE PARTECIPAZIONE", codParte
        elif campo == "CODICE INVITO":
            codInvito = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')[1:-1]
            quantitaInvito = lista[2].strip().split("-")[0].strip()[1:-1]
            print codInvito, quantitaInvito
        elif campo == "CODICE BOMBONIERA":
            codBombo = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')[1:-1]
            quantitaBombo = lista[2].strip().split("-")[0].strip()[1:-1]
            print codBombo, quantitaBombo
        elif campo == "PERCENTUALE DI SCONTO APPLICATO":
            percentualeSconto = lista[1].strip()[0:-1]
            print percentualeSconto
        elif campo == "COSTO STAMPA APPLICATO":
            costoStampa = lista[1].strip()
        elif campo == "TOTALE":
            totale = lista[1].strip()[1:].strip()
            print totale

    ordine = {"colore_stampa":colore_stampa,
                "carattere_stampa":carattere_stampa,
                "prodotto":prodotto,
                "codParte":codParte,
                "quantitaParte":quantitaParte,
                "codInvito":codInvito,
                "quantitaInvito":quantitaInvito,
                "codBombo":quantitaBombo,
                "costoStampa":costoStampa,
                "percentualeSconto": percentualeSconto,
                "totale":totale}

    ui.nomi_sposi_entry.set_text(cognome_sposo.upper()+" - "+cognome_sposa.upper())
    return ordine
