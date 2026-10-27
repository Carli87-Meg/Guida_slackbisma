# -*- coding: utf-8 -*-
"""Guida alle highline della Pietra di Bismantova.

Assemblatore: qui c'e' solo l'ordine delle parti e l'apparato. Il contenuto sta
nei moduli e nei dati, cosi' aggiungere una linea documentata non significa
mettere le mani in questo file.

    Come leggere     i livelli di documentazione, i marcatori, i nomi, l'avvertenza
    Indice
    Parte 1  La Pietra          lo spot, accesso e regole (dichiarati vuoti), i settori
    Parte 2  Le linee           la tavola di stato, una pagina per settore con le schede
                                delle sue linee (schede_linee.py, scheda_linea.py)
    Parte 3  Come si monta      il metodo Bisma, sei capitoli (metodo.py)
    Parte 4  Apparato           glossario, protocollo di rilievo, fonti, avvertenza, edizioni

Le schede di rilievo delle linee non documentate e il foglio dello spot escono in
un fascicolo a parte (build_schede_rilievo.py), costruito anche da qui alla fine.

Regola del documento: **niente dati dedotti**. Ogni numero viene da una fonte
dichiarata — riprese, fotogrammi, catalogo i-pietra, locandina, risposte dirette
di chi ha montato. Il resto e' marcato e raccolto in DUBBI.md.

    python build/build_manuale.py
"""
import io
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from schede_linee import (parte_linee, nota_copertura, nota_settori,   # noqa: E402
                          vista_insieme, pagina_protocollo)
from scheda_linea import (LINEA, C_MET, C_AREA, C_LIVELLO, T, marca,   # noqa: E402
                          dim, ha_scheda)
from metodo import parte_metodo                                     # noqa: E402
import linee as REG                                                 # noqa: E402
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,   # noqa: E402
                                PageBreak, NextPageTemplate, Spacer,
                                KeepTogether, Paragraph)
from reportlab.pdfbase.pdfmetrics import stringWidth                # noqa: E402

OUT = RADICE / 'output' / 'Pietra_Bismantova_Highline.pdf'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'

# Le edizioni della guida: numero, data, che cosa e' cambiato. L'ultima e' quella
# stampata in copertina e nel colophon.
EDIZIONI = [
    ('0.1', 'agosto 2026', 'Prima bozza: la 53 m dalle riprese del 16 maggio, il catalogo '
                           'dalla locandina e dai render i-pietra'),
    ('0.2', '8 ottobre 2026', 'Revisione su Figma: il metodo separato dalla scheda, le schede '
                              'di rilievo in un fascicolo a parte'),
    ('0.3', '27 ottobre 2026', 'Verifica delle fonti: GAS-OH e «Anfite-altro», il lato di '
                               'tensione, le fotografie del gruppo'),
    ('0.4', '27 ottobre 2026', 'Ristrutturazione: livelli di documentazione, codici delle '
                               'linee, una scheda per linea nel suo settore, metodo in sei '
                               'capitoli, protocollo di rilievo'),
]
EDIZIONE, DATA_EDIZIONE, _ = EDIZIONI[-1]
A_CURA = 'Bismaliners'


def spaziato(cv, x, y, testo, font, corpo, sp=1.9):
    """Testo spaziato sul canvas (track() di design.py serve ai Paragraph)."""
    cv.setFont(font, corpo)
    for ch in testo:
        cv.drawString(x, y, ch)
        x += stringWidth(ch, font, corpo) + (sp * 2.4 if ch == ' ' else sp)
    return x


