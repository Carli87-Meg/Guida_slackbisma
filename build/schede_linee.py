# -*- coding: utf-8 -*-
"""Parte 2 della guida, «Le linee», e il fascicolo delle schede di rilievo.

Legge il registro in dati/linee.py e produce:

* la **tavola di stato** delle ventiquattro linee, che apre la parte;
* una **pagina per settore**, nell'ordine della cresta: la vista i-pietra sopra,
  le sue linee sotto; e subito dopo le schede delle linee di quel settore che
  hanno qualcosa da mostrare (build/scheda_linea.py);
* il **fascicolo di rilievo**: il protocollo, il foglio dello spot, una scheda da
  compilare per ogni linea non documentata e, per le linee fotografate, la
  pagina con le parole del file del gruppo.

Fino all'edizione 0.3 le linee fotografate stavano in un capitolo a parte, nato
dal file che le conteneva, e la stessa linea compariva in tre posti. Ora ogni
linea ha un posto solo, nel suo settore, e il suo livello di documentazione
decide quanto spazio occupa.

Questo modulo non contiene dati: se una lunghezza va corretta, si corregge in
dati/linee.py; se un dato di una linea cambia, in dati/schede/<id>.py.
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
import file_lineebisma as FC                                        # noqa: E402
from scheda_linea import (C_AREA, LINEA, render_di, marca, T,       # noqa: E402
                          stato_chip, scheda, scheda_foto, ha_scheda)


def _etichetta(area):
    """«Settore Giallo» contiene gia' la parola: non anteporla due volte."""
    return area if area.lower().startswith('settore') else 'Settore ' + area


def vista_insieme():
    """La panoramica coi cinque settori etichettati, rigenerata se serve.

    Se la figura manca o e' piu' vecchia della panoramica o del registro, viene
    ridisegnata qui. Se manca la panoramica di partenza, la pagina lo dichiara.
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


# Le jpg di lavorazione/foto_linee/ non sono in git. Un build fatto da un clone
# pulito le trova mancanti: le linee tornano «censite» e le loro schede spariscono.
# Il build lo dice, una volta sola.
_AVVISO_DATO = False


def foto_mancanti():
    """Linee che il file del gruppo descrive come fotografate ma senza foto su disco."""
    return [l['id'] for l in REG.LINEE
            if REG.livello(l) < REG.DOCUMENTATA and FC.di(l['id']) is not None
            and not REG.foto_di(l)]


def avvisa_foto_mancanti():
    global _AVVISO_DATO
    if _AVVISO_DATO:
        return
    _AVVISO_DATO = True
    mancano = foto_mancanti()
    if not mancano:
        return
    print('\n*** AVVISO: mancano le fotografie di %d linee descritte in '
          'dati/file_lineebisma.py: %s.\n'
          '*** Le jpg di lavorazione/foto_linee/ non sono in git. Senza di esse queste '
          'linee escono come «censite»\n'
          '*** e le loro schede NON vengono stampate. Copiare le foto '
          '(vedi lavorazione/foto_linee/LEGGIMI.md)\n'
          '*** e rifare il build prima di diffondere il PDF.\n'
          % (len(mancano), ', '.join(mancano)), file=sys.stderr)


# ---------------------------------------------------------------- tabelle
_CODICE = ParagraphStyle('cod', fontName='Pop-M', fontSize=8.4, leading=11.6)
_DOVE = ParagraphStyle('dv', fontName='Pop-M', fontSize=8.2, leading=11)


def _cella_codice(l, col):
    return Paragraph('<font color="#%s">%s</font>' % (col.hexval()[2:], l['codice']), _CODICE)


def _cella_nome(l):
    if not l['nome']:
        return Paragraph('—', td)
    t = '<b>%s</b>' % l['nome']
    if l['soprannome']:
        t += ' · detta «%s»' % l['soprannome']
    return Paragraph(t, td)


def _dove(l):
    """Dove se ne legge di piu': la pagina della guida, la scheda di rilievo, o entrambe."""
    liv = REG.livello(l)
    n = REG.numero_scheda(l)
    if liv == REG.DOCUMENTATA:
        return rif('linea:%s' % l['id'])
    if liv >= REG.FOTOGRAFATA or ha_scheda(l):
        return '%s · scheda %d' % (rif('linea:%s' % l['id']), n)
    return 'scheda %d' % n


