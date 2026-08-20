# -*- coding: utf-8 -*-
"""Manuale di rigging — highline «la 50», settore Anfiteatro, Pietra di Bismantova.

Costruito con il sistema grafico di design/design.py, come il progetto Sillschlucht.

Regola di questo documento: **niente dati dedotti**. Ogni numero viene dalla
trascrizione audio, da cio' che si vede nei fotogrammi, dal catalogo i-pietra o
da una risposta esplicita dell'utente. Tutto il resto e' marcato [DA CONFERMARE]
e raccolto in DUBBI.md.

    python build/build_manuale.py
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from schede_linee import (parte_linee, tabella_aree,                # noqa: E402
                          nota_copertura)
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,   # noqa: E402
                                PageBreak, NextPageTemplate, Table,
                                TableStyle, Paragraph, Spacer)
from reportlab.lib.enums import TA_CENTER                           # noqa: E402
from reportlab.pdfbase.pdfmetrics import stringWidth                # noqa: E402
from PIL import Image as _PILImage                                  # noqa: E402

OUT = RADICE / 'output' / 'Bismantova_Anfiteatro_Rigging.pdf'
ANN = RADICE / 'lavorazione' / 'frame_annotati'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'

# ---------------------------------------------------------------- colori
LINEA = HexColor(0xF97316)      # colore che i-pietra assegna a questa linea
C_ANC = LC[1]                   # fase D — ancoraggio      (rosso)
C_SOS = LC[7]                   # fase B — sosta / slinga   (azzurro)
C_TEN = LC[3]                   # fase F — lato tensione    (ambra)
C_ASL = LC[5]                   # fase G — anti-slip        (verde)

DC = '<font color="#B3261E">[DA CONFERMARE]</font>'


def spaziato(cv, x, y, testo, font, corpo, sp=1.9):
    """Testo con spaziatura fra i caratteri, direttamente sul canvas.

    `track()` di design.py serve ai Paragraph: produce entita' &nbsp; che dentro
    un drawString finirebbero stampate alla lettera. Qui la spaziatura si fa
    posizionando un carattere alla volta.
    """
    cv.setFont(font, corpo)
    for ch in testo:
        cv.drawString(x, y, ch)
        x += stringWidth(ch, font, corpo) + (sp * 2.4 if ch == ' ' else sp)
    return x


def dim(p):
    """Dimensioni reali dell'immagine: PhotoStrip ne ha bisogno per il ritaglio."""
    with _PILImage.open(p) as im:
        return im.size


def foto(nome, w, cap, color=None, ratio=None, focus=0.5):
    p = FOTO / nome if (FOTO / nome).exists() else ANN / nome
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


# ---------------------------------------------------------------- copertina
def cover(cv, doc):
    p = FOTO / 'IMG_1396.jpg'
    ow, oh = dim(p)
    sh = H
    sw = sh * ow / oh
    cv.saveState()
    cv.drawImage(str(p), (W - sw) / 2, 0, sw, sh, preserveAspectRatio=False, mask=None)
    cv.setFillColor(HexColor(0x14181C))
    cv.setFillAlpha(0.42)
    cv.rect(0, 0, W, H, stroke=0, fill=1)
    cv.setFillAlpha(1)
    cv.restoreState()

    cv.setFillColor(LINEA)
    cv.rect(LM, H - 176, 54, 4, stroke=0, fill=1)
    cv.setFillColor(WHITE)
    spaziato(cv, LM, H - 200, 'PIETRA DI BISMANTOVA · ANFITEATRO', 'Pop-M', 8.6)
    cv.setFont('Pop-B', 40)
    cv.drawString(LM, H - 250, 'Manuale di rigging')
    cv.setFont('Pop-L', 27)
    cv.drawString(LM, H - 288, 'highline «la 50»')

    cv.setFont('Lora', 10.4)
    cv.setFillColor(HexColor(0xE8E5E0))
    for i, r in enumerate([
            'Sequenza di montaggio, ancoraggi e manovre,',
            'documentati passo per passo dalle riprese del 16 maggio 2026.']):
        cv.drawString(LM, H - 326 - i * 15, r)

    cv.setFillColor(WHITE)
    spaziato(cv, LM, 92, 'EDIZIONE DI LAVORO', 'Pop-M', 7.6)
    cv.setFont('Lora', 8.6)
    cv.setFillColor(HexColor(0xD8D4CE))
    cv.drawString(LM, 74, 'Le misure non pronunciate nelle riprese sono marcate [DA CONFERMARE]')
    cv.drawString(LM, 60, 'e vanno completate con chi ha montato la linea.')