# ---------------------------------------------------------------- copertina
def cover(cv, doc):
    p = FOTO / 'IMG_1396.jpg'
    ow, oh = dim(p)
    sh = H
    sw = sh * ow / oh
    cv.saveState()
    cv.drawImage(str(p), (W - sw) / 2, 0, sw, sh, preserveAspectRatio=False, mask=None)
    cv.setFillColor(HexColor(0x14181C))
    cv.setFillAlpha(0.44)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    # Sfumatura in basso: il piede di copertina cadeva sul prato illuminato e il
    # testo chiaro non si leggeva. Si scurisce solo la fascia che lo ospita.
    fascia, passi = 190.0, 48
    for i in range(passi):
        cv.setFillAlpha(0.60 * ((passi - i) / passi) ** 1.7)
        cv.rect(0, fascia * i / passi, W, fascia / passi + 0.6, stroke=0, fill=1)
    cv.setFillAlpha(1)
    cv.restoreState()

    c = REG.conteggi()
    cv.setFillColor(LINEA)
    cv.rect(LM, H - 176, 54, 4, stroke=0, fill=1)
    cv.setFillColor(WHITE)
    spaziato(cv, LM, H - 200, 'CASTELNOVO NE’ MONTI · REGGIO EMILIA', 'Pop-M', 8.6)
    cv.setFont('Pop-B', 37)
    cv.drawString(LM, H - 248, 'Guida alle highline')
    cv.setFont('Pop-L', 27)
    cv.drawString(LM, H - 286, 'della Pietra di Bismantova')

    cv.setFont('Lora', 10.4)
    cv.setFillColor(HexColor(0xE8E5E0))
    for i, r in enumerate([
            'Ventiquattro linee su cinque settori:',
            'dove sono, che cosa se ne sa, come si monta una linea.',
            'I dati che mancano sono dichiarati, e si aggiungono man mano.']):
        cv.drawString(LM, H - 324 - i * 15, r)
    cv.setFillColor(WHITE)
    spaziato(cv, LM, H - 384, 'A CURA DEI %s' % A_CURA.upper(), 'Pop-M', 8.6)

    cv.setFillColor(WHITE)
    spaziato(cv, LM, 92, 'EDIZIONE DI LAVORO %s · %s' % (EDIZIONE, DATA_EDIZIONE.upper()),
             'Pop-M', 7.6)
    cv.setFont('Lora', 8.6)
    cv.setFillColor(HexColor(0xD8D4CE))
    cv.drawString(LM, 74, '%d linee censite · %d documentata · %d fotografate · '
                  'i dati non verificati sono marcati.'
                  % (c['totale'], c['documentata'], c['fotografata']))
    cv.drawString(LM, 60, 'Da completare con chi le ha montate.')


def page_begin(cv, doc):
    """Colore e sezione correnti: persistono finche' un Accent non li cambia."""
    if not hasattr(cv, '_accent'):
        cv._accent = LINEA
        cv._sect = ''
    cv._sect_pagina = cv._sect
    cv._accent_pagina = cv._accent
    cv._cima_cornice = H - TM


def page_end(cv, doc):
    n = cv.getPageNumber()
    acc = getattr(cv, '_accent_pagina', getattr(cv, '_accent', LINEA))
    sect = getattr(cv, '_sect_pagina', getattr(cv, '_sect', ''))
    cv.setFont('Pop-M', 7)
    cv.setFillColor(MUT)
    cv.drawString(LM, H - 44, getattr(doc, 'testata',
                                      'PIETRA DI BISMANTOVA · GUIDA ALLE HIGHLINE'))
    cv.drawRightString(W - RM, H - 44, sect.upper())
    cv.setStrokeColor(HAIR)
    cv.setLineWidth(0.6)
    cv.line(LM, H - 54, W - RM, H - 54)
    cv.line(LM, 46, W - RM, 46)
    cv.setFillColor(acc)
    cv.rect(LM, 46, 26, 2.5, stroke=0, fill=1)
    cv.setFillColor(INK)
    cv.setFont('Pop-B', 9)
    cv.drawRightString(W - RM, 30, str(n))


NUMERI = {1: 'una', 2: 'due', 3: 'tre', 4: 'quattro', 5: 'cinque', 6: 'sei', 7: 'sette',
          8: 'otto', 9: 'nove', 10: 'dieci', 11: 'undici', 12: 'dodici', 13: 'tredici',
          14: 'quattordici', 15: 'quindici'}