def _cella_dove(l, col):
    return Paragraph('<font color="#%s">%s</font>' % (col.hexval()[2:], _dove(l)), _DOVE)


INTESTAZIONE = ['Codice', 'Nome', 'Lunghezza', 'Stato', 'Dove']
LARGHEZZE = [52, 164, 70, 88, FW - 374]


def _riga(l, col):
    lung = '%d m' % l['lunghezza']
    if REG.livello(l) == REG.DOCUMENTATA:
        lung = '<b>%s</b>' % lung
    return [_cella_codice(l, col), _cella_nome(l), Paragraph(lung, td), stato_chip(l),
            _cella_dove(l, col)]


def tabella_settore(area):
    """Le linee di un settore, con il rimando a dove se ne legge di piu'."""
    col = C_AREA[area]
    return data_table(INTESTAZIONE, [_riga(l, col) for l in REG.per_area(area)],
                      LARGHEZZE, color=col)


def tavola_stato():
    """Le ventiquattro linee in una tabella sola: codice, nome, livello, dove.

    E' il posto unico che prima non c'era: per sapere che cosa si sa di una linea
    bisognava girare cinque pagine di settore.
    """
    righe = []
    for area in REG.AREE:
        for l in REG.per_area(area):
            r = _riga(l, C_AREA[area])
            if not l['nome']:
                r[1] = Paragraph(l['settore'], td)
            else:
                r[1] = Paragraph('<b>%s</b> · %s' % (l['nome'], l['settore']), td)
            righe.append(r)
    t = data_table(['Codice', 'Linea', 'Lunghezza', 'Stato', 'Dove'], righe,
                   LARGHEZZE, color=LINEA)
    # ventiquattro righe in una pagina: imbottitura ridotta
    t.setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 3.2),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 3.2)]))
    return t


def nota_nome(area):
    """«La 50» vale per due linee: lo si dice dove c'e' il rischio, in una riga.

    Il dubbio 45 chiama questa l'ambiguita' piu' pericolosa del documento, perche'
    un lettore potrebbe attrezzare la linea sbagliata. La nota sta sotto la tabella
    del Settore Giallo e nel glossario; la riga di GAS-OH dice il soprannome.
    """
    if any(l['id'] in REG.COLLISIONE_NOME for l in REG.per_area(area)):
        g = REG.di('anfiteatro-53')
        return ('La 50 m di questo settore <b>non è «la 50»</b> del gruppo: quel soprannome '
                'indica <b>%s</b> (%s), la 53 m dell’Anfiteatro, a %s.'
                % (g['nome'], g['codice'], rif('linea:anfiteatro-53')))
    return None


def nota_settori():
    """Come le due fonti nominano i settori, e che cosa mostrano i render.

    Per l'apparato: calcolata dal registro, cosi' non va fuori sincrono. Fino
    all'edizione 0.3 era il primo riquadro rosso della guida, a p. 4.
    """
    pezzi = []
    for area in REG.SETTORI_IN_CONFLITTO:
        ip = REG.SETTORE_IPIETRA[area]
        ls = REG.per_area(area)
        pezzi.append('Nei render i-pietra del %s le %d linee che la locandina mette sotto '
                     '«%s» (%s m) sono etichettate «%s», e nel catalogo stanno nel settore '
                     '%s: la guida usa il nome della locandina.'
                     % (REG.RENDER_DATA, len(ls), area,
                        ', '.join(str(l['lunghezza']) for l in ls[:-1])
                        + ' e ' + str(ls[-1]['lunghezza']), ip, ip))
    dopo = [l for l in REG.LINEE if l['in_ipietra'] and not l['sul_render']]
    if dopo:
        pezzi.append('I render mostrano %d linee: %s %s in i-pietra dopo la loro data.'
                     % (sum(1 for l in REG.LINEE if l['sul_render']),
                        ' e '.join('la %d m dell’%s' % (l['lunghezza'], l['settore'])
                                   for l in dopo),
                        'sono entrate' if len(dopo) > 1 else 'è entrata'))
    assenti = REG.aree_assenti_da_ipietra()
    if assenti:
        pezzi.append('Il catalogo i-pietra non registra %s.'
                     % ' né '.join('<b>%s</b>' % a for a in assenti))
    return ' '.join(pezzi)


