#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from ui.SincroDb import SincroDb

class Pg2Sincro(object):
    def __init__(self):
        usage = """Uso: %prog [options]
            Opzioni disponibili sono :
                -i   --input Per visualizzare con delle print i dizionari dao
                -o   --output Per visualizzare maggiori informazioni sui filtri
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-i", "--input",
                            #action="store_true",
                            help="Per visualizzare con delle print i dizionari dao",
                            default="False",
                            type="string",
                            dest="Input")
        parser.add_option("-o", "--output",
                            #action="store_true",
                            help="Per mettere il debug al massimo",
                            default="",
                            #type="string",
                            dest="Output")

        (options, args) = parser.parse_args()
        if options.Input:
            slafile = options.Input
        if options.Output:
            slaout = slafile
        sla22 = Sla2Pdf(slafile=slafile).createPDF()
        #login.run()

if __name__ == '__main__':
    Pg2Sincro()