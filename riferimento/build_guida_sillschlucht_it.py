# -*- coding: utf-8 -*-
from design import *
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, PageBreak,
                                NextPageTemplate, Flowable, Table, TableStyle,
                                Paragraph, Spacer)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = '/mnt/user-data/outputs/Sillschlucht_Guida_Highline_IT_design.pdf'
IMG = 'img/'

REG = 'https://www.slacklineverband.com/formulare/highline-formular/'
TIR = 'https://www.tiroliners.at/verein/mitglied-werden/'
C = {
    'l1t': 'https://goo.gl/maps/oLqUggsXowHxVyQ36',
    'l1s': 'https://goo.gl/maps/KXbWMeFbNepGXzbMA',
    'l2s': 'https://goo.gl/maps/MLtwDNWSX3e1Wpuz7',
    'l3s': 'https://maps.app.goo.gl/sh2fCLLMWBnRVt7x7',
    'l4s': 'https://maps.app.goo.gl/hYqsGjaUDHLtu5yh6',
    'l5s': 'https://goo.gl/maps/a6Ffk9eL4y4W7YnXA',
    'l6t': 'https://goo.gl/maps/thFq5PPXd85kJtPo6',
    'l6s': 'https://goo.gl/maps/EEyq8GSAkiRq8zdz5',
}
CO = {
    'l1t': '47.24386067263707, 11.395109044441732',
    'l1s': '47.243663878397996, 11.39616067574284',
    'l2s': '47.24344878613477, 11.395749458097908',
    'l3s': '47.24336304930371, 11.39575989200507',
    'l4s': '47.24333801179552, 11.395727705427749',
    'l5s': '47.24312156766332, 11.395540478213261',
    'l6t': '47.24370278344269, 11.39495062550069',
    'l6s': '47.242824095164174, 11.394620312920315',
}


# ---------------------------------------------------------------- flowable extra
class Checklist(Flowable):
    def __init__(self, items, color, w=FW, cols=2):
        self.items, self.c, self.w, self.cols = items, color, w, cols
        self.rows = (len(items) + cols - 1) // cols
        self.rh = 17
        self.h = self.rows * self.rh

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        cw = self.w / self.cols
        for i, t in enumerate(self.items):
            col, row = i % self.cols, i // self.cols
            x = col * cw
            y = self.h - (row + 1) * self.rh + 4
            cv.setStrokeColor(self.c)
            cv.setLineWidth(1)
            cv.rect(x, y + 0.5, 8, 8, stroke=1, fill=0)
            cv.setFillColor(INK2)
            cv.setFont('Lora', 8.7)
            s = t
            while stringWidth(s, 'Lora', 8.7) > cw - 26 and len(s) > 6:
                s = s[:-2]
            cv.drawString(x + 15, y + 2, s)


class KitCard(Flowable):
    """Card compatta: titolo + elenco compatto."""

    def __init__(self, title, items, color, w):
        self.t, self.items, self.c, self.w = title, items, color, w
        self.h = 26 + len(items) * 12.4 + 8

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        cv.setFillColor(PAPER)
        cv.rect(0, 0, self.w, self.h, stroke=0, fill=1)
        cv.setFillColor(self.c)
        cv.rect(0, self.h - 3, self.w, 3, stroke=0, fill=1)
        cv.setFillColor(INK)
        cv.setFont('Pop-M', 8.6)
        cv.drawString(10, self.h - 18, self.t)
        cv.setFont('Lora', 8.4)
        y = self.h - 32
        for it in self.items:
            cv.setFillColor(self.c)
            cv.circle(13, y + 3, 1.6, stroke=0, fill=1)
            cv.setFillColor(INK2)
            cv.drawString(20, y, it)
            y -= 12.4


class Lines(Flowable):
    def __init__(self, n, w=FW, gap=22):
        self.n, self.w, self.gap = n, w, gap
        self.h = n * gap

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        cv.setStrokeColor(HAIR)
        cv.setLineWidth(0.5)
        for i in range(self.n):
            y = self.h - (i + 1) * self.gap
            cv.line(0, y, self.w, y)



