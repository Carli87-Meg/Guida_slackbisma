#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae fotogrammi da un video a timestamp precisi, con un ventaglio di scatti
attorno a ogni istante per poter scegliere quello nitido.

Uso:
    # tre candidati attorno a 4:12 e a 7:05
    python tools/03_estrai_frame.py video/rigging_01.mp4 4:12 7:05

    # un solo scatto per timestamp, lato lungo 1600 px
    python tools/03_estrai_frame.py video/rigging_01.mp4 4:12 --ventaglio 0 --lato 1600

    # da un file di timestamp (una riga: "4:12  ancoraggio principale")
    python tools/03_estrai_frame.py video/rigging_01.mp4 --lista frame.txt

Output in lavorazione/frame_grezzi/<nome_video>/ con nomi tipo
    rigging_01_0412_-05.jpg   (mezzo secondo prima)
    rigging_01_0412_000.jpg   (esatto)
    rigging_01_0412_+05.jpg   (mezzo secondo dopo)

Poi: guardare i file con il tool `view` e tenere solo i migliori.
Lo script stampa alla fine una stima di nitidezza (varianza del laplaciano) per
ogni frame, se opencv è installato: valori più alti = più a fuoco.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rotazione import rotazione_video, ruota_immagine        # noqa: E402


def parse_ts(s):
    """Accetta 90, 1:30, 01:30, 1:02:03 -> secondi float."""
    parti = [float(p) for p in str(s).split(':')]
    sec = 0.0
    for p in parti:
        sec = sec * 60 + p
    return sec


def tag(sec):
    return '%02d%02d' % (int(sec) // 60, int(sec) % 60)


def _estrai_pyav(video: Path, sec: float, out: Path, lato: int):
    """Estrazione senza il binario ffmpeg: PyAV porta con se' le librerie.

    Cerca il keyframe precedente e poi decodifica in avanti fino all'istante
    richiesto, cosi' il fotogramma e' quello giusto e non il keyframe.
    """
    import av
    sec = max(sec, 0.0)
    with av.open(str(video)) as c:
        vs = c.streams.video[0]
        vs.thread_type = 'AUTO'
        c.seek(int(sec / vs.time_base), stream=vs, any_frame=False, backward=True)
        scelto = None
        for frame in c.decode(vs):
            scelto = frame
            if frame.time is not None and frame.time >= sec:
                break
        if scelto is None:
            raise RuntimeError('nessun fotogramma a %.2f s in %s' % (sec, video.name))
        img = scelto.to_image()
    img = ruota_immagine(img, rotazione_video(video))
    w, h = img.size
    if max(w, h) > lato:
        from PIL import Image as _I
        if w >= h:
            img = img.resize((lato, round(h * lato / w)), _I.LANCZOS)
        else:
            img = img.resize((round(w * lato / h), lato), _I.LANCZOS)
    img.save(str(out), quality=92)


def estrai(video: Path, sec: float, out: Path, lato: int):
    out.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which('ffmpeg'):
        vf = "scale='if(gt(iw,ih),%d,-2)':'if(gt(iw,ih),-2,%d)'" % (lato, lato)
        cmd = ['ffmpeg', '-y', '-loglevel', 'error',
               '-ss', '%.3f' % max(sec, 0), '-i', str(video),
               '-frames:v', '1', '-vf', vf, '-q:v', '2', str(out)]
        subprocess.run(cmd, check=True)
    else:
        _estrai_pyav(video, sec, out, lato)
    return out


def nitidezza(path):
    try:
        import cv2
    except ImportError:
        return None
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    return float(cv2.Laplacian(img, cv2.CV_64F).var())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('timestamp', nargs='*', help='es. 4:12 7:05 1:02:33')
    ap.add_argument('--lista', help='file con "mm:ss  descrizione" per riga')
    ap.add_argument('--out', default='lavorazione/frame_grezzi')
    ap.add_argument('--lato', type=int, default=1600, help='lato lungo in px')
    ap.add_argument('--ventaglio', type=float, default=0.5,
                    help='secondi prima/dopo (0 = solo scatto esatto)')
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        sys.exit('Video non trovato: %s' % video)

    voci = [(parse_ts(t), '') for t in args.timestamp]
    if args.lista:
        for riga in Path(args.lista).read_text(encoding='utf-8').splitlines():
            riga = riga.strip()
            if not riga or riga.startswith('#'):
                continue
            campi = riga.split(None, 1)
            voci.append((parse_ts(campi[0]), campi[1] if len(campi) > 1 else ''))
    if not voci:
        sys.exit('Nessun timestamp indicato.')

    dest = Path(args.out) / video.stem
    offsets = [0.0] if args.ventaglio <= 0 else [-args.ventaglio, 0.0, args.ventaglio]
    prodotti = []

    for sec, desc in voci:
        print('\n%s  %s' % (tag(sec), desc))
        for off in offsets:
            suff = '000' if off == 0 else ('%+03d' % round(off * 10))
            f = dest / ('%s_%s_%s.jpg' % (video.stem, tag(sec), suff))
            estrai(video, sec + off, f, args.lato)
            n = nitidezza(f)
            prodotti.append((f, n))
            print('   %s%s' % (f.name, '   nitidezza %.0f' % n if n else ''))

    print('\n%d fotogrammi in %s' % (len(prodotti), dest))
    con_n = [(f, n) for f, n in prodotti if n is not None]
    if con_n:
        print('\nI più nitidi:')
        for f, n in sorted(con_n, key=lambda x: -x[1])[:8]:
            print('   %8.0f  %s' % (n, f.name))
    print('\nGuarda i file con il tool `view` prima di sceglierli: la nitidezza numerica')
    print('non dice se la manovra è leggibile o se qualcuno copre l\'inquadratura.')


if __name__ == '__main__':
    main()
