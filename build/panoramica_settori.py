#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etichette dei settori su una vista d'insieme della Pietra.

I cinque render di `fonti/render_ipietra/` inquadrano un settore per volta. Una
vista d'insieme con i cinque nomi al posto giusto e' un'altra cosa: serve a
capire come sono disposti attorno al massiccio, prima ancora di guardare le
singole linee.

QUESTO SCRIPT NON INDOVINA DOVE STANNO I SETTORI.

Le posizioni vanno dichiarate in POSIZIONI, e devono venire da una fonte:

* le etichette leggibili sulla panoramica esportata da i-pietra, oppure
* l'indicazione di chi conosce lo spot.

Dedurle dalla somiglianza della roccia fra un render e l'altro non e' una fonte.
Una panoramica con un settore scambiato manda a montare dal lato sbagliato, ed
e' il tipo di errore che CLAUDE.md chiede di non correre: finche' una posizione
non e' dichiarata, lo script lo dice e non la disegna.

    python build/panoramica_settori.py
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))
sys.path.insert(0, str(RADICE / 'tools'))

from PIL import Image, ImageDraw                                # noqa: E402

from annota import COLORI, _font                                # noqa: E402
import linee as REG                                             # noqa: E402

SORG = RADICE / 'fonti' / 'render_ipietra'
DEST = RADICE / 'lavorazione' / 'panoramiche'
_ESTENSIONI = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

# colore di ogni settore, gli stessi del manuale (schede_linee.C_AREA)
COLORE_AREA = {
    'Rookie':         (31, 190, 136),
    'Settore Giallo': (163, 167, 54),
    'Anfiteatro':     (226, 98, 46),
    'Anfite-altro':   (224, 58, 47),
    'Despedida':      (47, 159, 222),
}

# ---------------------------------------------------------------------------
# Dove cade ogni settore sulla panoramica, in coordinate relative 0..1:
#
#     'Nome settore': ((x_punta, y_punta), (x_etichetta, y_etichetta))
#
# `punta` e' il punto sulla parete a cui la linea di richiamo arriva;
# `etichetta` e' dove sta la pastiglia col nome.
#
# FONTE: panoramica etichettata a mano dall'utente il 21/08/2026, conservata in
# fonti/render_ipietra/riferimento_settori_utente.jpg. Non sono ricavate dai
# render per settore — quelli si sovrappongono a coppie e non collegano i due
# gruppi fra loro.
#
# Le punte sono state RIPORTATE sulla panoramica pulita, che ha un inquadramento
# diverso, registrando le due viste con SIFT + RANSAC: 184 corrispondenze
# valide, errore di riproiezione mediano 1,31 px e 2,64 px al novantacinquesimo
# percentile. E' piu' preciso di quanto le punte siano state lette a occhio, ma
# resta una misura su immagine: se la panoramica viene riesportata da un altro
# punto di vista, le posizioni vanno rifatte.
#
# Cio' che dichiarano, e che prima non si sapeva, e' l'ordine dei settori lungo
# la cresta, da sinistra a destra nella vista da sud-ovest:
#
#     Rookie - Anfiteatro - Anfite-altro - Settore Giallo - Despedida
#
# L'ordine e' il dato solido, ed e' quello con cui il manuale presenta le aree
# (dati/linee.py, AREE). Le coordinate puntano un tratto di parete, non un
# ancoraggio: servono a orientare, non a localizzare. La `y` e' prospettiva,
# non quota: non va usata per dislivelli.
# ---------------------------------------------------------------------------
POSIZIONI = {
    'Rookie':         ((0.208, 0.404), (0.208, 0.262)),
    'Anfiteatro':     ((0.563, 0.374), (0.563, 0.240)),
    'Anfite-altro':   ((0.669, 0.319), (0.669, 0.177)),
    'Settore Giallo': ((0.777, 0.210), (0.777, 0.118)),
    'Despedida':      ((0.811, 0.229), (0.811, 0.066)),
}


def panoramica():
    """Il file della vista d'insieme, comunque sia stato chiamato."""
    if not SORG.is_dir():
        return None
    for f in sorted(SORG.iterdir()):
        if f.suffix in _ESTENSIONI and any(
                p in f.stem.lower() for p in ('panoramica', 'insieme', 'generale')):
            return f
    return None


