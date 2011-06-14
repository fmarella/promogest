.. _vendita_dettaglio:


=====================================
Gestione Negozio ( Vendita Dettaglio)
=====================================

Dettaglio:
==========

Tra i moduli a disposizione del PromoGest ce n'è uno che si occupa di gestire la vendita al dettaglio tramite una interfaccia  dedicata. Vedremo nelle prossime immagini come è strutturata ed, a grandi linee, quali operazioni è possibile effettuare.

La prima immagine ci mostrerà la collocazione dell'icona di accesso alla sezione di vendita al dettaglio. Esistea anche un derivato di servizio del PromoGest battezzato Shop che permette l'accesso diretto alla sola schermata di vendita ma consideriamo quello all'interno del cerchio rosso come l'accesso classico al modulo dalla applicazione già in uso.

.. image:: http://dl.dropbox.com/u/8630608/venditaDettaglio/Selezione_020.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Selezione_020.jpeg

Come prima cosa ci verrà proposta una finestra di dialogo che ci chiederà di selezionare un "magazzino o punto vendita" ed un "punto cassa" che naturalmente potremo gestire tramite apposite anagrafiche. ( Simili a quelle di categoria articolo o categorie cliente ... ) .La selezione richiesta è utile in quanto la vendita verrà così abbinata ad un punto vendita ed all'interno dello stesso ad un singolo Punto cassa, l'abbinamento del modulo di profilazione utente e ruolo permette anche di registrare l'operatore che ha svolto l'operazione.



.. image:: http://dl.dropbox.com/u/8630608/venditaDettaglio/Attenzione_004.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Attenzione_004.jpeg

Interfaccia principale di vendita.
__________________________________

Nella parte superiore abbiamo le tre aree di ricerca diretta. La prima sarà quella dedicata al codice a barre, la troveremo sempre selezionata allingresso del modulo, dopo l'inserimento di una riga o dopo la chiusura di uno scontrino. Le altre due permettono una ricerca più classica e meno veloce per codice articolo e per descrizione. C'è comunque anche la possibilità di ricerca usando la classica finestra di ricerca complessa presente in altre parti dell'applicazione.

Poco sotto c'è una area informativa dove vengono inserii i dati relativi all'articolo che si sta vendendo. Informazioni su taglie e colori o eventuali giacenze di magazzino.

Arriviamo poi ad una fila di bottoni per svolgere le operazioni di annullamento dell'inserimento riga, di reso di un articolo , di cancellazione della riga selezionata ed un bottone che predispone l'interfaccia al futuro utilizzo con il touch screen che visualizza una tastiera numerica a video.