def page_begin(cv, doc):
    cv._accent = LINEA
    cv._sect = ''


def page_end(cv, doc):
    n = cv.getPageNumber()
    acc = getattr(cv, '_accent', LINEA)
    sect = getattr(cv, '_sect', '')
    cv.setFont('Pop-M', 7)
    cv.setFillColor(MUT)
    cv.drawString(LM, H - 44, 'BISMANTOVA · ANFITEATRO · MANUALE DI RIGGING')
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


# ================================================================ copertina
S.append(Spacer(1, 1))
S.append(NextPageTemplate('main'))
S.append(PageBreak())

# ================================================================ le due soste
sec(C_SOS, 'Le due soste')
S.append(LineHeader('1', 'Sosta main e sosta backup', 'Fase A · 13:00', C_SOS))
S.append(SP(10))
S.append(P('Il montaggio si apre allestendo <b>due soste indipendenti</b> sullo stesso lato, '
           'distinte a colpo d’occhio dal materiale: «sosta main, quella con le slinghe '
           'viola; sosta backup, quella con le corde rosa». Il codice colore non è '
           'decorativo — serve a non confondere i due sistemi mentre si lavora in parete.',
           lead))
S.append(SP(10))
S.append(ChipRow([('Sosta main', 'Slinghe viola'), ('Sosta backup', 'Corde rosa'),
                  ('Connettore', 'BFK'), ('Maglie', '4 delta')], C_SOS))
S.append(SP(12))
S.append(photo_pair(
    str(FOTO / 'IMG_1357.jpg'), str(FOTO / 'IMG_1359.jpg'),
    'Slinghe e corde stese prima del montaggio · 13:07',
    'Il materiale disposto sulla roccia · 13:07',
    *dim(FOTO / 'IMG_1357.jpg'), color=C_SOS, ratio=1.02, focus=0.5,
    ow2=dim(FOTO / 'IMG_1359.jpg')[0], oh2=dim(FOTO / 'IMG_1359.jpg')[1]))
S.append(SP(14))
S.append(P('<b>Come procede</b>', h3))
S.append(SP(5))
S.append(BU('Le due soste vengono allestite <b>in parallelo</b>, non una dopo l’altra: '
            'mentre una persona lavora sul lato principale, un’altra raggiunge il lato '
            'opposto per costruire la sosta di là.', C_SOS))
S.append(BU('La corda del backup viene collegata con un <b>BFK</b>, il moschettone '
            'd’acciaio grande.', C_SOS))
S.append(BU('Servono <b>quattro maglie rapide delta</b> — l’unica quantità dichiarata a '
            'voce durante tutto il montaggio.', C_SOS))
S.append(BU('Una <b>corda azzurra</b> ha doppia funzione: prima porta la tagline da un lato '
            'all’altro, poi diventa linea vita sulla sosta opposta.', C_SOS))
S.append(SP(10))
S.append(P('Lunghezze e diametri di slinghe e corde non vengono pronunciati: sono ' + DC +
           ' e vanno raccolti dal gruppo.', small))
S.append(PageBreak())

