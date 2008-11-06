--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Alessandro Scano <alessandro@promotux.it>
--
-- This program is free software; you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation; either version 2
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

/*

riga - Tabella riga documento / movimento

*/

DROP TABLE riga CASCADE;
DROP TABLE riga_movimento CASCADE;
DROP TABLE riga_documento CASCADE;

DROP SEQUENCE riga_documento_id_seq;
CREATE SEQUENCE riga_documento_id_seq;

CREATE TABLE riga (
      id                        bigint          DEFAULT NEXTVAL('riga_documento_id_seq') PRIMARY KEY NOT NULL
     ,valore_unitario_netto     decimal(16,4)   NULL
     ,valore_unitario_lordo     decimal(16,4)   NULL
     ,quantita                  decimal(16,4)   NOT NULL
     ,moltiplicatore            decimal(15,6)   NOT NULL
     ,applicazione_sconti       varchar(20)     NULL
     ,percentuale_iva           decimal(8,4)    NOT NULL DEFAULT 0
     ,descrizione               varchar(100)    NULL
     -- Chiavi esterne
     ,id_listino                bigint          NULL REFERENCES listino ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
     ,id_magazzino              bigint          NULL REFERENCES magazzino ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
     ,id_articolo               bigint          NULL REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
     ,id_multiplo               bigint          NULL REFERENCES multiplo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
     
     ,CHECK ( ( applicazione_sconti = 'scalare' ) OR ( applicazione_sconti = 'non scalare' ) )
);

CREATE TABLE riga_movimento (
       id                       bigint          NOT NULL PRIMARY KEY REFERENCES riga ( id ) ON UPDATE CASCADE ON DELETE CASCADE
     -- Chiavi esterne
      ,id_testata_movimento     bigint          NOT NULL REFERENCES testata_movimento ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE riga_documento (
       id                       bigint          NOT NULL PRIMARY KEY REFERENCES riga ( id ) ON UPDATE CASCADE ON DELETE CASCADE
     -- Chiavi esterne
      ,id_testata_documento     bigint          NOT NULL REFERENCES testata_documento ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);
