#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rotazione di visualizzazione di un video MOV/MP4.

I filmati girati con iPhone sono sempre registrati in orizzontale: l'orientamento
reale sta nella matrice di trasformazione dell'atomo `tkhd`, non nei pixel. PyAV
non la espone, e ffmpeg da riga di comando qui non c'e', quindi la leggiamo a mano
dal contenitore. Senza questa correzione i fotogrammi escono coricati.

    from tools.rotazione import rotazione_video
    gradi = rotazione_video(Path('video/IMG_1395.MOV'))   # 0, 90, 180 o 270

Uso da riga di comando, per controllo:

    python tools/rotazione.py video/IMG_1395.MOV
"""
import math
import struct
import sys
from pathlib import Path

# Atomi che contengono altri atomi e che quindi vanno aperti per cercare tkhd.
CONTENITORI = {b'moov', b'trak', b'mdia', b'edts'}


def _percorri(f, fine, cerca=b'tkhd'):
    """Scorre gli atomi fino a `fine`, scendendo nei contenitori."""
    while f.tell() < fine:
        inizio = f.tell()
        testa = f.read(8)
        if len(testa) < 8:
            return None
        dim, tipo = struct.unpack('>I4s', testa)
        if dim == 1:                       # dimensione a 64 bit
            dim = struct.unpack('>Q', f.read(8))[0]
            corpo = inizio + 16
        elif dim == 0:                     # arriva a fine file
            dim = fine - inizio
            corpo = inizio + 8
        else:
            corpo = inizio + 8
        if dim < 8:
            return None
        if tipo == cerca:
            f.seek(corpo)
            return f.read(inizio + dim - corpo)
        if tipo in CONTENITORI:
            f.seek(corpo)
            trovato = _percorri(f, inizio + dim, cerca)
            if trovato is not None:
                return trovato
        f.seek(inizio + dim)
    return None


def rotazione_video(percorso) -> int:
    """Gradi di rotazione da applicare in senso orario: 0, 90, 180 o 270.

    Restituisce 0 se il file non e' un MOV/MP4 o se la matrice non e' leggibile:
    meglio un fotogramma non ruotato che un errore a meta' pipeline.
    """
    percorso = Path(percorso)
    try:
        with percorso.open('rb') as f:
            fine = percorso.stat().st_size
            tkhd = _percorri(f, fine)
    except OSError:
        return 0
    if not tkhd or len(tkhd) < 4:
        return 0

    versione = tkhd[0]
    # salta version+flags, poi i campi a lunghezza variabile secondo la versione
    off = 4 + (32 if versione == 1 else 20) + 8 + 2 + 2 + 2 + 2
    if len(tkhd) < off + 36:
        return 0
    m = struct.unpack('>9i', tkhd[off:off + 36])
    a, b = m[0] / 65536.0, m[1] / 65536.0
    if a == 0 and b == 0:
        return 0
    gradi = round(math.degrees(math.atan2(b, a))) % 360
    # ammettiamo solo i quarti di giro: qualsiasi altro valore non e' orientamento
    return gradi if gradi in (0, 90, 180, 270) else 0


def ruota_immagine(img, gradi: int):
    """Applica a un'immagine PIL la rotazione di visualizzazione."""
    if gradi == 90:
        from PIL import Image
        return img.transpose(Image.ROTATE_270)     # orario
    if gradi == 180:
        from PIL import Image
        return img.transpose(Image.ROTATE_180)
    if gradi == 270:
        from PIL import Image
        return img.transpose(Image.ROTATE_90)
    return img


if __name__ == '__main__':
    for p in sys.argv[1:] or ['video']:
        p = Path(p)
        file = sorted(p.rglob('*.MOV')) if p.is_dir() else [p]
        for v in file:
            print('%-18s %3d gradi' % (v.name, rotazione_video(v)))
