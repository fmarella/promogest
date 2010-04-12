# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: Dr astico  (Marco Pinna)<marco@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import gtk
import datetime
from math import sqrt

from promogest import Environment
from GladeWidget import GladeWidget
from AnagraficaComplessa import AnagraficaEdit
from AnagraficaDocumentiEditUtils import *

from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.Articolo import Articolo
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Operazione import Operazione
from promogest.dao.Cliente import Cliente
from promogest.dao.Multiplo import Multiplo

from utils import *
from utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo

if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt
if "SuMisura" in Environment.modulesList:
    from promogest.modules.SuMisura.ui import AnagraficaDocumentiEditSuMisuraExt
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
if "GestioneNoleggio" in Environment.modulesList:
    from promogest.modules.GestioneNoleggio.ui import AnagraficaDocumentiEditGestioneNoleggioExt
if "Pagamenti" in Environment.modulesList:
    from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt

class AnagraficaDocumentiEdit(AnagraficaEdit):
    """ Modifica un record dei documenti """

    def __init__(self, anagrafica):
        self.anapri=AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_documenti_detail_vbox',
                                'Dati Documento',
                                'anagrafica_documenti.glade')
#        self.placeWindow(self.getTopLevel())
        self._widgetFirstFocus = self.data_documento_entry
        # contenitore (dizionario) righe (riga 0 riservata per  variazioni in corso)
        self._righe = []
        self._righe.append({})
        # numero riga corrente
        self._numRiga = 0
        self.noClean=False
        # iteratore riga corrente
        self._iteratorRiga = None
        # cliente o fornitore ?
        self._tipoPersonaGiuridica = None
        self._operazione = None
        self.mattu = False
        # prezzo vendita/acquisto, ivato/non ivato
        self._fonteValore = None
        # carico (+) o scarico (-)
        self._segno = None
        # pagamento preferenziale dell'intestatario
        self._id_pagamento = None
        # magazzino preferenziale dell'intestatario
        self._id_magazzino = None
        # listino preferenziale dell'intestatario
        self._id_listino = None
        # banca preferenziale dell'intestatario
        self._id_banca = None
        # caricamento documento (interrompe l'azione degli eventi on_changed nelle combobox)
        self._loading = False
        # risposta richiesta variazione listini per costo variato: 'yes', 'no', 'all', 'none'
        self._variazioneListiniResponse = ''
        # mostrare variazione listini ?
        self._variazioneListiniShow = True
        #campi controllo modifica
        self._controllo_data_documento = None
        self._controllo_numero_documento = None
        self.reuseDataRow = False
        self.NoRowUsableArticle = False
        self.noleggio = True
        self.oneshot = False
        self.tagliaColoreRigheList = None
        # Inizializziamo i moduli in interfaccia!
        #self.draw()
        self.completion = gtk.EntryCompletion()
        self.completion.set_match_func(self.match_func)
        self.completion.connect("match-selected",
                                            self.on_completion_match)
        listore = gtk.ListStore(str, object)
        self.completion.set_model(listore)
        self.completion.set_text_column(0)
        self.articolo_entry.set_completion(self.completion)
        self.sepric = "  ~  "
        self.articolo_matchato = None
        self.checkMAGAZZINO = True
#        self.completion.set_minimum_key_length(3)
        if "Pagamenti" not in Environment.modulesList:
            self.notebook.remove_page(3)
        if "PromoWear" in Environment.modulesList:
            self.promowear_manager_taglia_colore_togglebutton.set_property("visible", True)
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)
        else:
            hidePromoWear(self)
        if "SuMisura" not in Environment.modulesList:
            hideSuMisura(self)
        if "GestioneNoleggio" not in Environment.modulesList:
            self.rent_checkbutton.destroy()
            self.hbox29.destroy()
            self.hbox30.destroy()
            self.arco_temporale_frame.destroy()
            self.noleggio_frame.destroy()
            self.noleggio = False
            self.prezzo_aquisto_entry.destroy()
            self.label38.destroy()
            self.label40.destroy()
            self.totale_periodo_label.destroy()

    def draw(self, cplx=False):
        self.cplx = cplx
        drawPart (self)

    def on_scorporo_button_clicked(self, button):
        """ Bottone con una "s" minuscola, che permette di effettuare "al volo"
        lo scorporo di un valore finale nel campo prezzo """
        iva = self.percentuale_iva_entry.get_text()
        if iva == "" or iva == "0":
            self.showMessage(msg="ATTENZIONE IVA a 0%")
        else:
            prezzoLordo = self.prezzo_lordo_entry.get_text()
            print "PREZZO LORDO " , prezzoLordo
            imponibile = float(prezzoLordo)/(1+float(iva)/100)
            print "IMPONIBILE", mN(str(imponibile))
            self.prezzo_lordo_entry.set_text(str(mN(str(imponibile))))
            self.prezzo_lordo_entry.grab_focus()

    def on_articolo_entry_focus_in_event(self, widget, event):
        """ controlliamo prima di effettuare una ricerca che il magazzino sia
        selezionato per rendere la ricerca possibile e corretta"""