# ================================================================ p3 — lo spot
sec(LINEA, 'Lo spot')
S.append(LineHeader('', 'La Pietra di Bismantova', 'Castelnovo ne’ Monti, Reggio Emilia', LINEA))
S.append(SP(10))
S.append(P('La linea documentata qui appartiene al settore <b>Anfiteatro</b>. Sul posto la '
           'chiamano <b>«la 50»</b>, ed è il nome che questo manuale adotta. La lunghezza '
           'reale della campata non è però confermata: il catalogo i-pietra e la locandina '
           'delle linee registrano all’Anfiteatro una linea da 53 m, ma la misura va '
           'rifatta sui punti. ' + DC, lead))
S.append(SP(10))
S.append(callout('Attenzione al nome',
                 'Alla Pietra esiste <b>un’altra linea da 50 m, al Settore Giallo</b>. '
                 '«La 50» da sola è quindi ambigua: in questo manuale la linea va sempre '
                 'chiamata «la 50, settore Anfiteatro». Verificare il settore prima di '
                 'attrezzare qualsiasi cosa.', WARN, '!', FW, True))
S.append(SP(12))
S.append(P('<b>Le highline censite alla Pietra</b>', h3))
S.append(SP(5))
# tabella e nota vengono dal registro dati/linee.py: erano scritte a mano qui
# accanto agli stessi dati, e le due copie sono andate in conflitto appena il
# catalogo i-pietra e' cambiato.
S.append(tabella_aree())
S.append(SP(6))
S.append(P(nota_copertura(), small))
S.append(SP(12))
S.append(data_table(
    ['Voce', 'Valore', 'Fonte'],
    [['Settore', 'Anfiteatro', 'i-pietra · locandina'],
     ['Roccia', 'Arenaria', 'i-pietra'],
     ['Lunghezza', '[DA CONFERMARE] — 53 m nei cataloghi, da rimisurare', 'i-pietra'],
     ['Dislivello / offlevel', '[DA CONFERMARE]', '—'],
     ['Coordinate ancoraggi', '[DA CONFERMARE]', '—'],
     ['Avvicinamento', '[DA CONFERMARE]', '—'],
     ['Autorizzazioni, divieti', '[DA CONFERMARE]', '—'],
     ['Data del montaggio', '16 maggio 2026', 'metadati dei file'],
     ['Persone coinvolte', 'almeno 4', 'video · utente']],
    [128, 268, 95], LINEA))
S.append(PageBreak())

# ================================================================ p4 — cronologia
sec(LINEA, 'La giornata')
S.append(LineHeader('', 'Come si è svolto il montaggio', 'Cronologia dai metadati', LINEA))
S.append(SP(10))
S.append(P('I file portano l’ora di ripresa, e questo permette di ricostruire la sequenza '
           'reale senza doverla dedurre dal racconto. Il montaggio comincia alle 13:00 e la '
           'linea viene camminata alle 17:08.', lead))
S.append(SP(12))
S.append(Steps([
    ('13:00 — Le due soste', 'Sosta main con slinghe viola, backup con corde rosa'),
    ('13:13 — Costruzione', 'Instradamento della slinga nell’anello d’acciaio'),
    ('13:32 — Orientamento', 'Verso di lavoro delle slinghe, ingrillaggio'),
    ('13:41 — Ancoraggio', 'Sosta su tre punti sul lato opposto'),
    ('13:55 — Tensionamento', 'Paranchino di base, pretensionamento'),
    ('14:09 — Blocco backup', 'Collegamento che prende sosta main e backup'),
    ('14:49 — Anti-slip', 'Nodo che impedisce lo slittamento nel weblock'),
    ('17:08 — Linea camminata', 'Primi passaggi documentati dalle fotografie'),
], LINEA, FW, 2))
S.append(SP(14))
S.append(callout('Un buco di un’ora e mezza',
                 'Fra le 15:38 e le 17:08 non esiste alcuna ripresa. Il tensionamento finale '
                 'e i primi passaggi non sono documentati: quella parte della sequenza non '
                 'compare in questo manuale perché nessuno l’ha filmata.', LINEA))
