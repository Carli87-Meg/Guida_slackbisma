#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Annotazione dei fotogrammi: frecce, cerchi, riquadri, etichette numerate.
Stessa palette del sistema grafico, così le annotazioni parlano la stessa lingua
del PDF finale.

Due modi d'uso.

A) Da riga di comando, con una descrizione JSON:

    python tools/annota.py frame.jpg out.jpg --json annotazioni.json

    annotazioni.json:
    {
      "annotazioni": [
        {"tipo": "freccia", "da": [0.20, 0.80], "a": [0.46, 0.52],
         "testo": "1", "colore": "rosso"},
        {"tipo": "cerchio", "centro": [0.46, 0.50], "r": 0.07,
         "testo": "grillo di collegamento", "colore": "rosso"},
        {"tipo": "riquadro", "box": [0.60, 0.30, 0.88, 0.62],
         "testo": "backup", "colore": "verde"},
        {"tipo": "didascalia", "testo": "Fase 3 — collegamento al masterpoint"}
      ]
    }

Tutte le coordinate sono relative (0–1), così valgono a qualsiasi risoluzione.

B) Da Python, per uso dentro uno script di build:

    from tools.annota import Annotatore
    a = Annotatore('frame.jpg')
    a.freccia((.2,.8), (.46,.52), '1', 'rosso')
    a.cerchio((.46,.5), .07, 'grillo di collegamento', 'rosso')
    a.didascalia('Fase 3 — collegamento al masterpoint')
    a.salva('out.jpg')

Dipendenze: pillow
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Palette allineata a design.py
COLORI = {
    'rosso': (224, 58, 47),
    'arancio': (226, 98, 46),
    'ambra': (222, 138, 38),
    'oliva': (163, 167, 54),
    'verde': (63, 181, 58),
    'acqua': (31, 190, 136),
    'azzurro': (47, 159, 222),
    'blu': (24, 51, 63),
    'bianco': (255, 255, 255),
    'inchiostro': (20, 24, 28),
}
FONT_DIRS = [
    '/usr/share/fonts/truetype/google-fonts/',
    '/Library/Fonts/', '/System/Library/Fonts/Supplemental/',
    'C:/Windows/Fonts/',
]
FONT_CANDIDATI = ['Poppins-Bold.ttf', 'Poppins-SemiBold.ttf', 'Arial Bold.ttf',
                  'arialbd.ttf', 'DejaVuSans-Bold.ttf', 'Helvetica.ttc']


def _font(px):
    for d in FONT_DIRS:
        for n in FONT_CANDIDATI:
            p = Path(d) / n
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), px)
                except OSError:
                    pass
    return ImageFont.load_default()


