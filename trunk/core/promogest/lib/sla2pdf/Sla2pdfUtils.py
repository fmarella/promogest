# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Simone Cossu <simone@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>


import datetime
from decimal import *
from reportlab.platypus import  Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import cm

try:
    from reportlab.graphics.barcode.common import *
    from reportlab.graphics.barcode.usps import *
    from reportlab.graphics.barcode import createBarcodeDrawing
except:
    pass

def getPdfFontName(font=None):
    """ Trying to resolve font name """
    boldStr = 'BOLD'
    italicStr = 'ITALIC'
    obliqueStr = 'OBLIQUE'
    fontStr = font.upper()
    if 'COURIER' in fontStr:
        if boldStr in fontStr and obliqueStr in fontStr:
            fontName = 'Courier-BoldOblique'
        elif boldStr in fontStr:
            fontName = 'Courier-Bold'
        elif obliqueStr in fontStr:
            fontName = 'Courier-Oblique'
        else:
            fontName = 'Courier'
    elif 'HELVETICA' in fontStr:
        if boldStr in fontStr and obliqueStr in fontStr:
            fontName = 'Helvetica-BoldOblique'
        elif boldStr in fontStr:
            fontName = 'Helvetica-Bold'
        elif obliqueStr in fontStr:
            fontName = 'Helvetica-Oblique'
        else:
            fontName = 'Helvetica'
    else:
        if boldStr in fontStr and (obliqueStr in fontStr or italicStr in fontStr):
            fontName = 'Times-BoldItalic'
        elif boldStr in fontStr:
            fontName = 'Times-Bold'
        elif obliqueStr in fontStr or italicStr in fontStr:
            fontName = 'Times-Italic'
        else:
            fontName = 'Times-Roman'

    return fontName

def alignment(slaAlignment,styleAlignment=None):
    if slaAlignment:
        if slaAlignment == '0':
            pdfAlignment = 'LEFT'
        elif slaAlignment == '1':
            pdfAlignment = 'CENTER'
        elif slaAlignment == '2':
            pdfAlignment = 'RIGHT'
    else:
        #try:
            ##print "ATTENTION!!! NO ALIGNMENT FOUND I SWITCH TO A DEFAULT VALUE"
            #slaAlignment = styleAlignment.get('ALIGN')
            #pdfAlignment
        #except:
        print "ATTENTION!!! ARBITRARY ALIGNMENT USED '0'"
        #pdfAlignment = 'LEFT'
    return pdfAlignment


