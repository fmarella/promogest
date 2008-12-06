# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
 """

import gtk
import gobject
from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest import Environment
#from promogest.dao.Dao import Dao
import promogest.dao.Fornitura
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
from GladeWidget import GladeWidget
from utils import *
from utilsCombobox import *
if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.ui.AnagraficaArticoliExpand import articleTypeGuiManage, treeViewExpand

class AnagraficaArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_articoli_detail_table',
                                'Dati articolo',
                                gladeFile='_anagrafica_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_entry
        self._loading = False
        #FIXME: promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._codiceByFamiglia = promogest.dao.Articolo.isNuovoCodiceByFamiglia()
        self._duplicatedDaoId = None
        self.tipoArticoloTagliaColore=False
        if "PromoWear" not in Environment.modulesList:
            self.senza_taglie_colori_radiobutton.set_active(True)
            self.codici_a_barre_label.set_text('')
            self.senza_taglie_colori_radiobutton.set_property('visible', False)
            self.senza_taglie_colori_radiobutton.set_no_show_all(True)
            self.codici_a_barre_hseparator.set_property('visible', False)
            self.codici_a_barre_hseparator.set_no_show_all(True)
            self.con_taglie_colori_radiobutton.set_property('visible', False)
            self.con_taglie_colori_radiobutton.set_no_show_all(True)
            self.taglie_colori_togglebutton.set_property('visible', False)
            self.taglie_colori_togglebutton.set_no_show_all(True)
            self.notebook1.remove_page(3)
            self.promowear_frame.destroy()


    def draw(self):
        if "PromoWear" in Environment.modulesList:
            self.senza_taglie_colori_radiobutton.set_active(True)
            self.frame_promowear.set_sensitive(False)
            self.codici_a_barre_togglebutton.set_sensitive(True)
            self.taglie_colori_togglebutton.set_sensitive(False)
            #Popola combobox gruppi taglia
            fillComboboxGruppiTaglia(self.id_gruppo_taglia_customcombobox.combobox)
            self.id_gruppo_taglia_customcombobox.connect('clicked',
                                                         on_id_gruppo_taglia_customcombobox_clicked)
            #Popola combobox taglie
            fillComboboxTaglie(self.id_taglia_customcombobox.combobox)
            self.id_taglia_customcombobox.connect('clicked',
                                                  self.on_id_taglia_customcombobox_clicked)
            #Popola combobox colori
            fillComboboxColori(self.id_colore_customcombobox.combobox)
            self.id_colore_customcombobox.connect('clicked',
                                                  self.on_id_colore_customcombobox_clicked)
            #Popola combobox anni
            fillComboboxAnniAbbigliamento(self.id_anno_combobox)
            #Popola combobox stagioni
            fillComboboxStagioniAbbigliamento(self.id_stagione_combobox)
            #Popola combobox generi
            fillComboboxGeneriAbbigliamento(self.id_genere_combobox)

        #combo e draw della parte normale dell'applicazione  ...
        #Popola combobox aliquote iva
        fillComboboxAliquoteIva(self.id_aliquota_iva_customcombobox.combobox)
        self.id_aliquota_iva_customcombobox.connect('clicked',
                                            on_id_aliquota_iva_customcombobox_clicked)
        #Popola combobox categorie articolo
        fillComboboxCategorieArticoli(self.id_categoria_articolo_customcombobox.combobox)
        self.id_categoria_articolo_customcombobox.connect('clicked',
                                            on_id_categoria_articolo_customcombobox_clicked)
        #Popola combobox famiglie articolo
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_customcombobox.combobox)
        self.id_famiglia_articolo_customcombobox.connect('clicked',
                                            on_id_famiglia_articolo_customcombobox_clicked)
        if self._codiceByFamiglia:
            #Collega la creazione di un nuovo codice articolo al cambiamento della famiglia
            self.id_famiglia_articolo_customcombobox.combobox.connect('changed',
                                                                      self.on_id_famiglia_articolo_customcombobox_changed)
        #Popola combobox stati articolo
        fillComboboxStatiArticoli(self.id_stato_articolo_combobox)
        #Popola combobox imballaggi
        fillComboboxImballaggi(self.id_imballaggio_customcombobox.combobox)
        self.id_imballaggio_customcombobox.connect('clicked',
                                                   on_id_imballaggio_customcombobox_clicked)
        #Popola combobox unita base
        fillComboboxUnitaBase(self.id_unita_base_combobox)
        #Popola comboboxentry unita dimensioni
        fillComboboxUnitaFisica(self.unita_dimensioni_comboboxentry,'dimensioni')
        #Popola comboboxentry unita volume
        fillComboboxUnitaFisica(self.unita_volume_comboboxentry,'volume')
        #Popola comboboxentry unita peso
        fillComboboxUnitaFisica(self.unita_peso_comboboxentry,'peso')


    def setDao(self, dao):
        self.tipoArticoloTagliaColore=False
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Articolo()
            # Assegna il codice se ne e' prevista la crazione automatica, ma non per famiglia
            #if not self._codiceByFamiglia:
                #self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)
                #print "STAMPO IL NUOVO CODICE ARTICOLO IN SETDAO GENERATO",self.dao.codice
            # Prova a impostare "pezzi" come unita' di misura base
            self.dao.id_unita_base = 1
            self._oldDaoRicreato = False
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Articolo().getRecord(id=dao.id)
            self._oldDaoRicreato = True
        self._refresh()


    def _refresh(self):
        self._loading = True
        self.codice_entry.set_text(self.dao.codice or '')
        #print "STAMPO IL NUOVO CODICE ARTICOLO IN _REFRESH ",self.dao.codice
        #if self.dao.codice:
            #self.dao.codice = omogeneousCode(section="Articoli", string=self.dao.codice )
        #else:
            #print " ERRORE BY_PASSATO PER ILARIA :) "
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
        self.produttore_entry.set_text(self.dao.produttore or '')
        self.unita_dimensioni_comboboxentry.child.set_text(self.dao.unita_dimensioni or '')
        self.unita_volume_comboboxentry.child.set_text(self.dao.unita_volume
                                                       or '')
        self.unita_peso_comboboxentry.child.set_text(self.dao.unita_peso or '')
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
        if "PromoWear" in Environment.modulesList:
             #articolo ancora non salvato o articolo senza taglia e colore
            # Articolo in anagrafica già salvato con id_articolo_padre pieno quindi è una variante
            a = articleTypeGuiManage(self, self.dao)
        self._loading = False

    def saveDao(self):
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
        if "PromoWear" in Environment.modulesList and self.tipoArticoloTagliaColore:
            if self.dao is not None:
                articoloTagliaColore = ArticoloTagliaColore().getRecord(id=self.dao.id)
            else:
                articoloTagliaColore = ArticoloTagliaColore()
                articoloTagliaColore.id_articolo = self.dao.id

            articoloTagliaColore.id_gruppo_taglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
            articoloTagliaColore.id_taglia = findIdFromCombobox(self.id_taglia_customcombobox.combobox)
            articoloTagliaColore.id_colore = findIdFromCombobox(self.id_colore_customcombobox.combobox)
            articoloTagliaColore.id_anno = findIdFromCombobox(self.id_anno_combobox)
            articoloTagliaColore.id_stagione = findIdFromCombobox(self.id_stagione_combobox)
            articoloTagliaColore.id_genere = findIdFromCombobox(self.id_genere_combobox)
            self.dao.articoloTagliaColore = articoloTagliaColore
            articoloTagliaColore = None
        self.dao.codice = self.codice_entry.get_text()
        cod=checkCodiceDuplicato(codice=self.dao.codice,id=self.dao.id, tipo="Articolo")
        if not cod:
            return

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.id_aliquota_iva = findIdFromCombobox(self.id_aliquota_iva_customcombobox.combobox)
        self.dao.id_famiglia_articolo = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        self.dao.id_categoria_articolo = findIdFromCombobox(self.id_categoria_articolo_customcombobox.combobox)
        self.dao.id_unita_base = findIdFromCombobox(self.id_unita_base_combobox)
        self.dao.id_stato_articolo = findIdFromCombobox(self.id_stato_articolo_combobox)
        self.dao.id_imballaggio = findIdFromCombobox(self.id_imballaggio_customcombobox.combobox)
        self.dao.produttore = self.produttore_entry.get_text()
        self.dao.unita_dimensioni = self.unita_dimensioni_comboboxentry.child.get_text()
        self.dao.unita_volume = self.unita_volume_comboboxentry.child.get_text()
        self.dao.unita_peso = self.unita_peso_comboboxentry.child.get_text()
        try:
            self.dao.lunghezza = float(self.lunghezza_entry.get_text())
        except:
            self.dao.lunghezza = float(0)
        try:
            self.dao.larghezza = float(self.larghezza_entry.get_text())
        except:
            self.dao.larghezza = float(0)
        try:
            self.dao.altezza = float(self.altezza_entry.get_text())
        except:
            self.dao.altezza = float(0)
        try:
            self.dao.volume = float(self.volume_entry.get_text())
        except:
            self.dao.volume = float(0)
        try:
            self.dao.peso_lordo = float(self.peso_lordo_entry.get_text())
        except:
            self.dao.peso_lordo = float(0)
        try:
            self.dao.peso_imballaggio = float(self.peso_imballaggio_entry.get_text())
        except:
            self.dao.peso_imballaggio = float(0)
        try:
            self.dao.quantita_minima = float(self.quantita_minima_entry.get_text() or 0)
        except:
            self.dao.quantita_minima=float(0)
        self.dao.stampa_etichetta = self.stampa_etichetta_checkbutton.get_active()
        self.dao.codice_etichetta = self.codice_etichetta_entry.get_text()
        self.dao.descrizione_etichetta = self.descrizione_etichetta_entry.get_text()
        self.dao.stampa_listino = self.stampa_listino_checkbutton.get_active()
        self.dao.descrizione_listino = self.descrizione_listino_entry.get_text()
        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter())
        self.dao.sospeso = self.sospeso_checkbutton.get_active()
        if self.dao.cancellato == None:
            self.dao.cancellato = False
        if self.dao.aggiornamento_listino_auto == None:
            self.dao.aggiornamento_listino_auto = False
        self.dao.url_immagine = self.url_articolo_entry.get_text()
        self.dao.persist()

        if self._duplicatedDaoId is not None:
            self.duplicaListini()

    def on_codici_a_barre_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i codici a barre occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaCodiciABarreArticoli import AnagraficaCodiciABarreArticoli
        anag = AnagraficaCodiciABarreArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_multipli_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i multipli occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_stoccaggi_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i dati di stoccaggio occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaStoccaggi import AnagraficaStoccaggi
        anag = AnagraficaStoccaggi(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_forniture_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = ('Prima di poter inserire le forniture occorre '
                   + 'salvare l\' articolo.\n Salvare ?')
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def on_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i listini occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(self.dao.id)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)

    def duplicaListini(self):
        """ Duplica i listini relativi ad un articolo scelto su un nuovo articolo """
        if self._duplicatedDaoId is None:
            return

        from promogest.dao.ListinoArticolo import ListinoArticolo
        listini = ListinoArticolo(isList=True).select(idArticolo = self._duplicatedDaoId)
        for listino in listini:
            daoLA = ListinoArticolo()
            daoLA.id_listino = listino.id_listino
            daoLA.id_articolo = self.dao.id
            daoLA.prezzo_dettaglio = listino.prezzo_dettaglio
            daoLA.prezzo_ingrosso = listino.prezzo_ingrosso
            daoLA.ultimo_costo = listino.ultimo_costo
            daoLA.data_listino_articolo = listino.data_listino_articolo
            daoLA.persist()

        self._duplicatedDaoId = None

    def on_id_famiglia_articolo_customcombobox_changed(self, combobox):
        """ Restituisce un nuovo codice articolo al cambiamento della famiglia """

        if self._loading:
            return

        if not self._codiceByFamiglia:
            return

        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_customcombobox.combobox)
        if idFamiglia is not None:
            self.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=idFamiglia)
            self.codice_entry.set_text(self.dao.codice)

    def on_senza_taglie_colori_radiobutton_toggled(self, radioButton):
        active = radioButton.get_active()
        if active:
            self.senza_taglie_colori_radiobutton.set_active(True)
            self.codici_a_barre_togglebutton.set_sensitive(True)
            self.taglie_colori_togglebutton.set_sensitive(False)
            self.frame_promowear.set_sensitive(False)
        else:
            self.senza_taglie_colori_radiobutton.set_active(False)
            self.codici_a_barre_togglebutton.set_sensitive(False)
            self.taglie_colori_togglebutton.set_sensitive(True)
            self.frame_promowear.set_sensitive(True)

    def on_generate_article_code_button_clicked(self, button):
        codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)
        self.codice_entry.set_text(codice)

    def on_taglie_colori_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
            toggleButton.set_active(False)
            obligatoryField(self.dialogTopLevel, self.id_gruppo_taglia_customcombobox.combobox, 'Specificare il gruppo taglia !')
        idGruppoTaglia = findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox)
        idAnno = findIdFromCombobox(self.id_anno_combobox)
        idStagione = findIdFromCombobox(self.id_stagione_combobox)
        idGenere = findIdFromCombobox(self.id_genere_combobox)
        if idGruppoTaglia is not None or idAnno is not None or idStagione is not None or idGenere is not None:
                if findIdFromCombobox(self.id_gruppo_taglia_customcombobox.combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_gruppo_taglia_customcombobox.combobox,
                                    msg='Campo obbligatorio !\nGruppo taglia')

                if findIdFromCombobox(self.id_anno_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_anno_combobox,
                                    msg='Campo obbligatorio !\nAnno')

                if findIdFromCombobox(self.id_stagione_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_stagione_combobox,
                                    msg='Campo obbligatorio !\nStagione')

                if findIdFromCombobox(self.id_genere_combobox) is None:
                    obligatoryField(self.dialogTopLevel,
                                    self.id_genere_combobox,
                                    msg='Campo obbligatorio !\nGenere')

                if self.dao is not None:
                    if self.dao.id_articolo_padre is not None:
                        if findIdFromCombobox(self.id_taglia_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_taglia_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nTaglia')

                        if findIdFromCombobox(self.id_colore_customcombobox.combobox) is None:
                            obligatoryField(self.dialogTopLevel,
                                            self.id_colore_customcombobox.combobox,
                                            msg='Campo obbligatorio !\nColore')

        if self.dao.id is None or self.dao is None:
            msg = 'Prima di poter inserire taglie, colori e codici a barre occorre salvare l\' articolo.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION,
                                       gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                try:
                    self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                except:
                    toggleButton.set_active(False)
                    return
            else:
                toggleButton.set_active(False)
                return

        from promogest.modules.PromoWear.ui.TaglieColori import GestioneTaglieColori
        tagcol = GestioneTaglieColori(articolo=self.dao)
        tagcolWindow = tagcol.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, tagcolWindow, toggleButton)


    def on_id_taglia_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self.dao.articoliTagliaColore
        idTaglie = set(a.id_taglia for a in articoliTagliaColore)
        idTaglie.remove(self.dao.id_taglia)
        on_id_taglia_customcombobox_clicked(widget,
                                            button,
                                            idGruppoTaglia=self.dao.id_gruppo_taglia,
                                            ignore=list(idTaglie))


    def on_id_colore_customcombobox_clicked(self, widget, button):
        articoliTagliaColore = self.dao.articoliTagliaColore
        idColori = set(a.id_colore for a in articoliTagliaColore)
        idColori.remove(self.dao.id_colore)
        on_id_colore_customcombobox_clicked(widget,
                                            button,
                                            ignore=list(idColori))