#        print "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAZZINOOOOOOOOOO"
        if not findIdFromCombobox(self.id_magazzino_combobox) and self.checkMAGAZZINO:
            self.showMessage(msg="ATTENZIONE! \n SELEZIONARE UN MAGAZZINO\n PER UNA RICERCA CORRETTA")
            self.id_magazzino_combobox.grab_focus()
            self.checkMAGAZZINO = False

    def on_anagrafica_documenti_detail_vbox_key_press_event(self, widget=None, event=None):
        """ Mappiamo un po' di tasti su ana documenti"""
        print "AHAAHAHAHAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'F4':  # confermo e pulisco
            self.on_confirm_row_button_clicked(widget=None)
        elif keyname == 'F6':  # confermo e pulisco
            self.on_confirm_row_withoutclean_button_clicked(widget=None)

    def azzeraRiga(self, numero=0):
        """
        Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        """
        self._righe[numero] = {"idRiga": None,
                                "idMagazzino": None,
                                "magazzino": '',
                                "idArticolo": None,
                                "codiceArticolo": '',
                                "descrizione": '',
                                "percentualeIva": 0,
                                "idUnitaBase": None,
                                "unitaBase": '',
                                "idMultiplo": None,
                                "multiplo": '',
                                "idListino": None,
                                "listino": '',
                                "quantita": 1,
                                "moltiplicatore": 0,
                                "prezzoLordo": 0,
                                "applicazioneSconti": 'scalare',
                                "sconti": [],
                                "prezzoNetto": 0,
                                "totale": 0,
                                "codiceArticoloFornitore": '',
                                "prezzoNettoUltimo": 0,
                                "quantita_minima": None}
        if "SuMisura" in Environment.modulesList:
            AnagraficaDocumentiEditSuMisuraExt.azzeraRiga(self,numero)
        if "PromoWear" in Environment.modulesList:
            AnagraficaDocumentiEditPromoWearExt.azzeraRiga(self,numero)
        if "GestioneNoleggio" in Environment.modulesList:
            AnagraficaDocumentiEditGestioneNoleggioExt.azzeraRiga(self,numero)


    def azzeraRigaPartial(self, numero = 0, rigatampone=None):
        """
        Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        """
        self._righe[numero] = {"idRiga": None,
                                "idMagazzino": rigatampone['idMagazzino'],
                                "magazzino": rigatampone['magazzino'],
                                "idArticolo": rigatampone['idArticolo'],
                                "codiceArticolo": rigatampone['codiceArticolo'],
                                "descrizione": rigatampone['descrizione'],
                                "percentualeIva": rigatampone['percentualeIva'],
                                "idUnitaBase": rigatampone['idUnitaBase'],
                                "unitaBase": rigatampone['unitaBase'],
                                "idMultiplo": rigatampone['idMultiplo'],
                                "multiplo": rigatampone['multiplo'],
                                "idListino": rigatampone['idListino'],
                                "listino": rigatampone['listino'],
                                "quantita": rigatampone['quantita'],
                                "moltiplicatore": rigatampone['moltiplicatore'],
                                "prezzoLordo": rigatampone['prezzoLordo'],
                                "applicazioneSconti": 'scalare',
                                "sconti": rigatampone['sconti'],
                                "prezzoNetto": rigatampone['prezzoNetto'],
                                "totale": rigatampone['totale'],
                                "codiceArticoloFornitore": rigatampone['codiceArticoloFornitore'],
                                "prezzoNettoUltimo": rigatampone['prezzoNettoUltimo'],
                                "quantita_minima": rigatampone['quantita_minima']}
        if "SuMisura" in Environment.modulesList:
            AnagraficaDocumentiEditSuMisuraExt.azzeraRigaPartial(self,numero, rigatampone)


    def nuovaRiga(self):
        """
        Prepara per l'inserimento di una nuova riga
        """
        self._numRiga = 0
        self.azzeraRiga(0)

        self.articolo_entry.set_text('')
        self.unitaBaseLabel.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        self.percentuale_iva_entry.set_text('0')
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('1')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()
        self.totale_riga_label.set_text('0')
        self.giacenza_label.set_text('0')
        self.quantitaMinima_label.set_text('0')
        if "PromoWear" in Environment.modulesList:
            AnagraficaDocumentiEditPromoWearExt.setLabelInfo(self)
        if "SuMisura" in Environment.modulesList:
            AnagraficaDocumentiEditSuMisuraExt.setLabels(self)
        if "GestioneNoleggio" in Environment.modulesList:
            AnagraficaDocumentiEditGestioneNoleggioExt.setLabels(self)
        if "Pagamenti" in Environment.modulesList:
            AnagraficadocumentiPagamentExt.nuovaRiga(self)
            AnagraficadocumentiPagamentExt.attiva_prima_scadenza(self,False, True)
            AnagraficadocumentiPagamentExt.attiva_seconda_scadenza(self,False, True)
            AnagraficadocumentiPagamentExt.attiva_terza_scadenza(self,False, True)
            AnagraficadocumentiPagamentExt.attiva_quarta_scadenza(self,False, True)

        if len(self._righe) > 1:
            self.data_documento_entry.set_sensitive(False)
            self.id_operazione_combobox.set_sensitive(False)
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.articolo_entry.grab_focus()
        else:
            self.data_documento_entry.set_sensitive(True)
            self.id_persona_giuridica_customcombobox.set_sensitive(self.id_operazione_combobox.get_active() != -1)
            self.id_operazione_combobox.set_sensitive(True)
            if self._anagrafica._magazzinoFissato:
                findComboboxRowFromId(self.id_magazzino_combobox, self._anagrafica._idMagazzino)
            elif self._id_magazzino is not None:
                findComboboxRowFromId(self.id_magazzino_combobox, self._id_magazzino)
            self.id_magazzino_combobox.grab_focus()


    def nuovaRigaNoClean(self, rigatampone=None):
        """ Prepara per l'inserimento di una nuova riga seza cancellare i campi """
        self._numRiga = 0
        self.azzeraRigaPartial(0, rigatampone=rigatampone)
        self.unitaBaseLabel.set_text(rigatampone['unitaBase'])
        self.codice_articolo_fornitore_entry.set_text(rigatampone['codiceArticoloFornitore'])

    def clearRows(self):
        """ pulisce i campi per il trattamento e la conservazione delle righe """
        self._righe = []
        self._righe.append({})
        self._numRiga = 0
        self.modelRiga.clear()
        self._iteratorRiga = None
        self.nuovaRiga()

    def refresh_combobox_listini(self):

        if self._righe[0]["idArticolo"] is None:
            self.id_listino_customcombobox.combobox.clear
        else:
            a = fillComboboxListiniFiltrati(self.id_listino_customcombobox.combobox,
                                            self._righe[0]["idArticolo"],
                                            self._righe[0]["idMagazzino"],
                                            self.id_persona_giuridica_customcombobox.getId())
            if self._id_listino is not None:
                findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._id_listino)

    def on_id_multiplo_customcombobox_button_clicked(self, widget, toggleButton):
        on_id_multiplo_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"])

    def on_id_multiplo_customcombobox_changed(self, combobox):

        if self._loading:
            return
        self._righe[0]["idMultiplo"] = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        #multiplo = leggiMultiplo(self._righe[0]["idMultiplo"])
        multiplo = Multiplo().getRecord(id=self._righe[0]["idMultiplo"])
        self._righe[0]["multiplo"] = multiplo.denominazione_breve + ' ( ' + str(multiplo.moltiplicatore) + ' X )'
        self._righe[0]["moltiplicatore"] = multiplo.moltiplicatore
        self.calcolaTotaleRiga()

    def getPrezzoVenditaLordo(self, idListino, idArticolo):
        """ cerca il prezzo di vendita """
        prezzoLordo = 0
        sconti = []
        applicazione = "scalare"
        if idListino is not None and idArticolo is not None:
            listino = leggiListino(idListino, idArticolo)
            self._righe[0]["listino"] = listino["denominazione"]
            #print "TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY", self._fonteValore
            if (self._fonteValore == "vendita_iva"):
                    prezzoLordo = listino["prezzoDettaglio"]
                    sconti = listino["scontiDettaglio"]
                    applicazione = listino["applicazioneScontiDettaglio"]
            elif (self._fonteValore == "vendita_senza_iva"):
                    prezzoLordo = listino["prezzoIngrosso"]
                    sconti = listino["scontiIngrosso"]
                    applicazione = listino["applicazioneScontiIngrosso"]
        self._righe[0]["prezzoLordo"] = prezzoLordo
        self._righe[0]["idListino"] = idListino
        self._righe[0]["sconti"] = sconti
        self._righe[0]["applicazioneSconti"] = applicazione

    def getPrezzoAcquisto(self):
        """ funzione di lettura del prezzo di acquisto netto che serve per i noleggi """
        fornitura = leggiFornitura(self._righe[0]["idArticolo"], data=datetime.datetime.now())
        prezzo = fornitura["prezzoNetto"]
        self.prezzo_aquisto_entry.set_text(str(prezzo) or "0")

    def on_sconti_widget_button_toggled(self, button):
        """ """
        if button.get_property('active') is True:
            return

        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self.on_show_totali_riga()

    def on_sconti_testata_widget_button_toggled(self, button):
        """ """
        if button.get_property('active') is True:
            return
        self.calcolaTotale()

    def on_notebook_select_page(self,notebook,page, page_num):
        return
        #print notebook,page,page_num

    def on_notebook_switch_page(self, notebook, page, page_num):
        if page_num == 2:
            self.calcolaTotale()
        elif page_num ==3:
            if "Pagamenti" not in Environment.modulesList:
                fenceDialog()
                self.calcola_importi_scadenza_button.set_sensitive(False)
                self.controlla_rate_scadenza_button.set_sensitive(False)
                self.pulisci_scadenza_button.set_sensitive(False)

            #print "passato al terzo tab"

    def on_rent_checkbutton_toggled(self, checkbutton=None):
        """ check button in schermata documenti """
        stato = self.rent_checkbutton.get_active()
        self.noleggio = stato
        if not self.noleggio:
            self.prezzo_aquisto_entry.set_sensitive(False)
            self.coeficente_noleggio_entry.set_sensitive(False)
            self.totale_periodo_label.set_sensitive(False)
            self.giorni_label.set_sensitive(False)
            self.label40.set_sensitive(False)
            self.label33.set_sensitive(False)
            self.label31.set_sensitive(False)
        else:
            self.prezzo_aquisto_entry.set_sensitive(True)
            self.coeficente_noleggio_entry.set_sensitive(True)
            self.totale_periodo_label.set_sensitive(True)
            self.giorni_label.set_sensitive(True)
            self.label40.set_sensitive(True)
            self.label33.set_sensitive(True)
            self.label31.set_sensitive(True)

    def _refresh(self):
        """ Funzione importantissima di "impianto" del documento nella UI"""
        self._loading = True

        self._tipoPersonaGiuridica = None
        self._operazione = None
        self._fonteValore = None
        self._segno = None
        self._variazioneListiniResponse = ''
        self._variazioneListiniShow = True

        self.data_documento_entry.set_sensitive(self.dao.id is None)
        self.edit_date_and_number_button.set_sensitive(self.dao.id is not None)
        self.numero_documento_entry.set_sensitive(False)

        self.id_operazione_combobox.set_sensitive(self.dao.id is None)

        self.id_persona_giuridica_customcombobox.set_sensitive(self.dao.id is None)

        self.id_operazione_combobox.set_active(-1)
        self.id_persona_giuridica_customcombobox.set_active(-1)

        self._operazione = self.dao.operazione
        findComboboxRowFromId(self.id_operazione_combobox, self.dao.operazione)
        self.on_id_operazione_combobox_changed(self.id_operazione_combobox)
        self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
        if self._tipoPersonaGiuridica == "fornitore":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_fornitore)
            self.id_destinazione_merce_customcombobox.combobox.clear()
            self.id_destinazione_merce_customcombobox.set_sensitive(False)
        elif self._tipoPersonaGiuridica == "cliente":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_cliente)
            fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                    self.dao.id_cliente)
            findComboboxRowFromId(self.id_destinazione_merce_customcombobox.combobox,
                    (self.dao.id_destinazione_merce or -1))
            self.id_destinazione_merce_customcombobox.combobox.set_sensitive(True)

        self.data_documento_entry.set_text(dateToString(self.dao.data_documento))
        self.numero_documento_entry.set_text(str(self.dao.numero or '0'))
        self.showDatiMovimento()

        if "GestioneNoleggio" in Environment.modulesList:
            self.start_rent_entry.set_text(dateTimeToString(self.dao.data_inizio_noleggio))
            self.end_rent_entry.set_text(dateTimeToString(self.dao.data_fine_noleggio))
            self.on_end_rent_entry_focus_out_event()

        findComboboxRowFromId(self.id_pagamento_customcombobox.combobox, (self.dao.id_pagamento or -1))
        findComboboxRowFromId(self.id_banca_customcombobox.combobox, (self.dao.id_banca or -1) )
        findComboboxRowFromId(self.id_aliquota_iva_esenzione_customcombobox.combobox,
                (self.dao.id_aliquota_iva_esenzione or -1))
        self.id_agente_customcombobox.refresh(clear=True, filter=False)
        insertComboboxSearchAgente(self.id_agente_customcombobox,
                self.dao.id_agente)
        self.protocollo_entry1.set_text(self.dao.protocollo or '')
        self.note_pie_pagina_entry.set_text(self.dao.note_pie_pagina or '')
        textBuffer = self.note_interne_textview.get_buffer()
        if self.dao.note_interne is not None:
            textBuffer.set_text(self.dao.note_interne)
        else:
            textBuffer.set_text('')
        self.note_interne_textview.set_buffer(textBuffer)
        self.causale_trasporto_comboboxentry.child.set_text(self.dao.causale_trasporto or '')
        self.aspetto_esteriore_beni_comboboxentry.child.set_text(self.dao.aspetto_esteriore_beni or '')
        self.inizio_trasporto_entry.set_text(dateTimeToString(self.dao.inizio_trasporto))
        self.fine_trasporto_entry.set_text(dateTimeToString(self.dao.fine_trasporto))
        self.id_vettore_customcombobox.refresh(clear=True, filter=False)
        if self.dao.incaricato_trasporto == 'vettore':
            # Se l'incaricato e` un vettore, allora bisogna attivare il campo Porto
            self.vettore_radiobutton.set_active(True)
            insertComboboxSearchVettore(self.id_vettore_customcombobox,
                    self.dao.id_vettore)
            self.porto_combobox.set_sensitive(True)
