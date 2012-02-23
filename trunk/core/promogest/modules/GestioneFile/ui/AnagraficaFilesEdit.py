# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

import hashlib
import datetime
import base64
from base64 import b64decode
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.modules.GestioneFile.dao.Immagine import ImageFile
from promogest.modules.GestioneFile.dao.ArticoloImmagine import ArticoloImmagine

class AnagraficaFilesEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle prima nota cassa """
    def __init__(self, anagrafica, daoArticolo=None):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'anagrafica_gestione_file_detail_vbox',
                'Informazioni File.',
                gladeFile='GestioneFile/gui/_anagrafica_gestione_file_elements.glade',
                module=True)
        self._widgetFirstFocus = self.denominazione_entry
        self.anagrafica = anagrafica
        self.daoArticolo = daoArticolo

    def draw(self, cplx=False):
        return

    def setDao(self, dao):
        if dao is None:
            self.dao = ArticoloImmagine()
        else:
            #self.dao = ArticoloImmagine().getRecord(id=(dao.id_articolo,dao.id_immagine)) #ricontrollare
            self.dao = dao
        self._refresh()
        return self.dao

    def _refresh(self):
        if self.dao.id_articolo:
            try:
                img = ImageFile().getRecord(id=self.dao.id_immagine)
                fingerprint =Environment.CACHE+"/"+img.fingerprint
                f = open(fingerprint, "w")
                f.write(b64decode(img.data))
                f.close()
                self.art_image.set_from_file(fingerprint)
            except:
                self.art_image.set_from_file("")
            self.denominazione_entry.set_text(self.dao.immagine.denominazione)
        else:
            self.art_image.set_from_file("")
            self.denominazione_entry.set_text("")

    def clear(self):
        self.art_image.set_from_file("")
        self.denominazione_entry.set_text("")
        return

    def on_gestione_file_filechooserbutton_file_set(self, filechooser):
        size = 200, 200
        self.photo_src= filechooser.get_filename()
        self.art_image.set_from_file(self.photo_src)
        f = open(self.photo_src, "r")
        g = f.read()
        self.imgblob = base64.b64encode(str(g))
        f.close()


    def saveDao(self, tipo=None):
        if self.gestione_file_filechooserbutton.get_file():
            #print "LA FOTO SELEZIONATA", self.gestione_file_filechooserbutton.get_file().get_path(), self.gestione_file_filechooserbutton.get_file(), self.imgblob
            img = ImageFile().getRecord(id=self.dao.id_immagine)
            if not img:
                img = ImageFile()
            img.denominazione = self.denominazione_entry.get_text() or ""
            img.fingerprint = hashlib.md5(self.imgblob).hexdigest()
            img.data = self.imgblob
            img.persist()
            self.dao.id_articolo = self.daoArticolo.id
            self.dao.id_immagine = img.id
            self.dao.persist()
        self.clear()