def FONTI():
    """Le fonti della guida, una riga per fonte, con la data."""
    return [
        ['42 video del montaggio', 'Sequenza e manovre viste a mano, sulla sola 53 m',
         '16/05/2026'],
        ['19 fotografie', 'Ancoraggio, ferramenta e marcature, linea montata',
         '16/05/2026'],
        ['Locandina «La Pietra»', 'Le cinque aree e le ventiquattro linee; la cima a 1047 m',
         'non datata'],
        ['Catalogo i-pietra (snapshot)', 'Settore, tipo di roccia, prima ricognizione',
         '05/08/2026'],
        ['Render 3D i-pietra', 'Viste dei cinque settori, con 22 linee tracciate',
         '20/08/2026'],
        ['Risposte di chi ha montato', 'Luogo, tipo di ancoraggio, nome di lavoro',
         '19/08/2026'],
        ['Panoramica i-pietra annotata', 'Posizione e ordine dei settori, segnati a mano',
         '21/08/2026'],
        ['Fotografie del 22 agosto', 'L’altro capo della 53 m, montata con i bungee',
         '22/08/2026'],
        ['Posizione GPS di foto e video', 'Su quale capo è stata girata ogni ripresa',
         'letta il 27/10/2026'],
        ['Risposte e scelte dell’utente', 'Lato di tensione; titolo GAS-OH; «Anfite-altro»; '
         'la struttura di questa edizione', '27/10/2026'],
        ['SlackMap (API)', 'Nome, lunghezza del segmento e coordinate dei capi di tutte e '
         '24 le linee, con gli id abbinati nel catalogo i-pietra; gli ancoraggi della 113 m',
         'letta il 27/10/2026'],
        ['Catalogo i-pietra', 'Le linee censite: tutte e 24', '21/10/2026'],
        ['File LineeBisma del gruppo', 'Lo schema «Ancoraggio standard Bisma» e 31 fotografie '
         'sulle righe di sette linee: tutto «da controllare»', '20/10/2026'],
    ]


# Capitoli di ogni parte: li usano l'indice e i rimandi, cosi' non vanno fuori sincrono.
CAPITOLI = []
ALTEZZA_PAGINA = H - TM - BM


def elenco_capitoli():
    """Indice a due livelli: le quattro parti e, sotto ognuna, i suoi capitoli."""
    fuori = []
    for num, titolo_parte, col, stato, voci in CAPITOLI:
        righe = [[
            Paragraph('<font name="Pop-B" size="10">Parte %s · %s</font>'
                      % (num, titolo_parte),
                      ParagraphStyle('cp', fontName='Pop', leading=14)),
            Paragraph('<font name="Pop-M" size="7.4" color="#%s">%s</font>'
                      % (MUT.hexval()[2:], stato.upper()),
                      ParagraphStyle('cs', fontName='Pop', leading=14)),
            Paragraph('<font name="Pop-B" size="10" color="#%s">%s</font>'
                      % (col.hexval()[2:], rif('parte%s' % num)),
                      ParagraphStyle('cq', fontName='Pop', leading=14,
                                     alignment=TA_RIGHT))]]
        stile = [
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            # aria fra il titolo e la nota: «anti-slip» toccava «E l'A-frame»
            ('RIGHTPADDING', (0, 0), (0, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, 0), 1.2, col),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6)]
        for r, (chiave, titolo, nota) in enumerate(voci, start=1):
            righe.append([
                Paragraph('<font name="Pop-M" size="9">%s</font>' % titolo,
                          ParagraphStyle('ct', fontName='Pop', leading=12.5)),
                Paragraph(nota, small),
                Paragraph('<font name="Pop-M" size="9" color="#%s">%s</font>'
                          % (col.hexval()[2:], rif(chiave)),
                          ParagraphStyle('cn', fontName='Pop', leading=12.5,
                                         alignment=TA_RIGHT))])
            stile.append(('TOPPADDING', (0, r), (-1, r), 5))
            if r < len(voci):
                stile.append(('LINEBELOW', (0, r), (-1, r), 0.4, HAIR))
        t = Table(righe, colWidths=[172, FW - 172 - 46, 46])
        t.setStyle(TableStyle(stile))
        fuori.append(KeepTogether([t, SP(12)]))
    return fuori


