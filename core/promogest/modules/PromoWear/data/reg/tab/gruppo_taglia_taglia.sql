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

gruppo_taglia_taglia - Tabella associazioni gruppo_taglia <-> taglia 

*/



DROP TABLE gruppo_taglia_taglia CASCADE;

CREATE TABLE gruppo_taglia_taglia (
     id_gruppo_taglia       bigint      NOT NULL REFERENCES gruppo_taglia ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_taglia              bigint      NOT NULL REFERENCES taglia( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,ordine                 bigint      NOT NULL
    
    ,PRIMARY KEY ( id_gruppo_taglia, id_taglia )
);

INSERT INTO gruppo_taglia_taglia ( id_gruppo_taglia, id_taglia, ordine ) VALUES (1, 1, 1);
