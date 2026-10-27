#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Legge da SlackMap le ventiquattro linee della Pietra e scrive dati/slackmap.py.

SlackMap e' la mappa mondiale delle slackline dell'International Slackline
Association. Per ogni linea l'API pubblica restituisce nome, lunghezza del
segmento disegnato e le coordinate dei due capi:

    https://api.slackmap.com/line/<id>/details

Gli id delle ventiquattro linee vengono dal lotto 31 del catalogo i-pietra
(data/catalog/riscrittura/31-highline.md, 20/10/2026), dove l'utente ha
abbinato ogni linea della locandina alla sua voce SlackMap.

Che cosa vale e che cosa no:

* il **nome** e' quello che la linea ha su SlackMap, scritto da chi l'ha
  censita; le linee senza nome restano senza nome;
* le **coordinate** sono quelle del segmento disegnato sulla mappa, non una
  misura (`isMeasured` e' falso per tutte): sulla 53 m, confrontate con le
  letture del telefono fatte stando agli ancoraggi, risultano spostate di
  10-19 m verso ovest. Servono ad avvicinarsi, non a trovare un punto;
* la **lunghezza** e' quella del segmento disegnato: non sostituisce il valore
  di catalogo della locandina.

    python tools/06_slackmap.py            # scarica e riscrive dati/slackmap.py
    python tools/06_slackmap.py --offline  # riscrive dal json gia' scaricato
"""
import io
import json
import math
import sys
import urllib.request
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CACHE = RADICE / 'lavorazione' / 'slackmap'
DEST = RADICE / 'dati' / 'slackmap.py'
API = 'https://api.slackmap.com/line/%s/details'

# id della linea nel registro -> id SlackMap (lotto 31 di i-pietra, 20/10/2026)
ID = {
    'rookie-18': 'Sn8f0SS', 'rookie-27': 'r3yyHbn', 'rookie-40': '8y7K14L',
    'rookie-60': 'O9z7pFx',
    'anfiteatro-20': 'JG8Yi5z', 'anfiteatro-27': 'PX29ZPA', 'anfiteatro-46': 'FlwIt50',
    'anfiteatro-53': 'nym-s4g', 'anfiteatro-97': 'F4sDJKQ', 'anfiteatro-108': 'mXFD-6Q',
    'anfiteatro-113': 't2qJAK8',
    'anfite-altro-22': 'UQ2_y7z', 'anfite-altro-30': '1SJ6phO', 'anfite-altro-135': 'QPp5V-S',
    'settore-giallo-28': 'NYQcHAC', 'settore-giallo-45': 'UvttZ72',
    'settore-giallo-50': 'aUYtQdd', 'settore-giallo-55': 'jKzSch5',
    'despedida-35': 'svysOPW', 'despedida-45': '4z4WcEl', 'despedida-60': 'Rp-QqWJ',
    'despedida-70': 'f4EyGNs', 'despedida-85': 'PPySEMm', 'despedida-165': 'pqhMd2D',
}


def scarica(sid):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / ('%s.json' % sid)
    if '--offline' not in sys.argv or not f.exists():
        with urllib.request.urlopen(API % sid, timeout=30) as r:
            f.write_bytes(r.read())
    return json.loads(f.read_text(encoding='utf-8'))


def distanza_m(a, b):
    """Distanza fra due coppie (lon, lat), in metri, per tratti brevi."""
    lat = math.radians((a[1] + b[1]) / 2)
    dx = math.radians(b[0] - a[0]) * 6371000 * math.cos(lat)
    dy = math.radians(b[1] - a[1]) * 6371000
    return math.hypot(dx, dy)


def main():
    oggi = date.today().strftime('%d/%m/%Y')
    righe = []
    for lid, sid in ID.items():
        d = scarica(sid)
        geom = d['geoJson']['features'][0]['geometry']['coordinates']
        capi = [(c[1], c[0]) for c in geom]           # (lat, lon)
        nome = (d.get('name') or '').strip() or None
        righe.append((lid, sid, nome, round(float(d.get('length') or 0), 1),
                      bool(d.get('isMeasured')), capi,
                      (d.get('createdDateTime') or '')[:10]))
        print('%-18s %-8s %-22s %6.1f m  %s  capi %s' % (
            lid, sid, nome or '—', righe[-1][3], 'misurata' if righe[-1][4] else 'disegnata',
            ' · '.join('%.5f, %.5f' % c for c in capi)))

    out = io.StringIO()
    out.write('# -*- coding: utf-8 -*-\n')
    out.write('"""Le linee della Pietra su SlackMap. FILE GENERATO: non modificare a mano.\n\n')
    out.write('Scritto da tools/06_slackmap.py il %s, dall\'API pubblica\n' % oggi)
    out.write('https://api.slackmap.com/line/<id>/details. Gli id vengono dal lotto 31 del\n')
    out.write('catalogo i-pietra (20/10/2026), dove l\'utente ha abbinato ogni linea della\n')
    out.write('locandina alla sua voce SlackMap.\n\n')
    out.write('Le coordinate sono quelle del segmento DISEGNATO sulla mappa, non misurate\n')
    out.write('(`misurata` e\' falso per tutte): sulla 53 m risultano spostate di 10-19 m\n')
    out.write('verso ovest rispetto alle letture del telefono fatte agli ancoraggi. Servono\n')
    out.write('ad avvicinarsi, non a trovare un punto. La lunghezza e\' quella del segmento.\n"""\n\n')
    out.write("LETTO_IL = '%s'\n\n" % oggi)
    out.write('# id linea -> dati SlackMap\n')
    out.write('LINEE = {\n')
    for lid, sid, nome, lung, mis, capi, creata in righe:
        out.write("    '%s': {\n" % lid)
        out.write("        'id': '%s',\n" % sid)
        out.write("        'nome': %s,\n" % (repr(nome) if nome else 'None'))
        out.write("        'lunghezza_segmento': %.1f,\n" % lung)
        out.write("        'misurata': %s,\n" % mis)
        out.write("        'capi': [%s],\n" % ', '.join('(%.6f, %.6f)' % c for c in capi))
        out.write("        'creata': '%s',\n" % creata)
        out.write("        'url': 'https://slackmap.com/line/%s',\n" % sid)
        out.write('    },\n')
    out.write('}\n\n\n')
    out.write('def di(id_linea):\n    return LINEE.get(id_linea)\n\n\n')
    out.write('def mappa(lat, lon):\n')
    out.write("    return 'https://www.google.com/maps?q=%.6f,%.6f' % (lat, lon)\n")
    DEST.write_text(out.getvalue(), encoding='utf-8', newline='\n')
    print('\nscritto %s (%d linee)' % (DEST, len(righe)))


if __name__ == '__main__':
    main()
