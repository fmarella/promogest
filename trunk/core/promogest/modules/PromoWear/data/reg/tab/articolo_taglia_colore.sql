--
-- Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
-- Author: Andrea Argiolas <andrea@promotux.it>
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

articolo_taglia_colore - Tabella appendice articoli per la gestione di varianti taglia/colore

*/


DROP TABLE articolo_taglia_colore CASCADE;

CREATE TABLE articolo_taglia_colore (
     id_articolo                bigint          PRIMARY KEY NOT NULL REFERENCES articolo( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_articolo_padre          bigint          NULL REFERENCES articolo( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_gruppo_taglia           bigint          NULL REFERENCES gruppo_taglia( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_taglia                  bigint          NULL REFERENCES taglia( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_colore                  bigint          NULL REFERENCES colore( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_anno                    bigint          NOT NULL REFERENCES promogest.anno_abbigliamento( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_stagione                bigint          NOT NULL REFERENCES promogest.stagione_abbigliamento( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_genere                  bigint          NOT NULL REFERENCES promogest.genere_abbigliamento( id ) ON UPDATE CASCADE ON DELETE RESTRICT

    ,UNIQUE ( id_articolo_padre, id_gruppo_taglia, id_taglia, id_colore )
    ,FOREIGN KEY (id_gruppo_taglia, id_taglia) REFERENCES gruppo_taglia_taglia ( id_gruppo_taglia, id_taglia )
    ,CHECK ( ( ( id_taglia IS NOT NULL ) AND ( id_colore IS NOT NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NOT NULL ) ) OR
             ( ( id_taglia IS NULL ) AND ( id_colore IS NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NULL ) ) )
);
