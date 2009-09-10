--
-- Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth#gmail.com>
--
-- This program is free software; you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation; either version 2
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

testata_documento_scadenza - Tabella scadenze per la testata documento

*/


DROP TABLE testata_documento_scadenza CASCADE;

DROP SEQUENCE testata_documento_scadenza_id_seq;
CREATE SEQUENCE testata_documento_scadenza_id_seq;

CREATE TABLE testata_documento_scadenza (
     id                         bigint          DEFAULT NEXTVAL('testata_documento_scadenza_id_seq') PRIMARY KEY NOT NULL
    ,id_testata_documento       bigint          NOT NULL REFERENCES testata_documento ( id ) ON UPDATE CASCADE ON DELETE CASCADE 
    ,data                       date            NOT NULL
    ,importo                    decimal(16,4)   NOT NULL 
    ,pagamento                  varchar(100)    NOT NULL
    ,data_pagamento             date            NULL
    ,numero_scadenza            bigint          NOT NULL
);
