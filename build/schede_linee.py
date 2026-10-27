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
import re
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
import foto_carlo as FC                                             # noqa: E402

# Una cartella per linea, chiamata con l'id della linea. Vedi il LEGGIMI li'
# dentro: basta creare la cartella e metterci i file, nessun codice da toccare.
# Che cosa mostrino le foto, e che cosa ne dica il file LineeBisma, sta in dati/foto_carlo.py
# (riassunto dei LETTURA.md di ogni cartella).
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


def _etichetta(area):
    """«Settore Giallo» contiene gia' la parola: non anteporla due volte."""
    return area if area.lower().startswith('settore') else 'Settore ' + area


def foto_di(l):
    """Fotografie della linea montata, se qualcuno ne ha messe.

    La prima in ordine di nome e' la miniatura stampata: per convenzione la 01, che
    non deve mostrare volti riconoscibili (vedi lavorazione/foto_linee/LEGGIMI.md).
    """
    d = FOTO_LINEE / l['id']
    if not d.is_dir():
        return []
    return sorted(f for f in d.iterdir() if f.suffix in _ESTENSIONI)


# Le jpg di lavorazione/foto_linee/ non sono in git. Un build fatto da un clone
# pulito (la verifica del 27/10 l'ha fatto da `git archive`) le trova mancanti: le
# linee tornano «non documentate» e il capitolo «Le linee fotografate» sparisce.
# Prima succedeva in silenzio; ora il build lo dice, una volta sola.
_AVVISO_DATO = False


def foto_mancanti():
    """Linee che dati/foto_carlo.py descrive come fotografate ma senza foto su disco."""
    return [l['id'] for l in REG.LINEE
            if l['stato'] != REG.DOCUMENTATA and FC.di(l['id']) is not None
            and not foto_di(l)]


def _avvisa_foto_mancanti():
    global _AVVISO_DATO
    if _AVVISO_DATO:
        return
    _AVVISO_DATO = True
    mancano = foto_mancanti()
    if not mancano:
        return
    print('\n*** AVVISO: mancano le fotografie di %d linee descritte in '
          'dati/foto_carlo.py: %s.\n'
          '*** Le jpg di lavorazione/foto_linee/ non sono in git. Senza di esse queste '
          'linee escono come "non documentate"\n'
          '*** e il capitolo "Le linee fotografate" NON viene stampato. Copiare le foto '
          '(vedi lavorazione/foto_linee/LEGGIMI.md)\n'
          '*** e rifare il build prima di diffondere il PDF.\n'
          % (len(mancano), ', '.join(mancano)), file=sys.stderr)


def stato_effettivo(l):
    """Stato reale: il registro dice il rigging, il disco dice le foto."""
    if l['stato'] == REG.DOCUMENTATA:
        return REG.DOCUMENTATA
    if foto_di(l):
        return REG.FOTOGRAFATA
    if FC.di(l['id']) is not None:
        _avvisa_foto_mancanti()
    return REG.NON_DOCUMENTATA


def nome(l):
    """Nome completo di una linea: settore + lunghezza, mai la lunghezza sola."""
    return '%s · %d m' % (l['settore'], l['lunghezza'])


# ---------------------------------------------------------------- catalogo
def numero_scheda(l):
    """Numero della scheda di rilievo di una linea, nell'ordine della cresta.

    Le schede stanno in un fascicolo a parte: un numero di pagina del fascicolo
    stampato nella guida si confonderebbe con le pagine della guida stessa. Il
    numero di scheda no, ed e' quello che si scrive sul foglio.
    """
    da = [x for area in REG.AREE for x in REG.da_documentare() if x['settore'] == area]
    for i, x in enumerate(da, start=1):
        if x['id'] == l['id']:
            return i
    return None


def tabella_settore(area):
    """Le linee di un settore, con il rimando a dove se ne legge di piu'.

    La documentata rimanda al suo capitolo; le altre alla loro scheda di rilievo,
    nel fascicolo a parte.
    """
    col = C_AREA[area]
    righe = []
    for l in REG.per_area(area):
        if l['stato'] == REG.DOCUMENTATA:
            lung = '<b>%d m</b>' % l['lunghezza']
            # D3 (27/10/2026): nel titolo GAS-OH, «la 50» resta il soprannome
            doc = 'sì — GAS-OH, detta «la 50»: scheda in questa guida'
            dove = rif('cap53')
        elif stato_effettivo(l) == REG.FOTOGRAFATA:
            # le foto del file mostrano la sosta, non il montaggio: la linea
            # resta da documentare, ma ha un posto nella parte 3
            lung = '%d m' % l['lunghezza']
            doc = 'no — fotografata, %s' % rif('fotografata:%s' % l['id'],
                                                rif('fotografate'))
            dove = 'scheda %d' % numero_scheda(l)
        else:
            lung = '%d m' % l['lunghezza']
            doc = '—'
            dove = 'scheda %d' % numero_scheda(l)
        righe.append([Paragraph(lung, td),
                      Paragraph('sì' if l['in_ipietra'] else 'no', td),
                      Paragraph(doc, td),
                      Paragraph('<font name="Pop-M" size="8.2">%s</font>' % dove,
                                ParagraphStyle('dv', fontName='Pop', leading=11,
                                               textColor=col))])
    return data_table(['Lunghezza (catalogo)', 'In i-pietra', 'Rigging documentato', 'Dove'],
                      righe, [118, 64, FW - 118 - 64 - 64, 64], color=col)


