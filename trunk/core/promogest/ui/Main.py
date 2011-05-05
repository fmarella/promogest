# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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

import locale
import gtk
import hashlib
import os
import glob
try:
    import ho.pisa as pisa
except:
    print """ERRORE NELL'IMPORT DI PISA prova a digitare
'sudo apt-get install python-pisa" nel terminale' """
#    import pisaLib.ho.pisa as pisa

from datetime import datetime
import webbrowser
from  subprocess import *
from promogest import Environment
from GladeWidget import GladeWidget
from ElencoMagazzini import ElencoMagazzini
from ElencoListini import ElencoListini
from VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from promogest.ui.PrintDialog import PrintDialogHandler
from utils import hasAction, fencemsg, aggiorna, updateScadenzePromemoria,\
         setconf, dateTimeToString, dateToString, \
         orda, posso, messageInfo, installId , YesNoDialog
from utilsCombobox import *
from ParametriFrame import ParametriFrame
from SetConf import SetConfUI
from AnagraficaPrincipaleFrame import AnagrafichePrincipaliFrame
#from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.dao.VariazioneListino import VariazioneListino
from ConfiguraWindow import ConfiguraWindow
from promogest.ui.PanUi import PanUi, checkPan
from promogest.ui.AzioniVelociNotebookPage import AzioniVelociNotebookPage
from promogest.ui.NewsNotebookPage import NewsNotebookPage
from promogest.ui.CalendarNotebookPage import CalendarNotebookPage
from promogest.ui.NotificaAllarmiNotebookPage import NotificaAllarmiNotebookPage

#inizializzano il customwidget
from widgets.ArticoloSearchWidget import ArticoloSearchWidget
from widgets.ClienteSearchWidget import ClienteSearchWidget
from widgets.FornitoreSearchWidget import FornitoreSearchWidget
from widgets.PersonaGiuridicaSearchWidget import PersonaGiuridicaSearchWidget
if posso("GN"):
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio \
                            import TestataGestioneNoleggio
try:
    from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False


class Main(GladeWidget):

    def __init__(self, aziendaStr, anagrafiche_modules, parametri_modules,
                anagrafiche_dirette_modules, frame_modules, permanent_frames):

        GladeWidget.__init__(self, 'main_window')
        self.main_window.set_title('*** PromoGest2 *** Azienda : '+aziendaStr+\
                                '  *** Utente : '+\
                                Environment.params['usernameLoggedList'][1]+\
                                ' ***')
        self.aziendaStr = aziendaStr
        self.statusBarHandler()
        for filename in glob.glob(Environment.promogestDir+\
                                                    "temp"+os.sep+'*.cache'):
            try:
                os.remove(filename)
            except:
                pass
        Environment.windowGroup.append(self.getTopLevel())
        self.anagrafiche_modules = anagrafiche_modules
        self.parametri_modules = parametri_modules
        self.anagrafiche_dirette_modules=anagrafiche_dirette_modules
        self.frame_modules = frame_modules
        self.permanent_frames = permanent_frames
        self.currentFrame = None
        self.alarmFrame = None
        self.shop = Environment.shop
        self.creata = False
        if posso("SD"):
            self.sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo =="client":
            self.master_sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo =="server":
            self.client_sincro_db.destroy()
        if Environment.tipodb =="postgresql":
#            self.whatcant_button.destroy()
            self.test_promowear_button.destroy()
            self.test_promoshop_button.destroy()
        self.addNoteBookPage()
        self.updates()

    def show(self):
        """ Visualizza la finestra
        """
        #documenti_image = self.documenti_image.get_image()
        self.anno_lavoro_label.set_markup('<b>Anno di lavoro:   ' + \
                                        Environment.workingYear + '</b>')
        model = self.iconview_listore
        model.append([3, "Documenti\n(Fatture,DDT\nPreventivi)",
                        self.documenti_image.get_pixbuf(), None])
        model.append([4, "Prima Nota",
                        self.primanota_image.get_pixbuf(), None])
        model.append([5, "Promemoria",
                        self.promemoria_image.get_pixbuf(), None])
        model.append([10, "Gestione\nCommesse",
                        self.gest_commesse_image.get_pixbuf(), None])

        # right vertical icon list  adding modules
