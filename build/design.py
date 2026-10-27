# -*- coding: utf-8 -*-
"""Sistema grafico per la Guida Highline Sillschlucht (edizione italiana)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (Paragraph, Spacer, Image, Table, TableStyle,
                                Flowable, KeepTogether)

# ---------------------------------------------------------------- font
# L'originale registrava i font da un percorso Linux fisso. Qui la risoluzione
# e' delegata a build/font.py, che li cerca in locale, nel sistema, oppure li
# scarica da Google Fonts. Unica modifica rispetto a design/design.py.
import sys as _sys                                                  # noqa: E402
from pathlib import Path as _Path                                   # noqa: E402

_sys.path.insert(0, str(_Path(__file__).resolve().parent))
from font import registra as _registra_font, risolvi as _risolvi_font   # noqa: E402

FONT_USATI = _registra_font()

# ---------------------------------------------------------------- colori
INK = HexColor(0x14181C)
INK2 = HexColor(0x3C444C)
MUT = HexColor(0x7B8288)
HAIR = HexColor(0xDFDCD6)
PAPER = HexColor(0xF6F5F2)
PAPER2 = HexColor(0xEDEBE6)
WHITE = colors.white
WARN = HexColor(0xB3261E)

# colori delle 7 linee, ripresi dalla planimetria originale
LC = {
    1: HexColor(0xE03A2F),
    2: HexColor(0xE2622E),
    3: HexColor(0xDE8A26),
    4: HexColor(0xA3A736),
    5: HexColor(0x3FB53A),
    6: HexColor(0x1FBE88),
    7: HexColor(0x2F9FDE),
}
BRAND = HexColor(0x18333F)

W, H = A4
LM = RM = 52.0
TM, BM = 70.0, 62.0
FW = W - LM - RM          # 491.3
COL = (FW - 14) / 2       # colonna per blocchi affiancati


def tint(c, f):
    """Schiarisce un colore verso il bianco (f = 0 bianco, 1 colore pieno)."""
    return HexColor(int(((1 - f) + c.red * f) * 255) << 16 |
                    int(((1 - f) + c.green * f) * 255) << 8 |
                    int(((1 - f) + c.blue * f) * 255))


def track(text, sp=1.4):
    """Testo spaziato: spazio fra i caratteri, gap triplo fra le parole."""
    return '&nbsp;&nbsp;'.join(' '.join(w) for w in text.split(' '))


def swatch(color, size=7):
    """Quadratino di colore utilizzabile dentro una tabella."""
    t = Table([['']], colWidths=[size], rowHeights=[size])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 0), color),
                           ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


# ---------------------------------------------------------------- stili
body = ParagraphStyle('body', fontName='Lora', fontSize=9.6, leading=14.2,
                      textColor=INK2, alignment=TA_JUSTIFY)
bodyc = ParagraphStyle('bodyc', parent=body, alignment=TA_CENTER)
lead = ParagraphStyle('lead', parent=body, fontSize=11.4, leading=17.4,
                      textColor=INK, alignment=TA_JUSTIFY)
small = ParagraphStyle('small', parent=body, fontSize=8.6, leading=12.4)
item = ParagraphStyle('item', fontName='Lora', fontSize=9.1, leading=12.8,
                      textColor=INK2, leftIndent=11, bulletIndent=0,
                      spaceBefore=2.6, bulletFontName='Pop',
                      bulletFontSize=8.5, bulletColor=MUT)
eyebrow = ParagraphStyle('eyebrow', fontName='Pop-M', fontSize=7.4, leading=10,
                         textColor=MUT)
h1 = ParagraphStyle('h1', fontName='Pop-B', fontSize=21, leading=25,
                    textColor=INK, spaceAfter=4)
h2 = ParagraphStyle('h2', fontName='Pop-M', fontSize=12.5, leading=16,
                    textColor=INK, spaceBefore=6, spaceAfter=5)
h3 = ParagraphStyle('h3', fontName='Pop-M', fontSize=9.4, leading=13,
                    textColor=INK)
capt = ParagraphStyle('capt', fontName='Pop', fontSize=7.8, leading=10.6,
                      textColor=MUT)
th = ParagraphStyle('th', fontName='Pop-M', fontSize=7.4, leading=10,
                    textColor=WHITE)
td = ParagraphStyle('td', fontName='Lora', fontSize=8.4, leading=11.6,
                    textColor=INK2)
tdb = ParagraphStyle('tdb', fontName='Pop-M', fontSize=8.6, leading=11.6,
                     textColor=INK)


def A(url, text, c=None):
    col = (c or BRAND).hexval()[2:]
    return '<link href="%s"><font color="#%s">%s</font></link>' % (url, col, text)


# anche con lo spazio non separabile, che tiene il segno su una riga sola
_re_dc = re.compile('<font color="#B3261E">(\\[DA(?: |\u00a0|&nbsp;)CONF[^<]*\\])</font>')
_UNITA = re.compile(r'(\d) (m|mm|cm|kN|kg|t|L)\b')


def unito(t):
    """Numero e unita' di misura non si separano a fine riga: \u00ab53 m\u00bb, non \u00ab53 / m\u00bb."""
    return _UNITA.sub(r'\1&nbsp;\2', t)