def nota_nome(area):
    """Il nome «la 50» vale per due linee: lo si dice dove serve, in una riga.

    Il riquadro rosso «Due nomi che possono ingannare» e' stato tolto dalla
    pagina dello spot nella revisione su Figma dell'autore. L'informazione no:
    il dubbio 45 la chiama l'ambiguita' piu' pericolosa del documento, perche'
    un lettore potrebbe attrezzare la linea sbagliata. Resta qui, accanto alle
    due linee che riguarda.

    Decisione D3 del 27/10/2026 (dubbio 45): nel titolo la 53 m si chiama GAS-OH,
    il nome che ha su SlackMap; «la 50» resta il soprannome del gruppo, e resta la
    nota sull'altra 50 m della Pietra, al Settore Giallo.
    """
    if area == 'Anfiteatro':
        return ('La 53 m è <b>GAS-OH</b>, la linea che sul campo chiamano <b>«la 50»</b>: '
                'non va confusa con la 50 m del Settore Giallo.')
    if any(l['id'] in REG.COLLISIONE_NOME for l in REG.per_area(area)):
        return ('La 50 m di questo settore <b>non è «la 50»</b> documentata in questa guida: '
                'quel nome indica GAS-OH, la 53 m dell’Anfiteatro, a %s.' % rif('cap53'))
    return None


def nota_settori():
    """Testo del callout sui settori, calcolato dal registro.

    Era scritto a mano e si e' contraddetto con il paragrafo sopra appena la
    copertura di i-pietra e' cambiata. Ora non puo' piu' andare fuori sincrono.
    """
    pezzi = []
    for area in REG.SETTORI_IN_CONFLITTO:
        ip = REG.SETTORE_IPIETRA[area]
        ls = REG.per_area(area)
        # D4 (27/10/2026). L'etichetta «Anfiteatro» e' quella dei render del 20/08:
        # nel catalogo, al 21/10, le tre linee hanno nomi propri e stanno nel settore
        # anfiteatro (verifica «fonti» del 27/10, punto 4). Prima la frase diceva
        # «il catalogo etichetta», al presente.
        pezzi.append('nei render i-pietra del %s le %d linee che la locandina mette '
                     'sotto «%s» — %s m — sono etichettate «%s», e nel catalogo stanno nel '
                     'settore %s'
                     % (REG.RENDER_DATA, len(ls), area,
                        ', '.join(str(l['lunghezza']) for l in ls[:-1])
                        + ' e ' + str(ls[-1]['lunghezza']), ip, ip))
    assenti = REG.aree_assenti_da_ipietra()
    if assenti:
        pezzi.append('il catalogo i-pietra non registra %s'
                     % ' né '.join('<b>%s</b>' % a for a in assenti))
    # i-pietra e' minuscolo per convenzione: la frase comincia con un'altra parola,
    # cosi' nessuna maiuscola automatica lo storpia
    testo = ('; '.join(pezzi) if pezzi else 'le due fonti coincidono')
    testo = testo[0].upper() + testo[1:]
    # Decisione D4 del 27/10/2026 (dubbio 52): vale il nome della locandina.
    scelta = ''
    if REG.SETTORI_IN_CONFLITTO:
        scelta = (' In questo manuale vale il nome della locandina: %s.'
                  % ', '.join('<b>«%s»</b>' % a for a in REG.SETTORI_IN_CONFLITTO))
    # D3 (27/10/2026): la 53 m ha anche un nome proprio, GAS-OH, nel titolo
    return (testo + '. Chi cerca una linea partendo dall\'app e '
            'chi parte dalla locandina può quindi finire in due posti diversi.' + scelta +
            ' Ogni linea è nominata con <b>settore e lunghezza</b> — la 53 m anche con il '
            'suo nome, GAS-OH — mai con la lunghezza da sola.')


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


