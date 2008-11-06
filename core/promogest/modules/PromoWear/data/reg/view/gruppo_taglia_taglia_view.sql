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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

GruppoTaglia <-> Taglia  - Vista sulle taglie

*/


DROP VIEW v_gruppo_taglia_taglia;

CREATE OR REPLACE VIEW v_gruppo_taglia_taglia AS
        SELECT   GTT.id_gruppo_taglia
                ,GTT.id_taglia
                ,GTT.ordine
                ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
                ,GT.denominazione AS denominazione_gruppo_taglia
                ,T.denominazione_breve AS denominazione_breve_taglia
                ,T.denominazione AS denominazione_taglia
        FROM gruppo_taglia_taglia GTT
        LEFT OUTER JOIN gruppo_taglia GT ON GTT.id_gruppo_taglia = GT.id
        LEFT OUTER JOIN taglia T ON GTT.id_taglia = T.id;
