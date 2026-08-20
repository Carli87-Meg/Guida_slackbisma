#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reperimento e registrazione dei font per il PDF.

`design/design.py` registra Lora e Poppins da un percorso Linux
(`/usr/share/fonts/truetype/google-fonts/`) che su Windows non esiste. Questo
modulo li cerca in ordine:

    1. build/fonts/            (scaricati una volta e tenuti nel progetto)
    2. i percorsi di sistema   (Linux, macOS, Windows)
    3. scarico da Google Fonts (repository ufficiale, licenza SIL OFL)
    4. sostituti di sistema    (Georgia / Constantia per il testo,
                                Century Gothic / Calibri per i titoli)

Il punto 4 e' un ripiego dichiarato: cambia l'aspetto rispetto al progetto
Sillschlucht, e lo script lo dice invece di farlo di nascosto.

    python build/font.py          # verifica cosa userebbe, senza costruire il PDF

Nota sulle facce grassetto: i file Lora scaricati da Google Fonts sono font
*variabili* (asse wght 400-700), e ReportLab ne usa solo l'istanza di default.
`Lora-Bold.ttf` e `Lora-BoldItalic.ttf` sono percio' istanze statiche a wght=700
estratte una volta e tenute in build/fonts/. Per rigenerarle:

    python -c "from fontTools.ttLib import TTFont; \
    from fontTools.varLib.instancer import instantiateVariableFont as inst; \
    f=TTFont('build/fonts/Lora-Regular.ttf'); \
    inst(f,{'wght':700},inplace=True,updateFontNames=True); \
    f.save('build/fonts/Lora-Bold.ttf')"

Senza quei file il grassetto del testo in Lora e' silenziosamente piatto.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
LOCALI = RADICE / 'build' / 'fonts'

BASE = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'

# nome interno -> (file, url relativo su Google Fonts, sostituti di sistema)
FONT = {
    'Lora':   ('Lora-Regular.ttf',      'lora/Lora%5Bwght%5D.ttf',
               ['constan.ttf', 'georgia.ttf', 'DejaVuSerif.ttf']),
    'Lora-I': ('Lora-Italic.ttf',       'lora/Lora-Italic%5Bwght%5D.ttf',
               ['constani.ttf', 'georgiai.ttf', 'DejaVuSerif-Italic.ttf']),
    'Lora-B': ('Lora-Bold.ttf',         'lora/Lora%5Bwght%5D.ttf',
               ['constanb.ttf', 'georgiab.ttf', 'DejaVuSerif-Bold.ttf']),
    'Lora-BI': ('Lora-BoldItalic.ttf',  'lora/Lora-Italic%5Bwght%5D.ttf',
                ['constanz.ttf', 'georgiaz.ttf', 'DejaVuSerif-BoldItalic.ttf']),
    'Pop':    ('Poppins-Regular.ttf',   'poppins/Poppins-Regular.ttf',
               ['GOTHIC.TTF', 'calibri.ttf', 'DejaVuSans.ttf']),
    'Pop-L':  ('Poppins-Light.ttf',     'poppins/Poppins-Light.ttf',
               ['calibril.ttf', 'GOTHIC.TTF', 'DejaVuSans.ttf']),
    'Pop-M':  ('Poppins-Medium.ttf',    'poppins/Poppins-Medium.ttf',
               ['GOTHIC.TTF', 'calibri.ttf', 'DejaVuSans.ttf']),
    'Pop-B':  ('Poppins-Bold.ttf',      'poppins/Poppins-Bold.ttf',
               ['GOTHICB.TTF', 'calibrib.ttf', 'DejaVuSans-Bold.ttf']),
}

DIR_SISTEMA = [
    Path('/usr/share/fonts/truetype/google-fonts/'),
    Path('/usr/share/fonts/truetype/dejavu/'),
    Path('/Library/Fonts/'),
    Path('C:/Windows/Fonts/'),
]


def _in_sistema(nome):
    for d in DIR_SISTEMA:
        p = d / nome
        if p.exists():
            return p
    return None


def _scarica(rel, dest):
    url = BASE + rel
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            dati = r.read()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, str(e)
    if len(dati) < 20000:                      # una ttf vera pesa molto di piu'
        return None, 'risposta troppo corta (%d byte)' % len(dati)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(dati)
    return dest, None


def risolvi(scarica=True):
    """Restituisce {nome_interno: (percorso, provenienza)}."""
    esito = {}
    for nome, (file, rel, ripieghi) in FONT.items():
        loc = LOCALI / file
        if loc.exists():
            esito[nome] = (loc, 'locale')
            continue
        sis = _in_sistema(file)
        if sis:
            esito[nome] = (sis, 'sistema')
            continue
        if scarica:
            p, err = _scarica(rel, loc)
            if p:
                esito[nome] = (p, 'scaricato')
                continue
        for r in ripieghi:
            sis = _in_sistema(r)
            if sis:
                esito[nome] = (sis, 'SOSTITUTO (%s)' % r)
                break
        else:
            esito[nome] = (None, 'MANCANTE')
    return esito


def registra(esito=None):
    """Registra i font in ReportLab. Da chiamare prima di importare design."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    esito = esito or risolvi()
    mancanti = [n for n, (p, _) in esito.items() if p is None]
    if mancanti:
        raise SystemExit('Font non risolvibili: %s' % ', '.join(mancanti))
    for nome, (p, _) in esito.items():
        pdfmetrics.registerFont(TTFont(nome, str(p)))
    pdfmetrics.registerFontFamily('Lora', normal='Lora', bold='Lora-B',
                                  italic='Lora-I', boldItalic='Lora-BI')
    return esito


def sostituiti(esito):
    return [n for n, (_, prov) in esito.items() if prov.startswith('SOSTITUTO')]


if __name__ == '__main__':
    e = risolvi()
    print('%-8s %-12s %s' % ('NOME', 'PROVENIENZA', 'FILE'))
    print('-' * 74)
    for n, (p, prov) in e.items():
        print('%-8s %-12s %s' % (n, prov.split(' ')[0], p.name if p else '—'))
    s = sostituiti(e)
    if s:
        print('\n⚠  Font sostituiti: %s' % ', '.join(s))
        print('   Il PDF non avra\' esattamente l\'aspetto del progetto Sillschlucht.')
    elif all(prov != 'MANCANTE' for _, prov in e.values()):
        print('\nTutti i font originali disponibili.')
    sys.exit(0)