# Vedute di un settore prese da terra, quando ci sono. La didascalia dice che
# cosa si sa e che cosa no: IMG_3311, 22/08/2026, dubbio 57.
VEDUTE = {
    'Despedida': ('IMG_3311.jpg',
                  'La Despedida dal bordo della cresta, 22 agosto 2026.',
                  'La roccia sullo sfondo dovrebbe essere quella della linea da 165 m: '
                  '<font color="#B3261E">[DA CONFERMARE]</font>.'),
}
FOTO_DRITTE = RADICE / 'lavorazione' / 'foto_dritte'


def veduta(area, col):
    """Foto da terra a mezza colonna, con accanto che cosa mostra."""
    if area not in VEDUTE or not (FOTO_DRITTE / VEDUTE[area][0]).exists():
        return None
    nome, didascalia, nota = VEDUTE[area]
    f = FOTO_DRITTE / nome
    with _PILImage.open(f) as im:
        ow, oh = im.size
    lato = (FW - 14) / 2
    testo = [P('<b>Da terra</b>', h3), SP(4), P(didascalia, small), SP(4), P(nota, small)]
    return two_cols(PhotoStrip(str(f), lato, ow, oh, None, col, 0.50, 0.33), testo)


def pagina_settore(area, k):
    """Una pagina per settore: la vista i-pietra sopra, le sue linee sotto.

    E' la struttura che l'autore ha disegnato a mano su Figma. Prima i cinque
    render stavano su tre pagine e le ventiquattro linee in una tabella sola
    piu' avanti: per sapere quali linee mostrasse un render bisognava voltare
    pagina e cercarle.
    """
    col = C_AREA[area]
    ls = REG.per_area(area)
    ip = REG.SETTORE_IPIETRA[area]
    occhiello = 'Settore %d di %d · %d linee · %s' % (
        k, len(REG.AREE), len(ls),
        'in i-pietra «%s»' % ip if ip else 'assente da i-pietra')
    S = [Accent(col, 'Le linee · %s' % area),
         Segna('settore:%s' % area)]
    blocco = [LineHeader('', area, occhiello, col), SP(12)]
    f = render_di(area)
    if f:
        with _PILImage.open(f) as im:
            ow, oh = im.size
        # sul render, non in i-pietra: la 20 m e la 108 m sono entrate nel catalogo
        # il giorno dopo i render (dubbio 53, aggiornato il 27/10/2026)
        tracciate = sum(1 for l in ls if l['sul_render'])
        cap = ('%s · %d linee tracciate sul render, %d censite sulla locandina'
               % (_etichetta(area), tracciate, len(ls)))
        if area in REG.SETTORI_IN_CONFLITTO:
            # l'etichetta e' quella del render (D4), non il nome nel catalogo
            cap += ' · con l’etichetta «%s»' % REG.SETTORE_IPIETRA[area]
        blocco.append(PhotoStrip(str(f), FW, ow, oh, cap, col))
        dopo = [l['lunghezza'] for l in ls if l['in_ipietra'] and not l['sul_render']]
        if dopo:
            # Sotto la foto, non nella didascalia: PhotoStrip la scrive su una riga
            # sola, e con questa frase in coda usciva dal margine destro (p. 6,
            # visto il 27/10/2026).
            frase = ('%s %s in i-pietra dopo il render.'
                     % (' e '.join('la %d m' % m for m in dopo),
                        'sono entrate' if len(dopo) > 1 else 'è entrata'))
            blocco += [SP(5), P(frase[0].upper() + frase[1:], small)]
        blocco.append(SP(16))
    else:
        blocco += [P('Di questo settore non c’è un render i-pietra.', small), SP(10)]
    blocco.append(tabella_settore(area))
    nota = nota_nome(area)
    if nota:
        blocco += [SP(10), P(nota, small)]
    vista = veduta(area, col)
    if vista is not None:
        blocco += [SP(14), vista]
    S.append(KeepTogether(blocco))
    return S


