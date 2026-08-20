#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ricerca trasversale nelle trascrizioni, con fonte [file @ mm:ss].

    python tools/cerca.py sosta backup grillo

Serve a non citare mai un dato senza il timestamp da cui viene.
"""
import json
import re
import sys
from pathlib import Path

DIR = Path('lavorazione/trascrizioni')


def mmss(s):
    return '%d:%02d' % (int(s) // 60, int(s) % 60)


def main():
    if len(sys.argv) < 2:
        sys.exit('Uso: python tools/cerca.py <termine> [termine...]')
    termini = [t.lower() for t in sys.argv[1:]]
    rx = re.compile('|'.join(re.escape(t) for t in termini), re.I)

    trovati = 0
    for j in sorted(DIR.glob('*.json')):
        d = json.loads(j.read_text(encoding='utf-8'))
        for seg in d['segmenti']:
            if rx.search(seg['testo']):
                trovati += 1
                print('[%s @ %s] %s' % (d['file'], mmss(seg['start']), seg['testo']))
    print('\n-- %d occorrenze per: %s' % (trovati, ', '.join(termini)))


if __name__ == '__main__':
    main()
