# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
#from promogest.dao.Dao import Dao

#def create()
if hasattr(conf, 'VenditaDettaglio'):
    #if conf.VenditaDettaglio.primoavvio=="yes":

    testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])
    testataScontrinoTable = Table('testata_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                #chiavi esterne
                Column('id_testata_movimento',Integer,ForeignKey(params['schema']+'.testata_movimento.id', onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema']
                )
    testataScontrinoTable.create(checkfirst=True)

    #testataScontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    articoloTable = Table('articolo', params['metadata'], autoload=True, schema=params['schema'])

    rigaScontrinoTable = Table('riga_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('prezzo',Numeric(16,4),nullable=True),
            Column('prezzo_scontato',Numeric(16,4),nullable=True),
            Column('quantita',Numeric(16,4),nullable=False),
            Column('descrizione',String(200),nullable=False),
            #chiavi esterne
            Column('id_testata_scontrino',Integer,ForeignKey(params['schema'] +'.testata_scontrino.id', onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
            Column('id_articolo',Integer, ForeignKey(params['schema'] +'.articolo.id', onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
            schema=params['schema']
            )
    rigaScontrinoTable.create(checkfirst=True)


    scontoScontrinoTable= Table('sconto_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('valore',Numeric(16,4),nullable=True),
                Column('tipo_sconto',String(50),nullable=False),
                CheckConstraint( "tipo_sconto = 'valore' or tipo_sconto = 'percentuale'" ),
                schema = params['schema']
            )
    scontoScontrinoTable.create(checkfirst=True)


    #rigaDocumentoTable = Table('riga_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    rigaDotoTable = Table('sconto_scontrino', params['metadata'], autoload=True, schema=params['schema'])

    scontoRigaScontrinoTable = Table('sconto_riga_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(params['schema'] +'.sconto_scontrino.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_riga_scontrino',Integer,ForeignKey(params['schema']+'.riga_scontrino.id',onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'])
    scontoRigaScontrinoTable.create(checkfirst=True)

    chiusuraFiscaleTable = Table('chiusura_fiscale', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_chiusura',DateTime, unique=True, nullable=False),
                schema=params['schema']
                )
    chiusuraFiscaleTable.create(checkfirst=True)

        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        #conf.VenditaDettaglio.primoavvio = "no"
        #conf.save()

    testatascontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    testataDoctoTable = Table('sconto_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    scontoTestataScontrinoTable = Table('sconto_testata_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(params['schema']+'.sconto_scontrino.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_testata_scontrino',Integer,ForeignKey(params['schema']+'.testata_scontrino.id',onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema']
            )
    scontoTestataScontrinoTable.create(checkfirst=True)


    schema = params['schema']
    tabella = schema+".sconto_riga_scontrino"
    tabella2 = schema+".sconto_scontrino"
    tabella3 = schema+".sconto_testata_scontrino"

if not hasattr(conf.VenditaDettaglio,"migrazione_sincro_effettuata") or conf.VenditaDettaglio.migrazione_sincro_effettuata =="no" and "ciccio" == "pluto":
    msg = """ATTENZIONE, per qualche giorno l'avvio del pg2
potrebbe essere lento ( anche qualche minuto):
Il rallentamento è solo di chi usa il modulo di
vendita al dettaglio, ed è dovuto ad un aggiornamento/modifica
del database per facilitare e rendere coerente
la sincronizzazione di una sede centrale con i punti vendita
Se il Promogest parte correttamente ed il modulo funziona vi
invitiamo a contattarci al numero verde 800 034561 per disabilitare
l'aggiornamento grazie.
Ci scusiamo per l'inconveniente.
            """
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL
                               | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                               msg)
    dialog.run()
    dialog.destroy()
    ####################### sezione deciata allo sconto riga scontrino .... ##############

    from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import ScontoScontrino
    from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
    from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import ScontoTestataScontrino
    from promogest.dao.Sconto import Sconto

    try:
        stro = 'ALTER TABLE %s DROP CONSTRAINT "sconto_riga_scontrino_id_fkey";' %tabella
        session.execute(text(stro))
        session.commit()
        session.flush()
    except:
        session.rollback()

    dati_sconto = params["session"].query(scontoRigaScontrinoTable.c.id).all()
    cc = None
#    print dati_sconto
    if dati_sconto:
        for dato in dati_sconto:
            print dato[0]
            riga = Sconto().getRecord(id=dato[0])
            test = ScontoScontrino().getRecord(id=dato[0])
            if not test:
                cc = ScontoScontrino()
                cc.id = dato[0]
                cc.valore= riga.valore
                cc.tipo_sconto = riga.tipo_sconto
                cc.save_update(cc)
            else:
                continue
        try:
            if cc:
                cc.commit()
        except:
            cc.rollback()
            print "GIA FATTO"

    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT sconto_riga_scontrino_id_fkey FOREIGN KEY (id)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE CASCADE;"""%(tabella,tabella2)
        session.execute(text(stri))
        session.commit()
        session.flush()
    except:
        print "ADD fallito"

    #################### sezione sconto testata scontrino ##########################

    try:
        conn = params["engine"].connect()
        trans = conn.begin()
        stri = 'ALTER TABLE %s DROP CONSTRAINT sconto_testata_scontrino_id_fkey'%tabella3
        conn.execute(stri)
        trans.commit()
        trans.close()
    except:
        trans.rollback()
        print "drop fallito"

    dati_sconto2 = params["session"].query(scontoTestataScontrinoTable.c.id).all()
    cc2 = None
    #print dati_sconto2
    if dati_sconto2:
        for dato in dati_sconto2:
            print dato[0]
            riga = Sconto().getRecord(id=dato[0])
            test = ScontoScontrino().getRecord(id=dato[0])
            if not test:
                cc = ScontoScontrino()
                cc.id = dato[0]
                cc.valore= riga.valore
                cc.tipo_sconto = riga.tipo_sconto
                cc.save_update(cc)
            else:
                continue
        try:
            if cc:
                cc.commit()
        except:
            cc.rollback()
            print "GIA FATTO"

    try:
        stri= """ALTER TABLE %s
                    ADD CONSTRAINT sconto_testata_scontrino_id_fkey FOREIGN KEY (id)
                    REFERENCES %s (id) MATCH SIMPLE
                    ON UPDATE CASCADE ON DELETE CASCADE;"""%(tabella3,tabella2)
        session.execute(text(stri))
        session.commit()
        session.flush()
#        trans2.close()
    except:
        print "ADD fallito"


    ################################## sistemo la sequence ....che resta sfasata a causa degli inserimenti ..... ################à
    try:
        command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(params["schema"]+".sconto_scontrino_id_seq",params["schema"] +".sconto_scontrino")
        session.execute(text(command))
    except:
        print "PURE QUESTO FATTO"
