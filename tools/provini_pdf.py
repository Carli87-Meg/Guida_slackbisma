#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provini a contatto delle pagine del PDF: tutte le pagine su pochi fogli.

Serve a rivedere l'impaginazione. Aprire un PDF di cinquanta pagine e scorrerlo
per capire quali respirano male e' lento, e soprattutto non si confrontano fra
loro due pagine lontane. Su un provino si vede tutto insieme, e si indica una
pagina per numero: «la 14 e la 19».

    python tools/provini_pdf.py                     # il manuale
    python tools/provini_pdf.py output/altro.pdf    # un altro file
    python tools/provini_pdf.py --colonne 8         # griglia piu' fitta

Sotto ogni pagina c'e' il numero e la percentuale di altezza occupata, misurata
fra testatina e piede. Non e' un voto: una pagina di apertura di parte sta al
40% ed e' giusta cosi'. Serve a trovare in fretta le pagine che si sono svuotate
senza volerlo, che sono l'errore che si vede meno sfogliando.

Output in lavorazione/provini_pdf/.
"""
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

RADICE = Path(__file__).resolve().parent.parent
PREDEFINITO = RADICE / 'output' / 'Pietra_Bismantova_Highline.pdf'
DEST = RADICE / 'lavorazione' / 'provini_pdf'

COLONNE = 6
RIGHE = 5
LARGH = 250             # larghezza di ogni miniatura
MARG = 14
BARRA = 30              # striscia sotto la miniatura, per numero e riempimento

# banda di contenuto di una pagina A4 del manuale, esclusi testatina e piede:
# gli stessi valori con cui e' misurato il riempimento altrove
ALTO, BASSO = 88, 790

SFONDO = (250, 249, 246)
INCHIOSTRO = (20, 24, 28)
SMORTO = (123, 130, 136)
ALLARME = (179, 38, 30)
BORDO = (223, 220, 214)


def _font(px, grassetto=True):
    nomi = (('arialbd.ttf', 'DejaVuSans-Bold.ttf', 'seguisb.ttf') if grassetto
            else ('arial.ttf', 'DejaVuSans.ttf', 'segoeui.ttf'))
    for n in nomi:
        for d in ('C:/Windows/Fonts/', '/usr/share/fonts/truetype/dejavu/',
                  '/Library/Fonts/'):
            p = Path(d) / n
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), px)
                except Exception:
                    pass
    return ImageFont.load_default()


def riempimento(pagina):
    """Quanto in basso arriva il contenuto, in percentuale della banda utile.

    Conta testo, immagini e riquadri disegnati, ma non testatina e piede, che
    stanno su tutte le pagine e direbbero sempre cento.
    """
    giu = ALTO
    for b in pagina.get_text('blocks'):
        if b[4].strip() and b[1] >= ALTO and b[3] <= BASSO + 8:
            giu = max(giu, b[3])
    for im in pagina.get_images():
        try:
            for r in pagina.get_image_rects(im[0]):
                if r.y1 <= BASSO + 8:
                    giu = max(giu, r.y1)
        except Exception:
            pass
    for dis in pagina.get_drawings():
        r = dis['rect']
        if r.y1 <= BASSO and r.y0 >= ALTO and r.height > 1.5:
            giu = max(giu, r.y1)
    return (giu - ALTO) / (BASSO - ALTO) * 100


def miniature(pdf):
    """Una miniatura per pagina, con il numero e il riempimento."""
    doc = fitz.open(pdf)
    fuori = []
    for i, pagina in enumerate(doc):
        scala = LARGH / pagina.rect.width
        pix = pagina.get_pixmap(matrix=fitz.Matrix(scala, scala))
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        fuori.append((i + 1, im, riempimento(pagina)))
    return fuori


def provino(pezzi, colonne, righe, titolo):
    """Un foglio di provini."""
    ah = max(im.height for _, im, _ in pezzi)
    cella_w = LARGH + MARG
    cella_h = ah + BARRA + MARG
    testa = 44
    W = MARG + colonne * cella_w
    H = testa + righe * cella_h + MARG
    foglio = Image.new('RGB', (W, H), SFONDO)
    d = ImageDraw.Draw(foglio)
    d.text((MARG, 14), titolo, font=_font(19), fill=INCHIOSTRO)

    for k, (n, im, pct) in enumerate(pezzi):
        c, r = k % colonne, k // colonne
        x = MARG + c * cella_w
        y = testa + r * cella_h
        foglio.paste(im, (x, y))
        d.rectangle([x, y, x + im.width - 1, y + im.height - 1], outline=BORDO)
        # numero di pagina grande: e' con quello che la pagina viene indicata
        d.text((x + 2, y + im.height + 5), str(n), font=_font(17),
               fill=INCHIOSTRO)
        etichetta = '%.0f%%' % pct
        colore = ALLARME if pct < 60 else SMORTO
        d.text((x + im.width - 2, y + im.height + 7), etichetta,
               font=_font(13, False), fill=colore, anchor='ra')
    return foglio


def main():
    argomenti = [a for a in sys.argv[1:] if not a.startswith('--')]
    colonne = COLONNE
    if '--colonne' in sys.argv:
        colonne = int(sys.argv[sys.argv.index('--colonne') + 1])
    pdf = Path(argomenti[0]) if argomenti else PREDEFINITO
    if not pdf.exists():
        print('non trovo %s' % pdf)
        print('prima costruiscilo:  python build/build_manuale.py')
        raise SystemExit(1)

    DEST.mkdir(parents=True, exist_ok=True)
    pezzi = miniature(pdf)
    per_foglio = colonne * RIGHE
    fogli = [pezzi[i:i + per_foglio] for i in range(0, len(pezzi), per_foglio)]
    scritti = []
    for i, gruppo in enumerate(fogli, 1):
        titolo = ('%s  ·  pagine %d-%d di %d'
                  % (pdf.name, gruppo[0][0], gruppo[-1][0], len(pezzi)))
        righe = (len(gruppo) + colonne - 1) // colonne
        f = DEST / ('provino_%02d.jpg' % i)
        provino(gruppo, colonne, righe, titolo).save(
            f, 'JPEG', quality=88, optimize=True)
        scritti.append(f)
        print('scritto %s  (pagine %d-%d)' % (f, gruppo[0][0], gruppo[-1][0]))

    magre = [n for n, _, p in pezzi if p < 60]
    print()
    print('%d pagine, %d fogli' % (len(pezzi), len(scritti)))
    if magre:
        print('sotto il 60%% di riempimento: %s'
              % ', '.join(str(n) for n in magre))


if __name__ == '__main__':
    main()
