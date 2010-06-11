#!/usr/bin/env python
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

#import getpass, poplib, email, pdb
#from promogest import Environment


##class fetchPopPartecipazioni(object):
##    """classe di recupero email dal pop di stampalux , parsa le email e genera un dizionario pronto per
##    l'inserimento in schede lavorazione """
##    def __init_(self):
#try:
	#mail_box = poplib.POP3(Environment.conf.Stampalux.mail_server)
	#mail_box.user(Environment.conf.Stampalux.mail_user)
	#mail_box.pass_(Environment.conf.Stampalux.mail_password)
	#numMessages = len(mail_box.list()[1])
	#returned_mail_list = []
#except:
	#print "ATTENZIONE: SETTARE LE CONFIGURAZIONI PER LA LETTURA DELLA CASELLA DI MAIL"
	#pass
###        print dictionary

campi = ["Subject","From","Nome_sposo","Nome_sposa","messaggio alternativo a annunciano...",
            "cerimonia","nome_luogo_cerimonia","localita_matrimonio","Citta_matrimonio",
            "Data_matrimonio","Ora_matrimonio","Citta_sposo","Via_e_num_sposo","num_sposo",
            "Citta_sposa","sito_omaggio","Via_e_num_sposa","Num_sposa","Indirizzo_coniugale","Luogo_ricevimento",
            "biglietto_bomboniera","gradita_conferma","Commenti","carattere","colore","Luogo_spedizione",
            "nome","Presso","Via_e_num","Citta","Provincia","CAP","telefono","Cellulare","codicefiscale",
            "Note_aggiuntive","partitaiva","pagamento","documento","autorizzo_si","privacy","pagina","spesa","TOTALE",
            "Percentuale_di_sconto","Modulo inviato dalla pagina","Percentuale di sconto","CODICE"]
#email = file("Form ordine partecipazioni.eml","r")
#TEXT = email.readlines()
#for line in TEXT:
    #lista = line.split(":")
    #campo = lista[0].strip()
    ##valore = lista[1].strip()
    #if campo == "Subject":
        #if lista[1].strip() != "Form ordine partecipazioni":
            #raise Exception,"errore email di tipo errato"
    #if campo == "From":
        #emailFrom = lista[1].strip()
    #elif campo == "Nome_sposo":
        #nome_sposo = lista[1].strip()
    #elif campo == "Cognome_sposo":
        #cognome_sposo = lista[1].strip()
    #elif campo == "Nome_sposa":
        #nome_sposa = lista[1].strip()
    #elif campo == "Cognome_sposa":
        #cognome_sposa = lista[1].strip()
    #elif campo == "messaggio alternativo a annunciano...":
        #messaggio_alternativo  = lista[1].strip()
    #elif campo == "cerimonia":
        #cerimonia  = lista[1].strip()
    #elif campo == "nome_luogo_cerimonia":
        #nome_luogo_cerimonia  = lista[1].strip()
    #elif campo == "nome_luogo_cerimonia":
        #nome_luogo_cerimonia  = lista[1].strip()
    #elif campo == "localita_matrimonio":
        #localita_matrimonio  = lista[1].strip()
    #elif campo == "Citta_matrimonio":
        #citta_matrimonio  = lista[1].strip()
    #elif campo == "Data_matrimonio":
        #data_matrimonio  = lista[1].strip()
    #elif campo == "Data_matrimonio":
        #data_matrimonio  = lista[1].strip()
    #elif campo == "Ora_matrimonio":
        #ora_matrimonio  = lista[1].strip()
    #elif campo == "Citta_sposo":
        #citta_sposo  = lista[1].strip()
    #elif campo == "Via_e_num_sposo":
        #via_e_num_sposo  = lista[1].strip()
    #elif campo == "num_sposo":
        #num_sposo  = lista[1].strip()
    #elif campo == "Citta_sposa":
        #citta_sposa  = lista[1].strip()
    #elif campo == "Via_e_num_sposa":
        #via_e_num_sposa  = lista[1].strip()
    #elif campo == "Num_sposa":
        #num_sposa  = lista[1].strip()
    #elif campo == "Indirizzo_coniugale":
        #indirizzo_coniugale  = lista[1].strip()
    #elif campo == "Luogo_ricevimento":
        #luogo_ricevimento  = lista[1].strip()
    #elif campo == "biglietto_bomboniera":
        #biglietto_bomboniera  = lista[1].strip()
    #elif campo == "gradita_conferma":
        #gradita_conferma  = lista[1].strip()
    #elif campo == "Commenti":
        #commenti  = lista[1].strip()
    #elif campo == "carattere":
        #carattere_stampa  = lista[1].strip()
    #elif campo == "colore":
        #colore_stampa  = lista[1].strip()
    #elif campo == "sito_omaggio":
        #sito_omaggio  = lista[1].strip()
    #elif campo == "Luogo_spedizione":
        #luogo_spedizione  = lista[1].strip()
    #elif campo == "nome":
        #nome  = lista[1].strip()
    #elif campo == "Presso":
        #Presso  = lista[1].strip()
    #elif campo == "Via_e_num":
        #via_e_num  = lista[1].strip()
    #elif campo == "Citta":
        #citta  = lista[1].strip()
    #elif campo == "Provincia":
        #provincia  = lista[1].strip()
    #elif campo == "CAP":
        #cap  = lista[1].strip()
    #elif campo == "telefono":
        #telefono  = lista[1].strip()
    #elif campo == "Cellulare":
        #cellulare  = lista[1].strip()
    #elif campo == "codicefiscale":
        #codicefiscale  = lista[1].strip()
    #elif campo == "Note_aggiuntive":
        #note_aggiuntive  = lista[1].strip()
    #elif campo == "pagamento":
        #pagamento  = lista[1].strip()
    #elif campo == "documento":
        #documento  = lista[1].strip()
    #elif campo == "autorizzo_si":
        #autorizzo_si  = lista[1].strip()
    #elif campo == "privacy":
        #privacy  = lista[1].strip()
    #elif campo == "pagina":
        #pagina  = lista[1].strip()
    #elif campo == "spesa":
        #pagina  = lista[1].strip()
    #elif campo == "PRODOTTO":
        #prodotto  = lista[1].strip()
    #elif campo == "CODICE PARTECIPAZIONE":
        #codParte = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')
        #quantitaParte = lista[2].strip().split("-")[0].strip()[1:-1]
    #elif campo == "CODICE INVITO":
        #codInvito = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')
        #quantitaInvito = lista[2].strip().split("-")[0].strip()[1:-1]
        #print codInvito, quantitaInvito
    #elif campo == "CODICE BOMBONIERA":
        #codBombo = lista[1].strip().split("(")[0].strip()[1:-1].replace("Art.",'')
        #quantitaBombo = lista[2].strip().split("-")[0].strip()[1:-1]
        #print codBombo, quantitaBombo
    #elif campo == "PERCENTUALE DI SCONTO APPLICATO":
        #percentualeSconto = lista[1].strip()[0:-1]
        #print percentualeSconto
    #elif campo == "COSTO STAMPA APPLICATO":
        #costoStampa = lista[1].strip()
    #elif campo == "TOTALE":
        #totale = lista[1].strip()[1:].strip()
        #print totale
