# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

import sys
import hashlib
import os
from datetime import datetime
import webbrowser
from  subprocess import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.ElencoMagazzini import ElencoMagazzini
from promogest.ui.ElencoListini import ElencoListini
from promogest.ui.VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from promogest.lib.utils import hasAction, fencemsg, setconf,  \
         orda, posso, messageInfo, YesNoDialog, messageError,\
         obligatoryField, leggiRevisioni
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *
from ParametriFrame import ParametriFrame
from AnagraficaPrincipaleFrame import AnagrafichePrincipaliFrame

#ATTENZIONE: tenere perchè servono a caricare i dao nel giusto ordine
from promogest.dao.VariazioneListino import VariazioneListino
from promogest.dao.AnagraficaSecondaria import AnagraficaSecondaria_
from promogest.modules.GestioneFile.dao.Immagine import ImageFile
from promogest.dao.UtenteImmagine import UtenteImmagine
from promogest.modules.GestioneFile.dao.ArticoloImmagine import ArticoloImmagine
from promogest.modules.GestioneFile.dao.SlaFile import SlaFile
from promogest.dao.SlaFileImmagine import SlaFileImmagine
from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.modules.GestioneCommesse.dao.RigaCommessa import RigaCommessa

from promogest.ui.ConfiguraWindow import ConfiguraWindow
from promogest.ui.PanUi import PanUi, checkPan
#from promogest.ui.AzioniVelociNotebookPage import AzioniVelociNotebookPage
from promogest.ui.NewsNotebookPage import NewsNotebookPage
from promogest.ui.CalendarNotebookPage import CalendarNotebookPage
from promogest.ui.NotificaAllarmiNotebookPage import NotificaAllarmiNotebookPage
from promogest.ui.ScadenzarioNotebookPage import ScadenzarioNotebookPage

#inizializzano il customwidget
from promogest.ui.widgets.ArticoloSearchWidget import ArticoloSearchWidget
from promogest.ui.widgets.ClienteSearchWidget import ClienteSearchWidget
from promogest.ui.widgets.FornitoreSearchWidget import FornitoreSearchWidget
from promogest.ui.widgets.PersonaGiuridicaSearchWidget import PersonaGiuridicaSearchWidget
from promogest.ui.UpdateDialog import UpdateDialog
if posso("GN"):
    from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio \
                            import TestataGestioneNoleggio
try:
    from  xhtml2pdf import pisa
except:
    messageError(msg=_("ATTENIONE! modulo xhtml2pdf mancante,\n qualcosa non ha funzionato nell'installazione?"))

from promogest.dao.Setconf import SetConf

try:
    if Environment.pg3:
        from gi.repository.WebKit import WebView
    else:
        from webkit import WebView
    WEBKIT = True
except:
    WEBKIT = False


#from sqlalchemy import MetaData
#from sqlalchemy_schemadisplay import create_schema_graph

## create the pydot graph object by autoloading all tables via a bound metadata object
#graph = create_schema_graph(metadata=Environment.meta,
   #show_datatypes=True, # The image would get nasty big if we'd show the datatypes
   #show_indexes=True, # ditto for indexes
   #rankdir='LR', # From left to right (instead of top to bottom)
   #concentrate=True # Don't try to join the relation lines together
#)
#graph.write_png('dbschema.png') # write out the file


#from promogest.dao.Articolo import Articolo
#from sqlalchemy_schemadisplay import create_uml_graph
#from sqlalchemy.orm import class_mapper

## lets find all the mappers in our model
#mappers = []
#for attr in dir(Articolo):
    #print "AAAAAAAAAAAATRRR", attr
    #if attr[0] == '_': continue
    #try:
        #cls = getattr(Articolo, attr)
        #mappers.append(class_mapper(cls))
    #except:
        #pass

## pass them to the function and set some formatting options
#graph = create_uml_graph(mappers,
    #show_operations=False, # not necessary in this case
    #show_multiplicity_one=False # some people like to see the ones, some don't
#)
#graph.write_png('schema.png') # write out the file

