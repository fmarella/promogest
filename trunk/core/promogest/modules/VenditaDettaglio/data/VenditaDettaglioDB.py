# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
#from promogest.dao.Dao import Dao

if hasattr(conf, 'VenditaDettaglio'):
    #if conf.VenditaDettaglio.primoavvio=="yes":


    posTable = Table('pos', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('denominazione', String(200), nullable=False ),
            Column('denominazione_breve', String(10), nullable=False),
            schema=params['schema'], useexisting =True
            )
    posTable.create(checkfirst=True)

    magazzinoTable = Table('magazzino', params['metadata'], autoload=True, schema=params['schema'])
    testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])
#    ccdTypeTable = Table('credit_card_type', params['metadata'], autoload=True, schema=params['schema'])
    testataScontrinoTable = Table('testata_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                #chiavi esterne
                Column('id_magazzino',Integer,ForeignKey(params['schema']+'.magazzino.id', onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_pos',Integer,ForeignKey(params['schema']+'.pos.id', onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_ccardtype',Integer,ForeignKey(params['schema']+'.credit_card_type.id', onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_user',Integer,ForeignKey(params['mainSchema']+'.utente.id', onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_testata_movimento',Integer,ForeignKey(params['schema']+'.testata_movimento.id', onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema'],
                useexisting =True
                )
    testataScontrinoTable.create(checkfirst=True)

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

    rigaDotoTable = Table('sconto_scontrino', params['metadata'], autoload=True, schema=params['schema'])

    scontoRigaScontrinoTable = Table('sconto_riga_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(params['schema'] +'.sconto_scontrino.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_riga_scontrino',Integer,ForeignKey(params['schema']+'.riga_scontrino.id',onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'])
    scontoRigaScontrinoTable.create(checkfirst=True)

    chiusuraFiscaleTable = Table('chiusura_fiscale', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_chiusura',DateTime,nullable=False),
                Column('id_magazzino',Integer,ForeignKey(params['schema']+'.magazzino.id', onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_pos',Integer,ForeignKey(params['schema']+'.pos.id', onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema']
                )
    chiusuraFiscaleTable.create(checkfirst=True)

        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        #conf.VenditaDettaglio.primoavvio = "no"
        #conf.save()

#    testatascontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
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
    tabella4 = schema+".testata_scontrino"
    tabella5 = schema+".magazzino"
    tabella6 = schema+".pos"
    tabella7 = "promogest2.utente"
    tabella8 = schema+".chiusura_fiscale"
    tabella9 = schema+".credit_card_type"

#testataScontrinoTable
#    if "testata_scontrino.id_magazzino" in str(testataScontrinoTable.c):
#        print "OOOOOOOOOOOOOOOOOOOOO"

    """ Rivediamo la struttura della testata vendita al dettaglio per gestire
        anche una definizione dei magazzini, dei punti cassa e possibilmente
        anche del cassiere che ha effettuato la vendita """

    #if "testata_scontrino.id_magazzino" not in testatascontrinoTable.c:
    #    print "OKOKOKOKOKO NN CE"
    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_magazzino integer ;'  % tabella4
        session.connection().execute(text(comando))
        session.commit()
    #    session.flush()
    except:
        session.rollback()
        print "LACOLONNA ID_MAGAZZINO C'E"

    #if "id_magazzino" in testatascontrinoTable.c:
    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT testata_scontrino_id_magazzino_id_fkey FOREIGN KEY (id_magazzino)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE RESTRICT;""" %(tabella4,tabella5)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD ID MAGAZZINO fallito"



    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_ccardtype integer ;'  % tabella4
        session.connection().execute(text(comando))
        session.commit()
    #    session.flush()
    except:
        session.rollback()
        print "LACOLONNA ID_CCARDTYPE C'E"

    #if "id_magazzino" in testatascontrinoTable.c:
    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT testata_scontrino_id_ccardtype_id_fkey FOREIGN KEY (id_ccardtype)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE SET NULL;""" %(tabella4,tabella9)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD ID CCardType fallito"

    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_pos integer ;'  % tabella4
        session.connection().execute(text(comando))
        session.commit()
    #    session.flush()
    except:
        session.rollback()
        print "LACOLONNA ID_POS C'E"


    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT testata_scontrino_id_pos_id_fkey FOREIGN KEY (id_pos)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE RESTRICT;""" %(tabella4,tabella6)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD FK ID POS fallito"


    """ AGGIUNGO LA FK ID_USER NELLA TABELLA TESTATA SCONTRINO"""
    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_user integer ;'  % tabella4
        session.connection().execute(text(comando))
        session.commit()
    #    session.flush()
    except:
        session.rollback()
        print "LACOLONNA ID_USER C'E"

    #if "id_magazzino" in testatascontrinoTable.c:
    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT testata_scontrino_id_user_id_fkey FOREIGN KEY (id_user)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE RESTRICT;""" %(tabella4,tabella7)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD FK ID USER fallito"

    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT sconto_riga_scontrino_id_fkey FOREIGN KEY (id)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE DELETE;"""%(tabella,tabella2)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD FK SCONTO RIGA SCONTRINO fallito"


    """ AGGIUNGO LA FK ID_MAGAZZINO NELLA TABELLA CHIUSURA FISCALE"""

    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_magazzino integer ;'  % tabella8
        session.connection().execute(text(comando))
        session.commit()
    except:
        session.rollback()
        print "LA COLONNA ID_MAGAZZINO C'E"

    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT chiusura_fiscale_id_magazzino_id_fkey FOREIGN KEY (id_magazzino)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE RESTRICT;""" %(tabella8,tabella5)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD FK ID MAGAZZINO fallito"

    """ AGGIUNGO LA FK ID_POS NELLA TABELLA CHIUSURA FISCALE"""

    try:
        comando = 'ALTER TABLE %s ADD COLUMN id_pos integer ;'  % tabella8
        session.connection().execute(text(comando))
        session.commit()
    except:
        session.rollback()
        print "LA COLONNA ID_pos C'E"

    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT chiusura_fiscale_id_pos_id_fkey FOREIGN KEY (id_pos)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE RESTRICT;""" %(tabella8,tabella6)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD FK ID POS fallito"

    try:
        stri = 'ALTER TABLE %s DROP CONSTRAINT chiusura_fiscale_data_chiusura_key'%tabella8
        session.execute(stri)
        session.commit()
    except:
        session.rollback()
        print " LA UNIQUE e' già stata tolta"

    try:
        stri = 'ALTER TABLE %s ADD CONSTRAINT chiusura_fiscale_data_chiusura_key'%tabella8
        session.execute(stri)
        session.commit()
    except:
        session.rollback()
        print " LA UNIQUE e' già stata tolta"


if not hasattr(conf.VenditaDettaglio,"migrazione_sincro_effettuata") or conf.VenditaDettaglio.migrazione_sincro_effettuata =="no":
#if "ciccio" == "pluto":
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

    dati_sconto = params["session"].query(scontoRigaScontrinoTable.c.id).all()
    cc = None
#    print dati_sconto
    if dati_sconto:
        for dato in dati_sconto:
            riga = Sconto().getRecord(id=dato[0])
            test = ScontoScontrino().getRecord(id=dato[0])
            if not test:
                cc = ScontoScontrino()
                cc.id = dato[0]
                cc.valore= riga.valore
                cc.tipo_sconto = riga.tipo_sconto
                session.add(cc)
            else:
                continue
        try:
            session.commit()
        except:
            session.rollback()
            print "GIA FATTO"

    try:
        stri="""ALTER TABLE %s
            ADD CONSTRAINT sconto_riga_scontrino_id_fkey FOREIGN KEY (id)
            REFERENCES %s (id) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE CASCADE;"""%(tabella,tabella2)
        session.execute(text(stri))
        session.commit()
    except:
        print "ADD fallito"

    #################### sezione sconto testata scontrino ##########################

    try:
        stri = 'ALTER TABLE %s DROP CONSTRAINT sconto_testata_scontrino_id_fkey'%tabella3
        session.connection().execute(stri)
        session.commit()
    except:
        session.rollback()
        print "drop fallito"

    dati_sconto2 = params["session"].query(scontoTestataScontrinoTable.c.id).all()
    cc2 = None
    if dati_sconto2:
        for dato in dati_sconto2:
            riga = Sconto().getRecord(id=dato[0])
            test = ScontoScontrino().getRecord(id=dato[0])
            if not test:
                cc = ScontoScontrino()
                cc.id = dato[0]
                cc.valore= riga.valore
                cc.tipo_sconto = riga.tipo_sconto
                session.add(cc)
        try:
            session.commit()
        except:
            session.rollback()
            print "GIA FATTO"

    try:
        stri= """ALTER TABLE %s
                    ADD CONSTRAINT sconto_testata_scontrino_id_fkey FOREIGN KEY (id)
                    REFERENCES %s (id) MATCH SIMPLE
                    ON UPDATE CASCADE ON DELETE CASCADE;"""%(tabella3,tabella2)
        session.execute(text(stri))
        session.commit()
    except:
        session.rollback()
        print "ADD fallito"


    ################################## sistemo la sequence ....che resta sfasata a causa degli inserimenti ..... ################à
    try:
        command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(params["schema"]+".sconto_scontrino_id_seq",params["schema"] +".sconto_scontrino")
        session.execute(text(command))
        session.commit()
    except:
        session.rollback()
        print "PURE QUESTO FATTO"