def P(t, s=body):
    return Paragraph(unito(t), s)


def BU(t, c=MUT):
    st = ParagraphStyle('i%s' % id(t), parent=item, bulletColor=c)
    return Paragraph(unito(t), st, bulletText='\u2014')


def SP(h):
    return Spacer(1, h)


# ---------------------------------------------------------------- flowable
class Rule(Flowable):
    """Filetto orizzontale."""

    def __init__(self, w=FW, thick=0.6, color=HAIR, space=0):
        self.w, self.t, self.c, self.s = w, thick, color, space

    def wrap(self, aw, ah):
        return (self.w, self.t + self.s)

    def draw(self):
        self.canv.setStrokeColor(self.c)
        self.canv.setLineWidth(self.t)
        self.canv.line(0, self.s / 2, self.w, self.s / 2)


# ---------------------------------------------------------------- rimandi
# Mappa chiave -> numero di pagina, riempita durante l'impaginazione. Serve a
# stampare «p. 27» nell'indice e nel catalogo: in un documento di cinquanta
# pagine un elenco senza numeri non e' un indice, e' una lista.
PAGINE = {}


class Segna(Flowable):
    """Marcatore invisibile: registra su quale pagina cade questo punto."""

    def __init__(self, chiave):
        self.chiave = chiave

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        PAGINE[self.chiave] = self.canv.getPageNumber()


def rif(chiave, vuoto='—'):
    """Rimando di pagina, se la passata precedente lo ha gia' registrato."""
    n = PAGINE.get(chiave)
    return 'p. %d' % n if n else vuoto


class Accent(Flowable):
    """Marcatore invisibile: fissa il colore d'accento della pagina."""

    def __init__(self, color, label=''):
        self.color, self.label = color, label

    def wrap(self, aw, ah):
        return (0, 0)

    def drawOn(self, canvas, x, y, _sW=0):
        # Una sezione che si apre in cima alla cornice e' quella della pagina.
        # Una che si apre piu' in basso no: la pagina appartiene ancora alla
        # sezione in corso, e la testatina deve dire quella. Prima vinceva
        # l'ultimo marcatore disegnato, e la testatina annunciava il capitolo
        # che cominciava in fondo pagina.
        if y >= getattr(canvas, '_cima_cornice', float('inf')) - 1.0:
            canvas._sect_pagina = self.label
            canvas._accent_pagina = self.color
        Flowable.drawOn(self, canvas, x, y, _sW)

    def draw(self):
        self.canv._accent = self.color
        self.canv._sect = self.label


def lega_testate(storia):
    """Lega ogni testata a cio' che la segue, cosi' non resta sola in fondo pagina.

    Vale per le testate di capitolo e per i titoletti h3. Gli spaziatori subito
    dopo vengono legati anche loro: una testata legata a uno spazio vuoto
    resterebbe comunque orfana.
    """
    for i, f in enumerate(storia):
        testata = isinstance(f, LineHeader) or (
            isinstance(f, Paragraph) and getattr(f.style, 'name', '') == 'h3')
        if not testata:
            continue
        f.keepWithNext = 1
        j = i + 1
        while j < len(storia) and isinstance(storia[j], Spacer):
            storia[j].keepWithNext = 1
            j += 1
    return storia