#            print "VETTOREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
        if self.dao.porto == 'Franco':
            self.porto_combobox.set_active(0)
        elif self.dao.porto == 'Assegnato':
            self.porto_combobox.set_active(1)
            self.id_vettore_customcombobox.set_sensitive(True)

        if self.dao.incaricato_trasporto == 'destinatario':
            self.destinatario_radiobutton.set_active(True)
            self.id_vettore_customcombobox.set_sensitive(False)
            self.porto_combobox.set_sensitive(False)
        elif self.dao.incaricato_trasporto == 'mittente':
            self.mittente_radiobutton.set_active(True)
            self.id_vettore_customcombobox.set_sensitive(False)
            self.porto_combobox.set_sensitive(False)

        self.totale_colli_entry.set_text(str(self.dao.totale_colli or 0))
        self.totale_peso_entry.set_text(str(self.dao.totale_peso or 0))
        self.sconti_testata_widget.setValues(self.dao.sconti, self.dao.applicazione_sconti)
        # gestione righe documento in visualizzazione

        self.clearRows()

        for riga in self.dao.righe:
            self.azzeraRiga(0)
            j = self.dao.righe.index(riga) + 1
            magazzino = leggiMagazzino(riga.id_magazzino)
            #magazzino = Magazzino().getRecord(id=riga.id_magazzino)
            articolo = leggiArticolo(riga.id_articolo)
            listino = leggiListino(riga.id_listino)
            multiplo = leggiMultiplo(riga.id_multiplo)
            (sconti, applicazione) = getScontiFromDao(
                    riga.sconti, riga.applicazione_sconti)
            if "SuMisura" in Environment.modulesList and riga.misura_pezzo:
                altezza = (riga.misura_pezzo[-1].altezza)
                larghezza = (riga.misura_pezzo[-1].larghezza)
                moltiplicatore_pezzi = riga.misura_pezzo[-1].moltiplicatore
            else:
                altezza = ''
                larghezza = ''
                moltiplicatore_pezzi = ''

            self._righe[0]["idRiga"] = riga.id
            self._righe[0]["idMagazzino"] = riga.id_magazzino
            self._righe[0]["magazzino"] = magazzino['denominazione']
            self._righe[0]["idArticolo"] = riga.id_articolo
            self._righe[0]["codiceArticolo"] = articolo["codice"]
            self._righe[0]["descrizione"] = riga.descrizione
            self._righe[0]["percentualeIva"] = mN(riga.percentuale_iva,2)
            self._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
            self._righe[0]["unitaBase"] = articolo["unitaBase"]
            self._righe[0]["idMultiplo"] = riga.id_multiplo
            if multiplo["moltiplicatore"] != 0:
                self._righe[0]["multiplo"] = multiplo["denominazioneBreve"] + ' ( ' + str(mN(multiplo["moltiplicatore"],2)) + ' X )'
            else:
                self._righe[0]["multiplo"] = ''
            self._righe[0]["idListino"] = riga.id_listino
            self._righe[0]["listino"] = listino["denominazione"]
            self._righe[0]["quantita"] = mN(riga.quantita)
            self._righe[0]["moltiplicatore"] = mN(riga.moltiplicatore,2)
            self._righe[0]["prezzoLordo"] = mN(riga.valore_unitario_lordo)
            self._righe[0]["sconti"] = sconti
            self._righe[0]["applicazioneSconti"] = applicazione
            self._righe[0]["prezzoNetto"] = Decimal(riga.valore_unitario_netto)
            self._righe[0]["prezzoNettoUltimo"] = Decimal(riga.valore_unitario_netto)
            self._righe[0]["totale"] = 0
            if "SuMisura" in Environment.modulesList:
                self._righe[0]["altezza"] = mN(altezza)
                self._righe[0]["larghezza"] = mN(larghezza)
                self._righe[0]["molt_pezzi"] =mN(moltiplicatore_pezzi)
            if "GestioneNoleggio" in  Environment.modulesList:
                print " ISRENT  ",riga.isrent
                if riga.isrent :
                    self._righe[0]["arco_temporale"] = self.giorni_label.get_text()
                else:
                    self._righe[0]["arco_temporale"] = "NO"
                self._righe[0]["prezzo_acquisto"] = mN(riga.prezzo_acquisto_noleggio)
                self._righe[0]["divisore_noleggio"] = mN(riga.coeficente_noleggio)
            self.getTotaleRiga()
            if "GestioneNoleggio" in Environment.modulesList and self._righe[0]["arco_temporale"] != "NO" :
                totaleNoleggio = self.totaleNoleggio()

            self.unitaBaseLabel.set_text(self._righe[0]["unitaBase"])
            if self._tipoPersonaGiuridica == "fornitore":
                fornitura = leggiFornitura(riga.id_articolo, self.dao.id_fornitore, self.dao.data_documento, True)
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]

            self._righe.append(self._righe[0])
            rigadoc= self._righe[j]

            if "SuMisura" in Environment.modulesList:
                    altezza=rigadoc["altezza"]
                    larghezza =rigadoc["larghezza"]
                    molt_pezzi = rigadoc["molt_pezzi"]
            else:
                altezza = larghezza= molt_pezzi= ""
            #riempimento della treeview righe
            if "GestioneNoleggio" in Environment.modulesList:
                arc_temp = rigadoc["arco_temporale"]
            else:
                arc_temp = ""
            row = [j,
                    rigadoc["magazzino"],
                    rigadoc["codiceArticolo"],
                    rigadoc["descrizione"],
                    str(rigadoc["percentualeIva"]),
                    str(altezza),
                    str(larghezza),
                    str(molt_pezzi),
                    str(rigadoc["multiplo"]),
                    rigadoc["listino"],
                    rigadoc["unitaBase"],
                    str(rigadoc["quantita"]),
                    str(rigadoc["prezzoLordo"]),
                    rigadoc["applicazioneSconti"] + ' ' + getStringaSconti(rigadoc["sconti"]),
                    str(rigadoc["prezzoNetto"]),
                    arc_temp,
                    str(rigadoc["totale"])]
            self.modelRiga.append(row)


        self._loading = False
        if self.oneshot : self.persona_giuridica_changed()
        self.oneshot =False
        self.calcolaTotale()

        self.label_numero_righe.set_text(str(len(self.dao.righe)))
        #setto il notebook sulla prima pagina principale
        self.notebook.set_current_page(0)
        #imposto una nuova riga
        self.nuovaRiga()

        if self.dao.id is None or self.numero_documento_entry.get_text() == '0':
            self.id_operazione_combobox.grab_focus()
        else:
            self.id_magazzino_combobox.grab_focus()
        if "Pagamenti" in Environment.modulesList:
           AnagraficadocumentiPagamentExt.getScadenze(self)

    def setDao(self, dao):
        """
            imposta un nuovo dao Testata documenco
        """
        self.destinatario_radiobutton.set_active(True)
        self.id_vettore_customcombobox.set_sensitive(False)
        if dao is None:
            # Crea un nuovo Dao vuoto
            #Environment.tagliacoloretempdata = (False,[])
            self.dao = TestataDocumento()
            # Suggerisce la data odierna
            self.dao.data_documento = datetime.datetime.today()
            self._oldDaoRicreato = False #il dao è nuovo il controllo sul nuovo codice è necessario
            try:
                if Environment.conf.Documenti.tipo_documento_predefinito:
                    op = Operazione().select(denominazioneEM= Environment.conf.Documenti.tipo_documento_predefinito)
                    if op:
                        self.dao.operazione = op[0].denominazione
            except:
                print "TIPO_DOCUMENTO_PREDEFINITO NON SETTATO"
            try:
                if Environment.conf.Documenti.cliente_predefinito:
                    cli = Cliente().select(codicesatto=Environment.conf.Documenti.cliente_predefinito)
                    if cli:
                        self.dao.id_cliente = cli[0].id
                        self.oneshot = True
                        self.articolo_entry.grab_focus()
            except:
                print "CLIENTE_PREDEFINITO NON SETTATO"

        else:
            # Ricrea il Dao prendendolo dal DB
            self.dao = TestataDocumento().getRecord(id=dao.id)
            self._controllo_data_documento = dateToString(self.dao.data_documento)
            self._controllo_numero_documento = self.dao.numero
            self.oneshot = False
            self._oldDaoRicreato = True #il dao è nuovo il controllo sul nuovo codice non  è necessario
        self._refresh()

    def saveDao(self):
        """ Salvataggio del Dao
        """
        scontiRigaDocumentoList = {}
        if not(len(self._righe) > 1):
            messageInfo(msg="TENTATIVO DI SALVATAGGIO DOCUMENTO SENZA RIGHE???")
            raise Exception, "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????"

        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                    self.data_documento_entry,
                    'Inserire la data del documento !1')

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.dialogTopLevel,
                    self.id_operazione_combobox,
                    'Inserire il tipo di documento !')

        if self.id_persona_giuridica_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel,
                    self.id_persona_giuridica_customcombobox,
                    'Inserire l\'intestatario del documento !')

        self.dao.data_documento = stringToDate(self.data_documento_entry.get_text())
        if self.dao.id is not None and self.numero_documento_entry.get_text() != '0':

            if self.data_documento_entry.get_text() != self._controllo_data_documento\
                        or str(self.numero_documento_entry.get_text()) != str(self._controllo_numero_documento):
                numero = self.numero_documento_entry.get_text()
                idOperazione = findIdFromCombobox(self.id_operazione_combobox)
                daData, aData = getDateRange(self.data_documento_entry.get_text())
                docs = TestataDocumento().select(daNumero=numero,
                                                    aNumero=numero,
                                                    daData=daData, aData=aData,
                                                    idOperazione=idOperazione,
                                                    offset=None,
                                                    batchSize=None)
                if len(docs) > 0:
                    msg = """Attenzione!
Esiste già un documento numero %s per
l'anno di esercizio indicato nella data
del documento.
    Continuare comunque?""" % numero

                    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_INFO, gtk.BUTTONS_OK_CANCEL, msg)
                    response = dialog.run()
                    dialog.destroy()
                    if response == gtk.RESPONSE_NONE or response == gtk.RESPONSE_CANCEL:
                        return
                    elif response == gtk.RESPONSE_OK:
                        #nothing to do about it.
                        print """si è deciso di salvare un documento il cui numero
            è già stato usato per un altro. questo comporterà
            l 'esistenza di due documenti con lo stesso numero!"""


                self.dao.numero = numero
        self.dao.operazione = self._operazione
        if self._tipoPersonaGiuridica == "fornitore":
            self.dao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_cliente = None
            self.dao.id_destinazione_merce = None
        elif self._tipoPersonaGiuridica == "cliente":
            self.dao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_fornitore = None
            self.dao.id_destinazione_merce = findIdFromCombobox(self.id_destinazione_merce_customcombobox.combobox)

        self.dao.id_pagamento = findIdFromCombobox(self.id_pagamento_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(self.id_banca_customcombobox.combobox)
        self.dao.id_aliquota_iva_esenzione = findIdFromCombobox(self.id_aliquota_iva_esenzione_customcombobox.combobox)
        self.dao.id_agente = self.id_agente_customcombobox._id
        self.dao.protocollo = self.protocollo_entry1.get_text()
        self.dao.causale_trasporto = self.causale_trasporto_comboboxentry.child.get_text()
        self.dao.aspetto_esteriore_beni = self.aspetto_esteriore_beni_comboboxentry.child.get_text()
        self.dao.inizio_trasporto = stringToDateTime(self.inizio_trasporto_entry.get_text())
        self.dao.fine_trasporto = stringToDateTime(self.fine_trasporto_entry.get_text())

        if self.vettore_radiobutton.get_active():
            self.dao.id_vettore = self.id_vettore_customcombobox._id
            self.dao.incaricato_trasporto = 'vettore'
            if self.porto_combobox.get_active() == 0:
                self.dao.porto = 'Franco'
            elif self.porto_combobox.get_active() == 1:
                self.dao.porto = 'Assegnato'
            if not self.dao.id_vettore:
                obligatoryField(self.dialogTopLevel,
                    self.id_vettore_customcombobox,
                    'Quando si seleziona vettore è obbligatorio settarne uno!')
            print "QUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII", self.dao.id_vettore
        elif self.mittente_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'mittente'
            self.dao.porto = 'Franco'
        elif self.destinatario_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'destinatario'
            self.dao.porto = 'Assegnato'
        self.dao.totale_colli = self.totale_colli_entry.get_text()
        self.dao.totale_peso = self.totale_peso_entry.get_text()
        textBuffer = self.note_interne_textview.get_buffer()
        self.dao.note_interne = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        self.dao.note_pie_pagina = self.note_pie_pagina_entry.get_text()
        self.dao.applicazione_sconti = self.sconti_testata_widget.getApplicazione()
        if "GestioneNoleggio" in Environment.modulesList:
            self.dao.data_inizio_noleggio= self.start_rent_entry.get_text()
            self.dao.data_fine_noleggio = self.end_rent_entry.get_text()

        scontiSuTotale = []

        res = self.sconti_testata_widget.getSconti()
        if res:
            print " MA ALLLLLLLLLLLORA", res
            for scrow in res:
                daoScontost = ScontoTestataDocumento()
                daoScontost.valore = scrow["valore"]
                daoScontost.tipo_sconto = scrow["tipo"]
                scontiSuTotale.append(daoScontost)
#        print "DAOOOOOOOOOSCONTO", daoScontost.__dict__
        print "SCONTI SU TOTALE", scontiSuTotale
        self.dao.scontiSuTotale = scontiSuTotale

        scontiRigaDocumento=[]
        righeDocumento = []
        for i in range(1, len(self._righe)):
            daoRiga = RigaDocumento()
            daoRiga.id_testata_documento = self.dao.id
            daoRiga.id_articolo = self._righe[i]["idArticolo"]
            daoRiga.id_magazzino = self._righe[i]["idMagazzino"]
            daoRiga.descrizione = self._righe[i]["descrizione"]
            daoRiga.codiceArticoloFornitore = self._righe[i]["codiceArticoloFornitore"]
            daoRiga.id_listino = self._righe[i]["idListino"]
            daoRiga.percentuale_iva = self._righe[i]["percentualeIva"]
            daoRiga.applicazione_sconti = self._righe[i]["applicazioneSconti"]
            daoRiga.quantita = self._righe[i]["quantita"]
            daoRiga.id_multiplo = self._righe[i]["idMultiplo"]
            daoRiga.moltiplicatore = self._righe[i]["moltiplicatore"]
            daoRiga.valore_unitario_lordo = self._righe[i]["prezzoLordo"]
            daoRiga.valore_unitario_netto = self._righe[i]["prezzoNetto"]

            if "GestioneNoleggio" in Environment.modulesList:
                daoRiga.prezzo_acquisto_noleggio = self._righe[i]["prezzo_acquisto"]
                daoRiga.coeficente_noleggio = self._righe[i]["divisore_noleggio"]
                if self._righe[i]["arco_temporale"] != "NO":
                    daoRiga.isrent =  "True"
                else:
                    daoRiga.isrent = "False"
            sconti =[]
            listsco=[]
            if self._righe[i]["sconti"] is not None:
                for scon in self._righe[i]["sconti"]:
                    daoSconto = ScontoRigaDocumento()
                    daoSconto.valore = scon["valore"]
                    daoSconto.tipo_sconto = scon["tipo"]
                    scontiRigaDocumento.append(daoSconto)
            #scontiRigaDocumento[daoRiga] = sconti
            daoRiga.scontiRigaDocumento = scontiRigaDocumento
            scontiRigaDocumento =[]
            misure = []
            if "SuMisura" in Environment.modulesList and \
                            self._righe[i]["altezza"] != '' and \
                            self._righe[i]["larghezza"] != '':
                daoMisura = MisuraPezzo()
                daoMisura.altezza = float(self._righe[i]["altezza"] or 0)
                daoMisura.larghezza = float(self._righe[i]["larghezza"] or 0)
                daoMisura.moltiplicatore = float(self._righe[i]["molt_pezzi"] or 0)
                daoRiga.misura_pezzo = [daoMisura]
            #righe[i]=daoRiga
            righeDocumento.append(daoRiga)
        self.dao.righeDocumento = righeDocumento

        if "Pagamenti" in Environment.modulesList:
            AnagraficadocumentiPagamentExt.saveScadenze(self)

        tipoid = findIdFromCombobox(self.id_operazione_combobox)
        tipo = Operazione().getRecord(id=tipoid)
        if not self.dao.numero:
            valori = numeroRegistroGet(tipo=tipo.denominazione, date=self.data_documento_entry.get_text())
            self.dao.numero = valori[0]
            self.dao.registro_numerazione= valori[1]
        #porto in persist tre dizionari: uno per gli sconti sul totale, l'altro per gli sconti sulle righe e le righe stesse
        self.dao.persist()
        self.label_numero_righe.hide()
        text = str(len(self.dao.righe))
        self.label_numero_righe.set_text(text)
        self.label_numero_righe.show()

    def on_importo_da_ripartire_entry_changed(self, entry):
        self.dao.removeDividedCost()
        self.dao.ripartire_importo = False
        self.ripartire_importo_checkbutton.set_active(self.dao.ripartire_importo)
        self.dao.costo_da_ripartire = Decimal(self.importo_da_ripartire_entry.get_text())

        self.importo_sovrapprezzo_label.set_text(str((mN(self.dao.costo_da_ripartire) or 0)/self.dao.totalConfections))

    #def on_righe_treeview_drag_data_received(self, treeview,drag_context, x, y, selection, info, eventtime):
        #path, pos = treeview.get_dest_row_at_pos(x, y)
        #model = treeview.get_model()
        #if path:
            #self.target_iter___ = model.get_iter(path)

    def on_righe_treeview_drag_begin(self, treeview, drag_context):
        """ starting dragging func, just give the row start to drag """
        model, iter_to_copy = treeview.get_selection().get_selected()
        self.riga_partenza =  model.get_path(iter_to_copy)


    def on_righe_treeview_drag_leave(self, treeview, drag_context, timestamp):
        """ questa è la funzione di "scarico" del drop, abbiamo la riga di
        destinazione con la funzione get_drag_dest_row() e prendiamo
        la riga di partenza con la funzione precedente """
        duplicarighe= []
        model, iter_to_copy = treeview.get_selection().get_selected()
        row, pos = treeview.get_drag_dest_row()
        if self.riga_partenza != row[0]:
            duplicarighe = self._righe[:]
            if self.riga_partenza[0] > row[0]:
                self._righe.insert(row[0]+1,duplicarighe[self.riga_partenza[0]+1])
                self._righe.pop(self.riga_partenza[0]+2)
            elif self.riga_partenza[0] < row[0]:
                self._righe.insert(row[0]+2,duplicarighe[self.riga_partenza[0]+1])
                self._righe.pop(self.riga_partenza[0]+1)
            duplicarighe= []
        self.riga_partenza = None

    def on_righe_treeview_row_activated(self, treeview, path, column):
        """ riporta la riga selezionata in primo piano per la modifica"""

        sel = treeview.get_selection()
        (model, self._iteratorRiga) = sel.get_selected()
        (selRow, ) = path
        self._numRiga = selRow + 1
        self.azzeraRiga(0)
        self._loading = True

        self._righe[0]["idRiga"] = self._righe[self._numRiga]["idRiga"]
        self._righe[0]["idMagazzino"] = self._righe[self._numRiga]["idMagazzino"]
        self._righe[0]["magazzino"] = self._righe[self._numRiga]["magazzino"]
        self._righe[0]["idArticolo"] = self._righe[self._numRiga]["idArticolo"]
        self._righe[0]["codiceArticolo"] = self._righe[self._numRiga]["codiceArticolo"]
        self._righe[0]["descrizione"] = self._righe[self._numRiga]["descrizione"]
        self._righe[0]["codiceArticoloFornitore"] = self._righe[self._numRiga]["codiceArticoloFornitore"]
        self._righe[0]["idUnitaBase"] = self._righe[self._numRiga]["idUnitaBase"]
        self._righe[0]["unitaBase"] = self._righe[self._numRiga]["unitaBase"]
        self._righe[0]["idMultiplo"] = self._righe[self._numRiga]["idMultiplo"]
        self._righe[0]["multiplo"] = self._righe[self._numRiga]["multiplo"]
        self._righe[0]["idListino"] = self._righe[self._numRiga]["idListino"]
        self._righe[0]["listino"] = self._righe[self._numRiga]["listino"]
        self._righe[0]["quantita"] = self._righe[self._numRiga]["quantita"]
        self._righe[0]["moltiplicatore"] = self._righe[self._numRiga]["moltiplicatore"]
        self._righe[0]["prezzoLordo"] = self._righe[self._numRiga]["prezzoLordo"]
        self._righe[0]["percentualeIva"] = self._righe[self._numRiga]["percentualeIva"]
        self._righe[0]["applicazioneSconti"] = self._righe[self._numRiga]["applicazioneSconti"]
        self._righe[0]["sconti"] = self._righe[self._numRiga]["sconti"]
        self._righe[0]["prezzoNetto"] = self._righe[self._numRiga]["prezzoNetto"]
        self._righe[0]["totale"] = self._righe[self._numRiga]["totale"]
        self._righe[0]["prezzoNettoUltimo"] = self._righe[self._numRiga]["prezzoNettoUltimo"]
        if "SuMisura" in Environment.modulesList:
            self._righe[0]["altezza"] = self._righe[self._numRiga]["altezza"]
            self._righe[0]["larghezza"] = self._righe[self._numRiga]["larghezza"]
            self._righe[0]["molt_pezzi"] = self._righe[self._numRiga]["molt_pezzi"]
        if "GestioneNoleggio"in Environment.modulesList:
            self._righe[0]["divisore_noleggio"] = self._righe[self._numRiga]["divisore_noleggio"]
            self._righe[0]["prezzo_acquisto"] = self._righe[self._numRiga]["prezzo_acquisto"]
        self.giacenza_label.set_text(str(giacenzaArticolo(year=Environment.workingYear,
                                                idMagazzino=self._righe[0]["idMagazzino"],
                                                idArticolo=self._righe[0]["idArticolo"])))
        findComboboxRowFromId(self.id_magazzino_combobox, self._righe[0]["idMagazzino"])
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self._righe[0]["idArticolo"], True)
        findComboboxRowFromId(self.id_multiplo_customcombobox.combobox, self._righe[0]["idMultiplo"])
        self.refresh_combobox_listini()
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._righe[0]["idListino"])
        self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
        self.descrizione_entry.set_text(self._righe[0]["descrizione"])
        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
        self.percentuale_iva_entry.set_text(str(self._righe[0]["percentualeIva"]))
        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
        self.quantita_entry.set_text(str(self._righe[0]["quantita"]))
        try:
            self.quantitaMinima_label.set_text(str(Articolo().getRecord(id=self._righe[0]["idArticolo"]).quantita_minima))
        except:
            print "QUANTITA MINIMA NON PRESENTE"
        self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))
        self.prezzo_netto_label.set_text(str(self._righe[0]["prezzoNetto"]))
        self.totale_riga_label.set_text(str(self._righe[0]["totale"]))
        if "SuMisura" in Environment.modulesList:
            self.altezza_entry.set_text(str(self._righe[0]["altezza"]))
            self.larghezza_entry.set_text(str(self._righe[0]["larghezza"]))
            self.moltiplicatore_entry.set_text(str(self._righe[0]["molt_pezzi"]))
        if "GestioneNoleggio"in Environment.modulesList and self.noleggio:
            self.coeficente_noleggio_entry.set_text(str(self._righe[0]["divisore_noleggio"]))
            self.prezzo_aquisto_entry.set_text(str(self._righe[0]["prezzo_acquisto"]))
            #self._righe[0]["totale"] = self._righe[self._numRiga]["totale_periodo"]
            self.on_show_totali_riga()
            #self.getPrezzoAcquisto()

        self._loading = False
        self.articolo_entry.grab_focus()


    def on_confirm_row_button_clicked(self, widget=None,row=None):
        """
        Memorizza la riga inserita o modificata
        """
        self.checkMAGAZZINO = False
        if self.NoRowUsableArticle:
            self.showMessage('ARTICOLO NON USABILE IN UNA RIGA IN QUANTO ARTICOLO PRINCIPALE O PADRE!')
            return

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        #magazzino = Magazzino().getRecord(id=self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino['denominazione']

        if (self.data_documento_entry.get_text() == ''):
            self.showMessage('Inserire la data del documento !2')
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            self.showMessage('Inserire il tipo di documento !')
            return

        if (self.id_persona_giuridica_customcombobox.getId() is None):
            self.showMessage('Inserire l\'intestatario del documento !')
            return

        if ((self._righe[0]["idMagazzino"] is not None) and
                (self._righe[0]["idArticolo"] is None)):
            self.showMessage('Inserire l\'articolo !')
            return

        if ((self._righe[0]["idArticolo"] is not None) and
                (self._righe[0]["idMagazzino"] is None)):
            self.showMessage('Inserire il magazzino !')
            return

        costoVariato = (self._tipoPersonaGiuridica == "fornitore" and self._righe[0]["idArticolo"] is not None and
                (self._righe[0]["prezzoNetto"] != self._righe[0]["prezzoNettoUltimo"]) and
                (self._segno is not None and self._segno != ''))

        if self._numRiga == 0:
            self._numRiga = len(self._righe)
            self._righe.append(self._righe[0])
            inserisci = True
        else:
            inserisci = False
        # memorizzazione delle parti descrittive (liberamente modificabili)
        self._righe[0]["descrizione"] = self.descrizione_entry.get_text()
        self._righe[0]["codiceArticoloFornitore"] = self.codice_articolo_fornitore_entry.get_text()
        totale = self._righe[0]["totale"]
        #print "TOTALE IN CONFIRM", totale
        if "GestioneNoleggio" in Environment.modulesList and self.noleggio:
            self._righe[0]["divisore_noleggio"] = self.coeficente_noleggio_entry.get_text()
            self._righe[0]["arco_temporale"] = self.giorni_label.get_text()
            self._righe[0]["totale_periodo"] = self.totale_periodo_label.get_text()
            totale = self.totaleNoleggio()
        if "SuMisura" in Environment.modulesList:
            self._righe[0]["altezza"] = self.altezza_entry.get_text()
            self._righe[0]["larghezza"] = self.larghezza_entry.get_text()
            self._righe[0]["molt_pezzi"] = self.moltiplicatore_entry.get_text()
        self._righe[self._numRiga]["idRiga"] = self._righe[0]["idRiga"]
        self._righe[self._numRiga]["idMagazzino"] = self._righe[0]["idMagazzino"]
        self._righe[self._numRiga]["magazzino"] = self._righe[0]["magazzino"]
        self._righe[self._numRiga]["idArticolo"] = self._righe[0]["idArticolo"]
        self._righe[self._numRiga]["codiceArticolo"] = self._righe[0]["codiceArticolo"]
        self._righe[self._numRiga]["descrizione"] = self._righe[0]["descrizione"]
        self._righe[self._numRiga]["codiceArticoloFornitore"] = self._righe[0]["codiceArticoloFornitore"]
        self._righe[self._numRiga]["percentualeIva"] = self._righe[0]["percentualeIva"]
        self._righe[self._numRiga]["idUnitaBase"] = self._righe[0]["idUnitaBase"]
        self._righe[self._numRiga]["unitaBase"] = self._righe[0]["unitaBase"]
        self._righe[self._numRiga]["idMultiplo"] = self._righe[0]["idMultiplo"]
        self._righe[self._numRiga]["multiplo"] = self._righe[0]["multiplo"]
        self._righe[self._numRiga]["idListino"] = self._righe[0]["idListino"]
        self._righe[self._numRiga]["listino"] = self._righe[0]["listino"]
        self._righe[self._numRiga]["quantita"] = self._righe[0]["quantita"]
        self._righe[self._numRiga]["moltiplicatore"] = self._righe[0]["moltiplicatore"]
        self._righe[self._numRiga]["prezzoLordo"] = self._righe[0]["prezzoLordo"]
        self._righe[self._numRiga]["applicazioneSconti"] = self._righe[0]["applicazioneSconti"]
        self._righe[self._numRiga]["sconti"] = self._righe[0]["sconti"]
        self._righe[self._numRiga]["prezzoNetto"] = self._righe[0]["prezzoNetto"]
        if "GestioneNoleggio" in Environment.modulesList and self.noleggio:
            self._righe[self._numRiga]["divisore_noleggio"] = self._righe[0]["divisore_noleggio"]
            self._righe[self._numRiga]["prezzo_acquisto"] = self._righe[0]["prezzo_acquisto"]
            arco_temporale = self._righe[self._numRiga]["arco_temporale"] = self._righe[0]["arco_temporale"]
        else:
            arco_temporale="NO"
        if "SuMisura" in Environment.modulesList:
            altezza =self._righe[self._numRiga]["altezza"] = self._righe[0]["altezza"]
            larghezza=self._righe[self._numRiga]["larghezza"] = self._righe[0]["larghezza"]
            molt_pezzi=self._righe[self._numRiga]["molt_pezzi"] = self._righe[0]["molt_pezzi"]
        else:
            altezza= larghezza= molt_pezzi= ""
        # inserisci è true quando si sta editando la riga selezionata
        if inserisci is False:
            if self._iteratorRiga is None:
                return
            print "ITERATOREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", self._iteratorRiga
            #self.modelRiga.set_value(self._iteratorRiga, 0, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 1, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 2, self._righe[self._numRiga]["codiceArticolo"])
            self.modelRiga.set_value(self._iteratorRiga, 3, self._righe[self._numRiga]["descrizione"])
            self.modelRiga.set_value(self._iteratorRiga, 4, self._righe[self._numRiga]["percentualeIva"])
            if "SuMisura" in Environment.modulesList:
                self.modelRiga.set_value(self._iteratorRiga, 5, altezza)
                self.modelRiga.set_value(self._iteratorRiga, 6, larghezza)
                self.modelRiga.set_value(self._iteratorRiga, 7, molt_pezzi)
            self.modelRiga.set_value(self._iteratorRiga, 8, self._righe[self._numRiga]["multiplo"])
            self.modelRiga.set_value(self._iteratorRiga, 9, self._righe[self._numRiga]["listino"])
            self.modelRiga.set_value(self._iteratorRiga, 10, self._righe[self._numRiga]["unitaBase"])
            self.modelRiga.set_value(self._iteratorRiga, 11, self._righe[self._numRiga]["quantita"])
            self.modelRiga.set_value(self._iteratorRiga, 12, self._righe[self._numRiga]["prezzoLordo"])
            self.modelRiga.set_value(self._iteratorRiga, 13, self._righe[self._numRiga]["applicazioneSconti"] + (
                ' ' + getStringaSconti(self._righe[self._numRiga]["sconti"])))
            self.modelRiga.set_value(self._iteratorRiga, 14, self._righe[self._numRiga]["prezzoNetto"])

            if "GestioneNoleggio" in Environment.modulesList and self.noleggio:
                self.modelRiga.set_value(self._iteratorRiga, 15, arco_temporale)

            self.modelRiga.set_value(self._iteratorRiga, 16, totale)
        else:
            self.modelRiga.append([self._numRiga,
                            self._righe[self._numRiga]["magazzino"],
                            self._righe[self._numRiga]["codiceArticolo"],
                            self._righe[self._numRiga]["descrizione"],
                            self._righe[self._numRiga]["percentualeIva"],
                            altezza,
                            larghezza,
                            molt_pezzi,
                            self._righe[self._numRiga]["multiplo"],
                            self._righe[self._numRiga]["listino"],
                            self._righe[self._numRiga]["unitaBase"],
                            self._righe[self._numRiga]["quantita"],
                            self._righe[self._numRiga]["prezzoLordo"],
                            str(self._righe[self._numRiga]["applicazioneSconti"]) + ' ' + str(getStringaSconti(
                            self._righe[self._numRiga]["sconti"])),
                            self._righe[self._numRiga]["prezzoNetto"],
                            arco_temporale,
                            totale])
        self.righe_treeview.set_model(self.modelRiga)
        self.calcolaTotale()
        if costoVariato:
            if not(self._variazioneListiniResponse == 'all' or self._variazioneListiniResponse == 'none'):
                msg = 'Il prezzo di acquisto e\' stato variato:\n\n   si desidera aggiornare i listini di vendita ?'
                response = showComplexQuestion(self.dialogTopLevel, msg)
                if response == gtk.RESPONSE_YES:
                    self._variazioneListiniResponse = 'yes'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = True
                elif response == gtk.RESPONSE_NO:
                    self._variazioneListiniResponse = 'no'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = False
                elif response == gtk.RESPONSE_APPLY:
                    self._variazioneListiniResponse = 'all'
                    #la richiesta non verra' riproposta per la successiva variante o articolo
                    #ma per il prossimo articolo padre si'
                    self._variazioneListiniShow = True
                elif response == gtk.RESPONSE_REJECT:
                    self._variazioneListiniResponse = 'none'
                    #la richiesta non verra' riproposta per la successiva variante o articolo
                    #ma per il prossimo articolo padre si'
                    self._variazioneListiniShow = False

            if self._variazioneListiniShow:
                self.on_variazione_listini_button_clicked(self.variazione_listini_button)

        self._righe[self._numRiga]["prezzoNettoUltimo"] = self._righe[0]["prezzoNetto"]
        if self.reuseDataRow:
            rigatampone = self._righe[0]
            self.reuseDataRow=False
            self.nuovaRigaNoClean(rigatampone=rigatampone)
        else:
            self.nuovaRiga()

    def on_articolo_entry_insert_text(self, text):
        stringa = text.get_text()
