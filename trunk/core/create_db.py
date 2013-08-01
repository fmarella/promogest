#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Promogest2 - promoCMS database

 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 All right reserved
 license: Gplv3 see LICENSE file
"""
""" parametri di configurazione INIZIO """

MAINSCHEMA = "promogest2"
#MAINSCHEMA = None
SCHEMA = None # da passare anche come primo parametri al lancio del comando
USER = "promoadmin"
PASSWORD = "admin"
HOST = "localhost"
PORT = 5432
DATABASE = "promogest_db"
VERSIONE_DB = "0.9.12"

""" parametri di configurazione FINE """

import os
import sys
from sqlalchemy import *
import sqlalchemy
if sqlalchemy.__version__ < "0.5":
    msg= "VERSIONE DI SQLALCHEMY NON AGGIORNATA, E' RICHIESTA LA VERSIONE 0.5"
    raise Exception,msg

from sqlalchemy.orm import *
#from core.promogest import Environment
from sqlalchemy.databases import postgres
from schemi import *
from optparse import OptionParser


tableListUniversal = [
    ("azienda","CompanyDb"),
    ("operazione","OperazioneDb"),
    ("tipo_aliquota_iva","TipoAliquotaIvaDb"),
    ("stato_articolo","StatoArticoloDb"),
    ("unita_base","UnitaBaseDb"),
    ("role","RoleDb"),
    ("language","LanguageDb"),
    ("tipo_recapito","TipoRecapitoDb"),
    ("user","UserDb"),
    #("application_log", "ApplicationLogDb"),
    ("app_log", "AppLogDb"),
    ("chiavi_primarie_log","ChiaviPrimarieLogDb"),
    ("action","ActionDb"),
    ("roleaction","RoleActionDb"),
    ]
# lista delle tabelle dello schema ( tupla tabella, classe )
tableListPromogest=[
    ("magazzino","MagazzinoDb"),                                               #
    ("setting","SettingDb"),                                                  #0
    ("aliquota_iva","AliquotaIvaDb"),                                          #
    ("categoria_articolo","CategoriaArticoloDb"),                              #
    ("famiglia_articolo","FamilyArticleDb"),                                   #
    ("image","ImageDb"),                                                      #0
    ("imballaggio","ImballaggioDb"),
    ("articolo","ArticleDb"),
    ("multiplo","MultiploDb"),
    ("listino","ListinoDb"),                                                   #
    ("persona_giuridica","PersonaGiuridicaDb"),                                #
    ("pagamento","PagamentoDb"),                                               #
    ("banca","BancaDb"),                                                       #
    ("cliente","ClienteDb"),                                                   #
    ("categoria_fornitore","CategoriaFornitoreDb"),                            #
    ("fornitore","FornitoreDb"),                                               #
    ("destinazione_merce","DestinazioneMerceDb"),
    ("vettore","VettoreDb"),
    ("agente","AgenteDb"),
    ("testata_documento","TestataDocumentoDb"),                               #0
    ("testata_movimento","TestataMovimentoDb"),                               #0
    ("riga","RigaDb"),                                                        #0
    ("sconto","ScontoDb"),                                                    #0
    ("riga_movimento","RigaMovimentoDb"),                                     #0
    ("sconto_riga_movimento","ScontoRigaMovimentoDb"),                        #0
    ("static_page","PagesDb"),                                                #0
    ("static_menu","StaticMenuDb"),                                           #0
    ("contatto","ContattoDb"),                                                 #
    ("contatto_cliente","ContattoClienteDb"),                                  #
    ("recapito","RecapitoDb"),                                                 #
    ("categoria_contatto","CategoriaContattoDb"),                              #
    ("contatto_categoria_contatto","ContattoCategoriaContattoDb"),             #
    ("categoria_cliente","CategoriaClienteDb"),                                #
    ("codice_a_barre_articolo","CodiceBarreArticoloDb"),
    ("listino_articolo","ListinoArticoloDb"),
    ("cart","CartDb"),                                                        #0
    ("articolo_associato","ArticoloAssociatoDb"),
    ("access","AccessDb"),                                                    #0
    ("listino_magazzino","ListinoMagazzinoDb"),
    ("listino_categoria_cliente","ListinoCategoriaClienteDb"),
    ("cliente_categoria_cliente","ClienteCategoriaClienteDb"),                 #
    ("contatto_fornitore","ContattoFornitoreDb"),                              #
    ("contatto_magazzino","ContattoMagazzinoDb"),                              #
    ("contatto_azienda","ContattoAziendaDb"),                                  #
    ("feed","FeedDb"),                                                        #0
    ("fornitura","FornituraDb"),
    ("sconto_fornitura","ScontoFornituraDb"),
    ("informazioni_contabili_documento","InformazioniContabiliDocumentoDb"),  #0
    ("inventario","InventarioDb"),                                            #0
    ("promemoria","PromemoriaDb"),
    ("riga_documento","RigaDocumentoDb"),
    ("listino_complesso_listino","ListinoComplessoListinoDb"),
    ("listino_complesso_articolo_prevalente","ListinoComplessoArticoloPrevalenteDb"),
    ("sconto_riga_documento","ScontoRigaDocumentoDb"),                        #0
    ("sconto_testata_documento","ScontoTestataDocumentoDb"),                  #0
    ("sconti_vendita_dettaglio","ScontiVenditaDettaglioDb"),
    ("sconti_vendita_ingrosso","ScontiVenditaIngrossoDb"),
    ("spesa","SpesaDb"),                                                      #0
    ("testata_documento_scadenza","TestataDocumentoScadenzaDb"),              #0
    ("stoccaggio","StoccaggioDb"),
    ("stadio_commessa", "StadioCommessaDb"),
    ("testata_commessa", "TestataCommessaDb"),
    ("riga_commessa", "RigaCommessaDb"),
    ]

action= ["setup","create","create_all","create_azienda","drop","drop_all","drop_azienda","update","update_all","alter","alter_all", "data","data_all" ]

importDebug = True
db = create_engine('postgres://'+USER + ':' + PASSWORD +'@'+ HOST +':'+ str(PORT) +'/'+ DATABASE,
                    encoding='utf-8',
                    convert_unicode=True )
#db = create_engine('sqlite:////home/vete/pg2_work/promogest_db')
db.echo = True
meta = MetaData(db)
session = create_session(db)


class CreateAndDropTable(object):
    """
    create and drop single and all  tables
    """
    def __init__(self, schema=None, tabella=None, operazione=None, req=None):
        usage = """Uso: %prog [options]

                    Prima di tutto lanciare questi due comandi da shell sostituendo i valori desiderati:

                    # Cambiamo e settiamo la password di postgresql dopo aver modificato il file pg_hba.conf e postgresql.conf

                    sudo -u postgres psql template1

                    e poi:

                    ALTER USER postgres WITH PASSWORD ' "password" ';

                    poi \q

                    #CREAZIONE UTENTE CON PRIVILEGI
                    psql -d template1 -U postgres -h HOST_DEL_DB -c "CREATE USER NOME_UTENTE WITH ENCRYPTED PASSWORD 'PASSWORD_TRA_VIRGOLETTE' CREATEDB;"

                    #CREAZIONE DATABASE
                    psql -d template1 -U NOME_UTENTE -h HOST_DEL_DB -c "CREATE DATABASE NOME_DE_DATABSE WITH ENCODING = 'UNICODE';"

                    #LANCIARE UNO DI QUESTI COMANDI DOPO AVER EDITATO LE PRIME RIGHE DI QUESTO FILE

                    Es: python create_db.py -s mia_azienda -o setup -t classico  <----questa e' la consigliata!!

                """
        parser = OptionParser(usage=usage)
        parser.add_option("-s", "--schema",
                            action="store",
                            help="Schema azienda o sottodominio da inserire",
                            type="string",
                            dest="schema")
        parser.add_option("-o", "--operation",
                            action="store",
                            help="Operazione da svolgere con lo schema",
                            type="string",
                            dest="operazione")
        parser.add_option("-t", "--type",
                            action="store",
                            help="Typo di azione ( scegliere tra: classico e web )",
                            type="string",
                            default="classico",
                            dest="tipo")
        parser.add_option("-v","--verbose",
                            help="rende l'operazione di creazione piu' dettagliata",
                            action="store_true",
                            dest="verbose")

        (options, args) = parser.parse_args()
        self.tipo = options.tipo
        print self.tipo, options.schema
        if self.tipo != "web" and self.tipo !="classico" and self.tipo !="all":
            print "ATTENZIONE!!!, Opzioni possibili per -t (--tipo)  sono 'classico', 'web', 'all'"
            sys.exit()

        self.tabella = tabella
        if not options.schema:
            print " ATTENZIONE !!!!, non e' stato selezionato uno schema con -s schema "
            ok=0
            while ok==0:
                first = raw_input("Vuoi usare 'azienda_prova'? Si/No: ")
                if first == "No" or "N" == first:
                    sys.exit()
                elif first=="Si" or first=="S" or first=="Y" or first=="Yes":
                    self.schema = SCHEMA
                    ok=1
                    break
                else:
                    print "ATTENZIONE, rispondi o Si o no"
        else:
            self.schema = options.schema
        self.metadata = meta
        self.session_sl = session
        if not options.operazione:
            print "ATTENZIONE !!! Manca l'operazione da svolgere!, Scegli tra %s " %action
            sys.exit(2)
        elif options.operazione == "drop_all":
            self.dropAllTable()
        elif options.operazione == "create_all":
            self.createAllTable(lista=tableListPromogest)
        elif options.operazione == "create_azienda" or options.operazione=="setup":
            self.createAziendaSchema(lista=tableListUniversal)
            print "creata l'azienda"
        elif options.operazione == "drop_azienda":
            self.dropAziendaSchema()
            print "cancellata l'azienda"
        elif options.operazione == "update_all":
            print "e' stata richiesta una operazione di drop della tabella "
        elif options.operazione == "alter_all":
            print "e' stata richiesta una operazione di alterazione delle tabelle "
        elif options.operazione == "data_all":
            print "e' stata richiesta una operazione di inserimento dati di tutte le tabelle "
        elif options.operazione == "drop":
            self.dropTable()
            print "E' stata rimossa la tabella : %s" %self.tabella
        elif options.operazione == "create":
            self.createTable(tab=self.tabella)
            print "E'stata aggiunta la tabella: %s" %self.tabella
        elif options.operazione == "update":
            print "E'stata aggiornata la tabella: %s" %self.tabella
        elif options.operazione == "alter":
            print "E'stata alterata la tabella: %s" %self.tabella

    def createAziendaSchema(self, lista=[]):
        try:
            comando= "CREATE SCHEMA %s AUTHORIZATION %s" %(MAINSCHEMA,USER)
            session.execute(text(comando))
        except Exception, e:
            print "Errore %s " % e
        try:
            comando= "CREATE SCHEMA %s AUTHORIZATION %s" %(self.schema, USER)
            session.execute(text(comando))
        except Exception, e:
            print "Errore %s " % e

        self.createAllTable(lista=tableListUniversal)
        self.createAllTable(lista=tableListPromogest)


    def dropAziendaSchema(self):
        comando = "DROP SCHEMA %s CASCADE" %self.schema
        session.execute(text(comando))

    def createTable(self, lista=[], tab=None):
        if tab[0] == "azienda":
            print "----------------   CREO LA TABELLA           :", tab[1]
            exec "%s(schema=self.schema,mainSchema=MAINSCHEMA,tipo=self.tipo, metadata=self.metadata,session=self.session_sl).create()" %tab[1]
        else:
            print "++++++++++++++++++CREO LA TABELLA             :", tab[1]
            exec "%s(schema=self.schema,mainSchema=MAINSCHEMA,metadata=self.metadata,session=self.session_sl).create()" %tab[1]

    def dropTable(self):
        table = Table(self.tabella, self.metadata, autoload=True,schema=self.schema)
        table.drop(checkfirst=True)
        #del self.metadata.tables[self.tabella]

    def createAllTable(self, lista=[]):

        for table in lista:
            #self.tabella = table[0]
            #if table[0] in mainSchemaTable:
                #self.schema= MAINSCHEMA
            #else:
            self.createTable(lista=lista, tab=table)
            print "AGGIUNTA LA TABELLA: %s" %table[0]


    def dropAllTable(self):
        meta.reflect(schema=self.schema)
        meta.drop_all()

if __name__ == '__main__':
    CreateAndDropTable()