# ---------------------------------------------------------------- copertina
def cover(cv, doc):
    cv.setFillColor(WHITE)
    cv.rect(0, 0, W, H, stroke=0, fill=1)

    # ---- fascia fotografica full-bleed, ritagliata tenendo il soggetto a sinistra
    bh = 252.0
    top = H - 104
    iw = bh * 1812 / 500
    cv.saveState()
    p = cv.beginPath()
    p.rect(0, top - bh, W, bh)
    cv.clipPath(p, stroke=0, fill=0)
    cv.drawImage(IMG + 'p01_0.jpeg', -(iw - W) * 0.22, top - bh, iw, bh, mask=None)
    cv.restoreState()

    # ---- occhiello
    cv.setFillColor(MUT)
    cv.setFont('Pop-M', 8)
    cv.drawString(LM, H - 62, 'I N N S B R U C K   ·   T I R O L O   ·   A U S T R I A')
    cv.setStrokeColor(HAIR)
    cv.setLineWidth(0.7)
    cv.line(LM, H - 78, W - RM, H - 78)

    # ---- titolo
    y = top - bh - 78
    cv.setFillColor(INK)
    cv.setFont('Pop-B', 48)
    cv.drawString(LM, y, 'SILLSCHLUCHT')
    cv.setFont('Pop-L', 19)
    cv.setFillColor(INK2)
    cv.drawString(LM + 2, y - 31, 'Guida agli ancoraggi delle highline')
    cv.setFont('Lora', 10.4)
    cv.setFillColor(MUT)
    cv.drawString(LM + 2, y - 62,
                  'Homespot della scena highline di Innsbruck: sette linee da 70 a 102 metri,')
    cv.drawString(LM + 2, y - 77,
                  'materiale, coordinate e regole dello spot. Edizione italiana.')

    # ---- zoccolo scuro full-bleed
    ph = 258.0
    cv.setFillColor(BRAND)
    cv.rect(0, 0, W, ph, stroke=0, fill=1)
    seg = W / 7.0
    data = [(1, '76 m', 'classica'), (2, '70 m', 'classica/freestyle'),
            (3, '70 m', 'freestyle'), (4, '70 m', 'freestyle'),
            (5, '90 m', 'offlevel'), (6, '102 m', 'la più lunga'),
            (7, '100 m', 'mai montata')]
    for i, (n, l, note) in enumerate(data):
        x = i * seg
        cv.setFillColor(LC[n])
        cv.rect(x, ph - 7, seg, 7, stroke=0, fill=1)
        cv.setFillColor(WHITE)
        cv.setFont('Pop-B', 14)
        cv.drawString(x + 12, ph - 36, '0%d' % n)
        cv.setFont('Pop-M', 8.6)
        cv.drawString(x + 12, ph - 51, l)
        cv.setFillColor(HexColor(0x8FA6B0))
        cv.setFont('Pop', 6.2)
        t = note
        while stringWidth(t, 'Pop', 6.2) > seg - 16 and len(t) > 4:
            t = t[:-2]
        cv.drawString(x + 12, ph - 63, t)

    cv.setStrokeColor(HexColor(0x2E4C59))
    cv.setLineWidth(0.8)
    cv.line(LM, ph - 88, W - RM, ph - 88)

    # ---- avviso
    cv.setFillColor(WARN)
    cv.rect(LM, ph - 152, 4, 42, stroke=0, fill=1)
    cv.setFillColor(WHITE)
    cv.setFont('Pop-B', 11)
    cv.drawString(LM + 16, ph - 122, 'REGISTRAZIONE OBBLIGATORIA')
    cv.setFillColor(HexColor(0xC7D4DA))
    cv.setFont('Pop-L', 9)
    cv.drawString(LM + 16, ph - 138,
                  'Ogni highline va annunciata almeno un giorno prima, per la sicurezza del traffico aereo.')
    cv.drawString(LM + 16, ph - 151,
                  'Nessuna linea va lasciata incustodita durante la notte.')

    cv.setStrokeColor(HexColor(0x2E4C59))
    cv.line(LM, 62, W - RM, 62)
    cv.setFillColor(HexColor(0x8FA6B0))
    cv.setFont('Pop', 8)
    cv.drawString(LM, 42, 'Edizione 10 agosto 2026')
    cv.drawRightString(W - RM, 42, '7 linee · 8 ancoraggi georeferenziati')


# ---------------------------------------------------------------- testatine
def page_begin(cv, doc):
    cv._accent = BRAND
    cv._sect = ''


def page_end(cv, doc):
    n = cv.getPageNumber()
    acc = getattr(cv, '_accent', BRAND)
    sect = getattr(cv, '_sect', '')
    cv.setFont('Pop-M', 7)
    cv.setFillColor(MUT)
    cv.drawString(LM, H - 44, 'SILLSCHLUCHT · GUIDA HIGHLINE')
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


# ================================================================ P1 copertina
S.append(Spacer(1, 1))
S.append(NextPageTemplate('main'))
S.append(PageBreak())

# ================================================================ P2 indice
sec(BRAND, 'Indice')
S.append(LineHeader('', 'Indice', 'Guida alla lettura', BRAND))
S.append(SP(10))

toc = [('Il posto, regole e sicurezza', '3', None),
       ('Planimetria delle linee', '4', None),
       ('Panoramica delle sette linee', '5', None),
       ('Glossario e kit di base', '6', None),
       ('Linea 1 · 76 m', '7', 1),
       ('Linea 2 classica · 70 m', '8', 2),
       ('Linee freestyle · 3 × 70 m', '9', None),
       ('     Linea 2 · variante freestyle', '10', 2),
       ('     Linea 3', '11', 3),
       ('     Linea 4', '12', 4),
       ('Linea 5 · 90 m  (offlevel)', '13', 5),
       ('Linea 6 · 102 m  (la più lunga)', '14', 6),
       ('Linea 7 · 100 m  (mai montata)', '15', 7),
       ('Coordinate, link utili e colophon', '16', None)]

rows = []
for label, pg, ln in toc:
    sub = label.startswith(' ')
    st = ParagraphStyle('t%s' % label, fontName='Pop' if sub else 'Pop-M',
                        fontSize=9.2 if sub else 10, leading=15,
                        textColor=INK2 if sub else INK,
                        leftIndent=16 if sub else 0)
    sw = swatch(LC[ln], 7) if ln else ''
    rows.append([sw, Paragraph(label.strip(), st),
                 Paragraph('<font name="Pop-M" size="9.5" color="#7B8288">%s</font>' % pg,
                           ParagraphStyle('p', alignment=TA_RIGHT, leading=15))])
t = Table(rows, colWidths=[16, FW - 56, 40])
t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                       ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                       ('TOPPADDING', (0, 0), (-1, -1), 6),
                       ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                       ('LINEBELOW', (0, 0), (-1, -2), 0.4, HAIR),
                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
