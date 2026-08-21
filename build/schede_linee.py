# -*- coding: utf-8 -*-
"""Impaginazione della parte multi-linea del manuale.

Legge il registro in dati/linee.py e produce due cose:

* il **catalogo** delle ventiquattro linee censite, per area;
* una **scheda segnaposto** per ognuna delle linee non ancora documentate.

Le schede segnaposto sono l'impalcatura: quando una linea viene filmata e
trascritta, il suo segnaposto va sostituito da un capitolo vero, senza toccare
il resto del documento.

Questo modulo non contiene dati: se una lunghezza va corretta, si corregge in
dati/linee.py.
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from campi import griglia_campi                                     # noqa: E402
from reportlab.platypus import (PageBreak, Table, TableStyle,       # noqa: E402
                                Paragraph, KeepTogether)

from PIL import Image as _PILImage                                  # noqa: E402

import linee as REG                                                 # noqa: E402

# Una cartella per linea, chiamata con l'id della linea. Vedi il LEGGIMI li'
# dentro: basta creare la cartella e metterci i file, nessun codice da toccare.
FOTO_LINEE = RADICE / 'lavorazione' / 'foto_linee'

# Viste 3D del catalogo i-pietra, un file per settore. Vedi il LEGGIMI li'
# dentro. I settori senza render vengono saltati e il manuale lo dichiara.
RENDER_IPIETRA = RADICE / 'fonti' / 'render_ipietra'
_ESTENSIONI = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

LINEA = HexColor(0xF97316)      # colore che i-pietra assegna alla 53 m

# un colore per area, coerente in tutta la parte
C_AREA = {
    'Rookie':         LC[6],
    'Settore Giallo': LC[4],
    'Anfiteatro':     LC[2],
    'Anfite-altro':   LC[1],
    'Despedida':      LC[7],
}


def _norm(t):
    """Minuscolo e senza separatori: «Anfite-altro» e «anfite_altro» coincidono."""
    return ''.join(c for c in t.lower() if c.isalnum())


def _slug_area(area):
    return area.lower().replace(' ', '-')


def _cartella_render():
    """La cartella dei render, comunque sia scritta.

    Windows non distingue maiuscole e minuscole, Linux si': una cartella creata
    come «Render_ipietra» sarebbe invisibile al build senza questa ricerca.
    """
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

    Il nome del file non deve essere esatto: basta che contenga il nome del
    settore. «Anfiteatro.jpg», «render_anfiteatro.png» e «anfiteatro-vista2.jpg»
    vanno tutti bene. Non si puo' pretendere che un export sia rinominato a mano.
    """
    d = _cartella_render()
    if d is None:
        return None
    bersaglio = _norm(area)
    trovati = sorted(f for f in d.iterdir()
                     if f.suffix.lower() in _ESTENSIONI and bersaglio in _norm(f.stem))
    return trovati[0] if trovati else None


def vista_insieme():
    """La panoramica coi cinque settori etichettati, rigenerata se serve.

    Il manuale non dipende dall'aver lanciato prima panoramica_settori.py: se la
    figura manca o e' piu' vecchia della panoramica o del registro, viene
    ridisegnata qui. Se manca la panoramica di partenza, il capitolo si apre
    senza figura e piu' sotto lo dichiara.
    """
    try:
        import panoramica_settori as PS
    except Exception:
        return None
    sorgente = PS.panoramica()
    if sorgente is None or not PS.POSIZIONI:
        return None
    fatta = PS.DEST / 'panoramica_settori.jpg'
    fonti = [sorgente, RADICE / 'dati' / 'linee.py',
             RADICE / 'build' / 'panoramica_settori.py']
    if (not fatta.exists()
            or fatta.stat().st_mtime < max(f.stat().st_mtime for f in fonti
                                           if f.exists())):
        PS.disegna(sorgente, PS.POSIZIONI, fatta)
    return fatta