def italianizza(value, decimal=0, curr='', sep='.', dp=',',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
#    qq = Decimal(10) ** -places      # 2 places --> '0.01'
#    precisione = int(setconf(key="decimals", section="Numbers")) or int(decimal)
    precisione = int(decimal)
    sign, digits, exp = Decimal(value).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(precisione):
        build(next() if digits else '0')
    if not precisione:
        build("0")
        build("0")
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def createbarcode(ch):
        data = ch.split(';')
        #print "DATA for Barcode", ch,data[1]
        #print "CODICE A BARRE " , data[1]
        if len(data[1]) ==13:
            bcd = createBarcodeDrawing('EAN13', value=data[1], width=float(data[2])*cm,height=float(data[3])*cm)
        elif len(data[1]) == 8:
            bcd = createBarcodeDrawing('EAN8', value=data[1], width=float(data[2])*cm,height=float(data[3])*cm)
        else:
            bcd = createBarcodeDrawing('EAN13', value=data[1], width=float(data[2])*cm,height=float(data[3])*cm)
        #bcd = createBarcodeDrawing('EAN13', value="8002705005009", width=float(data[2])*cm,height=float(data[3])*cm)
        return bcd



def makeParagraphs(text, background, foreground, pdfAlignment, fontName, fontSize):
        """Convert plain text into a list of paragraphs."""
        if (text == '') or ('\\n' not in text):
            return text

        if pdfAlignment == 'CENTER':
            alignment = TA_CENTER
        elif pdfAlignment == 'RIGHT':
            alignment = TA_RIGHT
        else:
            alignment = TA_LEFT
        style = ParagraphStyle(name='Normal',
                               fontName=fontName,
                               fontSize=fontSize,
                               alignment=alignment,
                               backColor=background,
                               textColor=foreground)
        lines = text.split("\\n")
        retval = [Paragraph(line[:6]=='<para>' and line or ('<para>%s</para>' % line), style) for line in lines]
        return retval

def bcviewValue(value,parameter):
    width = parameter[0]
    height = parameter[1]
    bc = "bcview" + ";" + str(value) + ";" + width + ";" + height
    return str(bc)

def truncValue(value, length):
    """
    Trunc the length of the element
    """
    return str(value[0:length])


def approxValue(value, decimals):
    """
    Approximate the floating point values of the element with the
    given number of decimals
    """
    format = '%%.%df' % decimals
    #print value
    value = float(value)
    return ((value != '' and value is not None) and (format % (value or 0.0)) or '')

def approxValueIt(value, decimals):
    """
    Approximate the floating point values of the element with the
    given number of decimals
    """
    format = '%%.%df' % decimals
    #print value
    value = float(value)
    if value !="" and value is not None:
        return italianizza((format % (value)),decimal=decimals)
    else:
        return "0"

def itformatValue(value,tronca=False):
    """
    Convert the dates of the element into strings with italian
    datetime format
    """
    if isinstance(value, datetime.datetime):
        if tronca:
            return value.strftime('%d/%m/%Y')
        else:
            return value.strftime('%d/%m/%Y, ore %H:%M')
    elif isinstance(value, datetime.date):
        return value.strftime('%d/%m/%Y')
    elif isinstance(value, datetime.time):
        return value.strftime('%H:%M')


def getNowValue(tag):
    """ Returns formatted now value """
    if tag == 'date':
        return datetime.datetime.now().strftime('%d/%m/%Y')
    elif tag == 'time':
        return datetime.datetime.now().strftime('%H:%M')
    else:
        return datetime.datetime.now().strftime('%d/%m/%Y  %H:%M')

#def createbarcode(self, ch):
    #data = ch.split(';')
    #print "DATA for Barcode", ch
    #bcd = createBarcodeDrawing('EAN13', value=data[1], width=float(data[2])*cm,height=float(data[3])*cm)
    ##bcd = createBarcodeDrawing('EAN13', value="8002705005009", width=float(data[2])*cm,height=float(data[3])*cm)
    #return bcd

def cancelOperation():
    """
    Cancel current operation (i.e. make the computation stop as
    soon as possible, e.g. when executed in a parallel thread)
    """
    pass

def findTags(string):
    """ Isolating tags and functions applied to tags"""
    # RULES:
    # Tags must be divided by spaces
    # No spaces inside a tag
    # Parenthesis [] and () must be balanced
    #
    # EXAMPLES:
    # [[prova1(n)]]    [[itformat(prova2(n))]]    [[trunc(prova3,3)]]
    # [[last:approx(righe(n).prova4,4)]]    [[last:prova5]]    [[last:righe(n).prova6]]

    squareOpen = string.count('[')
    squaresOpen = string.count('[[')
    squareClose = string.count(']')
    squaresClose = string.count(']]')
    roundOpen = string.count('(')
    roundClose = string.count(')')
    chDict = {}

    # Syntax control
    if not ((squaresOpen == squareOpen/2) and (squareOpen%2 == 0) and
            (squaresClose == squareClose/2) and (squareClose%2 == 0) and
            (squaresOpen == squaresClose) and (roundOpen == roundClose)):
        print 'ERROR: Please check your tags!!'
        #print string
        return None

    # Better choice to work with RE
    # wordList = re.findall(r'\b[\S]+\b',string)
    elements = string.split()
    # Finding Tags
    for element in elements:
        if not((element[:2] == '[[') and (element[-2:] == ']]')):
            continue

        position = ''
        function = ''
        tag = ''
        parameter = ''
        arrayName = ''

        # Finding position
        indexPosition = element.find(':')
        if indexPosition != -1:
            position = element[2:indexPosition]

        # Analyzing tag
        if element.count('(') != element.count(')'):
            continue

        indexBeginFunction = element.find('(')
        indexEndFunction = element.rfind(')')
        isIterator = element.find('(n)')
        if (((isIterator == -1) or ((isIterator != -1) and (isIterator != indexBeginFunction))) and
            (indexBeginFunction != -1) and (indexEndFunction != -1)):
                # Finding function
            if indexPosition != -1:
                function = element[indexPosition+1:indexBeginFunction]
            else:
                function = element[2:indexBeginFunction]

            # Finding tag and parameter
            indexParameter = element.find(',')
            if indexParameter != -1:
                parameter = element[indexParameter+1:indexEndFunction]
                tag = element[indexBeginFunction+1:indexParameter]
            else:
                tag = element[indexBeginFunction+1:indexEndFunction]

        # Finding tag
        else:
            if indexPosition != -1:
                tag = element[indexPosition+1:-2]
            else:
                tag = element[2:-2]
        if "(n)" in tag:
            arrayName = tag.split("(n)")[0]
        #qui compone il tag con i vai elementi
        chDict[tag] = {'position': position,
                        'function': function,
                        'parameter': parameter,
                        "arrayName": arrayName,
                        'completeTag': element}

    if chDict != {}:
        return chDict
    else:
        return None

def sumRowsFunc(heights, rows):
    sumRows = 0
    for u in heights[:rows]:
        sumRows += u
    return sumRows

def sumColumnsFunc(widths, columns):
    sumColumns = 0
    for i in widths[:columns]:
        sumColumns += i
    return sumColumns


def pageProFunc(document):
    pageProperties = []
    numPages = document.findall('PAGE')
    for n in numPages:
        size = n.get('Size')
        num  = int(n.get('NUM')) + 1
        borderTop = float(n.get('BORDERTOP'))
        borderBottom = float(n.get('BORDERBOTTOM'))
        borderRight = float(n.get('BORDERRIGHT'))
        borderLeft = float(n.get('BORDERLEFT'))
        orientation = int(n.get('Orientation'))
        pageHeight = float(n.get('PAGEHEIGHT'))
        pageWidth = float(n.get('PAGEWIDTH'))
        pageXPos = float(n.get('PAGEXPOS'))
        pageYPos = float(n.get('PAGEYPOS'))
        pageProperties.append([size, num,
                                    borderTop, borderBottom, borderRight, borderLeft,
                                    orientation, pageHeight, pageWidth, pageXPos, pageYPos])
        #print "PROPRIETA' DELLA PAGINA", pageProperties
        #self.canvas = Canvas(filename = self.pdfFolder + self.pdfFileName + '.pdf', pagesize=(pageWidth, pageHeight))

    return pageProperties

def cancelOperation():
    """
    Cancel current operation (i.e. make the computation stop as
    soon as possible, e.g. when executed in a parallel thread)
    """
    pass
