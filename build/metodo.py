# -*- coding: utf-8 -*-
"""Parte 3 della guida: come si monta una linea alla Pietra, il metodo Bisma.

Sei capitoli, ordinati come si esegue: lo schema e la sequenza, il materiale, i
punti su roccia, le due soste del lato tensione, la tensione con l'A-frame, e
cio' che il metodo non copre ancora. Fino all'edizione 0.3 erano dieci, tre dei
quali di poche righe.

Il criterio che separa questa parte dalla scheda di una linea, lo stesso della
guida Sillschlucht di Innsbruck: **qui si dice come si fa** — funzioni, tipi di
materiale, principi. **La scheda dice com'e' fatta quella linea**: quantita',
colori, numero di punti, posizioni, che cosa manca. Le fotografie della 53 m
compaiono qui solo come esempi, e la didascalia lo dichiara.

Le fonti: il montaggio della 53 m dell'Anfiteatro (trascrizioni e fotogrammi,
NOTE_RIGGING.md, sezioni A-G), il montaggio con i bungee del 22/08/2026, le
risposte di chi ha montato e la scheda «Ancoraggio Standard Bisma» del file del
gruppo, stampata con le sue parole e «da controllare». I riferimenti ai file
stanno nei commenti, non nel testo per il lettore.

Dall'edizione 0.4 (decisione C dell'utente) il metodo non contiene piu' regole
generiche di highlining messe a colmare un vuoto: la checklist dei controlli sul
punto, il confronto fra spit, tasselli e resinati e la spiegazione di che cosa fa
l'A-frame non venivano dal gruppo e sono usciti. Al loro posto, nel capitolo 6,
la domanda da fare a chi monta.

    from metodo import parte_metodo
"""
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / 'build'))
sys.path.insert(0, str(RADICE / 'dati'))

from design import *                                                # noqa: E402,F403
from reportlab.platypus import KeepTogether, PageBreak              # noqa: E402
from scheda_linea import (foto, coppia, dim, ANN, FOTO, C_TEN, C_STA,   # noqa: E402
                          C_MET, T, BUm, marca)
import linee as REG                                                 # noqa: E402
import file_lineebisma as FC                                        # noqa: E402

LINEA_53 = REG.di('anfiteatro-53')


def _apre(testata, *seguito, marcatori=()):
    """Testata legata al suo primo blocco: non resta mai sola in fondo pagina."""
    return KeepTogether(list(marcatori) + [testata, SP(10)] + list(seguito))


def _marcatori(etichetta, chiave):
    """Accento e rimando di una sezione, dentro il blocco che la apre.

    Lasciati fuori restano in fondo alla pagina prima, e l'indice stampa il
    capitolo una pagina prima di dove comincia.
    """
    return [Accent(C_MET, etichetta), Segna(chiave)]


def _testata(n, titolo, occhiello):
    return LineHeader(str(n), titolo, 'Come si monta · %s' % occhiello, C_MET)


def _h3(t):
    return P('<b>%s</b>' % t, h3)


def _virgolette(t):
    return '«%s»' % t if t else '—'


def tabella_scheda_sosta():
    """La scheda «Sosta Bisma Standard» del file, blocco per blocco, con le sue parole.

    Si stampano le celle; cio' che la scheda lascia aperto si dice sotto, con
    [DA CONFERMARE]. Nessuna equivalenza con il materiale della guida: quella fu
    stampata una volta per deduzione, ed e' stata tolta (dubbio 72).
    """
    righe = []
    for blocco, celle in FC.SCHEDA_SOSTA:
        voci = [' '.join(_virgolette(x) for x in riga) for riga in celle]
        righe.append([Paragraph('<b>%s</b>' % blocco, td),
                      Paragraph(' · '.join(voci), td)])
    t = data_table(['Blocco del file', 'Celle, con le parole del file'],
                   righe, [118, FW - 118], color=C_MET)
    # righe strette: cosi' lo schema sta sotto la tabella del materiale, e il capitolo 3
    # tiene sulla sua pagina la fotografia della sosta
    t.setStyle(TableStyle([('TOPPADDING', (0, 1), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 4)]))
    return t