def parte_planimetria():
    """Le viste 3D disponibili, una per settore.

    Non e' una planimetria topografica: sono viste prospettiche di un modello
    fotogrammetrico, e mostrano le linee secondo i-pietra, che non coincidono
    con quelle della locandina. La didascalia lo dichiara.
    """
    disponibili = [(a, render_di(a)) for a in REG.AREE]
    disponibili = [(a, f) for a, f in disponibili if f]
    mancanti = [a for a in REG.AREE if not render_di(a)]
    if not disponibili:
        return [P('Nessun render del catalogo i-pietra è disponibile: i settori sono '
                  'descritti solo dalle tabelle qui sotto. I file vanno in '
                  'fonti/render_ipietra/ — vedi il LEGGIMI lì dentro.', small), SP(12)]
    S = [P('<b>Le viste del catalogo i-pietra.</b> Non sono planimetrie topografiche: '
           'sono viste prospettiche di un modello fotogrammetrico, e tracciano le linee '
           '<b>secondo i-pietra</b>, che accorpa Anfite-altro dentro Anfiteatro. '
           'Servono a riconoscere dove corre ciascuna linea sulla parete, non a '
           'misurarla.', body), SP(12)]
    for area, f in disponibili:
        ls = REG.per_area(area)
        censite = sum(1 for l in ls if l['in_ipietra'])
        with _PILImage.open(f) as im:
            ow, oh = im.size
        # «Settore Giallo» contiene gia' la parola: non anteporla due volte
        etichetta = area if area.lower().startswith('settore') else 'Settore ' + area
        cap = ('%s · %d linee tracciate sul render, %d censite sulla locandina'
               % (etichetta, censite, len(ls)))
        if area in REG.SETTORI_IN_CONFLITTO:
            cap += ' · etichettate «%s» in i-pietra' % REG.SETTORE_IPIETRA[area]
        S.append(PhotoStrip(str(f), FW, ow, oh, cap, C_AREA[area], 0.58, 0.5))
        S.append(SP(14))
    if mancanti:
        S.append(P('Senza render: %s. Finché manca, la copertura di i-pietra su quel '
                   'settore non è verificata — è il dubbio 53.'
                   % ' e '.join('<b>%s</b>' % a for a in mancanti), small))
        S.append(SP(12))
    return S


def foto_di(l):
    """Fotografie della linea montata, se qualcuno ne ha messe."""
    d = FOTO_LINEE / l['id']
    if not d.is_dir():
        return []
    return sorted(f for f in d.iterdir() if f.suffix in _ESTENSIONI)


def stato_effettivo(l):
    """Stato reale: il registro dice il rigging, il disco dice le foto."""
    if l['stato'] == REG.DOCUMENTATA:
        return REG.DOCUMENTATA
    return REG.FOTOGRAFATA if foto_di(l) else REG.NON_DOCUMENTATA


def nome(l):
    """Nome completo di una linea: settore + lunghezza, mai la lunghezza sola."""
    return '%s · %d m' % (l['settore'], l['lunghezza'])