def _misura(d, testo, px):
    """Ingombro della pastiglia attorno al suo centro: (larghezza, altezza)."""
    l, t, r, b = d.textbbox((0, 0), testo, font=_font(px))
    imb = px * 0.55
    return (r - l) + imb * 2, (b - t) + imb * 1.44


def _pastiglia(d, xy, testo, colore, px):
    """Nome del settore su fondo colorato, come le etichette di i-pietra."""
    f = _font(px)
    x, y = xy
    l, t, r, b = d.textbbox((0, 0), testo, font=f)
    w, h = r - l, b - t
    imb = px * 0.55
    box = [x - w / 2 - imb, y - h / 2 - imb * 0.72,
           x + w / 2 + imb, y + h / 2 + imb * 0.72]
    d.rounded_rectangle(box, radius=px * 0.42, fill=colore + (238,))
    d.text((x - w / 2 - l, y - h / 2 - t), testo, font=f, fill=COLORI['bianco'])
    return box


def _scosta(etichette, aria, limite):
    """Allontana le pastiglie che si accavallano, senza toccare le punte.

    Le posizioni sono lette a occhio su una panoramica, e due settori vicini
    sulla cresta hanno etichette vicine: Anfite-altro e Settore Giallo si
    sovrapponevano di cinque pixel. Qui la pastiglia che sta piu' in basso viene
    spinta verso la sua punta finche' non e' libera, cosi' il disegno regge
    anche se cambia il numero di linee o la panoramica.

    `etichette` e' una lista di dizionari con centro, ingombro e punta.
    """
    for _ in range(40):
        fermo = True
        ordinate = sorted(etichette, key=lambda e: e['cy'])
        for i, a in enumerate(ordinate):
            for b in ordinate[i + 1:]:
                sx = min(a['cx'] + a['w'] / 2, b['cx'] + b['w'] / 2)                     - max(a['cx'] - a['w'] / 2, b['cx'] - b['w'] / 2)
                sy = min(a['cy'] + a['h'] / 2, b['cy'] + b['h'] / 2)                     - max(a['cy'] - a['h'] / 2, b['cy'] - b['h'] / 2)
                if sx <= 0 or sy <= -aria:
                    continue
                # b sta piu' in basso: scende verso la sua punta
                giu = min(sy + aria, max(0.0, b['py'] - limite - b['cy']))
                if giu <= 0.5:
                    continue
                b['cy'] += giu
                fermo = False
        if fermo:
            break
    return etichette