def nota_copertura():
    """La copertura di i-pietra, con la sua data e la sua storia (dubbio 53)."""
    c = REG.conteggi()
    prima = REG.IPIETRA_STORIA[:-1]
    storia = ''
    if prima:
        storia = '; ne aveva %s' % ' e '.join('%d al %s' % (n, d) for d, n, _f in prima)
    if c['in_ipietra'] == c['totale']:
        return ('Al %s il catalogo i-pietra registra <b>tutte le %d linee</b> della '
                'locandina%s.' % (REG.IPIETRA_DATA, c['totale'], storia))
    pezzi = []
    for area in REG.AREE:
        mancanti = REG.lunghezze_assenti(area)
        if mancanti:
            pezzi.append('all’%s mancano %s' % (
                area, ' e '.join('la %d m' % m for m in mancanti)))
    return ('Al %s, delle %d linee della locandina, il catalogo i-pietra ne registra '
            '<b>%d</b>%s: %s. La differenza è segnalata ma non risolta.'
            % (REG.IPIETRA_DATA, c['totale'], c['in_ipietra'], storia,
               '; '.join(pezzi) or 'le copre tutte'))


# ---------------------------------------------------------------- le pagine
def pagina_settore(area, k):
    """Una pagina per settore: la vista i-pietra sopra, le sue linee sotto.

    E' la struttura disegnata a mano su Figma. Dall'edizione 0.4 l'occhiello, la
    didascalia e la tabella non parlano piu' del catalogo i-pietra: quella storia
    sta nell'apparato.
    """
    col = C_AREA[area]
    ls = REG.per_area(area)
    S = [Accent(col, 'Le linee · %s' % area), Segna('settore:%s' % area)]
    blocco = [LineHeader('', area, 'Settore %d di %d · %d linee · %s'
                         % (k, len(REG.AREE), len(ls), REG.CODICE_SETTORE[area]), col),
              SP(12)]
    f = render_di(area)
    if f:
        ow, oh = _PILImage.open(f).size
        cap = '%s · vista i-pietra' % _etichetta(area)
        if area in REG.SETTORI_IN_CONFLITTO:
            cap += ' · sul render le linee sono etichettate «%s»' % REG.SETTORE_IPIETRA[area]
        blocco.append(PhotoStrip(str(f), FW, ow, oh, cap, col))
        dopo = [l for l in ls if l['in_ipietra'] and not l['sul_render']]
        if dopo:
            frase = ('%s non %s tracciate sul render.'
                     % (' e '.join('la %d m' % l['lunghezza'] for l in dopo),
                        'sono' if len(dopo) > 1 else 'è'))
            blocco += [SP(5), P(frase[0].upper() + frase[1:], small)]
        blocco.append(SP(16))
    else:
        blocco += [P('Di questo settore non c’è una vista i-pietra.', small), SP(10)]
    blocco.append(tabella_settore(area))
    nota = nota_nome(area)
    if nota:
        blocco += [SP(10), P(nota, small)]
    S.append(KeepTogether(blocco))
    return S


def schede_del_settore(area):
    """Le schede delle linee del settore che hanno qualcosa da mostrare.

    Prima le linee documentate, una scheda completa ciascuna; poi le fotografate,
    a due per riga. Le linee censite non hanno scheda: la tabella del settore e'
    tutto cio' che se ne sa.
    """
    col = C_AREA[area]
    ls = REG.per_area(area)
    S = []
    for l in ls:
        if ha_scheda(l):
            # la scheda chiude con un salto pagina: un secondo salto prima della
            # successiva lasciava una pagina bianca (visto il 27/10/2026)
            if not (S and isinstance(S[-1], PageBreak)):
                S.append(PageBreak())
            S.extend(scheda(l))
    fot = [l for l in ls if REG.livello(l) == REG.FOTOGRAFATA and not ha_scheda(l)]
    if fot:
        righe = []
        for i in range(0, len(fot), 2):
            coppia = fot[i:i + 2]
            riga = (two_cols(scheda_foto(coppia[0]), scheda_foto(coppia[1]))
                    if len(coppia) == 2 else two_cols(scheda_foto(coppia[0]), SP(1)))
            # il rimando di ogni linea viaggia con la sua riga di schede
            righe.append([Segna('linea:%s' % l['id']) for l in coppia] + [riga])
        testa = Paragraph('<font name="Pop-B" size="10.5" color="#%s">Le linee fotografate '
                          '· %s</font>' % (col.hexval()[2:], area),
                          ParagraphStyle('ah', fontName='Pop', leading=14))
        if not (S and isinstance(S[-1], PageBreak)):
            S.append(SP(18))
        S.append(KeepTogether([Accent(col, 'Le linee · %s' % area), testa, SP(4),
                               P('Fotografie del gruppo: mostrano la linea montata, non come '
                                 'è stata ancorata. Il lato di tensione non è dichiarato.',
                                 small), SP(8)] + righe[0]))
        for r in righe[1:]:
            S += [SP(10), KeepTogether(r)]
    return S