class LineHeader(Flowable):
    """Testata di sezione: numero in pastiglia colorata + titolo + occhiello."""

    def __init__(self, num, title, eyebrow_txt, color, w=FW):
        self.num, self.title = num, title
        self.eb, self.c, self.w = eyebrow_txt, color, w
        self.h = 56

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        s = 40
        y = self.h - s - 4
        if str(self.num).strip():
            c.setFillColor(self.c)
            c.roundRect(0, y, s, s, 5, stroke=0, fill=1)
            c.setFillColor(WHITE)
            c.setFont('Pop-B', 17)
            tw = stringWidth(str(self.num), 'Pop-B', 17)
            c.drawString((s - tw) / 2, y + s / 2 - 6, str(self.num))
            x = s + 14
        else:
            c.setFillColor(self.c)
            c.rect(0, y + 2, 4, s - 2, stroke=0, fill=1)
            x = 18
        c.setFillColor(MUT)
        c.setFont('Pop-M', 7.4)
        c.drawString(x, self.h - 9, self.eb.upper())
        c.setFillColor(INK)
        c.setFont('Pop-B', 19)
        c.drawString(x, self.h - 32, self.title)
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.6)
        c.line(0, 2, self.w, 2)


class TestataLinea(Flowable):
    """Testata di una scheda linea: sigla del settore, nome, lunghezza in grande.

    Ricalca la scheda linea della guida Sillschlucht di Innsbruck, che e' il
    modello di riferimento del progetto: chi apre la scheda vede subito quale
    linea e' e quanto e' lunga.
    """

    def __init__(self, sigla, titolo, sotto, lunghezza, colore, w=FW):
        self.sigla, self.titolo, self.sotto = sigla, titolo, sotto
        self.lung, self.c, self.w = lunghezza, colore, w
        self.h = 64

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        c.setFillColor(PAPER)
        c.roundRect(0, 0, self.w, self.h, 4, stroke=0, fill=1)
        c.setFillColor(self.c)
        c.rect(0, self.h - 3, self.w, 3, stroke=0, fill=1)
        s = 38
        y = (self.h - 3 - s) / 2
        c.roundRect(14, y, s, s, 4, stroke=0, fill=1)
        c.setFillColor(WHITE)
        corpo = 15 if len(self.sigla) < 3 else 12
        c.setFont('Pop-B', corpo)
        c.drawString(14 + (s - stringWidth(self.sigla, 'Pop-B', corpo)) / 2,
                     y + s / 2 - corpo * 0.36, self.sigla)
        x = 14 + s + 14
        c.setFillColor(INK)
        c.setFont('Pop-B', 18)
        c.drawString(x, self.h - 30, self.titolo)
        c.setFillColor(MUT)
        c.setFont('Lora', 9.4)
        c.drawString(x, self.h - 46, self.sotto)
        # la lunghezza a destra, grande, con l'unita' piccola accanto
        c.setFillColor(self.c)
        c.setFont('Pop-M', 10)
        c.drawRightString(self.w - 14, self.h - 40, 'm')
        c.setFont('Pop-B', 26)
        c.drawRightString(self.w - 14 - stringWidth('m', 'Pop-M', 10) - 3, self.h - 40,
                          str(self.lung))


class ChipRow(Flowable):
    """Riga di pastiglie dati (etichetta piccola + valore)."""

    def __init__(self, items, color, w=FW):
        self.items, self.c, self.w = items, color, w
        self.h = 34

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        n = len(self.items)
        gap = 7
        cw = (self.w - gap * (n - 1)) / n
        for i, (lab, val) in enumerate(self.items):
            x = i * (cw + gap)
            c.setFillColor(PAPER)
            c.roundRect(x, 0, cw, self.h, 3, stroke=0, fill=1)
            c.setFillColor(self.c)
            c.rect(x, 0, 2.4, self.h, stroke=0, fill=1)
            c.setFillColor(MUT)
            c.setFont('Pop-M', 6.5)
            c.drawString(x + 10, self.h - 13, lab.upper())
            c.setFillColor(INK)
            # il valore si rimpicciolisce fino a 7 pt prima di essere troncato
            corpo = 9.0
            while stringWidth(val, 'Pop-M', corpo) > cw - 18 and corpo > 7.0:
                corpo -= 0.5
            c.setFont('Pop-M', corpo)
            t = val
            while stringWidth(t, 'Pop-M', corpo) > cw - 18 and len(t) > 4:
                t = t[:-2]
            c.drawString(x + 10, 9, t)


