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
C_FOT = LC[6]                   # file LineeBisma e sue foto (verde acqua)


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
    cv.drawString(LM, H - 44, 'PIETRA DI BISMANTOVA · SCHEDA DI VERIFICA SUL CAMPO')
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
                    'del 27/10/2026', LINEA))
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
# Erano sette: il nome della linea (45) e quello del settore (52) sono chiusi il
# 27/10/2026 dalle decisioni D3 e D4 dell'utente. La 70 (placchette) e' diventata
# PRIORITARIO nella seconda verifica del 27/10: il rischio e' arrivare
# all'ancoraggio senza placchette.
S.append(P('<b>Le sei voci segnate PRIORITARIO</b> sono le più gravi: la portata delle '
           'brache, la fotografia dell\'ancoraggio, le placchette (sul posto o da portare), '
           'la lunghezza della campata, il nastro e il suo backup. Se il tempo con i ragazzi '
           'è poco, si parte da lì.', body))
S.append(SP(14))
S.append(data_table(
    ['Sezione', 'Voci', 'Che tipo di risposta serve'],
    [['1 · Quadro generale', '1-2, 4-7', 'Misure e dati della linea e della giornata'],
     ['2 · Materiale', '8-24', 'Lunghezze, diametri, modelli, quantità'],
     ['3 · Manovre', '25-36', 'Nomi di nodi, sequenze, esecuzione'],
     ['4 · Ancoraggio', '37-41, 50, 51, 54, 70', 'Verifiche a immagine e scatti da fare'],
     ['5 · Fonti', '42-44, 46, 49, 57-58', 'Locandina, foto, buchi di ripresa'],
     ['6 · Linee fotografate', '59-69, 71-74', 'Foto e schede del file del gruppo']],
    [118, 78, FW - 196], color=LINEA))
S.append(PageBreak())

