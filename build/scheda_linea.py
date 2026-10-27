# -*- coding: utf-8 -*-
"""La scheda di una linea, impaginata dal suo dizionario di dati.

Una scheda sola per tutte le linee: legge `dati/schede/<id>.py` e stampa le
sezioni per cui esistono dati. Il livello di documentazione (dati/linee.py)
decide la forma:

* **documentata** o **rilevata**: la scheda completa, sul modello della guida
  Sillschlucht — testata, pastiglie, dove corre, i due ancoraggi con le coordinate,
  il materiale, l'A-frame, le fotografie, le varianti, che cosa manca;
* **fotografata**: una scheda a mezza colonna — la fotografia, tre righe su cio'
  che si vede, il rimando alla scheda di rilievo;
* **censita**: nessuna scheda, solo la riga nella tabella del settore.

Fino all'edizione 0.3 la 53 m era un modulo a parte (build/scheda_53.py) con i
dati dentro il codice: documentare una seconda linea avrebbe voluto dire
copiarlo. Ora si scrive il file di dati e basta.

Qui stanno anche le costanti condivise con il metodo e con il catalogo: i colori
dei settori e dei due lati, i marcatori, la ricerca delle fotografie e dei render.

    python build/scheda_linea.py anfiteatro-53     # diagnostica del render
"""
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import (PageBreak, KeepTogether, Table,     # noqa: E402
                                TableStyle, Paragraph, Spacer, CondPageBreak)
from PIL import Image as _PILImage                                  # noqa: E402

import linee as REG                                                 # noqa: E402
import file_lineebisma as FC                                        # noqa: E402

ANN = RADICE / 'lavorazione' / 'frame_annotati'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'
DETT = RADICE / 'lavorazione' / 'dettagli'
ANCO = RADICE / 'lavorazione' / 'ancoraggi'
FOTO_LINEE = REG.FOTO_LINEE
RENDER_IPIETRA = RADICE / 'fonti' / 'render_ipietra'
_ESTENSIONI = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

# ---------------------------------------------------------------- colori
LINEA = HexColor(0xF97316)      # il colore che i-pietra assegna alla 53 m: accento della guida

# un colore per settore, coerente in tutta la guida (catalogo, schede, fascicolo)
C_AREA = {
    'Rookie':         LC[6],
    'Settore Giallo': LC[4],
    'Anfiteatro':     LC[2],
    'Anfite-altro':   LC[1],
    'Despedida':      LC[7],
}

# I due lati di una linea, uguali nel metodo e in ogni scheda. Fino alla 0.3 il
# lato statico era rosso LC[1], lo stesso dell'Anfite-altro, e le soste azzurre
# LC[7], lo stesso della Despedida: due sistemi di colore sulla stessa tavolozza.
C_TEN = LC[3]                   # lato tensione: ambra, nessun settore lo usa
C_STA = BRAND                   # lato statico: il blu scuro del sistema grafico
C_MET = BRAND                   # la parte del metodo

# i livelli di documentazione, per le pastiglie di stato
C_LIVELLO = {
    REG.CENSITA: MUT,
    REG.FOTOGRAFATA: HexColor(0xB07A18),
    REG.RILEVATA: HexColor(0x5B7F9A),
    REG.DOCUMENTATA: LC[5],
}

# ---------------------------------------------------------------- marcatori
# Due marcatori, spiegati in «Come leggere questa guida»:
#   [DA CONFERMARE]  in rosso: dato incerto o contraddetto da un'altra fonte;
#   da rilevare      in grigio: dato non raccolto (nelle tabelle, cella vuota).
# Il testo dei dati li scrive in chiaro; qui si colorano.
DC = '[DA CONFERMARE]'
DR = 'da rilevare'
_RE_DC = re.compile(r'\[DA[  ]CONF(?:ERMARE|\.)[^\]]*\]')
_RE_DR = re.compile(r'(?<![\w>])da rilevare(?![\w<])')


def marca(t):
    """Colora i marcatori dentro un testo con markup ReportLab."""
    if not t:
        return t
    t = _RE_DC.sub(lambda m: '<font color="#%s">%s</font>'
                   % (WARN.hexval()[2:], m.group(0).replace('[DA CONF', '[DA CONF')), t)
    t = _RE_DR.sub('<font color="#%s">da rilevare</font>' % MUT.hexval()[2:], t)
    return t