def parte_catalogo():
    c = REG.conteggi()
    # Testata, testo e panoramica viaggiano insieme. Sotto «Lo spot» la
    # panoramica non entra: da sola sarebbe scivolata alla pagina dopo, e la
    # testata del catalogo sarebbe rimasta in fondo, separata dalla sua figura.
    # Marcatore e segnalibro stanno dentro il blocco, cosi' il numero di pagina
    # dell'indice e' quello dove il capitolo si apre davvero.
    apertura = [Accent(LINEA, 'Le linee della Pietra'),
         Segna('catalogo'),
         LineHeader('', 'Le linee della Pietra', 'Catalogo · cinque aree', LINEA),
         SP(10),
         P('La locandina «La Pietra — Yeah Vez!» censisce <b>%d linee</b> distribuite su '
           'cinque aree, e il catalogo i-pietra ne registra <b>%d</b> al %s. Una sola — la '
           '%d m dell’Anfiteatro, GAS-OH — è documentata: la sua scheda è a %s, e il metodo '
           'con cui è montata è nella parte 2.'
           % (c['totale'], c['in_ipietra'], REG.IPIETRA_DATA,
              REG.documentate()[0]['lunghezza'], rif('cap53')), lead),
         SP(12)]

    # la vista d'insieme apre il capitolo: i render per settore mostrano una
    # parete per volta e non dicono mai come i settori stiano fra loro
    vista = vista_insieme()
    if vista is not None:
        with _PILImage.open(vista) as _im:
            _ow, _oh = _im.size
        apertura.append(PhotoStrip(
            str(vista), FW, _ow, _oh,
            'I cinque settori sulla vista d’insieme i-pietra · '
            'da sinistra a destra come stanno sulla cresta', LINEA))
    S = [KeepTogether(apertura)]
    if vista is not None:
        S.append(SP(14))
        S.append(P('I settori seguono l’ordine in cui stanno sulla cresta, ed è l’ordine di '
                   'tutta la guida. Le pastiglie segnano <b>un tratto di parete, non un '
                   'ancoraggio</b>: servono a orientarsi, non a trovare un punto. L’altezza a '
                   'cui cadono è prospettiva, non quota.', small))
        S.append(SP(14))

    S += [callout('Le due fonti non concordano sui settori', nota_settori(),
                  WARN, strong=True),
          SP(14),
          P('Nelle pagine che seguono ogni settore ha la sua vista i-pietra e l’elenco delle '
            'sue linee. Le viste <b>non sono planimetrie</b>: sono prospettive di un modello '
            'fotogrammetrico, e servono a riconoscere dove corre una linea sulla parete, non '
            'a misurarla. Le lunghezze sono <b>valori di catalogo</b>, non misure fatte sui '
            'punti: nemmeno la 53 m è ancora stata rimisurata. Nella colonna «Dove», il '
            'numero di scheda rimanda al fascicolo delle schede di rilievo.', body)]
    for k, area in enumerate(REG.AREE, start=1):
        S.append(PageBreak())
        S.extend(pagina_settore(area, k))
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


def _virgolette(t):
    return '«%s»' % t if t else '—'


# «[DA CONFERMARE]» e «[DA CONFERMARE: …]» in rosso, come nel resto della guida
_DC = re.compile(r'\[DA CONFERMARE[^\]]*\]')


def _dc(t):
    # «DA CONFERMARE» non va a capo a meta'
    return _DC.sub(lambda m: '<font color="#%s">%s</font>'
                   % (WARN.hexval()[2:],
                      m.group(0).replace('DA CONFERMARE', 'DA&nbsp;CONFERMARE')), t)


def _righe_file(l, ds, miniatura=None):
    """Che cosa dice il file e che cosa si vede nelle sue foto, colonna per colonna.

    Le due fonti restano distinte in ogni riga: le parole del file fra virgolette,
    la descrizione delle foto dopo «nelle foto». Dove una delle due manca, la riga
    lo dice invece di tacere. Niente numeri di dubbio, niente percorsi: i rimandi
    stanno nei commenti di dati/foto_carlo.py. `miniatura` e' la colonna da cui
    viene la foto stampata ('vicino', 'lontano', 'fuori'): quella riga lo dice.
    """
    c = FC.di(l['id'])
    if c is None:
        return []
    qui = ' (in miniatura)'
    righe = []
    for lato in ('vicino', 'lontano'):
        schema = c[lato]
        # le parole del file sono un nome di schema oppure una frase sua: la frase
        # si stampa com'e', il nome con la glossa «schema»
        detto = (('schema %s' % _virgolette(schema)) if schema in FC.NOMI_SCHEMA
                 else _virgolette(schema))
        visto = c['foto_' + lato] or 'nessuna foto'
        righe.append(Paragraph(_dc('<b>Lato «%s»</b>%s · nel file: %s · nelle foto: %s.'
                                   % (lato, qui if miniatura == lato else '', detto,
                                      visto)), ds))
    # foto sulla riga della linea ma fuori dalle colonne dei lati (la 108): prima
    # finivano tutte sotto «lontano» senza dirlo
    if c.get('foto_fuori'):
        righe.append(Paragraph(_dc('<b>Fuori dalle colonne dei lati</b>%s · nelle foto: %s.'
                                   % (qui if miniatura == 'fuori' else '',
                                      c['foto_fuori'])), ds))
    # Prima difficolta' e persone uscivano solo se c'erano note: una riga con
    # Schetchy ma senza note (nel file, la despedida-165) le avrebbe perse.
    s_v, s_l = c['schetchy']
    p_v, p_l = c['persone']
    pezzi = []
    if c['note']:
        pezzi.append('note %s' % _virgolette(c['note']))
    if s_v or s_l:
        pezzi.append('Schetchy&nbsp;(dal&nbsp;file) %s / %s' % (s_v or '—', s_l or '—'))
    if p_v or p_l:
        pezzi.append('persone %s / %s' % (_virgolette(p_v), _virgolette(p_l)))
    if pezzi:
        righe.append(Paragraph('<b>Dal file</b> · %s.' % ' · '.join(pezzi), ds))
    righe.append(Paragraph(_dc('<b>%s</b> · %s.' % (FC.DC, c['da_confermare'])), ds))
    return righe