#        print "AJAJAAJAJAJAJAJ", stringa, self.mattu,self.ricerca
        if self.mattu:
            text.set_text(stringa.split(self.sepric)[0])
        model = gtk.ListStore(str,object)
        vediamo = self.completion.get_model()
        vediamo.clear()
        art = []
        if stringa ==[] or len(stringa)<2:
            return
        if self.ricerca == "ricerca_codice_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codice=stringa, batchSize=20)
            else:
                art = Articolo().select(codice=stringa, batchSize=50)
        elif self.ricerca == "ricerca_descrizione_button":
            if len(text.get_text()) <3:
                art = Articolo().select(denominazione=stringa, batchSize=20)
            else:
                art = Articolo().select(denominazione=stringa, batchSize=50)
        elif self.ricerca == "ricerca_codice_a_barre_button":
            if len(text.get_text()) <7:
                art = Articolo().select(codiceABarre=stringa, batchSize=10)
            else:
                art = Articolo().select(codiceABarre=stringa, batchSize=40)
        elif self.ricerca == "ricerca_codice_articolo_fornitore_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codiceArticoloFornitore=stringa, batchSize=10)
            else:
                art = Articolo().select(codiceArticoloFornitore=stringa, batchSize=40)
#        print "MMMM",art
        for m in art:
            codice_art = m.codice
            den = m.denominazione
            bloccoInformazioni = codice_art+self.sepric+den
            compl_string = bloccoInformazioni
            if self.ricerca == "ricerca_codice_articolo_fornitore_button":
                caf = m.codice_articolo_fornitore
                compl_string = bloccoInformazioni+self.sepric+caf
            if self.ricerca == "ricerca_codice_a_barre_button":
                cb = m.codice_a_barre
                compl_string = bloccoInformazioni+self.sepric+cb
            model.append([compl_string,m])
        self.completion.set_model(model)

    def match_func(self, completion, key, iter):
        model = self.completion.get_model()
        self.mattu = False
        self.articolo_matchato = None
