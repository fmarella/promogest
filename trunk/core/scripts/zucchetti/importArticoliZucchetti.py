# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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




import ConfigParser
import time
from datetime import datetime
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy.interfaces import ConnectionProxy
from optparse import OptionParser

import csv

"""
    #CAMPI CSV CLIENTI Easyfatt:

        #0  "Cod."; =  Clienti:string
        #1  "Denominazione"; = Clienti:string
        #2  "Indirizzo";  =  Clienti:string.  Sede_legale_indirizzo
        #3  "Cap"; = Clienti:string Sede_legale_cap
        #4  "Città"; Clienti:string Sede_legale_citta
        #5  "Prov."; Clienti:string Sede_legale_provincia
        #6  "Regione"; Clienti: strig Sede_legale_regione
        #7  "Nazione"; Clienti: string  nazione
        #8  "Partita Iva"; Clienti :string
        #9  "Codice fiscale"; Clienti: string
        #10 "Extra 1"; NO
        #11 "Extra 2"; NO
        #12 "Note";  NO
        #13 "Listino";  Cliente integer  id_listino
        #14 "Sconti";   CHE VUOL DIRE ....
        #15 "Banca";    Clienti id_banca
        #16 "Ns Banca"; NO
        #17 "Agente"; NO
        #18 "Rit. acconto?"; NO
        #19 "Pagamento";  id_pagamento
        #20 "Fatt. con Iva"; ???  RIFERIMENTO A CLIENTE DETTAGLIO ... Interessante....
        #21 "Rif. Persona"; ??? CHE VUOL DIRE ?

        #22 "Tel.";  Recapito Telefono
        #23 "Cell";  Recapito Cellulare
        #24 "Fax";   Recapito Fax
        #25 "Desc. Tel. 2";  SU PG NON SERVE
        #26 "Tel. 2"; Recapito Telefono
        #27 "Desc. Tel. 3";  SU PG NON SERVE
        #28 "Tel. 3"; Recapito Telefono
        #29 "e-mail";  Recapito Email
        #30 "Home page"; Recapito Sito
        #31 "Login web"; NO
        #32 "Conto reg."; ??????????
        #33 "Note doc." ??????????
"""


def stringToDate(stringa):
    """
    Converte una stringa in data
    """
    if stringa is None or stringa == '':
        return None
    else:
        try:
            d = time.strptime(stringa, "%d/%m/%Y")
            data = datetime.date(d[0], d[1], d[2])
        except Exception:
            data=None
        return data

class MyProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        return execute(cursor, statement, parameters, context)

class SetTextFactory(PoolListener):
     def connect(self, dbapi_con, con_record):
         dbapi_con.text_factory = str

