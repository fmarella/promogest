#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from promogest.modules.SincroDB.ui.SincroDB import SincroDB
from optparse import OptionParser
from config import Config

class Pg2Sincro(object):
    def __init__(self):
        usage = """Uso: %prog [options]
            Opzioni disponibili sono :
                -c   --configure  Quale configure utilizzare
                -s   --schema Quale schema dev'essere utilizzato
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-f", "--fileconf",
                            #action="store_true",
                            help="Necessario per definire quale configure utlizzare",
                            default="",
                            type="string",
                            dest="Configure")
        parser.add_option("-s", "--schema",
                            #action="store_true",
                            help="definizione dello schema in uso",
                            default="",
                            type="string",
                            dest="Schema")

        (options, args) = parser.parse_args()
        if options.Schema:
            schema = options.Schema
        configure = options.Configure
        new_conf = Config(configure)
        print "CONFFFFF", new_conf
        sla22 = SincroDB(batch=True, conf=new_conf, fileconf=configure, schema=schema).on_run_button_clicked()
        #login.run()

if __name__ == '__main__':
    Pg2Sincro()
