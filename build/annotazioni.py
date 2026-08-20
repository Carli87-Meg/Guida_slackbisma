#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Annotazioni dei fotogrammi scelti — Fase 5.

Ogni voce e' stata posizionata guardando il fotogramma, non a stima. Le didascalie
descrivono solo cio' che si vede: dove il nome tecnico non e' confermato, lo dicono
con `[DA CONFERMARE]` invece di inventarlo.

Codice colore, uno per fase (palette di design.py via tools/annota.py):
    azzurro  fase B — costruzione della sosta, instradamento della slinga
    ambra    fase F — blocco del backup
    verde    fase G — anti-slip

    python build/annotazioni.py
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'tools'))

from annota import Annotatore                                   # noqa: E402

SORG = RADICE / 'lavorazione' / 'frame_grezzi'
DEST = RADICE / 'lavorazione' / 'frame_annotati'


def frame(video, ts):
    return SORG / video / ('%s_%s_000.jpg' % (video, ts))


# --------------------------------------------------------------------------
# Fase B — instradamento della slinga viola nell'anello d'acciaio
# La manovra che l'audio rende incomprensibile ("pista, pif, paf").
# --------------------------------------------------------------------------
def fase_b():
    C = 'azzurro'

    a = Annotatore(frame('IMG_1366', '0017'))
    a.numero((0.09, 0.07), 1, C)
    a.cerchio((0.66, 0.22), 0.075, 'riga di marcatura', C)
    a.freccia((0.42, 0.62), (0.30, 0.44), None, C)
    a.didascalia('1 — La slinga viola aperta in mano, pronta a essere instradata', C)
    a.salva(DEST / 'B1_slinga_aperta.jpg')

    a = Annotatore(frame('IMG_1366', '0020'))
    a.numero((0.90, 0.06), 2, C)          # a destra: a sinistra c'e' l'etichetta
    a.cerchio((0.13, 0.17), 0.090, "anello d'acciaio", C)
    a.freccia((0.52, 0.40), (0.27, 0.25), None, C)
    a.didascalia("2 — La slinga viene fatta passare nell'anello d'acciaio", C)
    a.salva(DEST / 'B2_passaggio_anello.jpg')

    a = Annotatore(frame('IMG_1366', '0030'))
    a.numero((0.09, 0.06), 3, C)
    a.cerchio((0.20, 0.455), 0.115, "anello d'acciaio", C)
    a.freccia((0.63, 0.60), (0.35, 0.49), None, C)
    a.didascalia('3 — Il giro si chiude sull\'anello  ·  nome del nodo [DA CONFERMARE]', C)
    a.salva(DEST / 'B3_giro_chiuso.jpg')


# --------------------------------------------------------------------------
# Fase F — collegamento weblock / grillo sul lato tensione
# --------------------------------------------------------------------------
def fase_f():
    C = 'ambra'

    a = Annotatore(frame('IMG_1384', '0050'))
    a.numero((0.09, 0.06), 1, C)
    a.cerchio((0.56, 0.505), 0.100, 'grillo a lira', C)
    a.cerchio((0.55, 0.735), 0.085, 'weblock azzurro', C)
    a.riquadro([0.02, 0.47, 0.34, 0.72], 'fettuccia viola e corda rosa', C)
    a.didascalia('Lato tensione: weblock, grillo a lira, fettuccia viola e corda rosa'
                 '  ·  percorso del carico [DA CONFERMARE]', C)
    a.salva(DEST / 'F1_weblock_grillo.jpg')


# --------------------------------------------------------------------------
# Fase G — anti-slip
# L'unico passaggio del corpus insieme spiegato a voce e mostrato:
# "serve per evitare che la linea slitti nella banana" [IMG_1395 @ 0:25].
# --------------------------------------------------------------------------
def fase_g():
    C = 'verde'

    a = Annotatore(frame('IMG_1395', '0025'))
    a.numero((0.09, 0.06), 1, C)
    a.cerchio((0.62, 0.545), 0.085, 'anti-slip', C)
    a.didascalia('Anti-slip — «serve per evitare che la linea slitti nella banana»'
                 '  [IMG_1395 @ 0:25]', C)
    a.salva(DEST / 'G1_antislip.jpg')


# --------------------------------------------------------------------------
# Fase D — ancoraggio su roccia
# Documentato dalle foto iCloud del 16/05 alle 13:41, non dai video.
# --------------------------------------------------------------------------
FOTO = RADICE / 'lavorazione' / 'foto_dritte'
DETT = RADICE / 'lavorazione' / 'dettagli'


def fase_d():
    C = 'rosso'

    a = Annotatore(FOTO / 'IMG_1371.jpg')
    a.numero((0.09, 0.05), 1, C)
    a.cerchio((0.50, 0.537), 0.045, 'placchetta su bullone', C)
    a.cerchio((0.76, 0.620), 0.040, 'cordino di collegamento', C)
    a.cerchio((0.89, 0.812), 0.045, 'carrucola bloccante', C)
    a.riquadro([0.22, 0.700, 0.69, 0.762], 'slinga viola', C)
    a.didascalia('Ancoraggio su roccia — i punti sono uniti da corda annodata'
                 '  ·  angolo di apertura [DA CONFERMARE]', C)
    a.salva(DEST / 'D1_ancoraggio.jpg')

    a = Annotatore(DETT / 'IMG_1372_placchetta.jpg')
    a.cerchio((0.27, 0.72), 0.105, 'dado esagonale', C)
    a.didascalia('Placchetta fissata con dado su bullone: tassello meccanico, '
                 'non spit a vite né resinato  ·  misura [DA CONFERMARE]', C)
    a.salva(DEST / 'D2_placchetta_dettaglio.jpg')


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    fase_b()
    fase_d()
    fase_f()
    fase_g()


if __name__ == '__main__':
    main()
