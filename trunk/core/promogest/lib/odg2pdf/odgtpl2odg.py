# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
import zipfile
import xml.etree.cElementTree as ElementTree

class OdgParser(object):
    def __init__(self, odg_file=None):
        odg_file = "/home/vete/test.odg"
        self.filename = odg_file
        self.m_odf = zipfile.ZipFile(odg_file)
        self.filelist = self.m_odf.infolist()
        ostr = self.m_odf.open('content.xml')
        self.doc = ElementTree.parse(ostr)
        #fil = self.filelist["content.xml"].filename
        print "DOC", self.doc

        #self.namelist = self.m_odf.namelist()
        #print self.namelist ,self.doc
        self.root = self.doc.getroot()
        print "ROOT", self.root
        #for child in self.root:
            #print child.tag, child.attrib
        for c  in self.doc.iter(tag='{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-column'):
            print c.tag, c.attrib
        self.body = self.root.findall('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}page')
        print self.body
#        print self.root.findall('urn:oasis:names:tc:opendocument:xmlns:office:body:page')
#        for neighbor in self.body:
#            print "AAAAAAAAA", neighbor.tag
        #self.showManifest()

    def showManifest(self):
        """
        Just tell me what files exist in the ODF file.
        """
        for s in self.filelist:
            #print s.orig_filename, s.date_time
            print s.filename
            #print s.orig_filename









if __name__ == '__main__':
    OdgParser()