# ---------------------------------------------------------------- catalogo
def tabella_catalogo():
    """Le ventiquattro linee in una sola tabella, divisa per settore.

    Prima erano cinque tabelle separate che ripetevano la stessa testata cinque
    volte e non stavano su una pagina sola: due pagine riempite a meta'. Qui il
    settore diventa una banda colorata dentro un'unica tabella, e il catalogo
    torna a leggersi tutto insieme.

    La colonna dei rimandi e' il motivo per cui il documento viene impaginato
    piu' volte: senza, il catalogo elenca ventiquattro linee e non dice dove
    andare a leggerne una.
    """
    larghezze = [126, 70, FW - 126 - 70 - 52, 52]
    dati = [[Paragraph(t.upper(), th) for t in
             ('Lunghezza (catalogo)', 'In i-pietra', 'Rigging documentato', 'Vedi')]]
    stile = [('BACKGROUND', (0, 0), (-1, 0), INK),
             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
             ('LEFTPADDING', (0, 0), (-1, -1), 8),
             ('RIGHTPADDING', (0, 0), (-1, -1), 8),
             ('TOPPADDING', (0, 0), (-1, -1), 4),
             ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    r = 1
    for area in REG.AREE:
        ls = REG.per_area(area)
        col = C_AREA[area]
        ip = REG.SETTORE_IPIETRA[area]
        occhiello = 'in i-pietra: «%s»' % ip if ip else 'assente da i-pietra'
        banda = Paragraph(
            '<font name="Pop-B" size="9">%s</font>&nbsp;&nbsp;'
            '<font name="Pop-M" size="7">%d LINEE · %s</font>'
            % (area, len(ls), occhiello.upper()),
            ParagraphStyle('bd', fontName='Pop', leading=12, textColor=WHITE))
        dati.append([banda, '', '', ''])
        stile += [('BACKGROUND', (0, r), (-1, r), col),
                  ('SPAN', (0, r), (-1, r)),
                  ('TOPPADDING', (0, r), (-1, r), 5),
                  ('BOTTOMPADDING', (0, r), (-1, r), 5)]
        r += 1
        for k, l in enumerate(ls):
            if l['stato'] == REG.DOCUMENTATA:
                doc, vai = 'sì — capitolo di questo manuale', rif('cap53')
                lung = '<b>%d m</b>' % l['lunghezza']
            else:
                doc, vai = '—', rif('linea:%s' % l['id'])
                lung = '%d m' % l['lunghezza']
            dati.append([
                Paragraph(lung, td),
                Paragraph('sì' if l['in_ipietra'] else 'no', td),
                Paragraph(doc, td),
                Paragraph('<font name="Pop-M" size="8.2">%s</font>' % vai,
                          ParagraphStyle('vp', fontName='Pop', leading=11,
                                         textColor=col))])
            if k % 2:
                stile.append(('BACKGROUND', (0, r), (-1, r), PAPER))
            stile.append(('LINEBELOW', (0, r), (-1, r), 0.4, HAIR))
            r += 1
    t = Table(dati, colWidths=larghezze, repeatRows=1)
    t.setStyle(TableStyle(stile))
    return t


def nota_settori():
    """Testo del callout sui settori, calcolato dal registro.

    Era scritto a mano e si e' contraddetto con il paragrafo sopra appena la
    copertura di i-pietra e' cambiata. Ora non puo' piu' andare fuori sincrono.
    """
    pezzi = []
    for area in REG.SETTORI_IN_CONFLITTO:
        ip = REG.SETTORE_IPIETRA[area]
        ls = REG.per_area(area)
        pezzi.append('chiama «%s» anche le %d linee che la locandina mette '
                     'sotto «%s» — %s m'
                     % (ip, len(ls), area,
                        ', '.join(str(l['lunghezza']) for l in ls[:-1])
                        + ' e ' + str(ls[-1]['lunghezza'])))
    assenti = REG.aree_assenti_da_ipietra()
    if assenti:
        pezzi.append('non registra %s' % ' né '.join('<b>%s</b>' % a for a in assenti))
    # il nome del catalogo e' minuscolo per convenzione: la frase parte da
    # «Il catalogo» cosi' nessuna maiuscola automatica lo storpia
    testo = ('Il catalogo i-pietra ' + ', e '.join(pezzi) if pezzi
             else 'Le due fonti coincidono')
    return (testo + '. Chi cerca una linea partendo dall\'app e '
            'chi parte dalla locandina può quindi finire in due posti diversi. Finché non '
            'è chiarito, in questo manuale ogni linea è nominata <b>settore più '
            'lunghezza</b>, mai con la lunghezza da sola.')


ALTEZZA_PAGINA = H - TM - BM


def _bilancia(blocchi, altezza=None):
    """Distribuisce blocchi indivisibili su piu' pagine, il piu' pari possibile.

    Impaginati a flusso libero, i cinque settori entravano in quattro nella
    prima pagina e lasciavano il quinto da solo nella seconda, riempita per un
    quarto. Qui si calcola prima quante pagine servono, poi fra tutti i modi di
    tagliare l'elenco in quel numero di pagine si sceglie quello che rende le
    pagine piu' simili fra loro.
    """
    altezza = altezza or ALTEZZA_PAGINA
    misurati = [(KeepTogether(inner),
                 sum(f.wrap(FW, altezza)[1] for f in inner))
                for inner in blocchi]
    alt = [h for _, h in misurati]
    n = len(misurati)

    def pagine_di(tagli):
        """Gruppi contigui definiti dai punti di taglio."""
        bordi = [0] + list(tagli) + [n]
        return [alt[a:b] for a, b in zip(bordi, bordi[1:])]

    def valida(gruppi):
        return all(g and sum(g) <= altezza for g in gruppi)

    # numero minimo di pagine, per riempimento avido
    n_pag, corrente = 1, 0.0
    for h in alt:
        if corrente + h > altezza:
            n_pag += 1
            corrente = 0.0
        corrente += h

    from itertools import combinations
    migliore = None
    for tagli in combinations(range(1, n), n_pag - 1):
        gruppi = pagine_di(tagli)
        if not valida(gruppi):
            continue
        somme = [sum(g) for g in gruppi]
        # squilibrio: quanto la pagina piu' vuota si discosta dalla piu' piena
        costo = max(somme) - min(somme)
        if migliore is None or costo < migliore[0]:
            migliore = (costo, tagli)

    tagli = migliore[1] if migliore else ()
    bordi = [0] + list(tagli) + [n]
    fuori = []
    for k, (a, b) in enumerate(zip(bordi, bordi[1:])):
        if k:
            fuori.append(PageBreak())
        fuori.extend(f for f, _ in misurati[a:b])
    return fuori


def parte_catalogo():
    c = REG.conteggi()
    S = [Accent(LINEA, 'Le linee della Pietra'),
         Segna('catalogo'),
         LineHeader('', 'Le linee della Pietra', 'Catalogo · cinque aree', LINEA),
         SP(10),
         P('La locandina «La Pietra — Yeah Vez!» censisce <b>%d linee</b> distribuite su '
           'cinque aree. Il catalogo i-pietra ne registra <b>%d</b>. Di tutte, una sola — '
           'la %d m dell\'Anfiteatro — è documentata da riprese di montaggio ed è quella '
           'descritta nei capitoli precedenti.'
           % (c['totale'], c['in_ipietra'], REG.documentate()[0]['lunghezza']), lead),
         SP(12)]

    # la vista d'insieme apre il capitolo: i render per settore mostrano una
    # parete per volta e non dicono mai come i settori stiano fra loro
    vista = vista_insieme()
    if vista is not None:
        with _PILImage.open(vista) as _im:
            _ow, _oh = _im.size
        S.append(PhotoStrip(
            str(vista), FW, _ow, _oh,
            'I cinque settori sulla vista d’insieme i-pietra · '
            'da sinistra a destra come stanno sulla cresta', LINEA))
        S.append(SP(14))
        S.append(P('I settori sono indicati nell’ordine in cui si susseguono '
                   'lungo la cresta, ed è l’ordine con cui compaiono in tutta '
                   'la guida. Le pastiglie segnano <b>un tratto di parete, non un '
                   'ancoraggio</b>: servono a orientarsi, non a trovare un punto. '
                   'L’altezza a cui cadono è prospettiva, non quota.', small))
        S.append(SP(14))

    S += [P('Le lunghezze qui sotto sono <b>valori di catalogo</b>, non misure fatte sui '
            'punti: vale per tutte quello che la nota N2 dice della 53 m.', body),
          SP(14),
          callout('Le due fonti non concordano sui settori', nota_settori(),
                  WARN, strong=True),
          SP(16)]
    S.extend(parte_planimetria())
    S.append(PageBreak())
    S.append(Accent(LINEA, 'Le linee della Pietra'))
    S.append(tabella_catalogo())
    return S


# ---------------------------------------------------------------- segnaposto
def segnaposto(l):
    """Scheda compatta di una linea non ancora documentata.

    Che cosa manchi e' detto una volta nell'introduzione della parte: ripeterlo
    ventitre' volte non aggiunge informazione e raddoppia le pagine.
    """
    col = C_AREA[l['settore']]
    ts = ParagraphStyle('sn', fontName='Pop-B', fontSize=11, leading=14)
    fs = ParagraphStyle('sf', fontName='Pop-M', fontSize=7, leading=10,
                        textColor=MUT)
    fonte = 'LOCANDINA' + (' · I-PIETRA' if l['in_ipietra'] else '')
    inner = [[Paragraph(nome(l), ts)], [Paragraph(fonte, fs)]]
    it = Table(inner, colWidths=[COL - 22])
    it.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (0, 0), 3),
                            ('BOTTOMPADDING', (0, 1), (0, 1), 0)]))
    t = Table([[it]], colWidths=[COL])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), tint(col, 0.07)),
                           ('LINEBEFORE', (0, 0), (0, 0), 3, col),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 9),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    t.hAlign = 'LEFT'
    return t