S.append(SP(10))
S.append(P('Nel complesso i video coprono <b>ventidue minuti e mezzo</b> su un arco di oltre '
           'quattro ore. Sono campioni sparsi, non una ripresa continua: buona parte delle '
           'operazioni non è stata filmata, e il manuale documenta ciò che si vede.', body))
S.append(PageBreak())

# ================================================================ p5 — ancoraggio
sec(C_ANC, 'Ancoraggio')
S.append(LineHeader('1', 'L’ancoraggio su roccia', 'Fase D · 13:41', C_ANC))
S.append(SP(10))
S.append(P('Gli ancoraggi sono <b>tutti su roccia</b>. Sul lato documentato la sosta è '
           'costruita su <b>tre punti</b> — «i punti quali sono? Uno, due e tre» — collegati '
           'fra loro. Il numero e il tipo dei punti sul lato opposto non sono documentati.',
           lead))
S.append(SP(10))
S.append(ChipRow([('Punti', '3'), ('Tipo', 'Placchetta su bullone'),
                  ('Collegamento', 'Corda annodata'), ('Angolo', '[DA CONF.]')], C_ANC))
S.append(SP(12))
S.append(foto('D1_ancoraggio.jpg', FW, 'Sosta su roccia — placchetta, cordino di '
              'collegamento, carrucola bloccante e slinga viola  ·  IMG_1371, 13:41',
              C_ANC, ratio=1.02, focus=0.78))
S.append(PageBreak())

sec(C_ANC, 'Ancoraggio')
S.append(LineHeader('', 'Che cosa si vede e che cosa manca', 'Fase D · inventario', C_ANC))
S.append(SP(12))
S.append(two_cols(
    gear_block('Ciò che si vede', [
        'Placchetta metallica su bullone con dado esagonale',
        'Connettore d’acciaio a ghiera',
        'Maglia rapida in acciaio',
        'Corda verde acqua annodata fra i punti',
        'Slinga viola (braca ad anello industriale)',
        'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm',
    ], C_ANC),
    gear_block('Ciò che manca', [
        'Diametro e marca del bullone — [DA CONFERMARE]',
        'Angolo di apertura fra i punti — [DA CONFERMARE]',
        'Numero dei punti sul lato opposto — [DA CONFERMARE]',
        'Portata delle slinghe — [DA CONFERMARE]',
        'Marca della carrucola bloccante — [DA CONFERMARE]',
        'Presenza o meno di protezione veloce — [DA CONFERMARE]',
    ], WARN)))
S.append(SP(12))
S.append(callout('Fotografia da fare sul campo',
                 'Nessuna immagine disponibile inquadra i tre punti insieme, e l’angolo di '
                 'apertura non è quindi verificabile. <b>Questa scheda resta incompleta fino '
                 'a quando non verrà scattata una fotografia d’insieme dell’ancoraggio.</b>',
                 WARN, '!', FW, True))
S.append(PageBreak())

# ================================================================ p6 — dettaglio punto
sec(C_ANC, 'Ancoraggio')
S.append(LineHeader('2', 'Il singolo punto', 'Fase D · dettaglio', C_ANC))
S.append(SP(10))
S.append(P('Il punto è una <b>placchetta metallica fissata con un dado esagonale su '
           'bullone</b>. Si tratta quindi di un tassello meccanico: non di uno spit a vite, '
           'e non di un resinato con occhiello integrato. Misura, marca e anno di posa non '
           'sono ricavabili dalle immagini.', lead))
S.append(SP(12))
S.append(foto('D2_placchetta_dettaglio.jpg', FW,
              'Placchetta e dado esagonale  ·  ingrandimento da IMG_1372, 13:41', C_ANC))
