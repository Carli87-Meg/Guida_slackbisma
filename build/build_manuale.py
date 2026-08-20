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
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from schede_linee import (parte_catalogo, parte_rilievi,            # noqa: E402
                          tabella_aree, nota_copertura)
from scheda_53 import parte_53                                      # noqa: E402
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
            'Ventiquattro linee su cinque aree.',
            'Di una esiste la documentazione completa del montaggio;',
            'delle altre, una scheda da compilare sul campo.']):
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
    cv._accent = LINEA
    cv._sect = ''


def page_end(cv, doc):
    n = cv.getPageNumber()
    acc = getattr(cv, '_accent', LINEA)
    sect = getattr(cv, '_sect', '')
    cv.setFont('Pop-M', 7)
    cv.setFillColor(MUT)
    cv.drawString(LM, H - 44, 'PIETRA DI BISMANTOVA · GUIDA ALLE HIGHLINE')
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


S = []


def sec(color, label):
    S.append(Accent(color, label))


def parte(num, titolo, sommario, color=LINEA):
    """Frontespizio di parte: separa le quattro sezioni della guida."""
    S.append(Accent(color, titolo))
    S.append(SP(150))
    S.append(LineHeader(num, titolo, 'Parte %s' % num, color))
    S.append(SP(14))
    S.append(P(sommario, lead))
    S.append(PageBreak())


# ================================================================ copertina
S.append(Spacer(1, 1))
S.append(NextPageTemplate('main'))
S.append(PageBreak())

# ================================================================ indice
sec(LINEA, 'Indice')
S.append(LineHeader('', 'Che cosa c’è in questa guida', 'Indice', LINEA))
S.append(SP(12))
_c = REG.conteggi()
S.append(data_table(
    ['Parte', 'Contenuto', 'Stato'],
    [['1 · La Pietra', 'Lo spot, la planimetria dei cinque settori, il catalogo '
      'delle %d linee' % _c['totale'], 'completo'],
     ['2 · Tecnica', 'Roccia, ancoraggi, gergo e materiale: ciò che si è visto e '
      'su quante linee', 'parziale'],
     ['3 · Le linee', 'Il montaggio della 53 m dell’Anfiteatro, documentato · '
      'schede di rilievo per le altre %d' % (_c['totale'] - _c['documentate']),
      '1 su %d' % _c['totale']],
     ['4 · Apparato', 'Le fonti con le loro date, avvertenza finale', 'completo']],
    [96, 300, 95], LINEA))
S.append(SP(16))
S.append(callout('Una guida che si compila',
                 'Di ventiquattro linee, <b>una sola</b> ha una documentazione di rigging. '
                 'Le altre non sono capitoli mancanti ma <b>schede di rilievo</b>: i campi '
                 'vuoti della parte 3 sono fatti per essere riempiti sul posto, e riportati '
                 'poi nel registro <b>dati/linee.py</b>. La guida cresce man mano che le '
                 'linee vengono documentate.', LINEA))
S.append(SP(14))
S.append(P('<b>Come leggere i dati</b>', h3))
S.append(SP(5))
S.append(BU('Ogni numero porta la sua fonte. Dove la fonte è un catalogo che cambia '
            'nel tempo, porta anche la data della lettura.', LINEA))
S.append(BU('%s significa che il dato non compare in nessuna fonte. Non è una '
            'dimenticanza: è un campo vuoto dichiarato.' % DC, LINEA))
S.append(BU('Ciò che è stato osservato su una linea sola è attribuito a quella linea, '
            'non presentato come pratica dello spot.', LINEA))
S.append(PageBreak())

# ================================================================ PARTE 1
parte('1', 'La Pietra', 'Lo spot, i cinque settori e le ventiquattro linee censite. '
      'È la parte che risponde alla domanda «che cosa c’è, e dove».')

sec(LINEA, 'Lo spot')
S.append(LineHeader('', 'La Pietra di Bismantova', 'Castelnovo ne’ Monti, Reggio Emilia',
                    LINEA))
S.append(SP(10))
S.append(P('La Pietra è un massiccio isolato che si alza sulla pianura reggiana, con pareti '
           'verticali su tutti i lati. Le highline sono raccolte in <b>cinque aree</b> e '
           'contate in <b>%d linee</b>, dai diciotto metri della Rookie ai centosessantacinque '
           'della Despedida.' % _c['totale'], lead))