# ================================================================ 1 · quadro
sezione('1', 'Quadro generale della linea', 'Sezione 1 · dati di testata', LINEA,
        'Dati che vanno nella testata del manuale e nella planimetria. Nessuno di questi '
        'viene pronunciato nei video: vanno misurati o ricordati.',
        # La 56 (quale lato e' quale) e' chiusa il 27/10/2026: tensione sopra Cocoa.
        [(1, 'Lunghezza effettiva della campata. Il catalogo i-pietra e la locandina danno '
             '53 m, SlackMap 52,84 m del segmento disegnato sulla mappa, i due GPS del '
             'telefono 51,4 m: '
             'nessuno è una misura. Quanto misura davvero da placchetta a placchetta?',
          'mai pronunciata · nota N2 del manuale', 2, True),
         (2, 'Dislivello fra i due lati — l\'offlevel. Quanto, e da che parte pende? '
             'Influenza il tensionamento.', 'mai pronunciato'),
         (4,'Accesso e avvicinamento: da dove si parte, quanto si cammina, dove si '
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
         (13, 'Cos\'è il «<b>Mighty Lock</b>», descritto come «quello quadratino»? Nella '
              'lista della cernita del gruppo c\'è un <b>anello quadrato MightyLock</b> '
              '(Balance Community): era quello? E come lavorava nel backup?',
          '[IMG_1351 @ 0:19-0:28] · lista della cernita del gruppo'),
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
              'scorrevole; in IMG_1369 sulla parete le placchette sono almeno tre. Più in '
              'basso c\'è un altro punto: con placchetta il 16/05, senza il 22/08 — è lo '
              'stesso? Manca l\'inquadratura d\'insieme.',
          'IMG_1371.JPEG · IMG_1369 @ 0:05-0:45 · IMG_3331', 3),
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
        [(37, '<b>Portata (WLL) delle brache.</b> Alla sosta main ci sono due tinte, lilla '
              'chiaro e viola scuro; la lilla porta una linguetta blu e un\'etichetta '
              'bianca, illeggibili in tutte le foto. Le etichette viola fotografate per il '
              'catalogo non sono legate a nessun pezzo usato il 16/05. <b>Di chi erano le '
              'viola della sosta main? Erano pezzi del catalogo, e quali?</b> Poi va letta '
              'l\'etichetta sul pezzo.',
          'IMG_1357 · IMG_1359 · catalogo · il danno peggiore possibile se sbagliata',
          2, True),
         (38, 'Nell\'ancoraggio c\'è <b>protezione veloce</b> — un friend — accanto ai punti '
              'fissi? L\'oggetto mosso di IMG_1374 @ 0:33 somiglia alla carrucola '
              'bloccante, e in nessuna immagine si vede una camma: questo non prova che un '
              'friend non ci fosse. <b>Scatto da fare sul campo.</b>',
          'IMG_1374 @ 0:33 · nota N1 del manuale', 2, True),
         (39, 'I <b>punti</b> sono placchetta metallica su bullone con dado esagonale — '
              'confermato a immagine. <b>Tassello meccanico o barra resinata?</b> Su '
              'SlackMap la Brifing ha barre resinate. Su una placchetta si legge «FOR 1 '
              'PERSON», logo e codice incerti. Restano <b>marca e diametro del bullone</b>, '
              'e <b>chi li ha posati</b>.', 'IMG_1371.JPEG · IMG_1372.JPEG · IMG_3324'),
         (70, '<b>Placchette: in loco o da portare?</b> Il file del gruppo, nella scheda '
              '«Sosta Bisma Standard», mette in loco «Spit e Dadi» e da portare «3 '
              'piastrine da 10 mm»; la scheda della 53 m elenca 3 placchette su bullone '
              'all\'ancoraggio statico, e il 22/08 più in basso c\'era un bullone senza '
              'placchetta. Le «piastrine» del file sono le placchette? Restano sul posto o '
              'vanno portate a ogni montaggio?',
          'file LineeBisma, «Sosta Bisma Standard» · IMG_3331 · cfr. voci 28 e 72', 2,
          True),
         (40, '<b>Marca</b> della carrucola bloccante nera con puleggia arancio. Le marcature '
              'lette sono CE 0082, UK CA 20, EN 567:2013, Ø 7,8-11 mm; il logo non è '
              'leggibile.', 'IMG_1371.JPEG · dettaglio in lavorazione/dettagli/'),
         (41, 'La <b>corda verde acqua</b> è la linea vita o il cordino di collegamento fra '
              'i punti? In IMG_1371 si vede annodata fra i punti dell\'ancoraggio. Le due '
              'funzioni potrebbero coesistere.', 'IMG_1371.JPEG · [IMG_1350 @ 0:33]', 3),
         (50, '<b>A-frame</b>: quanto sono <b>alti</b> i pali, che legno e che diametro, '
              'come sono legati in testa, e di quanto sollevano la linea sopra il bordo? '
              'Al piede dei pali c\'è <b>filo metallico</b> — due o tre giri a quello di '
              'sinistra, almeno uno a quello di destra — con fili da un palo all\'altro: '
              'legano i piedi o sono un recinto che c\'era già?',
          'IMG_1396 · IMG_1416', 4),
         (54, 'Sullo sfondo di IMG_1416 e IMG_1396 corre una <b>linea tesa con sotto una '
              'seconda linea appesa a festoni</b>: non è la 53 m, che nelle stesse foto si '
              'vede a parte. <b>Quale linea è?</b> E quella a festoni '
              'che cos\'è — backup, tagline lasciata in posa, altro?',
          'IMG_1416 · IMG_1396 · voci 54-55', 4),
         (51, 'Il nastro appare <b>bianco o crema</b> in IMG_1401, con un secondo nastro '
              'chiaro parallelo. Se confermato chiude le voci 22 e 23.',
          'foto/IMG_1401.JPG')])

# ================================================================ 5 · nome e fonti
# 45 (titolo) e 52 (settore) chiuse il 27/10/2026 dalle decisioni D3 e D4
# dell'utente: GAS-OH nel titolo, «Anfite-altro» come la locandina.
sezione('5', 'Fonti e buchi di ripresa', 'Sezione 5 · apparato', C_ASL,
        'Che cosa dicono le fonti esterne, da dove vengono le immagini, dove le riprese '
        'si interrompono.',
        [(42, 'Dati presi da i-pietra da validare: settore <b>Anfiteatro</b>, roccia '
              '<b>arenaria</b>, colore linea <b>#F97316</b>. Se il manuale li stampa devono '
              'essere corretti anche fuori dall\'app.', 'catalogo i-pietra'),
         (43, 'La <b>locandina</b> «La Pietra — Yeah Vez!» è stata letta, ma il file '
              'disponibile è uno screenshot 1600×720 con bande nere: non è stampabile in '
              'A4. Serve il file sorgente.', 'fonti/locandina_la_pietra.jpeg'),
         (44, '<b>Anno</b> del Bismantova Highline Meeting riportato sul logo della '
              'locandina. Il logo è poco leggibile.', 'locandina'),
         (46, 'Cos\'è la «<b>Bifida</b>»? Non compare sulla locandina.',
          '[IMG_1373 @ 0:24]'),
         (57, 'Le foto del <b>22/08</b> sulla cresta (IMG_3308-3322): quali sono della '
              '<b>Despedida</b> e quali del <b>Settore Giallo</b>? La roccia sullo sfondo '
              'di IMG_3311 è davvero quella della Despedida 165 m?',
          'IMG_3308-3322 · chi ha accompagnato il sopralluogo', 3),
         (49, 'Fra le <b>15:38 e le 17:08</b> non esiste nessuna ripresa, ma alle 17:08 la '
              'linea è montata e camminata. Manca la documentazione del tensionamento '
              'finale e dei primi passaggi: cosa è successo in quell\'ora e mezza?',
          'metadati · il manuale deve dichiarare il buco', 3),
         (58, 'Il video <b>IMG_1376</b> sta fra le riprese della sosta sull\'altro lato, ma '
              'il GPS lo colloca <b>al main</b>, a circa 5 m (accuratezza 13 m). Che cosa '
              'si stava facendo lì?',
          'GPS dei video · fase D di NOTE_RIGGING', 2)])

# ================================================================ 6 · linee fotografate
# Voci 59-69 e 71-74 di DUBBI.md, riscritte il 27/10/2026 sulle copie raddrizzate e
# corrette nella seconda verifica dello stesso giorno (74 nuova).
# La 70 (placchette) sta nella sezione 4, con gli ancoraggi.
sezione('6', 'Le linee fotografate', 'Sezione 6 · il file del gruppo e le sue foto', C_FOT,
        'Voci aperte dalle fotografie e dalle schede del file LineeBisma del gruppo '
        '(20/10/2026). «Vicino» e «lontano» sono le colonne del file, non il lato tensione '
        'e il lato statico. Si chiedono a chi ha compilato il file e a chi era sul posto.',
        [(59, 'Di quale linea è la <b>sosta con il tronco</b>, 108 o 113? Il file mette '
              'foto diverse della stessa sosta su tutte e due le righe. Si vedono un tronco con la corteccia, '
              'coperto in parte da un\'imbottitura bianca, slinghe verdi che lo scavalcano, '
              'una placchetta con dado e, subito accanto, un albero: non escludono né «Bisma '
              'standard senza cavalletto + tronco» (113) né «alberi e uno spit» (108).',
          'anfiteatro-108_01-04 · anfiteatro-113_05-07', 3),
         (60, 'Il <b>lato di tensione</b> di ogni linea fotografata: 46, 97, 108, 113, '
              'Despedida 60 e 70; e se il «vicino» della 53 sia il main. Nessuna foto lo '
              'mostra. Indizi: sul lato lontano della 46 un elemento metallico con il nastro '
              'avvolto; su 46 e 53 due elementi in calza nera che convergono su un anello '
              'arancione; '
              'in 53_01 due pali di legno; cavalletti su più lati.',
          'tutte le cartelle delle foto', 4),
         (61, '<b>Data e autore</b> di ogni foto: Excel ha tolto gli EXIF. Il cavalletto '
              'della 113 compare in tre forme (due pali tondi d\'estate, tre pali d\'autunno, '
              'due assi squadrate di notte), quello della 46 in due (corda color canapa '
              'd\'autunno, forse con tre pali; fettuccia azzurra d\'estate, con due).',
          '113_01-04, 113_08 · 46_01, 46_05', 3),
         (62, 'La «<b>91</b>» del file è la 97 m del registro? Le sue righe sono state messe '
              'sulla 97 per posizione.', 'LineeBisma, scheda «Elenco»'),
         (63, 'Dove sono gli «<b>alberi e uno spit</b>» del lato lontano della 108? Le foto '
              'della sua riga mostrano la sosta con il tronco con un albero accanto, ma né '
              'lo spit né una braca legata all\'albero. La calza grigia e rossa che va verso '
              'l\'interno è la «sosta molto lunga»?',
          'anfiteatro-108 · cfr. voce 59', 3),
         (64, 'Che cosa sono i <b>due elementi in calza nera</b> che convergono su un '
              'anello arancione (46_01, 53_01), e che cos\'è l\'anello? Di nero si vede solo '
              'la calza; ne escono anelli lilla e giallo-verde. Fettucce, bungee (come quelli '
              'della 53 m del 22/08), altro? L\'etichetta «SPIDER» sta sulla protezione '
              'infilata su uno dei due, non su ciò che è dentro la calza. '
              'Stesso materiale, stessa stagione, stesso parcheggio sotto, e in 53_01 due '
              'pali come il cavalletto della 46: è la stessa giornata, o la stessa sosta '
              'messa su due righe?',
          '46_01 · 46_02 · 53_01', 3),
         (65, 'Sul lato lontano della 46, l\'<b>elemento metallico</b> con il nastro '
              'bianco avvolto, da cui parte un elemento in calza nera, è un weblock? E i '
              'due elementi verticali dietro le brache (uno di legno) sono un cavalletto? Il file '
              'chiama quel lato «senza cavalletto».',
          '46_03 · 46_04 · decide la voce 60 per la 46'),
         (66, 'Despedida 70: <b>un cavalletto a tutti e due i capi?</b> Due pali sul lato '
              'vicino (estate), tre sul lontano (autunno). Sul lontano, a che cosa è '
              'ancorata la corda chiara doppia (70_03)? La protezione bianca attorno al masso '
              '(70_04) è chiusa sul masso, sull\'alberello o su tutti e due?',
          'despedida-70_01-04', 3),
         (67, 'Despedida 60, lato lontano: che funzione ha la <b>fettuccia Gibbon</b> (una '
              'sola o più?), che gira attorno alla base di un albero e passa accanto a tre '
              'moschettoni sul bordo, '
              'e la corda arancione annodata all\'albero? I bastoni incrociati accanto al '
              'tronco sottile sono un cavalletto? Del lato vicino non c\'è nessuna foto; '
              'l\'highliner di 60_01 è sulla 60 o sulla 70?',
          'despedida-60_01-06 · despedida-70_02', 3),
         (68, 'Le <b>etichette</b> alla sosta con il tronco: sulla calza di una slinga verde '
              'una scritta che sembra «2 t», non leggibile con certezza; sulla braca viola '
              'un\'etichetta azzurra illeggibile. <b>Foto da fare sul campo</b>, con le '
              'etichette distese.',
          '113_05 · 113_06 · come la voce 37'),
         (69, 'Quale linea della foto del lato vicino della 97 è la 97? Per il ritaglio del '
              'file è la <b>terza linea</b>, quella che parte dall\'ancoraggio in basso a '
              'destra, non una delle due con gli highliner. E il lato lontano è sugli alberi, '
              'sulla roccia (un moschettone su un elemento metallico, forse una placchetta) '
              'o su tutti e due?',
          'anfiteatro-97_03 · ritaglio del file · 97_01', 3),
         (71, 'Gli <b>omega</b> sono elencati due volte, in «Materiale da portare» e in '
              '«Sosta Main»: sono gli stessi pezzi o pezzi in più?',
          'LineeBisma, «Sosta Bisma Standard», B9-B10 e B14-B15'),
         (72, 'Le <b>parole del file</b>: a quali pezzi corrispondono «spit», «piastrine», '
              '«delta», «omega», «slinga», «sliding x» e «BFK»? E «Bisma standard senza '
              'cavalletto» è la stessa sosta senza il blocco «Cavalletto»? Lo schema «Bisma '
              'standard» delle righe è la scheda «Sosta Bisma Standard»?',
          'LineeBisma, «Sosta Bisma Standard» ed «Elenco»', 3),
         (73, 'Che cosa misura «<b>Schetchy</b>» (colonne «Schetchy» e «Schetchy2», valori '
              '«No» e da 2 a 5)? Che scala è, e in che verso? E le due colonne valgono per il '
              '«vicino» e il «lontano», come dice la loro posizione?',
          'LineeBisma, scheda «Elenco», D3 e G3'),
         (74, 'Anfiteatro 113, lato vicino: sotto la linea c\'è una <b>seconda '
              'linea appesa a festoni</b> (113_01, 113_03, 113_08): è il backup della linea?',
          '113_01 · 113_03 · 113_08 · cfr. voce 55')])

# ================================================================ chiusura
sec(LINEA, 'Dopo la compilazione')
S.append(LineHeader('', 'Riportare le risposte', 'Chiusura', LINEA))
S.append(SP(12))
S.append(P('Le risposte raccolte vanno riportate in <b>DUBBI.md</b>, sulla riga del numero '
           'corrispondente, indicando la data e chi ha risposto — come è già stato fatto per '
           'i tre bloccanti chiusi il 19/08/2026. Solo dopo si rigenera il manuale.', body))
S.append(SP(14))
S.append(callout('Le fotografie che mancano',
                 'Tre voci non si chiudono a parole: l\'etichetta di una braca (voce 37), '
                 'l\'insieme dei tre punti dell\'ancoraggio, con il dispositivo di '
                 'protezione veloce se c\'è (voce 38), e le etichette alla sosta con il '
                 'tronco (voce 68). Sono scatti. I primi due vale la pena farli nella stessa '
                 'uscita in cui si rimisura la campata della 53 m.', C_ANC))
S.append(SP(20))
S.append(two_cols(campo('Compilata il', COL), campo('Compilata da', COL)))
S.append(SP(16))
S.append(campo('Hanno risposto', FW))
S.append(SP(16))
S.append(campo('Note libere', FW))
S.append(Righe(5))
S.append(SP(14))
S.append(P('Scheda generata da build/build_scheda_dubbi.py sulle voci aperte di DUBBI.md. '
           'Le voci già chiuse — B1, B2, B3, 3, 45, 47, 48, 52, 53, 56, M2 — non compaiono; '
           'la 55 è dentro la 54.', small))

# ---------------------------------------------------------------- build
OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM,
                      title='Bismantova · Scheda di verifica sul campo',
                      author='Dubbi aperti del manuale di rigging')
frame = Frame(LM, BM, FW, H - TM - BM, id='n',
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPageEnd=page_end)])
doc.build(S)
print('scritto %s' % OUT)