S.append(SP(14))
S.append(callout('Perché la distinzione conta',
                 'Spit, tasselli a espansione e resinati hanno comportamenti, durate e '
                 'controlli diversi. Quello che si vede in fotografia è un dado su bullone: '
                 'è quanto basta per escludere lo spit a vite e il resinato con occhiello, '
                 'non per stabilire quale tassello sia. Verificare sul posto.', C_ANC))
S.append(SP(12))
S.append(P('<b>Controlli da fare prima di caricare</b>', h3))
S.append(SP(5))
S.append(BU('Che il dado sia serrato e non presenti gioco.', C_ANC))
S.append(BU('Che la placchetta non ruoti sul bullone.', C_ANC))
S.append(BU('Che la roccia attorno al foro non presenti fratture o sfaldature: '
            'l’arenaria è meno tenace del calcare.', C_ANC))
S.append(BU('Che non vi sia corrosione visibile su placchetta, dado o bullone.', C_ANC))
S.append(SP(10))
S.append(P('Questo elenco discende dal tipo di ancoraggio osservato, non da una procedura '
           'dettata nei video: nessuno, nelle riprese, enuncia una lista di controlli. '
           'La checklist realmente usata dal gruppo è ' + DC + '.', small))
S.append(PageBreak())

# ================================================================ p7 — la sosta
sec(C_SOS, 'Sosta')
S.append(LineHeader('3', 'Instradamento della slinga', 'Fase B · 13:13', C_SOS))
S.append(SP(10))
S.append(P('È il passaggio che l’audio rende del tutto incomprensibile. La descrizione '
           'pronunciata a voce è: «qua, che gira qua dentro, questa qua sotto, fa il giro '
           'qui, che fa il giro qui dietro, pista, pif, paf, sotto, torna sotto». Precisa '
           'per chi guarda le mani, inutilizzabile per chi legge. La sequenza qui sotto '
           'ricostruisce la manovra dai fotogrammi.', lead))
S.append(SP(12))
S.append(photo_row([
    (str(ANN / 'B1_slinga_aperta.jpg'),) + dim(ANN / 'B1_slinga_aperta.jpg') + ('1 · slinga aperta',),
    (str(ANN / 'B2_passaggio_anello.jpg'),) + dim(ANN / 'B2_passaggio_anello.jpg') + ('2 · nell’anello',),
    (str(ANN / 'B3_giro_chiuso.jpg'),) + dim(ANN / 'B3_giro_chiuso.jpg') + ('3 · giro chiuso',),
], C_SOS))
S.append(SP(14))
S.append(callout('Il nodo non ha un nome, qui',
                 'Nei video nessuno lo chiama. I fotogrammi mostrano <b>che cosa</b> viene '
                 'fatto, non <b>come si chiama</b> né quale alternativa sia accettabile. '
                 'Il nome del nodo è ' + DC + ' e va chiesto a chi lo ha eseguito.',
                 C_SOS))
S.append(SP(12))
S.append(P('<b>L’unica motivazione tecnica spiegata a voce in tutto il girato</b>', h3))
S.append(SP(5))
S.append(P('«Perché armi questo nodo qua? — Per forzare la slinga. Ci sono anche altre '
           'maniere per farlo, a me piace quella lì perché tanto la tenuta è sufficiente, '
           'ed è veloce anche da regolare.»', lead))
S.append(SP(4))
S.append(P('Trascrizione da IMG_1367, minuto 0:43. In ventidue minuti di parlato è '
           'l’unico momento in cui qualcuno spiega <i>perché</i> sceglie una soluzione '
           'invece di un’altra.', small))
S.append(PageBreak())

# ================================================================ p8 — tensione e anti-slip
sec(C_TEN, 'Tensione')
S.append(LineHeader('4', 'Lato tensione e anti-slip', 'Fasi F e G · 14:09 e 14:49', C_TEN))
S.append(SP(10))
S.append(P('Sul lato di tensione la linea passa nel <b>weblock</b>, che il gruppo chiama '
           '«banana». A tensionamento concluso viene aggiunto l’<b>anti-slip</b>, un nodo '
           'sulla linea la cui funzione è l’unica del corpus a essere insieme spiegata a '
           'voce e mostrata.', lead))
