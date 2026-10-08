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
ANCO = RADICE / 'lavorazione' / 'ancoraggi' / 'anfiteatro-53'

LINEA = HexColor(0xF97316)
C_ANC = LC[1]                   # ancoraggio      (rosso)
C_SOS = LC[7]                   # sosta / slinga  (azzurro)
C_TEN = LC[3]                   # lato tensione   (ambra)
C_ASL = LC[5]                   # anti-slip       (verde)

DC = '<font color="#B3261E">[DA CONFERMARE]</font>'
DCC = '[DA CONF.]'

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
    p = next((c / nome for c in (FOTO, ANN, DETT, ANCO) if (c / nome).exists()),
             FOTO / nome)
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


# ---------------------------------------------------------------- dove sta
# Estremi della 53 m nel render i-pietra dell'Anfiteatro, come frazioni
# dell'immagine. Trovati per colore — i-pietra disegna la 53 m in arancio
# #f97316, lo stesso colore che le da' nel catalogo — e verificati a vista:
# l'etichetta «Anfiteatro – 53m» poggia su quella linea e non su un'altra.
# Su un render 1354 x 884 sono i pixel (476, 299) e (840, 337).
# Se il render viene riesportato vanno ritrovati: python build/scheda_53.py
ESTREMI_53 = ((476 / 1354, 299 / 884), (840 / 1354, 337 / 884))
# porzione del render da mostrare: sinistra, alto, destra, basso
RITAGLIO_53 = (0.20, 0.16, 0.82, 0.62)
ARANCIO_IPIETRA = (249, 115, 22)