def T(t, s=body):
    """Paragrafo con i marcatori colorati."""
    return P(marca(t), s)


def BUm(t, c=MUT):
    return BU(marca(t), c)


def stato_chip(l):
    """La pastiglia di stato di una linea: il nome del livello nel suo colore."""
    liv = REG.livello(l)
    return livello_chip(REG.LIVELLI[liv][0], C_LIVELLO[liv])


# ---------------------------------------------------------------- immagini
def dim(p):
    with _PILImage.open(p) as im:
        return im.size


def trova_foto(nome, id_linea=None):
    """Il file di una fotografia, in qualunque cartella di lavorazione stia.

    Foto raddrizzate, fotogrammi annotati, ritagli di dettaglio, foto degli
    ancoraggi e foto delle linee (queste due per linea): chi scrive una scheda
    indica il nome, non il percorso.
    """
    cartelle = [FOTO, ANN, DETT]
    if id_linea:
        cartelle += [ANCO / id_linea, FOTO_LINEE / id_linea]
    for c in cartelle:
        if (c / nome).exists():
            return c / nome
    return FOTO / nome


def foto(nome, w, cap, color=None, ratio=None, focus=0.5, id_linea=None):
    p = trova_foto(nome, id_linea)
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


def coppia(f1, c1, f2, c2, ratio=None, focus=0.5, color=None, id_linea=None):
    p1, p2 = trova_foto(f1, id_linea), trova_foto(f2, id_linea)
    return photo_pair(str(p1), str(p2), c1, c2, *dim(p1), color=color, ratio=ratio,
                      focus=focus, ow2=dim(p2)[0], oh2=dim(p2)[1])


def _norm(t):
    """Minuscolo e senza separatori: «Anfite-altro» e «anfite_altro» coincidono."""
    return ''.join(c for c in t.lower() if c.isalnum())


def _cartella_render():
    """La cartella dei render, comunque sia scritta (Windows non distingue le maiuscole)."""
    if RENDER_IPIETRA.is_dir():
        return RENDER_IPIETRA
    base = RENDER_IPIETRA.parent
    if base.is_dir():
        atteso = _norm(RENDER_IPIETRA.name)
        for d in sorted(base.iterdir()):
            if d.is_dir() and _norm(d.name) == atteso:
                return d
    return None


def render_di(area):
    """Render i-pietra del settore, se qualcuno l'ha esportato.

    Basta che il nome del file contenga il nome del settore: non si puo'
    pretendere che un export sia rinominato a mano.
    """
    d = _cartella_render()
    if d is None:
        return None
    bersaglio = _norm(area)
    trovati = sorted(f for f in d.iterdir()
                     if f.suffix.lower() in _ESTENSIONI and bersaglio in _norm(f.stem))
    return trovati[0] if trovati else None