#        model_right = gtk.ListStore(int, str, gtk.gdk.Pixbuf, object)
        ind = 6
        for mod in self.anagrafiche_dirette_modules.keys():
            currModule = self.anagrafiche_dirette_modules[mod]
            if self.shop and currModule["module"].VIEW_TYPE[1] =="Vendita Dettaglio":
                anag = currModule["module"].getApplication()
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                #icon_view.unselect_all()
                return
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model.append(row)
            ind += 1
        for mod in self.frame_modules.keys():
            currModule = self.frame_modules[mod]
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row =(ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model.append(row)
            ind += 1

        self.main_iconview.set_model(model)
        self.main_iconview.set_text_column(1)
        self.main_iconview.set_pixbuf_column(2)
        #self.main_iconview.connect('selection-changed',
                                   #self.on_main_iconview_select, model)

        self.main_iconview.set_columns(1)
        self.main_iconview.set_item_width(95)
        self.main_iconview.set_size_request(115, -1)

        if self.currentFrame is None:
#            self.main_hbox.remove(self.box_immagini_iniziali)
            self._refresh()
        self.setModulesButtons()
        self.placeWindow(self.main_window)
        self.main_window.show_all()
        self.on_button_refresh_clicked()

    def updates(self):
        """ Aggiornamenti e controlli da fare all'avvio del programma
        """
        #Aggiornamento scadenze promemoria
        if posso("PR"):
            print "VERIFICA DEI PROMEMORIA IN SCADENZA"
            updateScadenzePromemoria()

    def _refresh(self):
        """
        Update the window, setting the appropriate frame
        """
        self.main_iconview.unselect_all()
        self.main_hbox.show_all()

    def on_button_help_clicked(self, button):
        sendemail = SendEmail()

    def on_button_refresh_clicked(self, widget=None):
#        if WEBKIT:
#            self.create_planning_frame()
        if self.creata:
            self.main_notebook.remove_page(0)
#           self.creata = False
        self._refresh()

    def on_main_iconview_select(self, icon_view, model=None):

        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = self.iconview_listore[i][0]

        if selection == 3:
            #self.currentFrame = self.create_registrazioni_frame()
            # Andrea
            # richiamo diretto dei documenti: evita di dover premere il
            # pulsante nel frame registrazioni
            if not hasAction(actionID=2):
                return
            from AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 4:
            if not hasAction(actionID=2):
                return
            from promogest.modules.PrimaNota.ui.AnagraficaPrimaNota import AnagraficaPrimaNota
            anag = AnagraficaPrimaNota(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 5:
            if posso("PR"):
                from AnagraficaPromemoria import AnagraficaPromemoria
                anag = AnagraficaPromemoria(self.aziendaStr)
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                icon_view.unselect_all()
                return
            else:
                fencemsg()
        elif selection == 10: #gestione commessa
#            messageInfo(msg="""RICORDIAMO CHE QUESTO MODULO E' ANCORA IN FASE DI TEST """)
#            if posso("GC"):
            from promogest.modules.GestioneCommesse.ui.AnagraficaCommesse import AnagraficaCommesse
            anag = AnagraficaCommesse(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        else:
            i = selected[0][0]
            selection = self.iconview_listore[i][0]
            module = self.iconview_listore[i][3]

            if self.currentFrame is not None:
                self.main_hbox.remove(self.currentFrame)
                self.currentFrame.destroy()
                self.currentFrame = None
            if module.VIEW_TYPE[0] == 'anagrafica_diretta':
                anag = module.getApplication()
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                icon_view.unselect_all()
                return
            elif module.VIEW_TYPE[0] == 'frame':
                frame = module.getApplication()
                self.currentFrame = frame.getTopLevel()
        self.main_notebook.set_current_page(0)
        self._refresh()

    def setModulesButtons(self):

        if self.anagrafiche_modules is not None:
            for module in self.anagrafiche_modules.iteritems():
                module_button = gtk.Button()
                module_butt_image = gtk.Image()
                module_butt_image.set_from_file(module[1]['guiDir']+'/'+module[1]['module'].VIEW_TYPE[2])
                module_button.set_image(module_butt_image)
                module_button.set_label(module[1]['module'].VIEW_TYPE[1])
                module_button.connect('clicked', self.on_module_button_clicked)
                self.anagrafiche_moduli_vbox.pack_start(module_button, False, False)
            return
        else:
            return

    def on_module_button_clicked(self, button):
        label = button.get_label()
        for mk in self.anagrafiche_modules.iteritems():
            module = mk[1]['module']
            if label == module.VIEW_TYPE[1]:
                #chiave di tutto il richiamo di passaggio alla classe in module.py che poi fa la vera istanza"
                anag = module.getApplication()
                showAnagrafica(self.getTopLevel(), anag, button=None, mainClass=self)

    def on_articoli_button_clicked(self, toggleButton):
        if not hasAction(actionID=2):
            return
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(aziendaStr=Environment.azienda)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_forniture_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaForniture import AnagraficaForniture
        anag = AnagraficaForniture(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_vettori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_agenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("AG"):
            from promogest.modules.Agenti.ui.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_active(False)

    def on_categorie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
        anag = AnagraficaCategorieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_famiglie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
        anag = AnagraficaFamiglieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieClienti import AnagraficaCategorieClienti
        anag = AnagraficaCategorieClienti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
        anag = AnagraficaCategorieFornitori()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_utenti_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.AnagraficaUtenti import AnagraficaUtenti
            anag = AnagraficaUtenti()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active', False)

    def on_ruoli_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.AnagraficaRuoli import AnagraficaRuoli
            anag = AnagraficaRuoli()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active', False)

    def on_ruoli_azioni_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if posso("RA"):
            from promogest.modules.RuoliAzioni.ui.ManageRoleAction import ManageRuoloAzioni
            anag = ManageRuoloAzioni()
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_property('active', False)

    def on_multipli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_pagamenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaPagamenti import AnagraficaPagamenti
        anag = AnagraficaPagamenti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_banche_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaBanche import AnagraficaBanche
        anag = AnagraficaBanche()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_contatti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from promogest.modules.Contatti.ui.AnagraficaCategorieContatti import AnagraficaCategorieContatti
        anag = AnagraficaCategorieContatti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_aliquote_iva_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaAliquoteIva import AnagraficaAliquoteIva
        anag = AnagraficaAliquoteIva()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_imballaggi_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from AnagraficaImballaggi import AnagraficaImballaggi
        anag = AnagraficaImballaggi()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_stadio_commessa_button_toggled(self, toggleButton):

        if toggleButton.get_property('active') is False:
            return
#        if posso("GC"):
#        messageInfo(msg="""RICORDIAMO CHE QUESTO MODULO E' ANCORA IN FASE DI TEST """)
        from promogest.modules.GestioneCommesse.ui.AnagraficaStadioCommessa import AnagraficaStadioCommessa
        anag = AnagraficaStadioCommessa()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_main_iconview_right_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = model[i][0]
        module = model[i][3]

        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
            self.currentFrame.destroy()
            self.currentFrame = None
        if module.VIEW_TYPE[0] == 'anagrafica_diretta':
            anag = module.getApplication()
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif module.VIEW_TYPE[0] == 'frame':
            frame = module.getApplication()
            self.currentFrame = frame.getTopLevel()
##            icon_view.unselect_all()
        self._refresh()

    # INIZIO CREAZIONE FRAME


    def create_main_window_frame(self):
#        if self.currentFrame is not None:
#            self.main_hbox.remove(self.currentFrame)
        frame = VistaPrincipale(self, self.aziendaStr)
#        return frame.vista_principale_frame
        return frame

    def create_anagrafiche_principali_frame(self):
        if not hasAction(actionID=11):return
#        if self.currentFrame is not None:
#            self.main_hbox.remove(self.currentFrame)
        frame = AnagrafichePrincipaliFrame(self.main_window, self.aziendaStr, modules=self.anagrafiche_modules)
        return frame.getTopLevel()

    def create_registrazioni_frame(self):
        if not hasAction(actionID=2):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = RegistrazioniFrame(self.main_window, self.aziendaStr)
        return frame.getTopLevel()

    def create_parametri_frame(self):
        if not hasAction(actionID=6):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = ParametriFrame(self.main_window, self.aziendaStr, modules=self.parametri_modules)
        return frame.getTopLevel()

    # FINE CREAZIONE FRAME

    def on_configurazione_menu_activate(self, widget):
        if not hasAction(actionID=14):return
        configuraWindow = ConfiguraWindow(self)
#        configuraWindow = SetConfUI(self)
        showAnagrafica(self.getTopLevel(), configuraWindow)

    def on_dati_azienda_activate(self, widget):
        from AnagraficaAziende import AnagraficaAziende
        anag =AnagraficaAziende(self)
        showAnagrafica(self.getTopLevel(), anag)

    def on_importa_modulo_activate(self, widget):
        return
        fileDialog = gtk.FileChooserDialog(title='Importazione modulo',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_OK,
                                                    gtk.RESPONSE_OK),
                                           backend=None)
        fltr = gtk.FileFilter()
        fltr.add_pattern('*.pg2')
        fltr.set_name('File Pg2 (*.pg2)')
        fileDialog.add_filter(fltr)
        fltr = gtk.FileFilter()
        fltr.add_pattern('*')
        fltr.set_name('Tutti i file')
        fileDialog.add_filter(fltr)
        n = ""
        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            f = open(filename)
            r = f.readline()
            al = f.readlines()
            for a in al:
                if "MODULES_NAME" in a:
                    n = a.split("=")[1].strip()[1:-1]
                    break
                else:
                    continue
            c = Environment.PRODOTTO.strip()
            v = Environment.VERSIONE.strip()
            p = hashlib.sha224(n+c+v).hexdigest()
            if p.strip()==r.strip():
                pa = os.path.join(Environment.cartella_moduli,n+"/"+"module.py")
                g = file(pa,"w")
                for a in al:
                    g.write(a)
                g.close()
                f.close()
                msg = "MODULO CORRETTAMENTE INSTALLATO, CHIUDERE L'APPLICAZIONE\nED AGGIUNGERE I PARAMETRI NECESSARI\n"
            else:
                msg ="ATTENZIONE, MODULO NON INSTALLATO, CORROTTO O NON CORRETTO, CONTATTARE L'ASSISTENZA"
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
                #self.path_file_entry.set_text(filename)
            fileDialog.destroy()

    def on_credits_menu_activate(self, widget):
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == gtk.RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_inserimento_codice_activate(self,widget):
        from promogest.dao.Setconf import SetConf
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
        dialog.set_markup("""<b>                CODICE ATTIVAZIONE PACCHETTO               </b>""")
        hbox = gtk.HBox()
        entry___ = gtk.Entry()

        label = gtk.Label()
        label.set_markup("<b>   Inserisci codice   </b>")
        hbox.pack_start(label)
        hbox.pack_start(entry___)
        dialog.vbox.pack_start(hbox)
        dialog.show_all()
        response = dialog.run()
        codice = entry___.get_text()
#        hascode = str(hashlib.sha224(codice+orda(codice)).hexdigest())
        if "cl" and "|" in codice :
            d = codice.split("|")
            if d[1] == "azienda":
                if Environment.tipodb == "sqlite":
                    from promogest.dao.Azienda import Azienda
                    oldnomeazienda= d[2]
                    newnameazienda = d[3]
                    aa = Azienda().select(schemaa = oldnomeazienda)
                    if aa:
                        aa[0].schemaa = newnameazienda.strip()
                        aa[0].persist()
                        messageInfo(msg="NOME AZIENDA MODIFICATO")
                        dialog.destroy()
                        return
                    else:
                        messageInfo(msg="VECCHIO NOME AZIENDA NON TROVATO")
                        dialog.destroy()
                        return
                    return
                else:
                    messageInfo(msg="POSSIBILE SOLO CON LA VERSIONE ONE")
                    dialog.destroy()
                    return
            elif d[1] == "modulo":
                tipo_section = d[2] #Modulo
                section = d[3] # Inventario
                description = str(d[4]) or "" #Gestione inventario
                tipo = d[5] or None # Niente o BOOLEAN o colore
                active = bool(d[6]) or True # bool
                visible = bool(d[7]) or True #bool
                key = d[8]  # mod_enable
                value = d[9] # yes or no
                if section not in Environment.modules_folders:
                    messageInfo(msg="ERRORE ATTIVAZIONE MODULO")
                    return
                dao = SetConf().select(key=key,section=section)
                if dao:
                    d = dao[0]
                else:
                    d = SetConf()
                d.key = key
                d.value =value
                d.section = section
                d.description = description
                d.tipo_section = tipo_section
                d.tipo = tipo
                d.active = active
                d.visible = visible
                d.date = datetime.datetime.now()
                d.persist()
                messageInfo(msg="MODULO O OPZIONE MODIFICATO attivato o disattivato")
                dialog.destroy()
                return
            elif d[1] =="registro":
                operazione = d[2].strip()+".registro"
                registro_da_assegnare = d[3]
                from promogest.dao.Setting import Setting
                a = Setting().getRecord(id=operazione)
                if a:
                    b = Setting().select(value=registro_da_assegnare)
                    if b:
                        a.value = registro_da_assegnare
                        a.persist()
                        messageInfo(msg="REGISTRO NUMERAZIONE MODIFICATO\n\nRIAVVIARE")
                        dialog.destroy()
                        return True
                    else:
                        messageInfo(msg="REGISTRO DA ASSEGNARE NON TROVATO O CORRETTO\n\n RIPROVARE")
                        return False
                else:
                    messageInfo(msg="OPERAZIONE NON CORRETTA E NON TROVATA\n\nRIPROVARE")
                    return False
        else:
            sets = SetConf().select(key="install_code",section="Master")
            if sets:
                sets[0].delete()
            if codice:
                k = SetConf()
                k.key = "install_code"
                k.value =str(hashlib.sha224(codice+orda(codice)).hexdigest())
                k.section = "Master"
                k.description = "codice identificativo della propria installazione"
                k.tipo_section = "General"
                k.tipo = "ONE"
                k.active = True
                k.date = datetime.datetime.now()
                k.persist()
        dialog.destroy()


    def on_licenza_menu_activate(self, widget):
        licenzaDialog = GladeWidget('licenza_dialog', callbacks_proxy=self)
        licenzaDialog.getTopLevel().set_transient_for(self.getTopLevel())
        licenseText = ''
        try:
            lines = open('./LICENSE').readlines()
            for l in lines:
                licenseText += l
        except:
            licenseText = 'Lavori in corso ....'
            print 'License file not found (LICENSE).'
        textBuffer = licenzaDialog.licenza_textview.get_buffer()
        textBuffer.set_text(licenseText)
        licenzaDialog.licenza_textview.set_buffer(textBuffer)
        licenzaDialog.getTopLevel().show_all()
        response = licenzaDialog.licenza_dialog.run()
        if response == gtk.RESPONSE_OK:
            licenzaDialog.licenza_dialog.destroy()

    def on_manuale_online_activate(self, widget):
        url ="http://help.promotux.it"
        webbrowser.open_new_tab(url)

    def on_aggiorna_activate(self, widget):
        aggiorna(self)

    def on_Back_up_Database_activate(self, widget):
        """ Si prepara un file zip con il dump del DB """

        if Environment.tipodb == "sqlite":
            msg = """NELLA VERSIONE LITE IL BACKUP SI
EFFETTUA COPIANDO IL FILE db CHE SI TROVA NELLA CARTELLA
promogest2 IN /HOME/NOMEUTENTE/ O IN C:/UTENTI/NOMEUTENTE"""
            messageInfo(msg= msg)
        else:
            st= Environment.startdir()
            nameDump = "promoGest2_dump_"+self.aziendaStr+"_"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
            msgg = """Il "dump" del database verrà salvato in

    %s
    ed avrà il nome

    %s.zip

    ATTENZIONE!!!! la procedura potrebbe richiedere diversi minuti.""" %(st, nameDump)
            messageInfo(msg= msgg, transient=self.getTopLevel())
            #if response == gtk.RESPONSE_OK:
            st= Environment.startdir()

            stname = st+nameDump
            os.environ["PGPASSWORD"]=Environment.password
            retcode = call(["pg_dump",
                            "-h",Environment.host,
                            "-p",Environment.port,
                            "-U",Environment.user,
                            "-Z","7",
                            "-f",stname,
                            Environment.database])

            Environment.pg2log.info("STO EFFETTUANDO UN BACKUP DEL FILE %s" %stname)
            #print "YYYYYYYYYYYYYYYYYY", retcode
            if not retcode:
                #zfilename = nameDump +".zip"
                #zout = zipfile.ZipFile(str(stname) +".zip", "w")
                #zout.write(stname,zfilename,zipfile.ZIP_DEFLATED)
                #zout.close()
                Environment.pg2log.info("DUMP EFFETTUATO CON SUCCESSO")
                #os.remove(stname)
            else:
                Environment.pg2log.info("ATTENZIONE DUMP NON RIUSCITO")

    def on_pan_active_clicked(self, button):
#        if not hasAction(actionID=14):return
        configuraWindow = PanUi(self)
        showAnagrafica(self.getTopLevel(), configuraWindow)


    def on_seriale_menu_activate(self, widget):
        from promogest.dao.Setconf import SetConf
        try:
            data = SetConf().select(key="install_code",section="Master")
            codice = data[0].value
            msg = 'Codice installazione:\n\n' + str(codice)
        except:
            msg = 'Impossibile generare il codice !!!'
        messageInfo(msg= msg, transient=self.getTopLevel())

    def on_send_Email_activate(self, widget):
        sendemail = SendEmail()

    def on_master_sincro_db_activate(self, widget):
        msg ="SERVER NON ANCORA IMPLEMENTATO"
        messageInfo(msg= msg, transient=self.getTopLevel())

    def on_client_sincro_db_activate(self, widget):
        if posso("SD") and Environment.conf.SincroDB.tipo =="client":
            from promogest.modules.SincroDB.ui.SincroDB import SincroDB
            anag = SincroDB()
            showAnagrafica(self.getTopLevel(), anag)
        else:
            print "PASSIQUI"

    def on_test_promowear_button_clicked(self, button):
        msg = """ATTENZIONE!!
QUESTA FUNZIONALITÀ È STATA AGGIUNTA PER
PERMETTERE DI PROVARE IL PROMOGEST ONE BASIC CON
IL MODULO TAGLIA E COLORE PROMOWEAR
QUESTO MODULO SERVE A CHI DEVE GESTIRE
UNA ATTIVITÀ CHE MOVIMENTA E VENDE
ABBIGLIAMENTO O CALZATURE.
L'OPERAZIONE È IRREVERSIBILE,AGGIUNGE DIVERSE
TABELLE NEL DATABASE E NUOVE INTERFACCE UTENTE
DEDICATE,NON CAUSA PERDITA DI DATI
MA NON È CONSIGLIATO FARLO SE NON
NE AVETE BISOGNO

Procedere all'installazione del modulo PromoWear? """
        if not YesNoDialog(msg=msg, transient=self.getTopLevel()):
            return
        if not hasattr(Environment.conf,"PromoWear"):
            Environment.conf.add_section("PromoWear")
            Environment.conf.save()
            Environment.conf.PromoWear.primoavvio = "yes"
            Environment.conf.PromoWear.mod_enable = "yes"
            Environment.conf.save()
            tables = [t.name for t in Environment.params["metadata"].sorted_tables]
            if "colore" not in tables and "taglia" not in tables:
                from promogest.modules.PromoWear.data.PromoWearDB import *
                msg = " TABELLE AGGIUNTE, RIAVVIARE IL PROGRAMMA "
                messageInfo(msg=msg)
        else:
            msg= "PULSANTE DI TEST GIA' PREMUTO"
            messageInfo(msg=msg, transient=self.getTopLevel())


    def on_test_promoshop_button_clicked(self, button):
        from promogest.dao.Setconf import SetConf
        msg = """ATTENZIONE!!
QUESTA FUNZIONALITÀ È STATA AGGIUNTA PER
PERMETTERE DI PROVARE IL PROMOGEST ONE BASIC CON
IL MODULO VENDITA DETTAGLIO

Procedere all'installazione del modulo PromoShop? """
        if not YesNoDialog(msg=msg, transient=self.getTopLevel()):
            return
        if not setconf("VenditaDettaglio", "mod_enable"):
            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "Modulo Vendita Dettaglio"
            a.tipo = "bool"
            a.key = "mod_enable"
            a.value = "yes"
            a.persist()

            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "Nome del movimento generato"
            a.tipo = "str"
            a.key = "operazione"
            a.value = "Scarico venduto da cassa"
            a.persist()

            a = SetConf()
            a.section = "VenditaDettaglio"
            a.tipo_section ="Modulo"
            a.description = "disabilita_stampa"
            a.tipo = "bool"
            a.key = "disabilita_stampa"
            a.value = "True"
            a.active = True
            a.persist()
            #tables = [t.name for t in Environment.params["metadata"].sorted_tables]
            #if "testata_scontrino" not in tables:
                #from promogest.modules.VenditaDettaglio.data.VenditaDettaglioDB import *
                #msg = " TABELLE AGGIUNTE, RIAVVIARE IL PROGRAMMA "
                #messageInfo(msg=msg)
        else:
            messageInfo(msg="RISULTA GIA' ATTIVATO")

    def on_ricmedio_activate(self, widget):
        """ entry Menu statistiche Ricarico medio """
        from promogest.modules.Statistiche.ui.StatisticaGenerale import StatisticaGenerale
        anag = StatisticaGenerale(idMagazzino=None, nome="RICARICO MEDIO e INFLUENZA SULLE VENDITE")
        anagWindow = anag.getTopLevel()

    def on_controllo_fatturato_activate(self, widget):
        print "CONTROLLO FATTURATO NON GESTITO"

    def on_whatcant_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/whatCanT"
        webbrowser.open_new_tab(url)

    def on_export_magazzino_activate(self, button):
        from promogest.modules.Statistiche.ui.StatisticheMagazzino import StatisticheMagazzino
        anag = StatisticheMagazzino(idMagazzino=None)
        anagWindow = anag.getTopLevel()

    def on_main_window_key_press_event(self, widget, event):
        on_main_window_key_press_eventPart(self,widget, event)

    def on_disconnect(self, widget=None):
        if YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            self.destroy()
        else:
            return

    def on_quit(self, widget=None):
        if YesNoDialog(msg='Confermi la chiusura?', transient=self.getTopLevel()):
            self.hide()
            gtk.main_quit()
        else:
            return


    def addNoteBookPage(self):

        if WEBKIT:
            self.nn = NewsNotebookPage(self, self.aziendaStr).draw()
            n = gtk.Label()
            n.set_markup("<b>NEWS/A.VEL</b>")
            ind = self.main_notebook.append_page(self.nn.notizie_frame, n)
            self.main_notebook.set_current_page(ind)

        self.pp = checkPan(self)

        self.elenco_magazzini_page = ElencoMagazzini(self, self.aziendaStr).draw()
        self.main_notebook.append_page(self.elenco_magazzini_page.elenco_magazzini_frame, self.elenco_magazzini_page.magazzini_label)

        self.elenco_listini_page = ElencoListini(self, self.aziendaStr).draw()
        self.main_notebook.append_page(self.elenco_listini_page.elenco_listini_frame,self.elenco_listini_page.elenco_listini_label)

        self.calendar_page = CalendarNotebookPage(self, self.aziendaStr).draw()
        calendar_page_label = gtk.Label()
        calendar_page_label.set_markup("<b>CALENDARIO</b>")
        self.main_notebook.append_page(self.calendar_page.calendario_frame, calendar_page_label)

        self.notifica_allarmi = NotificaAllarmiNotebookPage(self, self.aziendaStr)
        notifica_allarmi_label = gtk.Label()
        notifica_allarmi_label.set_markup("<b>NOTIFICA ALLARMI</b>")
        self.main_notebook.append_page(self.notifica_allarmi.notifica_allarmi_frame, notifica_allarmi_label)

#        azioni_veloci_page = AzioniVelociNotebookPage(self, self.aziendaStr).draw()
#        self.azioni_veloci_page = azioni_veloci_page
#        azioni_veloci_page_label = gtk.Label()
#        azioni_veloci_page_label.set_markup("<b>AZIONI VELOCI</b>")
#        self.main_notebook.append_page(azioni_veloci_page.azioni_veloci_frame, azioni_veloci_page_label)


    def statusBarHandler(self):
        textStatusBar = "    PromoGest2 - 070 8649705 - www.promogest.me - info@promotux.it     "
        context_id =  self.pg2_statusbar.get_context_id("main_window")
        self.pg2_statusbar.push(context_id,textStatusBar)

        if Environment.rev_locale < Environment.rev_remota:
            self.active_img.set_from_file("gui/active_off.png")
            self.aggiornamento_label.set_label("DA AGGIORNARE!!! ")
        else:
            self.active_img.set_from_file("gui/active_on.png")
            self.aggiornamento_label.set_label("AGGIORNATO ")

class MainWindowFrame(VistaPrincipale):
    def __init__(self, mainWindow, azs):
        VistaPrincipale.__init__(self, self.mainWindow, azs)


class RegistrazioniFrame(GladeWidget):
    """ Frame per la gestione delle registrazioni """

    def __init__(self, mainWindow,azs):
        self.mainWindow = mainWindow
        self.aziendaStr = azs
        GladeWidget.__init__(self, 'registrazioni_select_frame', fileName='_registrazioni_select.glade')

    def on_documenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=2):return
        from AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)

def on_anagrafica_destroyed(anagrafica_window, argList):
    mainWindow = argList[0]
    anagraficaButton= argList[1]
    mainClass = argList[2]
    if anagrafica_window in Environment.windowGroup:
        Environment.windowGroup.remove(anagrafica_window)
    if anagraficaButton is not None:
        anagraficaButton.set_active(False)
    if mainClass is not None:
        mainClass.on_button_refresh_clicked()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button, mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
    anagWindow.set_transient_for(window)
#    setattr(anagWindow, "mainClass",mainClass)
    anagWindow.show_all()