S.append(t)
S.append(SP(22))
S.append(P(track('COME USARE QUESTA GUIDA'), eyebrow))
S.append(SP(6))
S.append(P('Ogni linea ha un colore, ripreso dalla planimetria originale a pagina 4: lo ritrovi '
           'nel numero di testata, nelle intestazioni dei blocchi materiale e nel filetto a piè '
           'di pagina. Sotto il titolo di ogni linea, una riga di pastiglie riassume lunghezza, '
           'tipo di ancoraggio e tagline necessaria. Il materiale è sempre diviso in due colonne: '
           '<b>lato tension</b> a sinistra, <b>lato statico</b> a destra, con le coordinate '
           'cliccabili sotto l\'intestazione.'))
S.append(SP(12))
S.append(callout('Cosa è stato aggiunto in questa edizione',
                 'Il contenuto tecnico è quello della guida originale, tradotto integralmente. '
                 'Sono nuovi: la tabella panoramica (p. 5), il glossario e il kit di base (p. 6), '
                 'la checklist e la sequenza di montaggio (p. 3), il riepilogo '
                 'coordinate (p. 16) e il codice colore delle linee. Nessun dato tecnico è stato inventato o modificato.',
                 BRAND, icon='+'))
S.append(PageBreak())

# ================================================================ P3 il posto
sec(BRAND, 'Il posto')
S.append(LineHeader('', 'Il posto', 'Introduzione · regole · checklist', BRAND))
S.append(SP(12))
S.append(P('Homespot della scena highline di Innsbruck. Qui ci si può allenare, provare, '
           'rilassare e grigliare. Anche la Sill invita tutto l\'anno a un bagno rinfrescante.',
           lead))
S.append(SP(12))
S.append(P('Di norma un collegamento resta teso tra le due sponde come <i>fishingline</i>: per '
           'recuperarla sono adatti i mulinelli da pesca a mosca. È poi necessaria una tagline '
           'per tirare la highline sull\'altra sponda. Tutti gli ancoraggi sono su alberi e '
           'possono essere realizzati con brache per carichi pesanti.'))
S.append(SP(16))
S.append(callout('Registrazione obbligatoria, almeno un giorno prima',
                 'Le highline <b>devono</b> essere annunciate tramite il '
                 '<link href="%s"><u>modulo online</u></link>. Non è una formalità: serve alla '
                 'sicurezza del traffico aereo.' % REG, WARN, icon='!', strong=True))
S.append(SP(9))
S.append(two_cols(
    callout('Mai incustodite di notte',
            'Le highline non possono essere lasciate montate senza sorveglianza durante la notte.',
            HexColor(0xB07A18), icon='!', w=COL),
    callout('Niente permarig',
            'Nella Sillschlucht non vanno lasciati montaggi permanenti incustoditi.',
            HexColor(0xB07A18), icon='!', w=COL)))
S.append(SP(9))
S.append(callout('Alternative legali e prestito materiale',
                 'In alternativa allo spot della Sillschlucht, l\'associazione Tiroliners '
                 '(<link href="%s"><u>modulo di iscrizione</u></link>) mette a disposizione '
                 'alcuni spot per highline legali in Tirolo, utilizzabili dai soci nel rispetto '
                 'delle rispettive prescrizioni. I soci possono anche prendere in prestito '
                 'gratuitamente parecchio materiale da highline e slackline: le informazioni, '
                 'insieme a una maglietta gratuita, si ricevono al momento dell\'iscrizione.'
                 % TIR, BRAND, icon='\u2022'))
S.append(SP(20))
S.append(P(track('CHECKLIST PRE-USCITA'), eyebrow))
S.append(SP(8))
S.append(Checklist([
    'Highline registrata (almeno 1 giorno prima)',
    'Tagline ≥ 100 m — ≥ 110 m per la Linea 6',
    'Mulinello da pesca a mosca per la fishingline',
    'Microtrax o equivalente per il tiro',
    'Protezioni albero per ogni ancoraggio',
    'Weblock + softrelease sul lato tension',
    'Brache e grilli secondo la scheda della linea',
    'Piano di smontaggio prima di sera',
], BRAND))
S.append(SP(22))
S.append(P(track('SEQUENZA TIPICA DI MONTAGGIO'), eyebrow))
S.append(SP(10))
S.append(Steps([
    ('Annuncia la linea', 'Registrazione online almeno un giorno prima.'),
    ('Monta gli ancoraggi', 'Brache sugli alberi, sempre con protezione.'),
    ('Recupera la fishingline', 'Con un mulinello da pesca a mosca.'),
    ('Collega la tagline', 'Alla fishingline, per passare sull\'altra sponda.'),
    ('Tira la highline', 'Con la tagline e un Microtrax o simile.'),
    ('Tensiona e verifica', 'Weblock con softrelease; controlla ogni nodo.'),
], BRAND))
S.append(SP(10))
S.append(P('Sequenza ricavata dalle indicazioni della guida originale: adattala sempre alla '
           'linea e alle condizioni del giorno.', small))
S.append(PageBreak())

# ================================================================ P4 mappa
sec(BRAND, 'Planimetria')
S.append(LineHeader('', 'Planimetria delle linee', 'Figura 1 · originale', BRAND))
S.append(SP(10))
S.append(PhotoStrip(IMG + 'p02_0.png', FW, 849, 741,
                    'Le sette linee viste dall\'alto. I numeri e i colori sono quelli usati in tutta la guida.'))
S.append(SP(16))
S.append(ColorKey([(1, '76 m', 'classica'), (2, '70 m', 'classica/freestyle'),
                   (3, '70 m', 'freestyle'), (4, '70 m', 'freestyle'),
                   (5, '90 m', 'offlevel'), (6, '102 m', 'la più lunga'),
                   (7, '100 m', 'mai montata')]))