#        print "MODELLLLLLLLLLLLLLLLLL", model[iter][0], key, completion.get_text_column()
        if model[iter][0] and self.articolo_entry.get_text().lower() in model[iter][0].lower():
            return model[iter][0]
        else:
            return None

    def on_completion_match(self, completion=None, model=None, iter=None):
        self.mattu = True
        self.articolo_matchato = model[iter][1]
        self.articolo_entry.set_position(-1)

    def ricercaArticolo(self):
        print "ECCOMI QUIIIIIIIIIIIIIIII"
        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao.id)

        if (self.data_documento_entry.get_text() == ''):
            self.showMessage('Inserire la data del documento !')
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            self.showMessage('Inserire il tipo di documento !')
            return

        if (findIdFromCombobox(self.id_magazzino_combobox) is None):
            self.showMessage('Inserire il magazzino !')
            return

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None
        join = None
#        print "MA L?ARTICOLO E SEEZIONATO?", self.articolo_matchato, self.mattu
        if self.ricerca_codice_button.get_active():
            codice = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".articolo.codice"
                batchSize = Environment.conf.batch_size
        elif self.ricerca_codice_a_barre_button.get_active():
            codiceABarre = self.articolo_entry.get_text()
            join= Articolo.cod_barre
            if Environment.tipo_eng =="sqlite":
                orderBy = "codice_a_barre_articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".codice_a_barre_articolo.codice"
            batchSize = Environment.conf.batch_size
        elif self.ricerca_descrizione_button.get_active():
            denominazione = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.denominazione"
            else:
                orderBy = Environment.params["schema"]+".articolo.denominazione"
            batchSize = Environment.conf.batch_size
        elif self.ricerca_codice_articolo_fornitore_button.get_active():
            codiceArticoloFornitore = self.articolo_entry.get_text()
            join= Articolo.fornitur
            if Environment.tipo_eng =="sqlite":
                orderBy = "fornitura.codice_articolo_fornitore"
            else:
                orderBy = Environment.params["schema"]+".fornitura.codice_articolo_fornitore"
        batchSize = Environment.conf.batch_size
        if self.articolo_matchato:
