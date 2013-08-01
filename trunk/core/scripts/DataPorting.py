# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/


import locale
#import gtk
#import pickle
import os
import string
import shutil
import glob
import getopt, sys
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import pool
from sqlalchemy.ext.sqlsoup import SqlSoup

"""Utilizzo:
        abbastanza semplice:
        è già impostato e testato per lavorare sul db di mysound quindi non c'è granchè da cambiare...
        'azienda_sorgente' è lo schema azienda database pg1 da cui prelevare i dati (mysound, in questo caso)
        'azienda_destinazione' inveceè lo schema azienda del pg2 in cui salvare i dati prelevati da azienda sorgente.
        'database','host', etc sono i soliti....

        la funzione redefineColumns è stata progettata per cambiare i itpi delle colonne delle tabelle
        (una chiamata per ogni tabella), è stata fatta correttamente, ma non funziona, probabilmente per via della versione di sqlalchemy...
        devo indagare...
        l'unica alternativa, per il momento sembra essere pgadmin3 con cui ho cambiato senza problemi i tipi che mi serviva cambiare
        nella tabella persona_giuridica cambiando TUTTI i varchar(50) in varchar(100) dal browser tabelle a sinistra: click sinistro: proprietà
        (sia sulla singola colonna che direttamente sulla tabella)
        ma se non si ha una porta 5432 aperta bisogna farlo in locale.

        un metodo, potrebbe essere usare un dump fatto con pg_dumpall modificarlo in locale, ricreare un dump del db modificato poi da remoto
        droppare il database sul computer del cliente (via ssh  magari con un banale script)  e ricreare il database con il dump modificato.
        ovviamente, il database di mysound non deve essere modificato dopo il dump iniziale (meglio dropparlo subito per evitare inconvenienti)
        o si perdono i  nuovi dati inseriti quando si droppa e si ricrea il db con le tabelle riempite.

        il dizionario params, di fatto, esiste ma non viene utilizzato. potrebbe tornare utile in futuro.

        data_depot è un dizionario di liste di record, divisi per tabella.
        data2delete viene usato dalla funzione deleteData per cancellare tutti i record nelle tabelle in cui si intende portare dei dati.
        indispensabile se si vuole mantenere coerenza nelle relazioni degli oggetti (dao) che si andranno a creare
        in alternativa, è possibile commentare la chiamata a questa funzione, ma bisogna ricordarsi di togliere la specificazionedell' id
        (o comunque della pk) dagli argomenti della insert() solo nel caso in cui questa non sia una fk a qualche altra tabella
        (ad es: pg_db_dest.cliente.id è una primaryKey che referenzia a sua volta pg_db_dest.persona_giuridica.id) in questo caso,
        deve necessariamente essere specificato tra gli argomenti ma non è ancora possibile gestire in automatico i valori delle
        chiavi per una referenziazione corretta dei record.
        bisogna lavorarci un pò su....
        In sostanza:
        questo script funziona abbastanza bene, a patto che il db di destinazione pg2 sia VUOTO.
        la casistica che copre la creazione coerente di tutti i record in una rete di relazioni, dopotutto, è la chiave di volta per la sincronizzazione dei db....
        sembra comunque un buon inizio per azzardare una analisi coerente.

        probabilmente, l'utilizzo della sessione interna di sqlSoap, permette di trasferire i dati semplicemente chiamando il metodo Session.add()
        e passando il record (rec, in questo script) direttamente come oggetto.
        ma è solo una ipotesi.

        per farlo funzionare è sufficiente lanciarlo da riga di comando (python dataPorting.py).
        manca la valutazione del namespace (if __name__==__main__:)
        che permetterebbe di utilizzare questo script come libreria per una migrazione automatica dei dati.
        utile se decidiamo di automatizzare la procedura.

        non necessita di argomenti, nè di aggiustamenti particolari (a parte, ovviamente, host, user, password):
        solo assicurasi che il db di destinazione sia VUOTO. magari decommentando la funzione deleteData()

        bisogna necessariamente cambiare la lunghezza dei varchar della tabella persona_giuridica dello schema pg2 da 50 a 100
        PRIMA di lanciare questo script sennò bisogna andare a caccia dei record della tabella persona_giuridica del pg1
        con una lunghezza maggiore di 50 (perchè non verranno salvati e con essi tutti i record, cliente, fornitore, ecc che si riferiscono ad essi)

        come giàdetto sopra, la funzione redefineColumns è sintatticamente corretta, ma non va a buon fine. (il server cerca di processare la
        query ma non rende nessuna risposta, lasciando il client in attesa.)


        enjoy :D

"""
azienda_sorgente="rudolf"
azienda_destinazione="rudolf2"
database_source = "promowear_db"
database_dest = "promogest_db"
schema_source = "rudolf"
port = "5432"
user = "promoadmin"
password = "admin"
host = "localhost"
mainSchema_source = "promogest"
mainSchema_dest = "promogest2"