class ColorKey(Flowable):
    """Legenda a scala cromatica delle 7 linee."""

    def __init__(self, data, w=FW):
        self.data, self.w = data, w
        self.h = 46

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        n = len(self.data)
        gap = 6
        cw = (self.w - gap * (n - 1)) / n
        for i, (num, length, note) in enumerate(self.data):
            x = i * (cw + gap)
            col = LC[num]
            c.setFillColor(col)
            c.rect(x, self.h - 6, cw, 6, stroke=0, fill=1)
            c.setFillColor(INK)
            c.setFont('Pop-B', 12)
            c.drawString(x, self.h - 24, '0%d' % num)
            c.setFillColor(INK2)
            c.setFont('Pop-M', 8.4)
            c.drawString(x, self.h - 36, length)
            c.setFillColor(MUT)
            c.setFont('Pop', 6.6)
            c.drawString(x, self.h - 45, note)


class PhotoStrip(Flowable):
    """Fascia fotografica a tutta larghezza colonna, con ritaglio verticale opzionale."""

    def __init__(self, path, w, ow, oh, caption='', color=None, ratio=None, focus=0.5):
        self.p, self.w = path, w
        self.full = w * oh / ow
        self.ih = w * ratio if ratio else self.full
        self.focus = focus
        self.cap, self.c = caption, color or BRAND
        self.h = self.ih + (13 if caption else 0)

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        y0 = self.h - self.ih
        c.saveState()
        p = c.beginPath()
        p.rect(0, y0, self.w, self.ih)
        c.clipPath(p, stroke=0, fill=0)
        sw, sh = self.w, self.full
        if sh < self.ih - 0.1:          # immagine troppo bassa: riempie in altezza
            sh = self.ih
            sw = self.w * (self.full / self.ih) ** 0 * (self.ih / self.full) ** 0
            sw = self.w * self.ih / self.full
        off = (sh - self.ih) * (1 - self.focus)
        c.drawImage(self.p, -(sw - self.w) / 2, y0 - off, sw, sh,
                    preserveAspectRatio=False, mask=None)
        c.restoreState()
        if self.cap:
            c.setFillColor(self.c)
            c.rect(0, self.h - self.ih - 11, 16, 2, stroke=0, fill=1)
            c.setFillColor(MUT)
            c.setFont('Pop', 7.4)
            # la didascalia sta su una riga: se e' piu' larga della foto si tronca
            # con i puntini, invece di finire sopra la didascalia accanto
            cap = self.cap
            while stringWidth(cap, 'Pop', 7.4) > self.w - 24 and len(cap) > 4:
                cap = cap[:-2].rstrip() + '…' if not cap.endswith('…') else cap[:-2] + '…'
            c.drawString(22, self.h - self.ih - 13.5, cap)