class Main(GladeWidget):

    def __init__(self, aziendaStr, anagrafiche_modules, parametri_modules,
                anagrafiche_dirette_modules, frame_modules, permanent_frames):

        GladeWidget.__init__(self, root= 'main_window', path="main_window.glade")
        welcome_str = _("Benvenuto {0} ({1})!".format(Environment.params['usernameLoggedList'][1],
            aziendaStr))
        self.welcome_label.set_text(welcome_str)
        self.aziendaStr = aziendaStr
        self.statusBarHandler()
        #for filename in glob.glob(Environment.promogestDir + \
                                                    #"temp" + \
                                                    #os.sep + \
                                                    #'*.cache'):
            #try:
                #os.remove(filename)
            #except:
                #pass
        Environment.windowGroup.append(self.getTopLevel())
        self.anagrafiche_modules = anagrafiche_modules
        self.parametri_modules = parametri_modules
        self.anagrafiche_dirette_modules = anagrafiche_dirette_modules
        self.frame_modules = frame_modules
        self.permanent_frames = permanent_frames
        self.currentFrame = None
        self.alarmFrame = None

        self.creata = False
        if posso("SD"):
            self.sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo == "client":
            self.master_sincro_db.destroy()
        elif posso("SD") and \
                            Environment.conf.SincroDB.tipo == "server":
            self.client_sincro_db.destroy()
        if Environment.tipodb == "postgresql":
#            self.whatcant_button.destroy()
            self.test_promowear_button.destroy()
            self.test_promoshop_button.destroy()
        self.addNoteBookPage()
        self.updates()

    def show(self):
        """ show the main windows program
        """
        #documenti_image = self.documenti_image.get_image()
        model = self.iconview_listore
        model.append([3, _("Documenti\n(Fatture,DDT\nPreventivi)"),
                        self.documenti_image.get_pixbuf(), None])
        model.append([4, _("Prima Nota"),
                        self.primanota_image.get_pixbuf(), None])
        model.append([5, _("Promemoria"),
                        self.promemoria_image.get_pixbuf(), None])
        model.append([10, _("Gestione\nCommesse"),
                        self.gest_commesse_image.get_pixbuf(), None])

        # right vertical icon list  adding modules
#        model_right = gtk.ListStore(int, str, gtk.gdk.Pixbuf, object)
        ind = 6
        for mod in self.anagrafiche_dirette_modules:
            currModule = self.anagrafiche_dirette_modules[mod]
            from promogest.preEnv import shop
            if shop \
                and currModule["module"].VIEW_TYPE[1] == "Vendita Dettaglio":
                anag = currModule["module"].getApplication()
                from promogest.modules.VenditaDettaglio.ui.AnagraficaVenditaDettaglio import showAnagrafica
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                #icon_view.unselect_all()
                return
            pbuf = GDK_PIXBUF_NEW_FROM_FILE(currModule['guiDir'] \
                                    + currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1],
                                            pbuf, currModule['module'])
            model.append(row)
            ind += 1
        for mod in self.frame_modules:
            currModule = self.frame_modules[mod]
            pbuf = GDK_PIXBUF_NEW_FROM_FILE(currModule['guiDir'] \
                                    + currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1],
                                            pbuf, currModule['module'])
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
        self.main_window.show()
        self.on_button_refresh_clicked()

        fillComboboxRole(self.anag_minori_combobox, noAdmin=True)

        # conf_timeout = SetConf().select(key="updates_timeout",