#email.close()



#def fetchMail():
    #emailDictList=[]
    #emailDictCodList = []
    #emailDict = {}
    #emailDictCod = {}
    #campi = ["Subject","From","Nome_sposo","Nome_sposa","messaggio alternativo a annunciano...",
            #"cerimonia","nome_luogo_cerimonia","localita_matrimonio","Citta_matrimonio",
            #"Data_matrimonio","Ora_matrimonio","Citta_sposo","Via_e_num_sposo","num_sposo",
            #"Citta_sposa","sito_omaggio","Via_e_num_sposa","Num_sposa","Indirizzo_coniugale","Luogo_ricevimento",
            #"biglietto_bomboniera","gradita_conferma","Commenti","carattere","colore","Luogo_spedizione",
            #"nome","Presso","Via_e_num","Citta","Provincia","CAP","telefono","Cellulare","codicefiscale",
            #"Note_aggiuntive","partitaiva","pagamento","documento","autorizzo_si","privacy","pagina","spesa","TOTALE",
            #"Percentuale_di_sconto","Modulo inviato dalla pagina","Percentuale di sconto","CODICE"]
    ##for m in range(numMessages):
    #email = mail_box.retr(m+1)[1]
    #if "Form ordine partecipazioni" in email[18]:
        #for campo in campi:
            #for i in range(len(email[21:120])):
                #if email[21:120][i].split(":")[0].strip() == campo and campo == "CODICE":
                    #articoli = email[21:120][i].split("---")
                    #for articolo in articoli.strip():
                        #articolo = articolo.split()[1][4:].replace("\xa0", "").strip()
                        #quantita = articolo.split()[-1].replace("\xa0", "").strip()
                        #emailDictCod[articolo] = int(quantita)
                    #emailDict['articoli'] = emailDictCod
                #elif email[21:120][i].split(":")[0].strip() == campo:
                    #valoreList = []
                    #f = i+1
                    #righe = ""
                    #while f < len(email[21:120]) and  email[21:120][f].split(":")[0].strip() not in campi and len(email[21:120][f]) != 0:
                        #valore_ = email[21:120][f].replace("\xe0","à")\
                                                                #.replace("\xa0", "")\
                                                                #.replace("\xf2", "ò")\
                                                                #.strip()
                        #righe = righe +" " + valore_
                        #valore_ = ""
                        #f+=1
                    #try:
                        #valore = email[21:120][i].split(":")[1].replace("\xc3","à")\
                                                                #.replace("\xa0", "")\
                                                                #.replace("\xc3\xb2", "ò")\
                                                                #.strip() + ""+ righe
                    #except :
                        #valore = ""
                    #if campo != "CODICE":
                        #emailDict[campo] = valore

        #emailDictList.append(emailDict)
        #emailDictCod = {}
#returned_mail_list = emailDictList