def photo_pair(p1, p2, c1, c2, ow=600, oh=900, color=None, w=FW,
               ratio=None, focus=0.5, ow2=None, oh2=None):
    """Due foto affiancate con didascalia."""
    cw = (w - 12) / 2
    a = PhotoStrip(p1, cw, ow, oh, c1, color, ratio, focus)
    b = PhotoStrip(p2, cw, ow2 or ow, oh2 or oh, c2, color, ratio, focus)
    t = Table([[a, b]], colWidths=[cw + 12, cw])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (0, 0), 12),
                           ('RIGHTPADDING', (1, 0), (1, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


def gear_block(title, items, color, coord=None, url=None, w=COL, note=None):
    """Blocco materiale con testata colorata."""
    rows = [[Paragraph(title.upper(), th)]]
    styles = [('BACKGROUND', (0, 0), (0, 0), color),
              ('LEFTPADDING', (0, 0), (-1, -1), 10),
              ('RIGHTPADDING', (0, 0), (-1, -1), 10),
              ('TOPPADDING', (0, 0), (0, 0), 6),
              ('BOTTOMPADDING', (0, 0), (0, 0), 6),
              ('TOPPADDING', (0, 1), (-1, -1), 3),
              ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
              ('BACKGROUND', (0, 1), (0, -1), PAPER),
              ('VALIGN', (0, 0), (-1, -1), 'TOP')]
    r = 1
    if coord:
        rows.append([Paragraph(
            '<font name="Pop" size="7.6">%s</font>' % A(url, coord, color),
            ParagraphStyle('co', fontName='Pop', fontSize=7.6, leading=10.4))])
        styles += [('BACKGROUND', (0, r), (0, r), tint(color, 0.16)),
                   ('TOPPADDING', (0, r), (0, r), 5),
                   ('BOTTOMPADDING', (0, r), (0, r), 5)]
        r += 1
    for it in items:
        rows.append([BU(it, color)])
        r += 1
    if note:
        rows.append([Paragraph(note, ParagraphStyle(
            'nt', fontName='Lora-I', fontSize=8.2, leading=11.4, textColor=MUT))])
        styles += [('TOPPADDING', (0, r), (0, r), 6)]
    styles.append(('BOTTOMPADDING', (0, len(rows) - 1), (0, len(rows) - 1), 9))
    t = Table(rows, colWidths=[w])
    t.setStyle(TableStyle(styles))
    return t


def two_cols(a, b, gap=14, w=FW):
    cw = (w - gap) / 2
    t = Table([[a, b]], colWidths=[cw + gap, cw])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (0, 0), gap),
                           ('RIGHTPADDING', (1, 0), (1, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


class DueColonne(Flowable):
    """Due blocchi affiancati (gear_block) che, se non entrano, continuano sulla pagina dopo.

    two_cols e' una tabella di una riga sola, e una riga non si spezza: i due lati di una
    linea, quando non entravano sotto la figura, saltavano interi alla pagina dopo e
    lasciavano un terzo di pagina bianco. Qui ogni colonna si spezza per conto suo, e la
    testata colorata si ripete in cima alla continuazione.
    """

    def __init__(self, a, b, gap=14, w=FW, minimo=70):
        self.a, self.b, self.gap, self.w, self.minimo = a, b, gap, w, minimo
        self.cw = (w - gap) / 2
        for t in (a, b):
            if isinstance(t, Table):
                t.repeatRows = 1
        self._t = two_cols(a, b, gap, w)

    def wrap(self, aw, ah):
        self.width, self.height = self._t.wrap(aw, ah)
        return self.width, self.height

    def draw(self):
        self._t.drawOn(self.canv, 0, 0)

    @staticmethod
    def _voci(t):
        """Le voci di una parte di colonna, senza la testata."""
        return len(t._cellvalues) - 1

    def _spezza(self, t, ah):
        """Spezza una colonna lasciando almeno due voci per parte: una voce sola in
        cima alla pagina dopo sembrava un errore (Brifing, edizione 0.4)."""
        h = ah
        while h >= self.minimo:
            pezzi = t.split(self.cw, h)
            if len(pezzi) < 2:
                return None
            if self._voci(pezzi[0]) >= 2 and self._voci(pezzi[1]) >= 2:
                return pezzi[0], pezzi[1]
            if self._voci(pezzi[0]) < 2:
                return None
            h -= 8
        return None

    def split(self, aw, ah):
        if ah < self.minimo:
            return []
        parti = []
        for t in (self.a, self.b):
            if t.wrap(self.cw, ah)[1] <= ah:
                parti.append((t, Spacer(1, 0)))
                continue
            pezzi = self._spezza(t, ah)
            if pezzi is None:
                return []
            parti.append(pezzi)
        (a1, a2), (b1, b2) = parti
        return [two_cols(a1, b1, self.gap, self.w),
                DueColonne(a2, b2, self.gap, self.w, self.minimo)]


def callout(title, text, color=BRAND, icon='!', w=FW, strong=False):
    """Riquadro di avviso / nota."""
    tc = WHITE if strong else INK
    bg = color if strong else tint(color, 0.10)
    ts = ParagraphStyle('ct', fontName='Pop-M', fontSize=9.2, leading=12.6,
                        textColor=tc)
    bs = ParagraphStyle('cb', fontName='Lora', fontSize=9.0, leading=13,
                        textColor=WHITE if strong else INK2)
    # Sul fondo pieno il segno [DA CONFERMARE], rosso, spariva: rosso su rosso.
    # Proprio nelle avvertenze il dato mancante non si vedeva. Qui diventa bianco
    # e in grassetto.
    if strong and text:
        text = _re_dc.sub(lambda m: '<b>%s</b>' % m.group(1), text)
    inner = [[Paragraph(unito(title), ts)]]
    if text:
        inner.append([Paragraph(unito(text), bs)])
    it = Table(inner, colWidths=[w - 46])
    it.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('TOPPADDING', (0, 0), (0, 0), 0),
                            ('BOTTOMPADDING', (0, 0), (0, 0), 2),
                            ('TOPPADDING', (0, 1), (-1, -1), 0)]))
    badge = Paragraph('<font name="Pop-B" size="13" color="%s">%s</font>'
                      % ((WHITE if strong else color).hexval().replace('0x', '#'), icon),
                      ParagraphStyle('bd', fontName='Pop-B', alignment=TA_CENTER, leading=16))
    t = Table([[badge, it]], colWidths=[26, w - 26])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg),
                           ('LINEBEFORE', (0, 0), (0, 0), 3, color),
                           ('LEFTPADDING', (0, 0), (0, 0), 8),
                           ('LEFTPADDING', (1, 0), (1, 0), 0),
                           ('RIGHTPADDING', (1, 0), (1, 0), 14),
                           ('TOPPADDING', (0, 0), (-1, -1), 10),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return t


