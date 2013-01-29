# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Authors:
#             Andrea Argiolas <andrea@promotux.it>
#             JJDaNiMoTh <jjdanimoth@gmail.com>
#             Dr astico (Marco Pinna) <marco@promotux.it>
#             Francesco Meloni <francesco@promotux.it>
#             Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.gtk_compat import *
import datetime

from promogest import Environment
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.anagDocumenti.AnagraficaDocumentiEditUtils import *

from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.Articolo import Articolo
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Operazione import Operazione
from promogest.dao.Multiplo import Multiplo
from promogest.dao.Pagamento import Pagamento
from promogest.dao.Cliente import Cliente
#from promogest.dao.RigaRitenutaAcconto import RigaRitenutaAcconto
from promogest.ui.DettaglioGiacenzaWindow import DettaglioGiacenzaWindow
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.CachedDaosDict import CachedDaosDict
from promogest.dao.RigaRitenutaAcconto import RigaRitenutaAcconto

if posso("PW"):
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt
if posso("SM"):
    from promogest.modules.SuMisura.ui import AnagraficaDocumentiEditSuMisuraExt
    from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
if posso("GN"):
    from promogest.modules.GestioneNoleggio.ui import AnagraficaDocumentiEditGestioneNoleggioExt
from promogest.modules.Pagamenti.ui.PagamentiNotebookPage import PagamentiNotebookPage
from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
if posso("ADR"):
    from promogest.modules.ADR.ui import AnagraficaDocumentiEditADRExt


