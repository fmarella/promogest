# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Authors: Francesco Meloni  <francesco@promotux.it>
#             Andrea Argiolas   <andrea@promotux.it>
#             Francesco Marella <francesco.marella@gmail.com>

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


from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.modules.Agenti.ui.AnagraficaAgentiEdit import AnagraficaAgentiEdit
from promogest.modules.Agenti.ui.AnagraficaAgentiFilter import AnagraficaAgentiFilter
from promogest import Environment
from promogest.modules.Agenti.dao.Agente import Agente, getNuovoCodiceAgente
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaAgenti(Anagrafica):
    """ Anagrafica agenti """

    def __init__(self,aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica agenti',
                            recordMenuLabel='_Agenti',
                            filterElement=AnagraficaAgentiFilter(self),
                            htmlHandler=AnagraficaAgentiHtml(self),
                            reportHandler=AnagraficaAgentiReport(self),
                            editElement=AnagraficaAgentiEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaAgentiHtml(AnagraficaHtml):
    """ Anagrafica Agenti HTML widget di anteprima"""
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica,
                                'agente',
                                "Informazioni sull'agente",
                                )



class AnagraficaAgentiReport(AnagraficaReport):
    """ Anagrafica agenti Report pdf ..."""
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli agenti',
                                  defaultFileName='agenti',
                                  htmlTemplate='agenti',
                                  sxwTemplate='agenti')