engine_source = create_engine('postgres:'+'//'+user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database_source,
                    encoding='utf-8',
                    convert_unicode=True )

engine_source.echo = True
meta_source = MetaData(engine_source)
pg_db_source = SqlSoup(meta_source)
pg_db_source.schema = azienda_sorgente

engine_dest = create_engine('postgres:'+'//'+user+':'
                    + password+ '@'
                    + host + ':'
                    + port + '/'
                    + database_dest,
                    encoding='utf-8',
                    convert_unicode=True )
engine_dest.echo = True
meta_dest = MetaData(engine_dest)
pg_db_dest = SqlSoup(meta_dest)
pg_db_dest.schema = azienda_destinazione

params = {'db_pg_source': engine_source ,
            'db_pg_dest': engine_dest ,
        'mainSchema_source': mainSchema_source,
        'mainSchema_dest': mainSchema_dest,
        'schema_sorgente': azienda_sorgente,
        'schema_destinazione': azienda_destinazione,
        'metadata_source': meta_source,
        'metadata_dest':meta_dest,
        }

_agente = pg_db_source.agente.all()
_magazzino = pg_db_source.magazzino.all()
_aliquota_iva = pg_db_source.aliquota_iva.all()
_categoria_fornitore = pg_db_source.categoria_fornitore.all()
_categoria_contatto = pg_db_source.categoria_contatto.all()
_categoria_cliente = pg_db_source.categoria_cliente.all()
_categoria_articolo = pg_db_source.categoria_articolo.all()
_famiglia_articolo = pg_db_source.famiglia_articolo.all()
_contatti = pg_db_source.contatto.all()
_cliente_categoria_cliente = pg_db_source.cliente_categoria_cliente.all()
_contatti_azienda = pg_db_source.contatto_azienda.all()
_contatti_categoria_contatti = pg_db_source.contatto_categoria_contatto.all()
_contatti_cliente = pg_db_source.contatto_cliente.all()
_contatti_fornitore = pg_db_source.contatto_fornitore.all()
_contatti_magazzino = pg_db_source.contatto_magazzino.all()
_fornitori = pg_db_source.fornitore.all()
_listino = pg_db_source.listino.all()
_pagamento = pg_db_source.pagamento.all()
_clienti = pg_db_source.cliente.all()
_banche = pg_db_source.banca.all()
_articoli = pg_db_source.articolo.all()
_articolo_taglia_colore = pg_db_source.articolo_taglia_colore.all()
_codice_a_barre_articolo = pg_db_source.codice_a_barre_articolo.all()
_persone_giuridiche = pg_db_source.persona_giuridica.all()
_destinazione_merce = pg_db_source.destinazione_merce.all()
_fornitura = pg_db_source.fornitura.all()
_listino_articolo = pg_db_source.listino_articolo.all()
_listino_categoria_cliente = pg_db_source.listino_categoria_cliente.all()
_listino_magazzino = pg_db_source.listino_magazzino.all()
_multiplo = pg_db_source.multiplo.all()
_recapiti = pg_db_source.recapito.all()
_colore = pg_db_source.colore.all()
_gruppo_taglia = pg_db_source.gruppo_taglia.all()
_gruppo_taglia_taglia = pg_db_source.gruppo_taglia_taglia.all()
_imballaggio = pg_db_source.imballaggio.all()
_stoccaggio = pg_db_source.stoccaggio.all()
_taglia = pg_db_source.taglia.all()
_vettore = pg_db_source.vettore.all()


