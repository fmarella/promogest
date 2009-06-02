# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>, Francesco Meloni <francesco@promotux.it>
# License GNU Gplv2

import locale
import gtk, gobject
import hashlib
import os
from  subprocess import *
import threading, os, signal
from promogest import Environment
from GladeWidget import GladeWidget
from ElencoMagazzini import ElencoMagazzini
from ElencoListini import ElencoListini
from VistaPrincipale import VistaPrincipale
from promogest.ui.SendEmail import SendEmail
from utils import hasAction,fenceDialog
from utilsCombobox import *
from ParametriFrame import ParametriFrame
from AnagraficaPrincipaleFrame import AnagrafichePrincipaliFrame
import Login

class Main(GladeWidget):

    def __init__(self,aziendaStr,anagrafiche_modules,parametri_modules,
                    anagrafiche_dirette_modules,frame_modules,permanent_frames):

        GladeWidget.__init__(self, 'main_window')
        self.main_window.set_title('*** PromoGest2 *** Azienda : '+aziendaStr+'  *** Utente : '+Environment.params['usernameLoggedList'][1]+' ***')
        self.aziendaStr = aziendaStr
        Login.windowGroup.append(self.getTopLevel())
        self.anagrafiche_modules = anagrafiche_modules
        self.parametri_modules = parametri_modules
        self.anagrafiche_dirette_modules=anagrafiche_dirette_modules
        self.frame_modules = frame_modules
        self.permanent_frames = permanent_frames
        self.currentFrame = None
        self.alarmFrame = None

        self.updates()


    def show(self):
        """ Visualizza la finestra """

        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf)

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'anagrafica48x48.png')
        model.append([0, "Anagrafiche", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'magazzino48x48.png')
        model.append([1, "Magazzini", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'listino48x48.png')
        model.append([2, "Listini", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'documento48x48.png')
        model.append([3, "Documenti", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'parametri48x48.png')
        model.append([4, "Parametri", pbuf])

        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'promemoria48x48.png')
        model.append([5, "Promemoria", pbuf])

        self.main_iconview.set_model(model)
        self.main_iconview.set_text_column(1)
        self.main_iconview.set_pixbuf_column(2)
        self.main_iconview.connect('selection-changed',
                                   self.on_main_iconview_select, model)

        self.main_iconview.set_columns(1)
        self.main_iconview.set_item_width(120)
        self.main_iconview.set_size_request(130, -1)

        # right vertical icon list  adding modules
        model_right = gtk.ListStore(int, str, gtk.gdk.Pixbuf, object)
        ind = 0
        for mod in self.anagrafiche_dirette_modules.keys():
            currModule = self.anagrafiche_dirette_modules[mod]
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row = (ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model_right.append(row)
            ind += 1
        for mod in self.frame_modules.keys():
            currModule = self.frame_modules[mod]
            pbuf = gtk.gdk.pixbuf_new_from_file(currModule['guiDir']+ currModule['module'].VIEW_TYPE[2])
            row =(ind, currModule['module'].VIEW_TYPE[1], pbuf, currModule['module'])
            model_right.append(row)
            ind += 1

        self.main_iconview_right.set_model(model_right)
        self.main_iconview_right.set_text_column(1)
        self.main_iconview_right.set_pixbuf_column(2)
        self.main_iconview_right.connect('selection-changed',
                                   self.on_main_iconview_right_select, model_right)

        self.main_iconview_right.set_columns(1)
        self.main_iconview_right.set_item_width(120)
        self.main_iconview_right.set_size_request(130, -1)
        #load the alarm notification frame (AKA MainWindowFrame)
        if self.currentFrame is None:
            self.main_hbox.remove(self.box_immagini_iniziali)
            self._refresh()
        self.placeWindow(self.main_window)
        self.main_window.show_all()


    def updates(self):
        """
            Aggiornamenti e controlli da fare all'avvio del programma
        """
        #Aggiornamento scadenze promemoria
        if "Promemoria" in Environment.modulesList:
            import promogest.dao.Promemoria
            promogest.dao.Promemoria.updateScadenze()
        #Verifica inventario  FIXME: DA SISTEMAREEEEEEEEEEEEEEEE ( FRANCESCO )
        #from promogest.dao.Inventario import Inventario
        #Inventario().control(self.getTopLevel())
        return

    def _refresh(self):
        """
        Update the window, setting the appropriate frame
        """
        self.main_iconview.unselect_all()
        if self.currentFrame is None:
            self.currentFrame = self.create_main_window_frame()
        self.main_notebook = gtk.Notebook()
        if len(self.permanent_frames) > 0:
            self.main_notebook.append_page(self.currentFrame, 'Home')
            for module in self.pemanent_frames.iteritems():
                frame = module[1]['module'].getApplication().getTopLevel()
                self.main_notebook.append_page(frame,module[1]['module'].VIEW_TYPE[1])
            self.main_hbox.pack_start(self.main_notebook, fill=True, expand=True)
        else:
            self.main_hbox.pack_start(self.currentFrame, fill=True, expand=True)
        self.main_hbox.show_all()

    def on_disconnect(self, widget=None):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la disconnessione?')

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            self.destroy()
        else:
            return


    def on_quit(self, widget=None):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi la chiusura?')

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            self.hide()
            gtk.main_quit()
        else:
            return

    def on_button_help_clicked(self, button):
        sendemail = SendEmail()

    def on_button_refresh_clicked(self, widget=None):
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        self.currentFrame = None
        self._refresh()

    def on_main_iconview_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0:
            return
        i = selected[0][0]
        selection = model[i][0]

        if self.currentFrame is not None: #and self.currentFrame != self.alarmFrame:
            self.main_hbox.remove(self.currentFrame)
            self.currentFrame.destroy()
            self.currentFrame = None
        if selection == 0:
            self.currentFrame = self.create_anagrafiche_principali_frame()
        elif selection == 1:
            self.currentFrame = self.create_magazzini_frame()
        elif selection == 2:
            self.currentFrame = self.create_listini_frame()
        elif selection == 3:
            #self.currentFrame = self.create_registrazioni_frame()
            # Andrea
            # richiamo diretto dei documenti: evita di dover premere il
            # pulsante nel frame registrazioni
            if not hasAction(actionID=2):return
            from AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti(aziendaStr=self.aziendaStr)
            showAnagrafica(self.getTopLevel(), anag, mainClass=self)
            icon_view.unselect_all()
            return
        elif selection == 4:
            self.currentFrame = self.create_parametri_frame()
        elif selection == 5:
            if "Promemoria" in Environment.modulesList:
                from AnagraficaPromemoria import AnagraficaPromemoria
                anag = AnagraficaPromemoria(self.aziendaStr)
                showAnagrafica(self.getTopLevel(), anag, mainClass=self)
                icon_view.unselect_all()
                return
            else:
                fenceDialog()
        self._refresh()

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


    def create_main_window_frame(self):
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = VistaPrincipale(self, self.aziendaStr)
        return frame.vista_principale_frame

    def create_anagrafiche_principali_frame(self):
        if not hasAction(actionID=11):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = AnagrafichePrincipaliFrame(self.main_window, self.aziendaStr, modules=self.anagrafiche_modules)
        return frame.getTopLevel()

    def create_magazzini_frame(self):
        if not hasAction(actionID=12):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = MagazziniFrame(self.main_window, self.aziendaStr)
        return frame.getTopLevel()

    def create_listini_frame(self):
        if not hasAction(actionID=9):return
        if self.currentFrame is not None:
            self.main_hbox.remove(self.currentFrame)
        frame = ListiniFrame(self.main_window, self.aziendaStr)
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


    def on_nuovo_articolo_menu_activate(self, widget):
        if not hasAction(actionID=8):return
        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_cliente_menu_activate(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_nuovo_fornitore_menu_activate(self, widget):
        if not hasAction(actionID=11):return
        from AnagraficaFornitori import AnagraficaFornitori
        anag = AnagraficaFornitori(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()

    def on_fattura_vendita_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura vendita")


    def on_fattura_acquisto_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura acquisto")


    def on_ddt_vendita_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT vendita")


    def on_ddt_acquisto_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT acquisto")


    def on_ddt_reso_da_cliente_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso da cliente")


    def on_ddt_reso_a_fornitore_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("DDT reso a fornitore")


    def on_nota_di_credito_a_cliente_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito a cliente")


    def on_nota_di_credito_a_fornitore_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Nota di credito da fornitore")


    def on_fattura_accompagnatoria_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Fattura accompagnatoria")


    def on_preventivo_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Preventivo")


    def on_vendita_al_dettaglio_menu_activate(self, widget):
        if not hasAction(actionID=2):return
        self.nuovoDocumento("Vendita dettaglio")

    def nuovoDocumento(self, kind):
        if not hasAction(actionID=2):return
        from AnagraficaDocumenti import AnagraficaDocumenti
        #from utils import findComboboxRowFromStr
        anag = AnagraficaDocumenti(self.aziendaStr)
        showAnagrafica(self.getTopLevel(), anag)
        anag.on_record_new_activate()
        findComboboxRowFromStr(anag.editElement.id_operazione_combobox, kind, 1)
        anag.editElement.id_persona_giuridica_customcombobox.grab_focus()
        findComboboxRowFromStr(anag.editElement.id_persona_giuridica_customcombobox, "Altro", 1)

    def on_configurazione_menu_activate(self, widget):
        if not hasAction(actionID=14):return
        configuraWindow = ConfiguraWindow(self)
        showAnagrafica(self.getTopLevel(), configuraWindow)

    def on_dati_azienda_activate(self, widget):
        from AnagraficaAziende import AnagraficaAziende
        anag =AnagraficaAziende(self)
        showAnagrafica(self.getTopLevel(), anag)

    def on_importa_modulo_activate(self, widget):
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
                pa = os.path.join(Environment.conf.Moduli.cartella_moduli,n+"/"+"module.py")
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
        from promogest.dao.Setting import Setting
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        encoding = locale.getlocale()[1]
        utf8conv = lambda x : unicode(x, encoding).encode('utf8')
        licenseText = ''
        textBuffer = creditsDialog.svn_info_textview.get_buffer()
        textBuffer.set_text(licenseText)
        command = 'svn info ~/pg2'
        p = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        (stdin, stdouterr) = (p.stdin, p.stdout)
        for line in stdouterr.readlines():
            textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
        textBuffer.insert(textBuffer.get_end_iter(),"""I moduli installati sono :
""")
        for line in Environment.modulesList:
            textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
        response = creditsDialog.credits_dialog.run()
        if response == gtk.RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()


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

    def on_aggiorna_activate(self, widget):
        svndialog = GladeWidget('svnupdate_dialog', callbacks_proxy=self)
        svndialog.getTopLevel().set_transient_for(self.getTopLevel())
        encoding = locale.getlocale()[1]
        utf8conv = lambda x : unicode(x, encoding).encode('utf8')
        licenseText = ''
        textBuffer = svndialog.svn_textview.get_buffer()
        textBuffer.set_text(licenseText)
        svndialog.svn_textview.set_buffer(textBuffer)
        svndialog.getTopLevel().show_all()
        response = svndialog.svnupdate_dialog.run()
        if response == gtk.RESPONSE_OK:
            command = 'svn co http://svn.promotux.it/svn/promogest2/trunk/ ~/pg2'
            p = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            (stdin, stdouterr) = (p.stdin, p.stdout)
            #stdin, stdouterr = os.popen4(command)
            for line in stdouterr.readlines():
                textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
            msg = """ Se è apparsa la dicitura "Estratta Revisione XXXX
l'aggiornamento è riuscito, nel caso di messaggio fosse differente
potete contattare l'assistenza tramite il numero verde 80034561
o tramite email all'indirizzo info@promotux.it

        Aggiornamento de|l Promogest2 terminato !!!
        Riavviare l'applicazione per rendere le modifiche effettive
                    """
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
            svndialog.svnupdate_dialog.destroy()

    def on_Back_up_Database_activate(self, widget):
        import zipfile
        bkdbdialog = GladeWidget('svnupdate_dialog', callbacks_proxy=self)
        bkdbdialog.getTopLevel().set_transient_for(self.getTopLevel())
        encoding = locale.getlocale()[1]
        utf8conv = lambda x : unicode(x, encoding).encode('utf8')
        licenseText = 'Il "dump" del database verrà salvato nella home utente'
        textBuffer = bkdbdialog.svn_textview.get_buffer()
        textBuffer.set_text(licenseText)
        bkdbdialog.svn_textview.set_buffer(textBuffer)
        bkdbdialog.getTopLevel().show_all()
        response = bkdbdialog.svnupdate_dialog.run()
        if response == gtk.RESPONSE_OK:
            nameDump= "promoGest2_dump_"+self.aziendaStr+"_"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
            command = 'pg_dump -h %s -p %s -U %s %s > ~/%s' %(Environment.host,
                                                            Environment.port,
                                                            Environment.user,
                                                            Environment.database,
                                                            nameDump)
            p = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            (stdin, stdouterr) = (p.stdin, p.stdout)
            #zfilename = nameDump +".zip"
            #zout = zipfile.ZipFile(zfilename, "w")
            #zout.write(nameDump, zipfile.ZIP_DEFLATED)
            #zout.close()
            #stdin, stdouterr = os.popen4(command)
            for line in stdouterr.readlines():
                textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
            msg = """Se nella finestra NON è apparso alcun messaggio d'errore
il dump è stato effettuato correttamente.

Il file si chiama %s .
                    """ %(nameDump)
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
            bkdbdialog.svnupdate_dialog.destroy()

    def on_seriale_menu_activate(self, widget):
        try:
            fileName = Environment.conf.guiDir + 'logo_promogest.png'
            f = open(fileName,'rb')
            content = f.read()
            f.close()
            msg = 'Codice installazione:\n\n' + str(hashlib.md5(content).hexdigest().upper())
        except:
            msg = 'Impossibile generare il codice !!!'
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
        dialog.run()
        dialog.destroy()

    def on_send_Email_activate(self, widget):
        sendemail = SendEmail()

    def on_master_sincro_db_activate(self, widget):
        print "DFGDFDHSDHSHFHF"
        if "SincroDB" in Environment.modulesList:
            from promogest.modules.SincroDB.ui.SincroDB import SincroDB
            anag = SincroDB()
            showAnagrafica(self.getTopLevel(), anag)
        else:
            print "PASSIQUI"
            #return

    def on_main_window_key_press_event(self, widget, event):
        if event.type == gtk.gdk.KEY_PRESS:
            if event.state & gtk.gdk.CONTROL_MASK and (
                (event.state & gtk.gdk.MOD2_MASK) or (event.state & gtk.gdk.MOD1_MASK)):
                if gtk.gdk.keyval_name(event.keyval) == "m":
                    # easter egg

                    def menuitem_response(game):
                        games_menu.hide()
                        os.system(game)

                    tetris_games = (
                        'gnometris','ksirtet','xtris','kcalc','emacs','ksmiletris','ltris')
                    games_menu = gtk.Menu()
                    for game in tetris_games:
                        ret = os.system('which ' + game + ' > /dev/null')
                        if ret==0:
                            item = gtk.MenuItem(game)
                            games_menu.append(item)
                            item.connect_object("activate", menuitem_response, game)
                            item.show()
                    games_menu.popup(None, None, None, 3, event.time)
                    return True
                elif gtk.gdk.keyval_name(event.keyval) == "u":
                    # easter egg

                    def menuitem_response(utilities):
                        utilities_menu.hide()
                        os.system(utilities)

                    utils = (
                        'firefox','konqueror','thunderbird','kcalc','kate','gcalctool')
                    utilities_menu = gtk.Menu()
                    for util in utils:
                        ret = os.system('which ' + util + ' > /dev/null')
                        if ret==0:
                            item = gtk.MenuItem(util)
                            utilities_menu.append(item)
                            item.connect_object("activate", menuitem_response, util)
                            item.show()
                    utilities_menu.popup(None, None, None, 3, event.time)
                    return True
            elif gtk.gdk.keyval_name(event.keyval) == "t":
                import random
                msg= """
Il Promogest2 "MentoR" ha generato per te due sestine
"vincenti" per il prossimo concorso del superenalotto
giocale e facci sapere .....
Mi raccomando se dovessi vincere ricordati di noi :)

Il Team:

I Numeri:   %s
                %s
""" %(str(random.sample(xrange(90), 6))[1:-1],str(random.sample(xrange(90), 6))[1:-1])
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
                dialog.run()
                dialog.destroy()

            return True
        else:
            return False





class ConfiguraWindow(GladeWidget):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        GladeWidget.__init__(self, 'configura_window', fileName='configura_window.glade')
        self.placeWindow(self.getTopLevel())

        self.draw()


    def draw(self):
        self.sections_box = gtk.VBox()
        self.sections_box.set_spacing(6)
        sections = Environment.conf.sections()
        i = 0
        for section in sections:
            localFrame = gtk.Frame(section)
            localFrame.set_border_width(8)
            current_section = getattr(Environment.conf, section)

            #get the sections' attributes
            attrs = current_section.options()

            #populate the frame with labels containing the attributes' names
            attr_box = gtk.VBox()

            for attr in attrs:
                attr_hbox = gtk.HBox()
                attr_hbox.set_homogeneous(False)
                label_attribute = gtk.Label(attr)
                label_attribute.set_padding(7, 0)
                label_attribute.set_alignment(0.0, 0.5)
                label_attribute.set_size_request(200, -1)
                attr_hbox.pack_start(label_attribute, False, False)

                #create the entry containing the attribute's value
                entry_valore = gtk.Entry()
                entry_valore.connect('changed', self.on_entry_value_changed, current_section, attr)
                attr_hbox.add(entry_valore)
                attr_value = getattr(current_section, attr)
                if attr == 'password':
                    entry_valore.set_visibility(False)
                entry_valore.set_text(attr_value)

                attr_box.add(attr_hbox)

            localFrame.add(attr_box)
            self.sections_box.add(localFrame)

        self.params_scrolled_window.add_with_viewport(self.sections_box)
        self.salva_button.set_sensitive(False)


    def on_entry_value_changed(self, entry,current_section, attr):
        self.salva_button.set_sensitive(True)
        setattr(current_section,attr,entry.get_text())


    def on_salva_button_clicked(self, button_salva):
        Environment.conf.save()
        self.salva_button.set_sensitive(False)


    def on_quit(self, widget=None, event=None):
        self.destroy()

class MainWindowFrame(VistaPrincipale):
    def __init__(self, mainWindow, azs):
        VistaPrincipale.__init__(self, self.mainWindow, azs)


class MagazziniFrame(ElencoMagazzini):
    """ Frame per la gestione dei magazzini """

    def __init__(self, mainWindow, azs):
        self.mainWindow = mainWindow
        ElencoMagazzini.__init__(self, self.mainWindow, azs)



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


#class AziendaFrame(AnagraficaAziende):
    #""" Frame per la gestione delle aziende """

    #def __init__(self, mainWindow, mainClass=None):
        #self.mainWindow = mainWindow
        #AnagraficaAziende.__init__(self, self.mainWindow)

class ListiniFrame(ElencoListini):
    """ Frame per la gestione dei listini """

    def __init__(self, mainWindow,azs):
        self.mainWindow = mainWindow
        ElencoListini.__init__(self, self.mainWindow,azs)

def on_anagrafica_destroyed(anagrafica_window, argList):
    mainWindow = argList[0]
    anagraficaButton= argList[1]
    mainClass = argList[2]
    if anagrafica_window in Login.windowGroup:
        Login.windowGroup.remove(anagrafica_window)
    if anagraficaButton is not None:
        anagraficaButton.set_active(False)
    if mainClass is not None:
        mainClass.on_button_refresh_clicked()

def showAnagrafica(window, anag, button=None, mainClass=None):
    anagWindow = anag.getTopLevel()
    anagWindow.connect("destroy", on_anagrafica_destroyed, [window, button,mainClass])
    #anagWindow.connect("hide", on_anagrafica_destroyed, [window, button,mainClass])
    anagWindow.set_transient_for(window)
    anagWindow.show_all()
