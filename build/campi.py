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


def campo(label, w, righe=1):
    """Etichetta piccola sopra una o piu' righe su cui scrivere."""
    st = ParagraphStyle('cl', fontName='Pop-M', fontSize=7.2, leading=10,
                        textColor=MUT)
    t = Table([[Paragraph(label.upper(), st)], [Righe(righe, w=w)]], colWidths=[w])
    t.setStyle(TableStyle(_SENZA_BORDI))
    return t


def griglia_campi(etichette, w=FW, cols=2, gap=14):
    """Campi da compilare disposti su piu' colonne.

    `etichette` e' una sequenza di stringhe, oppure di coppie (etichetta, righe)
    per i campi che hanno bisogno di piu' spazio.
    """
    cw = (w - gap * (cols - 1)) / cols
    celle = []
    for e in etichette:
        lab, righe = e if isinstance(e, (tuple, list)) else (e, 1)
        celle.append(campo(lab, cw, righe))

    righe_tab = [celle[i:i + cols] for i in range(0, len(celle), cols)]
    if righe_tab and len(righe_tab[-1]) < cols:            # pareggia l'ultima riga
        righe_tab[-1] += [''] * (cols - len(righe_tab[-1]))

    t = Table(righe_tab, colWidths=[cw + gap] * (cols - 1) + [cw])
    t.setStyle(TableStyle(_SENZA_BORDI + [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-2, -1), gap)]))
    return t
