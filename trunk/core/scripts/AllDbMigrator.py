#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Promogest2 - promoCMS database

 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 All right reserved
 license: Gplv3 see LICENSE file
"""

import os
from sqlalchemy import *
import sqlalchemy
from sqlalchemy.orm import *
from sqlalchemy.databases import postgres

""" Questo è uno script di migrazione del DB del PromoGest2 dal PG1 tabella per tabella
    effettua un backup di ogni singola tabella, la elabora se necessario modificando
    lo schema di destinazione se diverso  ( per esempio rudol to rudolf3 )
    modifica alcuni campi come nel caso fornitore che da id_categoria è diventato
    id_categoria_fornitore e poi crea dei file temporanei. Da qui poi avviene l'import
    successivo secondo un ordine di priorità e di vincoli di relazione.
    l'ultimo passo è l'aggiornamento delle Sequence e la cancellazione di tutti i file

    USO: Configurare i parametri sottostanti

    e lanciare con un  python AllDbMigrator.py
"""

schemasrc = "partecipazioni_nozze"
schemadest =  "nozze2"
utente = "promoadmin"
password ="admin"
host = "localhost"
port ="5432"
databasesrc = "promogest_db"
databasedest = "promogest_db"

tablelist = [
            "categoria_articolo","famiglia_articolo","access","aliquota_iva","listino","imballaggio",
            "articolo","articolo_associato","gruppo_taglia","taglia","gruppo_taglia_taglia","colore","articolo_taglia_colore",
            "banca","cart","categoria_cliente","categoria_contatto","categoria_fornitore","persona_giuridica","magazzino","pagamento",
            "cliente","cliente_categoria_cliente","codice_a_barre_articolo","contatto",
            "contatto_azienda","contatto_categoria_contatto","contatto_cliente",
            "fornitore","contatto_fornitore",
            "contatto_magazzino","destinazione_merce","feed","fornitura","agente",
            "image","informazioni_contabili_documento",
            "inventario","listino_articolo","listino_categoria_cliente","listino_complesso_articolo_prevalente",
            "listino_complesso_listino","listino_magazzino","modello","multiplo",
            "promemoria","recapito","vettore","testata_documento",
            "testata_movimento","riga","riga_documento","riga_movimento",
            "sconti_vendita_dettaglio","sconti_vendita_ingrosso","sconto","sconto_fornitura",
            "sconto_riga_documento","sconto_riga_movimento","sconto_testata_documento",
            "setting","spesa","static_menu","static_page","stoccaggio",
            "testata_documento_scadenza", "colori_stampa","caratteri_stampa","schede_ordinazioni",
            "contatti_schede","associazione_articolo",
            "datari","recapiti_spedizioni", "note_schede", "promemoria_schede_ordinazioni",
            "righe_schede_ordinazioni","sconti_righe_schede", "sconti_schede_ordinazioni"]



for table in tablelist:
    finalFile = table+".sql"
    schemaTable = schemasrc+"."+table
    command = "pg_dump -U %s -h %s -t %s %s > %s" %(utente, host, schemaTable, databasesrc, finalFile)
    print command
    stdin, stdouterr = os.popen4(command)
    print stdouterr.read()

for table in tablelist:
    finalFile = table+".sql"
    schemaTable = schemasrc+"."+table
    print "APRO " , finalFile
    #try:
    f = open(finalFile, "r")
    freplaced = table+"rep.sql"
    opened = open(freplaced, "wb")
    for line in f.readlines():
        if table =="fornitore":
            line = line.replace("id_categoria", "id_categoria_fornitore")
        if table =="articolo":
            line = line.replace("immagine", "id_immagine")
        line = line.replace(schemasrc, schemadest)
        opened.write(line)
    f.close()
    opened.close()

for table in tablelist:
    freplaced = table+"rep.sql"
    command = "psql -U %s -h %s %s < %s" %(utente, host,databasedest, freplaced)
    print command
    stdin, stdouterr = os.popen4(command)
    print stdouterr.read()


db = create_engine('postgres://'+utente + ':' + password +'@'+ host +':'+ str(port) +'/'+ databasedest,
                    encoding='utf-8',
                    convert_unicode=True )
db.echo = True
meta = MetaData(db)
session = create_session(db)

command = "SELECT setval('%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".aliquota_iva_id_seq", schemadest +".aliquota_iva")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".articolo_id_seq",schemadest +".articolo")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".banca_id_seq",schemadest +".banca")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".categoria_articolo_id_seq",schemadest +".categoria_articolo")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".categoria_cliente_id_seq",schemadest +".categoria_cliente")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".categoria_contatto_id_seq",schemadest +".categoria_contatto")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".categoria_fornitore_id_seq",schemadest +".categoria_fornitore")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".codice_a_barre_articolo_id_seq",schemadest +".codice_a_barre_articolo")
session.execute(text(command))
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".colore_id_seq",schemadest +".colore")
    session.execute(text(command))
except:
    print "ERRORE colore_id_seq"
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".contatto_id_seq",schemadest +".contatto")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".destinazione_merce_id_seq",schemadest +".destinazione_merce")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".fornitura_id_seq",schemadest +".fornitura")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".famiglia_articolo_id_seq",schemadest +".famiglia_articolo")
session.execute(text(command))
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".gruppo_taglia_id_seq",schemadest +".gruppo_taglia")
    session.execute(text(command))
except:
    print "ERRORE gruppo_taglia_id_seq"
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".image_id_seq",schemadest +".image")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".imballaggio_id_seq",schemadest +".imballaggio")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".inventario_id_seq",schemadest +".inventario")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".listino_id_seq",schemadest +".listino")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".magazzino_id_seq",schemadest +".magazzino")
session.execute(text(command))
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".modello_id_seq",schemadest +".modello")
    session.execute(text(command))
except:
    print "ERRORE modello_id_seq"
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".multiplo_id_seq",schemadest +".multiplo")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".pagamento_id_seq",schemadest +".pagamento")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".persona_giuridica_id_seq",schemadest +".persona_giuridica")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".promemoria_id_seq",schemadest +".promemoria")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".recapito_id_seq",schemadest +".recapito")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".riga_id_seq",schemadest +".riga")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".sconto_id_seq",schemadest +".sconto")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".stoccaggio_id_seq",schemadest +".stoccaggio")
session.execute(text(command))
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".taglia_id_seq",schemadest +".taglia")
    session.execute(text(command))
except:
    print "ERRORE taglia_id_seq"
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".testata_documento_id_seq",schemadest +".testata_documento")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".testata_documento_scadenza_id_seq",schemadest +".testata_documento_scadenza")
session.execute(text(command))
command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".testata_movimento_id_seq",schemadest +".testata_movimento")
session.execute(text(command))
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".caratteri_stampa_id_seq",schemadest +".caratterie_stampa")
    session.execute(text(command))
except:
    print "ERRORE carattere_stampa_id_seq"
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".colori_stampa_id_seq",schemadest +".colori_stampa")
    session.execute(text(command))
except:
    print "ERRORE colore_stampa_id_seq"
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".contatti_schede_id_seq",schemadest +".contatti_scheda")
    session.execute(text(command))
except:
    print "ERRORE contatto_scheda_id_seq"
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".datari_id_seq",schemadest +".datari")
    session.execute(text(command))
except:
    print "ERRORE datario_id_seq"
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".schede_ordinazioni_id_seq",schemadest +".schede_ordinazioni")
    session.execute(text(command))
except:
    print "ERRORE scheda_ordinazione_id_seq"
try:
    command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".associazione_articolo_id_seq",schemadest +".associazione_articolo")
    session.execute(text(command))
except:
    print "ERRORE associazione_articolo_id_seq"

command = "rm *.sql"
stdin, stdouterr = os.popen4(command)
print stdouterr.read()