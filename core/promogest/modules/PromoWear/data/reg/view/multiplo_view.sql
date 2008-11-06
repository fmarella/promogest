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
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

/*

Multiplo - Vista

*/


DROP VIEW v_multiplo;

CREATE OR REPLACE VIEW v_multiplo AS
    SELECT 
         M.id
        ,M.denominazione_breve
        ,M.denominazione
        ,M.id_unita_base
        ,M.id_articolo
        ,M.moltiplicatore
    FROM multiplo M;


DROP VIEW v_multiplo_completa;

CREATE OR REPLACE VIEW v_multiplo_completa AS
    SELECT 
         M.id
        ,M.denominazione_breve
        ,M.denominazione
        ,M.id_unita_base
        ,M.id_articolo
        ,M.moltiplicatore
        ,A.codice AS codice_articolo
        ,A.denominazione AS articolo
        ,U.denominazione AS unita_base
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
    FROM multiplo M
    LEFT OUTER JOIN articolo A ON M.id_articolo = A.id
    LEFT OUTER JOIN promogest.unita_base U ON M.id_unita_base = U.id
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id
    WHERE (M.id_articolo IS NULL OR (M.id_articolo IS NOT NULL AND A.cancellato = False));
