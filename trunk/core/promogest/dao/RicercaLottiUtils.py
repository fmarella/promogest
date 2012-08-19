from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento


def ricerca_lotto(numero_lotto):
    lista_fornitori = []
    forniture = Fornitura().select(numeroLotto=numero_lotto, batchSize=None)
    for fornitura in forniture:

        righe_mf = RigaMovimentoFornitura().select(idFornitura=fornitura.id)
        righe_mov = [riga_mf.rigamovven or riga_mf.rigamovacq for riga_mf in righe_mf]

        docs = []
        for riga_mov in righe_mov:
            if not riga_mov:
                continue
            tm = TestataMovimento().getRecord(id=riga_mov.id_testata_movimento)
            if tm:
                td = TestataDocumento().getRecord(id=tm.id_testata_documento)
                if td:
                    docs.append(td)

            docs.extend(ricerca_in_lottotemp(numero_lotto))
            
            lista_fornitori.append({'data_fornitura': fornitura.data_fornitura,
                'fornitore': fornitura.forni, 'docs': docs})
    return lista_fornitori

def ricerca_in_lottotemp(numero_lotto):
    nltemps = NumeroLottoTemp().select(lottoTemp=numero_lotto)

    docs = []
    for nltemp in nltemps:
        tm = TestataMovimento().getRecord(id=nltemp.rigamovventemp.id_testata_movimento)
        if tm:
            td = TestataDocumento().getRecord(id=tm.id_testata_documento)
            if td:
                docs.append(td)
    return docs