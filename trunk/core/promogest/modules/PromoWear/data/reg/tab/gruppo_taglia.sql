--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Alessandro Scano <alessandro@test.it>
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

gruppo_taglia - Tabella dei gruppi di taglie

*/


DROP TABLE gruppo_taglia;

DROP SEQUENCE gruppo_taglia_id_seq;
CREATE SEQUENCE gruppo_taglia_id_seq;

CREATE TABLE gruppo_taglia (
     id                         bigint          DEFAULT NEXTVAL('gruppo_taglia_id_seq') PRIMARY KEY NOT NULL
    ,denominazione_breve        varchar(10)     NOT NULL 
    ,denominazione              varchar(200)    NOT NULL
     
    ,UNIQUE ( denominazione_breve )
    ,UNIQUE ( denominazione )
);

INSERT INTO gruppo_taglia ( denominazione_breve, denominazione ) VALUES ('n/a', 'n/a');
