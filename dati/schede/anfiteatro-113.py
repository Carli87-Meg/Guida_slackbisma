# -*- coding: utf-8 -*-
"""Scheda di Brifing, Anfiteatro 113 m (AN-7): linea fotografata.

Fonti: le otto fotografie del file LineeBisma (lavorazione/foto_linee/
anfiteatro-113/, lette il 27/10/2026 e riguardate per questa scheda), le parole
del file, il render i-pietra, il segmento SlackMap e la scheda SlackMap della
Brifing (dubbio 39: «barre filettate incollate chimicamente», scritta nel 2025;
che sia questa linea lo dice l'abbinamento del lotto 31 di i-pietra, 20/10/2026).
La sosta con il tronco sta anche sulla riga della 108 m (dubbio 59). Dubbi 39,
59, 60, 61, 68, 74.

Le fotografie 113_02, 113_03, 113_06 e 113_08 (persone riconoscibili, o al
limite) non si stampano.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-113',
    'occhiello': 'fotografata · 8 fotografie del gruppo',
    'intro': ('<b>Brifing</b> è il nome che la linea ha su SlackMap, con l’unica scheda di '
              'ancoraggi fra le ventiquattro della Pietra. Le fotografie del gruppo mostrano '
              'il cavalletto, in tre forme diverse e in almeno tre giornate, e la sosta con il '
              'tronco, che il file mette anche sulla riga della 108 m.'),
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
        'nota': 'La 113 m corre accanto alla 97 m. Quale capo sia il «vicino» del file, e '
                'quale il lato di tensione, non è noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Cavalletto di legno in tre forme: due pali tondi legati con corda verde '
                 '(estate), tre pali con fascia viola e rosa (autunno), due assi squadrate '
                 'legate con una braca viola (di notte)',
                 'Sotto l’incrocio un anello di fettuccia bianca e viola; fettucce bianca, '
                 'viola e gialla; brache viola, azzurre e bianche verso terra',
                 'Dalla cima una slinga verde a un connettore rosso, da cui parte la linea '
                 '(autunno)',
                 'Sotto la linea una seconda linea bianca a festoni: il backup? ' + DC,
                 'Punti fissi e ancoraggio a terra del cavalletto: non in inquadratura'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['La sosta con il tronco: tronco con la corteccia, imbottitura bianca e '
                 'tessuto rosso, legato con cordino viola',
                 'Due slinghe verdi tubolari sopra il tronco, verso la convergenza sul bordo',
                 'Una slinga su moschettone a ghiera e placchetta con dado; una braca viola '
                 'annodata su un altro elemento metallico nella roccia: numero e tipo dei '
                 'punti ' + DC,
                 'Calza grigia e rossa verso l’interno, fino a un connettore con cordino viola',
                 'Alla convergenza: calza lilla, braca azzurra, nastro verde lime, connettore '
                 'giallo-verde; da lì un nastro sottile bianco con bordo azzurro',
                 'Un albero con la chioma piena subito accanto'],
    },
    'lati_nota': ('Il file: «Bisma standard» per il «vicino», «Bisma standard senza cavalletto '
                  '+ tronco» per il «lontano». Su SlackMap la scheda della Brifing parla di '
                  'barre filettate incollate chimicamente: se siano i punti visti qui ' + DC
                  + '.'),

    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['vicino', 'Cavalletto: due pali tondi, oppure tre, oppure due assi squadrate', ''],
            ['vicino', 'Legature: corda verde; fascia viola e rosa; braca viola', ''],
            ['vicino', 'Anello di fettuccia bianca e viola sotto l’incrocio; fettucce bianca, '
                       'viola, gialla', ''],
            ['vicino', 'Brache ad anello viola, azzurre, bianche; corda grigia', ''],
            ['vicino', 'Slinga verde e connettore rosso in testa al cavalletto (autunno)', ''],
            ['lontano', 'Tronco con corteccia, imbottitura bianca, tessuto rosso, cordino '
                        'viola', ''],
            ['lontano', 'Due slinghe verdi tubolari (scritta scura, forse «2 t»: non va preso '
                        'per dato)', ''],
            ['lontano', 'Moschettone a ghiera su placchetta con dado', ''],
            ['lontano', 'Braca viola con etichetta azzurra illeggibile, su elemento metallico', ''],
            ['lontano', 'Corda in calza grigia e rossa; connettore con cordino viola', ''],
            ['lontano', 'Calza lilla, braca azzurra, nastro verde lime, matassa bianco-nera', ''],
        ],
        'nota': ('Riconosciuto per forma. Nessuna quantità e nessuna misura. Le scritte sulle '
                 'slinghe vanno fotografate distese prima di leggerci una portata.'),
    },

    'foto': [
        ('anfiteatro-113_01_vicino_cavalletto-e-linea-panorama.jpg',
         '«Vicino»: cavalletto a tre pali e la linea (autunno)',
         'anfiteatro-113_05_lontano_sosta-con-tronco-dettaglio.jpg',
         '«Lontano»: la sosta con il tronco e la placchetta', 0.66, 0.5),
        ('anfiteatro-113_07_lontano_sosta-con-tronco-bis.jpg',
         'La sosta dall’alto: slinghe, calza rossa, matassa',
         'anfiteatro-113_04_vicino_cavalletto-di-notte.jpg',
         'Il cavalletto di assi squadrate, di notte', 0.66, 0.5),
    ],

    'avvertenza': ('Una sosta, due linee',
                   'Fotografie diverse della stessa sosta con il tronco stanno sulla riga della '
                   '113 m e su quella della 108 m. Prima di attrezzare, chiedere a chi ha '
                   'compilato il file di quale linea è.'),

    'da_rilevare': [
        'Di quale linea è la sosta con il tronco: 113 m o 108 m.',
        'Quale lato è quello di tensione: nessuna foto mostra dove si tensiona.',
        'Numero e tipo dei punti fissi: placchette, barre resinate come dice SlackMap, altro.',
        'Che cosa fa il tronco; se l’albero accanto fa parte della sosta.',
        'Che cosa sono la seconda linea a festoni, la calza grigia e rossa, la matassa '
        'bianco-nera.',
        'Le scritte sulle slinghe verdi e l’etichetta della braca viola, da fotografare distese.',
        'Date e persone: almeno tre giornate diverse, nessuna foto ha i metadati.',
    ],
}