S.append(SP(14))
S.append(callout('Tutti gli ancoraggi sono su alberi',
                 'Sul lato tension si mette in tensione la linea (weblock + softrelease); il lato '
                 'statico la trattiene fisso. Su entrambi la protezione dell\'albero non è '
                 'opzionale.', BRAND, icon='\u2022'))
S.append(PageBreak())

# ================================================================ P5 panoramica
sec(BRAND, 'Panoramica')
S.append(LineHeader('', 'Le sette linee', 'Panoramica comparativa', BRAND))
S.append(SP(12))


def chip(n):
    t = Table([[swatch(LC[n], 7), Paragraph(str(n), tdb)]], colWidths=[11, 16])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    return t


rows = [
    [chip(1), '76 m', 'Classica', 'Fettucce 1,5 m su albero', 'Standard, 2 fettucce da 2 m', '7'],
    [chip(2), '70 m', 'Classica', 'Rinvio da albero arretrato (6 m)', 'Standard, 2 fettucce da 2 m', '8'],
    [chip(2), '70 m', 'Freestyle', 'A-frame + brache da 4 m', 'Standard, brache da 2 m', '10'],
    [chip(3), '70 m', 'Freestyle', 'Rinvio sul pino a bordo parete', 'Compensato ed equalizzato', '11'],
    [chip(4), '70 m', 'Freestyle', 'A-frame + brache da 2 t', 'Compensato ed equalizzato', '12'],
    [chip(5), '90 m', 'Offlevel', 'Come Linea 2 classica', 'Standard, 2 fettucce da 2 m', '13'],
    [chip(6), '102 m', 'Classica', 'Fettucce 1,5 m su albero', 'Standard, 2 fettucce da 2 m', '14'],
    [chip(7), '100 m', '—', 'Mai montata finora', '—', '15'],
]
S.append(data_table(['Linea', 'Metri', 'Tipo', 'Lato tension', 'Lato statico', 'Pag'],
                    rows, [54, 46, 56, 150, 150, 35]))
S.append(SP(6))
S.append(P('Le due righe «2» sono la <b>stessa linea del Lageplan</b>, montata in due modi alternativi: classica (p. 8) oppure freestyle (p. 10). Non sono due linee diverse.', small))
S.append(SP(12))
S.append(P(track('LE TRE FAMIGLIE DI MONTAGGIO'), eyebrow))
S.append(SP(8))
cw3 = (FW - 24) / 3
cards = Table([[
    KitCard('Classica', ['Ancoraggio diretto su albero',
                         'Fettucce corte, masterpoint vicino',
                         'Montaggio rapido, giornaliero'], BRAND, cw3),
    KitCard('Freestyle', ['Tre linee parallele da ~70 m',
                          'A-frame o rinvio su pino',
                          'Per permanenze più lunghe'], LC[3], cw3),
    KitCard('Compensata', ['Su alberelli e cespugli',
                           'Carico ripartito ed equalizzato',
                           'Controventata di lato e in basso'], LC[4], cw3)]],
    colWidths=[cw3 + 12, cw3 + 12, cw3])
