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
from reportlab.platypus import (PageBreak, Table, TableStyle,       # noqa: E402
                                Paragraph, KeepTogether)

from PIL import Image as _PILImage                                  # noqa: E402

import linee as REG                                                 # noqa: E402

# Una cartella per linea, chiamata con l'id della linea. Vedi il LEGGIMI li'
# dentro: basta creare la cartella e metterci i file, nessun codice da toccare.
FOTO_LINEE = RADICE / 'lavorazione' / 'foto_linee'
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
def tabella_area(area):
    ls = REG.per_area(area)
    righe = []
    for l in ls:
        doc = 'sì — capitolo di questo manuale' if l['stato'] == REG.DOCUMENTATA else '—'
        lung = '<b>%d m</b>' % l['lunghezza'] if l['stato'] == REG.DOCUMENTATA \
            else '%d m' % l['lunghezza']
        righe.append([lung, 'sì' if l['in_ipietra'] else 'no', doc])
    return data_table(['Lunghezza (catalogo)', 'In i-pietra', 'Rigging documentato'],
                      righe, [138, 78, FW - 216], color=C_AREA[area])


def parte_catalogo():
    c = REG.conteggi()
    S = [Accent(LINEA, 'Le linee della Pietra'),
         LineHeader('7', 'Le linee della Pietra', 'Catalogo · cinque aree', LINEA),
         SP(10),
         P('La locandina «La Pietra — Yeah Vez!» censisce <b>%d linee</b> distribuite su '
           'cinque aree. Il catalogo i-pietra ne registra <b>%d</b>. Di tutte, una sola — '
           'la %d m dell\'Anfiteatro — è documentata da riprese di montaggio ed è quella '
           'descritta nei capitoli precedenti.'
           % (c['totale'], c['in_ipietra'], REG.documentate()[0]['lunghezza']), lead),
         SP(12),
         P('Le lunghezze qui sotto sono <b>valori di catalogo</b>, non misure fatte sui '
           'punti: vale per tutte quello che la nota N2 dice della 53 m.', body),
         SP(14),
         callout('Le due fonti non concordano sui settori',
                 'i-pietra chiama «Anfiteatro» anche le tre linee che la locandina mette '
                 'sotto «Anfite-altro» — 22, 30 e 135 m — e non registra affatto Settore '
                 'Giallo e Despedida. Chi cerca una linea partendo dall\'app e chi parte '
                 'dalla locandina può quindi finire in due posti diversi. Finché non è '
                 'chiarito, in questo manuale ogni linea è nominata <b>settore più '
                 'lunghezza</b>, mai con la lunghezza da sola.', WARN, strong=True),
         SP(16)]
    for area in REG.AREE:
        ls = REG.per_area(area)
        ip = REG.SETTORE_IPIETRA[area]
        occhiello = 'in i-pietra: «%s»' % ip if ip else 'assente da i-pietra'
        S.append(Accent(LINEA, 'Le linee della Pietra'))
        S.append(KeepTogether([
            Paragraph('<font name="Pop-B" size="11">%s</font>&nbsp;&nbsp;'
                      '<font name="Pop-M" size="7.6" color="%s">%d LINEE · %s</font>'
                      % (area, MUT.hexval().replace('0x', '#'), len(ls),
                         occhiello.upper()),
                      ParagraphStyle('ar', leading=15)),
            SP(6),
            tabella_area(area),
            SP(14)]))
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
                          ParagraphStyle('ah', leading=14))
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