def _senza_salto_finale(S):
    while S and isinstance(S[-1], PageBreak):
        S.pop()
    return S


def parte_linee():
    """La parte 2 per intero: la tavola di stato, poi i settori con le loro schede."""
    avvisa_foto_mancanti()
    c = REG.conteggi()
    S = [Accent(LINEA, 'Le linee'), Segna('parte2'), Segna('stato'),
         LineHeader('', 'Le linee della Pietra', 'Parte 2 · %d linee, %d settori'
                    % (c['totale'], len(REG.AREE)), LINEA),
         SP(10),
         P('Le ventiquattro linee, nell’ordine in cui stanno sulla cresta. Per ognuna la '
           'tavola dice che cosa se ne sa — il <b>livello di documentazione</b> — e dove '
           'trovarla: la pagina di questa guida, o il numero della scheda nel fascicolo di '
           'rilievo.', lead),
         SP(12),
         tavola_stato(),
         SP(10),
         P('Le lunghezze sono <b>valori di catalogo</b>, non misure fatte sui punti: nemmeno '
           'la 53 m è ancora stata rimisurata. Il codice è la sigla del settore e il numero '
           'd’ordine sulla locandina; il nome proprio è quello di SlackMap, dove è stato '
           'raccolto.', small)]
    for k, area in enumerate(REG.AREE, start=1):
        if not (S and isinstance(S[-1], PageBreak)):
            S.append(PageBreak())
        S.extend(pagina_settore(area, k))
        S.extend(schede_del_settore(area))
    return _senza_salto_finale(S)


# ---------------------------------------------------------------- il fascicolo
ALTEZZA_UTILE = H - TM - BM


