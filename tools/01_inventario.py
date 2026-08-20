#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventario dei video sorgente, senza bisogno di ffprobe da riga di comando.

Variante Python di 01_inventario.sh per macchine dove il binario ffmpeg/ffprobe
non e' installato: usa PyAV, che porta con se' le librerie ffmpeg.

    python tools/01_inventario.py [cartella_video]

Legge solo i metadati, non modifica ne' sposta nulla.
Stampa anche la data di ripresa, che serve a mettere le clip in ordine reale.
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rotazione import rotazione_video                        # noqa: E402

VIDEO_EXT = {'.mp4', '.mov', '.m4v', '.avi', '.mkv', '.insv'}


def mmss(s):
    return '%d:%02d' % (int(s) // 60, int(s) % 60)


def leggi(p: Path):
    import av
    d = {'file': p.name, 'byte': p.stat().st_size, 'durata': None,
         'w': None, 'h': None, 'fps': None, 'audio': None, 'girato': None,
         'rot': 0}
    with av.open(str(p)) as c:
        if c.duration:
            d['durata'] = c.duration / 1_000_000
        meta = dict(c.metadata or {})
        for k in ('com.apple.quicktime.creationdate', 'creation_time', 'date'):
            if meta.get(k):
                d['girato'] = meta[k]
                break
        vs = next((s for s in c.streams if s.type == 'video'), None)
        if vs is not None:
            d['w'], d['h'] = vs.codec_context.width, vs.codec_context.height
            if vs.average_rate:
                d['fps'] = float(vs.average_rate)
            # Sui video da iPhone la geometria reale e' ruotata: l'orientamento
            # sta nella matrice del tkhd, che PyAV non espone.
            d['rot'] = rotazione_video(p)
            if d['rot'] in (90, 270):
                d['w'], d['h'] = d['h'], d['w']
        a = next((s for s in c.streams if s.type == 'audio'), None)
        if a is not None:
            d['audio'] = '%s %d Hz %dch' % (a.codec_context.name,
                                            a.codec_context.sample_rate or 0,
                                            a.codec_context.channels or 0)
    return d


def norm_data(s):
    if not s:
        return ''
    s = s.replace('Z', '+0000')
    for f in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z',
              '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(s, f).strftime('%d/%m/%Y %H:%M:%S')
        except ValueError:
            pass
    return s


def main():
    dir_video = Path(sys.argv[1] if len(sys.argv) > 1 else 'video')
    file = sorted(p for p in dir_video.rglob('*') if p.suffix.lower() in VIDEO_EXT)
    if not file:
        sys.exit('Nessun video in %s' % dir_video)

    righe = []
    for p in file:
        try:
            righe.append(leggi(p))
        except Exception as e:                                  # noqa: BLE001
            print('  ! %s: %s' % (p.name, e), file=sys.stderr)

    righe.sort(key=lambda r: (r['girato'] or '', r['file']))

    hdr = '%-16s %8s %11s %6s %8s  %-19s  %s'
    print(hdr % ('FILE', 'DURATA', 'RISOLUZ.', 'FPS', 'PESO', 'GIRATO IL', 'AUDIO'))
    print('-' * 104)
    for r in righe:
        print(hdr % (
            r['file'],
            mmss(r['durata']) if r['durata'] else '?',
            '%dx%d' % (r['w'], r['h']) if r['w'] else '?',
            '%.0f' % r['fps'] if r['fps'] else '?',
            '%.0f MB' % (r['byte'] / 1e6),
            norm_data(r['girato']),
            r['audio'] or 'NESSUNO'))

    tot = sum(r['durata'] or 0 for r in righe)
    peso = sum(r['byte'] for r in righe)
    senza = [r['file'] for r in righe if not r['audio']]
    print('-' * 104)
    print('%d file - durata totale %d min %02d s - %.1f GB'
          % (len(righe), tot // 60, tot % 60, peso / 1e9))
    if senza:
        print('Senza traccia audio (non trascrivibili): %s' % ', '.join(senza))


if __name__ == '__main__':
    main()
