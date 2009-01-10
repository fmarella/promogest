--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Dr astico (Marco Pinna) <zoccolodignu@gmail.com>
--

/*
 * CREAZIONE TABELLE DB PER MODIFICA nome in codice"STAMPALUX"
 */

DROP TABLE schede_ordinazioni ;
DROP TABLE contatti_schede ;
DROP TABLE datari ;
DROP TABLE recapiti_spedizioni ;
DROP TABLE note_schede ;
DROP TABLE colori_stampa ;
DROP TABLE caratteri_stampa ;
DROP TABLE associazioni_articoli ;
DROP TABLE articoli_schede_ordinazioni ;
DROP TABLE sconto_scheda_ordinazione ;
DROP TABLE riga_scheda_ordinazione ;
DROP TABLE promemoria_schede_ordinazioni ;


CREATE TABLE colori_stampa (
    id                      BIGSERIAL   NOT NULL PRIMARY KEY
    ,denominazione          VARCHAR(50) NOT NULL
    ,UNIQUE (id, denominazione)
);

CREATE TABLE caratteri_stampa (
    id                      BIGSERIAL   NOT NULL PRIMARY KEY
    ,denominazione          VARCHAR(50) NOT NULL
    ,UNIQUE (id, denominazione)
);

CREATE TABLE schede_ordinazioni
(
  id bigserial NOT NULL ,
  numero int8 NOT NULL,
  nomi_sposi varchar(100),
  mezzo_ordinazione varchar(50),
  mezzo_spedizione varchar(50),
  bomba_in_cliche bool NOT NULL DEFAULT false,
  codice_spedizione varchar(100),
  ricevuta_associata varchar(50),
  fattura bool DEFAULT false,
  documento_saldato bool DEFAULT false,
  operatore varchar(50) NOT NULL,
  provenienza varchar(50),
  disp_materiale bool NOT NULL DEFAULT true,
  applicazione_sconti varchar(20),
  totale_lordo numeric(16,4) DEFAULT 0,
  userid_cliente varchar(50),
  passwd_cliente varchar(15),
  lui_e_lei varchar(50),
  id_colore_stampa int8 NOT NULL,
  id_carattere_stampa int8 NOT NULL,
  id_cliente int8,
  id_magazzino int8,
  CONSTRAINT schede_ordinazioni_pkey PRIMARY KEY (id),
  CONSTRAINT schede_ordinazioni_id_carattere_stampa_fkey FOREIGN KEY (id_carattere_stampa)
      REFERENCES caratteri_stampa (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_cliente_fkey FOREIGN KEY (id_cliente)
      REFERENCES cliente (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_magazzino_fkey FOREIGN KEY (id_magazzino)
      REFERENCES magazzino (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_colore_stampa_fkey FOREIGN KEY (id_colore_stampa)
      REFERENCES colori_stampa (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_key UNIQUE (id, numero)
);


CREATE TABLE contatti_schede (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,referente              VARCHAR(100)        NULL
    ,prima_email            VARCHAR(100)        NULL
    ,seconda_email          VARCHAR(100)        NULL
    ,telefono               VARCHAR(15)         NULL
    ,cellulare              VARCHAR(15)         NULL
    ,skype                  VARCHAR(30)         NULL
    ,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id,id_scheda)
);

/*
CREAZIONE TABELLA datari
*/


CREATE TABLE datari (
	id			            BIGSERIAL	PRIMARY KEY
	,matrimonio		        date		NOT NULL
	,presa_in_carico	    date		NOT NULL
	,ordine_al_fornitore	date		    NULL
	,consegna_bozza		    date		    NULL
	,spedizione		        date		    NULL
	,consegna		        date		    NULL
	,ricevuta               date            NULL
	,id_scheda              BIGINT      NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);

/*
 * CREAZIONE TABELLE INDIRIZZI E CONTATTI
 *
 */



CREATE TABLE recapiti_spedizioni (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,referente              VARCHAR(100)        NULL
    ,presso                 VARCHAR(100)        NULL
    ,via_piazza             VARCHAR(50)         NULL
    ,num_civ                VARCHAR(5)          NULL
    ,zip                    VARCHAR(5)          NULL
    ,localita               VARCHAR(50)         NULL
    ,provincia              VARCHAR(50)         NULL
    ,stato                  VARCHAR(50)         NULL
	,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);



CREATE TABLE note_schede (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,note_text              text                NULL
    ,note_spedizione        varchar(300)        NULL
    ,note_fornitore         varchar(300)        NULL
    ,note_final             varchar(300)        NULL
	,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);


CREATE TABLE associazioni_articoli(
    id              BIGSERIAL   NOT NULL    PRIMARY KEY
	,id_padre	    BIGINT  	    NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
	,id_figlio	    BIGINT	        NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
	,posizione      INTEGER         NULL
	-- sono tutti riferimenti esterni alla tabella articolo. Questa tabella associa
	-- ad n articoli, n altri articoli della stessa tabella
	,UNIQUE (id_padre,id_figlio));




CREATE TABLE sconti_schede_ordinazioni (
     id                         bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_scheda_ordinazione       bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE righe_schede_ordinazioni (
       id                       bigint          NOT NULL PRIMARY KEY REFERENCES riga ( id ) ON UPDATE CASCADE ON DELETE CASCADE
      ,id_scheda                bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE sconti_righe_schede (
     id                         bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_riga_scheda             bigint          NOT NULL REFERENCES righe_schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE promemoria_schede_ordinazioni (
    id                          bigint       NOT NULL PRIMARY KEY REFERENCES promemoria(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_scheda                   bigint       NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
);