def data_table(header, rows, widths, color=BRAND, zebra=True, aligns=None):
    data = [[Paragraph(h.upper(), th) for h in header]]
    for r in rows:
        data.append([x if hasattr(x, 'wrap') else Paragraph(str(x), td) for x in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), color),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LEFTPADDING', (0, 0), (-1, -1), 8),
          ('RIGHTPADDING', (0, 0), (-1, -1), 8),
          ('TOPPADDING', (0, 0), (-1, -1), 6),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
          ('LINEBELOW', (0, 1), (-1, -1), 0.5, HAIR)]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(('BACKGROUND', (0, i), (-1, i), PAPER))
    t.setStyle(TableStyle(st))
    return t


def photo_row(items, color=None, w=FW, gap=12):
    """Riga di foto con altezze uguali e larghezze proporzionali all'aspetto."""
    avail = w - gap * (len(items) - 1)
    inv = sum(ow / oh for _, ow, oh, _ in items)
    h = avail / inv
    cells, widths = [], []
    for i, (p, ow, oh, cap) in enumerate(items):
        cwi = h * ow / oh
        cells.append(PhotoStrip(p, cwi, ow, oh, cap, color))
        widths.append(cwi + (gap if i < len(items) - 1 else 0))
    t = Table([cells], colWidths=widths)
    st = [('LEFTPADDING', (0, 0), (-1, -1), 0),
          ('TOPPADDING', (0, 0), (-1, -1), 0),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
          ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('RIGHTPADDING', (len(items) - 1, 0), (-1, 0), 0)]
    for i in range(len(items) - 1):
        st.append(('RIGHTPADDING', (i, 0), (i, 0), gap))
    t.setStyle(TableStyle(st))
    return t


def _a_capo(testo, font, corpo, larghezza):
    """Spezza un testo in righe che stanno nella larghezza data.

    Solo sugli spazi normali: lo spazio non separabile (U+00A0) tiene insieme
    «[DA CONFERMARE]», che str.split() senza argomenti spezzerebbe.
    """
    righe, riga = [], ''
    for parola in re.split(r'[ \t\r\n]+', testo.strip()):
        prova = (riga + ' ' + parola).strip()
        if riga and stringWidth(prova, font, corpo) > larghezza:
            righe.append(riga)
            riga = parola
        else:
            riga = prova
    if riga:
        righe.append(riga)
    return righe or ['']


