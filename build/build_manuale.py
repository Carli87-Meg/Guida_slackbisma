# -*- coding: utf-8 -*-
"""Guida alle highline della Pietra di Bismantova.

Assemblatore: qui c'e' solo l'ordine delle parti e l'apparato. Il contenuto sta
nei moduli, cosi' aggiungere una linea documentata non significa mettere le mani
in questo file.

    Parte 1  La Pietra          lo spot, la planimetria, il catalogo delle 24 linee
    Parte 2  Tecnica            cio' che vale per lo spot, non per una linea sola
    Parte 3  Le linee           il capitolo della 53 m + le schede di rilievo
    Parte 4  Apparato           fonti con le loro date, avvertenza finale

Regola del documento: **niente dati dedotti**. Ogni numero viene da una fonte
dichiarata — riprese, fotogrammi, catalogo i-pietra, locandina, risposte dirette
di chi ha montato. Il resto e' marcato [DA CONFERMARE] e raccolto in DUBBI.md.

    python build/build_manuale.py
"""
import io
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from schede_linee import parte_catalogo, nota_copertura             # noqa: E402
from scheda_53 import parte_53                                      # noqa: E402
from metodo import parte_metodo                                     # noqa: E402
import linee as REG                                                 # noqa: E402
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,   # noqa: E402
                                PageBreak, NextPageTemplate, Spacer,
                                KeepTogether)
from reportlab.pdfbase.pdfmetrics import stringWidth                # noqa: E402
from PIL import Image as _PILImage                                  # noqa: E402

OUT = RADICE / 'output' / 'Pietra_Bismantova_Highline.pdf'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'
ANN = RADICE / 'lavorazione' / 'frame_annotati'

LINEA = HexColor(0xF97316)
C_ANC = LC[1]
C_SOS = LC[7]
C_TEN = LC[3]

DC = '<font color="#B3261E">[DA CONFERMARE]</font>'


def dim(p):
    with _PILImage.open(p) as im:
        return im.size


def foto(nome, w, cap, color=None, ratio=None, focus=0.5):
    p = FOTO / nome if (FOTO / nome).exists() else ANN / nome
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


def spaziato(cv, x, y, testo, font, corpo, sp=1.9):
    """Testo spaziato sul canvas.

    `track()` di design.py serve ai Paragraph: produce entita' &nbsp; che dentro
    un drawString finirebbero stampate alla lettera.
    """
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
            'Ventiquattro linee su cinque aree:',
            'dove sono, e come si monta una linea.',
            'I dati che mancano sono dichiarati, e si aggiungono man mano.']):
        cv.drawString(LM, H - 324 - i * 15, r)

    cv.setFillColor(WHITE)
    spaziato(cv, LM, 92, 'EDIZIONE DI LAVORO', 'Pop-M', 7.6)
    cv.setFont('Lora', 8.6)
    cv.setFillColor(HexColor(0xD8D4CE))
    cv.drawString(LM, 74, '%d linee censite · %d con rigging documentato · '
                  'i dati non verificati sono marcati [DA CONFERMARE].'
                  % (c['totale'], c['documentate']))
    cv.drawString(LM, 60, 'Da completare con chi le ha montate.')


def page_begin(cv, doc):
    """Colore e sezione correnti.

    Prima qui si azzerava a ogni pagina: una sezione che proseguiva oltre la
    prima pagina perdeva l'etichetta in testatina e il filetto del piede tornava
    arancione anche dentro un capitolo blu. Il valore ora persiste finche' un
    Accent non lo cambia.
    """
    if not hasattr(cv, '_accent'):
        cv._accent = LINEA
        cv._sect = ''
    # La pagina comincia nella sezione in corso. Solo un Accent disegnato in
    # cima alla cornice la cambia (vedi Accent.drawOn in design.py).
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


NUMERI = {5: 'cinque', 6: 'sei', 7: 'sette', 8: 'otto', 9: 'nove'}