cards.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (1, 0), 12),
                           ('RIGHTPADDING', (2, 0), (2, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
S.append(cards)
S.append(SP(12))
S.append(callout('Tagline: la variabile che cambia più spesso',
                 'Per quasi tutte le linee serve una tagline di circa 100 m più il materiale per '
                 'il tiro (ad es. Microtrax). Per la Linea 6, la più lunga, la guida raccomanda '
                 'oltre 110 m.', BRAND, icon='\u2022'))
S.append(SP(14))
S.append(P(track('CONFRONTO DELLE LUNGHEZZE'), eyebrow))
S.append(SP(8))
S.append(Bars([('Linea 1', 76, LC[1]), ('Linea 2', 70, LC[2]), ('Linea 3', 70, LC[3]),
               ('Linea 4', 70, LC[4]), ('Linea 5', 90, LC[5]), ('Linea 6', 102, LC[6]),
               ('Linea 7', 100, LC[7])]))
S.append(PageBreak())

# ================================================================ P6 glossario
sec(BRAND, 'Glossario')
S.append(LineHeader('', 'Glossario e kit di base', 'Termini tecnici · materiale ricorrente', BRAND))
S.append(SP(12))

gl_a = [
    ('Fishingline', 'Cordino sottile già teso tra le sponde, serve a recuperare la tagline.'),
    ('Tagline', 'Cordino di servizio con cui si tira la highline dall\'altra parte.'),
    ('Weblock', 'Bloccante per fettuccia, sul lato in tensione.'),
    ('Softrelease', 'Sistema in cordino per scaricare la tensione in modo controllato.'),
    ('Leash', 'Cordino che collega l\'imbrago alla linea.'),
    ('Masterpoint', 'Punto di raccolta dell\'ancoraggio a cui si collega la linea.'),
    ('A-frame', 'Cavalletto che solleva la linea sopra il bordo.'),
    ('Rinvio', 'Deviazione della direzione di tiro con un grillo o un albero intermedio.'),
    ('Offlevel', 'Linea con i due ancoraggi a quote diverse.'),
    ('Permarig', 'Montaggio lasciato in posto a lungo.'),
]
gl_b = [
    ('Braca ad anello', 'Fettuccia tubolare chiusa ad anello (ted. <i>Rundschlinge</i>).'),
    ('Fettuccia Dyneema', 'Fettuccia cucita ad alta resistenza, qui sugli A-frame.'),
    ('Grillo', 'Maglia metallica a perno (ted. <i>Schäkel</i>).'),
    ('Softshackle', 'Grillo in fibra tessile.'),
    ('Maglia rapida', 'Anello metallico a chiusura filettata (quicklink).'),
    ('Treepro', 'Protezione fra corteccia e fettuccia: su ogni ancoraggio.'),
    ('Microtrax / Tibloc', 'Bloccanti progressivi per il tiro e le controventature.'),
    ('Grigri', 'Autobloccante, qui per tensionare gli spezzoni di statica.'),
    ('Anc. compensato', 'Carico ripartito su più alberelli, controventato.'),
    ('Backup', 'Ridondanza dell\'ancoraggio: corda o fettucce in più.'),
]


def gloss(data, w):
    rows = []
    for term, d in data:
        rows.append([Paragraph(term, ParagraphStyle('g', fontName='Pop-M', fontSize=8,
                                                    leading=11, textColor=INK)),
                     Paragraph(d, ParagraphStyle('gd', fontName='Lora', fontSize=8,
                                                 leading=11, textColor=INK2))])
    t = Table(rows, colWidths=[w * 0.36, w * 0.64])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (0, 0), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (0, -1), 8),
                           ('RIGHTPADDING', (1, 0), (1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 5),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                           ('LINEBELOW', (0, 0), (-1, -2), 0.4, HAIR),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


S.append(two_cols(gloss(gl_a, COL), gloss(gl_b, COL)))
S.append(SP(18))
S.append(P(track('KIT DI BASE PER UN ANCORAGGIO'), eyebrow))
S.append(SP(4))
S.append(P('Weblock, softrelease e il resto del materiale che fa comunque parte di ogni '
           'ancoraggio non vengono ripetuti nelle schede delle linee freestyle.', small))
S.append(SP(10))
cw2 = (FW - 14) / 2
kits = Table([[
    KitCard('Lato tension', ['2 brache (1,5–6 m secondo la linea)',
                             '1–2 protezioni per l\'albero',
                             'Weblock con softrelease oppure Orange',
                             '2–4 grilli, eventualmente uno di rinvio'], BRAND, cw2),
    KitCard('Lato statico', ['2 brache da 2 m',
                             '1 protezione per l\'albero',
                             '2 grilli',
                             'Tagline ~100 m + Microtrax'], BRAND, cw2)]],
    colWidths=[cw2 + 14, cw2])
kits.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                          ('RIGHTPADDING', (0, 0), (0, 0), 14),
                          ('RIGHTPADDING', (1, 0), (1, 0), 0),
                          ('TOPPADDING', (0, 0), (-1, -1), 0),
                          ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                          ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
S.append(kits)
S.append(SP(14))
S.append(callout('Nota terminologica',
                 '«Orange» è il nome di un dispositivo citato così anche nell\'originale ed è '
                 'stato mantenuto invariato, come tutti i nomi commerciali (Weblock, Microtrax, '
                 'Tibloc, Grigri, Treepro).', MUT, icon='\u2022'))
S.append(PageBreak())

# ================================================================ P7 Linea 1
c1 = LC[1]
sec(c1, 'Linea 1 · 76 m')
S.append(LineHeader('01', 'Linea 1 · 76 m', 'Classica · due ancoraggi georeferenziati', c1))
S.append(SP(12))
S.append(P('Linea n. 1 nella planimetria di pagina 4. Con un setup da 90 m la leash si riesce '
           'ancora a infilare senza problemi all\'estremità.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '76 m'), ('Setup consigliato', '90 m'),
                  ('Tagline', 'ca. 100 m'), ('Ancoraggi', 'Albero / albero')], c1))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension', [
        '2 pz. brache di almeno 1,5 m — con questa lunghezza il masterpoint resta vicino '
        'all\'albero (foto a). In alternativa una braca da 3 m doppiata.',
        '1 pz. protezione per l\'albero',
        'Weblock con softrelease oppure Orange',
        '2 pz. grilli'], c1, CO['l1t'], C['l1t']),
    gear_block('Lato statico', [
        '2 pz. brache: qui sono ideali quelle da 2 m',
        '1 pz. protezione per l\'albero',
        '2 pz. grilli',
        'Tagline di circa 100 m e materiale aggiuntivo per il tiro, ad es. Microtrax'],
        c1, CO['l1s'], C['l1s'])))
S.append(SP(16))
S.append(photo_pair(IMG + 'p03_0.jpeg', IMG + 'p03_1.jpeg',
                    'a · Ancoraggio di tensione', 'b · Ancoraggio statico', color=c1, ratio=1.12, focus=0.52))
S.append(PageBreak())

# ================================================================ P8 Linea 2 classica
c2 = LC[2]
sec(c2, 'Linea 2 classica · 70 m')
S.append(LineHeader('02', 'Linea 2 classica · 70 m', 'Variante A della Linea 2 · rinvio da albero arretrato', c2))
S.append(SP(12))
S.append(P('Un modo per montare la Linea n. 2 del Lageplan. Se si vogliono montare più linee '
           'freestyle parallele, la <b>stessa linea</b> si monta con gli ancoraggi descritti a '
           'pagina 10.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '70 m'), ('Tension', 'Rinvio'),
                  ('Tagline', 'ca. 100 m'), ('Altra variante', 'p. 10 · freestyle')], c2))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension', [
        '1 pz. fettuccia da 6 m complessivi — con questa si tira in avanti partendo '
        'dall\'albero che si trova un po\' più indietro',
        '1 pz. fettuccia da 1 m per il rinvio della fettuccia principale',
        '2 pz. protezione per l\'albero',
        'Weblock con softrelease oppure Orange',
        '3 pz. grilli, uno come rinvio'], c2,
        note='Coordinate non indicate nell\'originale.'),
    gear_block('Lato statico', [
        '2 pz. brache: qui sono ideali quelle da 2 m',
        '1 pz. protezione per l\'albero',
        '2 pz. grilli',
        'Tagline di circa 100 m e materiale aggiuntivo per il tiro, ad es. Microtrax'],
        c2, CO['l2s'], C['l2s'])))