#                                                        section="General")
        # timeout = '300'
        # if not conf_timeout:
            # conf_timeout = SetConf()
            # conf_timeout.key = "updates_timeout"
            # conf_timeout.value = '300'
            # conf_timeout.section = "General"
            # conf_timeout.tipo_section = "Generico"
            # conf_timeout.description = "intervallo controllo aggiornamenti"
            # conf_timeout.active = True
            # conf_timeout.tipo = "str"
            # conf_timeout.date = datetime.datetime.now()
            # Environment.session.add(conf_timeout)
        # else:
            # timeout = conf_timeout[0].value

        def update_timer():
            leggiRevisioni()
            if Environment.rev_locale < Environment.rev_remota:
                self.active_img.set_from_file("gui/active_off.png")
                # self.aggiornamento_label.set_label(_("DA AGGIORNARE!!! "))
            else:
                self.active_img.set_from_file("gui/active_on.png")
                # self.aggiornamento_label.set_label(_("AGGIORNATO "))
            return True
        #if timeout >= 300:
        glib.timeout_add_seconds(600, update_timer)

        def pulizia_lottotemp():
            ltemp = setconf("Documenti", "lotto_temp")
            if not ltemp:
                return
            from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
            from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
            from promogest.dao.Fornitura import Fornitura
            print "Avvio pulizia lotti temp..."
            lt = NumeroLottoTemp().select(batchSize=None)
            n = len(lt)
            g = 0
            for l in lt:
                print "RESIDUI DA ELABORARE", n-lt.index(l)
                rmf =  RigaMovimentoFornitura().select(idRigaMovimentoVendita=l.id_riga_movimento_vendita_temp)
                if not rmf:
                    #cerchiamo una fornitura precisa
                    daoForn = Fornitura().select(idArticolo=l.rigamovventemp.id_articolo,
                                            numeroLotto = l.lotto_temp,
                                            batchSize = None)

                    if daoForn:
                        a = RigaMovimentoFornitura()
                        a.id_articolo = l.rigamovventemp.id_articolo
                        a.id_riga_movimento_vendita = l.id_riga_movimento_vendita_temp
                        a.id_fornitura = daoForn[0].id
                        Environment.params["session"].add(a)
                        Environment.params["session"].delete(l)
                        g += 1
                        if g == 2000:
                            Environment.params["session"].commit()
                            g = 0
                else:
                    Environment.params["session"].delete(l)
            Environment.params["session"].commit()
        #pulizia_lottotemp()

        def pickle_meta():
            from pickle import dump
            meta_pickle = self.aziendaStr + "_meta_pickle"+sys.version[:1]
            if not os.path.exists(os.path.join(Environment.SRC_PATH,
                                                meta_pickle)):
                with open(os.path.join(Environment.SRC_PATH,
                                        meta_pickle), 'wb') as f:
                    dump(Environment.meta, f)
        pickle_meta()

   # ATTENZIONE: Tutto il codice di cambio IVA è stato spostato in __init__.py

    def updates(self):
        """ Aggiornamenti e controlli da fare all'avvio del programma
        TODO: it needs some work and maybe threads

        """
        from promogest.dao.Promemoria import updateScadenzePromemoria
        if posso("PR"):
            glib.timeout_add_seconds(20, updateScadenzePromemoria)

    def _refresh(self):
        """ Update the window, setting the appropriate frame

        """
        self.main_iconview.unselect_all()
        self.main_hbox.show_all()

    def on_ricerca_lotto_menuitem_activate(self, button):
        from promogest.ui.RicercaLottiWindow import RicercaLottiWindow
        anag = RicercaLottiWindow(self)
        showAnagrafica(self.getTopLevel(), anag)

    def on_button_help_clicked(self, button):
        SendEmail()

    def on_button_refresh_clicked(self, widget=None):
        if self.creata:
            self.main_notebook.remove_page(0)
        self._refresh()

    def on_main_iconview_select(self, icon_view, model=None):

        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        if Environment.pg3:
            i = selected[0]
        else:
            i = selected[0][0]
        selection = self.iconview_listore[i][0]

        if selection == 3:
            #self.currentFrame = self.create_registrazioni_frame()
            # Andrea
            # richiamo diretto dei documenti: evita di dover premere il
            # pulsante nel frame registrazioni
            if not hasAction(actionID=2):
                return
            from promogest.ui.anagDocumenti.AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 4:
            if not hasAction(actionID=15):
                return
            from promogest.modules.PrimaNota.ui.AnagraficaPrimaNota import AnagraficaPrimaNota
            anag = AnagraficaPrimaNota(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 5:
            if posso("PR"):
                from promogest.ui.anagPromemoria.AnagraficaPromemoria import AnagraficaPromemoria
                anag = AnagraficaPromemoria(self.aziendaStr)
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                icon_view.unselect_all()
                return
            else:
                fencemsg()
        elif selection == 10: #gestione commessa
            #if posso("GC"):
            from promogest.modules.GestioneCommesse.ui.AnagraficaCommesse import AnagraficaCommesse
            anag = AnagraficaCommesse(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return

        else:
            if Environment.pg3:
                i = selected[0]
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
        for module in self.anagrafiche_modules.iteritems():
            module_button = gtk.Button()
            module_butt_image = gtk.Image()
            module_butt_image.set_from_file(module[1]['guiDir']+'/'+module[1]['module'].VIEW_TYPE[2])
            module_button.set_image(module_butt_image)
            module_button.set_label(module[1]['module'].VIEW_TYPE[1])
            module_button.connect('clicked', self.on_module_button_clicked)
            self.anagrafiche_moduli_vbox.pack_start(module_button, False, False, 0)

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
        from promogest.ui.anagArti.AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(aziendaStr=Environment.azienda)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from promogest.ui.anagClienti.AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from promogest.ui.anagFornitori.AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_vettori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from promogest.ui.anagVettori.AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori(aziendaStr=self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_agenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        if posso("AG"):
            from promogest.ui.anagAgenti.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)
        else:
            fencemsg()
            toggleButton.set_active(False)

    def on_apri_anag_secondarie_toggle_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        from promogest.ui.AnagraficaSecondaria import AnagraficaSecondarie
        if not findIdFromCombobox(self.anag_minori_combobox):
            obligatoryField(None,
                            self.anag_minori_combobox,
                            msg=_('Campo obbligatorio !\n\nTipo AnagraficaSecondaria'))
            toggleButton.set_active(False)
        model = self.anag_minori_combobox.get_model()
        iterator = self.anag_minori_combobox.get_active_iter()
        if iterator is not None:
            dao = model.get_value(iterator, 0)
        anag = AnagraficaSecondarie(aziendaStr=self.aziendaStr, daoRole= dao)
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)


    def on_categorie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
        anag = AnagraficaCategorieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_famiglie_articoli_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
        anag = AnagraficaFamiglieArticoli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_clienti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaCategorieClienti import AnagraficaCategorieClienti
        anag = AnagraficaCategorieClienti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_fornitori_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaCategorieFornitori import AnagraficaCategorieFornitori
        anag = AnagraficaCategorieFornitori()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_utenti_button_toggled(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
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
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
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
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
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
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaMultipli import AnagraficaMultipli
        anag = AnagraficaMultipli()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_pagamenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaPagamenti import AnagraficaPagamenti
        anag = AnagraficaPagamenti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_banche_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaBanche import AnagraficaBanche
        anag = AnagraficaBanche()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_categorie_contatti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from promogest.ui.Contatti.AnagraficaCategorieContatti import AnagraficaCategorieContatti
        anag = AnagraficaCategorieContatti()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_aliquote_iva_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaAliquoteIva import AnagraficaAliquoteIva
        anag = AnagraficaAliquoteIva()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_imballaggi_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
            return
        from AnagraficaImballaggi import AnagraficaImballaggi
        anag = AnagraficaImballaggi()
        showAnagrafica(self.getTopLevel(), anag, toggleButton, mainClass=self)

    def on_stadio_commessa_button_toggled(self, toggleButton):

        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=6):
            toggleButton.set_active(False)
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
#        selection = model[i][0]
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
        fileDialog = gtk.FileChooserDialog(title=_('Importazione modulo'),
                                           parent=self.getTopLevel(),
                                           action=GTK_FILE_CHOOSER_ACTION_OPEN,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_OK,
                                                    GTK_RESPONSE_OK),
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
        if response == GTK_RESPONSE_OK:
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
                msg = _("MODULO CORRETTAMENTE INSTALLATO, CHIUDERE L'APPLICAZIONE\nED AGGIUNGERE I PARAMETRI NECESSARI\n")
            else:
                msg = _("ATTENZIONE, MODULO NON INSTALLATO, CORROTTO O NON CORRETTO, CONTATTARE L'ASSISTENZA")
            messageInfo(msg=msg)
                #self.path_file_entry.set_text(filename)
            fileDialog.destroy()

    def on_credits_menu_activate(self, widget):
        creditsDialog = GladeWidget(root='credits_dialog',path="credits_dialog.glade",  callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        info = "%s Build: %s" % (Environment.VERSIONE, Environment.rev_locale)
        creditsDialog.versione_label.set_markup(info)
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == GTK_RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_inserimento_codice_activate(self,widget):
        from promogest.dao.Setconf import SetConf
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   GTK_DIALOG_MODAL
                                   | GTK_DIALOG_DESTROY_WITH_PARENT,
                                   GTK_DIALOG_MESSAGE_INFO, GTK_BUTTON_OK)
        dialog.set_markup(_("""<b>                CODICE ATTIVAZIONE PACCHETTO               </b>"""))
        hbox = gtk.HBox()
        entry___ = gtk.Entry()

        label = gtk.Label()
        label.set_markup(_("<b>   Inserisci codice   </b>"))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry___, True, True, 0)
        dialog.get_content_area().pack_start(hbox, True, True, 0)
        dialog.show_all()
        dialog.run()
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
                        messageInfo(msg = _("NOME AZIENDA MODIFICATO"))
                        dialog.destroy()
                        return
                    else:
                        messageInfo(msg = _("VECCHIO NOME AZIENDA NON TROVATO"))
                        dialog.destroy()
                        return
                    return
                else:
                    messageInfo(msg = _("POSSIBILE SOLO CON LA VERSIONE ONE"))
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
                    messageInfo(msg = _("ERRORE ATTIVAZIONE MODULO"))
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
                d.date = datetime.now()
                d.persist()
                messageInfo(msg=_("MODULO O OPZIONE MODIFICATO attivato o disattivato"))
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
                        messageInfo(msg=_("REGISTRO NUMERAZIONE MODIFICATO\n\nRIAVVIARE"))
                        dialog.destroy()
                        return True
                    else:
                        messageInfo(msg=_("REGISTRO DA ASSEGNARE NON TROVATO O CORRETTO\n\n RIPROVARE"))
                        return False
                else:
                    messageInfo(msg=_("OPERAZIONE NON CORRETTA E NON TROVATA\n\nRIPROVARE"))
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
                k.date = datetime.now()
                k.persist()
                messageInfo(msg=_("ATTIVAZIONE EFFETTUATA, RIAVVIARE IL PROMOGEST"))
        dialog.destroy()


    def on_licenza_menu_activate(self, widget):
        licenzaDialog = GladeWidget(root='licenza_dialog',path="licenza_dialog.glade",  callbacks_proxy=self)
        licenzaDialog.getTopLevel().set_transient_for(self.getTopLevel())
        licenseText = ''
        try:
            lines = open('./LICENSE').readlines()
            for l in lines:
                licenseText += l
        except:
            licenseText = _('Lavori in corso ....')
            print 'License file not found (LICENSE).'
        textBuffer = licenzaDialog.licenza_textview.get_buffer()
        textBuffer.set_text(licenseText)
        licenzaDialog.licenza_textview.set_buffer(textBuffer)
        licenzaDialog.getTopLevel().show_all()
        response = licenzaDialog.licenza_dialog.run()
        if response == GTK_RESPONSE_OK:
            licenzaDialog.licenza_dialog.destroy()

    def on_manuale_online_activate(self, widget):
        url ="http://help.promogest.me"
        webbrowser.open_new_tab(url)

    def on_aggiorna_activate(self, widget):
        updateDialog = UpdateDialog(self)
        updateDialog.show()

    def on_Back_up_Database_activate(self, widget):
        """ Si prepara un file zip con il dump del DB """

        if Environment.tipodb == "sqlite":
            msg = _("""NELLA VERSIONE ONE IL BACKUP SI
EFFETTUA COPIANDO IL FILE db CHE SI TROVA NELLA CARTELLA
promogest2 IN /HOME/NOMEUTENTE/ O IN C:/UTENTI/NOMEUTENTE""")
            messageInfo(msg= msg)
        else:
            st= Environment.startdir()
            nameDump = "promoGest2_dump_"+self.aziendaStr+"_"+ datetime.now().strftime('%d_%m_%Y_%H_%M')
            msgg = _("""Il "dump" del database verrà salvato in

    %s
    ed avrà il nome

    %s.zip

    ATTENZIONE!!!! la procedura potrebbe richiedere diversi minuti.""") %(st, nameDump)
            messageInfo(msg= msgg, transient=self.getTopLevel())
            #if response == gtk.RESPONSE_OK:
            st= Environment.startdir()
            stname = st+nameDump
            os.environ["PGPASSWORD"] = Environment.password

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
            msg = _('Codice installazione:\n\n') + str(codice)
        except:
            msg = _('Impossibile generare il codice !!!')
        messageInfo(msg= msg, transient=self.getTopLevel())

    def on_send_Email_activate(self, widget):
        SendEmail()

    def on_master_sincro_db_activate(self, widget):
        msg = _("SERVER NON ANCORA IMPLEMENTATO")
        messageInfo(msg= msg, transient=self.getTopLevel())

    def on_client_sincro_db_activate(self, widget):
        if posso("SD") and Environment.conf.SincroDB.tipo =="client":
            from promogest.modules.SincroDB.ui.SincroDB import SincroDB
            anag = SincroDB()
            showAnagrafica(self.getTopLevel(), anag)

    def on_test_promowear_button_clicked(self, button):
        msg = _("""ATTENZIONE!!
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

Procedere all'installazione del modulo PromoWear? """)
        if not YesNoDialog(msg=msg, transient=self.getTopLevel()):
            return
        if not hasattr(Environment.conf,"PromoWear"):
            Environment.conf.add_section("PromoWear")
            Environment.conf.save()
            Environment.conf.PromoWear.primoavvio = "yes"
            Environment.conf.save()
        tables = [t.name for t in Environment.params["metadata"].sorted_tables]
        if "colore" not in tables and "taglia" not in tables:
            from promogest.modules.PromoWear.data.PromoWearDB import *
            msg = _(" TABELLE AGGIUNTE, RIAVVIARE IL PROGRAMMA ")
            messageInfo(msg=msg)
        else:
            msg= _("PULSANTE DI TEST GIA' PREMUTO")
            messageInfo(msg=msg, transient=self.getTopLevel())


    def on_test_promoshop_button_clicked(self, button):
        from promogest.dao.Setconf import SetConf
        msg = _("""ATTENZIONE!!
QUESTA FUNZIONALITÀ È STATA AGGIUNTA PER
PERMETTERE DI PROVARE IL PROMOGEST ONE BASIC CON
IL MODULO VENDITA DETTAGLIO

Procedere all'installazione del modulo PromoShop? """)
        if not YesNoDialog(msg=msg, transient=self.getTopLevel()):
            return
        if not setconf("VenditaDettaglio","mod_enable",value="yes"):
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
            messageInfo(msg=_("RISULTA GIA' ATTIVATO"))

    def on_ricmedio_activate(self, widget):
        """ entry Menu statistiche Ricarico medio """
        from promogest.modules.Statistiche.ui.StatisticaGenerale import StatisticaGenerale
        anag = StatisticaGenerale(idMagazzino=None,
                        nome=_("RICARICO MEDIO e INFLUENZA SULLE VENDITE"))
        anag.getTopLevel()

    def on_controllo_fatturato_activate(self, widget):
        from promogest.modules.Statistiche.ui.StatisticaGenerale import StatisticaGenerale
        anag = StatisticaGenerale(idMagazzino=None,
                        nome=_("CONTROLLO FATTURATO"))
        anag.getTopLevel()

    def on_whatcant_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/whatCanT"
        webbrowser.open_new_tab(url)

    def on_export_magazzino_activate(self, button):
        from promogest.modules.Statistiche.ui.StatisticheMagazzino import StatisticheMagazzino
        anag = StatisticheMagazzino(idMagazzino=None)
        anag.getTopLevel()

    def on_main_window_key_press_event(self, widget, event):
        on_main_window_key_press_eventPart(self, widget, event)

    def on_disconnect(self, widget=None):
        if YesNoDialog(msg=_('Disconnessione dal database, continuare?'), transient=self.getTopLevel()):
            self.destroy()
        else:
            return

    def on_quit(self, widget=None):
        if YesNoDialog(msg=_('Confermi la chiusura?'), transient=self.getTopLevel()):
            self.hide()
            gtk.main_quit()
        else:
            return

    def on_main_notebook_change_current_page(self, notebook):
        pass


    def on_main_notebook_select_page(self, noteebok):
        pass

    def addNoteBookPage(self):

        if WEBKIT:
            self.nn = NewsNotebookPage(self, self.aziendaStr).draw()
            n = gtk.Label()
            n.set_markup(_("<b>NEWS/A.VEL</b>"))
            ind = self.main_notebook.append_page(self.nn.notizie_frame, n)
            self.main_notebook.set_current_page(ind)

        self.pp = checkPan(self)

        self.elenco_magazzini_page = ElencoMagazzini(self, self.aziendaStr).draw()
        self.main_notebook.append_page(self.elenco_magazzini_page.elenco_magazzini_frame, self.elenco_magazzini_page.magazzini_label)

        self.elenco_listini_page = ElencoListini(self, self.aziendaStr).draw()
        self.main_notebook.append_page(self.elenco_listini_page.elenco_listini_frame,self.elenco_listini_page.elenco_listini_label)

        self.scadenzario = ScadenzarioNotebookPage(self, self.aziendaStr)
        scadenzario_label = gtk.Label()
        scadenzario_label.set_markup(_("<b>SCADENZARIO</b>"))
        self.main_notebook.append_page(self.scadenzario.scadenzario_frame, scadenzario_label)

        self.calendar_page = CalendarNotebookPage(self, self.aziendaStr).draw()
        calendar_page_label = gtk.Label()
        calendar_page_label.set_markup(_("<b>CALENDARIO</b>"))
        self.main_notebook.append_page(self.calendar_page.calendario_frame, calendar_page_label)

        self.notifica_allarmi = NotificaAllarmiNotebookPage(self, self.aziendaStr)
        notifica_allarmi_label = gtk.Label()
        notifica_allarmi_label.set_markup(_("<b>NOTIFICA ALLARMI</b>"))
        self.main_notebook.append_page(self.notifica_allarmi.notifica_allarmi_frame, notifica_allarmi_label)

