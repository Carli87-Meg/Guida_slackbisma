# -*- coding: utf-8 -*-
"""Capitolo della linea documentata: Anfiteatro, 53 m — «la 50».

E' il montaggio del 16 maggio 2026, l'unico di cui esistano riprese. Il contenuto
di queste pagine viene dal build del manuale, dove stava quando il documento
riguardava questa linea sola: le pagine funzionavano, e' cambiato dove stanno.

Cambia pero' come sono intitolate. Ogni testata dichiara adesso la linea e la
data, perche' in una guida che copre ventiquattro linee nulla di quanto si legge
qui deve poter essere scambiato per una procedura valida ovunque: e' cio' che ha
fatto un gruppo, su una linea, in un pomeriggio.

    from scheda_53 import parte_53
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import PageBreak, KeepTogether                            # noqa: E402
from PIL import Image as _PILImage                                  # noqa: E402

ANN = RADICE / 'lavorazione' / 'frame_annotati'
FOTO = RADICE / 'lavorazione' / 'foto_dritte'
DETT = RADICE / 'lavorazione' / 'dettagli'

LINEA = HexColor(0xF97316)
C_ANC = LC[1]                   # ancoraggio      (rosso)
C_SOS = LC[7]                   # sosta / slinga  (azzurro)
C_TEN = LC[3]                   # lato tensione   (ambra)
C_ASL = LC[5]                   # anti-slip       (verde)

DC = '<font color="#B3261E">[DA CONFERMARE]</font>'

# occhiello ripetuto su ogni testata: la linea e il giorno, sempre
GIORNO = '16/05/2026'


def _occh(fase):
    return 'Anfiteatro 53 m · %s · %s' % (fase, GIORNO)


def dim(p):
    with _PILImage.open(p) as im:
        return im.size


def foto(nome, w, cap, color=None, ratio=None, focus=0.5):
    # tre cartelle, un nome solo: foto raddrizzate, frame annotati, ritagli di
    # dettaglio. Cosi' chi scrive una pagina non deve sapere dove sta il file.
    p = next((c / nome for c in (FOTO, ANN, DETT) if (c / nome).exists()), FOTO / nome)
    ow, oh = dim(p)
    return PhotoStrip(str(p), w, ow, oh, cap, color, ratio, focus)


def _apre(testata, *seguito):
    """Testata di sottosezione legata a cio' che la segue.

    Il capitolo scorre invece di aprire una pagina per ogni fase: senza questo
    vincolo una testata potrebbe restare in fondo alla pagina con il suo testo
    di la'. Dove serve si lega anche il primo blocco visivo, cosi' una fase non
    si apre con l'ultimo centimetro di pagina disponibile.
    """
    dentro = [testata, SP(10)]
    for f in seguito:
        dentro.append(f)
    return KeepTogether(dentro)


def parte_53():
    S = []

    def sec(color, label):
        S.append(Accent(color, label))


    # ================================================================ p4 — cronologia
    sec(LINEA, 'La giornata')
    S.append(Segna('cap53'))
    S.append(LineHeader('', 'La giornata del 16 maggio', _occh('cronologia'), LINEA))
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
        ('17:08 — Linea camminata', 'Primi passaggi, documentati dalle fotografie fino alle 17:14'),
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
    S.append(SP(26))


    # ================================================================ le due soste
    sec(C_SOS, 'Le due soste')
    S.append(_apre(
        LineHeader('1', 'Sosta main e sosta backup', _occh('le due soste'), C_SOS),
        P('Il montaggio si apre allestendo <b>due soste indipendenti</b> sullo stesso lato, '
          'distinte a colpo d’occhio dal materiale: «sosta main, quella con le slinghe '
          'viola; sosta backup, quella con le corde rosa». Il codice colore non è '
          'decorativo — serve a non confondere i due sistemi mentre si lavora in parete.',
          lead)))
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
    S.append(foto('IMG_1360.jpg', FW,
                  'Slinghe viola, corde rosa, fettuccia verde, grilli e maglie rapide '
                  '· IMG_1360, 13:07', C_SOS, ratio=0.70, focus=0.42))
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
    S.append(SP(26))

    # ================================================================ etichette
    # La portata delle slinghe e' il dato piu' pericoloso da sbagliare di tutto
    # il documento: qui si dice che l'etichetta esiste e non si legge, e basta.
    sec(C_SOS, 'Le due soste')
    S.append(_apre(
        LineHeader('', 'La portata delle slinghe', _occh('le due soste · etichette'), C_SOS),
        P('Le slinghe della sosta main sono <b>brache ad anello industriali</b>: calza cucita '
          'per il lungo ed etichetta in tessuto. Nelle fotografie delle 13:07 l’etichetta '
          '<b>c’è</b> — bianca, cucita con filo blu sulla cucitura della calza — ma è '
          'rivoltata, e in nessuna inquadratura si legge. <b>La portata resta sconosciuta.</b>',
          lead)))
    S.append(SP(12))
    S.append(foto('IMG_1360_etichetta.jpg', FW,
                  'L’etichetta cucita sulla calza, rivoltata · dettaglio da IMG_1360, 13:07',
                  C_SOS, ratio=0.66, focus=0.5))
    S.append(SP(14))
    S.append(callout('Il colore non è una marcatura',
                     'Una calza viola con una riga scura assomiglia a una portata dichiarata, e '
                     'la tentazione di scriverla è forte. Non viene scritta. Il colore sbiadisce '
                     'al sole, le codifiche non sono le stesse per tutti i costruttori, e una '
                     'riga cucita non è una riga di portata. <b>L’unico dato che vale è quello '
                     'stampato sull’etichetta</b>, e per averlo serve una fotografia ravvicinata '
                     'dell’etichetta distesa. Finché non c’è, questa scheda non dichiara quanto '
                     'tengono le slinghe su cui sta appesa la linea.', WARN, '!', FW, True))
    S.append(SP(26))

    # ================================================================ p5 — ancoraggio
    sec(C_ANC, 'Ancoraggio')
    S.append(LineHeader('2', 'L’ancoraggio su roccia', _occh('ancoraggio'), C_ANC))
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
    S.append(SP(26))

    sec(C_ANC, 'Ancoraggio')
    S.append(LineHeader('', 'Che cosa si vede e che cosa manca', _occh('ancoraggio · inventario'), C_ANC))
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
    S.append(SP(26))

    # ================================================================ p6 — dettaglio punto
    sec(C_ANC, 'Ancoraggio')
    S.append(_apre(
        LineHeader('3', 'Il singolo punto', _occh('ancoraggio · dettaglio'), C_ANC),
        P('Il punto è una <b>placchetta metallica fissata con un dado esagonale su '
          'bullone</b>. Si tratta quindi di un tassello meccanico: non di uno spit a vite, '
          'e non di un resinato con occhiello integrato. Misura, marca e anno di posa non '
          'sono ricavabili dalle immagini.', lead)))
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
    S.append(SP(26))

    # ================================================================ p7 — la sosta
    sec(C_SOS, 'Sosta')
    S.append(LineHeader('4', 'Instradamento della slinga', _occh('costruzione della sosta'), C_SOS))
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
    S.append(SP(26))

    # ================================================================ p8 — tensione e anti-slip
    sec(C_TEN, 'Tensione')
    S.append(LineHeader('5', 'Lato tensione e anti-slip', _occh('tensione e anti-slip'), C_TEN))
    S.append(SP(10))
    S.append(P('Sul lato di tensione la linea passa nel <b>weblock</b>, che il gruppo chiama '
               '«banana». A tensionamento concluso viene aggiunto l’<b>anti-slip</b>, un nodo '
               'sulla linea la cui funzione è l’unica del corpus a essere insieme spiegata a '
               'voce e mostrata.', lead))
    S.append(SP(12))
    # la sequenza sta prima delle fotografie: messa in coda tracimava sulla
    # pagina successiva e la lasciava riempita per un quinto. Letta qui e' anche
    # l'indice di cio' che le due fotografie mostrano.
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
    S.append(SP(26))

    # ================================================================ p9 — materiale
    sec(LINEA, 'Materiale')
    S.append(KeepTogether([
        LineHeader('6', 'Il materiale', _occh('materiale'), LINEA),
        SP(10),
        P('Elenco costruito incrociando i nomi pronunciati nei video con gli oggetti '
          'riconoscibili nelle immagini. La colonna delle misure è quasi interamente '
          'vuota, e resta tale.', lead)]))
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
    S.append(SP(26))

    # ================================================================ p_ — A-frame
    # Elemento strutturale che nessuna trascrizione nomina: esiste solo nelle
    # fotografie, e per questo la sezione dice prima di tutto da dove viene.
    sec(C_TEN, 'A-frame')
    S.append(LineHeader('7', 'L’A-frame', _occh('lato tensione · A-frame'), C_TEN))
    S.append(SP(10))
    S.append(P('Sul lato dell’<b>ancoraggio main</b> la linea non esce dalla sosta e va '
               'diritta nel vuoto: passa sopra un <b>A-frame</b>, due pali di legno tondo '
               'incrociati in testa e appoggiati sul bordo. In ventidue minuti di parlato '
               'nessuno lo nomina mai. È documentato <b>solo da due fotografie</b>, ed è per '
               'questo che qui si descrive ciò che si vede e nient’altro.', lead))
    S.append(SP(10))
    S.append(ChipRow([('Pali', '2 · legno tondo'), ('Testa', 'Incrociata e legata'),
                      ('Piede', 'Appoggiato su roccia'), ('Altezza', '[DA CONF.]')], C_TEN))
    S.append(SP(12))
    S.append(photo_pair(
        str(FOTO / 'IMG_1416.jpg'), str(FOTO / 'IMG_1396.jpg'),
        # Le didascalie di photo_pair vanno su una riga sola e non vengono
        # mandate a capo: piu' larghe della colonna si sovrappongono a quella
        # accanto. Meta' colonna regge circa cinquanta battute a corpo 7,4.
        'Il palo visto dall’ancoraggio main · IMG_1416, 17:14',
        'Testa dei pali, con la fettuccia viola · IMG_1396',
        *dim(FOTO / 'IMG_1416.jpg'), color=C_TEN, ratio=1.28, focus=0.62,
        ow2=dim(FOTO / 'IMG_1396.jpg')[0], oh2=dim(FOTO / 'IMG_1396.jpg')[1]))
    S.append(SP(14))
    S.append(two_cols(
        gear_block('Ciò che si vede', [
            'Due pali di legno tondo, incrociati e legati in testa',
            'Fettuccia viola avvolta sulla testa dei pali',
            'Corda verde fluo, fettuccia blu e corda rosa in testa',
            'Piede dei pali appoggiato sulla roccia del bordo',
            'Giri di filo metallico attorno al piede di un palo',
        ], C_TEN),
        gear_block('Ciò che manca', [
            'Altezza dei pali — [DA CONFERMARE]',
            'Diametro e tipo del legno — [DA CONFERMARE]',
            'Come sono legati fra loro in testa — [DA CONFERMARE]',
            'Se i piedi siano fermati o solo appoggiati — [DA CONFERMARE]',
            'Se il filo metallico tenga il palo o sia un recinto — [DA CONFERMARE]',
            'Di quanto solleva la linea sopra il bordo — [DA CONFERMARE]',
        ], WARN)))
    S.append(SP(12))
    S.append(callout('Perché un elemento non nominato conta lo stesso',
                     'L’A-frame solleva la linea sopra il bordo: cambia l’angolo con cui la '
                     'linea carica la sosta e tiene il nastro lontano dalla roccia. '
                     '<b>Non è un accessorio.</b> Che di un pezzo così non esista né una '
                     'parola registrata né una misura è, di questo montaggio, il vuoto '
                     'documentale più grande dopo l’ancoraggio.', WARN, '!', FW, True))
    S.append(SP(26))

    # ================================================================ dove si trova
    sec(C_TEN, 'Posizione')
    S.append(_apre(
        LineHeader('', 'Dove si trova l’ancoraggio main', _occh('posizione'), C_TEN),
        P('La fotografia delle 17:14 è stata scattata <b>stando all’ancoraggio main</b>, e il '
          'telefono ha registrato la posizione. È il primo dato di posizione che questo '
          'progetto possiede: nessun video la nomina, e il catalogo i-pietra non aiuta perché '
          'le sue coordinate sono punti di una scena tridimensionale, non gradi sul terreno.',
          lead)))
    S.append(SP(12))
    S.append(data_table(
        ['Dato', 'Valore', 'Da dove viene'],
        [['Latitudine, longitudine', '44.419869, 10.412353',
          'EXIF di IMG_1416, 16/05/2026 17:14:38'],
         ['Quota', '1025 m', 'EXIF di IMG_1416 — lettura del telefono'],
         ['Ancoraggio opposto', '[DA CONFERMARE]', 'nessuna fotografia geolocalizzata']],
        [128, 132, FW - 260], C_TEN))
    S.append(SP(12))
    S.append(callout('Una posizione, non un rilievo',
                     'La coordinata dice dove stava <b>il telefono</b>, con la precisione che '
                     'ha un GPS telefonico sotto una parete: colloca l’ancoraggio su una mappa, '
                     'non lo quota. Vale come indicazione di avvicinamento — non per ritrovare '
                     'il singolo punto, che va cercato a vista.', C_TEN))
    S.append(SP(26))

    # ================================================================ la linea in opera
    sec(LINEA, 'In opera')
    S.append(LineHeader('8', 'La linea in opera', _occh('in opera, ore 17:08'), LINEA))
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

    return S
