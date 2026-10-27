# -*- coding: utf-8 -*-
"""Parte 2 della guida: come si monta una linea alla Pietra.

Il metodo, ordinato come lo si esegue: i due lati di una linea, che cosa serve,
la sequenza, poi ogni fase. Fino all'edizione dell'8 ottobre la stessa materia
stava in un capitolo intitolato alla giornata del 16 maggio, una cronologia.

Il criterio che separa questa parte dalla scheda di una linea, lo stesso della
guida Sillschlucht di Innsbruck: **qui si dice come si fa** — funzioni, tipi di
materiale, principi. **La scheda dice com'e' fatta quella linea**: quantita',
colori, numero di punti, posizioni, che cosa manca. Le fotografie della 53 m
compaiono qui solo come esempi, e la didascalia lo dichiara.

Le fonti: il montaggio della 53 m dell'Anfiteatro (trascrizioni e fotogrammi,
NOTE_RIGGING.md, sezioni A-G), il montaggio con i bungee del 22/08/2026 e le
risposte di chi ha montato. I riferimenti ai file stanno nei commenti, non nel
testo per il lettore. Dove manca qualcosa resta [DA CONFERMARE]: nessuna regola
generica di highlining entra qui per riempire un vuoto.

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


# Esempio dalle foto del file LineeBisma (lette il 27/10/2026, lavorazione/foto_linee/*/LETTURA.md)
# nel capitolo degli ancoraggi: quale foto usare lo decide Carlos, non il codice.
# Finche' non decide resta None e non si stampa nulla. Le due candidate leggibili:
#   ('anfiteatro-46', 'anfiteatro-46_04_lontano_ancoraggio-placchetta-dettaglio.jpg',
#    'Esempio dalla 46 m, lato «lontano» del file: placchetta con dado esagonale e '
#    'grillo a lira. Quale sia il lato di tensione non è noto')
#   ('anfiteatro-113', 'anfiteatro-113_05_lontano_sosta-con-tronco-dettaglio.jpg',
#    'Esempio dalla 113 m (o 108: da chiarire), lato «lontano» del file: sosta con '
#    'tronco. Quale sia il lato di tensione non è noto')
ESEMPIO_CARLO = None
FOTO_LINEE = RADICE / 'lavorazione' / 'foto_linee'


def esempio_carlo(colore):
    """La foto scelta dall'autore come esempio, con la didascalia che dichiara i limiti."""
    if not ESEMPIO_CARLO:
        return []
    id_linea, nome_file, didascalia = ESEMPIO_CARLO
    p = FOTO_LINEE / id_linea / nome_file
    if not p.exists():
        return []
    return [SP(12), PhotoStrip(str(p), FW, *dim(p), didascalia, colore, 0.55, 0.5)]


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
    # Ruoli dei due lati dall'ordine delle operazioni (NOTE_RIGGING A, D, E, F).
    # Quale lato sia quale sulla 53 m sta nella sua scheda (dubbio 56, chiuso il 27/10).
    sec(LINEA, 'Due lati', 'lati')
    S.append(_apre(
        _testata(1, 'Una linea, due lati', 'schema', LINEA),
        P('Una linea ha due ancoraggi, con compiti diversi. Sul <b>lato tensione</b> si '
          'costruiscono due soste indipendenti, main e backup, e si tensiona la linea. Sul '
          '<b>lato statico</b> c’è una sosta su più punti a cui la linea arriva.', lead)))
    S.append(SP(14))
    S.append(two_cols(
        gear_block('Lato tensione', [
            'Sosta main',
            'Sosta backup, indipendente dalla main',
            'Sistema di tensione: weblock, grillo, paranchino',
            'Blocco del backup, che prende entrambe le soste',
            'Anti-slip sulla linea, a tensione fatta',
            'A-frame sul bordo, se la linea lo prevede',
        ], C_TEN),
        gear_block('Lato statico', [
            'Sosta su più punti fissi',
            'Punti collegati fra loro',
            'Linea vita per chi lavora in sosta',
            'Sosta backup — com’è fatta, ' + DC,
        ], C_ANC)))
    S.append(SP(10))
    S.append(P('Com’è fatto ciascun lato su una linea precisa — quanti punti, quale materiale, '
               'dove si trova — lo dice la sua scheda, nella parte 3.', small))
    S.append(SP(26))

    # ============================================================ 2 · prima di uscire
    # Le voci sono quelle del materiale nominato (NOTE_RIGGING), raggruppate per
    # funzione con la colonna «dove si usa». Quantita' e misure stanno nella
    # scheda della linea: qui sarebbero quelle di una linea sola.
    sec(LINEA, 'Materiale', 'materiale')
    S.append(_apre(
        _testata(2, 'Prima di uscire: il materiale', 'che cosa serve', LINEA),
        P('Che cosa serve per montare una linea, voce per voce, nell’ordine del metodo. '
          'Quantità e misure dipendono dalla linea: le dà la sua scheda.', lead)))
    S.append(SP(12))
    S.append(data_table(
        ['Per', 'Che cosa serve'],
        [['La sosta main', 'Brache ad anello industriali («slinghe»)'],
         ['La sosta backup', 'Corde, con un connettore d’acciaio (BFK)'],
         ['Collegare i punti', 'Una corda, annodata fra i punti'],
         ['L’ancoraggio', 'Carrucola bloccante'],
         ['I collegamenti della sosta', 'Grilli a lira; maglie rapide — dove si usano, ' + DC],
         ['La tensione', 'Weblock e paranchino; softrelease — dove si usa, ' + DC],
         ['Portare la linea', 'Tagline, e una corda che poi fa da linea vita'],
         ['Chi lavora in sosta', 'Corda di backup e Grigri'],
         ['La linea', 'Nastro, backup della linea, leash — ' + DC],
         ['Il bordo', 'A-frame, se la linea lo prevede']],
        [150, FW - 150], LINEA))
    S.append(SP(8))
    S.append(P('L’elenco completo della 53 m dell’Anfiteatro, con le quantità, è a '
               + rif('materiale53', 'pagina [rimando]') + '.', small))
    S.append(SP(26))

    # ============================================================ 3 · sequenza
    # Ordine dai metadati dei file, NOTE_RIGGING A-G. Steps disegna testo
    # semplice: niente markup nelle descrizioni.
    sec(LINEA, 'Sequenza', 'sequenza')
    S.append(_apre(
        _testata(3, 'La sequenza di montaggio', 'in ordine', LINEA),
        P('Le fasi nell’ordine in cui si eseguono. Ognuna ha il suo capitolo nelle pagine '
          'che seguono.', lead),
        SP(12),
        Steps([
            ('Dividere il materiale', 'Un colore per la sosta main, uno per la backup'),
            ('Due soste in parallelo', 'Main e backup sul lato tensione; intanto una '
             'persona raggiunge il lato statico'),
            ('Instradare le slinghe', 'Nell’anello d’acciaio, con il nodo che le forza'),
            ('Orientare e ingrillare', 'Slinghe nel verso di lavoro, senza torsioni'),
            ('Sosta sul lato statico', 'Su più punti, collegati con una corda annodata'),
            ('Portare la linea', 'La tagline passa da un lato all’altro; la corda fa poi '
             'da linea vita'),
            ('Pretensionare', 'Paranchino di base, tensione provvisoria'),
            ('Bloccare il backup', 'Un collegamento che prende sosta main e sosta backup'),
            ('Tensionare', 'Tensionamento finale — come e quanto: [DA CONFERMARE]'),
            ('Anti-slip', 'Sulla linea, a tensione fatta'),
            ('Verificare', 'Si va sulla linea per vedere se va ritensionata'),
        ], LINEA, FW, 2),
        SP(12),
        # IMG_1370 @ 0:00-0:15 e IMG_1380 @ 0:54-0:57: dubbi 29 e 30
        callout('Due avvertenze da chiarire',
                'Durante il montaggio documentato è stato detto che un componente «ruotando '
                'può cadere» e che un’operazione «andrebbe fatta dopo, quando c’è del peso». '
                'Quale componente e quale operazione: ' + DC + ', da chiedere a chi ha '
                'montato.', WARN, '!', FW, True)))
    S.append(SP(26))

    # ============================================================ 4 · ancoraggi
    # Roccia dalla scheda di settore i-pietra; placchette in IMG_1371, IMG_1372 e
    # nelle foto del 22/08; punti collegati con corda annodata in entrambi i montaggi
    sec(C_ANC, 'Ancoraggi', 'ancoraggi')
    S.append(KeepTogether([
        _testata(4, 'Gli ancoraggi su roccia', 'i punti fissi', C_ANC),
        SP(10),
        P('La roccia della Pietra è <b>arenaria</b>, meno tenace del calcare: va valutata '
          'attorno a ogni foro. I punti sono <b>placchette metalliche fissate con un dado '
          'esagonale su bullone</b> — non uno spit a vite né un resinato con occhiello; se '
          'il bullone sia un tassello meccanico o una barra resinata si verifica sul posto. '
          'La sosta si costruisce su <b>più punti</b>, collegati fra '
          'loro con una corda annodata.', lead),
        SP(12),
        foto('D1_ancoraggio.jpg', FW, 'Esempio dalla 53 m: sosta su tre punti — placchetta, '
             'cordino di collegamento, carrucola bloccante, slinga', C_ANC,
             ratio=0.80, focus=0.78)]))
    S.append(SP(14))
    S.append(_apre(
        P('<b>Il punto da vicino</b>', h3),
        foto('D2_placchetta_dettaglio.jpg', FW, 'Placchetta e dado esagonale', C_ANC,
             ratio=0.50, focus=0.55),
        *esempio_carlo(C_ANC)))
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
    # IMG_1349 @ 0:00, IMG_1350 @ 0:00. Il codice colore e' un principio, non una
    # convenzione fissa: il 22/08, sulla stessa linea, la corda era verde.
    sec(C_SOS, 'Soste', 'soste')
    S.append(_apre(
        _testata(5, 'Le soste: main e backup', 'lato tensione', C_SOS),
        P('Sul lato tensione si allestiscono <b>due soste indipendenti</b>, main e backup, con '
          'materiale di <b>colore diverso</b>: il colore serve a non confondere i due sistemi '
          'mentre si lavora in parete.', lead)))
    S.append(SP(12))
    S.append(photo_pair(
        str(FOTO / 'IMG_1357.jpg'), str(FOTO / 'IMG_1359.jpg'),
        'Esempio dalla 53 m: viola la main, rosa la backup', 'Il materiale disposto sulla roccia',
        *dim(FOTO / 'IMG_1357.jpg'), color=C_SOS, ratio=0.95, focus=0.5,
        ow2=dim(FOTO / 'IMG_1359.jpg')[0], oh2=dim(FOTO / 'IMG_1359.jpg')[1]))
    S.append(SP(14))
    S.append(KeepTogether([
        P('<b>Come si procede</b>', h3),
        SP(5),
        BU('Le due soste si allestiscono <b>in parallelo</b>: mentre una persona lavora sul '
           'lato tensione, un’altra raggiunge il lato statico per costruire la sosta di là.',
           C_SOS),
        BU('La backup si collega con un <b>connettore d’acciaio</b> — il BFK, il moschettone '
           'grande.', C_SOS)]))
    S.append(SP(18))
    # dubbio 37: la portata delle brache, il dato piu' pericoloso da sbagliare
    S.append(KeepTogether([
        P('<b>La portata delle brache</b>', h3),
        SP(4),
        P('La portata di una braca ad anello è quella stampata sull’etichetta cucita sulla '
          'calza. Se l’etichetta non si legge, la portata non è nota.', body),
        SP(10),
        callout('Il colore non è una portata',
                'Una calza viola con una riga scura sembra una portata dichiarata, ma non lo '
                'è: il colore sbiadisce al sole, le codifiche cambiano fra costruttori, e una '
                'riga cucita non è un’indicazione di portata. <b>Vale solo l’etichetta</b>.',
                WARN, '!', FW, True)]))
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
    # IMG_1350 @ 0:33-0:41 (la stessa corda per tagline e linea vita),
    # IMG_1378 @ 0:42 (backup e Grigri per chi lavora in sosta)
    sec(C_SOS, 'Linea vita', 'lineavita')
    S.append(_apre(
        _testata(7, 'Portare la linea, la linea vita', 'fra i due lati', C_SOS),
        P('Una corda porta la <b>tagline</b> da un lato all’altro, e poi resta come <b>linea '
          'vita</b> sulla sosta del lato statico: la stessa corda, due usi. Per chi lavora in '
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
    # IMG_1396. L'A-frame della 53 m, con le sue misure, sta nella sua scheda.
    sec(C_TEN, 'A-frame', 'aframe')
    S.append(_apre(
        _testata(9, 'L’A-frame', 'sul bordo', C_TEN),
        P('L’<b>A-frame</b> è un cavalletto di due pali incrociati e legati in testa, '
          'appoggiato sul bordo: la linea passa sopra la testa. Solleva la linea sopra il '
          'bordo, cambia l’angolo con cui carica la sosta e tiene il nastro lontano dalla '
          'roccia: non è un accessorio.', lead),
        SP(12),
        foto('IMG_1396.jpg', FW, 'Esempio dalla 53 m: la testa dei pali, con la fettuccia',
             C_TEN, ratio=0.56, focus=0.40)))
    S.append(SP(8))
    S.append(P('L’A-frame della 53 m — com’è fatto e che cosa manca — è descritto nella sua '
               'scheda.', small))
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