S.append(SP(12))
S.append(photo_pair(
    str(ANN / 'F1_weblock_grillo.jpg'), str(ANN / 'G1_antislip.jpg'),
    'Weblock e grillo a lira  ·  IMG_1384, 14:09',
    'Anti-slip  ·  IMG_1395, 14:49',
    *dim(ANN / 'F1_weblock_grillo.jpg'), color=C_TEN,
    ow2=dim(ANN / 'G1_antislip.jpg')[0], oh2=dim(ANN / 'G1_antislip.jpg')[1]))
S.append(SP(14))
S.append(callout('«Serve per evitare che la linea slitti nella banana»',
                 'IMG_1395, minuto 0:25. La <b>funzione</b> dell’anti-slip è quindi certa. '
                 'Il <b>nodo</b> con cui viene realizzato, il materiale impiegato e il punto '
                 'esatto in cui va posizionato restano ' + DC + '.', C_ASL))
S.append(SP(12))
S.append(two_cols(
    gear_block('Sequenza osservata', [
        '13:58 — pretensionamento provvisorio',
        '14:09 — blocco del backup',
        'Tensionamento definitivo — orario [DA CONFERMARE]',
        '14:49 — anti-slip, a tensione fatta',
    ], C_TEN),
    gear_block('Avvertenze pronunciate', [
        '«Andrebbe fatto dopo, quando c’è del peso» — IMG_1380',
        '«Ruotando… può cadere» — IMG_1370',
        'In entrambe manca l’oggetto — [DA CONFERMARE]',
    ], WARN)))
S.append(SP(10))
S.append(P('Le due avvertenze sono state pronunciate davvero, ma in entrambi i casi chi '
           'parla non nomina l’oggetto: si capisce che qualcosa va fatto dopo e che '
           'qualcosa può cadere, non che cosa. Sono riportate perciò come citazioni, '
           'non come istruzioni.', small))
S.append(PageBreak())

# ================================================================ p9 — materiale
sec(LINEA, 'Materiale')
S.append(LineHeader('5', 'Il materiale', 'Quello che si sente e quello che si vede', LINEA))
S.append(SP(10))
S.append(P('Elenco costruito incrociando i nomi pronunciati nei video con gli oggetti '
           'riconoscibili nelle immagini. La colonna delle misure è quasi interamente '
           'vuota, e resta tale.', lead))
S.append(SP(12))
S.append(data_table(
    ['Qtà', 'Articolo', 'Misura', 'Fonte'],
    [['n.d.', 'Slinghe viola — brache ad anello industriali', '[DA CONF.]', 'video · foto'],
     ['n.d.', 'Corde rosa, sosta backup', '[DA CONF.]', 'video · foto'],
     ['1', 'BFK, moschettone d’acciaio grande', '[DA CONF.]', 'audio'],
     ['1', 'Corda azzurra — tagline, poi linea vita', '[DA CONF.]', 'audio'],
     ['4', 'Maglie rapide delta', '[DA CONF.]', 'audio'],
     ['1', 'Slinga verde lunga, «la più grossa che c’è»', '[DA CONF.]', 'audio'],
     ['≥1', 'Slinga verde e nera', '[DA CONF.]', 'audio'],
     ['1', 'Weblock azzurro anodizzato, detto «banana»', '[DA CONF.]', 'foto'],
     ['≥1', 'Grillo a lira in acciaio', '[DA CONF.]', 'foto'],
     ['≥1', 'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm', 'marca [DA CONF.]', 'foto'],
     ['≥2', 'Grigri', '—', 'audio'],
     ['1', 'Softrelease', '[DA CONF.]', 'audio'],
     ['1', 'Paranchino di tensionamento della base', '[DA CONF.]', 'audio'],
     ['1', 'Corda verde acqua, collegamento fra i punti', '[DA CONF.]', 'foto'],
     ['n.d.', 'Nastro della highline', '[DA CONF.]', 'mai nominato'],
     ['n.d.', 'Backup della linea', '[DA CONF.]', 'mai nominato'],
     ['n.d.', 'Leash', '[DA CONF.]', 'mai nominato']],
    [40, 250, 108, 93], LINEA))