#            print "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
            arts = [self.articolo_matchato]
        else:
            arts = Articolo().select(codice=prepareFilterString(codice),
                                        orderBy=orderBy,
                                        join = join,
                                        denominazione=prepareFilterString(denominazione),
                                        codiceABarre=prepareFilterString(codiceABarre),
                                        codiceArticoloFornitore=prepareFilterString(codiceArticoloFornitore),
                                        idFamiglia=None,
                                        idCategoria=None,
                                        idStato=None,
                                        offset=None,
                                        batchSize=None)
#        print "GGPGPGGPGPGPGGPGPGGP"
        if (len(arts) == 1):
            self.mostraArticolo(arts[0].id)
#            print "OASASASASASASASAS"
            self.articolo_matchato = None
        else:
            from RicercaComplessaArticoli import RicercaComplessaArticoli
            anag = RicercaComplessaArticoli(denominazione=denominazione,
                                            codice=codice,
                                            codiceABarre=codiceABarre,
                                            codiceArticoloFornitore=codiceArticoloFornitore)
            anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)

            anagWindow = anag.getTopLevel()
            anagWindow.connect("hide",
                               on_ricerca_articolo_hide,
                               anag)
            anagWindow.set_transient_for(self.dialogTopLevel)
            anag.show_all()
        self.cplx=False

    def on_promowear_manager_taglia_colore_togglebutton_toggled(self, togglebutton):
        active=self.promowear_manager_taglia_colore_togglebutton.get_active()
        if active:
            from promogest.modules.PromoWear.ui.ManageSizeAndColor import ManageSizeAndColor
            idPerGiu = self.id_persona_giuridica_customcombobox.getId()
            data = stringToDate(self.data_documento_entry.get_text())
            manag = ManageSizeAndColor(self, articolo=self.ArticoloPadre,
                                        data=data,
                                        idPerGiu=idPerGiu,
                                        idListino=self._id_listino,
                                        fonteValore=self._fonteValore)
            anagWindow = manag.getTopLevel()
            anagWindow.set_transient_for(self.dialogTopLevel)
        else:
            if self.tagliaColoreRigheList:
                for var in self.tagliaColoreRigheList:
                    self.mostraArticolo(var['id'],art=var)
            self.tagliaColoreRigheList = None
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)

    def mostraArticolo(self, id, art=None):
        mostraArticoloPart(self, id, art=art)


    def on_show_totali_riga(self, widget = None, event = None):
        """ calcola il prezzo netto """
        self._righe[0]["quantita"] = Decimal(self.quantita_entry.get_text().strip()) or 0
        self._righe[0]["prezzoLordo"] = Decimal(self.prezzo_lordo_entry.get_text().strip()) or 0
        self._righe[0]["percentualeIva"] = Decimal(self.percentuale_iva_entry.get_text().strip()) or 0
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self._righe[0]["prezzoNetto"] = Decimal(self._righe[0]["prezzoLordo"]) or 0
        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        if "GestioneNoleggio" in Environment.modulesList and self.noleggio:
            # Setti le label "indirette" come prezzoLordo dreivato dalla divisione
            self._righe[0]["arco_temporale"] = float(self.giorni_label.get_text() or 1)
            self._righe[0]["divisore_noleggio"] = float(self.coeficente_noleggio_entry.get_text() or 0)
            self._righe[0]["prezzo_acquisto"] = float(self.prezzo_aquisto_entry.get_text() or 0)
            if not (self._righe[0]["prezzo_acquisto"] == 0 and self._righe[0]["divisore_noleggio"] ==0):
                self._righe[0]["prezzoLordo"] = self._righe[0]["prezzo_acquisto"] / self._righe[0]["divisore_noleggio"]
                self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))

        self.getPrezzoNetto()
        self.prezzo_netto_label.set_text(str(self._righe[0]["prezzoNetto"]))

        self.calcolaTotaleRiga()
        return False


    def totaleNoleggio(self):
        totale = self._righe[0]["totale"]
        if "GestioneNoleggio" in Environment.modulesList and self.noleggio and self._righe[0]["arco_temporale"] != "NO":
            if str(self._righe[0]["divisore_noleggio"]).strip() == "1":
                totale = str(mN(float(self._righe[0]["totale"]) *float(self._righe[0]["arco_temporale"])))
                self.totale_periodo_label.set_text(totale)
            else:
                totale = str(mN(float(self._righe[0]["totale"]) *sqrt(float(self._righe[0]["arco_temporale"]))))
                self.totale_periodo_label.set_text(totale)
            self._righe[0]["totale_periodo"] = self.totale_periodo_label.get_text()
        return totale

    def calcolaTotaleRiga(self):
        """ calcola il totale riga """

        if self._righe[0]["prezzoNetto"] is None:
            self._righe[0]["prezzoNetto"] = 0
        if self._righe[0]["quantita"] is None:
            self._righe[0]["quantita"] = 0
        if self._righe[0]["moltiplicatore"] is None:
            self._righe[0]["moltiplicatore"] = 1
        elif self._righe[0]["moltiplicatore"] == 0:
            self._righe[0]["moltiplicatore"] = 1

        self.getTotaleRiga()
        # metto il totale riga nella label apposita"
        self.totale_riga_label.set_text(str(self._righe[0]["totale"]))
        if "GestioneNoleggio" in Environment.modulesList and self.noleggio:
            totaleNoleggio = self.totaleNoleggio()


    def getTotaleRiga(self):
        """ Questa funzione restituisce il valore del totale semplice della riga """
        segnoIva = 1
        percentualeIva = self._righe[0]["percentualeIva"]
        prezzoNetto = self._righe[0]["prezzoNetto"]
        quantita = self._righe[0]["quantita"]
        moltiplicatore = self._righe[0]["moltiplicatore"]
        self._righe[0]["totale"] = mN(Decimal(str(prezzoNetto)) * (Decimal(str(quantita)) * Decimal(str(moltiplicatore))),2)


    def getPrezzoNetto(self):
        """ calcola il prezzo netto dal prezzo lordo e dagli sconti """
        prezzoLordo = self._righe[0]["prezzoLordo"]
        prezzoNetto = self._righe[0]["prezzoLordo"]
        applicazione = self._righe[0]["applicazioneSconti"]
        sconti = self._righe[0]["sconti"]
        for s in sconti:
            if s["tipo"] == 'percentuale':
                if applicazione == 'scalare':
                    discaunt = str(s["valore"]).strip().replace(",",".")
                    prezzoNetto = prezzoNetto * (1 - Decimal(discaunt) / 100)
                elif applicazione == 'non scalare':
                    discaunt = str(s["valore"]).strip().replace(",",".")
                    prezzoNetto = prezzoNetto - prezzoLordo * Decimal(discaunt) / 100
            elif s["tipo"] == 'valore':
                prezzoNetto = prezzoNetto - Decimal(str(s["valore"]))

        self._righe[0]["prezzoNetto"] = prezzoNetto

    def calcolaTotale(self):
        calcolaTotalePart(self)

    def on_edit_date_and_number_button_clicked(self, toggleButton):
        """ This permit to change the date of the document """
        msg = 'Attenzione! Si sta per variare i riferimenti primari del documento.\n Continuare ?'
        dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            self.data_documento_entry.set_sensitive(True)
            self.numero_documento_entry.set_sensitive(True)
            self.data_documento_entry.grab_focus()
            self.id_persona_giuridica_customcombobox.set_sensitive(True)

    def showDatiMovimento(self):
        """ Show movimento related informations"""
        stringLabel = '-'
        if self.dao.id is not None:
            res = TestataMovimento().select(id_testata_documento= self.dao.id)
            if len(res) > 0:
                stringLabel = 'N.' + str(res[0].numero) + ' del ' + dateToString(res[0].data_movimento)
        self.rif_movimento_label.set_text(stringLabel)


    """ le ragioni per andare qui sotto non sono chiare, SONO segnali divisi per tab"""


    #NOTEBOOK TAB 1

    def on_undo_row_button_clicked(self, widget):
        """ annulla l'inserimento o la modifica della riga in primo piano """
        self.nuovaRiga()

    def on_delete_row_button_clicked(self, widget):
        """ elimina la riga in primo piano """

        if not(self._numRiga == 0):
            del(self._righe[self._numRiga])
            self.modelRiga.remove(self._iteratorRiga)
        self.calcolaTotale()
        self.nuovaRiga()

    def on_articolo_entry_key_press_event(self, widget, event):
        """ """
        keyname = gtk.gdk.keyval_name(event.keyval)
