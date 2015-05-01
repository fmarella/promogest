# FatturaPA notes #

Specifiche Operative dal sito: http://indicepa.gov.it/documentale/index.php

http://indicepa.gov.it/public-services/docs-read-service.php?dstype=FS&filename=IDENTIFICAZIONE_UNIVOCA_UFFICI_FATTURAZIONE_ELETTRONICA.pdf

le informazioni sotto forma di dataset sono disponibili tramite il formato Open data.

```
Gli attributi dei dataset open data contenenti i dati utili al processo di fatturazione elettronica sono
riportati in tabella 5 colonna B.
I dataset sono aggiornati ogni 24 ore, alle ore 6.00 del mattino.
```

nello stesso documento vengono specificate le informazioni necessarie per la creazione del servizio di fatturazione elettronica. Vedi **tabella 5**.


---


data di fine trasporto deve essere nel formato lungo
es. 2012-10-22T16:46:12.000+02:00

TipoDocumento ->
> TD01 Fattura
> TD02 Acconto / anticipo su fattura
> TD03 Acconto / anticipo su parcella
> TD04 Nota di credito
> TD05 Nota di debito
> TD06 Parcella

TipoRitenuta ->
> RT01 Ritenuta di acconto persone fisiche
> RT02 Ritenuta di acconto persone giuridiche

CondizioniPagamento ->
> TP01 (pagamento a rate)
> TP02 (pagamento completo)
> TP03 (anticipo)

TODO: scrivere la funzione getModalitaPagamento in utils che traduce scadenza.pagamento in una modalità corrispondente tra quelle elencate qui sotto.
ModalitaPagamentoType ->
> MP01 contanti
> MP02 assegno
> MP03 assegno circolare
> MP04 contanti presso Tesoreria
> MP05 bonifico
> MP06 vaglia cambiario
> MP07 bollettino bancario
> MP08 carta di credito
> MP09 RID
> MP10 RID utenze
> MP11 RID veloce
> MP12 RIBA
> MP13 MAV
> MP14 quietanza erario
> MP15 giroconto su conti di contabilità speciale
> MP16 domiciliazione bancaria
> MP17 domiciliazione postale