Ancora sotto c'è l'area dove vengono inserite e visualizzate le rige. Caratteri grandi ben visibili ci informano del codice della descrizione, del codice a barre e del prezzo ( modificabile cliccando direttamente sull'area ), un eventuale sconto e chiaramente la quantità anch'essa modificabile direttamente.

Abbiamo poi il frame dei metodi di pagamento. Con F1 Si accede al pagamento per contanti ma abbiamo anche quello con Assegno o con carta di credito per cui è addirittura possibile abbinare una tipologia di carta gestità come i punti cassa da una apposita anagrafica. C'è un'area per l'inserimento dello sconto scontrino quindi complessivo.

C'è poi l'area di riepilogo dei totali, che come potete vedere riporta un totale parziale, un eventuale sconto, un Totale finale italianizzato ( con punti e virgole come si usa  normalmente ) ed un possibile resto da restituire se il pagamento avviene in contanti.

A a destra in basso ci sono poi i bottoni di annullamento scontrino , di calcolo del subtotale utile quando si gestiscono degli sconti e quello di TOTALE/CHIUSURA scontrino ( F5 ) che si occuperà di chiudere la vendita e mandare loscontrino in stampa.

C'è poi un bottone di uscita ed uno che riporta la dicitura scontrini che vedremo dopo così come la voce di menu delle operazioni di fine giornata.

Tutte le operazioni si possono svolgere senza l'ausilio del mouse tramite l'uso di comodi shortcut da tastiera e l'uso di tasti funzione.

.. image:: http://www.promogest.me/templates/media/Vendita%20al%20dettaglio_002.png
 :target: http://www.promogest.me/templates/media/Vendita%20al%20dettaglio_002.png
 :width: 700 px



Questa immagine ci mostra come viene gestito dal promogest la vendita di un articolo Generico. Premendo il tasto F9 si ha la possibilità di vendere un articolo non catalogato ( storicamente un settore "varie" ). Sempre con i soli tasti si può definire un costo ed una quantità. Chiaramente l'abuso di una vendita i articoli generici denota una cattiva gestione della anagrafica magazzino dove la soluzione ottimale vorrebbe un rapporto di 1:1 tra anagrafica articolo e reale assortimento alla vendita.


.. image:: http://dl.dropbox.com/u/8630608/venditaDettaglio/Gestione%20articolo%20generico%20F9_019.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Gestione%20articolo%20generico%20F9_019.jpeg

Gestione scontrini
__________________

Questa è la finestra dello *storico Scontrini*.

.. image:: http://www.promogest.me/templates/media/Scontrini%20Emessi_003.png
 :target: http://www.promogest.me/templates/media/Scontrini%20Emessi_003.png
 :width: 700 px

Notiamo subito una divisione in tree aree:
In alto a sinistra abbiamo l'area di ricerca in cui possiamo selezionare tra uno o più fra i seguenti criteri:
 * Articolo. Per sapere quando è stato venduto un determinato articolo, verrà infatti visualizzato l'elenco
   degli scontrini in cui l'articolo è presente
 * Da data - a Data. Due campi che permettono di selezionare un arco temporale di ricerca
 * Mag/ PV. Qui possiamo filtrare per tutti gli scontrini emessi in un determinato punto vendita
 * Punto Cassa. Simile al PV ma relativo al singolo punto cassa all'interno del PV
 * Cliente. novità. Permette di sapere quali scontrini sono stati effettuati ad un determinato cliente se, chiaramente
   gli è stato assegnato lo scontrino stesso

La seconda area a destra è quella dell'anteprima dello scontrino selezionato.
La terza    è quella dell'elenco dei risultati. Ci sono diverse colonne per una visione veloce delle informazioni relative al singolo scontrino.

In aggiunta a queste tre aree possiamo vedere diversi bottoni e combobox:
 * Cliente
 * Tipo Operazione
 * Crea Fattura
 * Reso
 * Elimina
 * Storno
 * Chiudi

TODO: scrivere dei singoli bottoni!

Questa è la distinta di fine giornata.
______________________________________

Molto utile per verificare se i conti tra fondo cassa, incassato e venduto tramite assegni e pos "quadra" con ciò che il gestionale riporta. Abbiamo un'area di riepilogo, una parte dove avremo i parziali divisi per categoria articolo, ( i tradizionali reparti di vendita) ed i totali parziali e complessivi. Naturalmente con la semplice pressione di un tasto possiamo generare un file pdf pronto per la stampa.

.. image:: http://dl.dropbox.com/u/8630608/venditaDettaglio/%22%22_014.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/%22%22_014.jpeg
 :width: 700 px

Dopo aver lavorato per tutto il giorno, subito dopo aver effettuato la chiusura "Z" sul  vostro registratore di cassa si dovrà effettuare la chiusura anche sul  gestionale. Questa operazione creerà un movimento di scarico per venduto da cassa con una riga per ogni articolo venduto e si occuperà di scalare la giacenza.

.. image::  http://dl.dropbox.com/u/8630608/venditaDettaglio/Chiusura%20fine%20giornata_018.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Chiusura%20fine%20giornata_018.jpeg


Le prossime tre immagini sono dei grafici sulle vendite:
________________________________________________________

.. image::  http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_015.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_015.jpeg
 :width: 700 px

.. image::  http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_016.jpeg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_016.jpeg
 :width: 700 px

.. image::  http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_017.jpeg
 :target:  http://dl.dropbox.com/u/8630608/venditaDettaglio/Chart%20statistiche%20PromoGest2_017.jpeg
 :width: 700 px

DITRON
______
Questa è l'immagine di una Ditron ZIP, registratore di cassa ampiamente collaudato con il nostro gestionale. Ma sono supportate anche le casse olivetti. ( per altre marche contattateci pure a assistenza@promotux.it)

.. image::  http://dl.dropbox.com/u/8630608/venditaDettaglio/zip.jpg
 :target: http://dl.dropbox.com/u/8630608/venditaDettaglio/zip.jpg

OLIVETTI
________
.. image::  http://www.promogest.me/templates/media/20090625%20Listino%20Nettuna%20250%20Olivetti0003-2.jpg
 :target: http://www.promogest.me/templates/media/20090625%20Listino%20Nettuna%20250%20Olivetti0003-2.jpg

E' stato poi migliorato il sistema di collegamento nella vendita al dettaglio o gestione negozio con i misuratori fiscali OLIVETTI, l'utilizzo del driver ELAEXECUTE ( Testato sia su windows che su linux fedora e linux ubuntu) ci permette di collegare al momento questi misuratori fiscali:

 * NETTUNA 200
 * NETTUNA 400
 * NETTUNA 500
 * NETTUNA 600
 * PRT100 FISCALE
 * NETTUNA JET
 * NETTUNA 700
 * NETTUNA 300
 * PRT200 FISCALE
 * NETTUNA  250

*Elenco degli shortcut:*
 * F4 Attiva lo sconto su totale
 * F5 Attiva la chiusura scontrino e invio alla cassa ( pos)
 * F6 Calcola i totali parziali considerando anche gli sconti
 * F1 Attiva il pagamento contanti
 * F2 Pagamento con Assegni
 * F3 Pagamento con Carta di credito
 * F9 Attiva un Articolo Generico ( jolly)