def sec(S, color, label):
    S.append(Accent(color, label))


def _h3(t):
    return P('<b>%s</b>' % t, h3)


AVVERTENZA = ('Highlining e slacklining comportano rischi. Questa guida documenta un '
              'montaggio già realizzato da persone esperte: non sostituisce formazione, '
              'esperienza diretta e verifica autonoma di ogni ancoraggio prima di ogni '
              'utilizzo.')


def _voci_parte2(c):
    voci = [('stato', 'Tavola di stato', 'Le %d linee: livello di documentazione e dove '
                                         'trovarle' % c['totale'])]
    for area in REG.AREE:
        ls = REG.per_area(area)
        n_doc = sum(1 for l in ls if REG.livello(l) >= REG.RILEVATA)
        n_fot = sum(1 for l in ls if REG.livello(l) == REG.FOTOGRAFATA)
        nota = '%d linee' % len(ls)
        if n_doc:
            nota += ' · %d documentata' % n_doc if n_doc == 1 else ' · %d documentate' % n_doc
        if n_fot:
            nota += ' · %d fotografate' % n_fot if n_fot > 1 else ' · 1 fotografata'
        voci.append(('settore:%s' % area, area, nota))
        for l in ls:
            if ha_scheda(l):
                liv = REG.livello(l)
                nota = ('Scheda completa: ancoraggi, materiale, A-frame, varianti'
                        if liv == REG.DOCUMENTATA else
                        'Dalle fotografie del gruppo: dove corre, i capi, che cosa si vede')
                voci.append(('linea:%s' % l['id'], '%s · %s · %d m'
                             % (REG.titolo(l), l['codice'], l['lunghezza']), nota))
    return voci