def figura_posizione(s, l):
    """Il render del settore ritagliato sulla linea, con i due capi cerchiati.

    I due estremi non portano il nome del lato: quale sia il lato tensione il
    render non lo dice, e lo dice la nota sotto la figura, se qualcuno l'ha
    dichiarato.
    """
    pos = s.get('posizione')
    if not pos:
        return None
    from PIL import Image, ImageDraw
    import panoramica_settori as PS
    sorgente = render_di(pos['render'])
    if sorgente is None:
        return None
    out = PS.DEST / ('posizione_%s.jpg' % l['id'])
    fonti = [sorgente, REG.RADICE / 'dati' / 'schede' / ('%s.py' % l['id']), Path(__file__),
             RADICE / 'build' / 'panoramica_settori.py']
    if out.exists() and out.stat().st_mtime >= max(f.stat().st_mtime for f in fonti
                                                  if f.exists()):
        return out
    im = Image.open(sorgente).convert('RGB')
    W0, H0 = im.size
    l_, t_, r_, b_ = [int(v * m) for v, m in zip(pos['ritaglio'], (W0, H0, W0, H0))]
    k = 2                                   # il render e' piccolo: si ingrandisce
    im = im.crop((l_, t_, r_, b_)).resize(((r_ - l_) * k, (b_ - t_) * k), Image.LANCZOS)
    velo = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(velo)
    px = max(18, int(im.size[0] / 42))
    colore = tuple(pos.get('colore', (249, 115, 22)))
    punti = [((fx * W0 - l_) * k, (fy * H0 - t_) * k) for fx, fy in pos['estremi']]
    # La pastiglia sta di lato e sopra il punto; se cosi' uscirebbe dal ritaglio
    # si sposta dall'altra parte, o sotto. Prima «ancoraggio» usciva tagliata a
    # meta' sulle linee che arrivano al bordo del render (97 m, 113 m).
    IW, IH = im.size
    lw, lh = PS._misura(d, 'ancoraggio', px)
    pastiglie = []
    for (x, y), verso in zip(punti, (-1, 1)):
        candidati = [(x + v * px * 2.4, y + s * px * 3.4)
                     for s in (-1, 1) for v in (verso, -verso, 0)]
        scelto = None
        for cx, cy in candidati:
            if (cx - lw / 2 >= 6 and cx + lw / 2 <= IW - 6
                    and cy - lh / 2 >= 6 and cy + lh / 2 <= IH - 6):
                scelto = (cx, cy)
                break
        if scelto is None:
            scelto = (min(max(x, lw / 2 + 6), IW - lw / 2 - 6),
                      min(max(y - px * 3.4, lh / 2 + 6), IH - lh / 2 - 6))
        pastiglie.append(scelto)
    for (x, y), (cx, cy) in zip(punti, pastiglie):
        d.line([(cx, cy), (x, y)], fill=(255, 255, 255, 200), width=max(5, px // 4))
        d.line([(cx, cy), (x, y)], fill=colore + (255,), width=max(2, px // 8))
    for x, y in punti:
        R = px * 0.8
        d.ellipse([x - R, y - R, x + R, y + R], outline=(255, 255, 255, 240),
                  width=max(4, px // 5))
        R2 = R * 0.78
        d.ellipse([x - R2, y - R2, x + R2, y + R2], outline=colore + (255,),
                  width=max(3, px // 7))
    for cx, cy in pastiglie:
        PS._pastiglia(d, (cx, cy), 'ancoraggio', colore, px)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(im.convert('RGBA'), velo).convert('RGB').save(
        out, 'JPEG', quality=90, optimize=True, progressive=True)
    return out


# ---------------------------------------------------------------- la scheda completa
# Spazio fra due sezioni della scheda. Era 16 pt: la Brifing finiva con due righe
# sole su una pagina nuova.
STACCO = 12


def _h3(t):
    return P('<b>%s</b>' % t, h3)


# Titoletto di una sezione che puo' spezzarsi fra due pagine (il materiale, l'elenco
# di cio' che manca). Il titoletto h3 normale e' legato a cio' che segue
# (lega_testate) e trascinava con se' la tabella intera: con la tabella del materiale
# delle linee fotografate restava mezza pagina bianca. Questo va a capo solo se sotto
# non c'e' posto per qualche riga, poi lascia scorrere.
h3_flusso = ParagraphStyle('h3_flusso', parent=h3)


def _h3_flusso(t, almeno=110):
    return [CondPageBreak(almeno), P('<b>%s</b>' % t, h3_flusso), SP(5)]


def _blocco_lato(d, titolo_default, colore):
    return gear_block(d.get('titolo', titolo_default), [marca(v) for v in d.get('voci', [])],
                      colore, coord=d.get('coord'), url=d.get('url'))


# Le note che valgono per tutte le schede dalle fotografie. Fino all'edizione 0.4 si
# ripetevano in ognuna delle sei; ora stanno una volta in «Come leggere questa guida»
# (build_manuale.py), e la scheda rimanda li'.
def nota_slackmap():
    import slackmap as SM
    return ('Le coordinate dei capi sono quelle del segmento disegnato sulla mappa di '
            '<b>SlackMap</b>, letta il %s: <b>non sono misure</b>. Sulla 53 m risultano '
            'spostate di 10-19 m verso ovest rispetto alle letture del telefono fatte agli '
            'ancoraggi. Servono ad avvicinarsi, non a trovare un punto; l’ordine dei capi è '
            'quello di SlackMap e non dice quale sia il lato di tensione. Ogni coordinata '
            'stampata è un link che apre il punto in i-pietra.' % SM.LETTO_IL)


NOTA_FILE = ('Le parole del <b>file del gruppo</b> vengono dal file LineeBisma (20/10/2026), '
             'che segna tutto «da controllare»: sono proposte, non rilievi. «Vicino» e '
             '«lontano» sono le sue colonne, non il lato tensione e il lato statico; che cosa '
             'misuri «Schetchy» il file non lo dice: forse quanto è complicato montare gli '
             'ancoraggi, o quanto fa paura camminare la linea [DA CONFERMARE].')

NOTA_FOTO = ('Il <b>materiale</b> di una linea fotografata è riconosciuto per forma, non per '
             'marca, salvo dove la marca si legge, e senza quantità né misure: le foto non le '
             'danno.')


def tabella_slackmap(l, col):
    """I due capi del segmento disegnato su SlackMap, con il link alla mappa.

    Non sono misure: sulla 53 m scartano di 10-19 m verso ovest dalle letture del
    telefono fatte stando agli ancoraggi. Servono ad avvicinarsi, non a trovare un
    punto, e non dicono quale capo sia il «vicino» del file o il lato di tensione.
    La nota per esteso sta in «Come leggere»; qui resta il rimando, perche' la guida
    dichiara che non sono misure ogni volta che le stampa.
    """
    import slackmap as SM
    v = l.get('slackmap')
    if not v:
        return []
    righe = []
    for k, (lat, lon) in enumerate(v['capi'], start=1):
        righe.append([Paragraph('Capo %d' % k, td),
                      Paragraph(A(SM.mappa(lat, lon), '%.5f · %.5f' % (lat, lon), col), td),
                      Paragraph('segmento disegnato su SlackMap, non misurato', td)])
    righe.append([Paragraph('Segmento', td),
                  Paragraph('%.1f m' % v['lunghezza_segmento'], td),
                  Paragraph(A(v['url'], 'scheda SlackMap «%s»' % (v['nome'] or v['id']), col)
                            + ', creata il %s' % v['creata'], td)])
    return [KeepTogether([
        _h3('Dove sono i capi, secondo SlackMap'),
        SP(5),
        data_table(['Capo', 'Coordinate', 'Che cosa sono'], righe, [60, 130, FW - 190], col),
        SP(5),
        T('Non sono misure: servono ad avvicinarsi, non a trovare un punto (%s).'
          % rif('leggere'), small)])]


def tabella_file_gruppo(l, col):
    """Le parole del file LineeBisma sulla riga di questa linea, cella per cella.

    Tutto cio' che il file scrive e' segnato dal file stesso «da controllare» (decisione
    D6): si stampa con le sue parole, senza tradurlo nel materiale della guida.
    """
    c = FC.di(l['id'])
    if c is None:
        return []

    def virg(t):
        return '«%s»' % t if t else '—'
    righe = []
    for lato in ('vicino', 'lontano'):
        schema = c[lato]
        detto = (('schema %s' % virg(schema)) if schema in FC.NOMI_SCHEMA else virg(schema))
        righe.append(['Lato «%s»' % lato, detto])
    if c['tipologia']:
        righe.append(['Tipologia', virg(c['tipologia'])])
    if c['note']:
        righe.append(['Note', virg(c['note'])])
    s_v, s_l = c['schetchy']
    if s_v or s_l:
        righe.append(['«Schetchy» (vicino / lontano)', '%s / %s' % (s_v or '—', s_l or '—')])
    p_v, p_l = c['persone']
    if p_v or p_l:
        righe.append(['Persone (vicino / lontano)', '%s / %s' % (virg(p_v), virg(p_l))])
    # a flusso: tenuta intera lasciava un quinto di pagina bianco sopra di se' (Brifing).
    # Che cosa sia il file, e che cosa valga, lo dice «Come leggere» (NOTA_FILE).
    return _h3_flusso('Che cosa dice il file del gruppo') + [
        data_table(['Voce', 'Con le parole del file'],
                   [[Paragraph(a, td), Paragraph(b, td)] for a, b in righe],
                   [150, FW - 150], col)]


def _figura_o_nota(s, l, col):
    fig = figura_posizione(s, l)
    if fig is not None:
        ow, oh = dim(fig)
        pos = s['posizione']
        b = [PhotoStrip(str(fig), FW, ow, oh, pos.get('didascalia', ''), col)]
        if pos.get('nota'):
            b += [SP(8), T(pos['nota'], small)]
        return [KeepTogether(b), SP(14)]
    if s.get('posizione_nota'):
        return [T(s['posizione_nota'], small), SP(12)]
    return []


def _foto_voce(v, col, id_):
    """Una voce di 'foto': una coppia (6 valori) o una foto sola (dizionario)."""
    if isinstance(v, dict):
        return foto(v['file'], FW, v.get('cap', ''), col, ratio=v.get('ratio'),
                    focus=v.get('focus', 0.5), id_linea=id_)
    f1, c1, f2, c2, ratio, focus = v
    return coppia(f1, c1, f2, c2, ratio, focus, col, id_)


def scheda_completa(l, s):
    """Scheda di una linea dal suo dizionario: solo le sezioni con dati.

    Ordine: testata e pastiglie, dove corre, i due lati, le coordinate di SlackMap,
    le parole del file, il materiale, le fotografie, l'A-frame, le varianti,
    l'avvertenza propria della linea, che cosa manca. Con 'foto_dopo_lati' (le
    schede dalle fotografie) le foto salgono subito sotto i lati che le descrivono.
    Il materiale, le parole del file e l'elenco di cio' che manca possono spezzarsi
    fra due pagine. I lati si chiamano
    «tensione» e «statico» solo quando qualcuno lo ha dichiarato ('tensione' e
    'statico' nella scheda); altrimenti portano i nomi che da' la scheda ('lato_a'
    e 'lato_b', per il file del gruppo «vicino» e «lontano») e un colore neutro.
    """
    col = C_AREA[l['settore']]
    id_ = l['id']
    sotto = REG.nome_catalogo(l)
    if s.get('occhiello'):
        sotto += ' · ' + s['occhiello']
    S = [Accent(col, REG.nome(l)), Segna('linea:%s' % id_)]
    blocco = [TestataLinea(l['codice'], REG.titolo(l), sotto, l['lunghezza'], col), SP(10)]
    if s.get('intro'):
        blocco.append(T(s['intro'], lead))
    if s.get('chips'):
        blocco += [SP(12), ChipRow([(a, marca_chip(b)) for a, b in s['chips']], col)]
    S.append(KeepTogether(blocco))
    S.append(SP(14))

    # ------------------------------------------------ dove corre
    S += _figura_o_nota(s, l, col)

    # ------------------------------------------------ i due lati
    ten, sta = s.get('tensione'), s.get('statico')
    a, b = s.get('lato_a'), s.get('lato_b')
    blocchi = []
    if ten:
        blocchi.append(_blocco_lato(ten, 'T · Ancoraggio di tensione', C_TEN))
    if sta:
        blocchi.append(_blocco_lato(sta, 'S · Ancoraggio statico', C_STA))
    if a:
        blocchi.append(_blocco_lato(a, 'Lato A', tint(col, 0.75)))
    if b:
        blocchi.append(_blocco_lato(b, 'Lato B', tint(col, 0.75)))
    if blocchi:
        S.append(DueColonne(*blocchi[:2]) if len(blocchi) >= 2 else blocchi[0])
        for extra in blocchi[2:]:
            S += [SP(10), extra]
        nota = s.get('nota_coordinate') or s.get('lati_nota')
        if nota:
            S += [SP(10), T(nota, small)]

    # ------------------------------------------------ fotografie, subito sotto i lati
    # Nelle schede dalle fotografie le colonne dei lati descrivono proprio queste
    # foto: stanno accanto. In coda, una coppia scivolava da sola su una pagina
    # quasi bianca (p. 14, 28, 35, 39 dell'edizione 0.4).
    if s.get('foto_dopo_lati'):
        for v in s.get('foto', []):
            S += [SP(12), _foto_voce(v, col, id_)]
    if s.get('pagina_dopo_lati'):
        S.append(PageBreak())
    else:
        S.append(SP(STACCO))

    # ------------------------------------------------ dove sono i capi, secondo SlackMap
    if s.get('slackmap'):
        S += tabella_slackmap(l, col) + [SP(STACCO)]

    # ------------------------------------------------ le parole del file del gruppo
    if s.get('file_gruppo'):
        S += tabella_file_gruppo(l, col) + [SP(STACCO)]

    # ------------------------------------------------ il materiale di questa linea
    mat = s.get('materiale')
    if mat:
        S.append(Segna('materiale:%s' % id_))
        colonne = mat.get('colonne', ['Qtà', 'Articolo', 'Dove si usa', 'Misura'])
        larghezze = mat.get('larghezze', [36, 222, 142, 91])
        righe = [[Paragraph(marca(str(x)), td) for x in r] for r in mat['righe']]
        tab = data_table(colonne, righe, larghezze, col)
        # righe piu' strette: con diciannove voci la fotografia del materiale
        # scivolava da sola su una pagina quasi vuota
        tab.setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 4),
                                 ('BOTTOMPADDING', (0, 1), (-1, -1), 4)]))
        # la tabella si spezza, con l'intestazione ripetuta: tenuta intera lasciava
        # mezza pagina bianca sopra di se' (p. 26 dell'edizione 0.4)
        S += _h3_flusso(mat.get('titolo', 'Il materiale')) + [tab]
        if mat.get('nota'):
            S += [SP(5), T(mat['nota'], small)]
        if mat.get('foto'):
            f, cap, ratio, focus = mat['foto']
            S += [SP(14), foto(f, FW, cap, col, ratio=ratio, focus=focus, id_linea=id_)]
        if s.get('pagina_dopo_materiale'):
            S.append(PageBreak())
        else:
            S.append(SP(STACCO))

    # ------------------------------------------------ fotografie
    if not s.get('foto_dopo_lati'):
        for v in s.get('foto', []):
            S += [_foto_voce(v, col, id_), SP(16)]

    # ------------------------------------------------ l'A-frame
    af = s.get('aframe')
    if af:
        b_ = [_h3('L’A-frame di questa linea'), SP(6)]
        if af.get('chips'):
            b_ += [ChipRow([(x, marca_chip(y)) for x, y in af['chips']], C_TEN), SP(10)]
        b_.append(two_cols(gear_block('Com’è fatto', [marca(v) for v in af.get('come', [])],
                                      C_TEN),
                           gear_block('Da rilevare', af.get('da_rilevare', []), MUT)))
        S += [KeepTogether(b_), SP(STACCO)]

    # ------------------------------------------------ varianti
    for v in s.get('varianti', []):
        b_ = [_h3(v['titolo']), SP(5), T(v['testo'], body)]
        # 'foto' e' una coppia, o un elenco di coppie: la prima resta con il testo, le
        # altre scorrono dopo
        coppie = v.get('foto') or []
        if coppie and not isinstance(coppie, list):
            coppie = [coppie]
        if coppie:
            f1, c1, f2, c2, ratio, focus = coppie[0]
            b_ += [SP(10), coppia(f1, c1, f2, c2, ratio, focus, col, id_)]
        S += [KeepTogether(b_)]
        for f1, c1, f2, c2, ratio, focus in coppie[1:]:
            S += [SP(12), coppia(f1, c1, f2, c2, ratio, focus, col, id_)]
        S += [SP(STACCO)]

    S += _coda(s, col)
    while S and isinstance(S[-1], Spacer):
        S.pop()
    S.append(PageBreak())
    return S


def _coda(s, col):
    """L'avvertenza propria della linea e l'elenco di cio' che manca."""
    out = []
    if s.get('avvertenza'):
        titolo, testo = s['avvertenza']
        out += [callout(titolo, marca(testo), WARN, '!', FW, True), SP(STACCO)]
    if s.get('da_rilevare'):
        # Un elenco breve resta intero: spezzato, lasciava tre righe orfane su una pagina
        # nuova (108 m). Uno lungo puo' continuare sulla pagina dopo.
        voci = [BUm(x, col) for x in s['da_rilevare']]
        if len(voci) <= 8:
            out += [KeepTogether([_h3('Ancora da rilevare su questa linea'), SP(5)] + voci),
                    SP(STACCO)]
        else:
            out += (_h3_flusso('Ancora da rilevare su questa linea', 70) + voci
                    + [SP(STACCO)])
    return out


def marca_chip(v):
    """Le pastiglie disegnano testo semplice: il marcatore resta in chiaro."""
    return v


# ---------------------------------------------------------------- la scheda dalle foto
# Altezza della miniatura rispetto alla larghezza: basta a riconoscere la sosta e
# lascia stare due righe di schede in una pagina.
RAPPORTO_MINIATURA = 0.42


def scheda_foto(l):
    """Linea fotografata: la foto, che cosa si vede, dove sta il resto.

    Le parole del file del gruppo (schemi, note, «Schetchy») non stanno qui: sono
    nel fascicolo di rilievo, accanto alla scheda da compilare, dove servono a chi
    va a rilevare (edizione 0.4, decisione E).
    """
    col = C_AREA[l['settore']]
    fs = REG.foto_di(l)
    ts = ParagraphStyle('fn', fontName='Pop-B', fontSize=11, leading=14)
    fs_ = ParagraphStyle('ff', fontName='Pop-M', fontSize=7, leading=10,
                         textColor=C_LIVELLO[REG.FOTOGRAFATA])
    ds = ParagraphStyle('fd', fontName='Lora', fontSize=8.4, leading=11.4,
                        textColor=INK2, spaceBefore=2.5)
    ns = ParagraphStyle('fs', fontName='Lora', fontSize=7.8, leading=10.6,
                        textColor=MUT, spaceBefore=4)
    ow, oh = dim(fs[0])
    conta = '%d fotografie' % len(fs) if len(fs) > 1 else '1 fotografia'
    inner = [[PhotoStrip(str(fs[0]), COL - 22, ow, oh, None, col, RAPPORTO_MINIATURA, 0.5)],
             [SP(6)],
             [Paragraph('%s · %s' % (l['codice'], REG.nome_catalogo(l)), ts)],
             [Paragraph('FOTOGRAFATA · %s DEL GRUPPO · MONTAGGIO NON DOCUMENTATO'
                        % conta.upper().replace(' ', '&nbsp;'), fs_)]]
    sintesi = FC.sintesi(l['id'])
    if sintesi:
        inner.append([Paragraph(marca(sintesi), ds)])
    inner.append([Paragraph('Scheda di rilievo %d, con le note del file del gruppo. Lato di '
                            'tensione e date delle foto: da dichiarare da chi c’era.'
                            % REG.numero_scheda(l), ns)])
    it = Table(inner, colWidths=[COL - 22])
    it.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 2), (0, 2), 3),
                            ('BOTTOMPADDING', (0, 3), (0, 3), 4)]))
    t = Table([[it]], colWidths=[COL])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), tint(col, 0.07)),
                           ('LINEBEFORE', (0, 0), (0, 0), 3, col),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 9),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    t.hAlign = 'LEFT'
    return t


