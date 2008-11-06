--
-- Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
-- Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

Informazioni contabili documento

*/


DROP TABLE informazioni_contabili_documento CASCADE;

DROP SEQUENCE informazioni_contabili_documento_id_seq;
CREATE SEQUENCE informazioni_contabili_documento_id_seq;

CREATE TABLE informazioni_contabili_documento (
    id                          bigint      DEFAULT NEXTVAL('informazioni_contabili_documento_id_seq') PRIMARY KEY NOT NULL
    ,documento_saldato          boolean     NOT NULL DEFAULT FALSE
    ,id_documento               bigint      NOT NULL REFERENCES testata_documento ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_primo_riferimento       bigint          NULL REFERENCES testata_documento ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_secondo_riferimento     bigint          NULL REFERENCES testata_documento ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,totale_pagato              decimal(16,4)   NOT NULL DEFAULT 0
    ,totale_sospeso             decimal(16,4)   NOT NULL DEFAULT 0


,UNIQUE( id_primo_riferimento, id_secondo_riferimento )

);
