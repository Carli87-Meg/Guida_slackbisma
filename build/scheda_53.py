# -*- coding: utf-8 -*-
"""Scheda della linea documentata: Anfiteatro, 53 m — «la 50».

Fino all'edizione dell'8 ottobre questo modulo era un capitolo intitolato alla
giornata del 16 maggio, che raccontava il montaggio in ordine di ripresa. Il
metodo ora sta in metodo.py, ordinato come lo si esegue; qui resta cio' che e'
proprio di questa linea: dove sta, quanto e' lunga, com'e' ancorata, che cosa
manca. E' il modello della scheda che avranno le altre ventitre' linee quando
verranno documentate.

Il modulo tiene anche le costanti e la funzione foto() usate dal metodo, che
lavora sulle stesse fotografie.

    from scheda_53 import parte_53
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import PageBreak, KeepTogether                            # noqa: E402
from PIL import Image as _PILImage                                  # noqa: E402

ANN = RADICE / 'lavorazione' / 'frame_annotati'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'
DETT = RADICE / 'lavorazione' / 'dettagli'

LINEA = HexColor(0xF97316)
C_ANC = LC[1]                   # ancoraggio      (rosso)
C_SOS = LC[7]                   # sosta / slinga  (azzurro)
C_TEN = LC[3]                   # lato tensione   (ambra)
C_ASL = LC[5]                   # anti-slip       (verde)

DC = '<font color="#B3261E">[DA CONFERMARE]</font>'

# occhiello ripetuto su ogni testata: la linea e il giorno, sempre
GIORNO = '16/05/2026'


def _occh(fase):
    return 'Anfiteatro 53 m · %s · %s' % (fase, GIORNO)


def dim(p):
    with _PILImage.open(p) as im:
        return im.size


def foto(nome, w, cap, color=None, ratio=None, focus=0.5):
    # tre cartelle, un nome solo: foto raddrizzate, frame annotati, ritagli di
    # dettaglio. Cosi' chi scrive una pagina non deve sapere dove sta il file.
    p = next((c / nome for c in (FOTO, ANN, DETT) if (c / nome).exists()), FOTO / nome)
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


def parte_53():
    """La scheda della 53 m: dati della linea, posizione, fotografie in opera."""
    S = [Accent(LINEA, 'Anfiteatro 53 m'),
         Segna('cap53'),
         KeepTogether([
             LineHeader('', 'Anfiteatro · 53 m', '«la 50» · la linea documentata', LINEA),
             SP(10),
             P('La linea che sul campo chiamano <b>«la 50»</b>: da non confondere con la '
               '50 m del Settore Giallo. È la linea su cui è documentato il metodo della '
               'parte 2, montata il 16 maggio 2026.', lead),
             SP(10),
             ChipRow([('Settore', 'Anfiteatro'), ('Lunghezza', '53 m · catalogo'),
                      ('Ancoraggi', 'Roccia, due lati'), ('A-frame', 'Lato tensione')],
                     LINEA)]),
         SP(14)]
    # NOTE_RIGGING, «Quadro generale»; GPS dall'EXIF di IMG_1416, 17:14:38
    S.append(data_table(
        ['Voce', 'Valore'],
        [['Lunghezza', '53 m di catalogo (i-pietra e locandina) — misura sui punti '
          + DC],
         ['Dislivello, offlevel', DC],
         ['Lato tensione', 'Sosta main e sosta backup, A-frame sul bordo — numero e tipo '
          'dei punti ' + DC],
         ['Lato opposto', 'Sosta su tre punti, placchette su bullone collegate con corda '
          'annodata'],
         ['Ancoraggio main', '44.419869, 10.412353 · quota 1025 m'],
         ['Ancoraggio opposto', 'Posizione ' + DC],
         ['Nastro, backup, leash', DC],
         ['Ultimo montaggio documentato', '16 maggio 2026']],
        [150, FW - 150], LINEA))
    S.append(SP(12))
    S.append(callout('Una posizione, non un rilievo',
                     'La coordinata è quella registrata dal telefono stando all’ancoraggio '
                     'main, con la precisione di un GPS sotto una parete: serve ad avvicinarsi, '
                     'non a ritrovare il singolo punto, che va cercato a vista.', LINEA))
    S.append(SP(14))
    S.append(KeepTogether([
        P('<b>Ancora da rilevare su questa linea</b>', h3),
        SP(5),
        BU('La lunghezza, misurata sui punti.', LINEA),
        BU('Il dislivello fra i due ancoraggi.', LINEA),
        BU('I punti del lato tensione: quanti e di che tipo.', LINEA),
        BU('Una fotografia d’insieme dei tre punti del lato opposto, per l’angolo di '
           'apertura.', LINEA),
        BU('L’etichetta delle slinghe, distesa e leggibile.', LINEA),
        BU('La posizione dell’ancoraggio opposto.', LINEA)]))
    S.append(SP(14))
    S.append(KeepTogether([
        foto('IMG_1401.jpg', FW, 'La linea in opera, percorsa con il leash', LINEA,
             ratio=0.62, focus=0.5)]))
    S.append(SP(14))
    S.append(foto('IMG_1398.jpg', FW, 'La campata vista dal bordo', LINEA,
                  ratio=0.56, focus=0.5))
    S.append(PageBreak())
    return S