def _lato_miniatura(f):
    """Di quale colonna del file e' una foto, dal nome <linea>_<NN>_<lato>_<soggetto>:
    'vicino', 'lontano', 'fuori' (lato-nd) o None."""
    parti = f.stem.split('_')
    lato = parti[2] if len(parti) > 2 else ''
    if lato in ('vicino', 'lontano'):
        return lato
    return 'fuori' if lato == 'lato-nd' else None


# Altezza della miniatura rispetto alla larghezza, nelle schede delle linee
# fotografate: basta a riconoscere la sosta, e lascia stare due righe di schede
# in una pagina. 0.34 e interlinea 10.5 (erano 0.40 e 11.0) dalla seconda verifica del
# 27/10: con le letture corrette le schede della 108 e della 113 non stavano piu'
# sotto quelle della 46 e della 97, e il capitolo passava da tre a quattro pagine
# semivuote.
RAPPORTO_MINIATURA = 0.34
INTERLINEA_SCHEDA = 10.5


def scheda_fotografata(l):
    """Linea montata e fotografata, ma senza documentazione di rigging.

    Oltre alla miniatura, la scheda dice che cosa il file dice di ciascun
    lato e che cosa la foto mostra davvero: due fonti, due diciture. Tutto cio'
    che il file dice e' «da controllare», e lo dice l'introduzione del capitolo.
    """
    col = C_AREA[l['settore']]
    fs = foto_di(l)
    ts = ParagraphStyle('fn', fontName='Pop-B', fontSize=11, leading=14)
    fs_ = ParagraphStyle('ff', fontName='Pop-M', fontSize=7, leading=10,
                         textColor=MUT)
    ds = ParagraphStyle('fd', fontName='Lora', fontSize=8.2, leading=INTERLINEA_SCHEDA,
                        textColor=INK2, spaceBefore=2.5)
    with _PILImage.open(fs[0]) as im:
        ow, oh = im.size
    conta = '%d fotografie' % len(fs) if len(fs) > 1 else '1 fotografia'
    # ratio: a 0.62 l'introduzione del capitolo e la prima riga di schede non
    # stavano nella stessa pagina; a 0.54 due righe di schede non stavano in una
    # pagina, e le pagine del capitolo restavano vuote per il 40% (verifica del
    # 27/10, punto 24). Vedi RAPPORTO_MINIATURA.
    inner = [[PhotoStrip(str(fs[0]), COL - 22, ow, oh, None, col,
                         RAPPORTO_MINIATURA, 0.5)],
             [SP(6)],
             [Paragraph(nome(l), ts)],
             # spazi indivisibili: «DA CONTROLLARE» andava a capo spezzato
             [Paragraph('%s · FILE&nbsp;LINEEBISMA · DA&nbsp;CONTROLLARE'
                        % conta.upper().replace(' ', '&nbsp;'), fs_)]]
    # la riga del lato da cui viene la miniatura lo dice: il testo parte sempre dal
    # «vicino», e tre miniature su sei sono del «lontano» (verifica «coerenza» del
    # 27/10, punto 4)
    inner += [[r] for r in _righe_file(l, ds, _lato_miniatura(fs[0]))]
    # «Rigging non documentato» vale per tutte: lo dice una volta l'introduzione
    # del capitolo, e la scheda guadagna due righe
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

    fonte = ('SCHEDA %d · LOCANDINA' % numero_scheda(l)
             + (' · CENSITA IN I-PIETRA' if l['in_ipietra'] else ' · NON IN I-PIETRA'))
    note = []
    if not l['in_ipietra']:
        note.append('Non compare nel catalogo i-pietra: esiste sulla locandina, '
                    'ma nell’app non c’è.')
    if l['settore'] in REG.SETTORI_IN_CONFLITTO:
        # D4: l'etichetta e' quella dei render del 20/08, non del catalogo di oggi
        note.append('Nei render i-pietra del %s è etichettata <b>%s</b>, sulla locandina '
                    'sta sotto <b>%s</b>: due nomi per lo stesso posto. Qui vale quello '
                    'della locandina.'
                    % (REG.RENDER_DATA, REG.SETTORE_IPIETRA[l['settore']], l['settore']))
    if l['id'] in REG.COLLISIONE_NOME:
        note.append('<b>Attenzione al nome:</b> anche l’Anfiteatro ha una linea '
                    'chiamata «la 50» (GAS-OH, 53 m). Citare sempre il settore.')
    if stato_effettivo(l) == REG.FOTOGRAFATA:
        # chi va a rilevare deve sapere che le soste sono gia' state fotografate:
        # la foto non compila la scheda, ma dice che cosa aspettarsi
        note.append('Esistono <b>%d fotografie</b> della linea montata (file LineeBisma del '
                    'gruppo), descritte nella guida al capitolo «Le linee fotografate»: non '
                    'documentano il montaggio, e il lato di tensione resta da dichiarare.'
                    % len(foto_di(l)))
        # la sosta con il tronco sta sulle righe di 108 e 113: chi va a rilevare la
        # cercherebbe sul capo sbagliato (DUBBI 59)
        c = FC.di(l['id'])
        if c and c.get('nota_rilievo'):
            note.append(_dc(c['nota_rilievo']))

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
                    '<font name="Pop-M" size="7.6" color="#%s">%d</font>&nbsp;&nbsp;'
                    '<font color="#%s">%s</font> · %d m'
                    % (MUT.hexval()[2:], numero_scheda(l), col.hexval()[2:], area,
                       l['lunghezza']), ns))
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
    """Il fascicolo delle schede di rilievo: introduzione, indice, una scheda per linea.

    Nella revisione su Figma l'autore ha spostato le ventitre' schede fuori dalla
    guida: per ora non servono a chi la legge, servono a chi va a rilevare. Ora
    sono un documento a se', da stampare e portare in parete
    (build/build_schede_rilievo.py). La guida le cita per numero.
    """
    da = REG.da_documentare()
    # Prima: «Di queste linee si conoscono soltanto settore e lunghezza… nessun
    # fotogramma», smentito dalle schede con le foto dello stesso fascicolo
    # (verifiche «fonti» e «coerenza» del 27/10).
    fot = sorted(numero_scheda(l) for l in da if stato_effettivo(l) == REG.FOTOGRAFATA)
    if fot:
        conosciuto = ('Di %d di queste linee si conoscono soltanto settore e lunghezza di '
                      'catalogo: nessuna ripresa, nessuna trascrizione, nessun fotogramma. '
                      'Di %d (schede %s) esistono anche fotografie del gruppo, che mostrano '
                      'la linea montata ma non documentano il montaggio.'
                      % (len(da) - len(fot), len(fot),
                         ', '.join(str(n) for n in fot[:-1]) + ' e ' + str(fot[-1])))
    else:
        conosciuto = ('Di queste linee si conoscono soltanto settore e lunghezza di '
                      'catalogo: nessuna ripresa, nessuna trascrizione, nessun fotogramma.')
    S = [Accent(LINEA, 'Introduzione'),
         Segna('rilievi'),
         LineHeader('', 'Schede di rilievo', 'Le %d linee ancora da documentare'
                    % len(da), LINEA),
         SP(10),
         P(conosciuto + ' Ogni scheda è un '
           '<b>modulo da compilare sul posto</b>, con i campi che per la 53 m '
           'dell’Anfiteatro sono stati ricavati dalle riprese e quelli che anche per '
           'quella linea restano aperti.', lead),
         SP(8),
         P('Una scheda compilata permette di documentare la linea: da modulo diventa un '
           'capitolo della guida.', body),
         SP(14),
         callout('Compilare solo ciò che si è visto',
                 'Un campo lasciato in bianco è un dato mancante dichiarato, e va benissimo. '
                 'Un campo riempito a memoria o per somiglianza con un’altra linea è un dato '
                 'falso, e su un documento di rigging è la cosa peggiore che ci possa finire '
                 'dentro.', WARN, '!', FW, True),
         SP(18),
         P('<font name="Pop-M" size="7.4" color="#%s">DOVE STA CIASCUNA SCHEDA</font>'
           % MUT.hexval()[2:], ParagraphStyle('ds', fontName='Pop', leading=11)),
         SP(7),
         indice_schede(da),
         SP(20),
         Rule(FW, 0.6, HAIR, 8),
         SP(8),
         P('<b>Avvertenza.</b> Highlining e slacklining comportano rischi. Queste schede '
           'servono a raccogliere dati, non a montare: non sostituiscono formazione, '
           'esperienza diretta e verifica autonoma di ogni ancoraggio prima di ogni '
           'utilizzo.', small),
         PageBreak()]

    for area in REG.AREE:
        ls = [l for l in da if l['settore'] == area]
        for i, l in enumerate(ls):
            # il colore del settore vale anche per testatina e piede della
            # pagina, non solo per il filetto della cornice
            S.append(Accent(C_AREA[area], 'Scheda %d · %s' % (numero_scheda(l), area)))
            S.append(Segna('linea:%s' % l['id']))
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


