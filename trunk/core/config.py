# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>


import ConfigParser
from ConfigParser import ConfigParser
from datetime import datetime
import os, re



class Section(object):
    def __init__(self, config, name):
        self._name = name
        self._config = config
        
        
    def __setattr__(self, name, value):
        if name not in ('_name','_config'):
            self._config._configDict[self._name][name] = value
        self.__dict__[name] = value
        
        
    def remove_option(self, option):
        if self._config._ini.has_option(self._name, option):
            self._config._ini.remove_option(self._name, option)            
            del(self._config._configDict[self._name][option])
            del(self.__dict__[option])
            
            
    def options(self):
        return self._config._ini.options(self._name)
        
        
    def items(self):
        return self._config._ini.items(self._name)
        


class Config(object):
    def __init__(self, source):
        f = open(source)    
        self._configDict = {}
        self._source = source        
        self._ini = OrderedConfigParser()
        self._config = self._ini.read(source)
        if len(self._config) > 0:
            for section in self._ini.sections():
                self._configDict[section] = {}
                _sec = Section(self, section)
                #setattr(self, section, _sec)
                self.__dict__[section] = _sec
                items = self._ini.items(section)
                for item in items:
                    setattr(getattr(self, section), item[0], item[1])

            
    def save(self):
        for section in self._configDict:            
            for entry, entryValue in self._configDict[section].iteritems():
                self._ini.set(section, entry, entryValue)
        f = file(self._source,'w')
        self._ini.write(f)
        f.close()
        
    
    def add_section(self, section):
        if not self._ini.has_section(section):
            self._ini.add_section(section)
            self._configDict[section] = {}
            _sec = Section(self, section)
            self.__dict__[section] = _sec
            
            
    def remove_section(self, section):
        if self._ini.has_section(section):
            self._ini.remove_section(section)
            del(self._configDict[section])
            del(self.__dict__[section])

        
    def dump(self):
        print self._configDict
        

    def sections(self):
        return self._ini.sections()
                
        
    def parseDate(self, isoDate):
        __regDate = '(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\..*'
        reg = re.compile(__regDate)
        m = reg.match(isoDate)
        if m is not None:
            params = m.groups()
            params = map(lambda x: int(x), params)            
            return datetime(params[0],params[1],params[2],params[3],params[4],params[5])
        else:
            return None



class OrderedConfigParser(ConfigParser):
    """ Adds the feature of load/save sections from the config file in the exact order """

    def __init__(self):
        ConfigParser.__init__(self)

        self._orderedSectionNames = []


    def initOrderedSectionNames(self, filename):
        # ConfigParser does not return an ordered section list: we try to obtain this
        self._orderedSectionNames = []
        try:
            sectionsList = []
            f = open(filename, 'r')
            sectionLines = f.readlines()
            f.close()
            # FIXME: substitute this with regexp !!!
            for l in sectionLines:
                if len(l) > 0:
                    if l[0] == '[':
                       finishIndex = l.find(']')
                       if finishIndex > 0:
                           self._orderedSectionNames.append(l[1:finishIndex])
        except:
            print 'Error retrieving ordered sections list'
            self._orderedSectionNames = []


    def sections(self):
        return self.refreshOrderedSectionNames()


    def refreshOrderedSectionNames(self):
        # It is useful only if some section was added-removed
        # New sections are added to the end
        orderedSections = self._orderedSectionNames
        sections = self._sections.keys()
        for s in orderedSections:
            if s not in sections:
                orderedSections.pop(s)
        for s in sections:
            if s not in orderedSections:
                orderedSections.append(s)
        return orderedSections


    def read(self, filenames):
        # Overloads the base class method and create initial order list of sections names
        value = ConfigParser.read(self, filenames)
        self.initOrderedSectionNames(filenames)
        return value


    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        # Overloads the base class method: the only difference is how sections are inspected
        for section in self.sections():
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