def FONTI():
    """Le fonti della guida, una riga per fonte.

    Sono una lista sola perche' le usano due posti: la tabella dell'apparato e
    la riga dell'indice che dice quante sono. Prima l'indice diceva «sei» a
    mano, e aggiungere una fonte lo avrebbe smentito.
    """
    return [
        ['42 video del montaggio', 'Sequenza delle operazioni e manovre viste a mano, '
         'per la sola 53 m', '16/05/2026'],
        ['19 fotografie', 'Ancoraggio, ferramenta con marcature leggibili, linea montata',
         '16/05/2026'],
        ['Locandina «La Pietra»', 'Le cinque aree e le ventiquattro linee', 'non datata'],
        ['Catalogo i-pietra (snapshot)', 'Settore, tipo di roccia, prima ricognizione',
         '05/08/2026'],
        ['Render 3D i-pietra', 'Viste dei cinque settori, copertura reale del catalogo',
         '20/08/2026'],
        ['Risposte di chi ha montato', 'Luogo, tipo di ancoraggio, nome di lavoro',
         '19/08/2026'],
        ['Panoramica i-pietra, settori segnati a mano', 'Posizione e ordine dei cinque '
         'settori lungo la cresta', '21/08/2026'],
    ]


# Capitoli di ogni parte: li usano sia l'indice sia i frontespizi di parte,
# cosi' i due elenchi non possono andare fuori sincrono.
CAPITOLI = []


def _voci(num):
    for n, _t, _col, _st, voci in CAPITOLI:
        if n == num:
            return voci
    return ()


ALTEZZA_PAGINA = H - TM - BM


def _pag(chiave):
    """Cella con il numero di pagina, allineata a destra."""
    return Paragraph('<font name="Pop-B" size="8.6">%s</font>' % rif(chiave),
                     ParagraphStyle('pg', fontName='Pop', leading=11,
                                    textColor=LINEA, alignment=TA_RIGHT))


def elenco_capitoli():
    """Indice a due livelli: le quattro parti e, sotto ognuna, i suoi capitoli.

    Ogni parte e' un blocco a se': cosi' una testata di parte non puo' restare
    in fondo alla pagina con i suoi capitoli voltati.
    """
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
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, 0), 1.2, col),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7)]
        for r, (chiave, titolo, nota) in enumerate(voci, start=1):
            righe.append([
                Paragraph('<font name="Pop-M" size="9">%s</font>' % titolo,
                          ParagraphStyle('ct', fontName='Pop', leading=12.5)),
                Paragraph(nota, small),
                Paragraph('<font name="Pop-M" size="9" color="#%s">%s</font>'
                          % (col.hexval()[2:], rif(chiave)),
                          ParagraphStyle('cn', fontName='Pop', leading=12.5,
                                         alignment=TA_RIGHT))])
            stile.append(('TOPPADDING', (0, r), (-1, r), 6))
            if r < len(voci):
                stile.append(('LINEBELOW', (0, r), (-1, r), 0.4, HAIR))
        t = Table(righe, colWidths=[152, FW - 152 - 46, 46])
        t.setStyle(TableStyle(stile))
        fuori.append(KeepTogether([t, SP(13)]))
    return fuori


def sec(S, color, label):
    S.append(Accent(color, label))


def sommario_parte(voci, color):
    """Elenco dei capitoli di una parte, con il numero di pagina.

    Il frontespizio di parte era una pagina quasi bianca. Ora dice che cosa
    contiene la parte e a che pagina, e diventa il secondo livello dell'indice.
    """
    righe = []
    for chiave, titolo, nota in voci:
        righe.append([Paragraph('<font name="Pop-M" size="9.4">%s</font>' % titolo,
                                ParagraphStyle('vt', fontName='Pop', leading=13)),
                      Paragraph(nota, small),
                      Paragraph('<font name="Pop-B" size="9.4" color="#%s">%s</font>'
                                % (color.hexval()[2:], rif(chiave)),
                                ParagraphStyle('vp', fontName='Pop', leading=13,
                                               alignment=TA_RIGHT))])
    t = Table(righe, colWidths=[150, FW - 150 - 54, 54])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HAIR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


