# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


#def create()
if hasattr(conf, 'PromoWear'):
    if conf.PromoWear.primoavvio=="yes":
        """ tabelle schema principale """

        #CREATE TABLE colori_stampa (
            #id                      BIGSERIAL   NOT NULL PRIMARY KEY
            #,denominazione          VARCHAR(50) NOT NULL
            #,UNIQUE (id, denominazione));
        coloriStampaTable = Table('colori_stampa', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('denominazione',String(200),nullable=False),
                            schema=params['schema'])
        coloriStampaTable.create(checkfirst=True)

        #CREATE TABLE caratteri_stampa (
            #id                      BIGSERIAL   NOT NULL PRIMARY KEY
            #,denominazione          VARCHAR(50) NOT NULL
            #,UNIQUE (id, denominazione));
        caratteriStampaTable = Table('caratteri_stampa', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('denominazione',String(200),nullable=False),
                            schema=params['schema'])
        caratteriStampaTable.create(checkfirst=True)

        #CREATE TABLE schede_ordinazioni (
            #id bigserial NOT NULL ,
            #numero int8 NOT NULL,
            #nomi_sposi varchar(100),
            #mezzo_ordinazione varchar(50),
            #mezzo_spedizione varchar(50),
            #bomba_in_cliche bool NOT NULL DEFAULT false,
            #codice_spedizione varchar(100),
            #ricevuta_associata varchar(50),
            #fattura bool DEFAULT false,
            #documento_saldato bool DEFAULT false,
            #operatore varchar(50) NOT NULL,
            #provenienza varchar(50),
            #disp_materiale bool NOT NULL DEFAULT true,
            #applicazione_sconti varchar(20),
            #totale_lordo numeric(16,4) DEFAULT 0,
            #userid_cliente varchar(50),
            #passwd_cliente varchar(15),
            #lui_e_lei varchar(50),
            #id_colore_stampa int8 NOT NULL,
            #id_carattere_stampa int8 NOT NULL,
            #id_cliente int8,
            #id_magazzino int8,
        #CONSTRAINT schede_ordinazioni_pkey PRIMARY KEY (id),
        #CONSTRAINT schede_ordinazioni_id_carattere_stampa_fkey FOREIGN KEY (id_carattere_stampa)
            #REFERENCES caratteri_stampa (id) MATCH SIMPLE
            #ON UPDATE CASCADE ON DELETE RESTRICT,
        #CONSTRAINT schede_ordinazioni_id_cliente_fkey FOREIGN KEY (id_cliente)
            #REFERENCES cliente (id) MATCH SIMPLE
            #ON UPDATE CASCADE ON DELETE RESTRICT,
        #CONSTRAINT schede_ordinazioni_id_magazzino_fkey FOREIGN KEY (id_magazzino)
            #REFERENCES magazzino (id) MATCH SIMPLE
            #ON UPDATE CASCADE ON DELETE RESTRICT,
        #CONSTRAINT schede_ordinazioni_id_colore_stampa_fkey FOREIGN KEY (id_colore_stampa)
            #REFERENCES colori_stampa (id) MATCH SIMPLE
            #ON UPDATE CASCADE ON DELETE RESTRICT,
        #CONSTRAINT schede_ordinazioni_id_key UNIQUE (id, numero));

        #CREATE TABLE contatti_schede (
            #id                      BIGSERIAL       NOT NULL PRIMARY KEY
            #,referente              VARCHAR(100)        NULL
            #,prima_email            VARCHAR(100)        NULL
            #,seconda_email          VARCHAR(100)        NULL
            #,telefono               VARCHAR(15)         NULL
            #,cellulare              VARCHAR(15)         NULL
            #,skype                  VARCHAR(30)         NULL
            #,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
            #,UNIQUE (id,id_scheda));
        contattiSchedeTable = Table('contatti_schede', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('referente',text,nullable=True),
                            Column('prima_email',String(300),nullable=True),
                            Column('seconda_email',String(300),nullable=True),
                            Column('telefono',String(300),nullable=True),
                            Column('cellulare',String(300),nullable=True),
                            Column('skype',String(300),nullable=True),
                            Column('id_scheda',Integer,nullable=True),
                            schema=params['schema'])
        contattiSchedeTable.create(checkfirst=True)

        #CREATE TABLE datari (
            #id                      BIGSERIAL   PRIMARY KEY
            #,matrimonio             date        NOT NULL
            #,presa_in_carico        date        NOT NULL
            #,ordine_al_fornitore    date            NULL
            #,consegna_bozza         date            NULL
            #,spedizione             date            NULL
            #,consegna               date            NULL
            #,ricevuta               date            NULL
            #,id_scheda              BIGINT      NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
            #,UNIQUE (id, id_scheda));
        datariTable = Table('datari', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('matrimonio',Date,nullable=False),
                Column('presa_in_carico',Date,nullable=False),
                Column('ordine_al_fornitore',Date,nullable=True),
                Column('consegna_bozza',Date,nullable=True),
                Column('spedizione',Date,nullable=True),
                Column('consegna',Date,nullable=True),
                Column('ricevuta',Date,nullable=True),
                Column('id_scheda',Integer,nullable=True),
                schema=params['schema'])
        datariTable.create(checkfirst=True)


        #CREATE TABLE recapiti_spedizioni (
            #id                      BIGSERIAL       NOT NULL PRIMARY KEY
            #,referente              VARCHAR(100)        NULL
            #,presso                 VARCHAR(100)        NULL
            #,via_piazza             VARCHAR(50)         NULL
            #,num_civ                VARCHAR(5)          NULL
            #,zip                    VARCHAR(5)          NULL
            #,localita               VARCHAR(50)         NULL
            #,provincia              VARCHAR(50)         NULL
            #,stato                  VARCHAR(50)         NULL
            #,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
            #,UNIQUE (id, id_scheda));
        recapitiSpedizioniTable = Table('recapiti_spedizioni', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('referente',String(200),nullable=True),
                            Column('presso',String(200),nullable=True),
                            Column('via_piazza',String(100),nullable=True),
                            Column('num_civ',String(10),nullable=True),
                            Column('zip',String(5),nullable=True),
                            Column('localita',String(50),nullable=True),
                            Column('provincia',String(50),nullable=True),
                            Column('stato',String(50),nullable=True),
                            Column('id_scheda',Integer,nullable=True),
                            schema=params['schema'])
        recapitiSpedizioniTable.create(checkfirst=True)

        #CREATE TABLE note_schede (
            #id                      BIGSERIAL       NOT NULL PRIMARY KEY
            #,note_text              text                NULL
            #,note_spedizione        varchar(300)        NULL
            #,note_fornitore         varchar(300)        NULL
            #,note_final             varchar(300)        NULL
            #,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
            #,UNIQUE (id, id_scheda));
        noteSchedeTable = Table('note_schede', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('note_text',text,nullable=True),
                            Column('note_spedizione',String(300),nullable=True),
                            Column('note_fornitore',String(300),nullable=True),
                            Column('note_final',String(300),nullable=True),
                            Column('id_scheda',Integer,nullable=True),
                            schema=params['schema'])
        noteSchedeTable.create(checkfirst=True)

        #CREATE TABLE associazioni_articoli(
            #id              BIGSERIAL   NOT NULL    PRIMARY KEY
            #,id_padre       BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
            #,id_figlio      BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
            #,posizione      INTEGER         NULL
            #-- sono tutti riferimenti esterni alla tabella articolo. Questa tabella associa
            #-- ad n articoli, n altri articoli della stessa tabella
            #,UNIQUE (id_padre,id_figlio));
        associazioniArticoliTable = Table('associazioni_articoli', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_padre',Integer,nullable=True),
                            Column('id_figlio',Integer,nullable=True),
                            Column('posizione',Integer,nullable=True),
                            schema=params['schema'])
        associazioniArticoliTable.create(checkfirst=True)

        #CREATE TABLE promemoria_schede_ordinazioni (
        #id              bigint       NOT NULL PRIMARY KEY REFERENCES promemoria(id) ON UPDATE CASCADE ON DELETE CASCADE
        #,id_scheda      bigint       NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE);
        promemoriaSchedeOrdinazioniTable = Table('promemoria_schede_ordinazioni', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_scheda',Integer,nullable=False),
                            schema=params['schema'])
        promemoriaSchedeOrdinazioniTable.create(checkfirst=True)

        #CREATE TABLE sconti_righe_schede (
        #id          bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
        #,id_riga_scheda   bigint          NOT NULL REFERENCES righe_schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE);
        scontiRigheSchedeTable = Table('sconti_righe_schede', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_riga_scheda',Integer,nullable=False),
                            schema=params['schema'])
        scontiRigheSchedeTable.create(checkfirst=True)

        #CREATE TABLE righe_schede_ordinazioni (
        #id                       bigint          NOT NULL PRIMARY KEY REFERENCES riga ( id ) ON UPDATE CASCADE ON DELETE CASCADE
        #,id_scheda                bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE);
        scontiRigheSchedeTable = Table('sconti_righe_schede', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_riga_scheda',Integer,nullable=False),
                            schema=params['schema'])
        scontiRigheSchedeTable.create(checkfirst=True)

        #CREATE TABLE sconti_schede_ordinazioni (
        #id     bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
        #,id_scheda_ordinazione   bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE);
        scontiSchedeOrdinazioniTable = Table('sconti_schede_ordinazioni', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_scheda_ordinazione',Integer,nullable=False),
                            schema=params['schema'])
        scontiSchedeOrdinazioniTable.create(checkfirst=True)

        conf.PromoWear.primoavvio = "no"
        conf.save()