S.append(SP(10))
S.append(data_table(
    ['Voce', 'Valore', 'Fonte'],
    [['Località', 'Pietra di Bismantova, Castelnovo ne’ Monti (RE)', 'utente'],
     ['Roccia', 'Arenaria', 'i-pietra, scheda di settore'],
     ['Aree con highline', '%d' % len(REG.AREE), 'locandina'],
     ['Linee censite', '%d' % _c['totale'], 'locandina'],
     ['Di cui in i-pietra', '%d' % _c['in_ipietra'], 'render 20/08/2026'],
     ['Rigging documentato', '%d' % _c['documentate'], 'questo progetto'],
     ['Accesso e avvicinamento', '[DA CONFERMARE]', '—'],
     ['Autorizzazioni, divieti stagionali', '[DA CONFERMARE]', '—']],
    [140, 256, 95], LINEA))
S.append(SP(8))
S.append(P('Le due righe vuote non sono una svista. La Pietra è area protetta e falesia '
           'storica, e <b>CLAUDE.md</b> chiede di indicare vincoli e autorizzazioni solo se '
           'forniti, mai dedotti: finché non arrivano da chi frequenta lo spot, restano '
           'dichiarati mancanti.', small))
S.append(SP(14))
S.append(callout('Due nomi che possono ingannare',
                 '<b>«La 50».</b> Esiste una linea da 50 m al Settore Giallo <i>e</i> una '
                 'linea che all’Anfiteatro chiamano così. Citare sempre il settore.<br/>'
                 '<b>Anfite-altro.</b> La locandina la tiene separata, i-pietra la accorpa '
                 'dentro Anfiteatro: chi cerca partendo dall’app e chi parte dalla locandina '
                 'finiscono in due posti diversi.', WARN, '!', FW, True))
S.append(PageBreak())

# parte_catalogo() include gia' la planimetria: chiamarle entrambe la stampava due volte
S.extend(parte_catalogo())

# ================================================================ PARTE 2
# parte_catalogo() non chiude con un'interruzione: senza questa, il frontespizio
# della parte finiva in coda alla pagina precedente invece di aprirne una nuova.
S.append(PageBreak())
parte('2', 'Tecnica', 'Ciò che si è osservato e che ha ragionevolmente valore per lo spot, '
      'non per una linea sola: la roccia, il tipo di ancoraggio, il gergo del gruppo. '
      'Ogni voce dichiara su quante linee è stata vista.', C_ANC)

sec(C_ANC, 'Tecnica')
S.append(LineHeader('', 'La roccia e gli ancoraggi', 'Che cosa vale per lo spot', C_ANC))
S.append(SP(10))
S.append(P('Questa parte raccoglie ciò che si può ragionevolmente estendere oltre la linea '
           'da cui è stato osservato. È poca roba, e il motivo è semplice: <b>di un solo '
           'montaggio su ventiquattro esistono riprese</b>. Da un caso non si ricava la '
           'pratica di uno spot, quindi qui entra soltanto ciò che dipende dal luogo — la '
           'roccia, il tipo di attrezzatura fissa — e non dalle scelte di un pomeriggio.',
           lead))
S.append(SP(14))
S.append(data_table(
    ['Elemento', 'Che cosa si è osservato', 'Su quante linee'],
    [['Roccia', 'Arenaria: meno tenace del calcare, va valutata attorno al foro',
      'dato di settore'],
     ['Punti di ancoraggio', 'Placchetta metallica su bullone con dado esagonale: '
      'tassello meccanico, non spit a vite né resinato con occhiello', '1 su %d'
      % _c['totale']],
     ['Collegamento fra i punti', 'Corda annodata fra le placchette', '1 su %d'
      % _c['totale']],
     ['Numero di punti', 'Tre, sul lato documentato', '1 su %d' % _c['totale']]],
    [104, 292, 95], C_ANC))
S.append(SP(12))
S.append(foto('D2_placchetta_dettaglio.jpg', FW,
              'Placchetta e dado esagonale · Anfiteatro 53 m, 16/05/2026', C_ANC))
S.append(SP(14))
# una lista di controlli spezzata a meta' fra due pagine e' una lista che si
# smette di leggere: resta unita.
S.append(KeepTogether([
    P('<b>Controlli prima di caricare un punto</b>', h3),
    SP(5),
    BU('Che il dado sia serrato e non presenti gioco.', C_ANC),
    BU('Che la placchetta non ruoti sul bullone.', C_ANC),
    BU('Che la roccia attorno al foro non presenti fratture o sfaldature.', C_ANC),
    BU('Che non vi sia corrosione visibile su placchetta, dado o bullone.', C_ANC)]))
S.append(SP(10))
S.append(P('Questo elenco discende dal <i>tipo</i> di ancoraggio osservato, non da una '
           'procedura dettata nelle riprese: nessuno, nei video, enuncia una lista di '
           'controlli. La checklist realmente usata dal gruppo è ' + DC + '.', small))