def _cornice(contenuto, col, w=FW):
    """La cornice colorata delle schede da compilare."""
    t = Table([[contenuto]], colWidths=[w])
    t.setStyle(TableStyle([('LINEBEFORE', (0, 0), (0, 0), 3, col),
                           ('BACKGROUND', (0, 0), (-1, -1), tint(col, 0.05)),
                           ('LEFTPADDING', (0, 0), (-1, -1), 14),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 12),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


def _senza_bordi(righe, w):
    t = Table(righe, colWidths=[w])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


def _foglio(titolo, sotto, note, campi, col, spazio_sopra=0, checklist=None):
    """Un foglio da compilare che riempie la pagina: testata, note, griglia, caselle."""
    ts = ParagraphStyle('rn', fontName='Pop-B', fontSize=13, leading=16)
    fs = ParagraphStyle('rf', fontName='Pop-M', fontSize=7, leading=10, textColor=MUT)
    ds = ParagraphStyle('rd', fontName='Lora', fontSize=8.4, leading=11.6, textColor=INK2)
    testa = [[Paragraph(titolo, ts)], [Paragraph(sotto, fs)]]
    if note:
        testa += [[SP(4)], [Paragraph(marca(' '.join(note)), ds)]]
    it = _senza_bordi(testa, FW - 24)
    _, h_testa = it.wrap(FW - 24, 0)
    coda = []
    h_coda = 0
    if checklist:
        etichetta = Paragraph('<font name="Pop-M" size="7.2" color="#%s">FOTO FATTE</font>'
                              % MUT.hexval()[2:], ParagraphStyle('ck', fontName='Pop',
                                                                 leading=10))
        caselle = Checklist(checklist, col, w=FW - 24, cols=2)
        coda = [[SP(8)], [etichetta], [SP(4)], [caselle]]
        h_coda = 8 + 10 + 4 + caselle.h
    resto = (ALTEZZA_UTILE - spazio_sopra - 18 - h_testa - 10 - h_coda - 16)
    corpo = [[it], [SP(10)],
             [griglia_campi(list(campi), w=FW - 24, cols=2, altezza=resto)]] + coda
    return _cornice(_senza_bordi(corpo, FW - 24), col)


def _righe_file(l, ds):
    """Che cosa dice il file e che cosa si vede nelle sue foto, colonna per colonna.

    Le due fonti restano distinte in ogni riga: le parole del file fra virgolette,
    la descrizione delle foto dopo «nelle foto». Dove una delle due manca, la riga
    lo dice invece di tacere.
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
        visto = c['foto_' + lato] or 'nessuna foto'
        righe.append(Paragraph(marca('<b>Lato «%s»</b> · nel file: %s · nelle foto: %s.'
                                     % (lato, detto, visto)), ds))
    if c.get('foto_fuori'):
        righe.append(Paragraph(marca('<b>Fuori dalle colonne dei lati</b> · nelle foto: %s.'
                                     % c['foto_fuori']), ds))
    s_v, s_l = c['schetchy']
    p_v, p_l = c['persone']
    pezzi = []
    if c['note']:
        pezzi.append('note %s' % virg(c['note']))
    if c['tipologia']:
        pezzi.append('tipologia %s' % virg(c['tipologia']))
    if s_v or s_l:
        pezzi.append('Schetchy&nbsp;(dal&nbsp;file) %s / %s' % (s_v or '—', s_l or '—'))
    if p_v or p_l:
        pezzi.append('persone %s / %s' % (virg(p_v), virg(p_l)))
    if pezzi:
        righe.append(Paragraph('<b>Dal file</b> · %s.' % ' · '.join(pezzi), ds))
    righe.append(Paragraph(marca('<b>%s</b> · %s.' % (FC.DC, c['da_confermare'])), ds))
    return righe


def pagina_file(l):
    """Per una linea fotografata: la pagina con le parole del file del gruppo.

    Sta dopo la scheda da compilare, non nella guida: serve a chi va a rilevare,
    che deve sapere che cosa aspettarsi e che cosa controllare.
    """
    col = C_AREA[l['settore']]
    n = REG.numero_scheda(l)
    ds = ParagraphStyle('fd', fontName='Lora', fontSize=8.8, leading=12.4,
                        textColor=INK2, spaceBefore=5)
    S = [Accent(col, 'Scheda %d · %s · dal file' % (n, l['settore'])),
         LineHeader('', 'Che cosa dice il file del gruppo',
                    'Scheda %d · %s · %s · da controllare'
                    % (n, l['codice'], REG.nome_catalogo(l)), col),
         SP(10),
         P('Il file LineeBisma del gruppo ha una riga per questa linea e una colonna per '
           'lato, «vicino» e «lontano»: sono le <b>sue</b> colonne, non il lato tensione e '
           'il lato statico della guida. Tutto ciò che scrive è segnato <b>«da '
           'controllare»</b>; le sue fotografie non hanno data. Qui le sue parole e che cosa '
           'mostrano le foto, perché chi va a rilevare sappia che cosa aspettarsi e che cosa '
           'verificare.', lead),
         SP(8)]
    S += _righe_file(l, ds)
    S += [SP(14),
          P('Che cosa misuri «Schetchy» il file non lo dice; le coppie di valori seguono '
            'l’ordine delle colonne. Nessuna misura è letta a occhio dalle foto.', small),
          PageBreak()]
    return S


def scheda_rilievo(l, primo_di_area=False):
    """Scheda di una linea non documentata, con i campi da compilare sul campo.

    I campi vengono da REG.CAMPI_RILIEVO; le caselle in fondo da REG.FOTO_DA_FARE.
    La scheda occupa la pagina intera.
    """
    col = C_AREA[l['settore']]
    n = REG.numero_scheda(l)
    liv = REG.livello(l)
    sotto = 'SCHEDA %d · %s · %s' % (n, l['codice'], REG.LIVELLI[liv][0].upper())
    note = []
    if not l['in_ipietra']:
        note.append('Non compare nel catalogo i-pietra: esiste sulla locandina, ma nell’app '
                    'non c’è.')
    if l['settore'] in REG.SETTORI_IN_CONFLITTO:
        note.append('Nei render i-pietra del %s è etichettata <b>%s</b>, sulla locandina sta '
                    'sotto <b>%s</b>: due nomi per lo stesso posto. Qui vale quello della '
                    'locandina.' % (REG.RENDER_DATA, REG.SETTORE_IPIETRA[l['settore']],
                                    l['settore']))
    if l['id'] in REG.COLLISIONE_NOME:
        g = REG.di('anfiteatro-53')
        note.append('<b>Attenzione al nome:</b> «la 50» del gruppo è %s (%s), la 53 m '
                    'dell’Anfiteatro, non questa linea. Citare sempre il settore.'
                    % (g['nome'], g['codice']))
    if liv == REG.FOTOGRAFATA:
        note.append('Esistono <b>%d fotografie</b> della linea montata, nel file del gruppo: '
                    'la scheda nella guida dice che cosa mostrano e che cosa ne scrive il '
                    'file. Non documentano il montaggio; il lato di tensione resta da '
                    'dichiarare.' % len(REG.foto_di(l)))
    # la nota vale anche per una linea censita: la 108 ha perso le sue foto, che erano
    # della 113, e chi va a rilevarla deve saperlo
    c = FC.di(l['id'])
    if c and c.get('nota_rilievo'):
        note.append(c['nota_rilievo'])
    return _foglio(REG.nome_catalogo(l), sotto, note, REG.campi_rilievo(), col,
                   spazio_sopra=22 if primo_di_area else 0,
                   checklist=[t for t, _d in REG.FOTO_DA_FARE])


def scheda_spot():
    """Il foglio dello spot: le domande a cui la guida non risponde senza il gruppo."""
    note = ['Accesso, regole e contatti della Pietra sono vuoti nella guida di proposito: la '
            'Pietra è area protetta e falesia storica, e queste voci entrano solo con la '
            'risposta di chi frequenta lo spot. Scrivere ciò che si sa per certo; una voce '
            'vuota è un dato mancante dichiarato.']
    return _foglio('Rilievo dello spot', 'LA PIETRA DI BISMANTOVA · ACCESSO, REGOLE, CONTATTI',
                   note, REG.CAMPI_SPOT, LINEA)


def pagina_protocollo(col=LINEA):
    """Il protocollo di rilievo: che cosa misurare e fotografare. Senza salto pagina."""
    return [LineHeader('', 'Protocollo di rilievo', 'Che cosa misurare, dichiarare, fotografare',
                       col),
            SP(10),
            P('È la lezione del montaggio della 53 m, scritta come istruzione: ogni voce è un '
              'dato che allora non è stato raccolto e che poi si è dovuto ricostruire, o che '
              'manca ancora. Si applica a ogni linea che si monta, documentata o no.', lead),
            SP(14),
            Steps(list(REG.PROTOCOLLO_RILIEVO), col, FW, 2),
            SP(16),
            KeepTogether([P('<b>Le fotografie da fare</b>', h3), SP(6),
                          Checklist([t for t, _d in REG.FOTO_DA_FARE], col, w=FW, cols=1,
                                    corpo=9.0),
                          SP(8),
                          P('Ogni voce è una fotografia che per la 53 m è mancata o non si '
                            'legge. Una foto d’insieme e una per dettaglio, con un oggetto di '
                            'misura nota accanto, valgono più di dieci scatti da lontano.',
                            small)])]


def indice_schede(da, cols=3):
    """Dove sta la scheda di ogni linea, in griglia."""
    voci = [(l['settore'], l, C_AREA[l['settore']]) for l in da]
    n_righe = (len(voci) + cols - 1) // cols
    colonne = [voci[i * n_righe:(i + 1) * n_righe] for i in range(cols)]
    ns = ParagraphStyle('isn', fontName='Lora', fontSize=8.4, leading=11.6, textColor=INK2)
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
                riga.append(Paragraph(
                    '<font name="Pop-M" size="7.6" color="#%s">%d</font>&nbsp;&nbsp;'
                    '<font color="#%s">%s</font> · %d m'
                    % (MUT.hexval()[2:], REG.numero_scheda(l), col.hexval()[2:],
                       l['codice'], l['lunghezza']), ns))
                riga.append(Paragraph(
                    '<font name="Pop-M" size="8" color="#%s">%s</font>'
                    % (col.hexval()[2:], rif('rilievo:%s' % l['id'])),
                    ParagraphStyle('isp', fontName='Pop', leading=11, alignment=TA_RIGHT)))
            else:
                riga += ['', '']
        dati.append(riga)
        for k in range(cols):
            stile.append(('LINEBELOW', (k * 2, r), (k * 2 + 1, r), 0.4, HAIR))
    larg = []
    for k in range(cols):
        larg += [112, 34 + (26 if k < cols - 1 else 0)]
        if k < cols - 1:
            stile.append(('RIGHTPADDING', (k * 2 + 1, 0), (k * 2 + 1, -1), 26))
    t = Table(dati, colWidths=larg)
    t.setStyle(TableStyle(stile))
    return t


def parte_rilievi():
    """Il fascicolo: introduzione e indice, protocollo, foglio dello spot, una scheda per linea."""
    avvisa_foto_mancanti()
    da = REG.da_documentare()
    fot = [l for l in da if REG.livello(l) == REG.FOTOGRAFATA]
    n_fot = len(fot)
    conosciuto = ('Di %d di queste linee si conoscono soltanto settore e lunghezza di '
                  'catalogo. ' % (len(da) - n_fot))
    if fot:
        conosciuto += ('Di %d (schede %s) esistono anche fotografie del gruppo, che mostrano la '
                       'linea montata ma non documentano il montaggio: la loro scheda nella '
                       'guida dice che cosa mostrano e che cosa ne scrive il file del gruppo. '
                       % (n_fot, ', '.join(str(REG.numero_scheda(l)) for l in fot[:-1])
                          + ' e ' + str(REG.numero_scheda(fot[-1]))))
    S = [Accent(LINEA, 'Introduzione'),
         Segna('rilievi'),
         LineHeader('', 'Schede di rilievo', 'Le %d linee ancora da documentare, e lo spot'
                    % len(da), LINEA),
         SP(10),
         P(conosciuto + 'Ogni scheda è un <b>modulo da compilare sul posto</b>, con i campi '
           'che per la 53 m dell’Anfiteatro sono stati ricavati dalle riprese e quelli che '
           'anche per quella linea restano aperti. Il primo foglio è per lo spot: accesso, '
           'regole, contatti.', lead),
         SP(8),
         P('Una scheda compilata permette di documentare la linea: da modulo diventa una '
           'scheda della guida, al livello «rilevata».', body),
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
         SP(10),
         P('Protocollo di rilievo a %s; foglio dello spot a %s.'
           % (rif('rilievo:protocollo'), rif('rilievo:spot')), small),
         SP(16),
         Rule(FW, 0.6, HAIR, 8),
         SP(8),
         P('<b>Avvertenza.</b> Highlining e slacklining comportano rischi. Queste schede '
           'servono a raccogliere dati, non a montare: non sostituiscono formazione, '
           'esperienza diretta e verifica autonoma di ogni ancoraggio prima di ogni '
           'utilizzo.', small),
         PageBreak(),
         Accent(LINEA, 'Protocollo'), Segna('rilievo:protocollo')]
    S += pagina_protocollo(LINEA)
    S += [PageBreak(), Accent(LINEA, 'Lo spot'), Segna('rilievo:spot'), scheda_spot(),
          PageBreak()]

    for area in REG.AREE:
        ls = [l for l in da if l['settore'] == area]
        for i, l in enumerate(ls):
            S.append(Accent(C_AREA[area], 'Scheda %d · %s' % (REG.numero_scheda(l), area)))
            S.append(Segna('rilievo:%s' % l['id']))
            if i == 0:
                S.append(Paragraph(
                    '<font name="Pop-B" size="10.5" color="#%s">%s</font>'
                    % (C_AREA[area].hexval()[2:], area.upper()),
                    ParagraphStyle('rh', fontName='Pop', leading=14)))
                S.append(SP(8))
            S.append(scheda_rilievo(l, primo_di_area=(i == 0)))
            S.append(PageBreak())
            # le parole del file stanno nella scheda della guida, quando c'e'
            if REG.livello(l) == REG.FOTOGRAFATA and not ha_scheda(l):
                S.extend(pagina_file(l))
    return _senza_salto_finale(S)


if __name__ == '__main__':
    # diagnostica: che cosa il build vede davvero
    from scheda_linea import _cartella_render
    d = _cartella_render()
    print('cartella render: %s' % (d if d else '— NON TROVATA —'))
    for area in REG.AREE:
        f = render_di(area)
        print('  %-16s %s' % (area, f.name if f else '—'))
    print()
    for l in REG.in_ordine():
        print('%-6s %-28s %-12s %s' % (l['codice'], REG.nome(l), REG.nome_livello(l),
                                      'scheda %s' % REG.numero_scheda(l)
                                      if REG.numero_scheda(l) else ''))