def costruisci():
    """La storia completa della guida, impaginata piu' volte per i rimandi."""
    S = []
    c = REG.conteggi()
    fonti = FONTI()
    CAPITOLI[:] = [
        ('1', 'La Pietra', LINEA, 'accesso e regole da compilare', [
            ('spot', 'La Pietra di Bismantova', 'Lo spot; accesso e regole, ancora vuoti'),
            ('settori', 'I cinque settori', 'La vista d’insieme, nell’ordine della cresta')]),
        ('2', 'Le linee', LINEA, '%d documentata · %d fotografate · %d censite'
         % (c['documentata'], c['fotografata'], c['censita']), _voci_parte2(c)),
        ('3', 'Come si monta: il metodo Bisma', C_MET, 'parziale', [
            ('m1', 'Lo schema e la sequenza', 'Due lati, dodici passi, tagline e linea vita'),
            ('m2', 'Il materiale', 'La lista per una linea; lo schema del gruppo'),
            ('m3', 'I punti su roccia', 'Placchette su bullone, la sosta su più punti'),
            ('m4', 'Le due soste del lato tensione', 'Main e backup, la slinga, la portata'),
            ('m5', 'Tensione, blocco del backup, anti-slip', 'E l’A-frame'),
            ('m6', 'Che cosa il metodo non copre ancora', 'Le domande per chi monta')]),
        ('4', 'Apparato', LINEA, 'completo', [
            ('glossario', 'Il gergo del gruppo', 'I termini del campo e quelli della guida'),
            ('protocollo', 'Protocollo di rilievo', 'Che cosa misurare e fotografare'),
            ('fonti', 'Da dove viene ogni dato',
             'Le %s fonti con la loro data, l’avvertenza, le edizioni'
             % NUMERI.get(len(fonti), str(len(fonti))))]),
    ]

    # ================================================================ copertina
    S.append(Spacer(1, 1))
    S.append(NextPageTemplate('main'))
    S.append(PageBreak())

    # ================================================================ come leggere
    sec(S, LINEA, 'Come leggere')
    S.append(Segna('leggere'))
    S.append(LineHeader('', 'Come leggere questa guida', 'Prima di tutto', LINEA))
    S.append(SP(10))
    S.append(P('Questa guida descrive le <b>ventiquattro highline</b> della Pietra di '
               'Bismantova e il <b>metodo</b> con cui i %s le montano. È un documento che si '
               'compila: ogni linea ha un livello di documentazione dichiarato, e ciò che '
               'nessuno ha visto o detto non c’è.' % A_CURA, lead))
    S.append(SP(14))
    S.append(_h3('I quattro livelli di documentazione'))
    S.append(SP(6))
    S.append(data_table(
        ['Livello', 'Che cosa si sa', 'Oggi'],
        [[livello_chip(REG.LIVELLI[k][0], C_LIVELLO[k]), Paragraph(REG.LIVELLI[k][1], td),
          Paragraph('%d' % c[REG.LIVELLI[k][0]], td)]
         for k in sorted(REG.LIVELLI, reverse=True)],
        [96, FW - 96 - 54, 54], LINEA))
    S.append(SP(14))
    S.append(_h3('I marcatori'))
    S.append(SP(5))
    S.append(BU('<font color="#%s">[DA CONFERMARE]</font>: un dato incerto, o contraddetto da '
                'un’altra fonte. Si chiede a chi ha montato.' % WARN.hexval()[2:], LINEA))
    S.append(BU('<font color="#%s">da rilevare</font>, o una cella vuota in tabella: un dato '
                'che nessuno ha ancora raccolto. Si compila sul posto, con il protocollo di '
                'rilievo a %s.' % (MUT.hexval()[2:], rif('protocollo')), LINEA))
    S.append(BU('Niente è dedotto. Una misura plausibile ma sbagliata, in un documento di '
                'rigging, è un rischio reale: un campo vuoto dichiarato vale di più.', LINEA))
    S.append(SP(14))
    S.append(_h3('I nomi delle linee'))
    S.append(SP(5))
    S.append(P('Ogni linea ha un <b>codice</b>: la sigla del settore e il numero d’ordine '
               'sulla locandina, per lunghezza crescente (%s). Accanto al codice c’è il nome '
               'che la linea ha su <b>SlackMap</b>, la mappa mondiale delle slackline, dove '
               'chi l’ha censita gliene ha dato uno; la lunghezza è sempre quella di '
               'catalogo. I soprannomi del gruppo stanno fra virgolette e mai da soli: '
               '<b>«la 50»</b> è GAS-OH, AN-4, e la Pietra ha anche una 50 m al Settore Giallo.'
               % ', '.join('%s %s' % (REG.CODICE_SETTORE[a], a) for a in REG.AREE), body))
    S.append(SP(16))
    S.append(callout('Avvertenza',
                     AVVERTENZA + ' <b>Nessuna parte di questo documento va usata come '
                     'riferimento operativo</b> finché i dati marcati non sono stati '
                     'confermati da chi ha eseguito il montaggio.', WARN, '!', FW, True))
    S.append(SP(16))
    # le edizioni stanno qui, dove si capisce quale si sta leggendo: in coda alle
    # fonti facevano da sole una pagina in piu'
    S.append(KeepTogether([_h3('Le edizioni'), SP(4)]
                          + [P('<b>%s</b> · %s — %s' % e, small) for e in EDIZIONI]))
    S.append(PageBreak())

    # ================================================================ indice
    sec(S, LINEA, 'Indice')
    S.append(Segna('indice'))
    S.append(LineHeader('', 'Che cosa c’è in questa guida', 'Indice', LINEA))
    S.append(SP(12))
    S.extend(elenco_capitoli())
    S.append(PageBreak())

    # ================================================================ PARTE 1
    sec(S, LINEA, 'La Pietra')
    S.append(Segna('parte1'))
    S.append(Segna('spot'))
    S.append(LineHeader('', 'La Pietra di Bismantova',
                        'Parte 1 · Castelnovo ne’ Monti, Reggio Emilia', LINEA))
    S.append(SP(10))
    S.append(P('La Pietra è un massiccio isolato dell’Appennino reggiano, a pareti verticali. '
               'Le highline sono raccolte in <b>cinque settori</b> e contate in <b>%d '
               'linee</b>, dai diciotto metri della Rookie ai centosessantacinque della '
               'Despedida.' % c['totale'], lead))
    S.append(SP(10))
    S.append(data_table(
        ['Voce', 'Valore', 'Fonte'],
        [['Località', 'Pietra di Bismantova, Castelnovo ne’ Monti (RE)', 'chi ha montato'],
         ['Cima', '1047 m', 'locandina'],
         ['Roccia', 'Arenaria', 'i-pietra, scheda di settore'],
         ['Settori con highline', '%d' % len(REG.AREE), 'locandina'],
         ['Linee censite', '%d' % c['totale'], 'locandina; i-pietra al %s' % REG.IPIETRA_DATA],
         ['Ancoraggi', 'Su roccia (la 53 m); su alberi o misti dove le fotografie del '
                       'gruppo lo mostrano', 'chi ha montato; foto del gruppo']],
        [140, 256, 95], LINEA))
    S.append(SP(18))
    S.append(KeepTogether([
        _h3('Accesso e regole'),
        SP(5),
        P('Le voci che seguono sono quelle che chi arriva da fuori cerca per prime, e sono '
          'vuote. La Pietra è area protetta e falesia storica: vincoli, divieti stagionali e '
          'accordi entrano qui solo quando li fornisce chi frequenta lo spot, mai per '
          'deduzione. Il foglio «Rilievo dello spot» del fascicolo raccoglie le domande.',
          body),
        SP(10),
        two_cols(
            gear_block('Accesso', [marca(x) for x in [
                'Avvicinamento a ciascun settore: da rilevare',
                'Parcheggio e punto di partenza: da rilevare',
                'Tempi di avvicinamento: da rilevare',
                'Rifugio, acqua, punti di appoggio: da rilevare']], LINEA),
            gear_block('Regole e contatti', [marca(x) for x in [
                'Autorizzazioni e accordi con il gestore: da rilevare',
                'Divieti stagionali, nidificazione: da rilevare',
                'Linee lasciate montate, notte, permarig: da rilevare',
                'Emergenze: numeri e punto di raccolta: da rilevare',
                'Chi tiene la guida nel gruppo: da rilevare']], LINEA))]))
    S.append(SP(10))
    S.append(P('Una planimetria con sentieri e settori non c’è ancora: la vista d’insieme '
               'della pagina seguente serve a riconoscere la parete, non a muoversi.', small))
    S.append(PageBreak())

    sec(S, LINEA, 'I settori')
    S.append(Segna('settori'))
    S.append(LineHeader('', 'I cinque settori', 'Da sinistra a destra, come stanno sulla '
                        'cresta', LINEA))
    S.append(SP(10))
    S.append(P('I settori seguono l’ordine in cui stanno sulla cresta, ed è l’ordine di tutta '
               'la guida: %s.' % ', '.join(REG.AREE), lead))
    S.append(SP(12))
    vista = vista_insieme()
    if vista is not None:
        ow, oh = dim(vista)
        S.append(PhotoStrip(str(vista), FW, ow, oh,
                            'I cinque settori sulla vista d’insieme i-pietra', LINEA))
        S.append(SP(8))
        S.append(P('Le pastiglie segnano <b>un tratto di parete, non un ancoraggio</b>: '
                   'servono a orientarsi, non a trovare un punto; l’altezza a cui cadono è '
                   'prospettiva, non quota. Le viste i-pietra delle pagine seguenti '
                   '<b>non sono planimetrie</b>: sono prospettive di un modello '
                   'fotogrammetrico, e servono a riconoscere dove corre una linea sulla '
                   'parete, non a misurarla.', small))
    else:
        S.append(P('La vista d’insieme dei settori non è disponibile.', small))
    S.append(SP(14))
    righe = []
    for area in REG.AREE:
        ls = REG.per_area(area)
        righe.append([livello_chip(REG.CODICE_SETTORE[area], C_AREA[area]),
                      Paragraph(area, td), Paragraph('%d' % len(ls), td),
                      Paragraph(' · '.join(str(l['lunghezza']) for l in ls), td),
                      Paragraph('<font name="Pop-M" size="8.2" color="#%s">%s</font>'
                                % (C_AREA[area].hexval()[2:], rif('settore:%s' % area)),
                                ParagraphStyle('sp', fontName='Pop', leading=11))])
    S.append(data_table(['Sigla', 'Settore', 'Linee', 'Lunghezze di catalogo (m)', 'Pagina'],
                        righe, [50, 120, 50, FW - 50 - 120 - 50 - 60, 60], LINEA))
    S.append(PageBreak())

    # ================================================================ PARTE 2
    S.extend(parte_linee())
    S.append(PageBreak())

    # ================================================================ PARTE 3
    S.append(Segna('parte3'))
    S.extend(parte_metodo())

    # ================================================================ PARTE 4
    sec(S, LINEA, 'Glossario')
    S.append(Segna('parte4'))
    S.append(Segna('glossario'))
    S.append(LineHeader('', 'Il gergo del gruppo', 'Parte 4 · Glossario e terminologia', LINEA))
    S.append(SP(10))
    S.append(P('I termini come si dicono sul campo, con accanto il nome corrente; poi i '
               'termini con cui questa guida descrive una linea.', lead))
    S.append(SP(10))
    S.append(data_table(
        ['Come lo chiamano', 'Che cos’è'],
        [['slinga, slinghe', 'Braca ad anello industriale, calza tubolare'],
         ['banana', 'Weblock, il bloccante del lato tensione'],
         ['BFK', 'Moschettone d’acciaio di grandi dimensioni'],
         ['delta', 'Maglia rapida a forma di delta'],
         ['sosta main', 'Ancoraggio principale'],
         ['sosta backup', 'Ancoraggio di sicurezza, indipendente'],
         ['blocco del backup', 'Collegamento che prende sosta main e sosta backup'],
         ['anti-slip', 'Nodo che impedisce lo slittamento della linea nel weblock'],
         ['tag, tagline', 'Cordino di servizio per portare la linea da un lato all’altro'],
         ['linea vita', 'Corda di sicurezza per chi si muove sull’ancoraggio'],
         ['ingrillare', 'Collegare con un grillo'],
         ['paranchino', 'Piccolo paranco di tensionamento'],
         ['cavalletto', 'L’A-frame, nel file del gruppo'],
         ['«la 50»', 'GAS-OH, la 53 m dell’Anfiteatro (AN-4). La 50 m del Settore Giallo '
                     'è SG-3, un’altra linea'],
         ['«slide next»', 'Termine non identificato, forma incerta: [DA CONFERMARE]']],
        [150, 341], LINEA))
    # righe strette in tutte e due le tabelle: cosi' stanno in una pagina sola
    S[-1].setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 4),
                               ('BOTTOMPADDING', (0, 1), (-1, -1), 4)]))
    S.append(SP(14))
    S.append(KeepTogether([
        _h3('I termini di questa guida'),
        SP(6),
        data_table(
            ['Termine', 'In questa guida'],
            [['linea', 'La highline: nastro, backup e leash, fra due ancoraggi'],
             ['lato', 'Uno dei due capi: il lato tensione, dove si tensiona; il lato statico, '
                      'l’altro'],
             ['ancoraggio', 'Tutto ciò che tiene un lato: le soste e i punti'],
             ['sosta', 'Un sistema di ancoraggio completo: sulla 53 m, la main e la backup '
                       'del lato tensione'],
             ['punto', 'Il singolo elemento fisso nella roccia: una placchetta su bullone'],
             ['codice', 'Sigla del settore e numero d’ordine sulla locandina: AN-4 è la '
                        'quarta linea dell’Anfiteatro'],
             ['lato A, lato B', 'Nelle schede di rilievo, i due capi finché non si sa quale '
                                'sia quello di tensione'],
             ['livello', 'Quanto si sa di una linea: censita, fotografata, rilevata, '
                         'documentata (%s)' % rif('leggere')]],
            [150, 341], LINEA)]))
    S[-1]._content[-1].setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 4),
                                            ('BOTTOMPADDING', (0, 1), (-1, -1), 4)]))
    S.append(PageBreak())

    sec(S, LINEA, 'Protocollo')
    S.append(Segna('protocollo'))
    S.extend(pagina_protocollo(LINEA))
    S.append(PageBreak())

    sec(S, LINEA, 'Fonti')
    S.append(Segna('fonti'))
    S.append(LineHeader('', 'Da dove viene ogni dato', 'Fonti e date', LINEA))
    S.append(SP(8))
    S.append(P('Le fonti non hanno tutte lo stesso peso, e una di esse cambia nel tempo: il '
               'catalogo i-pietra compare con la data della lettura, non come un fatto fisso.',
               lead))
    S.append(SP(10))
    tab = data_table(['Fonte', 'Che cosa fornisce', 'Data'], fonti, [150, 246, 95], LINEA)
    # righe strette: con tredici fonti il colophon scivolava da solo su una pagina
    tab.setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 4),
                             ('BOTTOMPADDING', (0, 1), (-1, -1), 4)]))
    S.append(tab)
    S.append(SP(8))
    S.append(P(nota_copertura() + ' ' + nota_settori(), small))
    S.append(SP(8))
    S.append(Rule(FW, 0.6, HAIR, 8))
    S.append(SP(8))
    S.append(_h3('Avvertenza'))
    S.append(SP(4))
    S.append(P(AVVERTENZA, lead))
    S.append(SP(6))
    S.append(P('A ciò si aggiunge un limite specifico di questa edizione. Di %d linee una '
               'sola è documentata, e lo è a partire da riprese non didattiche: contiene '
               'numerosi dati non verificati, marcati come tali. %s hanno fotografie del '
               'gruppo, che non documentano il montaggio; le altre hanno una scheda di '
               'rilievo da compilare. <b>Nessuna parte di questo documento va usata come '
               'riferimento operativo</b> finché quei campi non sono stati riempiti da chi '
               'ha eseguito il montaggio.'
               % (c['totale'], NUMERI.get(c['fotografata'], str(c['fotografata'])).capitalize()),
               body))
    S.append(SP(8))
    S.append(P('Edizione di lavoro %s del %s, a cura dei %s; le edizioni precedenti sono a %s. '
               'Le correzioni si segnalano a chi tiene la guida nel gruppo. Sistema grafico '
               'ripreso dalla guida Sillschlucht.'
               % (EDIZIONE, DATA_EDIZIONE, A_CURA, rif('leggere')), small))

    return lega_testate(S)


