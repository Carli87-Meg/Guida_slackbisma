#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provini a contatto: mette i fotogrammi di un video in una griglia unica.

Serve per il triage della Fase 4. Guardare 77 fotogrammi uno per uno e' lento;
su un provino si vede subito quali sono mossi, quali hanno la manovra coperta e
quali vale la pena aprire a piena risoluzione.

    python tools/provini.py                 # un provino per ogni video estratto
    python tools/provini.py IMG_1384        # solo questo

Ogni riquadro porta il timestamp, cosi' il provino resta tracciabile alla fonte.
Output in lavorazione/provini/.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SORG = Path('lavorazione/frame_grezzi')
DEST = Path('lavorazione/provini')
LATO = 380          # lato lungo di ogni riquadro nel provino
COL = 4
MARG = 8
BARRA = 22


def _font(px):
    for n in ('arialbd.ttf', 'DejaVuSans-Bold.ttf', 'seguisb.ttf'):
        for d in ('C:/Windows/Fonts/', '/usr/share/fonts/truetype/dejavu/'):
            p = Path(d) / n
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), px)
                except OSError:
                    pass
    return ImageFont.load_default()


def etichetta(nome):
    """IMG_1384_0014_000.jpg -> 0:14"""
    parti = nome.split('_')
    if len(parti) >= 3 and len(parti[2]) == 4 and parti[2].isdigit():
        return '%d:%s' % (int(parti[2][:2]), parti[2][2:])
    return nome


def provino(cartella: Path):
    file = sorted(cartella.glob('*.jpg'))
    if not file:
        return None
    righe = (len(file) + COL - 1) // COL

    # tutti i fotogrammi hanno lo stesso orientamento: dimensiono sul primo
    with Image.open(file[0]) as c:
        w, h = c.size
    if w >= h:
        cw, ch = LATO, round(h * LATO / w)
    else:
        cw, ch = round(w * LATO / h), LATO

    W = COL * cw + (COL + 1) * MARG
    H = righe * (ch + BARRA) + (righe + 1) * MARG
    foglio = Image.new('RGB', (W, H), (24, 26, 30))
    d = ImageDraw.Draw(foglio)
    f = _font(15)

    for i, p in enumerate(file):
        r, c = divmod(i, COL)
        x = MARG + c * (cw + MARG)
        y = MARG + r * (ch + BARRA + MARG)
        with Image.open(p) as im:
            foglio.paste(im.resize((cw, ch), Image.LANCZOS), (x, y))
        d.text((x + 3, y + ch + 3), etichetta(p.name), fill=(235, 232, 226), font=f)

    DEST.mkdir(parents=True, exist_ok=True)
    out = DEST / ('provino_%s.jpg' % cartella.name)
    foglio.save(out, quality=88)
    return out, len(file)


def main():
    solo = sys.argv[1:]
    cartelle = sorted(p for p in SORG.iterdir() if p.is_dir())
    if solo:
        cartelle = [c for c in cartelle if c.name in solo]
    for c in cartelle:
        r = provino(c)
        if r:
            print('%s  (%d frame)' % (r[0], r[1]))


if __name__ == '__main__':
    main()
