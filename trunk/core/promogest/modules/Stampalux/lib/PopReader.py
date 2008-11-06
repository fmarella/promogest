# -*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
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

import getpass, poplib, email, pdb
from promogest import Environment


##class fetchPopPartecipazioni(object):
##    """classe di recupero email dal pop di stampalux , parsa le email e genera un dizionario pronto per
##    l'inserimento in schede lavorazione """
##    def __init_(self):
try:
	mail_box = poplib.POP3(Environment.conf.Stampalux.mail_server)
	mail_box.user(Environment.conf.Stampalux.mail_user)
	mail_box.pass_(Environment.conf.Stampalux.mail_password)
	numMessages = len(mail_box.list()[1])
	returned_mail_list = []
except:
	print "ATTENZIONE: SETTARE LE CONFIGURAZIONI PER LA LETTURA DELLA CASELLA DI MAIL"
	pass
##        print dictionary

def fetchMail():
    emailDictList=[]
    emailDictCodList = []
    emailDict = {}
    emailDictCod = {}
    campi = ["Subject","From","Nome_sposo","Nome_sposa","messaggio alternativo a annunciano...",
            "cerimonia","nome_luogo_cerimonia","localita_matrimonio","Citta_matrimonio",
            "Data_matrimonio","Ora_matrimonio","Citta_sposo","Via_e_num_sposo","num_sposo",
            "Citta_sposa","sito_omaggio","Via_e_num_sposa","Num_sposa","Indirizzo_coniugale","Luogo_ricevimento",
            "biglietto_bomboniera","gradita_conferma","Commenti","carattere","colore","Luogo_spedizione",
            "nome","Presso","Via_e_num","Citta","Provincia","CAP","telefono","Cellulare","codicefiscale",
            "Note_aggiuntive","partitaiva","pagamento","documento","autorizzo_si","privacy","pagina","spesa","TOTALE",
            "Percentuale_di_sconto","Modulo inviato dalla pagina","Percentuale di sconto","CODICE"]
    for m in range(numMessages):
        email = mail_box.retr(m+1)[1]
        if "Form ordine partecipazioni" in email[18]:
            for campo in campi:
                for i in range(len(email[21:120])):
                    if email[21:120][i].split(":")[0].strip() == campo and campo == "CODICE":
                        articoli = email[21:120][i].split("---")
                        for articolo in articoli.strip():
                            articolo = articolo.split()[1][4:].replace("\xa0", "").strip()
                            quantita = articolo.split()[-1].replace("\xa0", "").strip()
                            emailDictCod[articolo] = int(quantita)
                        emailDict['articoli'] = emailDictCod
                    elif email[21:120][i].split(":")[0].strip() == campo:
                        valoreList = []
                        f = i+1
                        righe = ""
                        while f < len(email[21:120]) and  email[21:120][f].split(":")[0].strip() not in campi and len(email[21:120][f]) != 0:
                            valore_ = email[21:120][f].replace("\xe0","à")\
                                                                    .replace("\xa0", "")\
                                                                    .replace("\xf2", "ò")\
                                                                    .strip()
                            righe = righe +" " + valore_
                            valore_ = ""
                            f+=1
                        try:
                            valore = email[21:120][i].split(":")[1].replace("\xc3","à")\
                                                                    .replace("\xa0", "")\
                                                                    .replace("\xc3\xb2", "ò")\
                                                                    .strip() + ""+ righe
                        except :
                            valore = ""
                        if campo != "CODICE":
                            emailDict[campo] = valore

            emailDictList.append(emailDict)
            emailDictCod = {}
    returned_mail_list = emailDictList



