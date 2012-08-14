# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>
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

import os
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *
from promogest.dao.DaoUtils import *
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML
from promogest.lib.html2csv import html2csv
from promogest.ui.PrintDialog import PrintDialogHandler
#try:
    #import ho.pisa as pisa
#except:
    #print "ERRORE NELL'IMPORT DI PISA"
    #import pisaLib.ho.pisa as pisa

try:
    from  xhtml2pdf import pisa
except:
    print "ERRORE NELL'IMPORT DI PISA"
    import pisaLib.ho.pisa as pisa



class HtmlViewer(GladeWidget):

    def __init__(self, pageData=None):
        self._htmlTemplate = None

        GladeWidget.__init__(self, root='visualizzatore_html',
                path="htmlviewer.glade")
        self._window = self.visualizzatore_html
        self.windowTitle = "Statistiche"
        self.placeWindow(self._window)
        self.pageData= pageData
        self.html = ""
        self.drawHtml()

    def drawHtml(self):
        self.detail = createHtmlObj(self)
        self.html_scrolledwindow.add(self.detail)
        self.html_scrolledwindow.show()
        self.refreshHtml()

    def on_pdf_button_clicked(self, button):

        f = self.html
        g = file(Environment.tempDir+".temp.pdf", "wb")
        pdf = pisa.CreatePDF(str(f), g)
        g .close()
        anag = PrintDialogHandler(self, self.windowTitle)
        anagWindow = anag.getTopLevel()
        returnWindow = self.getTopLevel().get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    def refreshHtml(self, dao=None):
        self.html = renderTemplate(self.pageData)
        renderHTML(self.detail, self.html)

    def on_quit_button_clicked(self, button):
        self.destroy()
        return None

    def on_csv_button_clicked(self, button):

        fileDialog = gtk.FileChooserDialog(title='Salvataggio file csv',
                                           parent=self.getTopLevel(),
                                           action=GTK_FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    GTK_RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    GTK_RESPONSE_OK),
                                           backend=None)
        folder = ''
        try:
            folder = Environment.documentsDir
        except:
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        fileDialog.set_current_folder(folder)

        f_name = self.pageData["nomestatistica"].lower()\
                                            .replace(" ", "_").strip()
        fileDialog.set_current_name(f_name+'.csv')

        response = fileDialog.run()

        if response == GTK_RESPONSE_OK:
            filename = fileDialog.get_filename()
            parser = html2csv()
            parser.feed(self.html)
            open(filename, 'w+b').write(parser.getCSV())
        fileDialog.destroy()