class Steps(Flowable):
    """Sequenza numerata su due colonne.

    La descrizione va a capo. Prima veniva accorciata un carattere alla volta
    finche' non entrava, e il passo 8 della cronologia finiva in «fino alle 17:».
    """

    INTERLINEA = 10.4

    def __init__(self, steps, color, w=FW, cols=2):
        self.s, self.c, self.w, self.cols = steps, color, w, cols
        cw = w / cols
        self.righe = [_a_capo(d, 'Lora', 8.2, cw - 34) for _, d in steps]
        n_righe = (len(steps) + cols - 1) // cols
        self.alt_riga = []
        for r in range(n_righe):
            gruppo = self.righe[r * cols:(r + 1) * cols]
            self.alt_riga.append(24 + self.INTERLINEA * max(len(g) for g in gruppo))
        self.h = sum(self.alt_riga)

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        cw = self.w / self.cols
        cima = self.h
        for r, alt in enumerate(self.alt_riga):
            for k in range(self.cols):
                i = r * self.cols + k
                if i >= len(self.s):
                    break
                t, _ = self.s[i]
                x = k * cw
                y = cima - 14          # linea di base del titolo del passo
                cv.setFillColor(self.c)
                cv.circle(x + 9, y + 3, 9, stroke=0, fill=1)
                cv.setFillColor(WHITE)
                cv.setFont('Pop-B', 8.4)
                n = str(i + 1)
                cv.drawString(x + 9 - stringWidth(n, 'Pop-B', 8.4) / 2, y, n)
                cv.setFillColor(INK)
                cv.setFont('Pop-M', 8.6)
                cv.drawString(x + 25, y + 3, t)
                cv.setFillColor(MUT)
                cv.setFont('Lora', 8.2)
                for k2, riga in enumerate(self.righe[i]):
                    cv.drawString(x + 25, y - 9 - k2 * self.INTERLINEA, riga)
            cima -= alt


class Bars(Flowable):
    """Confronto lunghezze: barre orizzontali colorate."""

    def __init__(self, data, w=FW, unit='m'):
        self.d, self.w, self.unit = data, w, unit
        self.rh = 24
        self.h = len(data) * self.rh + 6

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        mx = max(v for _, v, _ in self.d)
        x0, x1 = 74, self.w - 44
        for i, (label, v, col) in enumerate(self.d):
            y = self.h - (i + 1) * self.rh
            cv.setFillColor(INK2)
            cv.setFont('Pop-M', 8.2)
            cv.drawString(0, y + 6, label)
            cv.setFillColor(PAPER2)
            cv.rect(x0, y + 4, x1 - x0, 11, stroke=0, fill=1)
            cv.setFillColor(col)
            cv.rect(x0, y + 4, (x1 - x0) * v / mx, 11, stroke=0, fill=1)
            cv.setFillColor(INK)
            cv.setFont('Pop-M', 8.2)
            cv.drawRightString(self.w, y + 6, '%d %s' % (v, self.unit))


# ---------------------------------------------------------------- aggiunte 0.4
class Checklist(Flowable):
    """Caselle da spuntare, su una o piu' colonne.

    Ripresa dalla guida Sillschlucht: serve alle schede di rilievo per le foto da
    fare. Il testo va a capo invece di essere accorciato.
    """

    def __init__(self, items, color, w=FW, cols=2, corpo=8.4):
        self.items, self.c, self.w, self.cols, self.corpo = items, color, w, cols, corpo
        cw = w / cols
        self.righe = [_a_capo(t, 'Lora', corpo, cw - 24) for t in items]
        n_righe = (len(items) + cols - 1) // cols
        self.alt = []
        for r in range(n_righe):
            gruppo = self.righe[r * cols:(r + 1) * cols]
            self.alt.append(6 + (corpo + 3) * max(len(g) for g in gruppo))
        self.h = sum(self.alt)

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        cv = self.canv
        cw = self.w / self.cols
        cima = self.h
        for r, alt in enumerate(self.alt):
            for k in range(self.cols):
                i = r * self.cols + k
                if i >= len(self.items):
                    break
                x = k * cw
                y = cima - self.corpo - 3
                cv.setStrokeColor(self.c)
                cv.setLineWidth(1)
                cv.rect(x, y - 1, 8, 8, stroke=1, fill=0)
                cv.setFillColor(INK2)
                cv.setFont('Lora', self.corpo)
                for k2, riga in enumerate(self.righe[i]):
                    cv.drawString(x + 15, y - k2 * (self.corpo + 3), riga)
            cima -= alt


def livello_chip(testo, colore):
    """Etichetta piccola e colorata, per lo stato di una linea nelle tabelle."""
    return Paragraph('<font name="Pop-M" size="7.2" color="#%s">%s</font>'
                     % (colore.hexval()[2:], testo.upper()),
                     ParagraphStyle('lv', fontName='Pop', leading=10))
