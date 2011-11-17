# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import hashlib
from promogest.ui.utils import orda
from promogest import Environment
from promogest.dao.Setconf import SetConf
from promogest.dao.SectionUser import SectionUser
from GladeWidget import GladeWidget
import datetime

class SetConfUI(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main):
        pass

if not SetConf().select(key="rotazione_primanota", section="Primanota"):
    kee = SetConf()
    kee.key = "rotazione_primanota"
    kee.value ="mensile"
    kee.section = "Primanota"
    kee.tipo_section = "Generico"
    kee.description = "Gestione della creazione della prima nota, valori ammessi, MESE, SETTIMANA, TRIMESTRE"
    kee.active = True
    kee.date = datetime.datetime.now()
    kee.persist()
#-------------------------------------------------------------------------------------------
if not SetConf().select(key="install_code",section="Master"):
    kmm = SetConf()
    kmm.key = "install_code"
    kmm.value =str(hashlib.sha224("aziendapromo"+orda("aziendapromo")).hexdigest())
    kmm.section = "Master"
    kmm.description = "codice identificativo della propria installazione"
    kmm.tipo_section = "General"
    kmm.tipo = "ONE BASIC"
    kmm.active = True
    kmm.date = datetime.datetime.now()
    kmm.persist()

codice=  SetConf().select(key="install_code",section="Master")
if codice:
    if codice[0].value =="ad2a57ed2bd4d4df494e174b576cf8e822a18be2e1b074871c69b31f":
        codice[0].value = "8f0eff136d1fb1d2b76fde5de7c83eb60d558c4f155ee687dcac5504"
        codice[0].persist()

#---------------------------------------------------------------------------- OK
if not SetConf().select(key="altezza_logo",section="Documenti"):
    koo = SetConf()
    koo.key = "altezza_logo"
    koo.value ="110"
    koo.section = "Documenti"
    koo.description = "altezza logo documento"
    koo.tipo_section = "Generico"
    koo.active = True
    koo.date = datetime.datetime.now()
    koo.persist()
#---------------------------------------------------------------------------- OK
if not SetConf().select(key="larghezza_logo",section="Documenti"):
    kpp = SetConf()
    kpp.key = "larghezza_logo"
    kpp.value ="300"
    kpp.section = "Documenti"
    kpp.description = "larghezza logo documento"
    kpp.tipo_section = "Generico"
    kpp.active = True
    kpp.date = datetime.datetime.now()
    kpp.persist()

#---------------------------------------------------------------------------- OK
if not SetConf().select(key="ricerca_per",section="Documenti"):
    krr = SetConf()
    krr.key = "ricerca_per"
    krr.value ="codice"
    krr.section = "Documenti"
    krr.description = "Preimposta un tipo di ricerca Valori possibili:(codice,descrizione,codice_a_barre,codice_articolo_fornitore "
    krr.tipo_section = "Generico"
    krr.active = True
    krr.visible = True
    krr.date = datetime.datetime.now()
    krr.persist()
#-----------------------------------------------------------------------------

if not SetConf().select(key="cartella_predefinita",section="General"):
    krr = SetConf()
    krr.key = "cartella_predefinita"
    krr.value = Environment.documentsDir
    krr.section = "General"
    krr.description = "Cartella di salvataggio predefinita"
    krr.tipo_section = "Generico"
    krr.active = True
    krr.visible = True
    krr.date = datetime.datetime.now()
    krr.persist()

if not SetConf().select(key="gestione_totali_mercatino",section="General"):
    krr = SetConf()
    krr.key = "gestione_totali_mercatino"
    krr.value = "False"
    krr.section = "General"
    krr.description = "Gestione totali mercatino"
    krr.tipo_section = "Generico"
    krr.active = True
    krr.tipo = "bool"
    krr.visible = True
    krr.date = datetime.datetime.now()
    krr.persist()


if not SetConf().select(key="color_base",section="Documenti"):
    kss = SetConf()
    kss.key = "color_base"
    kss.value ="#F9FBA7"
    kss.section = "Documenti"
    kss.description = "Preimposta il colore di base "
    kss.tipo_section = "Generico"
    kss.tipo = "Colore"
    kss.active = True
    kss.date = datetime.datetime.now()
    kss.persist()
#------------------------------------------------------------------------------
if not SetConf().select(key="color_text",section="Documenti"):
    ktt = SetConf()
    ktt.key = "color_text"
    ktt.value ="black"
    ktt.section = "Documenti"
    ktt.description = "Preimposta il colore del testo "
    ktt.tipo_section = "Generico"
    ktt.tipo = "Colore"
    ktt.active = True
    ktt.date = datetime.datetime.now()
    ktt.persist()