def disegna(sorgente, posizioni, out):
    im = Image.open(sorgente).convert('RGB')
    velo = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(velo)
    px = max(15, int(im.size[0] / 52))

    etichette = []
    for area, ((px_, py_), (lx, ly)) in posizioni.items():
        testo = '%s · %d linee' % (area, len(REG.per_area(area)))
        w, h = _misura(d, testo, px)
        etichette.append(dict(area=area, testo=testo, w=w, h=h,
                              cx=lx * im.size[0], cy=ly * im.size[1],
                              ax=px_ * im.size[0], py=py_ * im.size[1]))
    # la punta resta dov'e': si sposta solo la pastiglia, e mai a ridosso
    _scosta(etichette, aria=px * 0.52, limite=px * 1.6)

    # prima tutti i richiami, poi tutte le pastiglie: dove due settori sono
    # vicini un richiamo passa sopra l'etichetta di un altro, e tagliata in due
    # una parola non si legge. Cosi' la linea sparisce dietro la pastiglia, che
    # e' come si comporta una cartina.
    for et in etichette:
        col = COLORE_AREA[et['area']]
        p = (et['ax'], et['py'])
        e = (et['cx'], et['cy'])
        # richiamo: filo bianco sotto, colore sopra, cosi' si legge su roccia
        # chiara come su bosco scuro
        d.line([e, p], fill=COLORI['bianco'] + (190,), width=max(5, px // 4))
        d.line([e, p], fill=col + (255,), width=max(2, px // 8))
        r = px * 0.30
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r],
                  fill=col + (255,), outline=COLORI['bianco'] + (220,),
                  width=max(2, px // 10))
    for et in etichette:
        _pastiglia(d, (et['cx'], et['cy']), et['testo'],
                   COLORE_AREA[et['area']], px)

    out.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB').save(
        out, 'JPEG', quality=90, optimize=True, progressive=True)
    return out


def griglia(sorgente, out, colonne=14):
    """Copia della panoramica con sopra una griglia di caselle nominate.

    Serve a farsi indicare le posizioni senza chiedere a nessuno di stimare
    coordinate a occhio: si dice «Anfiteatro in D5» e la casella diventa un
    punto. E' uno strumento di lavoro, non entra nel manuale.
    """
    im = Image.open(sorgente).convert('RGB')
    w, h = im.size
    passo = w / colonne
    righe = max(1, int(round(h / passo)))
    velo = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(velo)
    px = max(13, int(passo / 3.4))
    f = _font(px)

    for c in range(colonne + 1):
        x = c * passo
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, 90), width=1)
    for r in range(righe + 1):
        y = r * h / righe
        d.line([(0, y), (w, y)], fill=(255, 255, 255, 90), width=1)

    for c in range(colonne):
        for r in range(righe):
            nome = '%s%d' % (chr(ord('A') + c), r + 1)
            x, y = c * passo + passo * 0.5, (r + 0.5) * h / righe
            l, t, rr, b = d.textbbox((0, 0), nome, font=f)
            d.text((x - (rr - l) / 2 - l, y - (b - t) / 2 - t), nome, font=f,
                   fill=(255, 255, 255, 150),
                   stroke_width=max(1, px // 9), stroke_fill=(0, 0, 0, 170))

    out.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB').save(
        out, 'JPEG', quality=88, optimize=True, progressive=True)
    return out, colonne, righe


def centro_casella(nome, colonne=14, righe=9):
    """Da «D5» alle coordinate relative del centro della casella."""
    nome = nome.strip().upper()
    c = ord(nome[0]) - ord('A')
    r = int(nome[1:]) - 1
    return ((c + 0.5) / colonne, (r + 0.5) / righe)


def main():
    src = panoramica()
    if '--griglia' in sys.argv:
        if src is None:
            print('Nessuna vista d\'insieme da quadrettare: vedi sotto.')
        else:
            out, nc, nr = griglia(src, DEST / 'panoramica_griglia.jpg')
            print('scritto %s  (%d colonne A..%s, %d righe 1..%d)'
                  % (out, nc, chr(ord('A') + nc - 1), nr, nr))
            return 0
    if src is None:
        print('Nessuna vista d\'insieme trovata.')
        print()
        print('Mettere il file in %s/ con «panoramica» nel nome,' % SORG)
        print('per esempio  panoramica.jpg  —  esportato da i-pietra')
        print('CON LE ETICHETTE DELLE LINEE LEGGIBILI: sono quelle a dire quale')
        print('settore e\' quale, ed e\' l\'unico modo di posizionarli senza tirare')
        print('a indovinare.')
        return 1

    mancanti = [a for a in REG.AREE if a not in POSIZIONI]
    if mancanti:
        print('Vista d\'insieme: %s' % src.name)
        print()
        print('Posizioni non dichiarate per %d settori su %d:'
              % (len(mancanti), len(REG.AREE)))
        for a in mancanti:
            print('  - %-16s %d linee' % (a, len(REG.per_area(a))))
        print()
        print('Compilare POSIZIONI in questo file, in coordinate relative 0..1')
        print('con l\'origine in alto a sinistra:')
        print()
        print("    POSIZIONI = {")
        print("        'Anfiteatro': ((0.55, 0.48), (0.62, 0.30)),")
        print("        #              punta sulla parete,  pastiglia")
        print("    }")
        print()
        print('Le posizioni devono venire dalle etichette leggibili sulla')
        print('panoramica o da chi conosce lo spot, non dedotte per somiglianza.')
        return 1

    out = disegna(src, POSIZIONI, DEST / 'panoramica_settori.jpg')
    print('scritto %s' % out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