_agente2 = pg_db_dest.agente.all()
_magazzino2 = pg_db_dest.magazzino.all()
_aliquota_iva2 = pg_db_dest.aliquota_iva.all()
_categoria_fornitore2 = pg_db_dest.categoria_fornitore.all()
_categoria_contatto2 = pg_db_dest.categoria_contatto.all()
_categoria_cliente2 = pg_db_dest.categoria_cliente.all()
_categoria_articolo2 = pg_db_dest.categoria_articolo.all()
_famiglia_articolo2 = pg_db_dest.famiglia_articolo.all()
_cliente_categoria_cliente2 = pg_db_dest.cliente_categoria_cliente.all()
_contatti2 = pg_db_dest.contatto.all()
_contatti_azienda2 = pg_db_dest.contatto_azienda.all()
_contatti_categoria_contatti2 = pg_db_dest.contatto_categoria_contatto.all()
_contatti_cliente2 = pg_db_dest.contatto_cliente.all()
_contatti_fornitore2 = pg_db_dest.contatto_fornitore.all()
_contatti_magazzino2 = pg_db_dest.contatto_magazzino.all()
_fornitori2 = pg_db_dest.fornitore.all()
_listino2 = pg_db_dest.listino.all()
_pagamento2= pg_db_dest.pagamento.all()
_clienti2 = pg_db_dest.cliente.all()
_banche2 = pg_db_dest.banca.all()
_articoli2 = pg_db_dest.articolo.all()
_articolo_taglia_colore2 = pg_db_dest.articolo_taglia_colore.all()
_codice_a_barre_articolo2 = pg_db_dest.codice_a_barre_articolo.all()
_persone_giuridiche2 = pg_db_dest.persona_giuridica.all()
_destinazione_merce2 = pg_db_dest.destinazione_merce.all()
_fornitura2 = pg_db_dest.fornitura.all()
_listino_articolo2 = pg_db_dest.listino_articolo.all()
_listino_categoria_cliente2 = pg_db_dest.listino_categoria_cliente.all()
_listino_magazzino2 = pg_db_dest.listino_magazzino.all()
_multiplo2 = pg_db_dest.multiplo.all()
_recapiti2 = pg_db_dest.recapito.all()
_colore2 = pg_db_dest.colore.all()
_gruppo_taglia2 = pg_db_dest.gruppo_taglia.all()
_gruppo_taglia_taglia2 = pg_db_dest.gruppo_taglia_taglia.all()
_imballaggio2 = pg_db_dest.imballaggio.all()
_stoccaggio2 = pg_db_dest.stoccaggio.all()
_taglia2 = pg_db_dest.taglia.all()
_vettore2 = pg_db_dest.vettore.all()

