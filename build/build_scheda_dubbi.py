# -*- coding: utf-8 -*-
"""Scheda di verifica sul campo — dubbi aperti del manuale di rigging.

Versione da compilare a mano insieme a chi ha montato la linea. Riporta i punti
che in DUBBI.md risultano ancora aperti, raggruppati come lì, ciascuno con il
timestamp della fonte da cui il dubbio nasce e lo spazio per scrivere la risposta.

Nessuna domanda e' inventata: ogni voce e' la trascrizione di una riga di
DUBBI.md. Le voci gia' chiuse non compaiono.

    python build/build_scheda_dubbi.py
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,   # noqa: E402
                                PageBreak, Table, TableStyle, Paragraph,
                                Spacer, KeepTogether)

OUT = RADICE / 'output' / 'Bismantova_Dubbi_Scheda_Campo.pdf'

LINEA = HexColor(0xF97316)      # colore che i-pietra assegna a questa linea
C_ANC = LC[1]                   # ancoraggio      (rosso)
C_SOS = LC[7]                   # sosta / slinga  (azzurro)
C_TEN = LC[3]                   # lato tensione   (ambra)
C_ASL = LC[5]                   # anti-slip       (verde)


# ---------------------------------------------------------------- componenti
# Righe e campo stanno in build/campi.py: li usa anche schede_linee.py per le
# schede di rilievo, e una seconda copia sarebbe divergita alla prima modifica.
from campi import Righe, campo                                      # noqa: E402,F401

qs = ParagraphStyle('q', fontName='Lora', fontSize=9.8, leading=13.8, textColor=INK)
fs = ParagraphStyle('f', fontName='Pop-M', fontSize=7.0, leading=10, textColor=MUT)
bs = ParagraphStyle('b', fontName='Pop-B', fontSize=13, leading=15,
                    alignment=TA_RIGHT)


def domanda(num, testo, fonte, color, righe=2, prio=False):
    """Un dubbio: pastiglia col numero, testo, fonte, spazio per la risposta."""
    testa = ''
    if prio:
        testa = '<font color="%s">PRIORITARIO</font> &nbsp;·&nbsp; ' % \
                WARN.hexval().replace('0x', '#')
    inner = [[Paragraph(testo, qs)]]
    if fonte or prio:
        inner.append([Paragraph(testa + fonte.upper(), fs)])
    inner.append([Righe(righe, w=FW - 47)])
    it = Table(inner, colWidths=[FW - 47])
    it.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
    ]))
    badge = Paragraph('<font color="%s">%s</font>'
                      % (color.hexval().replace('0x', '#'), num), bs)
    t = Table([[badge, it]], colWidths=[34, FW - 34])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, 0), 'TOP'),
        ('LINEBEFORE', (1, 0), (1, 0), 2.5, color),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 12),
        ('LEFTPADDING', (1, 0), (1, 0), 13),
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (0, 0), 1),
        ('TOPPADDING', (1, 0), (1, 0), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return KeepTogether([t, SP(13)])


# ---------------------------------------------------------------- pagina
def page_end(cv, doc):
    n = cv.getPageNumber()
    acc = getattr(cv, '_accent', LINEA)
    sect = getattr(cv, '_sect', '')
    cv.setFont('Pop-M', 7)
    cv.setFillColor(MUT)
    cv.drawString(LM, H - 44, 'BISMANTOVA · ANFITEATRO · SCHEDA DI VERIFICA SUL CAMPO')
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


def sezione(num, titolo, occhiello, color, intro, voci):
    sec(color, label=titolo)
    S.append(LineHeader(num, titolo, occhiello, color))
    S.append(SP(10))
    S.append(P(intro, body))
    S.append(SP(14))
    for v in voci:
        S.append(domanda(v[0], v[1], v[2], color,
                         righe=v[3] if len(v) > 3 else 2,
                         prio=v[4] if len(v) > 4 else False))
    S.append(PageBreak())


# ================================================================ apertura
sec(LINEA, 'Come si usa')
S.append(LineHeader('', 'Dubbi da chiarire con chi ha montato', 'Scheda di verifica · edizione '
                    'del 20/08/2026', LINEA))
S.append(SP(12))
S.append(P('Questa scheda raccoglie i punti che il manuale non può stampare perché nessuna '
           'fonte disponibile li documenta. Non sono curiosità redazionali: finché restano '
           'vuoti, il manuale resta un\'edizione di lavoro e non un riferimento operativo.',
           lead))
S.append(SP(12))
S.append(P('Ogni voce porta il <b>numero</b> con cui compare in <b>DUBBI.md</b> e, in piccolo, '
           'la <b>fonte del dubbio</b>: il video e il minuto in cui la questione nasce, oppure '
           'la fotografia. Il numero serve a riportare la risposta nel file senza ambiguità — '
           'scrivere accanto alla riga giusta è più importante che scrivere molto.', body))
S.append(SP(16))
S.append(callout('La regola di questo progetto',
                 'Una risposta incerta è peggio di una casella vuota. Se nessuno se lo '
                 'ricorda con sicurezza, lasciare in bianco e annotare «non ricordato»: '
                 'il manuale sa già come dichiarare un dato mancante. Un numero plausibile '
                 'ma sbagliato, in un documento che descrive una linea sospesa nel vuoto, '
                 'è un rischio reale.', WARN, icon='!', strong=True))
S.append(SP(16))
S.append(P('<b>Le sette voci segnate PRIORITARIO</b> sono quelle che DUBBI.md indica come '
           'più gravi: la portata delle brache, il nome della linea e quello del settore, '
           'la fotografia dell\'ancoraggio, la lunghezza della campata, il nastro e il suo '
           'backup. Se il tempo con i ragazzi '
           'è poco, si parte da lì.', body))
S.append(SP(14))
S.append(data_table(
    ['Sezione', 'Voci', 'Che tipo di risposta serve'],
    [['1 · Quadro generale', '1-7', 'Misure e dati della linea e della giornata'],
     ['2 · Materiale', '8-24', 'Lunghezze, diametri, modelli, quantità'],
     ['3 · Manovre', '25-36', 'Nomi di nodi, sequenze, esecuzione'],
     ['4 · Ancoraggio', '37-41, 50-51', 'Verifiche a immagine e scatti da fare'],
     ['5 · Nome e fonti', '42-52', 'Denominazione, locandina, buchi di ripresa']],
    [118, 78, FW - 196], color=LINEA))
S.append(PageBreak())

# ================================================================ 1 · quadro
sezione('1', 'Quadro generale della linea', 'Sezione 1 · dati di testata', LINEA,
        'Dati che vanno nella testata del manuale e nella planimetria. Nessuno di questi '
        'viene pronunciato nei video: vanno misurati o ricordati.',
        [(1, 'Lunghezza effettiva della campata. Il catalogo i-pietra e la locandina danno '
             '53 m, ma è un dato di catalogo, non una misura fatta sui punti. Quanto misura '
             'davvero da placchetta a placchetta?',
          'mai pronunciata · nota N2 del manuale', 2, True),
         (2, 'Dislivello fra i due lati — l\'offlevel. Quanto, e da che parte pende? '
             'Influenza il tensionamento.', 'mai pronunciato'),
         (3, 'Coordinate GPS dell\'<b>ancoraggio opposto</b>. Quello main lo ha dato l\'EXIF '
             'di IMG_1416 — 44.419869, 10.412353 — perche\' la foto e\' stata scattata '
             'standoci. Basta una foto geolocalizzata di la\'.',
          'IMG_1416 · main risolto il 20/08/2026'),
         (4, 'Accesso e avvicinamento: da dove si parte, quanto si cammina, dove si '
             'parcheggia.', 'mai descritto', 3),
         (5, 'Autorizzazioni, divieti stagionali per nidificazione, accordi con il gestore. '
             'La Pietra è area protetta: se c\'è qualcosa da sapere, va scritto.',
          'mai nominati', 3),
         (6, 'Tempo reale di montaggio. I video coprono 2 h 38 min ma non dicono a che ora '
             'si è cominciato e a che ora si è finito.', 'metadati dei file'),
         (7, 'Quante persone servono per montare questa linea — non quante c\'erano quel '
             'giorno. Va nella checklist pre-uscita.', '[IMG_1373 @ 0:24] cita «quattro»')])

# ================================================================ 2 · materiale
sezione('2', 'Materiale', 'Sezione 2 · tabella materiale', C_TEN,
        'La tabella materiale del manuale è costruita incrociando i nomi pronunciati nei '
        'video con gli oggetti visibili nei fotogrammi. Mancano quasi tutte le misure.',
        [(8, 'Fettucce <b>viola</b> della sosta main: lunghezza e tipo.',
          '[IMG_1349 @ 0:00]'),
         (9, 'Corde <b>rosa</b> del backup: diametro, tipo e lunghezza.',
          '[IMG_1349 @ 0:00]'),
         (10, 'Modello del <b>BFK</b> montato sulla corda rosa.', '[IMG_1350 @ 0:00]'),
         (11, 'Corda <b>azzurra</b> usata come tagline e poi come linea vita: diametro e '
              'lunghezza.', '[IMG_1350 @ 0:37]'),
         (12, 'Le <b>4 maglie delta</b>: misura e materiale. La quantità è l\'unico numero '
              'certo di tutto il corpus.', '[IMG_1350 @ 0:53]'),
         (13, 'Cos\'è il «<b>Mighty Lock</b>», descritto come «quello quadratino»? Il nome è '
              'storpiato dalla trascrizione.', '[IMG_1351 @ 0:19-0:28]'),
         (14, 'Fettuccia <b>verde lunga</b>, «la più grossa che c\'è»: che misura?',
          '[IMG_1369 @ 0:31]'),
         (15, 'Fettuccia <b>piccola viola</b> dell\'ancoraggio: che misura?',
          '[IMG_1373 @ 0:41]'),
         (16, 'Fettuccia <b>verde e nera</b>: che misura?', '[IMG_1389 @ 0:02]'),
         (17, 'La «<b>banana</b>» è il weblock azzurro anodizzato — confermato a immagine. '
              'Resta il <b>modello</b>.', '[IMG_1381 @ 0:12] · visibile in IMG_1384 @ 0:03'),
         (18, 'Modello del <b>softrelease</b>.', '[IMG_1394 @ 0:15]'),
         (19, '<b>Grilli</b>: misura e tipo.', '[IMG_1384 @ 0:00]'),
         (20, 'Composizione del <b>paranchino di tensionamento della base</b>: quante '
              'carrucole, che rapporto.', '[IMG_1380 @ 0:09]', 3),
         (21, 'Quanti <b>Grigri</b> in totale, e montati su cosa. «Un altro Grigri» implica '
              'almeno due.', '[IMG_1378 @ 0:42]'),
         (22, '<b>Nastro della highline</b>: marca, larghezza, tipo. Non è mai nominato in '
              'nessuno dei quarantadue video. In IMG_1401 appare bianco o crema.',
          'mai nominato · cfr. voce 51', 2, True),
         (23, '<b>Backup della linea</b>: è nastro o corda, e quale. In IMG_1401 si vede un '
              'secondo nastro chiaro parallelo.', 'mai specificato · cfr. voce 51', 2, True),
         (24, '<b>Leash</b> e ancoraggio della leash.', 'mai nominati')])

# ================================================================ 3 · manovre
sezione('3', 'Manovre', 'Sezione 3 · sequenza di montaggio', C_SOS,
        'Qui il problema non è la misura ma il nome e l\'esecuzione. Diverse manovre sono '
        'filmate e comprensibili a immagine, ma nessuno le chiama per nome.',
        [(25, 'Che nodo è quello descritto come «<b>pista, pif, paf, sotto, torna sotto</b>»? '
              'È il passaggio centrale della sosta.', '[IMG_1366 @ 0:00]', 3),
         (26, 'Che nodo è quello «<b>per forzare la slinga</b>», regolabile? È l\'unica '
              'manovra motivata a voce, ma resta senza nome.', '[IMG_1367 @ 0:43]', 3),
         (27, '«<b>Slide next</b>» sui 3 punti: qual è il termine reale?',
          '[IMG_1374 @ 0:42]'),
         (28, 'Come sono <b>collegati ed equalizzati i 3 punti</b>, e con che angolo di '
              'apertura? A immagine si vede corda verde acqua annodata, non fettuccia '
              'scorrevole. Manca l\'inquadratura d\'insieme.', 'IMG_1371.JPEG', 3),
         (29, 'Quale componente è quello che «<b>ruotando può cadere</b>»? Deve diventare '
              'un\'avvertenza, ma non si sa di cosa parli.', '[IMG_1370 @ 0:00-0:15]'),
         (30, 'Quale operazione è quella che «<b>andrebbe fatta dopo, quando c\'è del '
              'peso</b>»?', '[IMG_1380 @ 0:57]'),
         (31, 'Come si costruisce l\'<b>anti-slip</b>: che nodo, che materiale, in che punto. '
              'La funzione è chiara, l\'esecuzione no.',
          '[IMG_1395 @ 0:25] · [IMG_1384 @ 0:55]', 3),
         (32, 'Cos\'è il «<b>blocco del backup</b>» che prende sia la sosta backup sia la '
              'sosta main? È un concetto centrale e non è mai illustrato a parole.',
          '[IMG_1384 @ 0:37]', 3),
         (33, '<b>Tensione finale</b> raggiunta e come è stata misurata. L\'audio dice solo '
              '«la tensioniamo a modo».', '[IMG_1383 @ 0:19]'),
         (34, 'Come è stata <b>portata la linea da un lato all\'altro</b>? Tagline a mano, '
              'drone, altro? Il drone è citato ma riferito ad altri.',
          '[IMG_1363 @ 0:10-0:14]', 3),
         (35, 'Sequenza di <b>smontaggio</b>. Non è ripresa in nessun video.',
          'mai filmata', 3),
         (36, '<b>Checklist pre-uscita</b> realmente usata. Nelle riprese nessuno enuncia '
              'una lista di controlli.', 'mai dettata', 3)])

# ================================================================ 4 · ancoraggio
sezione('4', 'Ancoraggio e verifiche a immagine', 'Sezione 4 · da guardare e fotografare',
        C_ANC,
        'Voci emerse esaminando i fotogrammi. Alcune si chiudono guardando meglio, altre '
        'richiedono uno scatto nuovo da fare sul posto.',
        [(37, '<b>Portata (WLL) delle brache.</b> Il tipo è confermato: brache ad anello '
              'industriali. In IMG_1366 @ 0:17 la viola ha una riga nera, e viola + 1 riga '
              'in EN 1492-2 vale 1 t — ma due indizi convergenti non sono una marcatura. '
              '<b>Serve la fotografia di un\'etichetta.</b>',
          'IMG_1366 @ 0:17 · il danno peggiore possibile se sbagliata', 2, True),
         (38, 'Nell\'ancoraggio c\'è <b>protezione veloce</b> — un friend — accanto ai punti '
              'fissi? Un dispositivo compatibile si intravede ma il fotogramma è mosso. '
              '<b>Scatto da fare sul campo.</b>',
          'IMG_1374 @ 0:33 · nota N1 del manuale', 2, True),
         (39, 'I <b>punti</b> sono placchetta metallica su bullone con dado esagonale — '
              'confermato a immagine, quindi tassello meccanico. Restano <b>marca e '
              'diametro del bullone</b>.', 'IMG_1371.JPEG · IMG_1372.JPEG'),
         (40, '<b>Marca</b> della carrucola bloccante nera con puleggia arancio. Le marcature '
              'lette sono CE 0082, UK CA 20, EN 567:2013, Ø 7,8-11 mm; il logo non è '
              'leggibile.', 'IMG_1371.JPEG · dettaglio in lavorazione/dettagli/'),
         (41, 'La <b>corda verde acqua</b> è la linea vita o il cordino di collegamento fra '
              'i punti? In IMG_1371 si vede annodata fra i punti dell\'ancoraggio. Le due '
              'funzioni potrebbero coesistere.', 'IMG_1371.JPEG · [IMG_1350 @ 0:33]', 3),
         (50, '<b>A-frame</b>: quanto sono <b>alti</b> i pali, che legno e che diametro, '
              'come sono legati in testa, e di quanto sollevano la linea sopra il bordo? '
              'In IMG_1416 attorno al piede di un palo si vedono giri di <b>filo '
              'metallico</b>: tengono il palo o sono un recinto che c\'era già?',
          'IMG_1396 · IMG_1416', 4),
         (54, 'Sullo sfondo di IMG_1416 e IMG_1396 corre una <b>linea tesa con sotto una '
              'seconda linea appesa a festoni</b>. È la campata della 53 m vista di '
              'scorcio o <b>un\'altra linea</b> dello spot? E la linea a festoni che cos\'è '
              '— backup, tagline lasciata in posa, altro?', 'IMG_1416 · IMG_1396', 4),
         (51, 'Il nastro appare <b>bianco o crema</b> in IMG_1401, con un secondo nastro '
              'chiaro parallelo. Se confermato chiude le voci 22 e 23.',
          'foto/IMG_1401.JPG')])

# ================================================================ 5 · nome e fonti
sezione('5', 'Nome della linea, fonti, buchi di ripresa', 'Sezione 5 · apparato', C_ASL,
        'Questioni editoriali, ma una di queste è il rischio più concreto dell\'intero '
        'documento.',
        [(45, '<b>Titolo definitivo del manuale.</b> «La 50» collide con la <b>50 M del '
              'Settore Giallo</b>, che esiste davvero: un lettore potrebbe attrezzare la '
              'linea sbagliata. Come si chiama davvero questa linea fra di voi?',
          'locandina · l\'ambiguità più pericolosa del documento', 3, True),
         (52, '<b>I due cataloghi non concordano sul nome del settore.</b> i-pietra '
              'etichetta «Anfiteatro» anche le tre linee che la locandina mette sotto '
              '<b>Anfite-altro</b> — 22, 30 e 135 m. Qual è il nome che usate voi?',
          'render 3D i-pietra · stesso rischio del dubbio 45', 3, True),
         (42, 'Dati presi da i-pietra da validare: settore <b>Anfiteatro</b>, roccia '
              '<b>arenaria</b>, colore linea <b>#F97316</b>. Se il manuale li stampa devono '
              'essere corretti anche fuori dall\'app.', 'catalogo i-pietra'),
         (43, 'La <b>locandina</b> «La Pietra — Yeah Vez!» è stata letta, ma il file '
              'disponibile è uno screenshot 1600×720 con bande nere: non è stampabile in '
              'A4. Serve il file sorgente.', 'fonti/locandina_la_pietra.jpeg'),
         (44, '<b>Anno</b> del Bismantova Highline Meeting riportato sul logo della '
              'locandina. Il logo è poco leggibile.', 'locandina'),
         (46, 'Cos\'è la «<b>Bifida</b>»? Non compare sulla locandina.',
          '[IMG_1373 @ 0:24]'),
         (49, 'Fra le <b>15:38 e le 17:08</b> non esiste nessuna ripresa, ma alle 17:08 la '
              'linea è montata e camminata. Manca la documentazione del tensionamento '
              'finale e dei primi passaggi: cosa è successo in quell\'ora e mezza?',
          'metadati · il manuale deve dichiarare il buco', 3)])

# ================================================================ chiusura
sec(LINEA, 'Dopo la compilazione')
S.append(LineHeader('', 'Riportare le risposte', 'Chiusura', LINEA))
S.append(SP(12))
S.append(P('Le risposte raccolte vanno riportate in <b>DUBBI.md</b>, sulla riga del numero '
           'corrispondente, indicando la data e chi ha risposto — come è già stato fatto per '
           'i tre bloccanti chiusi il 19/08/2026. Solo dopo si rigenera il manuale.', body))
S.append(SP(14))
S.append(callout('Le fotografie che mancano',
                 'Due voci non si chiudono a parole: l\'etichetta di una braca (voce 37) e '
                 'l\'insieme dei tre punti dell\'ancoraggio, con il dispositivo di '
                 'protezione veloce se c\'è (voce 38). Sono due scatti. Vale la pena farli '
                 'nella stessa uscita in cui si rimisura la campata.', C_ANC))
S.append(SP(20))
S.append(two_cols(campo('Compilata il', COL), campo('Compilata da', COL)))
S.append(SP(16))
S.append(campo('Hanno risposto', FW))
S.append(SP(16))
S.append(campo('Note libere', FW))
S.append(Righe(5))
S.append(SP(14))
S.append(P('Scheda generata da build/build_scheda_dubbi.py sulle voci aperte di DUBBI.md. '
           'Le voci già chiuse — B1, B2, B3, 47, 48, M2 — non compaiono.', small))

# ---------------------------------------------------------------- build
OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM,
                      title='Bismantova · Anfiteatro · Scheda di verifica sul campo',
                      author='Dubbi aperti del manuale di rigging')
frame = Frame(LM, BM, FW, H - TM - BM, id='n',
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPageEnd=page_end)])
doc.build(S)
print('scritto %s' % OUT)
