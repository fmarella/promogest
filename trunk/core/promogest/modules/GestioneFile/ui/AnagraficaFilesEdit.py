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
    def __init__(self, anagrafica, articolo=None):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'anagrafica_gestione_file_detail_vbox',
                'Informazioni File.',
                gladeFile='GestioneFile/gui/_anagrafica_gestione_file_elements.glade',
                module=True)
        self._widgetFirstFocus = self.art_image
        self.anagrafica = anagrafica
        self.daoArticolo = articolo

    def draw(self, cplx=False):
        return

    def setDao(self, dao):
        if dao is None:
            self.dao = ArticoloImmagine()
        else:
            self.dao = ArticoloImmagine().getRecord(id=dao.id)
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

    def clear(self):
        return

    def on_gestione_file_filechooserbutton_file_set(self, filechooser):
        #import StringIO
        #output = StringIO.StringIO()
        #image.save(output)
        #contents = output.getvalue()
        #output.close()

        print "LA FOTO SELEZIONATA",  filechooser.get_file().get_path(), filechooser.get_file()
        size = 200, 200
        self.photo_src= filechooser.get_filename()
        self.art_image.set_from_file(self.photo_src)
        #im1 = Image.fromstring(self.photo_src)
        f = open(self.photo_src, "r")
        g = f.read()
        #im = Image.open(g)
        #im.thumbnail(size, Image.ANTIALIAS)
        #im.tostring(self.photo_src + ".thumbnail)
        self.imgblob = base64.b64encode(str(g))
        f.close()


    def saveDao(self, tipo=None):
        if self.gestione_file_filechooserbutton.get_file():
            print "LA FOTO SELEZIONATA", self.gestione_file_filechooserbutton.get_file().get_path(), self.gestione_file_filechooserbutton.get_file()
        else:
            print "NESSUNA FOTO SELEZIONATA POSSO METTERE UN CONTROLO", self.art_image.get_file()
        return
        if self.dao.id_articolo:
            if a:
                a=a[0]
                img = ImageFile().getRecord(id=a.id_immagine)
            else:
                a= UtenteImmagine()
                img = ImageFile()
            img.denominazione = "nessuno"
            #img.altezza
            img.larghezza = 200
            img.fingerprint = hashlib.md5(self.imgblob).hexdigest()
            img.data = self.imgblob
            img.persist()
            a.id_utente = self.dao.id
            a.id_immagine = img.id
            a.persist()
        self.dao.persist()
        self.clear()