class GenericFillData(object):
    def __init__(self):
        usage = """Uso: %prog [options]
        Opzioni disponibili sono :
                -f   --fileCSV Il file da importare
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-f","--file",
                            help="file dei dati in formato csv",
                            type="string",
                            dest="fileDB")
        config = ConfigParser.RawConfigParser()
        config.read('zucchetti.cfg')
        self.azienda =  config.get("PRO","azienda")
        self.db_name = config.get("PRO","azienda")
        self.port = config.getint("PRO","port")
        self.tipo = config.get("TypeDB","tipo")
        self.user = config.get("PRO","user")
        self.password = config.get("PRO","password")
        self.mainSchema = config.get("PRO","mainschema")
        self.host = config.get("PRO","host")
        #self.file_csv = config.get("FileCSV","file_csv")
        self.db_path = config.get("ONE","db_path")
        self.delimiter = config.get("FileCSV","delimiter")
        self.quotechar = config.get("FileCSV","quotechar")

        (options, args) = parser.parse_args()
        if options.fileDB and options.fileDB != "":
            self.file_csv = options.fileDB
        else:
            print "ERRORE NESSUN FILE DA PARSARE"
            raise Exception("ERRORE: usare -f /path/to/file")
        self.connection()

    def connection(self):
        if self.tipo == "postgresql":
            engine = create_engine('postgres:'+'//'+self.user+':'
                                + self.password+ '@'
                                + self.host + ':'
                                + self.port + '/'
                                + self.db_name,
                                encoding='utf-8',
                                convert_unicode=True )
        else:
            self.azienda = None
            self.mainSchema = None
            engine =create_engine("sqlite:///"+self.db_path+"db",listeners=[SetTextFactory()],proxy=MyProxy())
        engine.echo = False
        meta = MetaData(engine)
        self.pg_db_dest = SqlSoup(meta)
        self.pg_db_dest.schema = self.azienda
        self.readFile()

    def readFile(self):
        spamReader = list(csv.reader(open(self.file_csv), delimiter=self.delimiter, quotechar=self.quotechar))
#        spamReader.next() # Skip header line.
        spamReaderList = spamReader[1:]
        if len(spamReader) >0:
            tabella = self.definisciTabella(spamReader[0])
            if tabella =="gruppomerceologico":
                self.fillFamigliaArticolo(spamReaderList)
            elif tabella == "articolo":
                self.fillArticolo(spamReaderList)
            elif tabella == "listino_articolo":
                self.fillListinoArticolo(spamReaderList)
        #print "OOOOOOOOOOOOOOOO", spamReaderList
        #self.fillDataContact(spamReaderList)

    def definisciTabella(self, dati):
        if dati:
            if dati[0] =="gmcodice" and dati[1] == "gmdescri":
                print "TABELLA GRUPPO MERCEOLOGICO"
                return "gruppomerceologico"
            elif dati[0] =="arcodart" and dati[1] == "ardesart":
                print "TABELLA ARTICOLO"
                return "articolo"
            elif dati[0] == "arcodart" and dati[0] == "lscodlis":
                print "TABELLA LISTINO"
                return "listino_articolo"

    def fillFamigliaArticolo(self, spamReaderList):
        """ SCHEMA CONVERSIONE gruppo merceologico:
        zucchetti : gruppomerceologico = promogest : famiglia articolo
        zucchetti 2 colonne
        promogest 3 colonne
        zucchetti : gmcodice = promogest : codice
        zucchetti : gmdescri = promogest :denominazione
        zucchetti : gmdescri[0:10] = promogest : denominazione_breve
        """
        for row in spamReaderList:
            a = self.pg_db_dest.famiglia_articolo.filter_by(codice=row[0]).all()
            if not a:
                a = self.pg_db_dest.famiglia_articolo()
            else:
                a = a[0]
            a.codice = row[0]
            a.denominazione = row[1]
            a.denominazione_breve = row[1][0:10]
            sqlalchemy.ext.sqlsoup.Session.add(a)
            sqlalchemy.ext.sqlsoup.Session.commit()

    def fillArticolo(self, spamReaderList):
        """ SCHEMA CONVERSIONE articolo:
        zucchetti : articoli = promogest : articolo
        0 zucchetti : arcodart = pg2 : codice
        1 zucchetti : ardesart = pg2:d enominazione
        2 zucchetti : argrumer = pg2 : id_famiglia_articolo
        3 zucchetti : arcatomo = pg2 : ??????????????
        4 zucchetti : arcodfam = pg2 : ??????????????
        5 zucchetti : arcatcon = Non rilevante
        6 zucchetti : arcodiva = pg2 : id_aliquota_iva
        7 zucchetti : arunmis1 = pg2 : id_unita_base
        "0000R";"OLIO RITONIFICANTE LT1";"0004";"00204";"2048";"ALTRA";"20";"LT"
        """
        for row in spamReaderList:
            a = self.pg_db_dest.articolo.filter_by(codice=row[0]).all()
            if not a:
                a = self.pg_db_dest.articolo()
            else:
                a = a[0]
            a.codice = row[0]
            a.denominazione = row[1]

            f = self.pg_db_dest.famiglia_articolo.filter_by(codice=row[2]).all()
            if not f:
                print "FAMIGLIA NON PRESENTE"
                del a
                continue
            a.id_famiglia_articolo = f[0].id
            g = self.pg_db_dest.aliquota_iva.filter_by(percentuale=float(row[6])).one()
            if not g:
                print "ATTENZIONE AGGIHNGERE IVA AL %s" %row[6]
                raise Exception("ATTENZIONE AGGIHNGERE IVA AL %s") %row[6]
            else:
                iva = g.id
            a.id_aliquota_iva = iva
            um = row[7]
            if um =="LT":
                umid = 3
            elif um == "MT":
                umid =2
            elif um =="NR":
                umid = 5
            elif um =="GR" or um =="KG":
                umid =4
            a.id_unita_base = umid
            a.id_categoria = 1
            a.cancellato = False
            sqlalchemy.ext.sqlsoup.Session.add(a)
        sqlalchemy.ext.sqlsoup.Session.commit()


    def fillListinoArticolo(self, spamReaderList):
        """ SCHEMA CONVERSIONE listino_articolo:
        0 zucchetti : arcodart = pg2 : "mi serve per agganciare id_articolo"
        1 zucchetti : lscodlis = pg2 : mi serve per agganciare id_listino
        2 zucchetti : lidatatt = pg2 : data_listino
        3 zucchetti : liprezzo = pg2 : prezzo_ingrosso
        """
        for row in spamReaderList:
            a = self.pg_db_dest.articolo.filter_by(codice=row[0]).all()
            if not f:
                print "FAMIGLIA NON PRESENTE"
                del a
                continue
            else:
                idArticolo = a[0].id

            b = self.pg_db_dest.listino_articolo.filter_by(id_articolo=idArticolo, id_listino=row[1]).all()
            if not b:
                b = self.pg_db_dest.listino_articolo()
            else:
                b = a[0]

            f = self.pg_db_dest.famiglia_articolo.filter_by(codice=row[2]).all()
            if not f:
                print "FAMIGLIA NON PRESENTE"
                del a
                continue
            a.id_famiglia_articolo = f[0].id
            g = self.pg_db_dest.aliquota_iva.filter_by(percentuale=float(row[6])).one()
            if not g:
                print "ATTENZIONE AGGIHNGERE IVA AL %s" %row[6]
                raise Exception("ATTENZIONE AGGIHNGERE IVA AL %s") %row[6]
            else:
                iva = g.id
            a.id_aliquota_iva = iva
            um = row[7]
            if um =="LT":
                umid = 3
            elif um == "MT":
                umid =2
            elif um =="NR":
                umid = 5
            elif um =="GR" or um =="KG":
                umid =4
            a.id_unita_base = umid
            a.id_categoria = 1
            a.cancellato = False
            sqlalchemy.ext.sqlsoup.Session.add(a)
        sqlalchemy.ext.sqlsoup.Session.commit()



    #def fillDataContact(self,spamReader):
        #f = open("scarti.txt", "w")
        #print "NUMERO DANEA", len(spamReader)
        #for cl in self.clientiGiustoPesoReaderList:
            #ce = False
            #for row in spamReader:
                #if cl[1].lower() in row[1].lower() and cl[2].lower() in row[1].lower():
                    #ce = True
            #if not ce:
                #codice = "CLI" +str(cl[1][:2]+cl[2][:2])
                #spamReader.append([codice, cl[1]+" "+cl[2],"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""])
    ##            f.write("\n\nCLI: "+ str(cl)+"\n")
    ##            for r in pesateGiustoPesoReaderList:
    ##                if r[1] == cl[0]:
    ##                    f.write("    PESATE: "+ str(r[2].split(" ")[0])+" "+r[3]+" "+r[4] +" "+r[5]+"\n")
                #ce = False
        #print "\n\n INI ZIO", datetime.now(), len(spamReader)
        #for row in spamReader:
            #ah = self.pg_db_dest.persona_giuridica.filter_by(codice=row[0]).all()
            #if ah:
                #for cl in self.clientiGiustoPesoReaderList:
                    #if cl[1].lower() in row[1].lower() and cl[2].lower() in row[1].lower():
                        #for p in self.pesateGiustoPesoReaderList:
                            #if p[1] == cl[0]:
                                #self.pesateGiustoPesoReaderList.remove(p)
                        #self.clientiGiustoPesoReaderList.remove(cl)
                #continue
            #print "\n\nDOPO CHECK SE ESISTE CLI", datetime.now()
            #pg = self.pg_db_dest.persona_giuridica()
            #pg.codice = row[0]
            #pg.ragione_sociale = row[1]
            #pg.sede_legale_indirizzo = row[2]
            #pg.sede_legale_cap = row[3]
            #pg.sede_legale_localita = row[4]
            #pg.sede_legale_provincia = row[5]
            #pg.nazione = row[7]
            #pg.partita_iva = row[8]
            #pg.codice_fiscale = row[9]
            #sqlalchemy.ext.sqlsoup.Session.add(pg)
            #sqlalchemy.ext.sqlsoup.Session.commit()

            #cli = self.pg_db_dest.cliente()
            #cli.id = pg.id
            #sqlalchemy.ext.sqlsoup.Session.add(cli)
            #sqlalchemy.ext.sqlsoup.Session.commit()
            #print "SALVATO CLI", datetime.now()
            #if self.ip:
##                clientiGiustoPeso.next() # Skip header line.
##                pesateGiustoPesoReader.next()
                #trovato = False
                #print "QUANTI CLIENTI", len(self.clientiGiustoPesoReaderList)
                #for cl in self.clientiGiustoPesoReaderList:
                    ##CLIENTI GIUSTO PESO:
                    ##"id";"cognome";"nome";"sesso";"datanascita";"altezza";"cellulare";"notes";"datanotifica"
                    ## PESATE GIUSTO PESO:
                    ##"id";"clienteId";"data";"peso";"dieta";"notes";"deltapeso"
                    #if cl[1].lower() in row[1].lower() and cl[2].lower() in row[1].lower():
                        #print "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", datetime.now(), row[1], cl[1], cl[2], cl[3], cl[4], cl[5], cl[6], cl[7]
                        #tip = self.pg_db_dest.testata_info_peso()
                        #tip.id_cliente = cli.id
                        #tip.note = cl[7]
                        #tip.citta = ""
                        #if "privacy" in cl[7].lower():
                            #tip.privacy = True
                        #else:
                            #tip.privacy = False

                        #clgen = self.pg_db_dest.cliente_generalita()
                        #clgen.id_cliente = cli.id
                        #try:
                            #clgen.data_nascita = datetime(int(cl[4].split(" ")[0].split("/")[2]),
                                                      #int(cl[4].split(" ")[0].split("/")[1]),
                                                      #int(cl[4].split(" ")[0].split("/")[0])  )
                        #except:
                            #clgen.data_nascita = datetime(2011,1,1)
                            #print "ERRORE DATA DI NASCITA", int(cl[4].split(" ")[0].split("/")[2])
                        #clgen.altezza = float(cl[5])
                        #if cl[3] =="F":
                            #genere = "Donna"
                        #else:
                            #genere = "Uomo"
                        #clgen.genere =genere
                        #sqlalchemy.ext.sqlsoup.Session.add(clgen)
                        #sqlalchemy.ext.sqlsoup.Session.commit()
                        #n = 0
                        #print "QUANTE RIGHE", len(self.pesateGiustoPesoReaderList)
                        #for p in self.pesateGiustoPesoReaderList:

                            #h = self.pg_db_dest.tipo_trattamento.filter_by(denominazione=p[4].upper()).all()
                            #if not h:
                                #tipoip = self.pg_db_dest.tipo_trattamento()
                                #tipoip.denominazione = p[4].upper()
                                #sqlalchemy.ext.sqlsoup.Session.add(tipoip)
                                #sqlalchemy.ext.sqlsoup.Session.commit()
                            #if p[1] == cl[0]:
                                #if not tip.data_inizio:
                                    #tip.data_inizio = datetime(int(p[2].split(" ")[0].split("/")[2]),
                                                      #int(p[2].split(" ")[0].split("/")[1]),
                                                      #int(p[2].split(" ")[0].split("/")[0]))
                                    #sqlalchemy.ext.sqlsoup.Session.add(tip)
                                    #sqlalchemy.ext.sqlsoup.Session.commit()
                                    #print "SALVO LA TESTATA PESATA", datetime.now()
                                #rip = self.pg_db_dest.riga_info_peso()
                                #rip.numero = n+1
                                #rip.id_testata_info_peso = tip.id
                                #rip.data_registrazione = datetime(int(p[2].split(" ")[0].split("/")[2]),
                                                      #int(p[2].split(" ")[0].split("/")[1]),
                                                      #int(p[2].split(" ")[0].split("/")[0]))
                                #rip.note = p[5]
                                #rip.peso = float(p[3])
                                #z = self.pg_db_dest.tipo_trattamento.filter_by(denominazione=p[4].upper()).all()
                                #rip.id_tipo_trattamento = z[0].id
                                #sqlalchemy.ext.sqlsoup.Session.add(rip)
                                #self.pesateGiustoPesoReaderList.remove(p)
                            #else:
                                #continue
                            #sqlalchemy.ext.sqlsoup.Session.commit()
                        #print "DOPO SALVATAGGIO RIGHE PESATA", datetime.now()
                        #n = 0
##                        print p[2], p[3], p[4], p[5]
                        #trovato = True
                        #self.clientiGiustoPesoReaderList.remove(cl)
                        #break
                #if not trovato:
                    #print " NIENTE DA FARE",  row[1]
                    #f.write(row[1]+"\n")
                    #trovato = False
            #if self.tipo =="sqlite":
                #iid = None
                #forMaxId = self.pg_db_dest.contatto.all()
                #if not forMaxId:
                    #iid = 1
                #else:
                    #idss = []
                    #for l in forMaxId:
                        #idss.append(l.id)
                    #iid = (max(idss)) +1
##            cont.id_cliente = cli.id

            #cont = self.pg_db_dest.contatto()
            #if self.tipo =="sqlite":
                #cont.id = iid
            #cont.ragione_sociale = row[1]
            #cont.tipo_contatto ="cliente"
            #cont.note = row[12]
            #sqlalchemy.ext.sqlsoup.Session.add(cont)
            #sqlalchemy.ext.sqlsoup.Session.commit()

            #concli = self.pg_db_dest.contatto_cliente()
            #concli.id = cont.id
            #concli.tipo_contatto = "cliente"
            #concli.id_cliente = cli.id
            #sqlalchemy.ext.sqlsoup.Session.add(concli)
##            sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[22] and row[22] != "":
                #_recapiti0 = self.pg_db_dest.recapito()
                #_recapiti0.recapito=row[22]
                #_recapiti0.tipo_recapito="Telefono"
                #_recapiti0.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti0)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[23] and row[23] != "":
                #_recapiti1 = self.pg_db_dest.recapito()
                #_recapiti1.recapito=row[23]
                #_recapiti1.tipo_recapito="Cellulare"
                #_recapiti1.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti1)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[24] and row[24] != "":
                #_recapiti2 = self.pg_db_dest.recapito()
                #_recapiti2.recapito=row[24]
                #_recapiti2.tipo_recapito="Fax"
                #_recapiti2.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti2)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[26] and row[26] != "":
                #_recapiti3 = self.pg_db_dest.recapito()
                #_recapiti3.recapito=row[26]
                #_recapiti3.tipo_recapito="Telefono"
                #_recapiti3.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti3)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[28] and row[28] != "":
                #_recapiti4 = self.pg_db_dest.recapito()
                #_recapiti4.recapito=row[28]
                #_recapiti4.tipo_recapito="Telefono"
                #_recapiti4.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti4)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[29] and row[29] != "":
                #_recapiti5 = self.pg_db_dest.recapito()
                #_recapiti5.recapito=row[29]
                #_recapiti5.tipo_recapito="Email"
                #_recapiti5.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti5)
##                sqlalchemy.ext.sqlsoup.Session.commit()

            #if row[29] and row[30] != "":
                #_recapiti6 = self.pg_db_dest.recapito()
                #_recapiti6.recapito=row[30]
                #_recapiti6.tipo_recapito="Sito"
                #_recapiti6.id_contatto=cont.id
                #sqlalchemy.ext.sqlsoup.Session.add(_recapiti6)
            #sqlalchemy.ext.sqlsoup.Session.commit()
            #print " DOPO SALVATAGGIO RECAPITI", datetime.now()
        #f.close()

if __name__ == "__main__":
    GenericFillData()