S.append(SP(16))
S.append(photo_pair(IMG + 'p04_0.jpeg', IMG + 'p04_1.jpeg',
                    'a · Ancoraggio di tensione', 'b · Ancoraggio statico', color=c2, ratio=1.12, focus=0.52))
S.append(PageBreak())

# ================================================================ P9 Freestyle intro
cf = LC[3]
sec(cf, 'Linee freestyle')
S.append(LineHeader('', 'Linee freestyle', '3 linee parallele · circa 70 m ciascuna', cf))
S.append(SP(12))
S.append(P('All\'inizio del 2024 è stato possibile realizzare tre linee freestyle parallele, '
           'ciascuna di circa 70 m. Il montaggio è più complesso e conviene quando devono '
           'restare tese per un periodo prolungato.', lead))
S.append(SP(14))
S.append(PhotoStrip(IMG + 'p05_0.png', FW, 897, 436,
                    'Figura 4 · Tutte e tre le linee freestyle montate.', cf))
S.append(SP(16))
cw3 = (FW - 24) / 3
cards = Table([[
    KitCard('Linea 2 · sinistra', ['A-frame con brache da 4 m',
                                   'Statico standard su albero',
                                   'Scheda a pagina 10'], LC[2], cw3),
    KitCard('Linea 3 · centrale', ['Rinvio sul pino a bordo parete',
                                   'Statico compensato',
                                   'Scheda a pagina 11'], LC[3], cw3),
    KitCard('Linea 4 · destra', ['A-frame con brache da 2 t',
                                 'Statico compensato',
                                 'Scheda a pagina 12'], LC[4], cw3)]],
    colWidths=[cw3 + 12, cw3 + 12, cw3])
cards.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (1, 0), 12),
                           ('RIGHTPADDING', (2, 0), (2, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
S.append(cards)
S.append(SP(16))
S.append(callout('Niente permarig incustoditi nella Sillschlucht',
                 'Le tre linee restano tese più a lungo, ma non vanno mai lasciate senza '
                 'sorveglianza. Weblock, softrelease e il materiale comune a ogni ancoraggio non '
                 'sono ripetuti nelle schede che seguono.', WARN, icon='!'))
S.append(PageBreak())

# ================================================================ P10 Linea 2 freestyle
sec(c2, 'Linea 2 freestyle · 70 m')
S.append(LineHeader('02', 'Linea 2 freestyle · 70 m', 'Variante B della Linea 2 · A-frame', c2))
S.append(SP(12))
S.append(P('È la <b>stessa Linea 2</b> di pagina 8, montata in modo diverso: qui è la linea di sinistra del gruppo freestyle, pensata per restare tesa più a lungo insieme alle Linee 3 e 4. L\'ancoraggio di tensione è quello della figura 5, con A-frame; il lato statico quello della figura 6.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '~70 m'), ('Tension', 'A-frame'),
                  ('Statico', 'Standard'), ('Altra variante', 'p. 8 · classica')], c2))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension · figura 5', [
        '2 pz. brache ad anello da 4 m',
        'Fettuccia in Dyneema da 90 cm per l\'A-frame',
        '2 pz. grilli',
        'Softshackle',
        'Treepro'], c2),
    gear_block('Lato statico · figura 6', [
        '2 pz. brache ad anello da 2 m',
        '2 pz. grilli',
        'Treepro'], c2)))
S.append(SP(16))
S.append(photo_row([(IMG + 'p06_0.png', 666, 465, 'Figura 5 · Primo ancoraggio con A-frame'),
                    (IMG + 'p06_1.png', 995, 484, 'Figura 6 · Ancoraggio statico')], c2))
S.append(SP(16))
S.append(callout('A che cosa serve l\'A-frame',
                 'Il cavalletto solleva la linea sopra il bordo e gli ostacoli. Nelle freestyle è '
                 'vincolato con una fettuccia in Dyneema — 90 cm qui, 120 cm sulla Linea 4 — '
                 'mentre le brache lunghe portano il carico dagli alberi fino al cavalletto.',
                 c2, icon='\u2022'))
S.append(SP(18))
S.append(P(track('NOTE DI MONTAGGIO'), eyebrow))
S.append(SP(8))
S.append(Lines(4))
S.append(PageBreak())

# ================================================================ P11 Linea 3
c3 = LC[3]
sec(c3, 'Linea 3 · 70 m')
S.append(LineHeader('03', 'Linea 3 · 70 m', 'Freestyle · rinvio sul pino a bordo parete', c3))
S.append(SP(12))
S.append(P('La linea centrale viene rinviata sul pino che si trova sul bordo della parete. Il '
           'lato statico è più laborioso: un ancoraggio compensato su alberelli e cespugli, '
           'controventato anche lateralmente e verso il basso. Con un po\' di pratica si sbriga '
           'comunque in fretta.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '~70 m'), ('Tension', 'Rinvio su pino'),
                  ('Statico', 'Compensato'), ('Posizione', 'Centrale')], c3))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension · figura 7', [
        'Braca ad anello da 6 m (2× 3 m)',
        'Braca ad anello da 1 m',
        '3 grilli',
        'Corda o fettucce supplementari per il backup'], c3,
        note='Ancoraggio come per la Linea 2 classica.'),
    gear_block('Lato statico · figura 8', [
        '2 pz. brache ad anello da 3 m',
        '1 pz. braca ad anello da 2 m',
        '3 pz. brache ad anello da 1,5 m',
        '2 pz. brache ad anello da 1 m',
        '3 maglie rapide',
        '1 softshackle',
        '4 grilli oppure 3 grilli e un anello d\'acciaio',
        '2 pz. corda statica da 20 m',
        '2 pz. moschettoni d\'acciaio',
        '1 Microtrax',
        '6 m di corda statica',
        '5 pz. Treepro piccoli'], c3, CO['l3s'], C['l3s'])))
