# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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



from sqlalchemy.interfaces import ConnectionProxy


class MyProxy(ConnectionProxy):

    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        from promogest.lib.utils import messageInfo
        try:
            return execute(cursor, statement, parameters, context)
        except OperationalError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+ str(e) )
        except IntegrityError as e:
            messageInfo(msg="IntegrityError UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+ str(e))
            session.rollback()
        except ProgrammingError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+str(e))
            session.rollback()
            delete_pickle()
        except InvalidRequestError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO: "+str(e))
            session.rollback()
        except AssertionError as e:
            messageInfo(msg="UN ERRORE È STATO INTERCETTATO E SEGNALATO\n Possibile tentativo di cancellazione di un dato\n collegato ad altri dati fondamentali: "+str(e))
            session.rollback()
        except ValueError as e:
            messageInfo(msg="Risulta inserito un Valore non corretto. Ricontrolla: "+str(e))
            session.rollback()