#------------------------------------------------------------------------------
if not SetConf().select(key="feed",section="Feed"):  # OK
    kuu = SetConf()
    kuu.key = "feed"
    kuu.value = "True"
    kuu.section = "Feed"
    kuu.description = "Notizie nella home"
    kuu.tipo_section = "Generico"
    kuu.active = True
    kuu.tipo = "bool"
    kuu.date = datetime.datetime.now()
    kuu.persist()
#ff = SetConf().select(key="feed", section="Feed")
#if ff:
#    ff[0].tipo = "bool"
#    ff[0].persist()
#-------------------------------------------------------------------------------
if not SetConf().select(key="smtpserver", section="Smtp"):
    kvv = SetConf()
    kvv.key = "smtpserver"
    kvv.value =""
    kvv.section = "Smtp"
    kvv.tipo_section = "Generico"
    kvv.description = "server per l'invio della posta"
    kvv.active = True
    kvv.date = datetime.datetime.now()
    kvv.persist()
#-----------------------------------------------------------------------------
if not SetConf().select(key="emailmittente", section="Smtp"):
    kzz = SetConf()
    kzz.key = "emailmittente"
    kzz.value =""
    kzz.section = "Smtp"
    kzz.tipo_section = "Generico"
    kzz.description = "Email del mittente"
    kzz.active = True
    kzz.tipo = "str"
    kzz.date = datetime.datetime.now()
    kzz.persist()
#-----------------------------------------------------------------------------
if not SetConf().select(key="multilinealimite", section="Multilinea"):
    kaa = SetConf()
    kaa.key = "multilinealimite"
    kaa.value ="60"
    kaa.section = "Multilinea"
    kaa.tipo_section = "Generico"
    kaa.description = "Gestione dei multilinea nei documenti"
    kaa.active = True
    kaa.tipo = "int"
    kaa.date = datetime.datetime.now()
    kaa.persist()

#----------------------------------------------------------------------------- ok
bb = SetConf().select(key="decimals", section="Numbers")
if not bb:
    kbb = SetConf()
    kbb.key = "decimals"
    kbb.value ="3"
    kbb.section = "Numbers"
    kbb.tipo_section = "Generico"
    kbb.description = "Gestione dei decimali"
    kbb.active = True
    kbb.tipo = "int"
    kbb.date = datetime.datetime.now()
    kbb.persist()
#else:
#    try:
#        int(bb[0].value)
#    except:
#        bb[0].value ="2"
#        bb[0].persist()
# ---------------------------------------------------------------------------- OK
aa = SetConf().select(key="batch_size", section="Numbers")
if not aa:
    kcc = SetConf()
    kcc.key = "batch_size"
    kcc.value ="15"
    kcc.section = "Numbers"
    kcc.tipo_section = "Generico"
    kcc.description = "Gestione dei batchSize"
    kcc.active = True
    kcc.tipo = "int"
    kcc.date = datetime.datetime.now()
    kcc.persist()
#else:
#    try:
#        int(aa[0].value)
#    except:
#        aa[0].value ="15"
#        aa[0].persist()
# ------------------------------------------------------------------------- OK
cc = SetConf().select(key="combo_column", section="Numbers")
if not cc:
    kdd = SetConf()
    kdd.key = "combo_column"
    kdd.value ="3"
    kdd.section = "Numbers"
    kdd.tipo_section = "Generico"
    kdd.description = "Gestione dei combo_column cioè le colonne nelle combobox"
    kdd.active = True
    kdd.tipo = "int"
    kdd.date = datetime.datetime.now()
    kdd.persist()
#else:
#    try:
#        int(cc[0].value)
#    except:
#        cc[0].value ="3"
#        cc[0].persist()
# -----------------------------------------------------------------------ok
if not SetConf().select(key="zeri_in_riga",section="Stampa"):
    kuu = SetConf()
    kuu.key = "zeri_in_riga"
    kuu.value =""
    kuu.section = "Stampa"
    kuu.description = "Visualizza gli zeri nelle righe documento"
    kuu.tipo_section = "Generico"
    kuu.active = False
    kuu.tipo = "bool"
    kuu.date = datetime.datetime.now()
    kuu.persist()
#ff = SetConf().select(key="zeri_in_riga", section="Stampa")
#if ff:
#    ff[0].tipo = "bool"
#    ff[0].persist()
#------------------------------------------------------------------------ok
if not SetConf().select(key="zeri_in_totali",section="Stampa"):
    kuu1 = SetConf()
    kuu1.key = "zeri_in_totali"
    kuu1.value =""
    kuu1.section = "Stampa"
    kuu1.description = "Visualizza gli zeri nei totali"
    kuu1.tipo_section = "Generico"
    kuu1.active = False
    kuu1.tipo = "bool"
    kuu1.date = datetime.datetime.now()
    kuu1.persist()
#ff1 = SetConf().select(key="zeri_in_totali", section="Stampa")
#if ff1:
#    ff1[0].tipo = "bool"
#    ff1[0].persist()