S.append(SP(16))
S.append(photo_row([(IMG + 'p07_0.png', 839, 649, 'Figura 7 · Ancoraggio di tensione'),
                    (IMG + 'p08_0.png', 1086, 360, 'Figura 8 · Ancoraggio compensato')], c3))
S.append(SP(16))
S.append(callout('Che cos\'è un ancoraggio compensato',
                 'Il carico viene ripartito su più alberelli e cespugli e l\'insieme è '
                 'controventato anche lateralmente e verso il basso. Servono molte brache corte, '
                 'spezzoni di corda statica e bloccanti: è il montaggio più lungo di tutta la '
                 'guida, ma con un po\' di pratica si sbriga in fretta.', c3, icon='\u2022'))
S.append(PageBreak())

# ================================================================ P12 Linea 4
c4 = LC[4]
sec(c4, 'Linea 4 · 70 m')
S.append(LineHeader('04', 'Linea 4 · 70 m', 'Freestyle · A-frame con brache da 2 t', c4))
S.append(SP(12))
S.append(P('La linea di destra viene montata di nuovo con un A-frame. Una lunga fettuccia viene '
           'portata in avanti a partire da due alberi più sottili situati più indietro; per '
           'mantenere il più bassa possibile la dinamica nell\'ancoraggio si consigliano le '
           'brache da 2 t. Il lato statico è simile a quello della linea centrale.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '~70 m'), ('Tension', 'A-frame'),
                  ('Statico', 'Compensato'), ('Posizione', 'Destra')], c4))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension · figura 9', [
        'Brache ad anello da 2 t',
        '4 pz. grilli',
        'A-frame',
        'Fettuccia in Dyneema da 120 cm per l\'A-frame'], c4,
        note='Per questo ancoraggio servono parecchi metri di fettucce.'),
    gear_block('Lato statico · figura 10', [
        '1 pz. braca ad anello da 3 m',
        '1 pz. braca ad anello da 2 m',
        '3 pz. brache ad anello da 1,5 m',
        '2 pz. brache ad anello da 1 m',
        '3 maglie rapide',
        '1 softshackle',
        '4 grilli oppure 3 grilli e un anello d\'acciaio',
        '2 pz. corda statica da 20 m',
        '2 pz. moschettoni d\'acciaio',
        '2 Microtrax oppure Grigri',
        '6 m di corda statica',
        '5 pz. Treepro piccoli'], c4, CO['l4s'], C['l4s'])))
S.append(SP(14))
S.append(photo_row([(IMG + 'p09_0.png', 905, 358, 'Figura 9 · Ancoraggio con A-frame'),
                    (IMG + 'p10_0.png', 751, 488, 'Figura 10 · Ancoraggio compensato')], c4))
S.append(SP(12))
S.append(callout('Come si controventa il punto di ancoraggio',
                 'I Microtrax e/o il Grigri si usano in combinazione con gli spezzoni corti di '
                 'corda statica per controventare lateralmente il punto di ancoraggio. Non '
                 'dimenticare Tibloc e carrucola per mettere in tensione.', c4, icon='\u2022'))
S.append(PageBreak())

# ================================================================ P13 Linea 5
c5 = LC[5]
sec(c5, 'Linea 5 · 90 m')
S.append(LineHeader('05', 'Linea 5 · 90 m', 'Offlevel · stesso tension della Linea 2', c5))
S.append(SP(12))
S.append(P('La linea è offlevel: i due ancoraggi si trovano a quote diverse. Utilizza lo stesso '
           'ancoraggio di tensione della Linea 2 classica.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '90 m'), ('Profilo', 'Offlevel'),
                  ('Tension', 'Come Linea 2'), ('Tagline', 'ca. 100 m')], c5))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension', [
        '1 pz. fettuccia da 6 m complessivi — si tira in avanti partendo dall\'albero che si '
        'trova un po\' più indietro',
        '1 pz. fettuccia da 1 m per il rinvio della fettuccia principale',
        '2 pz. protezione per l\'albero — se è montata anche la linea da 70 m si può rinunciare '
        'a quella aggiuntiva',
        'Weblock con softrelease oppure Orange',
        '3 pz. grilli, uno come rinvio'], c5),
    gear_block('Lato statico', [
        '2 pz. brache: qui sono ideali quelle da 2 m',
        '1 pz. protezione per l\'albero',
        '2 pz. grilli',
        'Tagline di circa 100 m e materiale aggiuntivo per il tiro, ad es. Microtrax'],
        c5, CO['l5s'], C['l5s'])))
S.append(SP(16))
S.append(photo_pair(IMG + 'p11_1.jpeg', IMG + 'p11_0.jpeg',
                    'a · Ancoraggio di tensione', 'b · Ancoraggio statico', color=c5, ratio=1.12, focus=0.52))
S.append(PageBreak())

# ================================================================ P14 Linea 6
c6 = LC[6]
sec(c6, 'Linea 6 · 102 m')
S.append(LineHeader('06', 'Linea 6 · 102 m', 'La linea più lunga della Sillschlucht', c6))
S.append(SP(12))
S.append(P('La linea più lunga finora nella Sillschlucht. Entrambi gli ancoraggi sono '
           'georeferenziati; per il tiro si raccomanda una tagline più lunga del solito.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza', '102 m'), ('Tagline', '> 110 m'),
                  ('Ancoraggi', 'Albero / albero'), ('Record', 'La più lunga')], c6))