class AnagraficaDocumentiEdit(AnagraficaEdit):
    """ Modifica un record dei documenti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati Documento',
                                root='anagrafica_documenti_detail_vbox',
                                path='anagrafica_documenti.glade')
        #self.placeWindow(self.getTopLevel())
        self._widgetFirstFocus = self.data_documento_entry
        # contenitore (dizionario) righe (
#           riga 0 riservata per  variazioni in corso)
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
        self._loading = False
        # risposta richiesta variazione
#        listini per costo variato: 'yes', 'no', 'all', 'none'
        self._variazioneListiniResponse = ''
        # mostrare variazione listini ?
        self._variazioneListiniShow = True
        #campi controllo modifica
        self._controllo_data_documento = None
        self._controllo_numero_documento = None
        self._controllo_parte_documento = None
        self.reuseDataRow = False
        self.NoRowUsableArticle = False
        self.noleggio = True
        self.oneshot = False
        self.tagliaColoreRigheList = None
        self.visualizza_prezzo_alternativo = False

        # Inizializziamo i moduli in interfaccia!
        #self.draw()
        self.completion = self.ricerca_articolo_entrycompletition
        if Environment.pg3:
            self.completion.set_match_func(self.match_func, None)
        else:
            self.completion.set_match_func(self.match_func)
        self.completion.set_text_column(0)
        self.articolo_entry.set_completion(self.completion)
        self.sepric = "  ~  "
        self.articolo_matchato = None
        self.checkMAGAZZINO = True
        self.edited_rows = []
        self.deleted_rows = []
#        self.completion.set_minimum_key_length(3)

        if posso("PW"):
            self.promowear_manager_taglia_colore_togglebutton.set_property(
                                                            "visible", True)
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(
                                                                    False)
        else:
            hidePromoWear(self)
        if not posso("SM"):
            hideSuMisura(self)
        if not posso("GN"):
            self.rent_checkbutton.destroy()
            self.hbox29.destroy()
            self.hbox30.destroy()
            self.arco_temporale_frame.destroy()
            self.noleggio_frame.destroy()
            self.noleggio = False
            self.prezzo_aquisto_entry.destroy()
            self.X_label.destroy()
            self.GG_label.destroy()
            self.totale_periodo_label.destroy()
        if not posso("ADR"):
            hideADR(self)
        self.nolottotemp = True
        self.auto_lotto_temp = True
        if not setconf("Documenti", "lotto_temp"):
            self.lotto_temp_hbox.destroy()
            self.nolottotemp = False
        if Environment.azienda != "daog":
            self.id_persona_giuridica_diretta_customcombobox.destroy()
            self.persona_giuridica_diretta_label.destroy()
            self.diretta_label.destroy()

    def on_lotto_temp_entry_changed(self, entry):
        """ Conferma automaticamente la riga dopo 3 secondi se viene
        inserito il lotto temp.
        """
        def do_confirm_row():
            if (len(self.lotto_temp_entry.get_text()) >= 6) and \
                    self.auto_lotto_temp:
                self.on_confirm_row_button_clicked(widget=None)
        if self.ricerca_criterio_combobox.get_active() == 1:
            gobject.timeout_add(500, do_confirm_row)

    def draw(self, cplx=False):
        """ Funzione che si occupa di disegnare l'interfaccia
        """
        self.cplx = cplx
        drawPart(self)
        self.pagamenti_page = PagamentiNotebookPage(self)
        self.notebook.append_page(self.pagamenti_page.pagamenti_vbox,
                                self.pagamenti_page.pagamenti_page_label)

    def on_scorporo_button_clicked(self, button):
        """ Bottone con una "s" minuscola, che permette di effettuare "al volo"
        lo scorporo di un valore finale nel campo prezzo
        """
        ivaobj = findStrFromCombobox(self.id_iva_customcombobox.combobox, 0)
        if not ivaobj:
            return
        if type(ivaobj) != type("CIAO"):
            iva = ivaobj.percentuale
            if iva == "" or iva == "0":
                messageInfo(msg=_("ATTENZIONE IVA a 0%"))
            else:
                prezzoLordo = self.prezzo_lordo_entry.get_text()
                imponibile = float(prezzoLordo) / (1 + float(iva) / 100)
                self.prezzo_lordo_entry.set_text(str(mN(str(imponibile))))
                self.prezzo_lordo_entry.grab_focus()

    def on_switch_prezzo_button_clicked(self, button):
        """ Bottone che alterna il prezzo ingrosso e quello dettaglio
        """
        idListino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        idArticolo = self._righe[0]["idArticolo"]
        prezzi = leggiListino(idListino, idArticolo)
        if not self.visualizza_prezzo_alternativo:
            self.prezzo_lordo_entry.set_text(str(prezzi["prezzoDettaglio"]))
            self.visualizza_prezzo_alternativo = True
        else:
            self.prezzo_lordo_entry.set_text(str(prezzi["prezzoIngrosso"]))
            self.visualizza_prezzo_alternativo = False

    def on_articolo_entry_focus_in_event(self, widget, event):
        """ Controlliamo prima di effettuare una ricerca che il magazzino sia
        selezionato per rendere la ricerca possibile e corretta
        """
        if not findIdFromCombobox(self.id_magazzino_combobox) \
                                                    and self.checkMAGAZZINO:
            messageInfo(msg=_(
        "ATTENZIONE! \n SELEZIONARE UN MAGAZZINO\n PER UNA RICERCA CORRETTA"))
            self.id_magazzino_combobox.grab_focus()
            self.checkMAGAZZINO = False

    def on_anagrafica_documenti_detail_vbox_key_press_event(self,
                                                widget=None, event=None):
        """ Mappiamo un po' di tasti su anag documenti
        """
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'F4':  # confermo e pulisco
            self.on_confirm_row_button_clicked(widget=None)
        elif keyname == 'F6':  # confermo e non pulisco
            self.on_confirm_row_withoutclean_button_clicked(widget=None)

    def azzeraRiga(self, numero=0):
        """
        Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        "ritAccPercentuale": 0,
        "rivalsaPercentuale": 0,
        "ritCaProvvigionale": False,
        "ritInarCassa":0
        """
        self._righe[numero] = {"idRiga": None,
                                "idMagazzino": None,
                                "magazzino": '',
                                "idArticolo": None,
                                "codiceArticolo": '',
                                "descrizione": '',
                                "percentualeIva": 0,
                                "idAliquotaIva": None,
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
                                "quantita_minima": None,
                                "ritenute": [],
                                "numeroLottoArticoloFornitura": None,
                                "numeroLottoTemp": "",
                                "dataScadenzaArticoloFornitura": None,
                                "dataProduzioneArticoloFornitura": None,
                                "dataPrezzoFornitura": None,
                                "ordineMinimoFornitura": None,
                                "tempoArrivoFornitura": None,
                                "rigaMovimentoFornituraList": [],
                                }
        #chiavi aggiuntive al dizionario RIGA
        if posso("SM"):
            AnagraficaDocumentiEditSuMisuraExt.azzeraRiga(self, numero)
        if posso("PW"):
            AnagraficaDocumentiEditPromoWearExt.azzeraRiga(self, numero)
        if posso("GN"):
            AnagraficaDocumentiEditGestioneNoleggioExt.azzeraRiga(self, numero)

    def azzeraRigaPartial(self, numero=0, rigatampone=None):
        """Azzera i campi del dizionario privato delle righe, alla riga
        indicata (o alla 0-esima)
        """
        self._righe[numero] = {"idRiga": None,
            "idMagazzino": rigatampone['idMagazzino'],
            "magazzino": rigatampone['magazzino'],
            "idArticolo": rigatampone['idArticolo'],
            "codiceArticolo": rigatampone['codiceArticolo'],
            "descrizione": rigatampone['descrizione'],
            "percentualeIva": rigatampone['percentualeIva'],
            "idAliquotaIva": rigatampone['idAliquotaIva'],
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
            "quantita_minima": rigatampone['quantita_minima'],
            "ritenute": rigatampone['ritenute'],
                                }
        if posso("SM"):
            AnagraficaDocumentiEditSuMisuraExt.azzeraRigaPartial(self, numero,
                                                            rigatampone)

    def nuovaRiga(self):
        """ Prepara la UI per l'inserimento di una nuova riga
        """
        self._numRiga = 0
        self.azzeraRiga(0)

        self.articolo_entry.set_text('')
        self.unitaBaseLabel.set_text('')
        self.descrizione_entry.set_text('')
        self.codice_articolo_fornitore_entry.set_text('')
        self.numero_lotto_entry.set_text("")
        self.data_scadenza_datewidget.set_text('')
        self.data_produzione_datewidget.set_text('')
        self.ordine_minimo_entry.set_text('')
        self.tempo_arrivo_merce_entry.set_text('')
        self.data_prezzo_datewidget.set_text('')
        self.id_iva_customcombobox.combobox.set_active(-1)
        self.id_multiplo_customcombobox.combobox.clear()
        self.id_listino_customcombobox.combobox.clear()
        self.prezzo_lordo_entry.set_text('0')
        self.quantita_entry.set_text('1')
        self.prezzo_netto_label.set_text('0')
        self.sconti_widget.clearValues()
        self.totale_riga_label.set_text('0')
        self.giacenza_label.set_text('0')
        self.quantitaMinima_label.set_text('0')
        self.ritenuta_percentuale_entry.set_text('')
        self.rivalsa_percentuale_entry.set_text('')
        self.provvigionale_check.set_active(False)
        if posso("PW"):
            AnagraficaDocumentiEditPromoWearExt.setLabelInfo(self)
        if posso("SM"):
            AnagraficaDocumentiEditSuMisuraExt.setLabels(self)
        if posso("GN"):
            AnagraficaDocumentiEditGestioneNoleggioExt.setLabels(self)
        if self.nolottotemp:
            self.lotto_temp_entry.set_text("")
        if len(self._righe) > 1:
            self.data_documento_entry.set_sensitive(False)
            self.id_operazione_combobox.set_sensitive(False)
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            self.articolo_entry.grab_focus()
        else:
            self.data_documento_entry.set_sensitive(True)
            self.id_persona_giuridica_customcombobox.set_sensitive(
                            self.id_operazione_combobox.get_active() != -1)
            self.id_operazione_combobox.set_sensitive(True)
            if self._anagrafica._magazzinoFissato:
                findComboboxRowFromId(self.id_magazzino_combobox,
                                            self._anagrafica._idMagazzino)
            elif self._id_magazzino is not None:
                findComboboxRowFromId(self.id_magazzino_combobox,
                                                        self._id_magazzino)
            self.id_magazzino_combobox.grab_focus()

        # Finita la manipolazione della riga e pulita l'interfaccia
        # riabilita la conferma automatica su lotto temp
        self.auto_lotto_temp = True

    def nuovaRigaNoClean(self, rigatampone=None):
        """ Prepara per l'inserimento di una nuova riga seza cancellare i campi
        TODO: aggiungere campi fornitura (F6)
        """
        self._numRiga = 0
        self.azzeraRigaPartial(0, rigatampone=rigatampone)
        self.unitaBaseLabel.set_text(rigatampone['unitaBase'])
        self.codice_articolo_fornitore_entry.set_text(
                                    rigatampone['codiceArticoloFornitore'])

    def clearRows(self):
        """Pulisce i campi per il trattamento e la conservazione delle righe
        """
        self._righe = []
        self._righe.append({})
        self._numRiga = 0
        if posso("ADR"):
            self.dati_adr = {}
            AnagraficaDocumentiEditADRExt.setLabels(self)
        self.modelRiga.clear()
        self._iteratorRiga = None
        self.nuovaRiga()

    def refresh_combobox_listini(self):

        if self._righe[0]["idArticolo"] is None:
            self.id_listino_customcombobox.combobox.clear
        else:
            fillComboboxListiniFiltrati(
                        self.id_listino_customcombobox.combobox,
                        self._righe[0]["idArticolo"],
                        self._righe[0]["idMagazzino"],
                        self.id_persona_giuridica_customcombobox.getId())
            if self._id_listino:
                findComboboxRowFromId(self.id_listino_customcombobox.combobox,
                                                            self._id_listino)

    def on_id_multiplo_customcombobox_button_clicked(self, widget, toggleButton):
        """ I multipli di fatto non vengono quasi mai usati ....
        """
        on_id_multiplo_customcombobox_clicked(widget, toggleButton, self._righe[0]["idArticolo"])

    def on_id_multiplo_customcombobox_changed(self, combobox):
        """ FIXME """
        if self._loading:
            return
        self._righe[0]["idMultiplo"] = findIdFromCombobox(self.id_multiplo_customcombobox.combobox)
        #multiplo = leggiMultiplo(self._righe[0]["idMultiplo"])
        multiplo = Multiplo().getRecord(id=self._righe[0]["idMultiplo"])
        if multiplo:
            self._righe[0]["multiplo"] = multiplo.denominazione_breve + ' ( ' + str(multiplo.moltiplicatore) + ' X )'
            self._righe[0]["moltiplicatore"] = multiplo.moltiplicatore
        self.calcolaTotaleRiga()

    def get_variazioni_listino(self, cliente, idListino):
        data = datetime.datetime.now()
        if cliente and cliente.vl is not []:
            return [{'valore':var.valore.strip(), 'tipo':var.tipo} for var in cliente.vl if ((var.id_listino == idListino) and (data > var.data_inizio and data < var.data_fine))]
        else:
            return []

    def getPrezzoVenditaLordo(self, idListino, idArticolo):
        """Cerca il prezzo di vendita
        """
        prezzoLordo = 0
        sconti = []
        applicazione = "scalare"
        if idListino is not None and idArticolo is not None:
            listino = leggiListino(idListino, idArticolo)
            self._righe[0]["listino"] = listino["denominazione"]
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
        cliente = Cliente().getRecord(id=self.id_persona_giuridica_customcombobox.getId()) if not self.dao.id else self.dao.CLI
        self._righe[0]["VL"] = self.get_variazioni_listino(cliente, idListino)

    def _getPrezzoAcquisto(self):
        """ Lettura del prezzo di acquisto netto che serve per i noleggi
        """
        fornitura = leggiFornitura(self._righe[0]["idArticolo"], data=datetime.datetime.now())
        prezzo = fornitura["prezzoNetto"]
        self.prezzo_aquisto_entry.set_text(str(prezzo) or "0")

    def on_sconti_widget_button_toggled(self, button):
        """ Apre il widget SCONTI
        """
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

    def on_notebook_select_page(self, notebook, move_focus=None, page=None, page_num=None):
        """ AL MOMENTO INUTILIZZATA
        """
        return

    def on_notebook_switch_page(self, notebook, page, page_num):
        if page_num == 2:
            self.calcolaTotale()
        elif page_num == 3:
            id_pag = findIdFromCombobox(self.pagamenti_page.id_pagamento_customcombobox.combobox)
            pago = Pagamento().getRecord(id=id_pag)
            if pago:
                self.pagamenti_page.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(pago.denominazione)+'</span></b>')
                if not self.dao.documento_saldato and not self.dao.id:
                    self.pagamenti_page.on_calcola_importi_scadenza_button_clicked(None)
            else:
                self.pagamenti_page.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(_("NESSUNO?"))+'</span></b>')
            if self.dao.documento_saldato:
                self.pagamenti_page.chiudi_pagamento_documento_button.set_sensitive(False)
                self.pagamenti_page.apri_pagamento_documento_button.set_sensitive(True)
            else:
                self.pagamenti_page.chiudi_pagamento_documento_button.set_sensitive(True)
                self.pagamenti_page.apri_pagamento_documento_button.set_sensitive(False)

    def on_rent_checkbutton_toggled(self, checkbutton=None):
        """ check button in schermata documenti relativa al noleggio """
        stato = self.rent_checkbutton.get_active()
        self.noleggio = stato
        if not self.noleggio:
            self.prezzo_aquisto_entry.set_sensitive(False)
            self.coeficente_noleggio_entry.set_sensitive(False)
            self.totale_periodo_label.set_sensitive(False)
            self.giorni_label.set_sensitive(False)
            self.periodo_label.set_sensitive(False)
            self.GG_label.set_sensitive(False)
            self.X_label.set_sensitive(False)
        else:
            self.prezzo_aquisto_entry.set_sensitive(True)
            self.coeficente_noleggio_entry.set_sensitive(True)
            self.totale_periodo_label.set_sensitive(True)
            self.giorni_label.set_sensitive(True)
            self.periodo_label.set_sensitive(True)
            self.GG_label.set_sensitive(True)
            self.X_label.set_sensitive(True)

    def _clear(self):
        self.causale_trasporto_comboboxentry.get_child().set_text('')
        self.destinatario_radiobutton.set_active(True)
        self.id_vettore_customcombobox.set_sensitive(False)
        self.porto_combobox.set_sensitive(False)
        findComboboxRowFromId(self.id_destinazione_merce_customcombobox.combobox, -1)
        self.id_operazione_combobox.set_active(-1)
        self.id_persona_giuridica_customcombobox.set_active(-1)
        #self.id_destinazione_merce_customcombobox.combobox.set_sensitive(False)

    def _refresh(self):
        """ Funzione importantissima di "impianto" del documento nella UI
        """
        self._loading = True

        self.pagamenti_page.clear()
        self._clear()

        self._tipoPersonaGiuridica = None
        self._operazione = None
        self._fonteValore = None
        self._segno = None
        self._variazioneListiniResponse = ''
        self._variazioneListiniShow = True

        self.data_documento_entry.set_sensitive(self.dao.id is None)
        self.edit_date_and_number_button.set_sensitive(self.dao.id is not None)
        self.numero_documento_entry.set_sensitive(False)
        self.parte_spinbutton.set_sensitive(False)
        self.id_operazione_combobox.set_sensitive(self.dao.id is None)
        self._operazione = self.dao.operazione
        findComboboxRowFromId(self.id_operazione_combobox, self.dao.operazione)
        self.on_id_operazione_combobox_changed(self.id_operazione_combobox)
        self.id_persona_giuridica_customcombobox.set_sensitive(self.dao.id is None)
        self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
        if self._tipoPersonaGiuridica == "fornitore":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_fornitore)
            self.id_destinazione_merce_customcombobox.combobox.clear()
            #self.id_destinazione_merce_customcombobox.set_sensitive(False)
        elif self._tipoPersonaGiuridica == "cliente":
            self.id_persona_giuridica_customcombobox.setId(self.dao.id_cliente)
            fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                    self.dao.id_cliente)
            findComboboxRowFromId(self.id_destinazione_merce_customcombobox.combobox,
                    (self.dao.id_destinazione_merce or -1))
            #self.id_destinazione_merce_customcombobox.combobox.set_sensitive(True)

        self.data_documento_entry.set_text(dateToString(self.dao.data_documento))
        self.numero_documento_entry.set_text(str(self.dao.numero or '0'))
        self.parte_spinbutton.set_value(self.dao.parte or 0)
        self.showDatiMovimento()

        if posso("GN"):
            self.start_rent_entry.set_text(dateTimeToString(self.dao.data_inizio_noleggio))
            self.end_rent_entry.set_text(dateTimeToString(self.dao.data_fine_noleggio))
#            self.on_end_rent_entry_focus_out_event()
        findComboboxRowFromId(self.pagamenti_page.id_pagamento_customcombobox.combobox, self.dao.id_pagamento)
        findComboboxRowFromId(self.pagamenti_page.id_banca_customcombobox.combobox, (self.dao.id_banca or -1) )
        findComboboxRowFromId(self.id_aliquota_iva_esenzione_customcombobox.combobox,
                (self.dao.id_aliquota_iva_esenzione or -1))
        self.id_agente_customcombobox.refresh(clear=True, filter=False)
        insertComboboxSearchAgente(self.id_agente_customcombobox,
                                                        self.dao.id_agente)
        self.protocollo_entry1.set_text(self.dao.protocollo or '')
        self.note_pie_pagina_comboboxentry.get_child().set_text(self.dao.note_pie_pagina or '')
        textview_set_text(self.note_interne_textview, self.dao.note_interne or '')
        if not self.dao.id:
            self.dao.causale_trasporto = setconf("Documenti", "causale_vendita") or ''
        self.causale_trasporto_comboboxentry.get_child().set_text(self.dao.causale_trasporto or '')
        self.aspetto_esteriore_beni_comboboxentry.get_child().set_text(self.dao.aspetto_esteriore_beni or '')
        self.inizio_trasporto_entry.set_text(dateTimeToString(self.dao.inizio_trasporto))
        self.fine_trasporto_entry.set_text(dateTimeToString(self.dao.fine_trasporto))
        self.id_vettore_customcombobox.refresh(clear=True, filter=False)
        if not self.dao.id:
           self.dao.incaricato_trasporto = setconf("Documenti","incaricato_predef") or 'destinatario'
        if self.dao.incaricato_trasporto == 'vettore':
            # Se l'incaricato e` un vettore, allora bisogna attivare il campo Porto
            self.vettore_radiobutton.set_active(True)
            insertComboboxSearchVettore(self.id_vettore_customcombobox,
                    self.dao.id_vettore)
            self.porto_combobox.set_sensitive(True)
        if self.dao.porto == 'Franco':
            self.porto_combobox.set_active(1)
        elif self.dao.porto == 'Assegnato':
            self.porto_combobox.set_active(2)
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

        adr = posso('ADR')
        sm = posso('SM')
        gn = posso('GN')
        scarta = False
        j = 0
        for riga in self.dao.righe:
            if adr:
                if "Rif. DDT" in riga.descrizione:
                    scarta = False
                # Scartiamo le righe di riepilogo ADR
                elif "RIEPILOGO" in riga.descrizione:
                    scarta = True
                    continue
                if scarta:
                    continue
            self.azzeraRiga(0)
            j += 1 #self.dao.righe.index(riga) + 1
            magazzino = leggiMagazzino(riga.id_magazzino)
            #magazzino = Magazzino().getRecord(id=riga.id_magazzino)
            articolo = leggiArticolo(riga.id_articolo)
            listino = leggiListino(riga.id_listino)
            multiplo = leggiMultiplo(riga.id_multiplo)
            (sconti, applicazione) = getScontiFromDao(
                    riga.sconti, riga.applicazione_sconti)
            if sm and riga.misura_pezzo:
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
            self._righe[0]["percentualeIva"] = mN(riga.percentuale_iva,0)

            idiva = None
            idiva = riga.id_iva
            self._righe[0]["idAliquotaIva"] = idiva

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
            if adr:
                if riga.id_articolo is not None:
                    artADR = AnagraficaDocumentiEditADRExt.getADRArticolo(riga.id_articolo)
                    if artADR:
                        # Calcola se viene superato il limite massimo di esenzione
                        AnagraficaDocumentiEditADRExt.calcolaLimiteTrasportoADR(self, artADR)
            if sm:
                self._righe[0]["altezza"] = mN(altezza)
                self._righe[0]["larghezza"] = mN(larghezza)
                self._righe[0]["molt_pezzi"] =mN(moltiplicatore_pezzi)
            if gn:
                print " ISRENT  ",riga.isrent
                if riga.isrent :
                    self._righe[0]["arco_temporale"] = self.giorni_label.get_text()
                else:
                    self._righe[0]["arco_temporale"] = "NO"
                self._righe[0]["prezzo_acquisto"] = mN(riga.prezzo_acquisto_noleggio)
                self._righe[0]["divisore_noleggio"] = mN(riga.coeficente_noleggio)
            self.getTotaleRiga()
            if gn and self._righe[0]["arco_temporale"] != "NO" :
                totaleNoleggio = AnagraficaDocumentiEditGestioneNoleggioExt.totaleNoleggio(self)

            self.unitaBaseLabel.set_text(self._righe[0]["unitaBase"])
            if self._tipoPersonaGiuridica == "fornitore":
                fornitura = leggiFornitura(riga.id_articolo, self.dao.id_fornitore, self.dao.data_documento, True)
                self._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"] #or articolo["codicearticolofornitore"]
                self._righe[0]["numeroLottoArticoloFornitura"] = fornitura["numeroLottoArticoloFornitura"]
                self._righe[0]["dataScadenzaArticoloFornitura"] = fornitura["dataScadenzaArticoloFornitura"]
                self._righe[0]["dataProduzioneArticoloFornitura"] = fornitura["dataProduzioneArticoloFornitura"]
                self._righe[0]["dataPrezzoFornitura"] = fornitura["dataPrezzoFornitura"]
                self._righe[0]["ordineMinimoFornitura"] = fornitura["ordineMinimoFornitura"]
                self._righe[0]["tempoArrivoFornitura"] = fornitura["tempoArrivoFornitura"]
            else: # persona giuridica cliente, quindi per la vendita
                if self._righe[0]["idRiga"] and not self._righe[0]["rigaMovimentoFornituraList"]:
                    ids = []
                    rmf = RigaMovimentoFornitura().select(idRigaMovimentoVendita=self._righe[0]["idRiga"], batchSize=None)
                    for r in rmf:
                        ids.append(r.id_fornitura)
                    self._righe[0]["rigaMovimentoFornituraList"] = ids
                else:
                    self._righe[0]["rigaMovimentoFornituraList"] = []
                #TODO: AGGIUNGERE UN RICHIAMO A RIGAMOVIMENTOFORNITURA CON I DATI PRESI DAL DB
                if self.nolottotemp:
                    if riga and hasattr(riga, 'numero_lotto_temp'):
                        self._righe[0]["numeroLottoTemp"] = riga.numero_lotto_temp
            self._righe.append(self._righe[0])
            rigadoc= self._righe[j]

            if sm:
                    altezza=rigadoc["altezza"]
                    larghezza =rigadoc["larghezza"]
                    molt_pezzi = rigadoc["molt_pezzi"]
            else:
                altezza = larghezza= molt_pezzi= ""
            #riempimento della treeview righe
            if gn:
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
                    str(rigadoc["totale"]),
                    ]
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

        self.pagamenti_page.getScadenze()
        self.pagamenti_page.ricalcola_sospeso_e_pagato()

    def setDao(self, dao):
        """ Imposta un nuovo dao Testata documento
        """
        self.variazioni_dati_testata = False
        self.destinatario_radiobutton.set_active(True)
        self.id_vettore_customcombobox.set_sensitive(False)
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = TestataDocumento()
            # Suggerisce la data odierna se stiamo lavorando con l'anno
            # di lavoro corrente, altrimenti lascia vuoto il campo data e
            # mostra un messaggio di avviso.
            if time.strftime("%Y") != Environment.workingYear:
                messageWarning(msg="Inserire la data del documento!")
            else:
                self.dao.data_documento = datetime.datetime.today()
            self._oldDaoRicreato = False #il dao è nuovo il controllo sul nuovo codice è necessario
            try:
                op = setconf("Documenti", "tipo_documento_predefinito")
                if op:
                    self.dao.operazione = op
            except:
                pass
            try:
                cli = setconf("Documenti", "cliente_predefinito")
                if cli:
                    self.dao.id_cliente = int(cli)
                    self.oneshot = True
                    self.articolo_entry.grab_focus()
            except:
                pass
            try:
                forn = setconf("Documenti", "fornitore_predefinito")
                if forn:
                    self.dao.id_fornitore = int(forn)
                    self.oneshot = True
                    self.articolo_entry.grab_focus()
            except:
                pass

        else:
            # Ricrea il Dao prendendolo dal DB
            #self.dao = TestataDocumento().getRecord(id=dao.id)
            self.dao= dao
            self._controllo_data_documento = dateToString(self.dao.data_documento)
            self._controllo_numero_documento = self.dao.numero
            self._controllo_parte_documento  = self.dao.parte
            self.oneshot = False
            self._oldDaoRicreato = True #il dao è nuovo il controllo sul nuovo codice non  è necessario
        self._refresh()
        return self.dao

    def saveDao(self, tipo=None):
        """ Salvataggio del Dao
        """
        print "\n\nINIZIO IL SALVATAGGIO DEL DOCUMENTO\n\n"
        GN = posso("GN")
        SM = posso("SM")
        if posso("ADR") and tipo==GTK_RESPONSE_OK:
            AnagraficaDocumentiEditADRExt.sposta_sommario_in_tabella(self)
        scontiRigaDocumentoList = {}
        if not(len(self._righe) > 1):
            messageInfo(msg=_("TENTATIVO DI SALVATAGGIO DOCUMENTO SENZA RIGHE???"))
            raise Exception, "ATTENZIONE, TENTATIVO DI SALVATAGGIO SENZA RIGHE?????"

        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                    self.data_documento_entry,
                    _('Inserire la data del documento !'))

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.dialogTopLevel,
                    self.id_operazione_combobox,
                    _('Inserire il tipo di documento !'))

        if self.id_persona_giuridica_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel,
                    self.id_persona_giuridica_customcombobox,
                    _('Inserire l\'intestatario del documento !'))

        self.dao.data_documento = stringToDate(self.data_documento_entry.get_text())

        if self.dao.id is not None and self.numero_documento_entry.get_text() != '0':

            #if self.data_documento_entry.get_text() != self._controllo_data_documento\
                        #or str(self.numero_documento_entry.get_text()) != str(self._controllo_numero_documento) \
                        #or str(self.parte_spinbutton.get_value_as_int()) != str(self._controllo_parte_documento):
            if self.variazioni_dati_testata:
                numero = self.numero_documento_entry.get_text()
                parte = self.parte_spinbutton.get_value_as_int()
                if parte == 0:
                    parte = None
                idOperazione = findIdFromCombobox(self.id_operazione_combobox)
                daData, aData = getDateRange(self.data_documento_entry.get_text())
                docs = TestataDocumento().select(numero=numero,
                                                    parte= parte,
                                                    daData=daData, aData=aData,
                                                    idOperazione=idOperazione,
                                                    offset=None,
                                                    batchSize=None)
                if docs:
                    msg = """Attenzione!
    Esiste già un documento numero %s per
    l'anno di esercizio indicato nella data
    del documento.
    Continuare comunque?""" % numero

                    if not YesNoDialog(msg=msg, transient=None):
                        return

                self.dao.numero = numero
                if parte == 0:
                    self.dao.parte = None
                else:
                    self.dao.parte = parte
        self.dao.operazione = self._operazione
        pbar(self.dialog.pbar,parziale=1, totale=4)
        if self._tipoPersonaGiuridica == "fornitore":
            self.dao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_cliente = None
            self.dao.id_destinazione_merce = None
        elif self._tipoPersonaGiuridica == "cliente":
            self.dao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
            self.dao.id_fornitore = None
            self.dao.id_destinazione_merce = findIdFromCombobox(self.id_destinazione_merce_customcombobox.combobox)
        self.dao.id_pagamento = findIdFromCombobox(self.pagamenti_page.id_pagamento_customcombobox.combobox)
        self.dao.id_banca = findIdFromCombobox(self.pagamenti_page.id_banca_customcombobox.combobox)
        self.dao.id_aliquota_iva_esenzione = findIdFromCombobox(self.id_aliquota_iva_esenzione_customcombobox.combobox)
        self.dao.id_agente = self.id_agente_customcombobox._id
        self.dao.protocollo = self.protocollo_entry1.get_text()
        self.dao.causale_trasporto = self.causale_trasporto_comboboxentry.get_child().get_text()[0:30]
        self.dao.aspetto_esteriore_beni = self.aspetto_esteriore_beni_comboboxentry.get_child().get_text()
        self.dao.inizio_trasporto = stringToDateTime(self.inizio_trasporto_entry.get_text())
        self.dao.fine_trasporto = stringToDateTime(self.fine_trasporto_entry.get_text())

        if self.vettore_radiobutton.get_active():
            self.dao.id_vettore = self.id_vettore_customcombobox._id
            self.dao.incaricato_trasporto = 'vettore'
            if self.porto_combobox.get_active() == 1:
                self.dao.porto = 'Franco'
            elif self.porto_combobox.get_active() == 2:
                self.dao.porto = 'Assegnato'
            if not self.dao.id_vettore:
                obligatoryField(self.dialogTopLevel,
                    self.id_vettore_customcombobox,
                    _('Quando si seleziona vettore è obbligatorio settarne uno!'))
        elif self.mittente_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'mittente'
            self.dao.porto = 'Franco'
        elif self.destinatario_radiobutton.get_active():
            self.dao.id_vettore = None
            self.dao.incaricato_trasporto = 'destinatario'
            self.dao.porto = 'Assegnato'
        self.dao.totale_colli = float(self.totale_colli_entry.get_text() or 0)
        self.dao.totale_peso = self.totale_peso_entry.get_text()
        self.dao.note_interne = textview_get_text(self.note_interne_textview)
        self.dao.note_pie_pagina = self.note_pie_pagina_comboboxentry.get_child().get_text()
        self.dao.applicazione_sconti = self.sconti_testata_widget.getApplicazione()
        if GN:
            self.dao.data_inizio_noleggio= self.start_rent_entry.get_text()
            self.dao.data_fine_noleggio = self.end_rent_entry.get_text()
        pbar(self.dialog.pbar,parziale=2, totale=4)

        scontiSuTotale = []
        res = self.sconti_testata_widget.getSconti()
        if res:
            for scrow in res:
                daoScontost = ScontoTestataDocumento()
                daoScontost.valore = scrow["valore"]
                daoScontost.tipo_sconto = scrow["tipo"]
                scontiSuTotale.append(daoScontost)
        self.dao.scontiSuTotale = scontiSuTotale

        scontiRigaDocumento=[]
        righeDocumento = []

        operazione = leggiOperazione(self._operazione)
        if operazione["segno"] != '':
            tipoDOC = "MOV"
        else:
            tipoDOC = "DOC"
        scontiRigaMovimento =[]
        scontiRigaDocumento =[]

        for i in range(1, len(self._righe)):
            pbar(self.dialog.pbar,parziale=3, totale=4)
            if (tipoDOC == "MOV" and self._righe[i]["idArticolo"] == None) or tipoDOC == "DOC":
                daoRiga = RigaDocumento()
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
            else:
                daoRiga = RigaMovimento()
                sconti =[]
                listsco=[]
                if self._righe[i]["sconti"] is not None:
                    for scon in self._righe[i]["sconti"]:
                        daoSconto = ScontoRigaMovimento()
                        daoSconto.valore = scon["valore"]
                        daoSconto.tipo_sconto = scon["tipo"]
                        scontiRigaMovimento.append(daoSconto)
                    #scontiRigaDocumento[daoRiga] = sconti
                    daoRiga.scontiRigheMovimento = scontiRigaMovimento
                    scontiRigaMovimento =[]
            #daoRiga.id_testata_documento = self.dao.id
            daoRiga.id_articolo = self._righe[i]["idArticolo"]
            daoRiga.id_magazzino = self._righe[i]["idMagazzino"]
            daoRiga.descrizione = self._righe[i]["descrizione"]
            daoRiga.codiceArticoloFornitore = self._righe[i]["codiceArticoloFornitore"]
            #aggancio degli attributi all'oggetto riga per portarli in salvataggio
            # alla fornitura...
            setattr(daoRiga,"numero_lotto", self._righe[i]["numeroLottoArticoloFornitura"])
            setattr(daoRiga,"data_scadenza", self._righe[i]["dataScadenzaArticoloFornitura"])
            setattr(daoRiga,"data_produzione", self._righe[i]["dataProduzioneArticoloFornitura"])
            setattr(daoRiga,"data_prezzo", self._righe[i]["dataPrezzoFornitura"])
            setattr(daoRiga,"ordine_minimo", self._righe[i]["ordineMinimoFornitura"])
            setattr(daoRiga,"tempo_arrivo", self._righe[i]["tempoArrivoFornitura"])
            if self.nolottotemp:
                setattr(daoRiga,"lotto_temp",self._righe[i]["numeroLottoTemp"])
            if "rigaMovimentoFornituraList" in self._righe[i]:
                setattr(daoRiga,"righe_movimento_fornitura",self._righe[i]["rigaMovimentoFornituraList"])
            daoRiga.posizione = i
            daoRiga.id_listino = self._righe[i]["idListino"]
            daoRiga.percentuale_iva = self._righe[i]["percentualeIva"]
            daoRiga.id_iva = self._righe[i]["idAliquotaIva"]
            daoRiga.applicazione_sconti = self._righe[i]["applicazioneSconti"]
            daoRiga.quantita = self._righe[i]["quantita"]
            daoRiga.id_multiplo = self._righe[i]["idMultiplo"]
            daoRiga.moltiplicatore = self._righe[i]["moltiplicatore"]
            daoRiga.valore_unitario_lordo = self._righe[i]["prezzoLordo"]
            daoRiga.valore_unitario_netto = self._righe[i]["prezzoNetto"]
#            pbar(self.dialog.pbar,pulse=True)
            if GN:
                daoRiga.prezzo_acquisto_noleggio = self._righe[i]["prezzo_acquisto"]
                daoRiga.coeficente_noleggio = self._righe[i]["divisore_noleggio"]
                if self._righe[i]["arco_temporale"] != "NO":
                    daoRiga.isrent =  "True"
                else:
                    daoRiga.isrent = "False"

            misure = []
            if SM and self._righe[i]["altezza"] != '' and \
                            self._righe[i]["larghezza"] != '':
                daoMisura = MisuraPezzo()
                daoMisura.altezza = float(self._righe[i]["altezza"] or 0)
                daoMisura.larghezza = float(self._righe[i]["larghezza"] or 0)
                daoMisura.moltiplicatore = float(self._righe[i]["molt_pezzi"] or 0)
                daoRiga.misura_pezzo = [daoMisura]
            #righe[i]=daoRiga
            ### Sezion dedicata alla gestione della ritenuta d'acconto
            ### della rivalsa e dela inarcassa
            #"ritAccPercentuale": 0, "rivalsaPercentuale": 0,
            #"ritCaProvvigionale": False, "ritInarCassa":0
            if self._righe[i]["ritenute"]:
                daoRiteAcc = RigaRitenutaAcconto()
                daoRiteAcc.provvigionale = self._righe[i]["ritenute"]["ritCaProvvigionale"]
                daoRiteAcc.ritenuta_percentuale = float(self._righe[i]["ritenute"]["ritAccPercentuale"] or 0)
                daoRiteAcc.rivalsa_percentuale = float(self._righe[i]["ritenute"]["rivalsaPercentuale"] or 0)
                daoRiteAcc.inarcassa_percentuale = float(self._righe[i]["ritenute"]["ritInarCassa"] or 0)
                daoRiga.ritenute = daoRiteAcc
            righeDocumento.append(daoRiga)
        self.dao.righeDocumento = righeDocumento
        self.pagamenti_page.saveScadenze()

        #porto in persist tre dizionari: uno per gli sconti sul totale, l'altro per gli sconti sulle righe e le righe stesse
        self.dao.persist()
        pbar(self.dialog.pbar,parziale=4, totale=4)
        self.label_numero_righe.hide()
        text = str(len(self.dao.righe))
        self.label_numero_righe.set_text(text)
        self.label_numero_righe.show()
        pbar(self.dialog.pbar, stop=True)
        print " \nFINE DEL SALVATAGGIO DEL DOCUMENTO\n\n"

    def on_importo_da_ripartire_entry_changed(self, entry):
        """Fesseria voluta da un cliente ....alla fine non serviva
        """
        return
        self.dao.removeDividedCost()
#        self.dao.ripartire_importo = False
#        self.ripartire_importo_checkbutton.set_active(self.dao.ripartire_importo)
        self.dao.costo_da_ripartire = Decimal(self.importo_da_ripartire_entry.get_text())

        self.importo_sovrapprezzo_label.set_text(str((mN(self.dao.costo_da_ripartire) or 0)/self.dao.totalConfections))

    def on_righe_treeview_drag_begin(self, treeview, drag_context):
        """ starting dragging func, just give the row start to drag """
        model, iter_to_copy = treeview.get_selection().get_selected()
        self.riga_partenza =  model.get_path(iter_to_copy)

    def on_righe_treeview_drag_leave(self, treeview, drag_context, timestamp):
        """ Questa è la funzione di "scarico" del drop, abbiamo la riga di
        destinazione con la funzione get_drag_dest_row() e prendiamo
        la riga di partenza con la funzione precedente
        """
        if not treeview:
            return
        duplicarighe= []
        try:
            row, pos = treeview.get_drag_dest_row()
        except:
            return
        if self.riga_partenza != row[0]:
            duplicarighe = self._righe[:]
            if self.riga_partenza[0] > row[0]:
                self._righe.insert(row[0]+1,duplicarighe[self.riga_partenza[0]+1])
                self._righe.pop(self.riga_partenza[0]+2)
            elif self.riga_partenza[0] < row[0]:
                self._righe.insert(row[0]+2,duplicarighe[self.riga_partenza[0]+1])
                self._righe.pop(self.riga_partenza[0]+1)
            duplicarighe= []

    def on_righe_treeview_row_activated(self, treeview, path, column):
        """ Riporta la riga selezionata in primo piano per la modifica
        """
        # Disabilita la conferma automatica su lotto temp
        self.auto_lotto_temp = False

        sel = treeview.get_selection()
        (model, self._iteratorRiga) = sel.get_selected()
        (selRow, ) = path
        self._numRiga = selRow + 1
        self.azzeraRiga(0)
        self._loading = True
        self._righe[0] = self._righe[self._numRiga]
        self.last_qta = self._righe[self._numRiga]["quantita"]
        self.giacenza_label.set_text(str(giacenzaArticolo(year=Environment.workingYear,
                                                idMagazzino=self._righe[0]["idMagazzino"],
                                                idArticolo=self._righe[0]["idArticolo"])[0]))
        findComboboxRowFromId(self.id_magazzino_combobox, self._righe[0]["idMagazzino"])
        fillComboboxMultipli(self.id_multiplo_customcombobox.combobox, self._righe[0]["idArticolo"], True)
        findComboboxRowFromId(self.id_multiplo_customcombobox.combobox, self._righe[0]["idMultiplo"])
        self.refresh_combobox_listini()
        findComboboxRowFromId(self.id_listino_customcombobox.combobox, self._righe[0]["idListino"])
        self.articolo_entry.set_text(self._righe[0]["codiceArticolo"])
        self.descrizione_entry.set_text(self._righe[0]["descrizione"])
        self.codice_articolo_fornitore_entry.set_text(self._righe[0]["codiceArticoloFornitore"])
        findComboboxRowFromId(self.id_iva_customcombobox.combobox, self._righe[0]["idAliquotaIva"])
#        self.percentuale_iva_entry.set_text(str(self._righe[0]["percentualeIva"]).strip())

        self.numero_lotto_entry.set_text(self._righe[0]["numeroLottoArticoloFornitura"] or "")
        self.lotto_temp_entry.set_text(self._righe[0]["numeroLottoTemp"] or "")
        self.data_scadenza_datewidget.set_text(self._righe[0]["dataScadenzaArticoloFornitura"] or "")
        self.data_produzione_datewidget.set_text(self._righe[0]["dataProduzioneArticoloFornitura"] or "")
        self.data_prezzo_datewidget.set_text(self._righe[0]["dataPrezzoFornitura"] or "")
        self.ordine_minimo_entry.set_text(str(self._righe[0]["ordineMinimoFornitura"] or ""))
        self.tempo_arrivo_merce_entry.set_text(str(self._righe[0]["tempoArrivoFornitura"] or ""))

        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)
        self.quantita_entry.set_text(str(self._righe[0]["quantita"]))
        try:
            self.quantitaMinima_label.set_text(str(Articolo().getRecord(id=self._righe[0]["idArticolo"]).quantita_minima))
        except:
            print "QUANTITA MINIMA NON PRESENTE"
        self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))
        self.prezzo_netto_label.set_text(str(self._righe[0]["prezzoNetto"]))
        self.totale_riga_label.set_text(str(self._righe[0]["totale"]))
        if posso("SM"):
            self.altezza_entry.set_text(str(self._righe[0]["altezza"]))
            self.larghezza_entry.set_text(str(self._righe[0]["larghezza"]))
            self.moltiplicatore_entry.set_text(str(self._righe[0]["molt_pezzi"]))
        if posso("GN") and self.noleggio:
            self.coeficente_noleggio_entry.set_text(str(self._righe[0]["divisore_noleggio"]))
            self.prezzo_aquisto_entry.set_text(str(self._righe[0]["prezzo_acquisto"]))
            #self._righe[0]["totale"] = self._righe[self._numRiga]["totale_periodo"]
            self.on_show_totali_riga()
            self._getPrezzoAcquisto()

        self._loading = False
        self.articolo_entry.grab_focus()


    def on_confirm_row_button_clicked(self, widget=None,row=None):
        """
        Memorizza la riga inserita o modificata
        """
        self.checkMAGAZZINO = False
        inserisci = False
        if self.NoRowUsableArticle:
            messageInfo(_('ARTICOLO NON USABILE IN UNA RIGA IN QUANTO ARTICOLO PRINCIPALE O PADRE!'))
            return

        self._righe[0]["idMagazzino"] = findIdFromCombobox(self.id_magazzino_combobox)
        magazzino = leggiMagazzino(self._righe[0]["idMagazzino"])
        self._righe[0]["magazzino"] = magazzino['denominazione']

        if (self.data_documento_entry.get_text() == ''):
            messageInfo(_('Inserire la data del documento !'))
            return

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            messageInfo(_('Inserire il tipo di documento !'))
            return

        if (self.id_persona_giuridica_customcombobox.getId() is None):
            messageInfo(_('Inserire l\'intestatario del documento !'))
            return

        if ((self._righe[0]["idMagazzino"] is not None) and
                (self._righe[0]["idArticolo"] is None)):
            messageInfo(_('Inserire l\'articolo !'))
            return

        if ((self._righe[0]["idArticolo"] is not None) and
                (self._righe[0]["idMagazzino"] is None)):
            messageInfo(_('Inserire il magazzino !'))
            return
        self.on_show_totali_riga()
        costoVariato = (self._tipoPersonaGiuridica == "fornitore" and self._righe[0]["idArticolo"] is not None and
                (self._righe[0]["prezzoNetto"] != self._righe[0]["prezzoNettoUltimo"]) and
                (self._segno is not None and self._segno != ''))
        self._righe[0]["numeroLottoTemp"] = self.lotto_temp_entry.get_text()
        if setconf("Documenti", "add_quantita") and not inserisci:
            for r in self._righe[1:]:
                if self._righe[0]["idArticolo"] == r["idArticolo"] and \
                        self._righe[0]["prezzoNetto"] == r["prezzoNetto"] and\
                        self._righe[0]["numeroLottoTemp"] == r["numeroLottoTemp"] and \
                        self._righe[0]["descrizione"] == r["descrizione"] and self._numRiga == 0:
                    r["quantita"] +=self._righe[0]["quantita"]
                    self.modelRiga[self._righe.index(r)-1][11]=str(r["quantita"])
                    self.nuovaRiga()
                    return
        if self._numRiga == 0:
            self._numRiga = len(self._righe)
            self._righe.append(self._righe[0])
            inserisci = True
        else:
            inserisci = False
        # memorizzazione delle parti descrittive (liberamente modificabili)
        self._righe[0]["descrizione"] = self.descrizione_entry.get_text()

        if self.ritenuta_percentuale_entry.get_text():
            self._righe[0]["ritAccPercentuale"] = self.ritenuta_percentuale_entry.get_text()
            print "RIGA CON RITENUTA"
        if self.rivalsa_percentuale_entry.get_text():
            self._righe[0]["rivalsaPercentuale"] = self.rivalsa_percentuale_entry.get_text()
            print "RIGA CON RIVALSA"
        if self.inarcassa_entry.get_text():
            self._righe[0]["ritInarCassa"] = self.inarcassa_entry.get_text()
            print "INARCASSA"
        if self.provvigionale_check.get_active():
            self._righe[0]["ritCaProvvigionale"] = self.provvigionale_check.get_active()
            print "E' di tipo provvigionale"


        if posso("ADR"):
            if self._righe[0]["idArticolo"] is not None:
                artADR = AnagraficaDocumentiEditADRExt.getADRArticolo(self._righe[0]["idArticolo"])
                if artADR:
                    if inserisci:
                        AnagraficaDocumentiEditADRExt.calcolaLimiteTrasportoADR(self, artADR)
                    else:
                        AnagraficaDocumentiEditADRExt.calcolaLimiteTrasportoADR(self, artADR, azione='agg', qta=self.last_qta)

        self._righe[0]["codiceArticoloFornitore"] = self.codice_articolo_fornitore_entry.get_text()
        self._righe[0]["numeroLottoArticoloFornitura"] = self.numero_lotto_entry.get_text()
        self._righe[0]["dataScadenzaArticoloFornitura"] = self.data_scadenza_datewidget.get_text()
        self._righe[0]["dataProduzioneArticoloFornitura"] = self.data_produzione_datewidget.get_text()
        self._righe[0]["dataPrezzoFornitura"] = self.data_prezzo_datewidget.get_text()
        self._righe[0]["ordineMinimoFornitura"] = self.ordine_minimo_entry.get_text()
        self._righe[0]["tempoArrivoFornitura"] = self.tempo_arrivo_merce_entry.get_text()


        totale = self._righe[0]["totale"]
        # CONTROLLI DI Gestione NOLEGGIO
        if posso("GN") and self.noleggio:
            self._righe[0]["divisore_noleggio"] = self.coeficente_noleggio_entry.get_text()
            self._righe[0]["arco_temporale"] = self.giorni_label.get_text()
            self._righe[0]["totale_periodo"] = self.totale_periodo_label.get_text()
            totale = AnagraficaDocumentiEditGestioneNoleggioExt.totaleNoleggio(self)
        if posso("SM"):
            self._righe[0]["altezza"] = self.altezza_entry.get_text()
            self._righe[0]["larghezza"] = self.larghezza_entry.get_text()
            self._righe[0]["molt_pezzi"] = self.moltiplicatore_entry.get_text()
        self._righe[self._numRiga] = self._righe[0]
        if posso("GN") and self.noleggio:
            if not "prezzo_acquisto" in self._righe[0]:
                messageInfo(msg=_("ATTENZIONE!!, SEMBRA UN NOLEGGIO MA MANCA PREZZO ACQUISTO.\n RICONTROLLARE RIGA"))
            arco_temporale = self._righe[self._numRiga]["arco_temporale"]
        else:
            arco_temporale="NO"
        if posso("SM"):
            altezza =self._righe[self._numRiga]["altezza"]
            larghezza=self._righe[self._numRiga]["larghezza"]
            molt_pezzi=self._righe[self._numRiga]["molt_pezzi"]
        else:
            altezza= larghezza= molt_pezzi= ""
        # inserisci è true quando si sta editando la riga selezionata
        if inserisci is False:
            if self._iteratorRiga is None:
                return
            #self.modelRiga.set_value(self._iteratorRiga, 0, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 1, self._righe[self._numRiga]["magazzino"])
            self.modelRiga.set_value(self._iteratorRiga, 2, self._righe[self._numRiga]["codiceArticolo"])
            self.modelRiga.set_value(self._iteratorRiga, 3, self._righe[self._numRiga]["descrizione"])
            self.modelRiga.set_value(self._iteratorRiga, 4, str(self._righe[self._numRiga]["percentualeIva"]))
            if posso("SM"):
                self.modelRiga.set_value(self._iteratorRiga, 5, str(altezza))
                self.modelRiga.set_value(self._iteratorRiga, 6, str(larghezza))
                self.modelRiga.set_value(self._iteratorRiga, 7, str(molt_pezzi))
            self.modelRiga.set_value(self._iteratorRiga, 8, str(self._righe[self._numRiga]["multiplo"]))
            self.modelRiga.set_value(self._iteratorRiga, 9, str(self._righe[self._numRiga]["listino"]))
            self.modelRiga.set_value(self._iteratorRiga, 10, str(self._righe[self._numRiga]["unitaBase"]))
            self.modelRiga.set_value(self._iteratorRiga, 11, str(self._righe[self._numRiga]["quantita"]))
            self.modelRiga.set_value(self._iteratorRiga, 12, str(self._righe[self._numRiga]["prezzoLordo"]))
            self.modelRiga.set_value(self._iteratorRiga, 13, self._righe[self._numRiga]["applicazioneSconti"] + (
                ' ' + getStringaSconti(self._righe[self._numRiga]["sconti"])))
            self.modelRiga.set_value(self._iteratorRiga, 14, str(self._righe[self._numRiga]["prezzoNetto"]))

            if posso("GN") and self.noleggio:
                self.modelRiga.set_value(self._iteratorRiga, 15, str(arco_temporale))

            self.modelRiga.set_value(self._iteratorRiga, 16, str(totale))
        else:
            self.modelRiga.append([int(self._numRiga),
                            self._righe[self._numRiga]["magazzino"],
                            self._righe[self._numRiga]["codiceArticolo"],
                            self._righe[self._numRiga]["descrizione"],
                            str(self._righe[self._numRiga]["percentualeIva"]),
                            str(altezza),
                            str(larghezza),
                            str(molt_pezzi),
                            self._righe[self._numRiga]["multiplo"],
                            self._righe[self._numRiga]["listino"],
                            self._righe[self._numRiga]["unitaBase"],
                            str(self._righe[self._numRiga]["quantita"]),
                            str(self._righe[self._numRiga]["prezzoLordo"]),
                            str(self._righe[self._numRiga]["applicazioneSconti"]) + ' ' + str(getStringaSconti(
                            self._righe[self._numRiga]["sconti"])),
                            str(self._righe[self._numRiga]["prezzoNetto"]),
                            str(arco_temporale),
                            str(totale)])
        self.righe_treeview.set_model(self.modelRiga)
        self.righe_treeview.scroll_to_cell(str(len(self.modelRiga)-1))
        self.calcolaTotale()
        if costoVariato:
            if not(self._variazioneListiniResponse == 'all' or self._variazioneListiniResponse == 'none'):
                msg = _('Il prezzo di acquisto e\' stato variato:\n\n   si desidera aggiornare i listini di vendita ?')
                response = showComplexQuestion(self.dialogTopLevel, msg)
                if response == GTK_RESPONSE_YES:
                    self._variazioneListiniResponse = 'yes'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = True
                elif response == GTK_RESPONSE_NO:
                    self._variazioneListiniResponse = 'no'
                    #la richiesta verra' riproposta per la successiva variante o articolo
                    self._variazioneListiniShow = False
                elif response == GTK_RESPONSE_APPLY:
                    self._variazioneListiniResponse = 'all'
                    #la richiesta non verra' riproposta per la successiva variante o articolo
                    #ma per il prossimo articolo padre si'
                    self._variazioneListiniShow = True
                elif response == GTK_RESPONSE_REJECT:
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
        # assegna il valore della casella di testo alla variabile
        stringa = text.get_text()
        if self.mattu:
            text.set_text(stringa.split(self.sepric)[0]) #lasciamo il codice articolo nella entry

        self.ricerca_art_listore.clear()
        art = []
        # evita la ricerca per stringhe vuote o più corte di due caratteri
        if self.ricerca == "codice_a_barre" and setconf("Documenti", "no_ricerca_incrementale"):
            return
        if stringa ==[] or len(stringa)<2:
            return
        if self.ricerca == "codice":
            if len(text.get_text()) <3:
                art = Articolo().select(codice=stringa,cancellato=True, batchSize=20)
            else:
                art = Articolo().select(codice=stringa,cancellato=True, batchSize=50)
        elif self.ricerca == "descrizione":
            if len(text.get_text()) <3:
                art = Articolo().select(denominazione=stringa,cancellato=True, batchSize=20)
            else:
                art = Articolo().select(denominazione=stringa,cancellato=True, batchSize=50)
        elif self.ricerca == "codice_a_barre":
            if len(text.get_text()) <7:
                art = Articolo().select(codiceABarre=stringa,cancellato=True, batchSize=10)
            else:
                art = Articolo().select(codiceABarre=stringa,cancellato=True, batchSize=40)
        elif self.ricerca == "codice_articolo_fornitore_button":
            if len(text.get_text()) <3:
                art = Articolo().select(codiceArticoloFornitore=stringa,cancellato=True, batchSize=10)
            else:
                art = Articolo().select(codiceArticoloFornitore=stringa,cancellato=True, batchSize=40)
        for m in art:
            codice_art = m.codice
            den = m.denominazione
            bloccoInformazioni = codice_art+self.sepric+den
            compl_string = bloccoInformazioni
            if self.ricerca == "codice_articolo_fornitore":
                caf = m.codice_articolo_fornitore
                compl_string = bloccoInformazioni+self.sepric+caf
            if self.ricerca == "codice_a_barre":
                cb = m.codice_a_barre
                compl_string = bloccoInformazioni+self.sepric+cb
            self.ricerca_art_listore.append([compl_string,m])
        #self.completion.set_model(model)

    def match_func(self, completion, key, iter, user_data=None):
        model = self.completion.get_model()
        self.mattu = False
        self.articolo_matchato = None
        if model[iter][0] and self.articolo_entry.get_text().lower() in model[iter][0].lower():
            return model[iter][0]
        else:
            return None

    def on_completion_match(self, completion=None, model=None, iter=None):
        #print "QUANTO CHIAMI QUESTA FUNZ", model[iter][1]
        self.mattu = True
        self.articolo_matchato = model[iter][1]
        self.articolo_entry.set_position(-1)


    def on_ricerca_criterio_combobox_changed(self, combobox):
        if combobox.get_active() ==0:
            self.ricerca = "codice"
        elif combobox.get_active() ==1:
            self.ricerca = "codice_a_barre"
        elif combobox.get_active() ==2:
            self.ricerca = "descrizione"
        elif combobox.get_active() == 3:
            self.ricerca = "codice_articolo_fornitore"


    def ricercaArticolo(self):
        def on_ricerca_articolo_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            self.mostraArticolo(anag.dao.id)

        if (self.data_documento_entry.get_text() == ''):
            messageInfo(_('Inserire la data del documento !'))
            return

        if findIdFromCombobox(self.id_operazione_combobox) is None:
            messageInfo(_('Inserire il tipo di documento !'))
            return

        if (findIdFromCombobox(self.id_magazzino_combobox) is None):
            messageInfo(_('Inserire il magazzino !'))
            return

        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None
        join = None
        orderBy = None
        if self.ricerca_criterio_combobox.get_active() == 0:
            codice = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".articolo.codice"
                batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 1:
            codiceABarre = self.articolo_entry.get_text()
            join= Articolo.cod_barre
            if Environment.tipo_eng =="sqlite":
                orderBy = "codice_a_barre_articolo.codice"
            else:
                orderBy = Environment.params["schema"]+".codice_a_barre_articolo.codice"
            batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 2:
            denominazione = self.articolo_entry.get_text()
            if Environment.tipo_eng =="sqlite":
                orderBy = "articolo.denominazione"
            else:
                orderBy = Environment.params["schema"]+".articolo.denominazione"
            batchSize = setconf("Numbers", "batch_size")
        elif self.ricerca_criterio_combobox.get_active() == 3:
            codiceArticoloFornitore = self.articolo_entry.get_text()
            join= Articolo.fornitur
            if Environment.tipo_eng =="sqlite":
                orderBy = "fornitura.codice_articolo_fornitore"
            else:
                orderBy = Environment.params["schema"]+".fornitura.codice_articolo_fornitore"
        batchSize = setconf("Numbers", "batch_size")
        quantita = 1
        if self.articolo_matchato:
            arts = [self.articolo_matchato]
        else:
            arts = Articolo().select(codiceEM=prepareFilterString(codice),
                                        orderBy=orderBy,
                                        join = join,
                                        denominazione=prepareFilterString(denominazione),
                                        codiceABarre = prepareFilterString(codiceABarre),
                                        codiceArticoloFornitore=prepareFilterString(codiceArticoloFornitore),
                                        idFamiglia=None,
                                        idCategoria=None,
                                        idStato=None,
                                        offset=None,
                                        batchSize=None)
        if not arts and self.ricerca_criterio_combobox.get_active() == 1:
            #print " PROVIAMO LA CARTA DEL PESO VARIABILE A SEI CIFRE",prepareFilterString(codiceABarre[0:6])
            arts = Articolo().select(
                                     codiceABarreEM = prepareFilterString(codiceABarre[0:6]),
                                     offset=None,
                                     batchSize=None)
            if arts: #1234560013189
                quan = codiceABarre[7:-1]
                quantita = list(quan)
                quantita.insert(-3,".")
                quantita =  str(Decimal(",".join(quantita).replace(",","").strip('[]')))
        if (len(arts) == 1):
            self.mostraArticolo(arts[0].id, quan=quantita)
            self.articolo_matchato = None
        else:
            from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
            anag = RicercaComplessaArticoli(denominazione=denominazione,
                                            codice=codice,
                                            codiceABarre=codiceABarre,
                                            codiceArticoloFornitore=codiceArticoloFornitore)
            anag.setTreeViewSelectionType(GTK_SELECTIONMODE_SINGLE)

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
            #anagWindow = manag.getTopLevel()
            #anagWindow.set_transient_for(self.dialogTopLevel)
        else:
            if self.tagliaColoreRigheList:
                for var in self.tagliaColoreRigheList:
                    self.mostraArticolo(var['id'],art=var)
            self.tagliaColoreRigheList = None
            self.promowear_manager_taglia_colore_togglebutton.set_sensitive(False)

    def mostraArticolo(self, id, art=None, quan=None):
        mostraArticoloPart(self, id, art=art, quan=quan)

    def apriAnagraficaArticoliEdit(self, idArticolo):
        from promogest.ui.anagArti.AnagraficaArticoli import AnagraficaArticoli
        from promogest.dao.Articolo import Articolo
        a = AnagraficaArticoli()
        art = Articolo().getRecord(id=idArticolo)
        a.on_record_edit_activate(a, dao=art)

    def on_edit_articolo_button_clicked(self, button):
        idArticolo = self._righe[0]["idArticolo"]
        self.apriAnagraficaArticoliEdit(idArticolo)

    def on_show_totali_riga(self, widget = None, event = None):
        """ calcola il prezzo netto """
        self._righe[0]["quantita"] = Decimal(self.quantita_entry.get_text().strip() or 0)
        self._righe[0]["prezzoLordo"] = Decimal(self.prezzo_lordo_entry.get_text().strip() or 0)
        iva = findStrFromCombobox(self.id_iva_customcombobox.combobox,0)
        if iva and type(iva) != type("CIAO"):
            self._righe[0]["percentualeIva"] = mN(iva.percentuale,0) or 0
            self._righe[0]["idAliquotaIva"] = iva.id or None
        else:
            self._righe[0]["percentualeIva"] =  0
            self._righe[0]["idAliquotaIva"] = None

        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        self._righe[0]["prezzoNetto"] = Decimal(self._righe[0]["prezzoLordo"]) or 0
        self._righe[0]["sconti"] = self.sconti_widget.getSconti()
        self._righe[0]["applicazioneSconti"] = self.sconti_widget.getApplicazione()
        if posso("GN") and self.noleggio:
            # Setti le label "indirette" come prezzoLordo dreivato dalla divisione
            if self.giorni_label.get_text() != "NO":
                giorni_lab = self.giorni_label.get_text()
                self._righe[0]["arco_temporale"] = float(giorni_lab or 1)
                self._righe[0]["divisore_noleggio"] = float(self.coeficente_noleggio_entry.get_text() or 0)
                self._righe[0]["prezzo_acquisto"] = float(self.prezzo_aquisto_entry.get_text() or 0)
                if self._righe[0]["prezzo_acquisto"] > 0 and self._righe[0]["divisore_noleggio"]  > 0 :
                    self._righe[0]["prezzoLordo"] = mN(self._righe[0]["prezzo_acquisto"] / self._righe[0]["divisore_noleggio"],3)
                    self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))

        self.getPrezzoNetto()
        self.prezzo_netto_label.set_text(str(self._righe[0]["prezzoNetto"]))

        self.calcolaTotaleRiga()
        return False

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
        if posso("GN") and self.noleggio:
            totaleNoleggio = AnagraficaDocumentiEditGestioneNoleggioExt.totaleNoleggio(self)


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
        self.pagamenti_page.ricalcola_sospeso_e_pagato()

    def on_edit_date_and_number_button_clicked(self, toggleButton):
        """ This permit to change the date of the document """
        msg = _('Attenzione! Si sta per variare i riferimenti primari del documento.\n Continuare ?')
        if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
            self.data_documento_entry.set_sensitive(True)
            self.numero_documento_entry.set_sensitive(True)
            self.parte_spinbutton.set_sensitive(True)
            self.data_documento_entry.grab_focus()
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            self.variazioni_dati_testata = True

    def showDatiMovimento(self):
        """ Show movimento related informations
        """
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
            if posso("ADR"):
                if self._righe[self._numRiga]["idArticolo"] is not None:
                    artADR = AnagraficaDocumentiEditADRExt.getADRArticolo(self._righe[self._numRiga]["idArticolo"])
                    if artADR:
                        # Calcola se viene superato il limite massimo di esenzione
                        AnagraficaDocumentiEditADRExt.calcolaLimiteTrasportoADR(self, artADR, azione='rm')
            #self.deleted_rows.append(self._righe[self._numRiga][0])
            del(self._righe[self._numRiga])
            self.modelRiga.remove(self._iteratorRiga)

        self.calcolaTotale()
        self.nuovaRiga()

    def on_articolo_entry_key_press_event(self, widget, event):
        """ """
        keyname = gdk_keyval_name(event.keyval)
        if self.ricerca == "codice_a_barre" \
                and setconf("Documenti", "no_ricerca_incrementale") \
                and (keyname == 'F3' \
                or keyname == 'KP_Enter' \
                or keyname == 'Return'):
            self.ricercaArticolo()
        if self.mattu and (keyname == 'Return' or keyname == 'KP_Enter'):
            self.ricercaArticolo()
        if keyname == 'F3' or keyname == 'KP_Enter':
            self.ricercaArticolo()

    def on_search_row_button_clicked(self, widget):
        self.ricercaArticolo()

    def on_storico_costi_button_clicked(self, toggleButton):
        """ """
        from promogest.ui.StoricoForniture import StoricoForniture
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
        from promogest.ui.StoricoListini import StoricoListini
        idArticolo = self._righe[0]["idArticolo"]
        anag = StoricoListini(idArticolo)
        anagWindow = anag.getTopLevel()
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()

    def on_variazione_listini_button_clicked(self, toggleButton):
        """ """
        if self._righe[0]["idArticolo"] is None:
            messageInfo(_('Selezionare un articolo !'))
            return

        from promogest.ui.VariazioneListini import VariazioneListini
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
        """ gestione multilinea in utils
        TODO: il multilinea è da rifare assolutamente
        """
        on_multi_line_button_clickedPart(self, widget)

    def on_id_operazione_combobox_changed(self, combobox):
        """ Funzione di gestione cambiamento combo operazione
        """
        self._operazione = findIdFromCombobox(self.id_operazione_combobox)
        if not self._operazione:
            return
        cache = CachedDaosDict()
        operazioneDao = cache['operazione'][self._operazione]
        if operazioneDao:
            if self._tipoPersonaGiuridica != operazioneDao.tipo_persona_giuridica:
                self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=False)
            self._tipoPersonaGiuridica = operazioneDao.tipo_persona_giuridica
            self._fonteValore = operazioneDao.fonte_valore
            self._segno = operazioneDao.segno

        if (self._tipoPersonaGiuridica == "fornitore"):
            self.persona_giuridica_label.set_text('Fornitore')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            if Environment.azienda == "daog" and "dirett" in operazioneDao.denominazione:
                self.id_persona_giuridica_diretta_customcombobox.setType("cliente")
                self.id_persona_giuridica_diretta_customcombobox.set_sensitive(True)
                self.persona_giuridica_diretta_label.set_text("Cli")
            else:
                self.id_persona_giuridica_diretta_customcombobox.set_sensitive(False)


            self.label_listino.set_property('visible', False)
            self.id_listino_customcombobox.set_property('visible', False)
            self.prz_lordo_label.set_text('Costo')
            self.prz_netto_label.set_text('Costo netto')
            self.codice_articolo_fornitore_label.set_property('visible', True)
            self.codice_articolo_fornitore_entry.set_property('visible', True)
            self.numero_lotto_label.set_property('visible', True)
            self.numero_lotto_entry.set_property('visible', True)
            self.lotto_temp_label.set_property('visible', False)
            self.lotto_temp_entry.set_property('visible', False)
            self.data_prezzo_label.set_property('visible', True)
            self.data_prezzo_datewidget.set_property('visible', True)
            self.data_scadenza_label.set_property('visible', True)
            self.data_scadenza_datewidget.set_property('visible', True)
            self.data_produzione_label.set_property('visible', True)
            self.data_produzione_datewidget.set_property('visible', True)
            self.ordine_minimo_label.set_property('visible', True)
            self.ordine_minimo_entry.set_property('visible', True)
            self.tempo_arrivo_merce_label.set_property('visible', True)
            self.tempo_arrivo_merce_entry.set_property('visible', True)
            self.dettaglio_giacenza_togglebutton.set_property("visible", False)
            self.protocollo_label.set_property('visible', True)
            self.protocollo_entry1.set_property('visible', True)
            self.numero_documento_label.set_text('N. reg.')

        elif (self._tipoPersonaGiuridica == "cliente"):
            self.persona_giuridica_label.set_text('Cliente')
            self.id_persona_giuridica_customcombobox.setType(self._tipoPersonaGiuridica)
            self.id_persona_giuridica_customcombobox.set_sensitive(True)
            if Environment.azienda == "daog" and "dirett" in operazioneDao.denominazione:
                self.id_persona_giuridica_diretta_customcombobox.setType("fornitore")
                self.id_persona_giuridica_diretta_customcombobox.set_sensitive(True)
                self.persona_giuridica_diretta_label.set_text("Forn")
            else:
                self.id_persona_giuridica_diretta_customcombobox.set_sensitive(False)


            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.numero_lotto_label.set_property('visible', False)
            self.numero_lotto_entry.set_property('visible', False)
            self.data_prezzo_label.set_property('visible', False)
            self.data_prezzo_datewidget.set_property('visible', False)
            self.data_scadenza_label.set_property('visible', False)
            self.data_scadenza_datewidget.set_property('visible', False)
            self.data_produzione_label.set_property('visible', False)
            self.data_produzione_datewidget.set_property('visible', False)
            self.ordine_minimo_label.set_property('visible', False)
            self.ordine_minimo_entry.set_property('visible', False)
            self.tempo_arrivo_merce_label.set_property('visible', False)
            self.tempo_arrivo_merce_entry.set_property('visible', False)
            self.dettaglio_giacenza_togglebutton.set_property("visible", True)
            self.lotto_temp_label.set_property('visible', True)
            self.lotto_temp_entry.set_property('visible', True)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')
        else:
            self.persona_giuridica_label.set_text('Cliente/Fornitore ?')
            self.id_persona_giuridica_customcombobox.set_sensitive(False)
            if Environment.azienda == "daog":
                self.id_persona_giuridica_diretta_customcombobox.set_sensitive(False)
                self.persona_giuridica_diretta_label.set_sensitive(False)
            self.label_listino.set_property('visible', True)
            self.id_listino_customcombobox.set_property('visible', True)
            self.prz_lordo_label.set_text('Prezzo')
            self.prz_netto_label.set_text('Prezzo netto')
            #self.codice_articolo_fornitore_label.set_property('visible', False)
            self.codice_articolo_fornitore_entry.set_property('visible', False)
            self.numero_lotto_label.set_property('visible', False)
            self.numero_lotto_entry.set_property('visible', False)
            self.data_prezzo_label.set_property('visible', False)
            self.data_prezzo_datewidget.set_property('visible', False)
            self.data_scadenza_label.set_property('visible', False)
            self.data_scadenza_datewidget.set_property('visible', False)
            self.data_produzione_label.set_property('visible', False)
            self.data_produzione_datewidget.set_property('visible', False)
            self.ordine_minimo_label.set_property('visible', False)
            self.ordine_minimo_entry.set_property('visible', False)
            self.tempo_arrivo_merce_label.set_property('visible', False)
            self.tempo_arrivo_merce_entry.set_property('visible', False)
            self.dettaglio_giacenza_togglebutton.set_property("visible", True)
            #self.dettaglio_giacenza_togglebutton.set_property("sensible", False)
            self.protocollo_label.set_property('visible', False)
            self.protocollo_entry1.set_property('visible', False)
            self.numero_documento_label.set_text('Numero')
            self.lotto_temp_label.set_property('visible', False)
            self.lotto_temp_entry.set_property('visible', False)
        self.persona_giuridica_changed()
        self.data_documento_entry.grab_focus()


    def on_dettaglio_giacenza_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        idArt =  self._righe[0]["idArticolo"]
        if not idArt:
            messageInfo(msg=_("NESSUN ARTICOLO o RIGA SELEZIONATO"))
            toggleButton.set_active(False)
            return
        a = DettaglioGiacenzaWindow(mainWindow=self,
                                    riga= self._righe[0])
        anagWindow = a.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()
        toggleButton.set_active(False)



    def persona_giuridica_changed(self):
        if self._loading:
            self.refresh_combobox_listini()
            return

        inseritoIntestatario = (self.id_persona_giuridica_customcombobox.getId() is not None)
        if inseritoIntestatario:
            datiIntestatario = self.id_persona_giuridica_customcombobox.getData()
            self._id_pagamento = datiIntestatario["id_pagamento"]
            self._id_magazzino = datiIntestatario["id_magazzino"]
            if self._tipoPersonaGiuridica == "cliente":
                self._id_listino = datiIntestatario["id_listino"]
                self._id_banca = datiIntestatario["id_banca"]
            if self.pagamenti_page.id_pagamento_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.pagamenti_page.id_pagamento_customcombobox.combobox, self._id_pagamento)
            if self.id_magazzino_combobox.get_active() == -1:
                findComboboxRowFromId(self.id_magazzino_combobox, self._id_magazzino)
            if self.pagamenti_page.id_banca_customcombobox.combobox.get_active() == -1:
                findComboboxRowFromId(self.pagamenti_page.id_banca_customcombobox.combobox, self._id_banca)

        if self._tipoPersonaGiuridica == "cliente":
            #self.id_destinazione_merce_customcombobox.set_sensitive(True)
            if self.id_persona_giuridica_customcombobox.getId() is None:
                self.id_destinazione_merce_customcombobox.combobox.clear()
                self.id_destinazione_merce_customcombobox.set_sensitive(False)
            else:
                fillComboboxDestinazioniMerce(self.id_destinazione_merce_customcombobox.combobox,
                        self.id_persona_giuridica_customcombobox.getId())
                if not self.dao.id:
                    if setconf('Documenti', 'primo_dest_merce'):
                        self.id_destinazione_merce_customcombobox.combobox.set_active(1)
                self.id_destinazione_merce_customcombobox.set_sensitive(True)
            self.refresh_combobox_listini()
        else:
            self.id_destinazione_merce_customcombobox.combobox.clear()
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

    def id_pagamento_customcombobox_changed(self, combobox):
        if self._loading:
            return
        self.pagamenti_page.on_calcola_importi_scadenza_button_clicked(None)

    def on_id_listino_customcombobox_changed(self, combobox=None):
        """ funzione richiamata quando viene modificato o settato il listino """
        if self._loading:
            return
        idListino = findIdFromCombobox(self.id_listino_customcombobox.combobox)
        idArticolo = self._righe[0]["idArticolo"]

        self.getPrezzoVenditaLordo(idListino, idArticolo)
        self.prezzo_lordo_entry.set_text(str(self._righe[0]["prezzoLordo"]))
        self._righe[0]["sconti"] = [{'valore':sconto.valore, 'tipo': sconto.tipo_sconto} for sconto in self._righe[0]["sconti"]]
        self._righe[0]["sconti"] += self._righe[0]["VL"]
        self.sconti_widget.setValues(self._righe[0]["sconti"], self._righe[0]["applicazioneSconti"], False)

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

    def on_moltiplicatore_entry_focus_out_event(self, entry, event):
        on_moltiplicatore_entry_focus_out_eventPart(self, entry, event)

    def on_end_rent_entry_focus_out_event(self, entry=None, event=None):
        if self.end_rent_entry.entry.get_text() and self.start_rent_entry.entry.get_text():
            self._durataNoleggio = stringToDateTime(self.end_rent_entry.get_text())- stringToDateTime(self.start_rent_entry.get_text())
            if self._durataNoleggio.days >0:
                self.giorni_label.set_text(str(self._durataNoleggio.days) or "")
                self.rent_checkbutton.set_active(True)
            else:
                msg =  _("ERRORE NELLA DURATA DEL NOLEGGIO\nNON PUO' ESSERE ZERO O NEGATIVA")
                messageInfo(msg=msg)

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


    def on_avvertimento_sconti_button_clicked(self, button):
        self.notebook.set_current_page(2)

    def on_articolo_entry_icon_press(self,entry, position,event ):
#        if position.real == 0:
#            x = int(event.x)
#            y = int(event.y)
#            time = event.time
#            self.menu_ricerca.popup( None, None, None, event.button, time)
#        else:                            #secondary
        self.articolo_entry.set_text("")

    def on_descrizione_entry_icon_press(self,entry, position,event ):
        if position.real == 1:
            self.descrizione_entry.set_text("")
