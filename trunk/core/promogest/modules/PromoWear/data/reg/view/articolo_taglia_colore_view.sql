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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

ArticoloTagliaColore  - Vista

*/


DROP VIEW v_articolo_taglia_colore_completa;

CREATE OR REPLACE VIEW v_articolo_taglia_colore_completa AS
    SELECT  
         ATC.id_articolo
        ,ATC.id_articolo_padre
        ,ATC.id_gruppo_taglia
        ,ATC.id_taglia
        ,ATC.id_colore
        ,ATC.id_anno
        ,ATC.id_stagione
        ,ATC.id_genere
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,AAB.denominazione AS anno
        ,SAB.denominazione AS stagione
        ,GAB.denominazione AS genere
    FROM articolo_taglia_colore ATC
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id 
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id 
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id;
