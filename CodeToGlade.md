# Introduction #

L'obiettivo di questa attività è quella di spostare la creazione di vari widget (es. CellRendererText, ListStore) utilizzati per le interfacce di PromoGest, nei rispettivi file glade.

# Dettagli #

**Glade** alla versione 3.8 va bene per portare i file a 2.24, fare una prima scrematura delle comboboxEntry che vanno sostituite con combobox has\_entry = True.
Glade3.10 porta invece l'intero file glade a gtk3. La nuova funzione di preview è molto utile e permette di vedere anche i widget minori con minore approssimazione.

Alcuni problemi si stanno verificando nel porting delle treeview in fase di recupero dati. Pygi obbliga al passaggio di argomenti normalmente di default.

## Stato ##

_Attenzione: a causa dei lavori in corso sull'attività, le informazioni contenute potrebbero essere obsolete._

**Core**:
| Nome | Anag. S/C |
|:-----|:----------|
| Anag. Banche | X |
| Anag. Categorie Articoli | X |
| Anag. Categorie Clienti | X |
| Anag. Categorie Fornitori | X |
| Anag. Destinazione merce | X |
| Anag. Imballaggi | X |
| Anag. Magazzini | X |
| Anag. Multipli | X |
| Anag. Pagamenti | X |
| Elenco Listini | X |
| Elenco Magazzini | X |

**Moduli**:
| Nome modulo | Anag. S/C |
|:------------|:----------|
| ADR | X |
| Agenti | X |
| Contatti | X |
| DistintaBase | wip - fmarl |
| ExportToPos | - |
| GestioneImmagini |  |
| ImportContacts |  |
| Label |  |
| ModuloGenerico | - |
| Multilingua |  |
| PrimaNota | X |
| GestioneNoleggio |  |
| GestioneCommesse |  |
| GestioneMatricole |  |
| ImportPriceList |  |
| InfoPeso | wip - fmarl |
| Inventario |  |
| Promemoria |  |
| SincroDB | - |
| SchedaLavorazione |  |
| Statistiche |  |
| NumerazioneComplessa |  |
| VenditaDettaglio |  |
| RuoliAzioni |  |
| MailAndFax |  |
| Pagamenti |  |
| PromoWear |  |
| SuMisura |  |

# Screenshots #

![http://dl.dropbox.com/u/8630608/PromoGest3/Accesso_PromoGest3_001.png](http://dl.dropbox.com/u/8630608/PromoGest3/Accesso_PromoGest3_001.png)

![http://dl.dropbox.com/u/8630608/PromoGest3/PromoGest3_main_002.png](http://dl.dropbox.com/u/8630608/PromoGest3/PromoGest3_main_002.png)

![http://dl.dropbox.com/u/8630608/PromoGest3/Dati%20articolo_Pg3_003.png](http://dl.dropbox.com/u/8630608/PromoGest3/Dati%20articolo_Pg3_003.png)

![http://dl.dropbox.com/u/8630608/PromoGest3/Finestra%20di%20configurazione%20PromoGest3_004.png](http://dl.dropbox.com/u/8630608/PromoGest3/Finestra%20di%20configurazione%20PromoGest3_004.png)