# Problemi/Soluzioni #
  1. P: utilizzo di librerie di terze parti inserite in promogest (es. feedparser)
> > S: rimuovere queste librerie dai sorgenti e installare tramite package manager / easy\_install
  1. P:  modulo **six** come nuova dipendenza per compatibilità tra Python 2/3
> > S: installare il modulo tramite package manager / easy\_install
  1. P: ooolib-python è deprecato
> > S: utilizzare [odslib-python](http://code.google.com/p/odslib-python/) (supporta python 2/3)
  1. P: print diventa una funzione in python3
> > S: utilizzare ` from __future__ import print_function ` come primo import dove necessario
  1. P: import dei moduli in python3
> > S: utilizzare ` from __future__ import absolute_import ` e revisionare tutti gli import

# Dettagli #

## Stato delle dipendenze ##

compatibili con py3:
  * sqlalchemy
  * jinja2
  * Gtk, Gdk, Webkit, Poppler, ect via gi
  * reportlab

non compatibili:
  * [html5lib](http://code.google.com/p/html5lib/), (presenta alcuni bug, esistono patch per renderlo compatibile)
  * [pisa,xhtml2pdf](https://github.com/chrisglass/xhtml2pdf) (~~una versione specifica verrà rilasciata appena python 3 sarà stabile~~

## Strumenti utili ##

Il pacchetto _python-tools_ contiene lo script **2to3** utilizzato per la traduzione automatica del codice dalla versione 2 alla 3.

Da terminale eseguire il comando:
```
$ cd promogest/core
$ 2to3 -n -w .
```

Glade e custom widget necessita di essere compilato con il supporto a python3. Vedi [bug 732328](https://bugzilla.gnome.org/show_bug.cgi?id=732328,)

# Altre info #

Nota. Ctrl+c non funziona perchè ancora non implementato ma si può usare in alternativa ctrl+4 ."It is not trivial" come mi hanno detto su #python

# Links #
[Writing Forwards Compatible Python Code](http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/)

[Promogest](http://www.promogest.me)