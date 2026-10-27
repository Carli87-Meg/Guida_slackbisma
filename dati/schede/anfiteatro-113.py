# -*- coding: utf-8 -*-
"""Scheda di Brifing, Anfiteatro 113 m (AN-7): linea fotografata.

Fonti: le otto fotografie del file LineeBisma (lavorazione/foto_linee/
anfiteatro-113/, lette il 27/10/2026 e riguardate per questa scheda), le parole
del file, il render i-pietra, il segmento SlackMap e la scheda SlackMap della
Brifing (dubbio 39: «barre filettate incollate chimicamente», scritta nel 2025;
che sia questa linea lo dice l'abbinamento del lotto 31 di i-pietra, 20/10/2026).
La sosta con il tronco e' di questa linea: il file la metteva anche sulla riga della
108 m, e il 27/10/2026 l'utente ha detto che quelle foto sono della 113 (dubbi 59 e
63); ora sono 113_09-12. Dubbi 39, 60, 61, 68.

Le fotografie 113_02, 113_03, 113_06, 113_08, 113_10 e 113_12 (persone riconoscibili, o
al limite) non si stampano.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-113',
    'occhiello': 'fotografata · 12 fotografie del gruppo',
    'intro': ('<b>Brifing</b> è il nome che la linea ha su SlackMap, con l’unica scheda di '
              'ancoraggi fra le ventiquattro della Pietra. Le fotografie del gruppo mostrano '
              'il cavalletto, in tre forme diverse e in almeno tre giornate, e la sosta con il '
              'tronco.'),
    'chips': [('Lunghezza', '113 m · catalogo'),
              ('Tipologia', 'Highline · file'),
              ('Cavalletto', 'sì · «vicino»'),
              ('Altezza · SlackMap', '120 m'),
              ('Tensione', DR)],

    # render: la 113 m e' la linea gialla, la piu' lunga del render (843 px contro
    # i 776 della blu 97 m); l'etichetta «113m» sta sotto quella della 97 m come la
    # gialla sta sotto la blu. Capi per tinta 50-75°.
    'posizione': {
        'render': 'Anfiteatro',
        'estremi': ((399 / 1354, 273 / 884), (1242 / 1354, 528 / 884)),
        'ritaglio': (0.12, 0.18, 1.00, 0.70),
        'colore': (230, 230, 30),
        'didascalia': 'Dove corre la 113 m nella vista i-pietra dell’Anfiteatro: i due cerchi '
                      'sono i capi',
        'nota': 'La 113 m corre accanto alla 97 m. Quale capo sia il «vicino» del file non è '
                'noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Cavalletto di legno in tre forme: due pali tondi legati con corda verde '
                 '(estate), tre pali con fascia viola e rosa (autunno), due assi squadrate '
                 'legate con una braca viola (di notte)',
                 'Sotto l’incrocio un anello di fettuccia bianca e viola; fettucce bianca, '
                 'viola e gialla; brache viola, azzurre e bianche verso terra; una corda grigia',
                 'Dalla cima una slinga verde a un connettore rosso, da cui parte la linea '
                 '(autunno)',
                 'Sotto la linea una seconda linea bianca a festoni: il backup della linea',
                 'Punti fissi e ancoraggio a terra del cavalletto: non in inquadratura'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['La sosta con il tronco: tronco con la corteccia, imbottitura bianca e '
                 'tessuto rosso, legato con cordino viola',
                 'Due slinghe verdi tubolari sopra il tronco, verso la convergenza sul bordo; '
                 'su una una scritta scura, forse «2 t»: non va presa per un dato',
                 'Una slinga su moschettone a ghiera e placchetta con dado; una braca viola '
                 'con etichetta azzurra illeggibile, annodata su un altro elemento metallico '
                 'nella roccia: numero e tipo dei punti ' + DC,
                 'Calza grigia e rossa verso l’interno, fino a un connettore con cordino viola',
                 'Alla convergenza: calza lilla, braca azzurra, nastro verde lime, connettore '
                 'giallo-verde; da lì un nastro sottile bianco con bordo azzurro',
                 'Una matassa bianco-nera',
                 'Un albero con la chioma piena subito accanto'],
    },
    'lati_nota': ('Il file: «Bisma standard» per il «vicino», «Bisma standard senza cavalletto '
                  '+ tronco» per il «lontano». Su SlackMap la scheda della Brifing parla di '
                  'barre filettate incollate chimicamente: se siano i punti visti qui ' + DC
                  + '.'),

    'slackmap': True,
    'foto_dopo_lati': True,      # le foto subito sotto i lati che descrivono
    'file_gruppo': True,

    'foto': [
        ('anfiteatro-113_01_vicino_cavalletto-e-linea-panorama.jpg',
         '«Vicino»: cavalletto a tre pali e la linea (autunno)',
         'anfiteatro-113_05_lontano_sosta-con-tronco-dettaglio.jpg',
         '«Lontano»: la sosta con il tronco e la placchetta', 0.66, 0.5),
        ('anfiteatro-113_07_lontano_sosta-con-tronco-bis.jpg',
         'La sosta dall’alto: slinghe, calza rossa, matassa',
         'anfiteatro-113_04_vicino_cavalletto-di-notte.jpg',
         'Il cavalletto di assi squadrate, di notte', 0.66, 0.5),
        # dalla riga della 108 nel file (dubbi 59 e 63): 113_09 era 108_01, 113_11 era 108_03
        ('anfiteatro-113_09_lontano_sosta-con-tronco-verso-la-torre.jpg',
         '«Lontano»: la sosta con il tronco, verso la torre (estate)',
         'anfiteatro-113_11_lontano_sosta-con-tronco-altra-vista.jpg',
         'La stessa sosta: slinghe, placchetta, calza rossa', 0.66, 0.45),
    ],

    'da_rilevare': [
        'Quale lato è quello di tensione: nessuna foto mostra dove si tensiona.',
        'Numero e tipo dei punti fissi: placchette, barre resinate come dice SlackMap, altro.',
        'Che cosa fa il tronco; se l’albero accanto fa parte della sosta.',
        'Che cosa sono la calza grigia e rossa e la matassa bianco-nera.',
        'Le scritte sulle slinghe verdi e l’etichetta della braca viola, da fotografare distese.',
        'Date e persone: almeno tre giornate diverse, nessuna foto ha i metadati.',
    ],
}