def parte_metodo():
    S = []

    # ============================================================ 1 · lo schema
    # Ruoli dei due lati dall'ordine delle operazioni (NOTE_RIGGING A, D, E, F).
    # Sequenza dai metadati dei file, NOTE_RIGGING A-G. Tagline e linea vita:
    # IMG_1350 @ 0:33-0:41; backup e Grigri per chi lavora in sosta: IMG_1378 @ 0:42.
    # Smontaggio: nessuna ripresa (dubbio 35).
    S.append(_apre(
        _testata(1, 'Lo schema e la sequenza', 'due lati, dodici passi'),
        P('Una linea ha due ancoraggi, con compiti diversi. Sul <b>lato tensione</b> si '
          'costruiscono due soste indipendenti, main e backup, e si tensiona la linea. Sul '
          '<b>lato statico</b> c’è una sosta su più punti a cui la linea arriva.', lead),
        marcatori=_marcatori('Lo schema', 'm1')))
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
            marca('Sosta backup: com’è fatta, da rilevare'),
        ], C_STA)))
    S.append(SP(8))
    S.append(P('Com’è fatto ciascun lato su una linea precisa — quanti punti, quale materiale, '
               'dove si trova — lo dice la sua scheda, nella parte 2.', small))
    S.append(SP(18))
    # Steps disegna testo semplice: niente markup nelle descrizioni
    S.append(KeepTogether([
        _h3('La sequenza'),
        SP(4),
        P('Le fasi nell’ordine in cui si eseguono. Ognuna è descritta nei capitoli che '
          'seguono.', body),
        SP(10),
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
            ('Tensionare', 'Tensionamento finale: come e quanto, da rilevare'),
            ('Anti-slip', 'Sulla linea, a tensione fatta'),
            ('Verificare', 'Si va sulla linea per vedere se va ritensionata'),
            ('Smontare', 'La sequenza di smontaggio non è documentata: da rilevare'),
        ], C_MET, FW, 2)]))
    S.append(SP(18))
    S.append(KeepTogether([
        _h3('Portare la linea, la linea vita'),
        SP(4),
        P('Una corda porta la <b>tagline</b> da un lato all’altro, e poi resta come <b>linea '
          'vita</b> sulla sosta del lato statico: la stessa corda, due usi. Per chi lavora in '
          'sosta servono una <b>corda di backup</b> e un <b>Grigri</b>.', body),
        SP(5),
        T('Come si porta la tagline da un lato all’altro: da rilevare.', small)]))
    S.append(SP(26))

    # ============================================================ 2 · il materiale
    # Le voci sono quelle del materiale nominato (NOTE_RIGGING), raggruppate per
    # funzione. Quantita' e misure stanno nella scheda della linea.
    # Placchette: il file LineeBisma le mette «da portare», la scheda della 53 m le
    # vede sui punti (dubbio 70). Carrucola: vista sull'ancoraggio (IMG_1371),
    # funzione mai detta (dubbio 40).
    S.append(_apre(
        _testata(2, 'Il materiale', 'che cosa serve'),
        P('Che cosa serve per montare una linea, voce per voce, nell’ordine del metodo. '
          'Quantità e misure dipendono dalla linea: le dà la sua scheda.', lead),
        marcatori=_marcatori('Il materiale', 'm2')))
    S.append(SP(12))
    righe = [
        ['I punti', 'Placchette: sulla 53 m oggi montate in loco; sulle altre linee da rilevare'],
        ['La sosta main', 'Brache ad anello industriali («slinghe»)'],
        ['La sosta backup', 'Corde, chiuse con un nodo, il «BFK» [DA CONFERMARE]'],
        ['Collegare i punti', 'Una corda, annodata fra i punti'],
        ['Sull’ancoraggio', 'Carrucola bloccante — vista sull’ancoraggio statico della 53 m; '
                            'funzione [DA CONFERMARE]'],
        ['I collegamenti della sosta', 'Grilli a lira; maglie rapide (dove si usano, da rilevare)'],
        ['La tensione', 'Weblock e paranchino; softrelease (dove si usa, da rilevare)'],
        ['Portare la linea', 'Tagline, e una corda che poi fa da linea vita'],
        ['Chi lavora in sosta', 'Corda di backup e Grigri'],
        ['La linea', 'Nastro, backup della linea, leash (marca e tipo, da rilevare)'],
        ['Il bordo', 'A-frame, se la linea lo prevede'],
    ]
    S.append(data_table(['Per', 'Che cosa serve'],
                        [[Paragraph(a, td), Paragraph(marca(b), td)] for a, b in righe],
                        [150, FW - 150], C_MET))
    S.append(SP(8))
    S.append(P('L’elenco di GAS-OH, la 53 m dell’Anfiteatro, con le quantità, è a '
               + rif('materiale:anfiteatro-53', 'pagina [rimando]') + '.', small))
    S.append(SP(12))
    # Lo schema del gruppo: la scheda «Sosta Bisma Standard» del file LineeBisma
    # (20/10/2026). Decisione D6: diventa una fonte dopo il controllo con chi l'ha
    # compilato, non ancora avvenuto. Le ambiguita': dubbi 70, 71, 72.
    # titolo, paragrafo e tabella insieme: spezzata, la tabella lasciava una riga
    # sola in cima alla pagina dopo. Le note possono seguire da sole.
    S.append(KeepTogether([
        _h3('Lo schema del gruppo: «Ancoraggio standard Bisma»'),
        SP(4),
        P('Il file del gruppo descrive una sosta tipo, che chiama <b>«Ancoraggio Standard '
          'Bisma»</b> e che assegna, con il nome «Bisma standard», ai lati di cinque linee. È '
          'una proposta che il file stesso segna <b>«da controllare»</b>, non un rilievo: si '
          'stampa con le sue parole finché chi l’ha compilato non la conferma. Che lo schema '
          'delle righe sia questa scheda lo dice solo il nome.', body),
        SP(8),
        tabella_scheda_sosta()]))
    S.append(SP(5))
    sx = ParagraphStyle('dcs', parent=small, alignment=0)
    S += [T(t, sx) for t in FC.SCHEDA_SOSTA_DA_CONFERMARE]
    S.append(SP(26))

    # ============================================================ 3 · i punti
    # Roccia dalla scheda di settore i-pietra; placchette in IMG_1371, IMG_1372 e
    # nelle foto del 22/08; punti collegati con corda annodata in entrambi i montaggi.
    S.append(_apre(
        _testata(3, 'I punti su roccia', 'gli ancoraggi'),
        P('La roccia della Pietra è <b>arenaria</b>. I punti visti sulla 53 m sono '
          '<b>placchette metalliche fissate con un dado esagonale su bullone</b>: non uno '
          'spit a vite né un resinato con occhiello. Se il bullone sia un tassello meccanico '
          'o una barra resinata non è noto. La sosta si costruisce su <b>più punti</b>, '
          'collegati fra loro con una corda annodata.', lead),
        marcatori=_marcatori('I punti', 'm3')))
    # la fotografia segue da sola: legata alla testata, il capitolo saltava pagina
    # e lasciava mezza pagina vuota dietro di se'
    S.append(SP(12))
    S.append(foto('D1_ancoraggio.jpg', FW, 'Esempio dalla 53 m: sosta su tre punti — '
                  'placchetta, cordino di collegamento, carrucola bloccante, slinga', C_MET,
                  ratio=0.72, focus=0.78))
    S.append(SP(14))
    S.append(_apre(
        _h3('Il punto da vicino'),
        foto('D2_placchetta_dettaglio.jpg', FW, 'Placchetta e dado esagonale', C_MET,
             ratio=0.50, focus=0.55)))
    S.append(SP(10))
    S.append(T('Quali controlli il gruppo fa su un punto prima di caricarlo, e che cosa '
               'guarda nella roccia attorno al foro: da rilevare (capitolo 6).', small))
    S.append(SP(26))

    # ============================================================ 4 · le due soste
    # IMG_1349 @ 0:00, IMG_1350 @ 0:00 (colori); IMG_1366, IMG_1367 @ 0:43 (il
    # perche' del nodo), IMG_1369 (verso di lavoro). Portata: dubbio 37.
    S.append(_apre(
        _testata(4, 'Le due soste del lato tensione', 'main e backup'),
        P('Sul lato tensione si allestiscono <b>due soste indipendenti</b>, main e backup, con '
          'materiale di <b>colore diverso</b>: il colore serve a non confondere i due sistemi '
          'mentre si lavora in parete.', lead),
        marcatori=_marcatori('Le soste', 'm4')))
    S.append(SP(12))
    S.append(coppia('IMG_1357.jpg', 'Esempio dalla 53 m: viola la main, rosa la backup',
                    'IMG_1359.jpg', 'Il materiale disposto sulla roccia',
                    ratio=0.95, focus=0.5, color=C_MET))
    S.append(SP(14))
    S.append(KeepTogether([
        _h3('Come si procede'),
        SP(5),
        BU('Le due soste si allestiscono <b>in parallelo</b>: mentre una persona lavora sul '
           'lato tensione, un’altra raggiunge il lato statico per costruire la sosta di là.',
           C_MET),
        BU(marca('La backup si chiude con il <b>BFK</b>, il nodo fatto con la corda di backup '
                 '[DA CONFERMARE].'), C_MET),
        BU('Il colore è un principio, non una convenzione fissa: il 22 agosto, sulla stessa '
           'linea, la corda fra i punti era verde.', C_MET)]))
    S.append(SP(18))
    S.append(KeepTogether([
        _h3('La portata delle brache'),
        SP(4),
        P('La portata di una braca ad anello è quella stampata sull’etichetta cucita sulla '
          'calza. Se l’etichetta non si legge, la portata non è nota.', body),
        SP(10),
        callout('Il colore non è una portata',
                # le due ragioni di prima (colore che sbiadisce, codifiche dei costruttori)
                # erano conoscenza generica, senza fonte: tolte il 27/10/2026
                'Una calza viola con una riga scura sembra una portata dichiarata, ma non lo '
                'è. <b>Vale solo l’etichetta</b> cucita sulla calza.',
                WARN, '!', FW, True)]))
    S.append(SP(18))
    S.append(_apre(
        _h3('Instradamento della slinga'),
        P('La slinga passa nell’anello d’acciaio e si ferma con un nodo che serve a '
          '<b>forzare la slinga</b>: chi lo usa lo sceglie perché la tenuta è sufficiente ed '
          'è veloce da regolare. Poi le slinghe si orientano nel <b>verso in cui lavorano</b>, '
          'senza torsioni, e si ingrillano.', body),
        SP(10),
        photo_row([
            (str(ANN / 'B1_slinga_aperta.jpg'),) + dim(ANN / 'B1_slinga_aperta.jpg')
            + ('1 · slinga aperta',),
            (str(ANN / 'B2_passaggio_anello.jpg'),) + dim(ANN / 'B2_passaggio_anello.jpg')
            + ('2 · nell’anello',),
            (str(ANN / 'B3_giro_chiuso.jpg'),) + dim(ANN / 'B3_giro_chiuso.jpg')
            + ('3 · giro chiuso',),
        ], C_MET),
        SP(8),
        T('Come si chiama il nodo, e quali alternative sono accettabili: da rilevare.', small)))
    S.append(SP(26))

    # ============================================================ 5 · tensione e A-frame
    # IMG_1380, 1381, 1383 (pretensione), IMG_1384 @ 0:00-0:55 (blocco backup),
    # IMG_1392 (tensione finale), IMG_1394 (softrelease), IMG_1395 (anti-slip).
    # A-frame: IMG_1396, IMG_1416; le sue misure stanno nella scheda della 53 m.
    S.append(_apre(
        _testata(5, 'Tensione, blocco del backup, anti-slip', 'e l’A-frame'),
        P('La linea passa nel <b>weblock</b> — in gergo «banana» — collegato con un grillo '
          'a lira. Si pretensiona con il <b>paranchino di tensionamento della base</b>. Poi '
          'si <b>blocca il backup</b>: un collegamento che prende sia la sosta main sia la '
          'sosta backup e si chiude sul grillo. Dopo il tensionamento finale si aggiunge '
          'l’<b>anti-slip</b>, un nodo sulla linea che impedisce che slitti nel weblock.',
          lead),
        SP(10),
        ChipRow([('Bloccante', 'Weblock'), ('Collegamento', 'Grillo a lira'),
                 ('Tensione', 'Paranchino'), ('Sicura', 'Anti-slip')], C_MET),
        marcatori=_marcatori('La tensione', 'm5')))
    S.append(SP(12))
    S.append(coppia('F1_weblock_grillo.jpg', 'Weblock e grillo a lira',
                    'G1_antislip.jpg', 'L’anti-slip sulla linea', color=C_MET))
    S.append(SP(16))
    S.append(_apre(
        _h3('L’A-frame'),
        P('L’<b>A-frame</b> è un cavalletto di due pali incrociati e legati in testa, '
          'appoggiato sul bordo: la linea passa sulla testa dei pali. Sulla 53 m sta sul lato '
          'tensione; il file del gruppo lo chiama «cavalletto» e lo mette fra il materiale da '
          'portare.', body),
        SP(10),
        # ratio 0.42: cosi' il capitolo 6 entra sotto, invece di lasciare mezza pagina vuota
        foto('IMG_1396.jpg', FW, 'Esempio dalla 53 m: la testa dei pali, con la fettuccia',
             C_MET, ratio=0.42, focus=0.40),
        SP(6),
        P('L’A-frame della 53 m — com’è fatto e che cosa manca — è descritto nella sua '
          'scheda, a %s.' % rif('linea:anfiteatro-53'), small)))
    S.append(SP(26))

    # ============================================================ 6 · che cosa manca
    # Una lista sola al posto delle liste sparse nei capitoli e del riquadro «Due
    # avvertenze da chiarire» (dubbi 29 e 30), che diceva al lettore che qualcosa
    # puo' cadere senza dire che cosa. Dubbi: 20, 25-27, 31-36, 41, 18.
    S.append(_apre(
        _testata(6, 'Che cosa il metodo non copre ancora', 'da chiedere a chi monta'),
        P('Il metodo è ricavato da un montaggio solo, ripreso senza intento didattico, e dalla '
          'scheda del gruppo ancora da controllare. Queste sono le cose che un’edizione '
          'successiva deve aggiungere, con le risposte di chi monta.', lead),
        SP(10),
        BU('Il nodo che forza la slinga: come si chiama, quali alternative sono accettabili.',
           C_MET),
        BU('Come si collegano ed equalizzano i punti di una sosta, e con quale angolo di '
           'apertura.', C_MET),
        BU('Quali controlli si fanno su un punto e sulla roccia attorno prima di caricarlo.',
           C_MET),
        BU('Come si porta la tagline da un lato all’altro.', C_MET),
        BU('Com’è fatto il paranchino di tensionamento della base, e come si fa il '
           'tensionamento finale: quanta tensione, come si misura.', C_MET),
        BU('Com’è fatto il blocco del backup, e l’anti-slip: nodo, materiale, punto esatto.',
           C_MET),
        BU('Dove sta il softrelease nel sistema, e quale modello.', C_MET),
        BU('La sosta backup del lato statico: se c’è sempre, e com’è fatta.', C_MET),
        BU('La sequenza di smontaggio.', C_MET),
        BU('Due avvertenze dette durante il montaggio restano senza oggetto: un componente '
           'che «ruotando può cadere» e un’operazione che «andrebbe fatta dopo, quando c’è del '
           'peso». Quale componente e quale operazione.', C_MET),
        BU('La checklist che il gruppo usa prima di uscire e prima di salire sulla linea.',
           C_MET),
        SP(10),
        P('L’elenco completo dei dubbi, con la fonte di ciascuno, è nella scheda dei dubbi '
          'che accompagna la guida, da compilare con chi ha montato.', small),
        marcatori=_marcatori('Che cosa manca', 'm6')))
    S.append(PageBreak())
    return S