S.append(PageBreak())

sec(C_ANC, 'Tecnica')
S.append(LineHeader('', 'Il gergo del gruppo', 'Glossario operativo', C_ANC))
S.append(SP(10))
S.append(P('I termini sono riportati come vengono pronunciati sul campo, con accanto il '
           'nome corrente. Vale per chiunque monti alla Pietra con questo gruppo, ed è per '
           'questo che sta qui e non nel capitolo di una linea.', lead))
S.append(SP(10))
S.append(data_table(
    ['Come lo chiamano', 'Che cos’è'],
    [['slinga, slinghe', 'Braca ad anello industriale, calza tubolare'],
     ['banana', 'Weblock, il bloccante del lato tensione'],
     ['BFK', 'Moschettone d’acciaio di grandi dimensioni'],
     ['delta', 'Maglia rapida a forma di delta'],
     ['sosta main', 'Ancoraggio principale'],
     ['sosta backup', 'Ancoraggio di sicurezza, indipendente'],
     ['anti-slip', 'Nodo che impedisce lo slittamento della linea nel weblock'],
     ['tag, tagline', 'Cordino di servizio per portare la linea da un lato all’altro'],
     ['linea vita', 'Corda di sicurezza per chi si muove sull’ancoraggio'],
     ['ingrillare', 'Collegare con un grillo'],
     ['paranchino', 'Piccolo paranco di tensionamento'],
     ['«slide next»', 'Termine non identificato: trascrizione incerta [DA CONFERMARE]']],
    [150, 341], C_ANC))
S.append(PageBreak())

# ================================================================ PARTE 3
parte('3', 'Le linee', 'Una scheda per ognuna delle %d linee. La 53 m dell’Anfiteatro ha il '
      'capitolo completo del suo montaggio; le altre %d hanno i campi da compilare sul '
      'campo.' % (_c['totale'], _c['totale'] - _c['documentate']), C_SOS)

S.extend(parte_53())
S.extend(parte_rilievi())

# ================================================================ PARTE 4
parte('4', 'Apparato', 'Le fonti da cui viene ogni dato, con le loro date, e l’avvertenza '
      'che chiude il documento.', LINEA)

sec(LINEA, 'Fonti')
S.append(LineHeader('', 'Da dove viene ogni dato', 'Fonti e date', LINEA))
S.append(SP(10))
S.append(P('Le fonti non hanno tutte lo stesso peso, e una di esse cambia nel tempo. Per '
           'questo il catalogo i-pietra compare qui con la data della lettura, non come '
           'un fatto fisso.', lead))
S.append(SP(12))
S.append(data_table(
    ['Fonte', 'Che cosa fornisce', 'Data'],
    [['42 video del montaggio', 'Sequenza delle operazioni e manovre viste a mano, '
      'per la sola 53 m', '16/05/2026'],
     ['19 fotografie', 'Ancoraggio, ferramenta con marcature leggibili, linea montata',
      '16/05/2026'],
     ['Locandina «La Pietra»', 'Le cinque aree e le ventiquattro linee', 'non datata'],
     ['Catalogo i-pietra (snapshot)', 'Settore, tipo di roccia, prima ricognizione',
      '05/08/2026'],
     ['Render 3D i-pietra', 'Planimetria dei settori, copertura reale del catalogo',
      '20/08/2026'],
     ['Risposte di chi ha montato', 'Luogo, tipo di ancoraggio, nome di lavoro',
      '19/08/2026']],
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
           'numerosi dati non verificati, marcati [DA CONFERMARE]. Le schede delle altre '
           'linee sono moduli vuoti, non descrizioni. <b>Nessuna parte di questo documento '
           'va usata come riferimento operativo</b> finché quei campi non sono stati '
           'riempiti da chi ha eseguito il montaggio.', body))
S.append(SP(12))
S.append(P('Edizione di lavoro generata dalle riprese del 16 maggio 2026. Sistema grafico '
           'ereditato dalla guida Sillschlucht. Il registro delle linee sta in '
           'dati/linee.py, i dati ancora aperti in DUBBI.md.', small))

# ---------------------------------------------------------------- build
OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM,
                      title='Guida alle highline della Pietra di Bismantova',
                      author='Ricostruzione dalle riprese del 16/05/2026')
frame = Frame(LM, BM, FW, H - TM - BM, id='n',
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id='cover', frames=[Frame(LM, BM, FW, 24, id='c', leftPadding=0,
                                           rightPadding=0, topPadding=0, bottomPadding=0)],
                 onPage=cover),
    PageTemplate(id='main', frames=[frame], onPage=page_begin, onPageEnd=page_end),
])
doc.build(S)
print('scritto %s' % OUT)
