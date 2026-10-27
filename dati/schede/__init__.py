# -*- coding: utf-8 -*-
"""Le schede di dati delle linee: un file per linea, chiamato con il suo id.

Una scheda e' un dizionario `SCHEDA` dentro `dati/schede/<id>.py` con tutto cio'
che e' proprio di quella linea: coordinate, ancoraggi, materiale, A-frame,
varianti, che cosa manca. Il build (`build/scheda_linea.py`) la impagina
mostrando solo le sezioni che hanno dati; il registro (`dati/linee.py`) ne ricava
il livello di documentazione:

* `montaggi` non vuoto  -> documentata (riprese, fotogrammi, dubbi chiusi);
* `rilievo` non vuoto   -> rilevata (scheda di rilievo compilata sul campo).

Documentare una linea nuova significa scrivere il suo file qui, non toccare il
build. Il modello e' `anfiteatro-53.py`, con il commento che spiega ogni campo.

    import schede
    schede.di('anfiteatro-53')['tensione']['coord']
"""
import importlib.util
from pathlib import Path

QUI = Path(__file__).resolve().parent
_CACHE = {}


def _carica(id_linea):
    f = QUI / ('%s.py' % id_linea)
    if not f.exists():
        return None
    # il nome del file ha i trattini: si carica dal percorso, non con import
    spec = importlib.util.spec_from_file_location(
        'scheda_%s' % id_linea.replace('-', '_'), f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    s = dict(mod.SCHEDA)
    s.setdefault('id', id_linea)
    return s


def di(id_linea):
    """La scheda della linea, o None se non esiste."""
    if id_linea not in _CACHE:
        _CACHE[id_linea] = _carica(id_linea)
    return _CACHE[id_linea]


def tutte():
    """Gli id delle linee che hanno una scheda."""
    return sorted(f.stem for f in QUI.glob('*.py') if f.stem != '__init__')