def scheda_fotografata(l):
    """Linea montata e fotografata, ma senza documentazione di rigging."""
    col = C_AREA[l['settore']]
    fs = foto_di(l)
    ts = ParagraphStyle('fn', fontName='Pop-B', fontSize=11, leading=14)
    ds = ParagraphStyle('fd', fontName='Lora', fontSize=8.6, leading=12,
                        textColor=INK2)
    with _PILImage.open(fs[0]) as im:
        ow, oh = im.size
    conta = '%d fotografie' % len(fs) if len(fs) > 1 else '1 fotografia'
    inner = [[PhotoStrip(str(fs[0]), COL - 22, ow, oh, None, col, 0.62, 0.5)],
             [SP(7)],
             [Paragraph(nome(l), ts)],
             [Paragraph('Montata e fotografata · %s. <b>Rigging non documentato</b>: '
                        'la fotografia mostra che la linea esiste, non come è stata '
                        'ancorata.' % conta, ds)]]
    it = Table(inner, colWidths=[COL - 22])
    it.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 2), (0, 2), 3)]))
    t = Table([[it]], colWidths=[COL])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), tint(col, 0.07)),
                           ('LINEBEFORE', (0, 0), (0, 0), 3, col),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 10),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    t.hAlign = 'LEFT'
    return t


