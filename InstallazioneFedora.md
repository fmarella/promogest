# Installazione di Promogest su Fedora #

**11/05/2011**: Da oggi, grazie al contributo di Francesco 'fmarl' Marella, è disponibile il _pacchetto rpm_ per Fedora, Opensuse e Mandriva. (Testato su F15). Potete scaricarlo [qui](ftp://promotux.it/promogest-2.7.2-1.fc15.noarch.rpm)

## Procedura manuale ##

Il procedimento di installazione del Promogest è stato testato su Fedora 15 (alpha del 16 Aprile 2011) su macchina virtuale tramite un live CD.

Il primo passo è quello di installare gli strumenti utili a creare una copia locale del promogest su disco locale:
Da terminale installiamo _subversion_:
```
# yum install subversion
```

Promogest dipende dai seguenti moduli Python disponibili nel repository:
```
python-sqlalchemy
python-reportlab
python-jinja2
pywebkitgtk
pypoppler
pysvn
```

mentre per le seguenti dipendenze, non presenti nel repository, è necessario digitare da terminale:
```
# yum install python-setuptools
```
e quindi:
```
# easy_install html5lib
# easy_install pisa
```

Possiamo procedere ora all'installazione del Promogest sulla macchina, cosi come viene descritto [qui](http://www.promogest.me/promoGest/cms/installa-promogest-su-linux),  nella sezione Installazione Sorgenti PromoGest2.