S.append(SP(10))
S.append(callout('Le ultime tre righe',
                 'Nastro, backup e leash sono gli elementi centrali di qualunque highline, '
                 'e <b>non vengono nominati in nessuno dei quarantadue video</b>. Non è una '
                 'dimenticanza di questo manuale: è un’assenza della fonte.', WARN, '!', FW, True))
S.append(PageBreak())

# ================================================================ la linea in opera
sec(LINEA, 'In opera')
S.append(LineHeader('6', 'La linea in opera', 'Ore 17:08', LINEA))
S.append(SP(10))
S.append(P('Il montaggio si chiude nel tardo pomeriggio. Le fotografie delle 17:08 sono la '
           'verifica che il sistema descritto in queste pagine ha retto: la campata è tesa '
           'fra i due ancoraggi e viene percorsa.', lead))
S.append(SP(12))
S.append(foto('IMG_1401.jpg', FW, 'La linea percorsa, con leash · IMG_1401, 17:08',
              LINEA, ratio=0.72, focus=0.5))
S.append(SP(14))
S.append(foto('IMG_1398.jpg', FW, 'La campata vista dal bordo · IMG_1398, 17:08',
              LINEA, ratio=0.62, focus=0.5))
S.append(PageBreak())

# ================================================================ le altre linee
# Catalogo delle ventiquattro linee e schede segnaposto per quelle non ancora
# documentate. Contenuto e impaginazione stanno in build/schede_linee.py, che
# legge il registro dati/linee.py.
S.extend(parte_linee())

# ================================================================ p11 — glossario e chiusura
sec(LINEA, 'Glossario')
S.append(LineHeader('9', 'Glossario', 'Il gergo del gruppo', LINEA))
S.append(SP(10))
S.append(P('I termini sono riportati come vengono pronunciati sul campo, con accanto il '
           'nome corrente. Dove il gergo è ambiguo, è segnalato.', lead))
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
     ['«slide next»', 'Termine non identificato: trascrizione incerta ' + '[DA CONF.]']],
    [150, 341], LINEA))
S.append(SP(16))
S.append(Rule(FW, 0.6, HAIR, 8))
S.append(SP(10))
S.append(P('<b>Avvertenza</b>', h3))
S.append(SP(4))
S.append(P('Highlining e slacklining comportano rischi. Questo manuale documenta un '
           'montaggio già realizzato da persone esperte: non sostituisce formazione, '
           'esperienza diretta e verifica autonoma di ogni ancoraggio prima di ogni '
           'utilizzo.', lead))
S.append(SP(10))
S.append(P('A ciò si aggiunge, per questa edizione, un limite specifico: il documento è '
           'stato ricostruito da riprese non didattiche e contiene numerosi dati non '
           'verificati, marcati [DA CONFERMARE]. Non deve essere usato come riferimento '
           'operativo finché quelle caselle non sono state riempite da chi ha eseguito il '
           'montaggio.', body))
S.append(SP(12))
S.append(P('Edizione di lavoro generata automaticamente da 42 video e 19 fotografie del '
           '16 maggio 2026. Sistema grafico ereditato dalla guida Sillschlucht.', small))

# ---------------------------------------------------------------- build
OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM,
                      title='Bismantova · Anfiteatro · Manuale di rigging',
                      author='Ricostruzione dai video del 16/05/2026')
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
