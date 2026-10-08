# -*- coding: utf-8 -*-
"""Fascicolo delle schede di rilievo della Pietra di Bismantova.

Una scheda per ognuna delle linee non ancora documentate, da stampare e portare
in parete. Fino all'edizione di agosto le schede stavano dentro la guida, in
fondo alla Parte 3: nella revisione su Figma l'autore le ha tolte, perche' a chi
legge la guida per ora non servono. Servono a chi va a rilevare, e qui stanno.

La guida le cita per numero di scheda, non per pagina: un numero di pagina di
questo fascicolo, stampato nella guida, si confonderebbe con le pagine della
guida stessa.

Lo costruisce anche build_manuale.py, alla fine: i due documenti escono sempre
in coppia.

    python build/build_schede_rilievo.py
"""
import io
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from schede_linee import parte_rilievi                              # noqa: E402
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame  # noqa: E402

OUT = RADICE / 'output' / 'Pietra_Bismantova_Schede_Rilievo.pdf'
TESTATA = 'PIETRA DI BISMANTOVA · SCHEDE DI RILIEVO'


def impagina(destinazione):
    """Impagina il fascicolo su `destinazione` e restituisce il numero di pagine."""
    # testatina e piede sono quelli della guida: importati qui e non in testa,
    # perche' build_manuale importa questo modulo per costruire la coppia
    from build_manuale import page_begin, page_end
    doc = BaseDocTemplate(destinazione, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title='Schede di rilievo — Pietra di Bismantova',
                          author='Bismaliners')
    doc.testata = TESTATA
    frame = Frame(LM, BM, FW, H - TM - BM, id='n',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=page_begin,
                                       onPageEnd=page_end)])
    doc.build(lega_testate(parte_rilievi()))
    return doc.page


def main():
    """Due passate bastano: l'unico rimando e' l'indice delle schede."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for passata in range(1, 4):
        prima = dict(PAGINE)
        impagina(io.BytesIO())
        if PAGINE == prima and passata > 1:
            break
    n = impagina(str(OUT))
    print('scritto %s (%d pagine)' % (OUT, n))
    return n


if __name__ == '__main__':
    main()