def scheda(l):
    """La scheda giusta per lo stato in cui la linea si trova."""
    return (scheda_fotografata(l) if stato_effettivo(l) == REG.FOTOGRAFATA
            else segnaposto(l))


def _intro_segnaposti(da):
    fotografate = [l for l in da if stato_effettivo(l) == REG.FOTOGRAFATA]
    testo = ('Di ognuna delle <b>%d linee</b> qui sotto non esiste documentazione di '
             'rigging: sono segnaposto dichiarati, non capitoli incompleti.' % len(da))
    if fotografate:
        testo += (' Di <b>%d</b> esistono fotografie della linea montata, che mostrano '
                  'che è stata attrezzata e camminata — non come è stata ancorata. '
                  'Delle altre %d si conoscono soltanto settore e lunghezza di catalogo.'
                  % (len(fotografate), len(da) - len(fotografate)))
    else:
        testo += (' Di tutte si conoscono soltanto il settore e la lunghezza di '
                  'catalogo: nessuna ripresa, nessuna trascrizione, nessun fotogramma.')
    return testo


# altezza utile di una pagina, al netto dei margini: la scheda di rilievo la
# riempie tutta invece di fermarsi a meta'
ALTEZZA_UTILE = H - TM - BM


def scheda_rilievo(l, primo_di_area=False):
    """Scheda di una linea non documentata, con i campi da compilare sul campo.

    Non e' un segnaposto: e' lo strumento con cui la linea viene documentata. I
    campi vengono da REG.CAMPI_RILIEVO, cioe' dalle stesse voci che per la 53 m
    sono state ricavate dalle riprese o che in DUBBI.md restano aperte.

    La scheda occupa la pagina intera. Prima ne occupava meno della meta': il
    foglio restava vuoto sotto e le righe erano troppo corte per ospitare la
    descrizione di un ancoraggio scritta a mano in parete.
    """
    col = C_AREA[l['settore']]
    ts = ParagraphStyle('rn', fontName='Pop-B', fontSize=13, leading=16)
    fs = ParagraphStyle('rf', fontName='Pop-M', fontSize=7, leading=10,
                        textColor=MUT)
    ds = ParagraphStyle('rd', fontName='Lora', fontSize=8.4, leading=11.6,
                        textColor=INK2)

    fonte = 'LOCANDINA' + (' · CENSITA IN I-PIETRA' if l['in_ipietra']
                           else ' · NON IN I-PIETRA')
    note = []
    if not l['in_ipietra']:
        note.append('Non compare nel catalogo i-pietra: esiste sulla locandina, '
                    'ma nell’app non c’è.')
    if l['settore'] in REG.SETTORI_IN_CONFLITTO:
        note.append('i-pietra la etichetta <b>Anfiteatro</b>, la locandina '
                    '<b>Anfite-altro</b>: due nomi per lo stesso posto.')
    if l['id'] in REG.COLLISIONE_NOME:
        note.append('<b>Attenzione al nome:</b> anche l’Anfiteatro ha una linea '
                    'chiamata «la 50». Citare sempre il settore.')

    testa = [[Paragraph(nome(l), ts)], [Paragraph(fonte, fs)]]
    if note:
        testa.append([SP(4)])
        testa.append([Paragraph(' '.join(note), ds)])
    it = Table(testa, colWidths=[FW - 24])
    it.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                            ('BOTTOMPADDING', (0, 0), (0, 0), 2)]))

    # quanto spazio resta alla griglia: pagina meno testata dell'area, bordi
    # della cornice e testata della scheda
    _, h_testa = it.wrap(FW - 24, 0)
    resto = (ALTEZZA_UTILE
             - (22 if primo_di_area else 0)     # etichetta del settore
             - 18                               # imbottitura della cornice
             - h_testa
             - 10                               # aria fra testata e griglia
             - 4)                               # margine di sicurezza
    corpo = [[it],
             [SP(10)],
             [griglia_campi(REG.campi_rilievo(), w=FW - 24, cols=2,
                            altezza=resto)]]
    t = Table(corpo, colWidths=[FW - 24])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))

    fuori = Table([[t]], colWidths=[FW])
    fuori.setStyle(TableStyle([('LINEBEFORE', (0, 0), (0, 0), 3, col),
                               ('BACKGROUND', (0, 0), (-1, -1), tint(col, 0.05)),
                               ('LEFTPADDING', (0, 0), (-1, -1), 14),
                               ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                               ('TOPPADDING', (0, 0), (-1, -1), 12),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return fuori


def indice_schede(da, cols=3):
    """Dove sta la scheda di ogni linea, in griglia.

    La pagina che apre i rilievi diceva che seguono ventitre' moduli e poi
    lasciava due terzi di foglio bianco. Chi va a montare una linea precisa ha
    bisogno di sapere a che pagina sta la sua: questo e' quel dato.
    """
    voci = []
    for area in REG.AREE:
        for l in da:
            if l['settore'] == area:
                voci.append((area, l, C_AREA[area]))
    n_righe = (len(voci) + cols - 1) // cols
    colonne = [voci[i * n_righe:(i + 1) * n_righe] for i in range(cols)]

    ns = ParagraphStyle('isn', fontName='Lora', fontSize=8.4, leading=11.6,
                        textColor=INK2)
    dati, stile = [], [
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]
    for r in range(n_righe):
        riga = []
        for k in range(cols):
            if r < len(colonne[k]):
                area, l, col = colonne[k][r]
                # il settore prende il suo colore: il quadratino unicode non
                # esiste in questo font e stampava un vuoto
                riga.append(Paragraph(
                    '<font color="#%s">%s</font> · %d m'
                    % (col.hexval()[2:], area, l['lunghezza']), ns))
                riga.append(Paragraph(
                    '<font name="Pop-M" size="8" color="#%s">%s</font>'
                    % (col.hexval()[2:], rif('linea:%s' % l['id'])),
                    ParagraphStyle('isp', fontName='Pop', leading=11,
                                   alignment=TA_RIGHT)))
            else:
                riga += ['', '']
        dati.append(riga)
        for k in range(cols):
            stile.append(('LINEBELOW', (k * 2, r), (k * 2 + 1, r), 0.4, HAIR))
    # Lo stacco fra le colonne non si ottiene allargando la cella del numero:
    # il numero e' allineato a destra e si sposterebbe con il bordo, restando
    # attaccato alla voce successiva. Si aggiunge invece margine interno.
    larg = []
    for k in range(cols):
        larg += [112, 34 + (26 if k < cols - 1 else 0)]
        if k < cols - 1:
            stile.append(('RIGHTPADDING', (k * 2 + 1, 0), (k * 2 + 1, -1), 26))
    t = Table(dati, colWidths=larg)
    t.setStyle(TableStyle(stile))
    return t


def parte_rilievi():
    """Una scheda di rilievo per ogni linea non ancora documentata."""
    da = REG.da_documentare()
    S = [Accent(LINEA, 'Rilievo'),
         Segna('rilievi'),
         LineHeader('', 'Schede di rilievo', 'Le %d linee ancora da documentare'
                    % len(da), LINEA),
         SP(10),
         P('Di queste linee si conoscono soltanto settore e lunghezza di catalogo: '
           'nessuna ripresa, nessuna trascrizione, nessun fotogramma. Le schede che '
           'seguono <b>non sono capitoli incompleti, sono moduli da compilare</b>: '
           'una pagina per linea, con i campi che per la 53 m dell’Anfiteatro sono '
           'stati ricavati dalle riprese, e quelli che anche per quella linea restano '
           'aperti.', lead),
         SP(8),
         P('Compilate sul posto, si riportano poi in <b>dati/linee.py</b> e la linea '
           'smette di essere un modulo e diventa un capitolo.', body),
         SP(14),
         callout('Compilare solo ciò che si è visto',
                 'Vale qui la regola di tutto il documento: un campo lasciato in bianco '
                 'è un dato mancante dichiarato, e va benissimo. Un campo riempito a '
                 'memoria o per somiglianza con un’altra linea è un dato falso, e su un '
                 'documento di rigging è la cosa peggiore che ci possa finire dentro.',
                 WARN, '!', FW, True),
         SP(18),
         P('<font name="Pop-M" size="7.4" color="#%s">DOVE STA CIASCUNA SCHEDA</font>'
           % MUT.hexval()[2:], ParagraphStyle('ds', fontName='Pop', leading=11)),
         SP(7),
         indice_schede(da),
         PageBreak()]

    for area in REG.AREE:
        ls = [l for l in da if l['settore'] == area]
        for i, l in enumerate(ls):
            # il colore del settore vale anche per testatina e piede della
            # pagina, non solo per il filetto della cornice
            S.append(Segna('linea:%s' % l['id']))
            S.append(Accent(C_AREA[area], 'Rilievo · %s' % area))
            if i == 0:
                S.append(Paragraph(
                    '<font name="Pop-B" size="10.5" color="#%s">%s</font>'
                    % (C_AREA[area].hexval()[2:], area.upper()),
                    ParagraphStyle('rh', fontName='Pop', leading=14)))
                S.append(SP(8))
            S.append(scheda_rilievo(l, primo_di_area=(i == 0)))
            if not (area == REG.AREE[-1] and l is ls[-1]):
                S.append(PageBreak())
    return S


def parte_segnaposti():
    da = REG.da_documentare()
    S = [Accent(LINEA, 'Da documentare'),
         LineHeader('8', 'Le linee da documentare', 'Impalcatura · %d schede vuote'
                    % len(da), LINEA),
         SP(10),
         P(_intro_segnaposti(da), lead),
         SP(12),
         P('Perché una di queste diventi un capitolo servono, nell\'ordine: riprese del '
           'montaggio con audio, la trascrizione, la selezione dei fotogrammi e la '
           'compilazione dei dubbi con chi ha montato. La stessa pipeline già percorsa per '
           'la 53 m dell\'Anfiteatro.', body),
         SP(16)]
    for area in REG.AREE:
        ls = [l for l in da if l['settore'] == area]
        if not ls:
            continue
        righe = []
        for i in range(0, len(ls), 2):
            coppia = ls[i:i + 2]
            righe.append(two_cols(scheda(coppia[0]), scheda(coppia[1]))
                         if len(coppia) == 2 else scheda(coppia[0]))
            righe.append(SP(10))
        testa = Paragraph('<font name="Pop-B" size="10.5">%s</font>' % area,
                          ParagraphStyle('ah', fontName='Pop', leading=14))
        S.append(Accent(LINEA, 'Da documentare'))
        # l'intestazione dell'area non resta mai sola in fondo alla pagina:
        # viaggia insieme alla prima riga di schede
        S.append(KeepTogether([testa, SP(8), righe[0]]))
        S.extend(righe[1:])
        S.append(SP(6))
    return S


def parte_linee():
    """Tutta la parte multi-linea, pronta da concatenare alla storia del manuale."""
    return parte_catalogo() + [PageBreak()] + parte_segnaposti() + [PageBreak()]


# ---------------------------------------------------------------- riepilogo aree
def tabella_aree():
    """Le cinque aree con le lunghezze: una riga per area.

    Generata dal registro. Prima era scritta a mano accanto agli stessi dati, e
    le due copie sono andate in conflitto appena i-pietra e' cambiato.
    """
    righe = []
    for area in REG.AREE:
        ls = REG.per_area(area)
        lunghezze = ' · '.join(
            '<b>%d</b>' % l['lunghezza']
            if l['stato'] == REG.DOCUMENTATA or l['id'] in REG.COLLISIONE_NOME
            else str(l['lunghezza']) for l in ls)
        righe.append([area, lunghezze, str(len(ls))])
    return data_table(['Area', 'Lunghezze rilevate (m)', 'N.'],
                      righe, [104, 340, 47], color=LINEA)


def nota_copertura():
    """Frase sulla copertura di i-pietra, calcolata invece che trascritta."""
    c = REG.conteggi()
    pezzi = []
    assenti = REG.aree_assenti_da_ipietra()
    if assenti:
        pezzi.append('manca %s per intero' % ' e '.join('<b>%s</b>' % a for a in assenti))
    for area in REG.AREE:
        if area in assenti:
            continue
        mancanti = REG.lunghezze_assenti(area)
        if mancanti:
            pezzi.append('all\'%s mancano %s' % (
                area, ' e '.join('la %d m' % m for m in mancanti)))
    dettaglio = '; '.join(pezzi) if pezzi else 'le copre tutte'
    incerto = ''
    if REG.NON_VERIFICATI:
        incerto = (' La presenza di %s in i-pietra <b>non è stata verificata</b> su un '
                   'render: è segnata assente sulla fede di una ricognizione più vecchia '
                   '(dubbio 53).'
                   % ' e '.join(REG.NON_VERIFICATI))
    return ('Dalla locandina «La Pietra». Il catalogo i-pietra ne registra <b>%d sulle '
            '%d</b>: %s. La differenza è segnalata ma non risolta.%s'
            % (c['in_ipietra'], c['totale'], dettaglio, incerto))


if __name__ == '__main__':
    # diagnostica: che cosa il build vede davvero nella cartella dei render
    d = _cartella_render()
    print('cartella render: %s' % (d if d else '— NON TROVATA —'))
    if d:
        immagini = [f.name for f in sorted(d.iterdir())
                    if f.suffix.lower() in _ESTENSIONI]
        print('immagini presenti: %s' % (', '.join(immagini) if immagini else 'nessuna'))
    print()
    for area in REG.AREE:
        f = render_di(area)
        print('  %-16s %s' % (area, f.name if f else '—'))
