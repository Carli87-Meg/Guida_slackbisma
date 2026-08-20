# -*- coding: utf-8 -*-
"""Componenti da compilare a mano: righe vuote ed etichette di campo.

Estratti da build/build_scheda_dubbi.py, dove erano nati, perche' servono anche
alle schede di rilievo delle linee non ancora documentate. Due copie dello stesso
componente sarebbero divergute alla prima modifica.

    from campi import Righe, campo, griglia_campi
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import Flowable, Table, TableStyle, Paragraph  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402

_SENZA_BORDI = [('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]


class Righe(Flowable):
    """Righe vuote su cui scrivere a penna."""

    def __init__(self, n=2, w=FW, passo=21):
        self.n, self.w, self.passo = n, w, passo
        self.h = n * passo

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.6)
        for i in range(self.n):
            y = self.h - (i + 1) * self.passo + 5
            c.line(0, y, self.w, y)


def campo(label, w, righe=1, passo=21):
    """Etichetta piccola sopra una o piu' righe su cui scrivere."""
    st = ParagraphStyle('cl', fontName='Pop-M', fontSize=7.2, leading=10,
                        textColor=MUT)
    t = Table([[Paragraph(label.upper(), st)], [Righe(righe, w=w, passo=passo)]],
              colWidths=[w])
    t.setStyle(TableStyle(_SENZA_BORDI))
    return t


# altezza dell'etichetta di un campo e aria sotto l'ultima riga: servono a
# calcolare il passo, non sono numeri decorativi
_H_ETICHETTA = 10.0
_PAD_CAMPO = 12.0
PASSO_MIN, PASSO_MAX = 22.0, 42.0


def passo_per_altezza(etichette, altezza, cols=2):
    """Passo delle righe che riempie `altezza` con i campi dati.

    Una scheda da compilare in parete che occupa meta' pagina spreca carta due
    volte: lascia il foglio vuoto e lascia righe corte su cui non ci sta la
    descrizione di un ancoraggio. Il passo viene calcolato perche' la griglia
    arrivi a fondo pagina, entro limiti leggibili.
    """
    n_righe = 0
    for i in range(0, len(etichette), cols):
        blocco = etichette[i:i + cols]
        n_righe += max((e[1] if isinstance(e, (tuple, list)) else 1) for e in blocco)
    n_blocchi = (len(etichette) + cols - 1) // cols
    fisso = n_blocchi * (_H_ETICHETTA + _PAD_CAMPO)
    if n_righe <= 0:
        return PASSO_MIN
    return max(PASSO_MIN, min(PASSO_MAX, (altezza - fisso) / n_righe))


def griglia_campi(etichette, w=FW, cols=2, gap=14, passo=None, altezza=None):
    """Campi da compilare disposti su piu' colonne.

    `etichette` e' una sequenza di stringhe, oppure di coppie (etichetta, righe)
    per i campi che hanno bisogno di piu' spazio. Con `altezza` la griglia
    calcola da se' il passo per riempire quello spazio.
    """
    if passo is None:
        passo = (passo_per_altezza(etichette, altezza, cols) if altezza
                 else 21)
    cw = (w - gap * (cols - 1)) / cols
    celle = []
    for e in etichette:
        lab, righe = e if isinstance(e, (tuple, list)) else (e, 1)
        celle.append(campo(lab, cw, righe, passo))

    righe_tab = [celle[i:i + cols] for i in range(0, len(celle), cols)]
    if righe_tab and len(righe_tab[-1]) < cols:            # pareggia l'ultima riga
        righe_tab[-1] += [''] * (cols - len(righe_tab[-1]))

    t = Table(righe_tab, colWidths=[cw + gap] * (cols - 1) + [cw])
    t.setStyle(TableStyle(_SENZA_BORDI + [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-2, -1), gap)]))
    return t
