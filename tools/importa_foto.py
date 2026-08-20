#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingresso delle fotografie nuove: raddrizza, ridimensiona, legge i metadati.

Ogni foto che arriva da un telefono porta con se' dei dati che sono **fonti**
quanto il parlato dei video: l'istante dello scatto, e a volte la posizione GPS.
Il dubbio 3 di DUBBI.md — le coordinate dei due ancoraggi — si chiude con una
fotografia geolocalizzata, non con una stima sulla mappa. Perche' non vada
perduto niente, l'importazione stampa tutto quello che trova prima di scrivere.

Fa tre cose e nessun'altra:

* applica l'orientamento EXIF ai pixel (le foto iPhone sono spesso registrate
  coricate, come i MOV: vedi tools/rotazione.py);
* riduce il lato lungo a 2000 px — il manuale non stampa mai piu' grande di
  mezza A4, e i file interi pesano diversi MB l'uno;
* riporta data, ora, modello e GPS di ciascuno scatto.

**Non decide a quale linea appartenga la foto e non tocca il manuale.** La
cartella di destinazione la si passa a mano, perche' attribuire un ancoraggio
alla linea sbagliata e' l'errore che manda a montare dal lato sbagliato.

    python tools/importa_foto.py --in scatti/*.jpg --out lavorazione/ancoraggi/anfiteatro-53
    python tools/importa_foto.py --in scatti/IMG_2001.HEIC --solo-dati
"""
import argparse
import sys
from fractions import Fraction
from pathlib import Path

from PIL import Image, ExifTags, ImageOps

RADICE = Path(__file__).resolve().parent.parent

LATO_MAX = 2000
QUALITA = 88

_TAG = {v: k for k, v in ExifTags.TAGS.items()}
_GPS = {v: k for k, v in ExifTags.GPSTAGS.items()}


def _gradi(valore, riferimento):
    """Terna gradi/primi/secondi dell'EXIF -> grado decimale con segno."""
    g, m, s = (float(Fraction(x)) for x in valore)
    dec = g + m / 60 + s / 3600
    return -dec if riferimento in ('S', 'W') else dec


def metadati(percorso):
    """Data, ora, dispositivo e coordinate, per quel che c'e'. Mai dedotti."""
    fuori = {'file': percorso.name}
    with Image.open(percorso) as im:
        fuori['pixel'] = '%d×%d' % im.size
        exif = im.getexif()
        if not exif:
            return fuori
        base = exif.get_ifd(_TAG['ExifOffset']) if _TAG['ExifOffset'] in exif else {}
        scatto = base.get(_TAG['DateTimeOriginal']) or exif.get(_TAG['DateTime'])
        if scatto:
            fuori['scatto'] = scatto
        marca = exif.get(_TAG['Make'])
        modello = exif.get(_TAG['Model'])
        if marca or modello:
            fuori['dispositivo'] = ' '.join(x.strip() for x in (marca, modello) if x)
        gps = exif.get_ifd(_TAG['GPSInfo']) if _TAG['GPSInfo'] in exif else {}
        if gps.get(_GPS['GPSLatitude']) and gps.get(_GPS['GPSLongitude']):
            lat = _gradi(gps[_GPS['GPSLatitude']], gps.get(_GPS['GPSLatitudeRef'], 'N'))
            lon = _gradi(gps[_GPS['GPSLongitude']], gps.get(_GPS['GPSLongitudeRef'], 'E'))
            fuori['gps'] = '%.6f, %.6f' % (lat, lon)
            quota = gps.get(_GPS['GPSAltitude'])
            if quota:
                fuori['quota'] = '%.0f m' % float(Fraction(quota))
    return fuori


def importa(sorgente, destinazione):
    """Raddrizza e ridimensiona in `destinazione`. Torna il percorso scritto."""
    destinazione.mkdir(parents=True, exist_ok=True)
    with Image.open(sorgente) as im:
        # exif_transpose ruota i pixel secondo il tag di orientamento e lo
        # azzera: senza questo passaggio ReportLab impagina la foto coricata.
        im = ImageOps.exif_transpose(im)
        if im.mode not in ('RGB', 'L'):
            im = im.convert('RGB')
        if max(im.size) > LATO_MAX:
            f = LATO_MAX / max(im.size)
            im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
        fuori = destinazione / (sorgente.stem + '.jpg')
        im.save(fuori, 'JPEG', quality=QUALITA, optimize=True)
    return fuori


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--in', dest='sorgenti', nargs='+', required=True,
                    help='file da importare')
    ap.add_argument('--out', dest='destinazione',
                    help='cartella di destinazione, relativa alla radice del progetto')
    ap.add_argument('--solo-dati', action='store_true',
                    help='legge e stampa i metadati senza scrivere niente')
    a = ap.parse_args()

    if not a.solo_dati and not a.destinazione:
        ap.error('serve --out, oppure --solo-dati per la sola lettura')

    dest = None
    if a.destinazione:
        dest = Path(a.destinazione)
        if not dest.is_absolute():
            dest = RADICE / dest

    scritti, senza_data, con_gps = [], [], []
    for nome in a.sorgenti:
        p = Path(nome)
        if not p.exists():
            print('  manca: %s' % p, file=sys.stderr)
            continue
        m = metadati(p)
        voci = [m['file'], m['pixel']]
        voci.append(m.get('scatto', 'data assente'))
        if 'dispositivo' in m:
            voci.append(m['dispositivo'])
        if 'gps' in m:
            voci.append('GPS ' + m['gps'] + (' · %s' % m['quota'] if 'quota' in m else ''))
            con_gps.append(m['file'])
        if 'scatto' not in m:
            senza_data.append(m['file'])
        print('  ' + '  ·  '.join(voci))
        if dest:
            scritti.append(importa(p, dest))

    if dest:
        dove = dest.relative_to(RADICE) if dest.is_relative_to(RADICE) else dest
        print('\nscritti %d file in %s' % (len(scritti), dove))
    if con_gps:
        print('GPS presente su %d file: candidati a chiudere il dubbio 3 '
              '(coordinate degli ancoraggi).' % len(con_gps))
    if senza_data:
        print('Senza data di scatto: %s. L\'ora non va inventata: la scheda '
              'dichiara la fonte come «fotografia, data non registrata».'
              % ', '.join(senza_data))


if __name__ == '__main__':
    main()
