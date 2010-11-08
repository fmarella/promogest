# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>
# Copyright (C) 2008-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>

import sys
import os
import math
import datetime
import time
from reportlab.lib import colors, utils
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import cm, inch, A4, landscape
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
import xml.etree.cElementTree as ElementTree

import Sla2pdfUtils

from SlaParser import SlaParser
from optparse import OptionParser


# KNOWN BUGS
# ****************************************************************
# Fonts don't selectable
# Double itexts or more, don't work (see also Paragraph)
# Tags live only in tables, at least 1x1
# Wrong tags break the program

# Fonts working
##const QString tmpf[] = {"/Courier", "/Courier-Bold", "/Courier-Oblique", "/Courier-BoldOblique",
##                        "/Helvetica", "/Helvetica-Bold", "/Helvetica-Oblique", "/Helvetica-BoldOblique",
##                        "/Times-Roman", "/Times-Bold", "/Times-Italic", "/Times-BoldItalic",
##                        "/ZapfDingbats", "/Symbol"};

## New tag  for 0.4 version :   [[bcview(codice_a_barre,1X2)]]  where bcview is
## function, codice_a_barre is the tag and 1X2 are width and height also decimal dot separated is allow. ( 1X0.8)
## Image Size fixed on pdf convertion.
# fixed fontsize recognition with standard font if not setted

VERSION = "0.6"

class Sla2Pdf(object):

    def __init__(self, slaFileName=None,pdfFolder=None, report=False,
                        label=False, slafile=None):
        print "SLAFILENAME" , slaFileName
        print "PDF_FOLDER", pdfFolder
        print "SLAFILE", slafile

        self.slaFileName = slaFileName
        self.pdfFolder = pdfFolder
        self.slafile = slafile
        self.report = report
        self.label = label

    def createPDF(self, daos=None,objects=None, classic=None, template_file=None):
        self.objects = objects
        self.daos = daos
#        print "SELF DAOSSSS", objects, daos
        if self.objects or self.daos:
            from promogest import Environment
            self._classic = classic
            self._template_file = template_file
            if template_file:
                self.slaFileName = Environment.labelTemplatesDir+template_file
            version = SlaParser(slaFileName=self.slaFileName,
                                    pdfFolder=self.pdfFolder,
                                    slafile=self.slafile).scribusVersion()
            if not version:
                from Sla2Pdf_classic import Sla2Pdf_classic
                slatopdf = Sla2Pdf_classic(pdfFolder = self.pdfFolder,
                                    slaFileName = self.slaFileName,
                                    report = self.report).serialize(objects, dao=daos)
                result = None
                filename = self.pdfFolder+"_temp.pdf"
                print "FILENAME FINALEEEEE", filename
                f = file(filename, 'rb')
                result = f.read()
                f.close()
                #os.remove(filename)
                return result
            else:
                self.slaToSla(objects=objects, daos=daos)
            result = None
            # temporary pdf file is removed immediately
            filename = self.pdfFolder+"_temppp.pdf"
            #print "FILENAME FINALEEEEE", self.pdfFolder + "_temp" + '.pdf'
            f = file(filename, 'rb')
            result = f.read()
            f.close()
            #os.remove(filename)
            return result
        else:
            print "QUESTO é SOLO PER LA CONVERSIONE"
            self.toPdf()

    def toPdf(self):
        #if version ==True:
        from Sla2Pdf_ng import Sla2Pdf_ng
        slatopdf = Sla2Pdf_ng(slafile=self.slafile).translate()
        return slatopdf
        #else:


    def slaToSla(self, objects=None, daos=None):

        """ Model parsing, values substitution and pdf creation """
        print "QUESTO DEVE PASSARE PER SLATPL2SLA"
        from SlaTpl2Sla import SlaTpl2Sla
        self.slatpl = SlaTpl2Sla(   slafile = self.slafile,
                                    label =self.label,
                                    objects = objects,
                                    daos=daos,
                                    report = self.report,
                                    slaFileName = self.slaFileName,
                                    pdfFolder =self.pdfFolder,
                                    classic=self._classic,
                                    template_file=self._template_file
                                )



class runSla2pdf(object):
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
    runSla2pdf()