def figura_posizione():
    """Il render dell'Anfiteatro ritagliato sulla 53 m, con i due ancoraggi cerchiati.

    I due estremi non portano il nome del lato: quale dei due sia il lato
    tensione il render non lo dice, e la didascalia lo dichiara.
    """
    from PIL import Image, ImageDraw
    from schede_linee import render_di
    import panoramica_settori as PS
    sorgente = render_di('Anfiteatro')
    if sorgente is None:
        return None
    out = PS.DEST / 'anfiteatro_53.jpg'
    fonti = [sorgente, Path(__file__), RADICE / 'build' / 'panoramica_settori.py']
    if out.exists() and out.stat().st_mtime >= max(f.stat().st_mtime for f in fonti):
        return out
    im = Image.open(sorgente).convert('RGB')
    W0, H0 = im.size
    l, t, r, b = [int(v * m) for v, m in zip(RITAGLIO_53, (W0, H0, W0, H0))]
    k = 2                                   # il render e' piccolo: si ingrandisce
    im = im.crop((l, t, r, b)).resize(((r - l) * k, (b - t) * k), Image.LANCZOS)
    velo = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(velo)
    px = max(18, int(im.size[0] / 42))
    punti = [((fx * W0 - l) * k, (fy * H0 - t) * k) for fx, fy in ESTREMI_53]
    pastiglie = [(x + verso * px * 2.4, y - px * 3.4)
                 for (x, y), verso in zip(punti, (-1, 1))]
    for (x, y), (cx, cy) in zip(punti, pastiglie):
        d.line([(cx, cy), (x, y)], fill=(255, 255, 255, 200), width=max(5, px // 4))
        d.line([(cx, cy), (x, y)], fill=ARANCIO_IPIETRA + (255,), width=max(2, px // 8))
    for x, y in punti:
        R = px * 0.8
        d.ellipse([x - R, y - R, x + R, y + R], outline=(255, 255, 255, 240),
                  width=max(4, px // 5))
        R2 = R * 0.78
        d.ellipse([x - R2, y - R2, x + R2, y + R2], outline=ARANCIO_IPIETRA + (255,),
                  width=max(3, px // 7))
    for cx, cy in pastiglie:
        PS._pastiglia(d, (cx, cy), 'ancoraggio', ARANCIO_IPIETRA, px)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB').save(
        out, 'JPEG', quality=90, optimize=True, progressive=True)
    return out


# ---------------------------------------------------------------- la scheda
C_SETTORE = LC[2]                       # Anfiteatro, come nel catalogo
MAPPA = 'https://www.google.com/maps?q=44.419869,10.412353'
# L'altro capo: dieci letture del 22/08/2026 entro 3 m, a 51,5 m dal main.
MAPPA_S = 'https://www.google.com/maps?q=44.419453,10.412072'


def parte_53():
    """La scheda della 53 m, sul modello della guida Sillschlucht.

    Qui sta tutto cio' che e' proprio di questa linea, e nella parte 2 non c'e'
    piu': dove corre, i due ancoraggi con posizione e materiale, l'elenco
    completo del materiale con le quantita', l'A-frame con le sue misure, quale
    lato e' quale, che cosa manca, la variante con i bungee.
    """
    S = [Accent(C_SETTORE, 'Anfiteatro 53 m'),
         Segna('cap53'),
         KeepTogether([
             TestataLinea('AN', 'Anfiteatro 53 m', 'Detta «la 50» · A-frame sul lato tensione',
                          53, C_SETTORE),
             SP(10),
             P('La linea che sul campo chiamano <b>«la 50»</b>: da non confondere con la 50 m '
               'del Settore Giallo. Come si monta una linea è descritto nella parte 2; qui c’è '
               'com’è fatta questa.', lead)]),
         SP(12)]

    # ------------------------------------------------ dove corre
    fig = figura_posizione()
    if fig is not None:
        with _PILImage.open(fig) as _im:
            _ow, _oh = _im.size
        S.append(KeepTogether([
            PhotoStrip(str(fig), FW, _ow, _oh,
                       'Dove corre la 53 m nella vista i-pietra dell’Anfiteatro: '
                       'i due cerchi sono gli ancoraggi', C_SETTORE),
            SP(4),
            P('Quale dei due sia l’ancoraggio di tensione: ' + DC + '.', small)]))
        S.append(SP(14))

    # ------------------------------------------------ i due ancoraggi
    # NOTE_RIGGING, «Materiale nominato» e sezioni A-F; lati: dubbio 56.
    # Coordinate: IMG_1416 (16/05, main) e IMG_3323-3332 (22/08, l'altro capo).
    S.append(two_cols(
        gear_block('T · Ancoraggio di tensione', [
            'Sosta main: slinghe viola — quante e quanto lunghe ' + DC,
            'Sosta backup: corde rosa, collegate con 1 BFK',
            '1 weblock («banana») con grillo a lira',
            '1 paranchino di tensionamento della base',
            'Blocco del backup su sosta main e sosta backup',
            'A-frame: 2 pali di legno tondo sul bordo',
        ], C_TEN, coord='44.419869 · 10.412353 · 1025 m', url=MAPPA),
        gear_block('S · Ancoraggio statico', [
            '3 placchette su bullone',
            '1 corda verde acqua fra i punti',
            'Slinga viola e carrucola bloccante',
            '1 corda azzurra: linea vita',
            'Sosta backup — com’è fatta ' + DC,
        ], C_ANC, coord='44.419453 · 10.412072 · 1025 m', url=MAPPA_S)))
    S.append(SP(10))
    S.append(P('Le coordinate sono quelle registrate dal telefono stando agli ancoraggi: '
               'servono ad avvicinarsi, non a ritrovare il singolo punto, che va cercato a vista. '
               'Le due posizioni distano circa 51 m, coerente con i 53 m della linea: non è una '
               'misura.', small))
    S.append(PageBreak())

    # ------------------------------------------------ il materiale di questa linea
    # NOTE_RIGGING, «Materiale nominato», con la colonna «dove si usa». La parte
    # 2 dice che cosa serve per funzione; qui ci sono le quantita' della 53 m.
    S.append(Segna('materiale53'))
    S.append(KeepTogether([
        P('<b>Il materiale del montaggio del 16 maggio</b>', h3),
        SP(6),
        data_table(
            ['Qtà', 'Articolo', 'Dove si usa', 'Misura'],
            [['n.d.', 'Slinghe viola — brache ad anello industriali', 'sosta main', DCC],
             ['n.d.', 'Corde rosa', 'sosta backup', DCC],
             ['1', 'BFK, moschettone d’acciaio grande', 'sulla corda rosa del backup', DCC],
             ['4', 'Maglie rapide delta', DCC, DCC],
             ['1', '«Mighty Lock», «quello quadratino» — nome incerto', 'backup', DCC],
             ['1', 'Slinga verde lunga, «la più grossa che c’è»', DCC, DCC],
             ['1', 'Slinga piccola viola', DCC, DCC],
             ['≥1', 'Slinga verde e nera', DCC, DCC],
             ['1', 'Corda azzurra', 'tagline, poi linea vita', DCC],
             ['1', 'Corda verde acqua', 'collegamento fra i punti', DCC],
             ['≥1', 'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm', 'sull’ancoraggio',
              'marca ' + DCC],
             ['1', 'Weblock azzurro anodizzato, detto «banana»', 'lato tensione',
              'modello ' + DCC],
             ['≥1', 'Grillo a lira in acciaio', 'collegamento della sosta', DCC],
             ['1', 'Paranchino', 'tensionamento della base', DCC],
             ['1', 'Softrelease', DCC, 'modello ' + DCC],
             ['≥2', 'Grigri', 'backup e calata', '—'],
             ['1', 'Corda di backup', 'per chi lavora in sosta', DCC],
             ['n.d.', 'Nastro, backup della linea, leash', '—', DCC]],
            [36, 222, 142, 91], C_SETTORE)]))
    S.append(SP(14))
    S.append(foto('IMG_1360.jpg', FW, 'Il materiale steso prima del montaggio, 16 maggio 2026',
                  C_SETTORE, ratio=0.34, focus=0.42))
    S.append(PageBreak())

    # ------------------------------------------------ fotografie dei due lati
    S.append(photo_pair(
        str(FOTO / 'IMG_1416.jpg'), str(ANCO / 'IMG_3329.jpg'),
        'Lato tensione: l’A-frame visto dall’ancoraggio', 'Lato statico: placchette e slinghe',
        *dim(FOTO / 'IMG_1416.jpg'), color=C_SETTORE, ratio=0.82, focus=0.6,
        ow2=dim(ANCO / 'IMG_3329.jpg')[0], oh2=dim(ANCO / 'IMG_3329.jpg')[1]))
    S.append(SP(16))
    # Le due fotografie in opera affiancate a mezza colonna: una sola a tutta
    # larghezza scivolava su una pagina in piu', e tagliata a striscia perdeva la
    # persona sulla linea, che sta al centro di una foto verticale.
    S.append(photo_pair(
        str(FOTO / 'IMG_1401.jpg'), str(FOTO / 'IMG_1398.jpg'),
        'La linea in opera, percorsa con il leash', 'La campata vista dal bordo',
        *dim(FOTO / 'IMG_1401.jpg'), color=C_SETTORE, ratio=0.68, focus=0.55,
        ow2=dim(FOTO / 'IMG_1398.jpg')[0], oh2=dim(FOTO / 'IMG_1398.jpg')[1]))
    S.append(SP(16))
    # ------------------------------------------------ l'A-frame di questa linea
    # IMG_1396 e IMG_1416; posizione sul lato main dalla risposta del 20/08
    S.append(KeepTogether([
        P('<b>L’A-frame di questa linea</b>', h3),
        SP(6),
        ChipRow([('Pali', '2 · legno tondo'), ('Testa', 'Incrociata e legata'),
                 ('Piede', 'Appoggiato su roccia'), ('Altezza', DCC)], C_TEN),
        SP(10),
        two_cols(
            gear_block('Com’è fatto', [
                'Due pali di legno tondo, incrociati e legati in testa',
                'Fettuccia viola avvolta sulla testa dei pali',
                'Corda verde fluo, fettuccia blu e corda rosa in testa',
                'Piedi appoggiati sulla roccia del bordo',
                'Giri di filo metallico attorno al piede di un palo',
            ], C_TEN),
            gear_block('Ancora da rilevare', [
                'Altezza dei pali — ' + DCC,
                'Diametro e tipo del legno — ' + DCC,
                'Come sono legati in testa — ' + DCC,
                'Se i piedi sono fermati o solo appoggiati — ' + DCC,
                'Se il filo metallico tiene il palo o è un recinto — ' + DCC,
                'Di quanto solleva la linea sopra il bordo — ' + DCC,
            ], WARN))]))
    S.append(SP(16))
    S.append(callout('Quale lato è quale',
                     'In questa scheda la tensione sta dove stanno sosta main, sosta backup e '
                     'A-frame, e la sosta su tre punti è sul lato statico. È ricostruito '
                     'dall’ordine delle operazioni del 16 maggio, e va confermato: ' + DC + '.',
                     C_TEN))
    S.append(SP(16))
    S.append(data_table(
        ['Voce', 'Valore'],
        [['Lunghezza', '53 m di catalogo (i-pietra e locandina) — misura sui punti ' + DC],
         ['Dislivello, offlevel', DC],
         ['Nastro, backup, leash', DC],
         ['Montaggi documentati', '16 maggio 2026; 22 agosto 2026, con i bungee']],
        [150, FW - 150], C_SETTORE))
    S.append(SP(14))
    S.append(KeepTogether([
        P('<b>Ancora da rilevare su questa linea</b>', h3),
        SP(5),
        BU('Quale dei due estremi è l’ancoraggio di tensione.', C_SETTORE),
        BU('La lunghezza, misurata sui punti, e il dislivello.', C_SETTORE),
        BU('I punti dell’ancoraggio di tensione: quanti e di che tipo.', C_SETTORE),
        BU('Una fotografia d’insieme dei tre punti, per l’angolo di apertura.', C_SETTORE),
        BU('Diametro e marca del bullone; marca della carrucola bloccante.', C_SETTORE),
        BU('Se accanto ai punti fissi c’è protezione veloce.', C_SETTORE),
        BU('L’etichetta delle slinghe: c’è, ma nelle fotografie è rivoltata.', C_SETTORE)]))
    S.append(SP(18))

    # ------------------------------------------------ la variante con i bungee
    # IMG_3323-3332, 22/08/2026, all'altro capo della linea (51,5 m dal main).
    # L'utente: «il montaggio fatto quel giorno era della 53 ma con i bungee».
    # Le placchette sono fisse e valgono per ogni montaggio; slinghe, corda verde,
    # fettucce rosse e bungee sono di quel giorno.
    S.append(KeepTogether([
        P('<b>La stessa linea, montata con i bungee</b>', h3),
        SP(5),
        P('Il 22 agosto 2026 la 53 m è stata montata con i <b>bungee</b>. Le fotografie sono '
          'state scattate all’ancoraggio statico: si vedono le placchette su bullone, le '
          'slinghe viola che portano al masterpoint e la corda annodata fra i punti. Il '
          'materiale di questa variante è ' + DC + '.', body),
        SP(10),
        photo_pair(
            str(ANCO / 'IMG_3324.jpg'), str(ANCO / 'IMG_3325.jpg'),
            'Placchette, slinghe viola e corda annodata', 'Dal masterpoint ai bungee',
            *dim(ANCO / 'IMG_3324.jpg'), color=C_SETTORE, ratio=0.95, focus=0.45,
            ow2=dim(ANCO / 'IMG_3325.jpg')[0], oh2=dim(ANCO / 'IMG_3325.jpg')[1])]))
    S.append(PageBreak())
    return S


if __name__ == '__main__':
    # Diagnostica: dove stanno i pixel arancio della 53 m nel render. Da usare
    # se il render viene riesportato e ESTREMI_53 va aggiornato.
    import numpy as np
    from PIL import Image
    from schede_linee import render_di
    f = render_di('Anfiteatro')
    a = np.asarray(Image.open(f).convert('RGB')).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ys, xs = np.nonzero((r > 200) & (g > 70) & (g < 160) & (b < 80) & (r - g > 80))
    print('render %s: %d x %d' % (f.name, a.shape[1], a.shape[0]))
    if len(xs):
        print('pixel arancio: %d, x %d-%d, y %d-%d' % (len(xs), xs.min(), xs.max(),
                                                       ys.min(), ys.max()))
        print('estremo sinistro ~ (%d, %d), destro ~ (%d, %d)' % (
            xs.min(), ys[xs.argmin()], xs.max(), ys[xs.argmax()]))
