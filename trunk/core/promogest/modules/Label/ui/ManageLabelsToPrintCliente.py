# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from decimal import *
from promogest.ui.gtk_compat import *
import os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.lib.sla2pdf.Sla2Pdf_ng import Sla2Pdf_ng
from promogest.lib.sla2pdf.SlaTpl2Sla import SlaTpl2Sla as SlaTpl2Sla_ng
#from promogest.lib.SlaTpl2Sla import SlaTpl2Sla
from promogest.ui.PrintDialog import PrintDialogHandler

class ManageLabelsToPrintCliente(GladeWidget):

    def __init__(self, mainWindow=None,daos=None, cliente=None):
        """Widget di transizione per visualizzare e confermare gli oggetti
            preparati per la stampa ( Multi_dialog.glade tab 1)
        """
        GladeWidget.__init__(self, root='label_clienti_dialog',
                        path='Label/gui/label_clienti_dialog.glade',
                        isModule=True)
        self.mainWindow = mainWindow
        self.cliente = cliente
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        path=Environment.labelTemplatesDir  # insert the path to the directory of interest
        # preleva i file .sla dalla cartella
        dirList=os.listdir(path)
        for fname in dirList:
            if os.path.splitext(fname)[1] ==".sla":
                self.select_template_listore.append([fname],)

    def get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def on_ok_button_clicked(self,button):
        self._folder = setconf("General", "cartella_predefinita") or ""
        if self._folder == '':
            if os.name == 'posix':
                self._folder = os.environ['HOME']
            elif os.name == 'nt':
                self._folder = os.environ['USERPROFILE']
        self.resultList= []
        param = [self.cliente.dictionary(complete=True)]
        template_file= self.get_active_text(self.template_combobox)
        if template_file:
            slafile = Environment.labelTemplatesDir +template_file
        else:
            messageInfo(msg="NESSUN TEMPLATE LABEL SELEZIONATO?")
            return
        stpl2sla = SlaTpl2Sla_ng(slafile=None,label=True,
                                    report=False,
                                    objects=param,
                                    daos=[], #self.daos,
                                    slaFileName=slafile,
                                    pdfFolder=self._folder,
                                    classic=False,
                                    template_file=template_file,
                                    )
        ecco= Sla2Pdf_ng(slafile=self._folder+"_temppp.sla").translate()
        g = file(Environment.tempDir+".temp.pdf", "wb")
        g.write(ecco)
        g.close()
        anag = PrintDialogHandler(self,g)

    def on_discard_button_clicked(self, button):
        self.getTopLevel().destroy()