# ---------------------------------------------------------------- build
def impagina(destinazione):
    """Impagina la storia su `destinazione` e restituisce il numero di pagine."""
    doc = BaseDocTemplate(destinazione, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title='Guida alle highline della Pietra di Bismantova',
                          author=A_CURA)
    frame = Frame(LM, BM, FW, H - TM - BM, id='n',
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id='cover',
                     frames=[Frame(LM, BM, FW, 24, id='c', leftPadding=0,
                                   rightPadding=0, topPadding=0, bottomPadding=0)],
                     onPage=cover),
        PageTemplate(id='main', frames=[frame], onPage=page_begin,
                     onPageEnd=page_end),
    ])
    doc.build(costruisci())
    return doc.page


def main():
    """Impagina piu' volte, finche' i rimandi di pagina non si assestano."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for passata in range(1, 5):
        prima = dict(PAGINE)
        impagina(io.BytesIO())
        if PAGINE == prima and passata > 1:
            break
    n = impagina(str(OUT))
    print('scritto %s (%d pagine, %d rimandi risolti in %d passate)'
          % (OUT, n, len(PAGINE), passata))
    # la guida cita le schede di rilievo per numero: il fascicolo esce con lei
    import build_schede_rilievo
    build_schede_rilievo.main()


if __name__ == '__main__':
    main()