def fotografate():
    """Le linee da documentare di cui esistono fotografie, nell'ordine della cresta."""
    return [l for area in REG.AREE for l in REG.da_documentare()
            if l['settore'] == area and stato_effettivo(l) == REG.FOTOGRAFATA]


def tabella_scheda_sosta():
    """La scheda «Sosta Bisma Standard» del file, blocco per blocco, con le sue parole.

    Prima la guida ne stampava un riassunto: gli omega elencati due volte erano
    contati una volta sola, «Dadi» e «Cavalletto» sparivano, «senza cavalletto»
    era definito per deduzione e i termini del file erano tradotti in quelli della
    guida. Ora si stampano le celle; cio' che la scheda lascia aperto si dice sotto,
    con [DA CONFERMARE].
    """
    righe = []
    for blocco, celle in FC.SCHEDA_SOSTA:
        # una cella per voce; due celle sulla stessa riga del file (B20, C20)
        # restano due virgolettati affiancati
        voci = [' '.join(_virgolette(x) for x in riga) for riga in celle]
        righe.append([Paragraph('<b>%s</b>' % blocco, td),
                      Paragraph(' · '.join(voci), td)])
    return data_table(['Blocco del file', 'Celle, con le parole del file'],
                      righe, [118, FW - 118], color=LINEA)