class Annotatore:
    def __init__(self, path, colore_default='rosso'):
        self.img = Image.open(path).convert('RGB')
        self.W, self.H = self.img.size
        self.d = ImageDraw.Draw(self.img, 'RGBA')
        self.k = max(self.W, self.H) / 1600.0     # fattore di scala
        self.default = colore_default
        self._cap = None

    # -------------------------------------------------- utilità
    def _c(self, nome):
        return COLORI.get(nome or self.default, COLORI['rosso'])

    def _p(self, xy):
        return (xy[0] * self.W, xy[1] * self.H)

    def _sp(self, v):
        return max(1, int(round(v * self.k)))

    def _testo_su_pastiglia(self, xy, testo, colore, px=26, ancora='centro'):
        f = _font(self._sp(px))
        bb = self.d.textbbox((0, 0), testo, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad = self._sp(10)
        w, h = tw + 2 * pad, th + int(1.5 * pad)
        x, y = xy
        if ancora == 'centro':
            x -= w / 2
            y -= h / 2
        r = h / 2
        self.d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                                 fill=colore + (242,))
        self.d.text((x + pad - bb[0], y + 0.75 * pad - bb[1]), testo,
                    font=f, fill=COLORI['bianco'])
        return (x, y, x + w, y + h)

    # -------------------------------------------------- primitive
    def freccia(self, da, a, testo=None, colore=None, spessore=5):
        """Freccia da un punto a un altro, entrambi in coordinate relative."""
        col = self._c(colore)
        x0, y0 = self._p(da)
        x1, y1 = self._p(a)
        s = self._sp(spessore)
        # alone bianco per leggibilità su qualsiasi sfondo
        self.d.line([x0, y0, x1, y1], fill=COLORI['bianco'] + (200,), width=s + self._sp(3))
        self.d.line([x0, y0, x1, y1], fill=col, width=s)
        ang = math.atan2(y1 - y0, x1 - x0)
        L = self._sp(26)
        ap = math.radians(24)
        p1 = (x1 - L * math.cos(ang - ap), y1 - L * math.sin(ang - ap))
        p2 = (x1 - L * math.cos(ang + ap), y1 - L * math.sin(ang + ap))
        self.d.polygon([(x1, y1), p1, p2], fill=col,
                       outline=COLORI['bianco'] + (200,))
        if testo:
            self._testo_su_pastiglia((x0, y0), testo, col)
        return self

    def cerchio(self, centro, r, testo=None, colore=None, spessore=5):
        """Evidenzia un dettaglio. r è relativo al lato lungo."""
        col = self._c(colore)
        cx, cy = self._p(centro)
        rr = r * max(self.W, self.H)
        s = self._sp(spessore)
        box = [cx - rr, cy - rr, cx + rr, cy + rr]
        self.d.ellipse(box, outline=COLORI['bianco'] + (200,), width=s + self._sp(3))
        self.d.ellipse(box, outline=col, width=s)
        if testo:
            self._etichetta_esterna(cx, cy - rr - self._sp(14), testo, col)
        return self

    def riquadro(self, box, testo=None, colore=None, spessore=5):
        """box = [x0, y0, x1, y1] relativi."""
        col = self._c(colore)
        x0, y0 = self._p(box[:2])
        x1, y1 = self._p(box[2:])
        s = self._sp(spessore)
        self.d.rectangle([x0, y0, x1, y1], outline=COLORI['bianco'] + (200,),
                         width=s + self._sp(3))
        self.d.rectangle([x0, y0, x1, y1], outline=col, width=s)
        if testo:
            self._etichetta_esterna((x0 + x1) / 2, y0 - self._sp(14), testo, col)
        return self

    def numero(self, xy, n, colore=None):
        """Pallino numerato per le sequenze."""
        col = self._c(colore)
        cx, cy = self._p(xy)
        r = self._sp(24)
        self.d.ellipse([cx - r - self._sp(2), cy - r - self._sp(2),
                        cx + r + self._sp(2), cy + r + self._sp(2)],
                       fill=COLORI['bianco'] + (220,))
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        f = _font(self._sp(28))
        t = str(n)
        bb = self.d.textbbox((0, 0), t, font=f)
        self.d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
                    t, font=f, fill=COLORI['bianco'])
        return self

    def _etichetta_esterna(self, cx, cy, testo, col):
        f = _font(self._sp(24))
        bb = self.d.textbbox((0, 0), testo, font=f)
        w = bb[2] - bb[0] + self._sp(20)
        x = min(max(cx - w / 2, self._sp(8)), self.W - w - self._sp(8))
        y = max(cy - self._sp(34), self._sp(8))
        self._testo_su_pastiglia((x, y), testo, col, px=24, ancora='alto-sx')
        return self

    def didascalia(self, testo, colore=None):
        """Fascia in basso con il titolo del passo."""
        self._cap = (testo, self._c(colore))
        return self

    def _adatta_didascalia(self, testo, larghezza):
        """Trova corpo e righe che fanno stare la didascalia nella fascia.

        Prima prova a rimpicciolire il carattere, poi manda a capo su due righe.
        Senza questo una didascalia lunga usciva dal bordo destro e il testo
        veniva perso: su un manuale tecnico e' una perdita di informazione.
        """
        for px in (28, 26, 24, 22, 20, 18):
            f = _font(self._sp(px))
            if self.d.textlength(testo, font=f) <= larghezza:
                return f, [testo], px
        # non basta rimpicciolire: si spezza in due righe sul confine di parola
        f = _font(self._sp(22))
        parole = testo.split(' ')
        migliore, scarto = None, None
        for i in range(1, len(parole)):
            a, b = ' '.join(parole[:i]), ' '.join(parole[i:])
            largo = max(self.d.textlength(a, font=f), self.d.textlength(b, font=f))
            if scarto is None or largo < scarto:
                migliore, scarto = (a, b), largo
        if migliore and scarto <= larghezza:
            return f, list(migliore), 22
        for px in (20, 18, 16, 14):
            f = _font(self._sp(px))
            if migliore and max(self.d.textlength(migliore[0], font=f),
                                self.d.textlength(migliore[1], font=f)) <= larghezza:
                return f, list(migliore), px
        return _font(self._sp(14)), list(migliore or [testo]), 14

    def _disegna_didascalia(self):
        if not self._cap:
            return
        testo, col = self._cap
        marg = self._sp(26)
        f, righe, px = self._adatta_didascalia(testo, self.W - 2 * marg)
        interlinea = self._sp(px + 8)
        h = max(self._sp(64), len(righe) * interlinea + self._sp(28))
        y = self.H - h
        self.d.rectangle([0, y, self.W, self.H], fill=(20, 24, 28, 214))
        self.d.rectangle([0, y, self._sp(8), self.H], fill=col)
        blocco = len(righe) * interlinea
        ty = y + (h - blocco) / 2
        for riga in righe:
            bb = self.d.textbbox((0, 0), riga, font=f)
            self.d.text((marg, ty - bb[1] + (interlinea - (bb[3] - bb[1])) / 2),
                        riga, font=f, fill=COLORI['bianco'])
            ty += interlinea

    def salva(self, out, qualita=90):
        self._disegna_didascalia()
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        self.img.save(out, quality=qualita)
        print('scritto %s  (%dx%d)' % (out, self.W, self.H))
        return out


def applica_json(sorgente, destinazione, spec):
    a = Annotatore(sorgente)
    for an in spec.get('annotazioni', []):
        t = an.get('tipo')
        c = an.get('colore')
        if t == 'freccia':
            a.freccia(an['da'], an['a'], an.get('testo'), c)
        elif t == 'cerchio':
            a.cerchio(an['centro'], an.get('r', 0.06), an.get('testo'), c)
        elif t == 'riquadro':
            a.riquadro(an['box'], an.get('testo'), c)
        elif t == 'numero':
            a.numero(an['xy'], an['n'], c)
        elif t == 'didascalia':
            a.didascalia(an['testo'], c)
        else:
            print('tipo sconosciuto, ignorato: %r' % t)
    return a.salva(destinazione)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sorgente')
    ap.add_argument('destinazione')
    ap.add_argument('--json', required=True, help='file con le annotazioni')
    args = ap.parse_args()
    spec = json.loads(Path(args.json).read_text(encoding='utf-8'))
    applica_json(args.sorgente, args.destinazione, spec)


if __name__ == '__main__':
    main()