#        print "KEYNAMEEEEEE", keyname
        if self.mattu and keyname == 'Return' or keyname == 'KP_Enter':
            self.ricercaArticolo()
        if keyname == 'F3':
            self.ricercaArticolo()

    def on_search_row_button_clicked(self, widget):
        self.ricercaArticolo()

#    def on_ricerca_codice_button_clicked(self, widget):
#        """ """
#        if self.ricerca_codice_button.get_active()  and not self.cplx:
#            self.cplx=False
#            self.ricercaArticolo()

#    def on_ricerca_codice_a_barre_button_clicked(self, widget):
#        """ """
#        if self.ricerca_codice_a_barre_button.get_active()  and not self.cplx:
#            self.cplx=False
#            self.ricercaArticolo()

#    def on_ricerca_descrizione_button_clicked(self, widget):
#        """ """
#        if self.ricerca_descrizione_button.get_active()  and not self.cplx:
#            self.cplx=False
#            self.ricercaArticolo()

#    def on_ricerca_codice_articolo_fornitore_button_clicked(self, widget):
#        """ """
#        if self.ricerca_codice_articolo_fornitore_button.get_active() and self.cplx:
#            self.cplx=False
#            self.ricercaArticolo()

    def on_storico_costi_button_clicked(self, toggleButton):
        """ """
        from StoricoForniture import StoricoForniture
        idArticolo = self._righe[0]["idArticolo"]
        if self._tipoPersonaGiuridica == "fornitore":
            idFornitore = self.id_persona_giuridica_customcombobox.getId()
        else:
            idFornitore = None
        anag = StoricoForniture(idArticolo, idFornitore)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()

    def on_storico_listini_button_clicked(self, toggleButton):
        """ """
        from StoricoListini import StoricoListini
        idArticolo = self._righe[0]["idArticolo"]
        anag = StoricoListini(idArticolo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()

    def on_variazione_listini_button_clicked(self, toggleButton):
        """ """
        if self._righe[0]["idArticolo"] is None:
            self.showMessage('Selezionare un articolo !')
            return

        from VariazioneListini import VariazioneListini
        idArticolo = self._righe[0]["idArticolo"]
        costoNuovo = None
        costoUltimo = None
        if self._tipoPersonaGiuridica == "fornitore":
            costoNuovo = self._righe[0]["prezzoNetto"]
            costoUltimo = self._righe[0]["prezzoNettoUltimo"]
        anag = VariazioneListini(idArticolo, costoUltimo, costoNuovo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def on_multi_line_button_clicked(self, widget):
        """ gestione multilinea in utils"""
        on_multi_line_button_clickedPart(self, widget)

    def on_id_operazione_combobox_changed(self, combobox):
        """ Funzione di gestione cambiamento combo operazione"""
        self._operazione = findIdFromCombobox(self.id_operazione_combobox)
        #operazione = leggiOperazione(self._operazione)
        operazione = Operazione().getRecord(id=self._operazione)
        if operazione:
            if self._tipoPersonaGiuridica != operazione.tipo_persona_giuridica:
                self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
            self._tipoPersonaGiuridica = operazione.tipo_persona_giuridica
            self._fonteValore = operazione.fonte_valore
            self._segno = operazione.segno

        #if self._tipoPersonaGiuridica != operazione["tipoPersonaGiuridica"]:
            #self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
        #self._tipoPersonaGiuridica = operazione["tipoPersonaGiuridica"]
        #self._fonteValore = operazione["fonteValore"]
        #self._segno = operazione["segno"]

        if (self._tipoPersonaGiuridica == "fornitore"):
            self.persona_giuridica_label.set_text('Fornitore')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.label_listino.set_property('visible', False)
            self.id_listino_customcombobox.set_property('visible', False)
            self.prz_lordo_label.set_text('Costo')
            self.prz_netto_label.set_text('Costo netto')
            self.codice_articolo_fornitore_label.set_property('visible', True)
            self.codice_articolo_fornitore_entry.set_property('visible', True)
            self.protocollo_label.set_property('visible', True)
            self.protocollo_entry1.set_property('visible', True)
            self.numero_documento_label.set_text('N. reg.')
        elif (self._tipoPersonaGiuridica == "cliente"):
            self.persona_giuridica_label.set_text('Cliente')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')
        else:
            self.persona_giuridica_label.set_text('Cliente/Fornitore ?')
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')

        self.persona_giuridica_changed()
        self.data_documento_entry.grab_focus()

    def persona_giuridica_changed(self):
        if self._loading:
            return

        inseritoIntestatario = (self.id_persona_giuridica_customcombobox.getId() is not None)
        if inseritoIntestatario:
            datiIntestatario = self.id_persona_giuridica_customcombobox.getData()
            self._id_pagamento = datiIntestatario["id_pagamento"]
            self._id_magazzino = datiIntestatario["id_magazzino"]
            if self._tipoPersonaGiuridica == "cliente":
                self._id_listino = datiIntestatario["id_listino"]
                self._id_banca = datiIntestatario["id_banca"]

            if self.id_pagamento_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.id_pagamento_customcombobox.combobox, self._id_pagamento)
            if self.id_magazzino_combobox.get_active() == -1:
                findComboboxRowFromId(self.id_magazzino_combobox, self._id_magazzino)
            if self.id_banca_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.id_banca_customcombobox.combobox, self._id_banca)

        if self._tipoPersonaGiuridica == "cliente":
            self.id_destinazione_merce_customcombobox.set_sensitive(True)
            if self.id_persona_giuridica_customcombobox.getId() is None:
                self.id_destinazione_merce_customcombobox.combobox.clear
                self.id_destinazione_merce_customcombobox.set_sensitive(False)
            else:
                fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                        self.id_persona_giuridica_customcombobox.getId())
                self.id_destinazione_merce_customcombobox.set_sensitive(True)
            self.refresh_combobox_listini()
        else:
            self.id_destinazione_merce_customcombobox.set_sensitive(False)

    def on_id_magazzino_combobox_changed(self, combobox):
        if self._loading:
            return

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        #magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        magazzino = Magazzino().getRecord(id=self._righe[0]["idMagazzino"])
        if magazzino:
            self._righe[0]["magazzino"] = magazzino.denominazione
        self.refresh_combobox_listini()


    def on_id_listino_customcombobox_button_clicked(self, widget, toggleButton):
        on_id_listino_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"], None)

    def on_id_listino_customcombobox_button_toggled(self, button):
        if button.get_property('active') is True:
            return
        self.refresh_combobox_listini()

    def on_id_listino_customcombobox_changed(self, combobox=None):
        """ funzione richiamata quando viene modificato o settato il listino """
        if self._loading:
            return
        idListino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        idArticolo = self._righe[0]["idArticolo"]

        self.getPrezzoVenditaLordo(idListino, idArticolo)
        self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))
        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], True)
        self.on_show_totali_riga()

    def on_new_row_button_clicked(self, widget):
        self.nuovaRiga()

    def on_confirm_row_withoutclean_button_clicked(self, widget=None):
        self.reuseDataRow = True
        self.on_confirm_row_button_clicked(widget)

    def on_larghezza_entry_key_press_event(self, entry, event):
        """ portata nel modulo su misura"""
        AnagraficaDocumentiEditSuMisuraExt.on_larghezza_entry_key_press_eventPart(self, entry, event)

    def on_altezza_entry_key_press_event(self, entry, event):
        """ portata nel modulo su misura """
        AnagraficaDocumentiEditSuMisuraExt.on_altezza_entry_key_press_eventPart(self, entry, event)

    def on_moltiplicatore_entry_key_press_event (self, entry, event):
        self.on_altezza_entry_key_press_event(entry, event)
        self.on_show_totali_riga()

    def on_quantita_entry_focus_out_event(self, entry, event):
        on_quantita_entry_focus_out_eventPart(self, entry, event)

    def on_end_rent_entry_focus_out_event(self, entry=None, event=None):
        if self.end_rent_entry.get_text() and self.start_rent_entry.get_text():
            self._durataNoleggio = stringToDateTime(self.end_rent_entry.get_text())- stringToDateTime(self.start_rent_entry.get_text())
            if self._durataNoleggio.days >0:
                self.giorni_label.set_text(str(self._durataNoleggio.days) or "")
                self.rent_checkbutton.set_active(True)
            else:
                msg =  "ERRORE NELLA DURATA DEL NOLEGGIO\nNON PUO' ESSERE ZERO O NEGATIVA"
                self.showMessage(msg)

    #NOTEBOOK FINE TAB 3

    #TAB 2
    def on_incaricato_trasporto_radiobutton_toggled(self, radiobutton):

        self.id_vettore_customcombobox.set_sensitive(self.vettore_radiobutton.get_active())
        self.porto_combobox.set_sensitive(self.vettore_radiobutton.get_active())
        # Se e` selezionato mittente o destinatario, riempe automaticamente il campo porto
        # con Franco o Assegnato.
        if not self.vettore_radiobutton.get_active():
            self.id_vettore_customcombobox.set_active(0)
        if self.mittente_radiobutton.get_active():
            self.porto_combobox.set_active(0)
        elif self.destinatario_radiobutton.get_active():
            self.porto_combobox.set_active(1)

    def on_id_destinazione_merce_customcombobox_button_clicked(self, widget, toggleButton):
        on_id_destinazione_merce_customcombobox_clicked(widget,
                                                toggleButton,
                                                self.id_persona_giuridica_customcombobox.getId())

    #END TAB 2



    #NOTEBOOK TAB 3

    def on_pulisci_scadenza_button_clicked(self, button):
        AnagraficadocumentiPagamentExt.on_pulisci_scadenza_button_clicked(self, button)

    def on_controlla_rate_scadenza_button_clicked(self, button):
        """ bottone che controlla le rate scadenza """
        AnagraficadocumentiPagamentExt.controlla_rate_scadenza(self,True)

    def on_calcola_importi_scadenza_button_clicked(self, button):
        """calcola importi scadenza pagamenti """
        AnagraficadocumentiPagamentExt.attiva_scadenze(self)
        AnagraficadocumentiPagamentExt.dividi_importo(self)
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self)

    def on_seleziona_prima_nota_button_clicked(self, button):
        """ Seleziona la prima nota da utilizzare come riferimento """
        AnagraficadocumentiPagamentExt.on_seleziona_prima_nota_button_clicked(self, button)

    def on_seleziona_seconda_nota_button_clicked(self, button):
        """ Seleziona la seconda nota di credito da utilizzare come riferimento """
        AnagraficadocumentiPagamentExt.on_seleziona_seconda_nota_button_clicked(self, button)

    def on_data_pagamento_prima_scadenza_entry_changed(self, entry):
        """ Reimposta i totali saldato e da saldare alla modifica della data
            di pagamento della prima scadenza """
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self)

    def on_data_pagamento_seconda_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self)

    def on_data_pagamento_terza_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self)

    def on_data_pagamento_quarta_scadenza_entry_changed(self, entry):
        AnagraficadocumentiPagamentExt.ricalcola_sospeso_e_pagato(self)

    # NOTEBOOK FINE TAB 3

    def showMessage(self, msg):
        """ Generic Show dialog func """
        dialog = gtk.MessageDialog(self.anapri,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        dialog.run()
        dialog.destroy()

    def on_avvertimento_sconti_button_clicked(self, button):
        self.notebook.set_current_page(2)

    def on_articolo_entry_icon_press(self,entry, position,event ):
        if position.real == 0:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            self.menu_ricerca.popup( None, None, None, event.button, time)
            #print "CERCA"
        else:                            #secondary
            self.articolo_entry.set_text("")

    def on_descrizione_entry_icon_press(self,entry, position,event ):
        if position.real == 1:
            self.descrizione_entry.set_text("")

    def on_codice_item_toggled(self,toggled):
        """ ATTENZIONE schifezza per tamponare il bug di gtk 2.17 numero :
        Bug 607492 - widget.get_name() """
        if toggled.get_active():
#            print "OLLLLALAAAA", dir(toggled), toggled.__dict__, toggled.get_label(), dir(toggled.get_name())
#            self.ricerca = toggled.get_name()
            self.ricerca = toggled.get_tooltip_text()
