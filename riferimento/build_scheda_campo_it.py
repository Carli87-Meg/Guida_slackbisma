# -*- coding: utf-8 -*-
"""Scheda rapida da campo — una pagina A4, pensata per la stampa e la plastificazione."""
from design import *
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = '/mnt/user-data/outputs/Sillschlucht_Scheda_Campo_IT.pdf'
IMG = 'img/'
M = 34.0                      # margini stretti: è una scheda densa
CW = W - 2 * M

c = pdfcanvas.Canvas(OUT, pagesize=A4)
c.setTitle('Sillschlucht · Scheda rapida da campo')


def txt(x, y, s, font='Pop', size=8, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, s)


def rtxt(x, y, s, font='Pop', size=8, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawRightString(x, y, s)


def eyeb(x, y, s):
    c.setFillColor(MUT)
    c.setFont('Pop-M', 7)
    c.drawString(x, y, '   '.join(s.upper().split(' ')).replace('  ', ' '))


def section(y, title):
    c.setFillColor(MUT)
    c.setFont('Pop-M', 7.2)
    c.drawString(M, y, title.upper())
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.6)
    c.line(M + stringWidth(title.upper(), 'Pop-M', 7.2) + 10, y + 2.4, W - M, y + 2.4)


# ---------------------------------------------------------------- testata
c.setFillColor(BRAND)
c.rect(0, H - 96, W, 96, stroke=0, fill=1)
seg = W / 7
for i in range(1, 8):
    c.setFillColor(LC[i])
    c.rect((i - 1) * seg, H - 6, seg, 6, stroke=0, fill=1)
txt(M, H - 46, 'SILLSCHLUCHT', 'Pop-B', 25, WHITE)
txt(M, H - 62, 'Scheda rapida da campo · edizione italiana', 'Pop-L', 10, HexColor(0xA9BEC7))
txt(M, H - 82, 'Innsbruck · Tirolo · 7 linee da 70 a 102 m', 'Pop', 8, HexColor(0x8FA6B0))

c.setFillColor(WARN)
c.rect(W - M - 196, H - 84, 196, 46, stroke=0, fill=1)
txt(W - M - 186, H - 56, 'REGISTRA LA LINEA', 'Pop-B', 10.5, WHITE)
txt(W - M - 186, H - 70, 'Obbligatorio, almeno 1 giorno prima', 'Pop-L', 7.6, WHITE)
c.drawImage('qr_reg.png', W - M - 40, H - 80, 36, 36, mask=None)

y = H - 122

# ---------------------------------------------------------------- tabella linee
section(y, 'Le sette linee')
y -= 16

hdrs = [('LINEA', M + 2), ('M', M + 62), ('LATO TENSION', M + 96), ('LATO STATICO', M + 280),
        ('COORDINATE STATICO', M + 400)]
c.setFillColor(BRAND)
c.rect(M, y - 5, CW, 15, stroke=0, fill=1)
for t, x in hdrs:
    txt(x, y, t, 'Pop-M', 6.8, WHITE)
y -= 16

rows = [
    (1, '76', 'Fettucce 1,5 m su albero', '2 fettucce da 2 m', '47.243664, 11.396161'),
    (2, '70', 'Rinvio albero arretrato (6 m + 1 m)', '2 fettucce da 2 m', '47.243449, 11.395749'),
    (2, '70', 'Freestyle · A-frame, brache 4 m', 'Brache da 2 m', 'non indicate'),
    (3, '70', 'Freestyle · rinvio sul pino', 'Compensato', '47.243363, 11.395760'),
    (4, '70', 'Freestyle · A-frame, brache 2 t', 'Compensato', '47.243338, 11.395728'),
    (5, '90', 'Offlevel · come Linea 2', '2 fettucce da 2 m', '47.243122, 11.395540'),
    (6, '102', 'Fettucce 1,5 m su albero', '2 fettucce da 2 m', '47.242824, 11.394620'),
    (7, '100', 'Mai montata — nessun dato', '—', '—'),
]
for i, (n, m, ten, sta, co) in enumerate(rows):
    rh = 15.5
    if i % 2 == 1:
        c.setFillColor(PAPER)
        c.rect(M, y - 4.5, CW, rh, stroke=0, fill=1)
    c.setFillColor(LC[n])
    c.rect(M + 2, y - 1, 7, 7, stroke=0, fill=1)
    txt(M + 13, y, str(n), 'Pop-M', 8)
    txt(M + 62, y, m, 'Pop-M', 8)
    txt(M + 96, y, ten, 'Pop', 7.6, INK2)
    txt(M + 280, y, sta, 'Pop', 7.6, INK2)
    txt(M + 400, y, co, 'Pop', 7.4, MUT)
    y -= rh
txt(M + 2, y - 5, 'Linea 1 · lato tension: 47.243861, 11.395109      Linea 6 · lato tension: '
                  '47.243703, 11.394951', 'Pop', 7, MUT)
txt(M + 2, y - 17, 'Le due righe «2» sono la stessa linea del Lageplan, montata in due modi.', 'Pop', 7, MUT)
y -= 34

# ---------------------------------------------------------------- kit + sequenza
section(y, 'Kit di base per un ancoraggio')
y -= 16
colw = (CW - 16) / 2
top = y

kit_t = ['2 brache (1,5–6 m secondo la linea)', '1–2 protezioni per l\'albero',
         'Weblock con softrelease oppure Orange', '2–4 grilli, eventualmente 1 di rinvio']
kit_s = ['2 brache da 2 m', '1 protezione per l\'albero', '2 grilli',
         'Tagline ~100 m + Microtrax']