S.append(SP(14))
S.append(two_cols(
    gear_block('Lato tension', [
        '2 pz. fettuccia da 1,5 m — con questa lunghezza l\'ancoraggio resta vicino all\'albero. '
        'In alternativa una braca da 3 m doppiata.',
        '1 pz. protezione per l\'albero',
        'Weblock con softrelease oppure Orange',
        '2 pz. grilli'], c6, CO['l6t'], C['l6t']),
    gear_block('Lato statico', [
        '2 pz. brache: qui sono adatte quelle da 2 m',
        '1 pz. protezione per l\'albero',
        '2 pz. grilli',
        'Si consiglia una tagline più lunga di 110 m e materiale aggiuntivo per il tiro, ad es. '
        'Microtrax'], c6, CO['l6s'], C['l6s'])))
S.append(SP(16))
S.append(photo_pair(IMG + 'p12_0.jpeg', IMG + 'p12_1.jpeg',
                    'a · Ancoraggio di tensione', 'b · Ancoraggio statico', color=c6, ratio=1.12, focus=0.52))
S.append(PageBreak())

# ================================================================ P15 Linea 7
c7 = LC[7]
sec(c7, 'Linea 7 · 100 m')
S.append(LineHeader('07', 'Linea 7 · 100 m', 'Progetto · mai montata finora', c7))
S.append(SP(12))
S.append(P('Non è ancora mai stata montata. Nella planimetria di pagina 4 il tracciato è '
           'indicato in azzurro, sulla sponda sinistra, parallelo alla Linea 6.', lead))
S.append(SP(14))
S.append(ChipRow([('Lunghezza stimata', '100 m'), ('Stato', 'Mai montata'),
                  ('Ancoraggi', 'Non documentati'), ('Coordinate', 'Non disponibili')], c7))
S.append(SP(16))
S.append(callout('Nessun dato di ancoraggio disponibile',
                 'La guida originale non riporta materiale, coordinate né fotografie per questa '
                 'linea. Chi la monta per primo può contribuire aggiungendo lista materiale, '
                 'coordinate dei due ancoraggi e foto, così da completare la scheda.',
                 c7, icon='\u2022'))
S.append(SP(20))
S.append(P(track('SPAZIO PER GLI APPUNTI'), eyebrow))
S.append(SP(10))


S.append(Lines(14))
S.append(PageBreak())

# ================================================================ P16 apparati
sec(BRAND, 'Coordinate e link')
S.append(LineHeader('', 'Coordinate e link utili', 'Riepilogo · colophon', BRAND))
S.append(SP(12))
coord_rows = [
    (1, 'Tensione', 'l1t'), (1, 'Statico', 'l1s'),
    (2, 'Statico', 'l2s'), (3, 'Statico', 'l3s'), (4, 'Statico', 'l4s'),
    (5, 'Statico', 'l5s'), (6, 'Tensione', 'l6t'), (6, 'Statico', 'l6s'),
]
rows = []
for n, kind, k in coord_rows:
    rows.append([chip(n), kind,
                 Paragraph('<font name="Pop" size="8">%s</font>' % A(C[k], CO[k], LC[n]), td)])
S.append(data_table(['Linea', 'Ancoraggio', 'Coordinate (tocca per aprire la mappa)'],
                    rows, [58, 84, FW - 142]))
S.append(SP(8))
S.append(P('La Linea 2 classica ha coordinate solo per il lato statico; per la Linea 7 non '
           'esistono dati. Le coordinate sono quelle dell\'originale, non verificate sul campo.',
           small))
S.append(SP(20))
S.append(P(track('LINK UTILI'), eyebrow))
S.append(SP(8))
S.append(two_cols(
    callout('Registrazione highline',
            'Modulo obbligatorio, almeno un giorno prima.<br/>'
            '<link href="%s"><u>slacklineverband.com</u></link>' % REG, WARN, icon='!', w=COL),
    callout('Verein Tiroliners',
            'Spot legali in Tirolo, prestito materiale, iscrizione.<br/>'
            '<link href="%s"><u>tiroliners.at</u></link>' % TIR, BRAND, icon='\u2022', w=COL)))
S.append(SP(22))
S.append(Rule())
S.append(SP(10))
S.append(P('<b>Colophon.</b> Edizione italiana dell\'<i>Highlineguide Sillschlucht</i> del '
           '10 agosto 2026. Testi tradotti integralmente dal tedesco; fotografie e planimetria '
           'sono quelle dell\'originale. Impaginazione rifatta: codice colore per linea, schede '
           'a doppia colonna tension/statico, pastiglie dati, glossario, checklist e riepilogo '
           'coordinate. I contenuti tecnici non sono stati alterati; le sezioni aggiunte sono '
           'elencate a pagina 2.', small))
S.append(SP(8))
S.append(P('Highlining e slacklining comportano rischi. Questa guida descrive montaggi già '
           'realizzati da altri: non sostituisce formazione, esperienza diretta e verifica '
           'autonoma di ogni ancoraggio.', small))

# ---------------------------------------------------------------- build
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM,
                      title='Sillschlucht · Guida agli ancoraggi delle highline',
                      author='Highlineguide Sillschlucht — edizione italiana')
frame = Frame(LM, BM, FW, H - TM - BM, id='n',
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id='cover', frames=[Frame(LM, BM, FW, 24, id='c', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=cover),
    PageTemplate(id='main', frames=[frame], onPage=page_begin, onPageEnd=page_end),
])
doc.build(S)
print('ok')