#        azioni_veloci_page = AzioniVelociNotebookPage(self, self.aziendaStr).draw()
#        self.azioni_veloci_page = azioni_veloci_page
#        azioni_veloci_page_label = gtk.Label()
#        azioni_veloci_page_label.set_markup("<b>AZIONI VELOCI</b>")
#        self.main_notebook.append_page(azioni_veloci_page.azioni_veloci_frame, azioni_veloci_page_label)


    def statusBarHandler(self):
        if not Environment.nobrand:
            textStatusBar = _(" %s Build: %s - 070 8649705 - www.promogest.me - info@promotux.it     " % (Environment.VERSIONE, Environment.rev_locale))
        else:
            textStatusBar = _(" %s Build: %s - %s" % (Environment.VERSIONE, Environment.rev_locale, Environment.partner))
        context_id =  self.pg2_statusbar.get_context_id("main_window")
        self.pg2_statusbar.push(context_id, textStatusBar)

class MainWindowFrame(VistaPrincipale):
    def __init__(self, mainWindow, azs):
        VistaPrincipale.__init__(self, self.mainWindow, azs)


class RegistrazioniFrame(GladeWidget):
    """ Frame per la gestione delle registrazioni """

    def __init__(self, mainWindow,azs):
        self.mainWindow = mainWindow
        self.aziendaStr = azs
        GladeWidget.__init__(self, root='registrazioni_select_frame',
                                    path='_registrazioni_select.glade')

    def on_documenti_button_clicked(self, toggleButton):
        if toggleButton.get_property('active') is False:
            return
        if not hasAction(actionID=2):return
        from promogest.ui.anagDocumenti.AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)

        showAnagrafica(self.mainWindow, anag, toggleButton)

def on_anagrafica_destroyed(anagrafica_window, argList):
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
