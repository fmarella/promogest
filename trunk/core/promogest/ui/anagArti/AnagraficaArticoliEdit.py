# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.gtk_compat import *
from promogest import Environment
import promogest.dao.Fornitura
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso

if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.Modello import Modello
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.ui.AnagraficaArticoliPromoWearExpand import articleTypeGuiManage, treeViewExpand
    from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori

if posso("ADR"):
    from promogest.modules.ADR.ui.ADRNotebookPage import ADRNotebookPage
if posso("CSA"):
    from promogest.modules.CSA.ui.CSANotebookPage import CSANotebookPage




class AnagraficaArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati articolo',
                                root='anagrafica_articoli_detail_table',
                                path='_anagrafica_articoli_detail.glade')
        self._widgetFirstFocus = self.codice_entry
        self._loading = False
        #FIXME: promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._codiceByFamiglia = promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._duplicatedDaoId = None

        if not posso("PW"):
            self.normale_radiobutton.set_active(True)
            self.codici_a_barre_label.set_text('')
            self.plus_radiobutton.set_property('visible', False)
            self.plus_radiobutton.set_no_show_all(True)
            self.codici_a_barre_hseparator.set_property('visible', False)
            self.codici_a_barre_hseparator.set_no_show_all(True)
            self.con_taglie_colori_radiobutton.set_property('visible', False)
            self.con_taglie_colori_radiobutton.set_no_show_all(True)
            self.taglie_colori_togglebutton.set_property('visible', False)
            self.taglie_colori_togglebutton.set_no_show_all(True)
            self.notebook1.remove_page(3)
            self.promowear_frame.destroy()
        if not posso("GN"):
            self.divisore_noleggio_entry.destroy()
            self.divisore_noleggio_label.destroy()

    def draw(self,cplx=False):
        if posso("PW"):
            self.normale_radiobutton.set_active(True)
            self.frame_promowear.set_sensitive(False)
            self.codici_a_barre_togglebutton.set_sensitive(True)
            self.taglie_colori_togglebutton.set_sensitive(False)
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_customcombobox.combobox)
            self.id_gruppo_taglia_customcombobox.connect('clicked',
                                                         on_id_gruppo_taglia_customcombobox_clicked)
            fillComboboxTaglie(self.id_taglia_customcombobox.combobox)
            self.id_taglia_customcombobox.connect('clicked',
                                                  self.on_id_taglia_customcombobox_clicked)
            fillComboboxColori(self.id_colore_customcombobox.combobox)
            self.id_colore_customcombobox.connect('clicked',
                                                  self.on_id_colore_customcombobox_clicked)
            fillComboboxModelli(self.id_modello_customcombobox.combobox)
            self.id_modello_customcombobox.connect('clicked',
                                                  on_id_modello_customcombobox_clicked)
            fillComboboxAnniAbbigliamento(self.id_anno_combobox)
            fillComboboxStagioniAbbigliamento(self.id_stagione_combobox)
            fillComboboxGeneriAbbigliamento(self.id_genere_combobox)

        #combo e draw della parte normale dell'applicazione  ...
        fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        self.id_aliquota_iva_customcombobox.connect('clicked',
                                            on_id_aliquota_iva_customcombobox_clicked)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_customcombobox.combobox)
        self.id_categoria_articolo_customcombobox.connect('clicked',
                                            on_id_categoria_articolo_customcombobox_clicked)
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_customcombobox.combobox)
        self.id_famiglia_articolo_customcombobox.connect('clicked',
                                            on_id_famiglia_articolo_customcombobox_clicked)
        if self._codiceByFamiglia:
            #Collega la creazione di un nuovo codice articolo al cambiamento della famiglia
            self.id_famiglia_articolo_customcombobox.combobox.connect('changed',
                                                                      self.on_id_famiglia_articolo_customcombobox_changed)
        fillComboboxStatiArticoli(self.id_stato_articolo_combobox)
        fillComboboxImballaggi(self.id_imballaggio_customcombobox.combobox)
        self.id_imballaggio_customcombobox.connect('clicked',
                                                   on_id_imballaggio_customcombobox_clicked)
        fillComboboxUnitaBase(self.id_unita_base_combobox)
        fillComboboxUnitaFisica(self.unita_dimensioni_comboboxentry,'dimensioni')
        fillComboboxUnitaFisica(self.unita_volume_comboboxentry,'volume')
        fillComboboxUnitaFisica(self.unita_peso_comboboxentry,'peso')

        fillComboboxProduttori(self.produttore_comboboxentry)

        if posso("ADR"):
            self.adr_page = ADRNotebookPage(self)
            self.notebook1.append_page(self.adr_page.adr_frame, self.adr_page.adr_page_label)
        if posso("CSA"):
            self.csa_page = CSANotebookPage(self)
            self.notebook1.append_page(self.csa_page.csa_frame, self.csa_page.csa_page_label)
        else:
            self.csa_togglebutton.destroy()

    def setDao(self, dao):
        if not dao:
            # Crea un nuovo Dao vuoto
            self.dao = Articolo()
            # Assegna il codice se ne e' prevista la crazione automatica, ma non per famiglia
            #if not self._codiceByFamiglia:
                #self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)
                #print "STAMPO IL NUOVO CODICE ARTICOLO IN SETDAO GENERATO",self.dao.codice
            # Prova a impostare "pezzi" come unita' di misura base
            self.dao.id_unita_base = 1
            self.new=True
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = dao
            self.new=False

        if posso("ADR"):
            self.adr_page.adrSetDao(self.dao)

        if posso("CSA"):
            self.csa_page.csaSetDao(self.dao)
        self._refresh()
        return self.dao


    def _refresh(self):
        self._loading = True
        self.codice_entry.set_text(self.dao.codice or '')
        self.denominazione_entry.set_text(self.dao.denominazione or '')

        findComboboxRowFromId(self.id_aliquota_iva_customcombobox.combobox,
                              self.dao.id_aliquota_iva)
        findComboboxRowFromId(self.id_famiglia_articolo_customcombobox.combobox,
                              self.dao.id_famiglia_articolo)
        findComboboxRowFromId(self.id_categoria_articolo_customcombobox.combobox,
                              self.dao.id_categoria_articolo)
        findComboboxRowFromId(self.id_unita_base_combobox,
                              self.dao.id_unita_base)
        findComboboxRowFromId(self.id_stato_articolo_combobox,
                              self.dao.id_stato_articolo)
        findComboboxRowFromId(self.id_imballaggio_customcombobox.combobox,
                              self.dao.id_imballaggio)
        fillComboboxProduttori(self.produttore_comboboxentry)
        self.produttore_comboboxentry.get_child().set_text(self.dao.produttore or '')
        self.unita_dimensioni_comboboxentry.get_child().set_text(self.dao.unita_dimensioni or '')
        self.unita_volume_comboboxentry.get_child().set_text(self.dao.unita_volume
                                                       or '')
        self.unita_peso_comboboxentry.get_child().set_text(self.dao.unita_peso or '')
        self.lunghezza_entry.set_text('%-6.3f' % float(self.dao.lunghezza or 0))
        self.larghezza_entry.set_text('%-6.3f' % float(self.dao.larghezza or 0))
        self.altezza_entry.set_text('%-6.3f' % float(self.dao.altezza or 0))
        self.volume_entry.set_text('%-6.3f' % float(self.dao.volume or 0))
        self.peso_lordo_entry.set_text('%-6.3f' % float(self.dao.peso_lordo or 0))
        self.peso_imballaggio_entry.set_text('%-6.3f' % float(self.dao.peso_imballaggio or 0))
        self.stampa_etichetta_checkbutton.set_active(self.dao.stampa_etichetta or True)
        self.codice_etichetta_entry.set_text(self.dao.codice_etichetta or '')
        self.url_articolo_entry.set_text(self.dao.url_immagine or '')
        self.descrizione_etichetta_entry.set_text(self.dao.descrizione_etichetta or '')
        self.stampa_listino_checkbutton.set_active(self.dao.stampa_listino or True)
        self.descrizione_listino_entry.set_text(self.dao.descrizione_listino or '')
        self.quantita_minima_entry.set_text(str(self.dao.quantita_minima or 0))
        if self.quantita_minima_entry.get_text() == '0':
            self.quantita_minima_entry.set_text('')
        textBuffer = self.note_textview.get_buffer()
        if self.dao.note is not None:
            textBuffer.set_text(self.dao.note)
        else:
            textBuffer.set_text('')
        self.note_textview.set_buffer(textBuffer)
        self.sospeso_checkbutton.set_active(self.dao.sospeso or False)
        if posso("PW"):
             #articolo ancora non salvato o articolo senza taglia e colore
             #Articolo in anagrafica già salvato con id_articolo_padre pieno quindi è una variante
            a = articleTypeGuiManage(self, self.dao, new=self.new)
        if posso("GN"):
            self.divisore_noleggio_entry.set_text(str(self.dao.divisore_noleggio))
        if posso("ADR"):
            self.adr_page.adr_refresh()
        if posso("CSA"):
            self.csa_page.csa_refresh()
        self._loading = False

    def saveDao(self, tipo=None):
        """ Salvataggio del dao con un po' di logica legata alle diverse
            tipologie di articolo :noleggio, su misura, promowear
        """
        if (self.codice_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.codice_entry,
                            msg='Campo obbligatorio !\n\nCodice')

        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.denominazione_entry,
                            msg='Campo obbligatorio !\n\nDenominazione')

        if findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_aliquota_iva_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nAliquota IVA')

        if findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_famiglia_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nFamiglia merceologica')

        if findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_categoria_articolo_customcombobox.combobox,
                            msg='Campo obbligatorio !\n\nCategoria articolo')

        if findIdFromCombobox(self.id_unita_base_combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_unita_base_combobox,
                            msg='Campo obbligatorio !\n\nUnita\' base')
        pbar(self.dialog.pbar,parziale=1, totale=4)
        if posso("PW") and (articleType(self.dao) == "plus" or self.plus_radiobutton.get_active()):
            articoloTagliaColore = ArticoloTagliaColore()
            articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
            articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
            articoloTagliaColore.id_modello = findIdFromCombobox(self.id_modello_customcombobox.combobox)
            articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
            articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
            articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
            self.dao.articoloTagliaColore = articoloTagliaColore
            articoloTagliaColore = None
            #potrà sembrare una ripetizione ma preferisco gestirlo di fino con altri controlli
        elif posso("PW") and (articleType(self.dao) == "son" and self.con_taglie_colori_radiobutton.get_active()):
            articoloTagliaColore = ArticoloTagliaColore()
            articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
            articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
            articoloTagliaColore.id_modello = findIdFromCombobox(self.id_modello_customcombobox.combobox)
            articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
            articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
            articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
            articoloTagliaColore.id_articolo_padre = self.dao.id_articolo_padre
            self.dao.articoloTagliaColore = articoloTagliaColore
            articoloTagliaColore = None
        elif posso("PW") and (articleType(self.dao) == "father" or self.con_taglie_colori_radiobutton.get_active()):
            print "SALVATAGGIO ARTICOLO PADRE"
            if self.dao.denominazione != self.denominazione_entry.get_text():
                msg = """ATTENZIONE La descrizione di un articolo padre è cambiata, vuoi riportare la modifica anche ai suoi figli?"""
                if YesNoDialog(msg=msg, transient=None):
                    if self.dao.articoliVarianti:
                        for ar in self.dao.articoliVarianti:
                            ar.denominazione= self.denominazione_entry.get_text() +" "+ ar.denominazione_breve_taglia + ' ' + ar.denominazione_breve_colore
                            ar.persist()

            if self.dao.produttore != self.produttore_comboboxentry.get_child().get_text():
                msg = """ATTENZIONE Il  produttore di un articolo padre è cambiata, vuoi riportare la modifica anche ai suoi figli?"""
                if YesNoDialog(msg=msg, transient=None):
                    if self.dao.articoliVarianti:
                        for ar in self.dao.articoliVarianti:
                            ar.produttore = self.produttore_comboboxentry.get_child().get_text()
                            ar.persist()

            articoloTagliaColore = ArticoloTagliaColore()
            articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
            articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
            articoloTagliaColore.id_modello = findIdFromCombobox(self.id_modello_customcombobox.combobox)
            if articoloTagliaColore.id_taglia or articoloTagliaColore.id_colore:
                msg =""" ATTENZIONE: Articolo Padre Taglia e Colore NON
    può avere Colore o Taglia propri."""
                messageInfo(msg=msg)
                return
            articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
            articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
            articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
            self.dao.articoloTagliaColore = articoloTagliaColore
            articoloTagliaColore = None
        pbar(self.dialog.pbar,parziale=2, totale=4)
        self.dao.codice = str(self.codice_entry.get_text()).strip()
        self.dao.codice = omogeneousCode(section="Articoli", string=self.dao.codice )
        cod=checkCodiceDuplicato(codice=self.dao.codice,id=self.dao.id, tipo="Articolo")
        if not cod:
            raise Exception, 'Operation aborted campo obbligatorio'
        #else:
            #raise Exception, 'Operation aborted codice articolo duplicato'
        self.dao.denominazione = self.denominazione_entry.get_text()
        if posso("GN"):
            self.dao.divisore_noleggio_value_set = self.divisore_noleggio_entry.get_text().strip()
        if posso("ADR"):
            self.dao.articolo_adr_dao = self.adr_page.adrSaveDao()
        if posso("CSA"):
            self.dao.articolo_csa_dao = self.csa_page.csaSaveDao()
        self.dao.id_aliquota_iva = findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox)
        self.dao.id_famiglia_articolo = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        self.dao.id_categoria_articolo = findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox)
        self.dao.id_unita_base = findIdFromCombobox(self.id_unita_base_combobox)
        self.dao.id_stato_articolo = findIdFromCombobox(self.id_stato_articolo_combobox)
        self.dao.id_imballaggio = findIdFromCombobox(self.id_imballaggio_customcombobox.combobox)
        self.dao.produttore = self.produttore_comboboxentry.get_child().get_text()
        self.dao.unita_dimensioni = self.unita_dimensioni_comboboxentry.get_child().get_text()
        self.dao.unita_volume = self.unita_volume_comboboxentry.get_child().get_text()
        self.dao.unita_peso = self.unita_peso_comboboxentry.get_child().get_text()
        self.dao.lunghezza = float(self.lunghezza_entry.get_text() or 0)
        self.dao.larghezza = float(self.larghezza_entry.get_text() or 0)
        self.dao.altezza = float(self.altezza_entry.get_text() or 0)
        self.dao.volume = float(self.volume_entry.get_text() or 0)
        self.dao.peso_lordo = float(self.peso_lordo_entry.get_text() or 0)
        self.dao.peso_imballaggio = float(self.peso_imballaggio_entry.get_text() or 0)
        self.dao.quantita_minima = float(self.quantita_minima_entry.get_text() or 0)
        self.dao.stampa_etichetta = self.stampa_etichetta_checkbutton.get_active()
        self.dao.codice_etichetta = self.codice_etichetta_entry.get_text()
        self.dao.descrizione_etichetta = self.descrizione_etichetta_entry.get_text()
        self.dao.stampa_listino = self.stampa_listino_checkbutton.get_active()
        self.dao.descrizione_listino = self.descrizione_listino_entry.get_text()
        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter(),True)
        self.dao.sospeso = self.sospeso_checkbutton.get_active()
        if self.dao.cancellato == None:
            self.dao.cancellato = False
        if self.dao.aggiornamento_listino_auto == None:
            self.dao.aggiornamento_listino_auto = False
        self.dao.url_immagine = self.url_articolo_entry.get_text()
        pbar(self.dialog.pbar,parziale=3, totale=4)
        self.dao.persist()
        pbar(self.dialog.pbar,parziale=4, totale=4)
        pbar(self.dialog.pbar,stop=True)

        if self._duplicatedDaoId is not None:
            self.duplicaListini()

    def on_codici_a_barre_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i codici a barre occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.AnagraficaCodiciABarreArticoli import AnagraficaCodiciABarreArticoli
        anag = AnagraficaCodiciABarreArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_multipli_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i multipli occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_stoccaggi_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i dati di stoccaggio occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagStoccaggi.AnagraficaStoccaggi import AnagraficaStoccaggi
        anag = AnagraficaStoccaggi(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_kit_master_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = ('Prima di poter creare un kit occorre '
                   + 'salvare l\' articolo.\n Salvare ?')

            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.modules.GestioneKit.ui.KitMaster import KitMaster
        anag = KitMaster(self.dao)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)


    def on_abbina_immagine_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = ('Prima di poter creare un kit occorre '
                   + 'salvare l\' articolo.\n Salvare ?')

            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return
        if posso("LA"):
            from promogest.modules.GestioneFile.ui.AnagraficaFiles import AnagraficaFiles
            anag = AnagraficaFiles(dao=self.dao)
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
        else:
            fencemsg()


    def on_forniture_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = ('Prima di poter inserire le forniture occorre '
                   + 'salvare l\' articolo.\n Salvare ?')

            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.anagForniture.AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i listini occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from promogest.ui.AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_label_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter stampare una label occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        if self.dao.codice_a_barre is None:
            msg = 'Prima di poter stampare una label occorre aggiungere un codice a barre ?'
            messageInfo(msg = msg)
            toggleButton.set_active(False)
            return

        if posso("LA"):
            from promogest.modules.Label.ui.ManageLabelsToPrint import ManageLabelsToPrint
            a = ManageLabelsToPrint(mainWindow=self,daos=[], art=self.dao)
            anagWindow = a.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            fencemsg()
        toggleButton.set_active(False)

    def duplicaListini(self):
        """ Duplica i listini relativi ad un articolo scelto su un nuovo articolo """
        if self._duplicatedDaoId is None:
            return

        from promogest.dao.ListinoArticolo import ListinoArticolo
        listini = ListinoArticolo().select(idArticolo = self._duplicatedDaoId)
        for listino in listini:
            daoLA = ListinoArticolo()
            daoLA.id_listino = listino.id_listino
            daoLA.id_articolo = self.dao.id
            daoLA.prezzo_dettaglio = listino.prezzo_dettaglio
            daoLA.prezzo_ingrosso = listino.prezzo_ingrosso
            daoLA.ultimo_costo = listino.ultimo_costo
            daoLA.data_listino_articolo = listino.data_listino_articolo
            sconti_ingrosso = []
            sconti_dettaglio = []
            if listino.sconto_vendita_dettaglio:
                daoLA.applicazione_sconti = "scalare"
                for s in listino.sconto_vendita_dettaglio:
                    daoScontod = ScontoVenditaDettaglio()
                    daoScontod.valore = s.valore
                    daoScontod.tipo_sconto = s.tipo_sconto
                    sconti_dettaglio.append(daoScontod)
            if listino.sconto_vendita_dettaglio:

                daoLA.applicazione_sconti = "scalare"
                for s in listino.sconto_vendita_ingrosso:
                    daoScontoi = ScontoVenditaIngrosso()
                    daoScontoi.valore = s.valore
                    daoScontoi.tipo_sconto = s.tipo_sconto
                    sconti_ingrosso.append(daoScontoi)
            daoLA.persist(sconti={"dettaglio":sconti_dettaglio,"ingrosso":sconti_ingrosso})

        self._duplicatedDaoId = None

    def on_id_famiglia_articolo_customcombobox_changed(self, combobox):
        """ Restituisce un nuovo codice articolo al cambiamento della famiglia
        """
        if self._loading:
            return

        if not self._codiceByFamiglia:
            return

        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        if idFamiglia is not None:
            self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=idFamiglia)
            self.codice_entry.set_text(self.dao.codice)

    def on_normale_radiobutton_toggled(self, radioButton):
        active = radioButton.get_active()
        if active:
            if findIdFromCombobox(self.id_colore_customcombobox.combobox) is not None or \
                findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is not None or \
                findIdFromCombobox(self.id_anno_combobox) is not None or \
                findIdFromCombobox(self.id_stagione_combobox) is not None or \
                findIdFromCombobox(self.id_genere_combobox) is not None or \
                findIdFromCombobox(self.id_taglia_customcombobox.combobox) is not None or \
                findIdFromCombobox(self.id_colore_customcombobox.combobox) is not None:
                if not self.new:
                    msg = """ATTENZIONE: Si sta modificando un Tipo Articolo
da PLUS a NORMALE questo comporta la perdita
dei dati accessori. Continuare?"""
                    if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                        #self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
                        self.id_anno_combobox.set_active(-1)
                        self.id_genere_combobox.set_active(-1)
                        self.id_stagione_combobox.set_active(-1)
                        self.id_gruppo_taglia_customcombobox.combobox.set_active(-1)
                        self.id_taglia_customcombobox.combobox.set_active(-1)
                        self.id_modello_customcombobox.combobox.set_active(-1)
                        self.id_colore_customcombobox.combobox.set_active(-1)
                        self.denominazione_genere_label.set_property('visible', False)
                        self.denominazione_taglia_label.set_property('visible', False)
                        self.denominazione_colore_label.set_property('visible', False)
                        self.denominazione_gruppo_taglia_label.set_property('visible', False)
                        self.denominazione_stagione_anno_label.set_property('visible', False)
                        self.memo_wear.set_text("""ARTICOLO NORMALE""")
                    else:
                        self.plus_radiobutton.set_sensitive(True)
                        self.on_plus_radiobutton_toggled(radioButton)
                        return
            self.normale_radiobutton.set_active(True)
            self.codici_a_barre_togglebutton.set_sensitive(True)
            self.taglie_colori_togglebutton.set_sensitive(False)
            self.id_colore_customcombobox.set_sensitive(True)
            self.id_taglia_customcombobox.set_sensitive(True)
            self.id_modello_customcombobox.set_sensitive(True)
            self.frame_promowear.set_sensitive(False)

    def on_plus_radiobutton_toggled(self, radioButton):
        active= radioButton.get_active()
        if active:
            self.plus_radiobutton.set_active(True)
            self.codici_a_barre_togglebutton.set_sensitive(True)
            self.varianti_taglia_colore_label.set_sensitive(False)
            self.taglie_colori_togglebutton.set_sensitive(False)
            self.id_colore_customcombobox.set_sensitive(True)
            self.id_taglia_customcombobox.set_sensitive(True)
            self.id_modello_customcombobox.set_sensitive(True)
            self.frame_promowear.set_sensitive(True)

    def on_con_taglie_colori_radiobutton_toggled(self, radioButton):
        active= radioButton.get_active()
        if active:
            self.con_taglie_colori_radiobutton.set_active(True)
            self.codici_a_barre_togglebutton.set_sensitive(False)
            self.varianti_taglia_colore_label.set_sensitive(True)
            self.taglie_colori_togglebutton.set_sensitive(True)
            self.id_colore_customcombobox.set_sensitive(False)
            self.id_taglia_customcombobox.set_sensitive(False)
            self.id_modello_customcombobox.set_sensitive(True)
            self.frame_promowear.set_sensitive(True)

    def on_icon_press_primary(self,entry,position,event):
        if position.value_nick == "primary":
            codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)
            self.codice_entry.set_text(codice)

    def on_taglie_colori_togglebutton_clicked(self, toggleButton):
        """ TogGLeButton delle taglie e colori, solo per la definizione delle varianti"""
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        #if idGruppoTaglia is not None or idAnno is not None or idStagione is not None or idGenere is not None:
        if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel,
                            self.id_gruppo_taglia_customcombobox.combobox,
                            msg='Campo obbligatorio !\nGruppo taglia')
        idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
        idAnno = findIdFromCombobox(self.id_anno_combobox)
        idStagione = findIdFromCombobox(self.id_stagione_combobox)
        idGenere = findIdFromCombobox(self.id_genere_combobox)
        if self.dao.id is None or self.dao is None:
            msg = 'Prima di poter inserire taglie, colori e codici a barre occorre salvare l\' articolo.\n Salvare ?'
            if YesNoDialog(msg=msg, transient=self.dialogTopLevel):
                try:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, GTK_RESPONSE_APPLY)
                except:
                    toggleButton.set_active(False)
                    return
            else:
                toggleButton.set_active(False)
                return
        if articleType(self.dao) == "son":
            if findIdFromCombobox(self.id_taglia_customcombobox.combobox) is None:
                obligatoryField(self.dialogTopLevel,
                                self.id_taglia_customcombobox.combobox,
                                msg='Campo obbligatorio !\nTaglia')

            if findIdFromCombobox(self.id_colore_customcombobox.combobox) is None:
                obligatoryField(self.dialogTopLevel,
                                self.id_colore_customcombobox.combobox,
                                msg='Campo obbligatorio !\nColore')

        tagcol = GestioneTaglieColori(articolo=self.dao)

    def on_id_taglia_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self.dao.articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        if idTaglie:
            idTaglie.remove(self.dao.id_taglia)
        on_id_taglia_customcombobox_clicked(widget,
                                            button,
                                            idGruppoTaglia=self.dao.id_gruppo_taglia,
                                            ignore=list(idTaglie))

    def on_id_colore_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self.dao.articoliTagliaColore
        idColori = set(a.id_colore for a in articoliTagliaColore)
        if idColori:
            idColori.remove(self.dao.id_colore)
        on_id_colore_customcombobox_clicked(widget,
                                            button,
                                            ignore=list(idColori))
