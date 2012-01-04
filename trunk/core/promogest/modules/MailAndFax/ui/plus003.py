# -*- coding: iso-8859-15 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
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

import threading
import smtplib, mimetypes, popen2, os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from email import Encoders
from promogest.dao.CategoriaContatto import CategoriaContatto
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from promogest.ui.gtk_compat import *


class SpamFrame(GladeWidget):
    """ Frame per la gestione delle aziende """

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        GladeWidget.__init__(self, 'spam_frame')

        # Costruisco treeview categorie mail e fax
        modelRiga = gtk.ListStore(int, str)
        treeview = self.category_treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        modelRiga = gtk.ListStore(int, str)
        treeview = self.sendfax_category_treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        # Costruisco treeview files
        modelRiga = gtk.ListStore(str)

        treeview = self.attachment_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Nome file', renderer, text=0)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_model(modelRiga)

        # Costruisco treeviews singoli contatti
        modelRiga = gtk.ListStore(str, str)
        treeview = self.contact_treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Contatto', renderer, text=0)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('E-Mail', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        modelRiga = gtk.ListStore(str, str)
        treeview = self.contact_fax_treeview
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Contatto', renderer, text=0)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Fax', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_model(modelRiga)

        # Riempio combobox categorie mail e fax
        combobox = self.category_combobox
        model = gtk.ListStore(int, str)
        cats = CategoriaContatto().select(denominazione=None,
                                                orderBy = None,
                                                offset = None,
                                                batchSize = None)
        for c in cats:
            model.append((c.id, (c.denominazione or '')[0:20]))

        combobox.clear()
        renderer = gtk.CellRendererText()
        combobox.pack_start(renderer, True)
        combobox.add_attribute(renderer, 'text', 1)
        combobox.set_model(model)

        combobox = self.sendfax_category_combobox
        model = gtk.ListStore(int, str)
        for c in cats:
            model.append((c.id, (c.denominazione or '')[0:20]))

        combobox.clear()
        renderer = gtk.CellRendererText()
        combobox.pack_start(renderer, True)
        combobox.add_attribute(renderer, 'text', 1)
        combobox.set_model(model)


    def on_add_button_clicked(self, button):
        combobox = self.category_combobox
        model = combobox.get_model()
        iterator = combobox.get_active_iter()
        if iterator is not None:
            id = model.get_value(iterator, 0)
            categoria = model.get_value(iterator, 1)
            for c in self.category_treeview.get_model():
                if c[0] == id:
                    return
            self.category_treeview.get_model().append((id, categoria))


    def on_delete_button_clicked(self, button):
        treeSelection = self.category_treeview.get_selection()
        (model, iterator) = treeSelection.get_selected()
        if iterator is not None:
            model.remove(iterator)


    def on_sendfax_add_button_clicked(self, button):
        combobox = self.sendfax_category_combobox
        model = combobox.get_model()
        iterator = combobox.get_active_iter()
        if iterator is not None:
            id = model.get_value(iterator, 0)
            categoria = model.get_value(iterator, 1)
            for c in self.sendfax_category_treeview.get_model():
                if c[0] == id:
                    return
            self.sendfax_category_treeview.get_model().append((id, categoria))


    def on_sendfax_delete_button_clicked(self, button):
        treeSelection = self.sendfax_category_treeview.get_selection()
        (model, iterator) = treeSelection.get_selected()
        if iterator is not None:
            model.remove(iterator)


    def on_button_open_attach_clicked(self, button):
        fileDialog = gtk.FileChooserDialog(title='Scegli attachment',
                            parent=self.mainWindow.getTopLevel(),
                            action=GTK_FILE_CHOOSER_ACTION_OPEN,
                             buttons=(gtk.STOCK_CANCEL, GTK_RESPONSE_CANCEL,
                                      gtk.STOCK_OPEN, GTK_RESPONSE_OK))
        response = fileDialog.run()
        if response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()
            for f in self.attachment_treeview.get_model():
                if f[0] == filename:
                    return
            self.attachment_treeview.get_model().append((filename,))
        elif response == GTK_RESPONSE_CANCEL:
            fileDialog.destroy()


    def on_button_delete_attach_clicked(self, button):
        treeSelection = self.attachment_treeview.get_selection()
        (model, iterator) = treeSelection.get_selected()
        if iterator is not None:
            model.remove(iterator)


    def on_sendfax_open_button_clicked(self, button):
        fileDialog = gtk.FileChooserDialog(title='Scegli file',
                            parent=self.mainWindow.getTopLevel(),
                            action=GTK_FILE_CHOOSER_ACTION_OPEN,
                             buttons=(gtk.STOCK_CANCEL, GTK_RESPONSE_CANCEL,
                                      gtk.STOCK_OPEN, GTK_RESPONSE_OK))

        filter = gtk.FileFilter()
        filter.set_name("Immagini TIFF")
        filter.add_mime_type("image/tiff")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.tiff")
        fileDialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("PDF/PS")
        filter.add_mime_type("application/pdf")
        filter.add_mime_type("application/postscript")
        filter.add_pattern("*.pdf")
        filter.add_pattern("*.ps")
        fileDialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Testo")
        filter.add_mime_type("text/plain")
        filter.add_pattern("*.txt")

        fileDialog.add_filter(filter)

        response = fileDialog.run()
        if response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()
            self.sendfax_file_entry.set_text(filename)
        elif response == GTK_RESPONSE_CANCEL:
            fileDialog.destroy()


    def check_before_send(self):
        # controllo se e` stato inserito il soggetto
        if self.subject_textentry.get_text() == '':
            dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
            dialog.set_markup("<b>ATTENZIONE: </b>Inserire il soggetto")
            response = dialog.run()
            dialog.destroy()
            return False
        # controllo se e` stato inserito del testo
        if self.plain_textview.get_buffer().get_char_count() == 0:
            dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
            dialog.set_markup("<b>ATTENZIONE: </b>Inserire il testo del messaggio")
            response = dialog.run()
            dialog.destroy()
            return False
        # controllo se e` stato inserita almeno una categoria od almeno un contatto
        elif len(self.category_treeview.get_model()) ==0 and len(self.contact_treeview.get_model()) == 0:
            dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
            dialog.set_markup(
                "<b>ATTENZIONE: </b>Specificare almeno una categoria od un contatto a cui spedire")
            response = dialog.run()
            dialog.destroy()
            return False
        else:
            return True


    def check_before_sendfax(self):
        # controllo se e` stato inserito il file
        if self.sendfax_file_entry.get_text() == '':
            dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
            dialog.set_markup("<b>ATTENZIONE: </b>Scegliere il file")
            response = dialog.run()
            dialog.destroy()
            return False
        # controllo se e` stato inserita almeno una categoria od un contatto singolo
        elif len(self.sendfax_category_treeview.get_model()) == 0 and len(
            self.contact_fax_treeview.get_model()) == 0:
            dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
            dialog.set_markup("<b>ATTENZIONE: </b>Specificare almeno una categoria od un contatto a cui spedire")
            response = dialog.run()
            dialog.destroy()
            return False
        else:
            return True


    def sendresponse(self, recipients):
        host = 'localhost'
        if hasattr(Environment.conf.Promospam,'mail_host'):
            host = Environment.conf.Promospam.mail_host

        sender = getattr(Environment.conf.Promospam,'mittente','mittente@mail.it')
        message = MIMEMultipart()
        message['Subject'] = 'Riepilogo spedizione'
        message['From'] = sender
        # To guarantee the message ends with a newline
        message.set_charset('iso-8859-15')
        message.epilogue = ''

        buffer = "Messaggio spedito a:\n\n"
        for rec in recipients:
            buffer = buffer + rec + "\n"
        msg = MIMEText(buffer, _subtype='plain')
        msg.set_charset('iso-8859-15')
        msg.add_header('Content-Disposition', 'inline')
        message.attach(msg)

        # Spedisco il messaggio
        message['To'] = sender
        s = smtplib.SMTP()
        s.connect(host=host)
        s.sendmail(sender, sender, message.as_string())
        s.close()


    def sendmail(self, subject, recipients):
        host = 'localhost'
        if hasattr(Environment.conf.Promospam,'mail_host'):
            host = Environment.conf.Promospam.mail_host

        sender = getattr(Environment.conf.Promospam,'mittente','mittente@mail.it')
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender
        # To guarantee the message ends with a newline
        message.set_charset('iso-8859-15')
        message.epilogue = ''

        buffer = self.plain_textview.get_buffer()
        msg = MIMEText(buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(),True)
                ,_subtype='plain')
        msg.set_charset('iso-8859-15')
        msg.add_header('Content-Disposition', 'inline')
        message.attach(msg)

        # allego i files
        model = self.attachment_treeview.get_model()
        for row in model:
            path = row[0]
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(path, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                Encoders.encode_base64(msg)
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=path)
            message.attach(msg)

        # Spedisco i messaggi
        for recipient in recipients:
            message['To'] = recipient
            s = smtplib.SMTP()
            #s.set_debuglevel(True)
            s.connect(host=host)
            s.sendmail(sender, recipient, message.as_string())
            s.close()
        # spedisco riepilogo
        self.sendresponse(recipients)


    def on_send_button_clicked(self, button):
        if self.check_before_send():

            def exitFunc(dialog):
                gobject.source_remove(self.__pulseSourceTag)
                dialog.getTopLevel().destroy()
                # controllo valore di ritorno
                if self._ret_value is not None:
                    self.response_label.set_markup(
                        "<b>ATTENZIONE: </b>alcuni destinatari non sono stati raggiunti")
                else:
                    self.response_label.set_markup(
                        "<b>Spedizione completata con successo</b>")
                return False

            # Instanziare finestra di progresso e schedulare funzione di pulse
            progressDialog = GladeWidget('spam_sending_dialog',
                                         callbacks_proxy=self)
            progressDialog.getTopLevel().set_transient_for(self.mainWindow.getTopLevel())
            progressDialog.getTopLevel().show_all()

            pbar = progressDialog.export_progressbar
            self.__pulseSourceTag = None
            self.__cancelOperation = False

            pbar.set_pulse_step(0.07)

            def pulsePBar():
                pbar.pulse()
                return True

            self.__pulseSourceTag = gobject.timeout_add(33, pulsePBar)

            def sendThread():
                model = self.category_treeview.get_model()
                recipients = []
                for row in model:
                    if self.__cancelOperation:
                        return
                    id_categoria = row[0]
                    # trovo indirizzi a cui spedire di questa categoria
                    strQuery = 'select R.recapito from ' + Environment.connection._schemaAzienda + (
                    '.contatto_categoria_contatto CCC ') + (
                    'left outer join ') + Environment.connection._schemaAzienda + (
                    '.recapito R on R.id_contatto = CCC.id_contatto ') + (
                    'left outer join ') + Environment.connection._schemaAzienda + (
                    '.categoria_contatto CC ') + (
                    'on CCC.id_categoria_contatto = CC.id ') + (
                    'where tipo_recapito = \'E-Mail\' and CC.id = %s')
                    if self.__cancelOperation:
                        return
                    Environment.connection._cursor.execute(strQuery, (id_categoria,))
                    res = Environment.connection._cursor.fetchall()
                    for row_res in res:
                        if self.__cancelOperation:
                            return
                        recipients.append(row_res[0])
                # Aggiungo contatti singoli
                model = self.contact_treeview.get_model()
                for row in model:
                    recipients.append(row[1])

                self._ret_value = self.sendmail(self.subject_textentry.get_text(), recipients)
                gobject.idle_add(exitFunc, progressDialog)

            t = threading.Thread(group=None, target=sendThread,
                                         name='Spam sending thread', args=(),
                                         kwargs={})
            t.setDaemon(True) # FIXME: are we sure? ( he doesn't remember )
            t.start()


    def on_sendfax_button_clicked(self, button):
        if self.check_before_sendfax():

            def exitFunc(dialog):
                gobject.source_remove(self.__pulseSourceTag)
                dialog.getTopLevel().destroy()
                if self.__cancelOperation:
                    self.export_message_label.set_markup("Esecuzione interrotta")
                    self.__cancelOperation = False
                elif self.__exitStatus!=0:
                    self.sendfax_result_label.set_markup(
                        "<b>Attenzione</b>: L' esecuzione del comando e` fallita miseramente, controllare il log per informazioni")
                else:
                    self.sendfax_result_label.set_markup(
                        "<b>" + str(self.faxcount) + " fax accodati con successo</b>")
                return False

            # Instanziare finestra di progresso e schedulare funzione di pulse
            progressDialog = GladeWidget('spam_sending_dialog',
                                         callbacks_proxy=self)
            progressDialog.getTopLevel().set_transient_for(self.mainWindow.getTopLevel())
            progressDialog.title_label.set_markup(
                '<span weight="bold" size="larger">Accodamento fax in corso...</span>')
            progressDialog.getTopLevel().show_all()

            pbar = progressDialog.export_progressbar
            self.__pulseSourceTag = None
            self.__cancelOperation = False

            pbar.set_pulse_step(0.07)


            def pulsePBar():
                pbar.pulse()
                return True

            self.__pulseSourceTag = gobject.timeout_add(33, pulsePBar)


            def sendfaxThread():
                model = self.sendfax_category_treeview.get_model()
                recipients = []
                for row in model:
                    if self.__cancelOperation:
                        return
                    id_categoria = row[0]
                    # trovo indirizzi a cui spedire di questa categoria
                    strQuery = 'select R.recapito from ' + Environment.connection._schemaAzienda + (
                    '.contatto_categoria_contatto CCC ') + (
                    'left outer join ') + Environment.connection._schemaAzienda + (
                    '.recapito R on R.id_contatto = CCC.id_contatto ') + (
                    'left outer join ') + Environment.connection._schemaAzienda + (
                    '.categoria_contatto CC ') + (
                    'on CCC.id_categoria_contatto = CC.id ') + (
                    'where tipo_recapito = \'Fax\' and CC.id = %s')
                    if self.__cancelOperation:
                        return
                    Environment.connection._cursor.execute(strQuery, (id_categoria,))
                    res = Environment.connection._cursor.fetchall()
                    for row_res in res:
                        if self.__cancelOperation:
                            return
                        recipients.append(row_res[0])

                # Aggiungo contatti singoli
                model = self.contact_fax_treeview.get_model()
                for row in model:
                    recipients.append(row[1])

                self.faxcount = 0
                buffer = ''
                for rec in recipients:
                    if self.__cancelOperation:
                        return
                    program_launch = Environment.conf.Promospam.sendfax_program
                    program_params = ' -n -G -f ' + Environment.conf.Promospam.mittente + (
                                     ' -h ') + Environment.conf.Promospam.halyfax_host + (
                                     ' -o ') + Environment.conf.Promospam.halyfax_user + (
                                     ' -s ') + Environment.conf.Promospam.fax_format + (
                                     ' -d ') + rec + ' ' + self.sendfax_file_entry.get_text()

                    if os.name == 'nt':
                        exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
                        id, self.__exitStatus = os.waitpid(exportingProcessPid, 0)
                        self.__exitStatus = self.__exitStatus >> 8
                        buffer = ''
                    else:
                        command = program_launch + program_params
                        process = popen2.Popen3(command, True)
                        buf = process.fromchild.readlines()
                        for line in buf:
                            buffer = buffer + line
                        self.__exitStatus = process.wait()
                    if self.__exitStatus == 0:
                        self.faxcount = self.faxcount + 1
                gobject.idle_add(exitFunc, progressDialog)


            t = threading.Thread(group=None, target=sendfaxThread,
                                         name='Sendfax thread', args=(),
                                         kwargs={})
            t.setDaemon(True) # FIXME: are we sure? ( he does'nt remember )
            t.start()


    def on_sending_mail_progress_dialog_response(self, dialog, responseId):
        if responseId == GTK_RESPONSE_CANCEL:
            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)
            self.__cancelOperation = True
            dialog.destroy()


    def on_sending_fax_progress_dialog_response(self, dialog, responseId):
        if responseId == GTK_RESPONSE_CANCEL:
            if self.__pulseSourceTag is not None:
                gobject.source_remove(self.__pulseSourceTag)
            self.__cancelOperation = True
            dialog.destroy()


    def ricercaContatto(self, source):

        def on_ricerca_contatto_email_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()

            email = None
            for recapito in anag.dao.recapiti:
                if recapito.tipo_recapito == 'E-Mail':
                    email = recapito.recapito

            if email is None:
                dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
                dialog.set_markup("<b>ATTENZIONE: </b>Questo contatto non dispone di un E-Mail")
                response = dialog.run()
                dialog.destroy()
            else:
                model = self.contact_treeview.get_model()
                model.append((anag.dao.cognome + ' ' + anag.dao.nome, email))


        def on_ricerca_contatto_fax_hide(anagWindow, anag):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()

            fax = None
            for recapito in anag.dao.recapiti:
                if recapito.tipo_recapito == 'Fax':
                    fax = recapito.recapito

            if fax is None:
                dialog = gtk.MessageDialog(self.mainWindow.getTopLevel(),
                                        GTK_DIALOG_MODAL
                                        | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_WARNING, GTK_BUTTONS_OK)
                dialog.set_markup("<b>ATTENZIONE: </b>Questo contatto non dispone di un numero Fax")
                response = dialog.run()
                dialog.destroy()
            else:
                model = self.contact_fax_treeview.get_model()
                model.append((anag.dao.cognome + ' ' + anag.dao.nome, fax))

        from promogest.ui.RicercaContatti import RicercaContatti
        anag = RicercaContatti()

        anagWindow = anag.getTopLevel()
        if source == 'contact_fax_add_button':
            anagWindow.connect("hide", on_ricerca_contatto_fax_hide, anag)
        elif source == 'contact_add_button':
            anagWindow.connect("hide", on_ricerca_contatto_email_hide, anag)
        anagWindow.set_transient_for(self.mainWindow.getTopLevel())
        anagWindow.show_all()


    def on_contact_add_button_clicked(self, button):
        self.ricercaContatto(button.name)


    def on_contact_delete_button_clicked(self, button):
        if button.name == 'contact_delete_button':
            treeSelection = self.contact_treeview.get_selection()
        elif button.name == 'contact_fax_delete_button':
            treeSelection = self.contact_fax_treeview.get_selection()
        (model, iterator) = treeSelection.get_selected()
        if iterator is not None:
            model.remove(iterator)
