# -*- coding: utf-8 -*-
"""Parte 2 della guida: come si monta una linea alla Pietra.

Fino all'edizione dell'8 ottobre la stessa materia stava in un capitolo
intitolato alla giornata del 16 maggio: una cronologia, citazioni dai video,
osservazioni su che cosa le riprese mostrassero o no. Era la ricostruzione di un
montaggio. Qui diventa il metodo, ordinato come lo si esegue: i due lati di una
linea, il materiale, la sequenza, poi ogni fase.

Le fonti non cambiano, cambia dove si dicono. Ogni riga di queste pagine viene
dal montaggio della 53 m dell'Anfiteatro (trascrizioni e fotogrammi, vedi
NOTE_RIGGING.md, sezioni A-G) o dalle risposte di chi ha montato; i riferimenti
ai file stanno nei commenti, non nel testo per il lettore. Dove una voce vale per
quella linea sola, il testo lo dice. Dove manca, resta [DA CONFERMARE].

Nessuna regola generica di highlining entra qui per riempire un vuoto.

    from metodo import parte_metodo
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import KeepTogether, PageBreak              # noqa: E402
from scheda_53 import (foto, dim, ANN, FOTO, LINEA, C_ANC, C_SOS,   # noqa: E402
                       C_TEN, C_ASL, DC)

DCC = '[DA CONF.]'


def _apre(testata, *seguito):
    """Testata legata al suo primo blocco: non resta mai sola in fondo pagina."""
    return KeepTogether([testata, SP(10)] + list(seguito))


def _testata(n, titolo, occhiello, colore):
    return LineHeader(str(n), titolo, 'Come si monta · %s' % occhiello, colore)


def parte_metodo():
    S = []

    def sec(colore, etichetta, chiave):
        S.append(Accent(colore, etichetta))
        S.append(Segna(chiave))

    # ============================================================ 1 · i due lati
    # Lati ricostruiti dall'ordine delle operazioni (NOTE_RIGGING A, D, E, F) e
    # dalla risposta del 20/08 sull'A-frame: dubbio 56.
    sec(LINEA, 'Due lati', 'lati')
    S.append(_apre(
        _testata(1, 'Una linea, due lati', 'schema', LINEA),
        P('Una linea ha due ancoraggi. Sul <b>lato tensione</b> si costruiscono due soste '
          'indipendenti, si tensiona la linea e la si fa passare sopra l’A-frame. Sul '
          '<b>lato opposto</b> c’è la sosta su più punti a cui la linea arriva. Sulla 53 m '
          'dell’Anfiteatro gli ancoraggi sono su roccia da entrambi i lati.', lead)))
    S.append(SP(14))
    S.append(two_cols(
        gear_block('Lato tensione', [
            'Sosta main con slinghe viola',
            'Sosta backup con corde rosa, collegate con un BFK',
            'Weblock («banana») e grillo a lira',
            'Paranchino di tensionamento della base',
            'Blocco del backup, che prende entrambe le soste',
            'Anti-slip sulla linea, a tensione fatta',
            'A-frame sul bordo',
        ], C_TEN),
        gear_block('Lato opposto', [
            'Sosta su tre punti: placchette su bullone',
            'Punti collegati con una corda annodata',
            'Slinga viola e carrucola bloccante',
            'Linea vita con la corda azzurra',
            'Una sosta backup anche qui — com’è fatta, ' + DC,
        ], C_ANC)))
    S.append(SP(12))
    S.append(callout('Quale lato è quale',
                     'Sulla 53 m la tensione si fa dove stanno sosta main e sosta backup, ed è '
                     'il lato dell’A-frame; la sosta su tre punti è sul lato opposto. È '
                     'ricostruito dall’ordine delle operazioni, e va confermato: ' + DC + '.',
                     C_TEN))
    S.append(SP(26))

    # ============================================================ 2 · materiale
    # Tabella da NOTE_RIGGING, «Materiale nominato», con la colonna «Dove si usa».
    # E' anche la lista prima di uscire che CLAUDE.md chiede fra gli apparati.
    sec(LINEA, 'Materiale', 'materiale')
    S.append(_apre(
        _testata(2, 'Prima di uscire: il materiale', 'il materiale per una linea', LINEA),
        P('Il materiale con cui è stata montata la 53 m dell’Anfiteatro: è la lista da '
          'preparare prima di uscire. Le quantità note sono indicate; le misure, per ora, '
          'quasi mai.', lead)))
    S.append(SP(14))
    S.append(data_table(
        ['Qtà', 'Articolo', 'Dove si usa', 'Misura'],
        [['n.d.', 'Slinghe viola — brache ad anello industriali', 'sosta main', DCC],
         ['n.d.', 'Corde rosa', 'sosta backup', DCC],
         ['1', 'BFK, moschettone d’acciaio grande', 'sulla corda rosa del backup', DCC],
         ['4', 'Maglie rapide delta', DCC, DCC],
         ['1', '«Mighty Lock», «quello quadratino» — nome incerto', 'backup', DCC],
         ['1', 'Slinga verde lunga, «la più grossa che c’è»', DCC, DCC],
         ['1', 'Slinga piccola viola', DCC, DCC],
         ['≥1', 'Slinga verde e nera', DCC, DCC],
         ['1', 'Corda azzurra', 'tagline, poi linea vita', DCC],
         ['1', 'Corda verde acqua', 'collegamento fra i punti', DCC],
         ['≥1', 'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm', 'sull’ancoraggio',
          'marca ' + DCC],
         ['1', 'Weblock azzurro anodizzato, detto «banana»', 'lato tensione',
          'modello ' + DCC],
         ['≥1', 'Grillo a lira in acciaio', 'collegamento della sosta', DCC],
         ['1', 'Paranchino', 'tensionamento della base', DCC],
         ['1', 'Softrelease', DCC, 'modello ' + DCC],
         ['≥2', 'Grigri', 'backup e calata', '—'],
         ['1', 'Corda di backup', 'per chi lavora in sosta', DCC],
         ['n.d.', 'Nastro della highline', '—', DCC],
         ['n.d.', 'Backup della linea', '—', DCC],
         ['n.d.', 'Leash', '—', DCC]],
        [36, 222, 142, 91], LINEA))
    S.append(SP(10))
    S.append(foto('IMG_1360.jpg', FW, 'Slinghe viola, corde rosa, fettuccia verde, grilli e '
                  'maglie rapide, stesi prima del montaggio', LINEA, ratio=0.42, focus=0.42))
    S.append(SP(12))
    S.append(callout('Ancora da documentare',
                     'Nastro della linea, backup della linea e leash sono gli elementi centrali '
                     'di una highline: marca, larghezza e tipo sono ' + DC + '.',
                     WARN, '!', FW, True))
    S.append(SP(26))

    # ============================================================ 3 · sequenza
    # Ordine dai metadati dei file, NOTE_RIGGING A-G. Gli orari stanno li'.
    # Steps disegna testo semplice: niente markup nelle descrizioni.
    sec(LINEA, 'Sequenza', 'sequenza')
    S.append(_apre(
        _testata(3, 'La sequenza di montaggio', 'in ordine', LINEA),
        P('Le fasi nell’ordine in cui si eseguono, come sulla 53 m dell’Anfiteatro. Ognuna '
          'ha il suo capitolo nelle pagine che seguono.', lead),
        SP(12),
        Steps([
            ('Dividere il materiale', 'Viola alla sosta main, rosa alla backup'),
            ('Due soste in parallelo', 'Main e backup sul lato tensione; intanto una '
             'persona raggiunge il lato opposto'),
            ('Instradare le slinghe', 'Nell’anello d’acciaio, con il nodo che le forza'),
            ('Orientare e ingrillare', 'Slinghe nel verso di lavoro, senza torsioni'),
            ('Sosta sul lato opposto', 'Su tre punti, collegati con una corda annodata'),
            ('Portare la linea', 'La corda azzurra porta la tagline, poi fa da linea vita'),
            ('Pretensionare', 'Paranchino di base, tensione provvisoria'),
            ('Bloccare il backup', 'Un collegamento che prende sosta main e sosta backup'),
            ('Tensionare', 'Tensionamento finale — come e quanto: [DA CONFERMARE]'),
            ('Anti-slip', 'Sulla linea, a tensione fatta'),
            ('Verificare', 'Si va sulla linea per vedere se va ritensionata'),
        ], LINEA, FW, 2),
        SP(12),
        # IMG_1370 @ 0:00-0:15 e IMG_1380 @ 0:54-0:57: dubbi 29 e 30. Legate alla
        # sequenza: da sole finivano su una pagina vuota.
        callout('Due avvertenze da chiarire',
                'Durante il montaggio è stato detto che un componente «ruotando può '
                'cadere» e che un’operazione «andrebbe fatta dopo, quando c’è del peso». '
                'Quale componente e quale operazione: ' + DC + ', da chiedere a chi ha '
                'montato.', WARN, '!', FW, True)))
    S.append(SP(26))

    # ============================================================ 4 · ancoraggi
    # IMG_1371, IMG_1372, IMG_1374 @ 0:29; roccia dalla scheda di settore i-pietra
    sec(C_ANC, 'Ancoraggi', 'ancoraggi')
    S.append(KeepTogether([
        _testata(4, 'Gli ancoraggi su roccia', 'lato opposto', C_ANC),
        SP(10),
        P('La roccia della Pietra è <b>arenaria</b>, meno tenace del calcare: va valutata '
          'attorno a ogni foro. I punti sono <b>placchette metalliche fissate con un dado '
          'esagonale su bullone</b> — un tassello meccanico, non uno spit a vite né un '
          'resinato con occhiello. Sulla 53 m la sosta del lato opposto usa <b>tre punti</b>, '
          'collegati con una corda annodata.', lead),
        SP(10),
        ChipRow([('Punti', '3'), ('Tipo', 'Placchetta su bullone'),
                 ('Collegamento', 'Corda annodata'), ('Angolo', DCC)], C_ANC),
        SP(12),
        foto('D1_ancoraggio.jpg', FW, 'Sosta su tre punti — placchetta, cordino di '
             'collegamento, carrucola bloccante e slinga viola', C_ANC,
             ratio=0.80, focus=0.78)]))
    S.append(SP(14))
    S.append(two_cols(
        gear_block('Com’è fatta', [
            'Placchetta metallica su bullone con dado esagonale',
            'Connettore d’acciaio a ghiera',
            'Maglia rapida in acciaio',
            'Corda verde acqua annodata fra i punti',
            'Slinga viola (braca ad anello industriale)',
            'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm',
        ], C_ANC),
        gear_block('Ancora da rilevare', [
            'Diametro e marca del bullone — ' + DCC,
            'Angolo di apertura fra i punti — ' + DCC,
            'Punti sul lato tensione: quanti e quali — ' + DCC,
            'Marca della carrucola bloccante — ' + DCC,
            'Protezione veloce accanto ai punti fissi — ' + DCC,
            'Una fotografia d’insieme dei tre punti',
        ], WARN)))
    S.append(SP(14))
    S.append(_apre(
        P('<b>Il punto da vicino</b>', h3),
        foto('D2_placchetta_dettaglio.jpg', FW, 'Placchetta e dado esagonale', C_ANC,
             ratio=0.50, focus=0.55)))
    S.append(SP(12))
    S.append(callout('Perché la distinzione conta',
                     'Spit, tasselli a espansione e resinati hanno comportamenti, durate e '
                     'controlli diversi. Un dado su bullone basta a escludere lo spit a vite e '
                     'il resinato con occhiello, non a stabilire quale tassello sia: si verifica '
                     'sul posto.', C_ANC))
    S.append(SP(12))
    S.append(Segna('controlli'))
    S.append(KeepTogether([
        P('<b>Controlli prima di caricare un punto</b>', h3),
        SP(5),
        BU('Che il dado sia serrato e non presenti gioco.', C_ANC),
        BU('Che la placchetta non ruoti sul bullone.', C_ANC),
        BU('Che la roccia attorno al foro non presenti fratture o sfaldature.', C_ANC),
        BU('Che non vi sia corrosione visibile su placchetta, dado o bullone.', C_ANC),
        SP(8),
        P('L’elenco discende dal tipo di ancoraggio. La checklist che usa il gruppo è '
          + DC + '.', small)]))
    S.append(SP(26))

    # ============================================================ 5 · soste
    # IMG_1349 @ 0:00, IMG_1350 @ 0:00 e 0:53; foto IMG_1357, IMG_1359 delle 13:07
    sec(C_SOS, 'Soste', 'soste')
    S.append(_apre(
        _testata(5, 'Le soste: main e backup', 'lato tensione', C_SOS),
        P('Sul lato tensione si allestiscono <b>due soste indipendenti</b>, distinte a colpo '
          'd’occhio dal materiale: la <b>sosta main</b> con le slinghe viola, la <b>sosta '
          'backup</b> con le corde rosa. Il codice colore serve a non confondere i due '
          'sistemi mentre si lavora in parete.', lead),
        SP(10),
        ChipRow([('Sosta main', 'Slinghe viola'), ('Sosta backup', 'Corde rosa'),
                 ('Connettore', 'BFK'), ('Maglie', '4 delta')], C_SOS)))
    S.append(SP(12))
    S.append(photo_pair(
        str(FOTO / 'IMG_1357.jpg'), str(FOTO / 'IMG_1359.jpg'),
        'Slinghe e corde stese, pronte per le due soste', 'Il materiale disposto sulla roccia',
        *dim(FOTO / 'IMG_1357.jpg'), color=C_SOS, ratio=0.95, focus=0.5,
        ow2=dim(FOTO / 'IMG_1359.jpg')[0], oh2=dim(FOTO / 'IMG_1359.jpg')[1]))
    S.append(SP(14))
    S.append(KeepTogether([
        P('<b>Come si procede</b>', h3),
        SP(5),
        BU('Le due soste si allestiscono <b>in parallelo</b>: mentre una persona lavora sul '
           'lato tensione, un’altra raggiunge il lato opposto per costruire la sosta di là.',
           C_SOS),
        BU('La corda rosa del backup si collega con un <b>BFK</b>, il moschettone '
           'd’acciaio grande.', C_SOS),
        BU('Sulla 53 m sono servite <b>quattro maglie rapide delta</b>.', C_SOS),
        SP(8),
        P('Lunghezze e diametri di slinghe e corde: ' + DC + '.', small)]))
    S.append(SP(18))
    # IMG_1360 e il suo ritaglio: dubbio 37, il piu' pericoloso del documento
    S.append(_apre(
        P('<b>La portata delle slinghe</b>', h3),
        P('Le slinghe della sosta main sono brache ad anello industriali, con un’etichetta '
          'cucita sulla calza. La portata è quella stampata sull’etichetta: ' + DC + '. '
          'Nelle fotografie disponibili l’etichetta è rivoltata e non si legge.', body),
        SP(10),
        foto('IMG_1360_etichetta.jpg', FW, 'L’etichetta cucita sulla calza, rivoltata',
             C_SOS, ratio=0.40, focus=0.5)))
    S.append(SP(12))
    S.append(callout('Il colore non è una portata',
                     'Una calza viola con una riga scura sembra una portata dichiarata, ma non lo '
                     'è: il colore sbiadisce al sole, le codifiche cambiano fra costruttori, e una '
                     'riga cucita non è un’indicazione di portata. <b>Vale solo l’etichetta</b>: '
                     'per leggerla serve una fotografia ravvicinata dell’etichetta distesa.',
                     WARN, '!', FW, True))
    S.append(SP(26))

    # ============================================================ 6 · slinga
    # IMG_1366, IMG_1367 @ 0:43 (il perche' del nodo), IMG_1369 (verso di lavoro)
    sec(C_SOS, 'Slinga', 'slinga')
    S.append(_apre(
        _testata(6, 'Instradamento della slinga', 'costruzione della sosta', C_SOS),
        P('La slinga passa nell’anello d’acciaio e si ferma con un nodo che serve a '
          '<b>forzare la slinga</b>: chi lo usa lo sceglie perché la tenuta è sufficiente ed '
          'è veloce da regolare. Poi le slinghe si orientano nel <b>verso in cui lavorano</b>, '
          'senza torsioni, e si ingrillano.', lead)))
    S.append(SP(12))
    S.append(photo_row([
            (str(ANN / 'B1_slinga_aperta.jpg'),) + dim(ANN / 'B1_slinga_aperta.jpg')
            + ('1 · slinga aperta',),
            (str(ANN / 'B2_passaggio_anello.jpg'),) + dim(ANN / 'B2_passaggio_anello.jpg')
            + ('2 · nell’anello',),
            (str(ANN / 'B3_giro_chiuso.jpg'),) + dim(ANN / 'B3_giro_chiuso.jpg')
            + ('3 · giro chiuso',),
        ], C_SOS))
    S.append(SP(12))
    S.append(callout('Il nome del nodo',
                     'Come si chiama il nodo e quali alternative sono accettabili: ' + DC +
                     ', da chiedere a chi lo esegue.', C_SOS))
    S.append(SP(26))

    # ============================================================ 7 · linea e linea vita
    # IMG_1350 @ 0:33-0:41 (corda azzurra), IMG_1378 @ 0:42 (backup e Grigri)
    sec(C_SOS, 'Linea vita', 'lineavita')
    S.append(_apre(
        _testata(7, 'Portare la linea, la linea vita', 'fra i due lati', C_SOS),
        P('La <b>corda azzurra</b> ha due usi: prima porta la tagline da un lato all’altro, '
          'poi diventa <b>linea vita</b> sulla sosta del lato opposto. Per chi lavora in '
          'sosta servono una <b>corda di backup</b> e un <b>Grigri</b>.', lead),
        SP(8),
        P('Come si porta la tagline da un lato all’altro: ' + DC + '.', small)))
    S.append(SP(26))

    # ============================================================ 8 · tensione
    # IMG_1380, 1381, 1383 (pretensione), IMG_1384 @ 0:00-0:55 (blocco backup),
    # IMG_1392 (tensione finale), IMG_1394 (softrelease), IMG_1395 (anti-slip)
    sec(C_TEN, 'Tensione', 'tensione')
    S.append(_apre(
        _testata(8, 'Il lato tensione', 'tensione e anti-slip', C_TEN),
        P('La linea passa nel <b>weblock</b> — in gergo «banana» — collegato con un grillo '
          'a lira. Si pretensiona con il <b>paranchino di tensionamento della base</b>. Poi '
          'si <b>blocca il backup</b>: un collegamento che prende sia la sosta main sia la '
          'sosta backup e si chiude sul grillo. Dopo il tensionamento finale si aggiunge '
          'l’<b>anti-slip</b>, un nodo sulla linea che impedisce che slitti nel weblock.',
          lead),
        SP(10),
        ChipRow([('Bloccante', 'Weblock'), ('Collegamento', 'Grillo a lira'),
                 ('Tensione', 'Paranchino'), ('Sicura', 'Anti-slip')], C_TEN)))
    S.append(SP(12))
    S.append(photo_pair(
        str(ANN / 'F1_weblock_grillo.jpg'), str(ANN / 'G1_antislip.jpg'),
        'Weblock e grillo a lira', 'L’anti-slip sulla linea',
        *dim(ANN / 'F1_weblock_grillo.jpg'), color=C_TEN,
        ow2=dim(ANN / 'G1_antislip.jpg')[0], oh2=dim(ANN / 'G1_antislip.jpg')[1]))
    S.append(SP(14))
    S.append(KeepTogether([
        P('<b>Ancora da rilevare</b>', h3),
        SP(5),
        BU('Il nodo dell’anti-slip, il materiale e il punto esatto in cui va: ' + DC + '.',
           C_TEN),
        BU('Come si fa il tensionamento finale e quanta tensione si raggiunge: ' + DC + '.',
           C_TEN),
        BU('Dove sta il softrelease nel sistema, e quale modello: ' + DC + '.', C_TEN)]))
    S.append(SP(26))

    # ============================================================ 9 · A-frame
    # IMG_1396 e IMG_1416; posizione sul lato main dalla risposta del 20/08
    sec(C_TEN, 'A-frame', 'aframe')
    S.append(_apre(
        _testata(9, 'L’A-frame', 'lato tensione', C_TEN),
        P('Sul lato tensione la linea passa sopra un <b>A-frame</b>: due pali di legno tondo '
          'incrociati e legati in testa, con i piedi appoggiati sulla roccia del bordo. '
          'Solleva la linea sopra il bordo, cambia l’angolo con cui la linea carica la sosta '
          'e tiene il nastro lontano dalla roccia: non è un accessorio.', lead),
        SP(10),
        ChipRow([('Pali', '2 · legno tondo'), ('Testa', 'Incrociata e legata'),
                 ('Piede', 'Appoggiato su roccia'), ('Altezza', DCC)], C_TEN)))
    S.append(SP(12))
    S.append(photo_pair(
        # Le didascalie di photo_pair vanno su una riga sola: meta' colonna regge
        # circa cinquanta battute a corpo 7,4.
        str(FOTO / 'IMG_1416.jpg'), str(FOTO / 'IMG_1396.jpg'),
        'Il palo visto dall’ancoraggio main', 'Testa dei pali, con la fettuccia viola',
        *dim(FOTO / 'IMG_1416.jpg'), color=C_TEN, ratio=1.20, focus=0.62,
        ow2=dim(FOTO / 'IMG_1396.jpg')[0], oh2=dim(FOTO / 'IMG_1396.jpg')[1]))
    S.append(SP(14))
    S.append(two_cols(
        gear_block('Com’è fatto', [
            'Due pali di legno tondo, incrociati e legati in testa',
            'Fettuccia viola avvolta sulla testa dei pali',
            'Corda verde fluo, fettuccia blu e corda rosa in testa',
            'Piedi appoggiati sulla roccia del bordo',
            'Giri di filo metallico attorno al piede di un palo',
        ], C_TEN),
        gear_block('Ancora da rilevare', [
            'Altezza dei pali — ' + DCC,
            'Diametro e tipo del legno — ' + DCC,
            'Come sono legati in testa — ' + DCC,
            'Se i piedi sono fermati o solo appoggiati — ' + DCC,
            'Se il filo metallico tiene il palo o è un recinto — ' + DCC,
            'Di quanto solleva la linea sopra il bordo — ' + DCC,
        ], WARN)))
    S.append(SP(26))

    # ============================================================ 10 · smontaggio
    # Dubbio 35: nessuna ripresa dello smontaggio
    sec(LINEA, 'Smontaggio', 'smontaggio')
    S.append(_apre(
        _testata(10, 'Lo smontaggio', 'alla fine', LINEA),
        P('La sequenza di smontaggio non è ancora documentata: ' + DC + '. È il prossimo '
          'capitolo da scrivere con chi monta.', lead)))
    S.append(PageBreak())
    return S
