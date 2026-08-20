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

import linee as REG                                                 # noqa: E402

LINEA = HexColor(0xF97316)      # colore che i-pietra assegna alla 53 m

# un colore per area, coerente in tutta la parte
C_AREA = {
    'Rookie':         LC[6],
    'Settore Giallo': LC[4],
    'Anfiteatro':     LC[2],
    'Anfite-altro':   LC[1],
    'Despedida':      LC[7],
}


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
         LineHeader('8', 'Le linee della Pietra', 'Catalogo · cinque aree', LINEA),
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


def parte_segnaposti():
    da = REG.da_documentare()
    S = [Accent(LINEA, 'Da documentare'),
         LineHeader('9', 'Le linee da documentare', 'Impalcatura · %d schede vuote'
                    % len(da), LINEA),
         SP(10),
         P('Di ognuna delle <b>%d linee</b> qui sotto si conoscono soltanto il settore e '
           'la lunghezza di catalogo. Nessuna ripresa di montaggio, nessuna trascrizione, '
           'nessun fotogramma: sono segnaposto dichiarati, non capitoli incompleti.'
           % len(da), lead),
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
            righe.append(two_cols(segnaposto(coppia[0]), segnaposto(coppia[1]))
                         if len(coppia) == 2 else segnaposto(coppia[0]))
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
