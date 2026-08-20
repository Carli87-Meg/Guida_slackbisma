#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estrae l'audio dai video e lo trascrive in italiano con timestamp.

Pensato per macchine senza CUDA: faster-whisper su CPU in int8.

Dipendenze:
    pip install faster-whisper
    ffmpeg nel PATH

Uso:
    python tools/02_trascrivi.py                     # tutti i video in ./video
    python tools/02_trascrivi.py --model large-v3    # modello più accurato, più lento
    python tools/02_trascrivi.py --solo IMG_0042.mp4

Output per ogni video, in lavorazione/trascrizioni/:
    <nome>.json   segmenti con start/end in secondi + parole con timestamp
    <nome>.md     testo leggibile con marcatori [mm:ss] ogni segmento
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_EXT = {'.mp4', '.mov', '.m4v', '.avi', '.mkv', '.insv'}
# Termini del gergo: aiutano il modello a non storpiarli.
PROMPT = (
    "Rigging di una highline: ancoraggio, fettuccia, braca, grillo, softshackle, "
    "maglia rapida, weblock, softrelease, tagline, fishingline, backup, masterpoint, "
    "leash, Microtrax, Tibloc, Grigri, spit, fix, placchetta, clessidra, sosta, "
    "equalizzazione, tensione, carrucola, paranco, moschettone, corda statica."
)


def mmss(s):
    return '%d:%02d' % (int(s) // 60, int(s) % 60)


def _ffmpeg_disponibile():
    return shutil.which('ffmpeg') is not None


def _estrai_audio_pyav(video: Path, dest: Path):
    """Estrazione audio senza il binario ffmpeg: PyAV porta con sé le librerie.

    Serve sulle macchine dove ffmpeg non è installato nel PATH. Produce lo
    stesso wav 16 kHz mono PCM che produrrebbe la riga di comando.
    """
    import av
    with av.open(str(video)) as src:
        if not any(s.type == 'audio' for s in src.streams):
            raise RuntimeError('nessuna traccia audio in %s' % video.name)
        with av.open(str(dest), mode='w', format='wav') as out:
            osx = out.add_stream('pcm_s16le', rate=16000)
            osx.layout = 'mono'
            resampler = av.audio.resampler.AudioResampler(
                format='s16', layout='mono', rate=16000)
            for frame in src.decode(audio=0):
                frame.pts = None
                for r in resampler.resample(frame):
                    for pkt in osx.encode(r):
                        out.mux(pkt)
            for pkt in osx.encode(None):
                out.mux(pkt)


def estrai_audio(video: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1024:
        print('  audio già presente, salto')
        return dest
    if _ffmpeg_disponibile():
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', str(video),
               '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(dest)]
        subprocess.run(cmd, check=True)
    else:
        _estrai_audio_pyav(video, dest)
    return dest


def trascrivi(audio: Path, model, out_dir: Path, nome: str):
    segments, info = model.transcribe(
        str(audio), language='it', word_timestamps=True,
        initial_prompt=PROMPT, vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=700))

    dati = {'file': nome, 'durata': info.duration, 'segmenti': []}
    righe = ['# Trascrizione — %s' % nome, '',
             '_Durata: %s. Timestamp riferiti a questo video._' % mmss(info.duration), '']

    for seg in segments:
        parole = [{'w': w.word.strip(), 't': round(w.start, 2)}
                  for w in (seg.words or [])]
        dati['segmenti'].append({
            'start': round(seg.start, 2), 'end': round(seg.end, 2),
            'testo': seg.text.strip(), 'parole': parole})
        righe.append('**[%s]** %s' % (mmss(seg.start), seg.text.strip()))
        print('    [%s] %s' % (mmss(seg.start), seg.text.strip()[:70]))

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / (nome + '.json')).write_text(
        json.dumps(dati, ensure_ascii=False, indent=1), encoding='utf-8')
    (out_dir / (nome + '.md')).write_text('\n\n'.join(righe), encoding='utf-8')
    print('  -> %s.json  +  %s.md  (%d segmenti)' % (nome, nome, len(dati['segmenti'])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video-dir', default='video')
    ap.add_argument('--out', default='lavorazione/trascrizioni')
    ap.add_argument('--audio-dir', default='lavorazione/audio')
    ap.add_argument('--model', default='medium',
                    help='tiny, base, small, medium (default), large-v3')
    ap.add_argument('--solo', default=None, help='trascrivi un solo file')
    ap.add_argument('--threads', type=int, default=0,
                    help='thread CPU (0 = metà dei core logici)')
    args = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit('Manca faster-whisper:  pip install faster-whisper')

    video = sorted(p for p in Path(args.video_dir).rglob('*')
                   if p.suffix.lower() in VIDEO_EXT)
    if args.solo:
        video = [p for p in video if p.name == args.solo]
    if not video:
        sys.exit('Nessun video trovato in %s' % args.video_dir)

    print('Carico il modello "%s" su CPU (int8)...' % args.model)
    thr = args.threads or max(1, os.cpu_count() // 2)
    print('  %d thread CPU' % thr)
    model = WhisperModel(args.model, device='cpu', compute_type='int8',
                         cpu_threads=thr)

    for i, v in enumerate(video, 1):
        nome = v.stem
        print('\n[%d/%d] %s' % (i, len(video), v.name))
        wav = estrai_audio(v, Path(args.audio_dir) / (nome + '.wav'))
        trascrivi(wav, model, Path(args.out), nome)

    print('\nFatto. Trascrizioni in %s' % args.out)
    print('Prossimo passo: leggere le trascrizioni e scrivere NOTE_RIGGING.md.')


if __name__ == '__main__':
    main()
