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

Inventario  - Vista

*/


DROP VIEW v_inventario;

CREATE OR REPLACE VIEW v_inventario AS
    SELECT  
         I.id
        ,I.anno
        ,I.id_magazzino
        ,I.id_articolo
        ,I.quantita
        ,I.valore_unitario
        ,I.data_aggiornamento
    FROM inventario I;


DROP VIEW v_inventario_completa;

CREATE OR REPLACE VIEW v_inventario_completa AS
    SELECT 
         I.id
        ,I.anno
        ,I.id_magazzino
        ,I.id_articolo
        ,I.quantita
        ,I.valore_unitario
        ,I.data_aggiornamento
        ,M.denominazione AS magazzino
        ,A.codice AS codice_articolo
        ,A.denominazione AS articolo
        ,A.produttore AS produttore
        ,CB.codice AS codice_a_barre
        ,F.codice_articolo_fornitore AS codice_articolo_fornitore
        ,A.id_aliquota_iva
        ,AI.denominazione_breve AS denominazione_breve_aliquota_iva
        ,AI.denominazione AS denominazione_aliquota_iva
        ,AI.percentuale AS percentuale_aliquota_iva
        ,A.id_famiglia_articolo
        ,FA.denominazione_breve AS denominazione_breve_famiglia
        ,FA.denominazione AS denominazione_famiglia
        ,A.id_categoria_articolo
        ,CA.denominazione_breve AS denominazione_breve_categoria
        ,CA.denominazione AS denominazione_categoria
        ,A.id_unita_base
        ,UB.denominazione_breve AS denominazione_breve_unita_base
        ,UB.denominazione AS denominazione_unita_base
        ,ATC.id_articolo_padre
        ,ATC.id_gruppo_taglia
        ,GT.denominazione_breve AS denominazione_breve_gruppo_taglia
        ,GT.denominazione AS denominazione_gruppo_taglia
        ,ATC.id_taglia
        ,T.denominazione_breve AS denominazione_breve_taglia
        ,T.denominazione AS denominazione_taglia
        ,ATC.id_colore
        ,C.denominazione_breve AS denominazione_breve_colore
        ,C.denominazione AS denominazione_colore
        ,ATC.id_anno
        ,AAB.denominazione AS anno_abbigliamento
        ,ATC.id_stagione
        ,SAB.denominazione AS stagione_abbigliamento
        ,ATC.id_genere
        ,GAB.denominazione AS genere_abbigliamento
    FROM inventario I
    LEFT OUTER JOIN magazzino M ON I.id_magazzino = M.id
    LEFT OUTER JOIN articolo A ON I.id_articolo = A.id
    LEFT OUTER JOIN aliquota_iva AI ON A.id_aliquota_iva = AI.id
    LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id
    LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id
    LEFT OUTER JOIN promogest.unita_base UB ON A.id_unita_base = UB.id
    LEFT OUTER JOIN codice_a_barre_articolo CB ON A.id = CB.id_articolo AND CB.primario
    LEFT OUTER JOIN fornitura F ON A.id = F.id_articolo AND F.fornitore_preferenziale
    LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo
    LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id
    LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id
    LEFT OUTER JOIN colore C ON ATC.id_colore = C.id
    LEFT OUTER JOIN promogest.anno_abbigliamento AAB ON ATC.id_anno = AAB.id
    LEFT OUTER JOIN promogest.stagione_abbigliamento SAB ON ATC.id_stagione = SAB.id
    LEFT OUTER JOIN promogest.genere_abbigliamento GAB ON ATC.id_genere = GAB.id
    WHERE A.cancellato = False;