data2delete = { "agente":_agente2,
                "magazzino":_magazzino2,
                "aliquota_iva":_aliquota_iva2,
                "categoria_fornitore":_categoria_fornitore2,
                "categoria_contatto":_categoria_contatto2,
                "categoria_cliente":_categoria_cliente2,
                "categoria_articolo":_categoria_articolo2,
                "famiglia_articolo":_famiglia_articolo2,
                'recapiti':_recapiti2,
                'listino' : _listino2,
                'pagamento':_pagamento2,
                'cliente_categoria_cliente':_cliente_categoria_cliente2,
                'clienti':_clienti2,
                'banche':_banche2,
                'fornitori':_fornitori2,
                'contatti':_contatti2,
                'contatti_azienda':_contatti_azienda2,
                'contatti_categoria_contatti':_contatti_categoria_contatti2,
                'contatti_cliente':_contatti_cliente2,
                'contatti_fornitore':_contatti_fornitore2,
                'contatti_magazzino':_contatti_magazzino2,
                'articoli':_articoli2,
                'persone_giuridiche':_persone_giuridiche2,
                'articolo_taglia_colore': _articolo_taglia_colore2,
                'codice_a_barre_articolo':_codice_a_barre_articolo2,
                'destinazione_merce':_destinazione_merce2,
                'fornitura':_fornitura2,
                'listino_articolo':_listino_articolo2,
                'listino_categoria_cliente':_listino_categoria_cliente2,
                'listino_magazzino':_listino_magazzino2,
                'multiplo':_multiplo2,
                'colore':_colore2,
                'gruppo_taglia':_gruppo_taglia2,
                'gruppo_taglia_taglia':_gruppo_taglia_taglia2,
                'imballaggio':_imballaggio2,
                'stoccaggio':_stoccaggio2,
                'taglia':_taglia2,
                'vettore':_vettore2}

data_depot = {  "magazzino":_magazzino,
                "aliquota_iva":_aliquota_iva,
                'banche':_banche,
                'listino':_listino,
                'pagamento':_pagamento,
                'clienti':_clienti,
                'categoria_fornitore':_categoria_fornitore,
                'categoria_contatto':_categoria_contatto,
                'categoria_cliente':_categoria_cliente,
                'categoria_articolo':_categoria_articolo,
                'famiglia_articolo':_famiglia_articolo,
                'cliente_categoria_cliente':_cliente_categoria_cliente,
                'fornitori':_fornitori,
                'contatti':_contatti,
                'contatti_azienda':_contatti_azienda,
                'contatti_categoria_contatti':_contatti_categoria_contatti,
                'contatti_cliente':_contatti_cliente,
                'contatti_fornitore':_contatti_fornitore,
                'contatti_magazzino':_contatti_magazzino,
                'articoli':_articoli,
                'persone_giuridiche':_persone_giuridiche,
                'recapiti':_recapiti,
                'agente':_agente,
                'articolo_taglia_colore':_articolo_taglia_colore,
                'codice_a_barre_articolo':_codice_a_barre_articolo,
                'destinazione_merce':_destinazione_merce,
                'fornitura':_fornitura,
                'listino_articolo':_listino_articolo,
                'listino_categoria_cliente':_listino_categoria_cliente,
                'listino_magazzino':_listino_magazzino,
                'multiplo':_multiplo,
                'colore':_colore,
                'gruppo_taglia':_gruppo_taglia,
                'gruppo_taglia_taglia':_gruppo_taglia_taglia,
                'imballaggio':_imballaggio,
                'stoccaggio':_stoccaggio,
                'taglia':_taglia,
                'vettore':_vettore}
data_shell = []

#import pdb
#pdb.set_trace()


def redefineColumns(db, schema, table,columns,types,lenghts,defaults=None,forKey=None):
    """modifica i campi di una tabella.... (sempre ammesso che la tabella sia modificabile in  tal senso....)"""
    for c in range(len(columns)):
        str = 'ALTER TABLE %(schema)s.%(table)s ALTER COLUMN  %(column)s TYPE %(type)s(%(lenght)s)'%{'schema':schema,'table':table, 'column':columns[c],'type':types[c], 'lenght':lenghts[c]}
        print str
        rp = db.bind.execute(text(str))

#    ALTER TABLE [ ONLY ] name [ * ]
#    ALTER [ COLUMN ] column { SET DEFAULT expression | DROP DEFAULT }


def deleteData(data):
    for k,v in data.items():
        for rec in v:
            pg_db_dest.delete(rec)
            sqlalchemy.ext.sqlsoup.Session.commit()
            pg_db_dest.flush()