for j, (title, items, col) in enumerate([('Lato tension', kit_t, BRAND),
                                         ('Lato statico', kit_s, BRAND)]):
    x = M + j * (colw + 16)
    bh = 20 + len(items) * 12
    c.setFillColor(PAPER)
    c.rect(x, y - bh + 12, colw, bh, stroke=0, fill=1)
    c.setFillColor(col)
    c.rect(x, y + 9, colw, 3, stroke=0, fill=1)
    txt(x + 9, y - 2, title, 'Pop-M', 8.4)
    yy = y - 16
    for it in items:
        c.setFillColor(col)
        c.circle(x + 12, yy + 3, 1.5, stroke=0, fill=1)
        txt(x + 19, yy, it, 'Lora', 7.8, INK2)
        yy -= 12
y = top - 20 - 4 * 12 - 14

# ---------------------------------------------------------------- sequenza
section(y, 'Sequenza di montaggio')
y -= 18
steps = ['Annuncia la linea', 'Monta gli ancoraggi', 'Recupera la fishingline',
         'Collega la tagline', 'Tira la highline', 'Tensiona e verifica']
sw = CW / 6
for i, s in enumerate(steps):
    x = M + i * sw
    c.setFillColor(BRAND)
    c.circle(x + 8, y + 3, 8, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont('Pop-B', 8)
    c.drawString(x + 8 - stringWidth(str(i + 1), 'Pop-B', 8) / 2, y, str(i + 1))
    if i < 5:
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.8)
        c.line(x + 18, y + 3, x + sw - 4, y + 3)
    c.setFillColor(INK2)
    c.setFont('Pop', 6.8)
    t = s
    while stringWidth(t, 'Pop', 6.8) > sw - 6 and len(t) > 5:
        t = t[:-2]
    c.drawString(x, y - 14, t)
y -= 34

# ---------------------------------------------------------------- checklist
section(y, 'Checklist pre-uscita')
y -= 16
chk = ['Linea registrata (≥ 1 giorno prima)', 'Tagline ≥ 100 m (≥ 110 m Linea 6)',
       'Mulinello da pesca a mosca', 'Microtrax per il tiro',
       'Protezioni albero per ogni ancoraggio', 'Weblock + softrelease',
       'Brache e grilli secondo la linea', 'Smontaggio prima di sera']
for i, t in enumerate(chk):
    col, row = i % 2, i // 2
    x = M + col * (CW / 2)
    yy = y - row * 15
    c.setStrokeColor(BRAND)
    c.setLineWidth(0.9)
    c.rect(x, yy - 1, 8, 8, stroke=1, fill=0)
    txt(x + 14, yy, t, 'Lora', 8, INK2)
y -= 4 * 15 + 14

# ---------------------------------------------------------------- planimetria + regole
y -= 10
section(y, 'Planimetria e regole')
y -= 12

bh = 190.0
mw = 218.0
c.saveState()
p = c.beginPath()
p.rect(M, y - bh, mw, bh)
c.clipPath(p, stroke=0, fill=0)
mh = mw * 741 / 849
c.drawImage(IMG + 'p02_0.png', M, y - bh + (bh - mh) / 2, mw, mh, mask=None)
c.restoreState()
c.setFillColor(WHITE)
c.rect(M, y - bh, mw, 13, stroke=0, fill=1)
txt(M + 4, y - bh + 4, 'Numeri e colori come nella guida', 'Pop', 6.6, MUT)

xr = M + mw + 14
wr = CW - mw - 14

c.setFillColor(WARN)
c.rect(xr, y - 92, wr, 92, stroke=0, fill=1)
txt(xr + 14, y - 20, 'LE TRE REGOLE DELLO SPOT', 'Pop-B', 9.4, WHITE)
for i, t in enumerate([
        '1.  Registrazione obbligatoria almeno un giorno prima,',
        '     per la sicurezza del traffico aereo.',
        '2.  Nessuna linea incustodita durante la notte.',
        '3.  Nessun permarig incustodito nella Sillschlucht.']):
    txt(xr + 14, y - 37 - i * 13, t, 'Pop-L', 7.8, WHITE)

c.setFillColor(PAPER)
c.rect(xr, y - bh, wr, bh - 104, stroke=0, fill=1)
c.setFillColor(BRAND)
c.rect(xr, y - 104 - 3, wr, 3, stroke=0, fill=1)
c.drawImage('qr_tir.png', xr + 12, y - bh + 20, 52, 52, mask=None)
txt(xr + 76, y - 124, 'Verein Tiroliners', 'Pop-M', 8.6)
c.setFillColor(MUT)
c.setFont('Pop', 7)
for i, t in enumerate(['Altri spot legali in Tirolo, prestito',
                       'gratuito di materiale highline e',
                       'slackline, iscrizione al club.']):
    c.drawString(xr + 76, y - 137 - i * 10, t)
txt(xr + 76, y - bh + 24, 'tiroliners.at', 'Pop-M', 7.4, BRAND)
y -= bh + 14

# ---------------------------------------------------------------- piede
c.setStrokeColor(HAIR)
c.setLineWidth(0.6)
c.line(M, 46, W - M, 46)
txt(M, 33, 'Sintesi della Guida Highline Sillschlucht (10 agosto 2026), edizione italiana. '
           'Coordinate arrotondate a 6 decimali: per il dettaglio completo vedi la guida.',
    'Pop', 6.8, MUT)
txt(M, 23, 'Highlining e slacklining comportano rischi: questa scheda non sostituisce '
           'formazione, esperienza e verifica autonoma di ogni ancoraggio.', 'Pop', 6.8, MUT)

c.showPage()
c.save()
print('ok')