def parte_fotografate():
    """Capitolo della parte 3: le linee fotografate dal gruppo, una scheda ciascuna.

    Prima queste schede non uscivano in nessun PDF: parte_segnaposti() non e'
    richiamata dal manuale dalla revisione su Figma. Le foto del file LineeBisma
    sono di sette linee, soste e linee montate; sei non hanno altra
    documentazione (la settima e' la 53 m, che ha la sua scheda e il build qui
    non la mostra): troppo per tacerle, troppo poco per una scheda
    come quella della 53 m. Stanno qui, dopo la 53 m, con la stessa regola: la
    foto dice che cosa c'e', non come si monta.

    Correzioni del 27/10/2026 (verifica, punti 10-19, 24): niente cronologia,
    percorsi del repository o numeri di dubbio nel testo stampato; [DA CONFERMARE]
    al posto di «Manca»; la provenienza in una riga; la scheda del file trascritta
    cella per cella. La provenienza nel dettaglio sta nell'apparato (fonti) e nei
    LETTURA.md di ogni cartella.
    """
    ls = fotografate()
    if not ls:
        return []
    n = len(ls)
    S = [Accent(LINEA, 'Linee fotografate'),
         Segna('fotografate'),
         LineHeader('', 'Le linee fotografate', 'Le linee · %d schede dalle foto del gruppo'
                    % n, LINEA),
         SP(10),
         P('Di <b>%d linee</b> esistono fotografie delle soste e della linea montata, '
           'raccolte in un file del gruppo con una riga per linea e una colonna per lato, '
           'insieme a schemi, note e valori che il file stesso segna <b>«da '
           'controllare»</b>: sono proposte, non rilievi. Nessuna di queste linee ha il '
           '<b>rigging documentato</b>: le foto mostrano la sosta, non come è stata montata. '
           'Ogni scheda tiene distinte le due cose, che cosa dice il file e che cosa si vede '
           'nelle foto; ciò che le foto non mostrano senza dubbi è marcato %s.'
           % (n, _dc(FC.DC)), lead),
         SP(6),
         # la data di lettura (FC.DATA_LETTURA) sta nei LETTURA.md e nell'apparato:
         # qui era cronologia (verifica «coerenza» del 27/10, punto 6)
         P('Fonte: file LineeBisma del gruppo (20/10/2026) e le sue fotografie, senza '
           'data.', small),
         SP(8),
         callout('«Vicino» e «lontano» sono le colonne del file',
                 'Non sono il lato tensione e il lato statico della guida: quale sia quale '
                 'non lo dice nessuna foto, ed è il primo dato da chiedere a chi ha '
                 'montato. Le coppie di valori stanno nell’ordine delle colonne, prima '
                 'quella accanto a «vicino», poi quella accanto a «lontano»: che valgano per '
                 'quel lato lo dice solo la posizione. Che cosa misuri «Schetchy» il file '
                 'non lo dice. Nessuna misura è letta a occhio.',
                 WARN, '!', FW, True),
         SP(10),
         # che lo schema «Bisma standard» delle righe sia questa scheda lo dice solo il
         # nome (verifica «fonti» del 27/10, punto 9; DUBBI 72)
         P(_dc('<b>La scheda «Sosta Bisma Standard» del file</b> («%s»); che sia lo schema '
               '«Bisma standard» delle righe lo dice il nome [DA CONFERMARE]:'
               % FC.SCHEDA_SOSTA_TITOLO), small),
         SP(5),
         tabella_scheda_sosta(),
         SP(5)]
    # allineate a sinistra: giustificate, le righe corte si allargavano a vuoto
    sx = ParagraphStyle('dcs', parent=small, alignment=0)
    S += [P(_dc(t), sx) for t in FC.SCHEDA_SOSTA_DA_CONFERMARE]
    S.append(SP(12))
    for area in REG.AREE:
        la = [l for l in ls if l['settore'] == area]
        if not la:
            continue
        righe = []
        for i in range(0, len(la), 2):
            coppia = la[i:i + 2]
            riga = (two_cols(scheda(coppia[0]), scheda(coppia[1]))
                    if len(coppia) == 2 else
                    two_cols(scheda(coppia[0]), SP(1)))
            # il rimando di ogni linea viaggia con la sua riga di schede: le tabelle
            # dei settori rimandano alla pagina della scheda, non all'inizio del
            # capitolo (la 60 m e la 70 m stavano a p. 26, il rimando diceva p. 24).
            # Una lista, non un KeepTogether: annidato in quello dell'intestazione
            # ne gonfia l'altezza e lascia una pagina bianca.
            righe.append([Segna('fotografata:%s' % l['id']) for l in coppia] + [riga])
        testa = Paragraph('<font name="Pop-B" size="10.5" color="#%s">%s</font>'
                          % (C_AREA[area].hexval()[2:], area.upper()),
                          ParagraphStyle('ah', fontName='Pop', leading=14))
        # l'intestazione dell'area non resta mai sola in fondo alla pagina:
        # viaggia insieme alla prima riga di schede
        S.append(KeepTogether([testa, SP(8)] + righe[0]))
        for r in righe[1:]:
            S.append(SP(10))
            S.append(KeepTogether(r))
        S.append(SP(10))
        S.append(SP(6))
    # Le letture complete stanno in lavorazione/foto_linee/<linea>/LETTURA.md, i
    # dubbi che aprono in DUBBI.md (voci 59-74): nel testo stampato non si citano.
    S.append(P('Per usare queste foto come documentazione degli ancoraggi serve che chi '
               'c’era dichiari il lato di tensione.', small))
    S.append(PageBreak())
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
    """Frase sulla copertura di i-pietra, calcolata invece che trascritta.

    La copertura cambia nel tempo (dubbio 53): la frase dice a che data vale il
    numero e quali erano i numeri prima (REG.IPIETRA_STORIA), e quante linee
    mostrano i render che la guida stampa.
    """
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
    # La storia sta in una frase sola: quali linee siano entrate dopo i render lo
    # dice la didascalia del render del settore, nel catalogo.
    prima = REG.IPIETRA_STORIA[:-1]
    storia = ''
    if prima:
        storia = ('; ne aveva %s' % ' e '.join(
            '%d al %s' % (n, d) for d, n, _f in prima))
        if any(d == REG.RENDER_DATA for d, _n, _f in prima):
            storia += ', la data dei render stampati nel catalogo'
    if c['in_ipietra'] == c['totale']:
        oggi = ('Al %s il catalogo i-pietra registra <b>tutte le %d linee</b> della '
                'locandina%s.' % (REG.IPIETRA_DATA, c['totale'], storia))
    else:
        oggi = ('Al %s, delle %d linee della locandina, il catalogo i-pietra ne registra '
                '<b>%d</b>%s: %s. La differenza è segnalata ma non risolta.'
                % (REG.IPIETRA_DATA, c['totale'], c['in_ipietra'], storia, dettaglio))
    return oggi + incerto


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
