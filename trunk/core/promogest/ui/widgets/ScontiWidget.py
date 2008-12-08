# -*- coding: iso-8859-15 -*-

"""
    Promogest
    Copyright (C) 2008 by Promotux Informatica - http://www.promotux.it/
"""

import gtk
from CustomLabel import CustomLabel
from promogest import Environment

class ScontiWidget(CustomLabel):

    def __init__(self, str1=None, str2=None):
        CustomLabel.__init__(self, str1, str2)
        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'sconti16x16.png')
        self.image.set_from_pixbuf(pbuf)

        self._scontiPercentuali = True
        self._scontiValore = True

        self.connect('clicked', self.on_button_clicked, str1)


    def on_button_clicked(self, widget, button, windowTitle):
        #richiama la gestione degli sconti

        def on_richiamo_destroy(anagWindow):
            self.button.set_active(False)

        def on_sconti_hide(anagWindow):
            if anag.listSconti is None:
                anag.listSconti = []

            container = {"sconti": anag.listSconti,
                        "applicazione": anag.stringApplicazione}
            self._container = container
            stringSconti = self.scontiStringRefresh(anag.listSconti)
            stringApplicazione = anag.stringApplicazione
            self.setCustomLabel(labelText=stringSconti,
                                buttonText=' (' + stringApplicazione + ')',
                                container=container)
            anagWindow.destroy()


        if self.button.get_property('active') is False:
            return

        from Sconti import Sconti
        anag = Sconti(windowTitle, self.getSconti(),
                                   self.getApplicazione(),
                                   self._scontiPercentuali,
                                   self._scontiValore)

        anagWindow = anag.getTopLevel()
        returnWindow = self.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("destroy",
                           on_richiamo_destroy)
        anagWindow.connect("hide",
                           on_sconti_hide)


    def scontiStringRefresh(self, listSconti):
        stringSconti = ''
        for s in listSconti:
            decimals = '2'
            tipo = s["tipo"]
            if tipo == 'percentuale':
                tipo = '%'
            elif tipo == 'valore':
                tipo = ''
                decimals = Environment.conf.decimals
            valore = ('%10.' + str(decimals) + 'f') % float(s["valore"])
            stringSconti = stringSconti + valore + tipo + '; '
        return stringSconti


    def getSconti(self):
        return self._container["sconti"]


    def getApplicazione(self):
        return self._container["applicazione"]


    def getStringaSconti(self):
        return self.scontiStringRefresh(self.getSconti())


    def setAPercentuale(self, value = True):
        self._scontiPercentuali = value


    def setAValore(self, value = True):
        self._scontiValore = value


    def setValues(self, sco=[], applic='scalare', fromDao=True):
        applicazione = 'scalare'
        sconti = []
        if applic == 'scalare' or applic == 'non scalare':
            applicazione = applic
        if not(fromDao):
            sconti = sco
        else:
            for s in sco:
                sconti.append({"valore": s.valore, "tipo": s.tipo_sconto})

        container = {"sconti": sconti,
                    "applicazione": applicazione}
        self.setCustomLabel(labelText=self.scontiStringRefresh(sconti),
                            buttonText=' (' + applicazione + ')',
                            container=container)


    def clearValues(self):
        self.setValues()


#gobject.type_register(ScontiCustomLabel)