def maxid(data):
    if data:
        a = max(rec.id for rec in data)
    else:
        a = 1
    return a


def insertData(data):

    v = data['magazzino']
    magazzino_sequence = Sequence("magazzino_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.magazzino.insert(id=rec.id,
                                    denominazione = rec.denominazione,
                                    indirizzo = rec.indirizzo,
                                    localita = rec.localita,
                                    cap = rec.cap,
                                    provincia = rec.provincia,
                                    nazione = rec.nazione,
                                    data_ultima_stampa_giornale = rec.data_ultima_stampa_giornale)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg_dest'].execute(magazzino_sequence)


    v = data['aliquota_iva']
    aliquota_iva_sequence = Sequence("aliquota_iva_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.aliquota_iva.insert(id=rec.id,
                                    denominazione = rec.denominazione,
                                    denominazione_breve = rec.denominazione_breve,
                                    percentuale = rec.percentuale,
                                    percentuale_detrazione = rec.percentuale_detrazione,
                                    descrizione_detrazione = rec.descrizione_detrazione,
                                    id_tipo = rec.id_tipo)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg_dest'].execute(aliquota_iva_sequence)


    v = data['pagamento']
    pagamento_sequence = Sequence("pagamento_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.pagamento.insert(id=rec.id,
                                    denominazione = rec.denominazione,
                                    visible = True,
                                    id_language = 7)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg_dest'].execute(pagamento_sequence)


    v =data['banche']
    banca_sequence = Sequence("banca_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.banca.insert(id=rec.id,
                                denominazione=rec.denominazione,
                                agenzia=rec.agenzia,
                                iban=rec.iban,
                                abi=rec.abi,
                                cab=rec.cab)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg_dest'].execute(banca_sequence)

    v = data['listino']
    listino_sequence = Sequence("listino_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.listino.insert(id=rec.id,
                                    denominazione = rec.denominazione,
                                    descrizione = rec.descrizione,
                                    data_listino = rec.data_listino,
                                    listino_attuale = rec.listino_attuale,
                                    visible = True)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg_dest'].execute(listino_sequence)

    v = data['persone_giuridiche']
    for rec in v:
        persona_giuridica_sequence = Sequence("persona_giuridica_id_seq", schema=params["schema_destinazione"])
        pg_db_dest.persona_giuridica.insert(id=rec.id,
                                            codice=rec.codice,
                                            ragione_sociale=rec.ragione_sociale,
                                            insegna=rec.insegna,
                                            cognome=rec.cognome,
                                            nome=rec.nome,
                                            sede_operativa_indirizzo=rec.sede_operativa_indirizzo,
                                            sede_operativa_cap=rec.sede_operativa_cap,
                                            sede_operativa_provincia=rec.sede_operativa_provincia,
                                            sede_operativa_localita=rec.sede_operativa_localita,
                                            sede_legale_indirizzo=rec.sede_legale_indirizzo,
                                            sede_legale_cap=rec.sede_legale_cap,
                                            sede_legale_provincia=rec.sede_legale_provincia,
                                            sede_legale_localita=rec.sede_legale_localita,
                                            nazione=rec.nazione,
                                            codice_fiscale=rec.codice_fiscale,
                                            partita_iva=rec.partita_iva,
                                            id_user=rec.id_user)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(persona_giuridica_sequence)


    v = data['clienti']
    for rec in v:
        pg_db_dest.cliente.insert(id=rec.id,
                                    id_pagamento=rec.id_pagamento,
                                    id_magazzino=rec.id_magazzino,
                                    id_listino=rec.id_listino,
                                    id_banca=rec.id_banca)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()


    v = data['famiglia_articolo']
    famiglia_articolo_sequence = Sequence("famiglia_articolo_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.famiglia_articolo.insert(id=rec.id,
                                            codice= rec.codice,
                                            denominazione = rec.denominazione,
                                            denominazione_breve= rec.denominazione_breve,
                                            id_padre = rec.id_padre)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(famiglia_articolo_sequence)


    v = data['categoria_fornitore']
    categoria_fornitore_sequence = Sequence("categoria_fornitore_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.categoria_fornitore.insert(id=rec.id,
                                            denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(categoria_fornitore_sequence)

    v = data['categoria_contatto']
    categoria_contatto_sequence = Sequence("categoria_contatto_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.categoria_contatto.insert(id=rec.id,
                                            denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(categoria_contatto_sequence)


    v = data['categoria_articolo']
    categoria_articolo_sequence = Sequence("categoria_articolo_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.categoria_articolo.insert(id=rec.id,
                                            denominazione = rec.denominazione,
                                            denominazione_breve= rec.denominazione_breve)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(categoria_articolo_sequence)


    v = data['categoria_cliente']
    categoria_cliente_sequence = Sequence("categoria_cliente_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.categoria_cliente.insert(id=rec.id,
                                            denominazione = rec.denominazione,
                                            descrizione=rec.descrizione,
                                            active=rec.active)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(categoria_cliente_sequence)



    v =data['cliente_categoria_cliente']
    for rec in v:
        pg_db_dest.cliente_categoria_cliente.insert(id_cliente=rec.id_cliente,
                                                    id_categoria_cliente=rec.id_categoria_cliente)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()


    v =data['fornitori']
    for rec in v:
        pg_db_dest.fornitore.insert(id=rec.id,
                                    id_categoria_fornitore=rec.id_categoria,
                                    id_pagamento=rec.id_pagamento,
                                    id_magazzino=rec.id_magazzino)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['contatti']
    contatto_sequence = Sequence("contatto_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.contatto.insert(id=rec.id,
                                    tipo_contatto=rec.tipo_contatto,
                                    nome=rec.nome,
                                    cognome=rec.cognome,
                                    ruolo=rec.ruolo,
                                    descrizione=rec.descrizione,
                                    note=rec.note)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(contatto_sequence)


    v =data['contatti_azienda']
    for rec in v:
        pg_db_dest.contatto_azienda.insert(id=rec.id,
                                            tipo_contatto=rec.tipo_contatto,
                                            schema_azienda=rec.schema_azienda)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['contatti_categoria_contatti']
    for rec in v:
        pg_db_dest.contatto_categoria_contatto(id=rec.id,
                                                id_contatto=rec.id_contatto,
                                                id_categoria_contatto=rec.id_categoria_contatto)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['contatti_cliente']
    for rec in v:
        pg_db_dest.contatto_cliente.insert(id=rec.id,
                                            tipo_contatto=rec.tipo_contatto,
                                            id_cliente=rec.id_cliente)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['contatti_fornitore']
    for rec in v:
        pg_db_dest.contatto_fornitore.insert(id=rec.id,
                                            tipo_contatto=rec.tipo_contatto,
                                            id_fornitore=rec.id_fornitore)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['contatti_magazzino']
    for rec in v:
        pg_db_dest.contatto_magazzino(id=rec.id,
                                        tipo_contatto=rec.tipo_contatto,
                                        id_magazzino=rec.id_magazzino)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

    v =data['recapiti']
    recapito_sequence = Sequence("recapito_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        if rec.tipo_recapito == "E-Mail": fix = "Email"
        else: fix = rec.tipo_recapito
        pg_db_dest.recapito(id=rec.id,
                            recapito=rec.recapito,
                            tipo_recapito=fix,
                            id_contatto=rec.id_contatto)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(recapito_sequence)

    v =data['articoli']
    articoli_sequence = Sequence("articolo_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        # if rec.tipo_recapito == "E-Mail": fix = "Email"
        # else: fix = rec.tipo_recapito
        pg_db_dest.articolo(id=rec.id,
                            codice=rec.codice,
                            denominazione=denominazione,
                            id_aliquota_iva=rec.id_aliquota_iva,
                            id_famiglia_articolo = rec.id_famiglia_articolo,
                            id_categoria_articolo = rec.id_categoria_articolo,
                            id_unita_base = rec.id_unita_base,
                            produttore = rec.produttore,
                            unita_dimensioni = rec.unita_dimensioni,
                            lunghezza = rec.lunghezza,
                            larghezza = rec.larghezza,
                            altezza = rec.altezza,
                            unita_volume = rec.unita_volume,
                            volume = rec.unita_volume,
                            unita_peso = rec.unita_peso,
                            peso_lordo = rec.peso_lordo,
                            id_imballaggio = rec.id_imballaggio,
                            peso_imballaggio = rec.peso_imballaggio,
                            stampa_etichetta = rec.stampa_etichetta,
                            codice_etichetta =rec.codice_etichetta,
                            descrizione_etichetta = rec.descrizione_etichetta,
                            stampa_listino = rec.stampa_listino,
                            descrizione_listino = rec.descrizione_listino,
                            aggiornamento_listino_auto = rec.aggiornamento_listino_auto,
                            timestamp_variazione = rec.timestamp_variazione,
                            note = rec.note,
                            cancellato = rec.cancellato,
                            sospeso = rec.sospeso,
                            id_stato_articolo = rec.id_stato_articolo,
                            contenuto = rec.contenuto,
                            )
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(articoli_sequence)

    v =data['agente']
    for rec in v:
        pg_db_dest.agente.insert(id=rec.id)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['articolo_taglia_colore']
    for rec in v:
        pg_db_dest.articolo_taglia_colore.insert(id_articolo=rec.id_articolo,
                                                id_articolo_padre= rec.id_articolo_padre,
                                                id_gruppo_taglia = rec.id_gruppo_taglia,
                                                id_taglia = rec.id_taglia,
                                                id_colore = rec.id_colore,
                                                id_anno = rec.id_anno,
                                                id_stagione = rec.id_stagione,
                                                id_genere = rec.id_genere)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['codice_a_barre_articolo']
    codice_a_barre_articolo_sequence = Sequence("codice_a_barre_articolo_id_seq", schema=params["schema_destinazione"])
    for rec in v:
            # if rec.tipo_recapito == "E-Mail": fix = "Email"
            # else: fix = rec.tipo_recapito
        pg_db_dest.codice_a_barre_articolo(id=rec.id,
                            codice=rec.codice,
                            id_articolo=rec.id_articolo,
                            primario=rec.primario)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(codice_a_barre_articolo_sequence)
        
    v =data['destinazione_merce']
    destinazione_merce_sequence = Sequence("destinazione_merce_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.destinazione_merce.insert(id=rec.id,
                                    denominazione=rec.denominazione,
                                    nome=rec.nome,
                                    cognome=rec.cognome,
                                    ruolo=rec.ruolo,
                                    descrizione=rec.descrizione,
                                    note=rec.note)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(destinazione_merce_sequence)

    v =data['fornitura']
    fornitura_sequence = Sequence("fornitura_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.fornitura.insert(id=rec.id,
                                    codice_articolo_fornitore=rec.codice_articolo_fornitore,
                                    prezzo_lordo = rec.prezzo_lordo,
                                    prezzo_netto=rec.prezzo_netto,
                                    applicazione_sconti=rec.applicazione_sconti,
                                    scorta_minima=rec.scorta_minima,
                                    tempo_arrivo_merce=rec.tempo_arrivo_merce,
                                    fornitore_preferenziale = rec.fornitore_preferenziale,
                                    percentuale_iva = rec.percentuale_iva,
                                    data_fornitura = rec.data_fornitura,
                                    data_prezzo = rec.data_prezzo,
                                    id_fornitore = rec.id_fornitore,
                                    id_articolo = rec.id_articolo,
                                    id_multiplo = rec.id_multiplo)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(fornitura_sequence)

    v =data['listino_articolo']
    for rec in v:
        pg_db_dest.listino_articolo.insert(id_articolo=rec.id_articolo,
                                            id_listino= rec.id_listino,
                                            id_gruppo_taglia = rec.id_gruppo_taglia,
                                            prezzo_dettaglio = rec.prezzo_dettaglio,
                                            prezzo_ingrosso = rec.prezzo_ingrosso,
                                            ultimo_costo = rec.ultimo_costo,
                                            data_listino_articolo= rec.data_listino_articolo,
                                            listino_attuale = rec.listino_attuale)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['listino_categoria_cliente']
    for rec in v:
        pg_db_dest.listino_categoria_cliente.insert(id_categoria_cliente=rec.id_categoria_cliente,
                                            id_listino= rec.id_listino)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['listino_magazzino']
    for rec in v:
        pg_db_dest.listino_magazzino.insert(id_magazzino=rec.id_magazzino,
                                            id_listino= rec.id_listino)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['multiplo']
    multiplo_sequence = Sequence("multiplo_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.multiplo.insert(id=rec.id,
                                    denominazione_breve=rec.denominazione_breve,
                                    denominazione = rec.denominazione,
                                    id_unita_base=rec.id_unita_base,
                                    id_articolo=rec.id_articolo,
                                    moltiplicatore=rec.moltiplicatore)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(multiplo_sequence)
        
    v =data['colore']
    colore_sequence = Sequence("colore_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.colore.insert(id=rec.id,
                                    denominazione_breve=rec.denominazione_breve,
                                    denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(colore_sequence)
        
    v =data['gruppo_taglia']
    gruppo_taglia_sequence = Sequence("gruppo_taglia_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.gruppo_taglia.insert(id=rec.id,
                                    denominazione_breve=rec.denominazione_breve,
                                    denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(gruppo_taglia_sequence)
        
    v =data['taglia']
    taglia_sequence = Sequence("taglia_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.taglia.insert(id=rec.id,
                                denominazione_breve=rec.denominazione_breve,
                                denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(taglia_sequence)
        
    v =data['imballaggio']
    imballaggio_sequence = Sequence("imballaggio_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.imballaggio.insert(id=rec.id,
                                denominazione = rec.denominazione)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(imballaggio_sequence)
        
    v =data['stoccaggio']
    stoccaggio_sequence = Sequence("stoccaggio_id_seq", schema=params["schema_destinazione"])
    for rec in v:
        pg_db_dest.stoccaggio.insert(id=rec.id,
                                scorta_minima = rec.scorta_minima,
                                livello_riordino = rec.livello_riordino,
                                data_fine_scorte = rec.data_fine_scorte,
                                data_prossimo_ordine = rec.data_prossimo_ordine,
                                id_articolo = rec.id_articolo,
                                id_magazzino= rec.id_magazzino)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
    maxo = maxid(v)
    for i in range(0,int(maxo)):
        params['db_pg'].execute(imballaggio_sequence)
        
    v =data['vettore']
    for rec in v:
        pg_db_dest.vettore.insert(id=rec.id)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()
        
    v =data['gruppo_taglia_taglia']
    for rec in v:
        pg_db_dest.gruppo_taglia_taglia.insert(id_gruppo_taglia=rec.id_gruppo_taglia,
                                                id_taglia = rec.id_taglia,
                                                ordine = rec.ordine)
        sqlalchemy.ext.sqlsoup.Session.commit()
        pg_db_dest.flush()

# decommentare per modificare le tabelle del database....
#redefineColumns(db=pg_db_dest, schema=azienda_destinazione, table='persona_giuridica', columns=['sede_operativa_indirizzo','sede_legale_indirizzo'], types=['VARCHAR','VARCHAR'], lenghts=['100','100'])
#decommentare per cancellare i dati sulle tabelle prima di effetuare il porting (consigliato, per evitare conflitti nell'inserimento dei nuovi record, in quanto mantengono invariate le chiavi identificative)
#deleteData(data2delete)

insertData(data_depot)