def ha_scheda(l):
    """Vero se la linea ha un file di dati in dati/schede/: allora ha la scheda completa."""
    return REG.scheda_di(l) is not None


def scheda(l):
    """La scheda giusta: completa se c'e' il file di dati, a mezza colonna se ci sono
    solo fotografie, niente per una linea censita."""
    if ha_scheda(l):
        return scheda_completa(l, REG.scheda_di(l))
    if REG.livello(l) == REG.FOTOGRAFATA:
        return [scheda_foto(l)]
    return []


if __name__ == '__main__':
    # Diagnostica: dove stanno i pixel del colore della linea nel render del
    # settore. Da usare se il render viene riesportato e `estremi` va aggiornato.
    import numpy as np
    from PIL import Image
    id_ = sys.argv[1] if len(sys.argv) > 1 else 'anfiteatro-53'
    l = REG.di(id_)
    s = REG.scheda_di(l)
    if not s or not s.get('posizione'):
        raise SystemExit('nessuna posizione nella scheda di %s' % id_)
    f = render_di(s['posizione']['render'])
    a = np.asarray(Image.open(f).convert('RGB')).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ys, xs = np.nonzero((r > 200) & (g > 70) & (g < 160) & (b < 80) & (r - g > 80))
    print('render %s: %d x %d' % (f.name, a.shape[1], a.shape[0]))
    if len(xs):
        print('pixel del colore della linea: %d, x %d-%d, y %d-%d'
              % (len(xs), xs.min(), xs.max(), ys.min(), ys.max()))
        print('estremo sinistro ~ (%d, %d), destro ~ (%d, %d)' % (
            xs.min(), ys[xs.argmin()], xs.max(), ys[xs.argmax()]))