def parte(S, num, titolo, sommario, color=LINEA, voci=()):
    """Frontespizio di parte: separa le quattro sezioni della guida.

    Il blocco viene centrato verticalmente. Prima partiva da un rientro fisso e
    finiva a un terzo dell'altezza, con il resto della pagina vuoto sotto: non
    era una pagina di apertura, era una pagina interrotta.
    """
    blocco = [LineHeader(num, titolo, 'Parte %s' % num, color),
              SP(16),
              P(sommario, lead)]
    if voci:
        blocco += [SP(26),
                   P('<font name="Pop-M" size="7.4" color="#%s">IN QUESTA PARTE</font>'
                     % MUT.hexval()[2:],
                     ParagraphStyle('ip', fontName='Pop', leading=11)),
                   SP(6),
                   sommario_parte(voci, color)]
    alto = sum(f.wrap(FW, ALTEZZA_PAGINA)[1] for f in blocco)
    S.append(Accent(color, titolo))
    S.append(Segna('parte%s' % num))
    S.append(SP(max(24, (ALTEZZA_PAGINA - alto) / 2)))
    S.extend(blocco)
    S.append(PageBreak())


def costruisci():
    """La storia completa del manuale.

    E' una funzione e non codice a livello di modulo perche' il documento viene
    impaginato piu' volte: la prima passata scopre a che pagina cade ogni
    capitolo, le successive stampano quei numeri nell'indice e nei rimandi.
    """
    S = []
    _c = REG.conteggi()
    _da_fare = _c['totale'] - _c['documentate']
    fonti = FONTI()
    CAPITOLI[:] = [
        ('1', 'Lo spot', LINEA, 'completo', [
            ('spot', 'La Pietra di Bismantova', 'Il massiccio e i numeri dello spot'),
            ('catalogo', 'Le linee della Pietra',
             'I cinque settori sulla cresta, con le loro linee')]),
        ('2', 'Come si monta una linea', C_SOS, 'parziale', [
            ('lati', 'Una linea, due lati', 'Lato tensione e lato opposto'),
            ('materiale', 'Prima di uscire: il materiale', 'La lista per una linea'),
            ('sequenza', 'La sequenza di montaggio', 'Le fasi in ordine'),
            ('ancoraggi', 'Gli ancoraggi su roccia', 'Placchette, punti, controlli'),
            ('soste', 'Le soste: main e backup', 'Il codice colore, la portata'),
            ('slinga', 'Instradamento della slinga', 'Il nodo che forza la slinga'),
            ('lineavita', 'Portare la linea, la linea vita', 'Tagline e corda azzurra'),
            ('tensione', 'Il lato tensione', 'Weblock, blocco del backup, anti-slip'),
            ('aframe', 'L’A-frame', 'I due pali sul bordo'),
            ('smontaggio', 'Lo smontaggio', 'Da documentare')]),
        ('3', 'Le linee', LINEA, '1 linea su %d' % _c['totale'], [
            ('cap53', 'Anfiteatro 53 m, «la 50»',
             'Dati, posizione, fotografie in opera')]),
        ('4', 'Apparato', LINEA, 'completo', [
            ('glossario', 'Il gergo del gruppo', 'Come si chiamano le cose sul campo'),
            ('fonti', 'Da dove viene ogni dato',
             'Le %s fonti con la loro data, e l’avvertenza finale'
             % NUMERI.get(len(fonti), str(len(fonti))))]),
    ]

    # ================================================================ copertina
    S.append(Spacer(1, 1))
    S.append(NextPageTemplate('main'))
    S.append(PageBreak())

    # ================================================================ indice
    sec(S, LINEA, 'Indice')
    S.append(Segna('indice'))
    S.append(LineHeader('', 'Che cosa c’è in questa guida', 'Indice', LINEA))
    S.append(SP(12))
    _c = REG.conteggi()
    # Un indice solo, a due livelli. Prima c'erano due elenchi sulla stessa
    # pagina — le quattro parti qui e gli stessi titoli piu' sotto — e il
    # secondo faceva traboccare l'indice su una pagina in piu'.
    S.extend(elenco_capitoli())
    S.append(SP(16))
    S.append(callout('Una guida che si compila',
                     'Ciò che manca è marcato %s: si completa sul campo, con chi monta, e '
                     'non si deduce. Per le %d linee non ancora documentate c’è un fascicolo '
                     'a parte di schede di rilievo, da compilare sul posto.' % (DC, _da_fare),
                     LINEA))
    S.append(PageBreak())

    # ================================================================ PARTE 1
    # La Parte 1 non ha frontespizio: viene subito dopo l'indice, che ne mostra
    # gia' il contenuto, e una pagina con il solo titolo era una pagina in piu'.
    sec(S, LINEA, 'Lo spot')
    S.append(Segna('parte1'))
    S.append(Segna('spot'))
    S.append(LineHeader('', 'La Pietra di Bismantova', 'Castelnovo ne’ Monti, Reggio Emilia',
                        LINEA))
    S.append(SP(10))
    S.append(P('La Pietra è un massiccio isolato dell’Appennino reggiano, a pareti verticali. '
               'Le highline sono raccolte in <b>cinque aree</b> e contate in <b>%d linee</b>, dai '
               'diciotto metri della Rookie ai centosessantacinque della Despedida.'
               % _c['totale'], lead))
    S.append(SP(10))
    S.append(data_table(
        ['Voce', 'Valore', 'Fonte'],
        [['Località', 'Pietra di Bismantova, Castelnovo ne’ Monti (RE)', 'chi ha montato'],
         ['Roccia', 'Arenaria', 'i-pietra, scheda di settore'],
         ['Aree con highline', '%d' % len(REG.AREE), 'locandina'],
         ['Linee censite', '%d' % _c['totale'], 'locandina'],
         ['Di cui in i-pietra', '%d' % _c['in_ipietra'], 'render 20/08/2026'],
         ['Rigging documentato', '%d' % _c['documentate'], 'questa guida'],
         ['Accesso e avvicinamento', '[DA CONFERMARE]', '—'],
         ['Autorizzazioni, divieti stagionali', '[DA CONFERMARE]', '—']],
        [140, 256, 95], LINEA))
    S.append(SP(8))
    S.append(P('Accesso e autorizzazioni restano vuoti di proposito. La Pietra è area '
               'protetta e falesia storica: vincoli, divieti stagionali e accordi entrano '
               'qui solo quando li fornisce chi frequenta lo spot, mai per deduzione.', small))
    # il catalogo prosegue sulla stessa pagina, aperto dalla sua testata
    S.append(SP(26))

    # parte_catalogo() include gia' la planimetria: chiamarle entrambe la stampava due volte
    S.extend(parte_catalogo())

    # ================================================================ PARTE 2
    # parte_catalogo() non chiude con un'interruzione: senza questa, il frontespizio
    # della parte finiva in coda alla pagina precedente invece di aprirne una nuova.
    # La parte «Tecnica» non c'e' piu': roccia e ancoraggi stanno nel metodo, il
    # glossario nell'apparato.
    S.append(PageBreak())
    parte(S, '2', 'Come si monta una linea', 'Il metodo con cui il gruppo monta una linea '
          'alla Pietra, dagli ancoraggi all’anti-slip, documentato sulla 53 m '
          'dell’Anfiteatro. Ciò che manca è marcato [DA CONFERMARE] e si aggiunge man mano.',
          C_SOS, voci=_voci('2'))
    S.extend(parte_metodo())

    # ================================================================ PARTE 3
    parte(S, '3', 'Le linee', 'Una scheda per linea: dove sta, quanto è lunga, com’è '
          'ancorata, che cosa manca. Per ora è completa quella della 53 m dell’Anfiteatro; '
          'le altre %d hanno una scheda di rilievo da compilare, nel fascicolo a parte.'
          % _da_fare, LINEA, voci=_voci('3'))

    S.extend(parte_53())

    # ================================================================ PARTE 4
    # Anche la Parte 4 non ha frontespizio: e' una pagina sola, e un titolo
    # davanti a una pagina sola raddoppia l'apparato senza aggiungere niente.
    sec(S, LINEA, 'Glossario')
    S.append(Segna('parte4'))
    S.append(Segna('glossario'))
    S.append(LineHeader('', 'Il gergo del gruppo', 'Glossario', LINEA))
    S.append(SP(10))
    S.append(P('I termini come si dicono sul campo, con accanto il nome corrente.', lead))
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
         ['«slide next»', 'Termine non identificato, forma incerta: [DA CONFERMARE]']],
        [150, 341], LINEA))
    S.append(PageBreak())

    sec(S, LINEA, 'Fonti')
    S.append(Segna('fonti'))
    S.append(LineHeader('', 'Da dove viene ogni dato', 'Fonti e date', LINEA))
    S.append(SP(10))
    S.append(P('Le fonti non hanno tutte lo stesso peso, e una di esse cambia nel tempo: '
               'il catalogo i-pietra compare con la data della lettura, non come un fatto '
               'fisso.', lead))
    S.append(SP(12))
    S.append(data_table(['Fonte', 'Che cosa fornisce', 'Data'], fonti,
                        [150, 246, 95], LINEA))
    S.append(SP(10))
    S.append(P(nota_copertura(), small))
    S.append(SP(16))
    S.append(Rule(FW, 0.6, HAIR, 8))
    S.append(SP(10))
    S.append(P('<b>Avvertenza</b>', h3))
    S.append(SP(4))
    S.append(P('Highlining e slacklining comportano rischi. Questa guida documenta un montaggio '
               'già realizzato da persone esperte: non sostituisce formazione, esperienza '
               'diretta e verifica autonoma di ogni ancoraggio prima di ogni utilizzo.', lead))
    S.append(SP(10))
    S.append(P('A ciò si aggiunge un limite specifico di questa edizione. Di ventiquattro linee '
               'una sola è documentata, e lo è a partire da riprese non didattiche: contiene '
               'numerosi dati non verificati, marcati [DA CONFERMARE]. Le altre hanno soltanto '
               'una scheda di rilievo vuota. <b>Nessuna parte di questo documento va usata '
               'come riferimento operativo</b> finché quei campi non sono stati riempiti da '
               'chi ha eseguito il montaggio.', body))
    S.append(SP(12))
    S.append(P('Edizione di lavoro dell’8 ottobre 2026, ricostruita dalle riprese del montaggio '
               'del 16 maggio 2026. Sistema grafico ripreso dalla guida Sillschlucht.', small))

    return lega_testate(S)


# capitoli di ogni parte, per il sommario dei frontespizi
VOCI = {}


# ---------------------------------------------------------------- build
def impagina(destinazione):
    """Impagina la storia su `destinazione` e restituisce il numero di pagine."""
    doc = BaseDocTemplate(destinazione, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title='Guida alle highline della Pietra di Bismantova',
                          author='Ricostruzione dalle riprese del 16/05/2026')
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
    """Impagina piu' volte, finche' i rimandi di pagina non si assestano.

    La prima passata non conosce ancora i numeri di pagina: li scopre mentre
    impagina. La seconda li stampa, e cosi' facendo puo' spostare qualcosa; si
    ripete finche' la mappa non cambia piu', poi si scrive il file vero.
    """
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
