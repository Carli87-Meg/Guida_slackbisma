# -*- coding: utf-8 -*-
"""Scheda di Il saso, Despedida 60 m (DE-3): linea fotografata.

Fonti: le sei fotografie del file LineeBisma (lavorazione/foto_linee/despedida-60/,
lette il 27/10/2026 e riguardate per questa scheda), la tipologia del file (che
per questa linea non ha altro), il render i-pietra e il segmento SlackMap. Tutte
le foto stanno nella colonna «lontano» del file. Dubbi 60, 67.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'despedida-60',
    'occhiello': 'fotografata · 6 fotografie del gruppo',
    'intro': ('<b>Il saso</b> è il nome che la linea ha su SlackMap. Le fotografie del gruppo '
              'mostrano un capo solo, d’autunno, con una fettuccia Gibbon attorno a un albero '
              'e un tronco sottile in piedi sul bordo: che l’ancoraggio sia sugli alberi non '
              'è dimostrato. Il lato di tensione non è dichiarato.'),
    'chips': [('Lunghezza', '60 m · catalogo'),
              ('Tipologia', 'Freestyle · file'),
              ('Ancoraggio', 'alberi?'),
              ('Cavalletto', 'bastoni?'),
              ('Tensione', DR)],

    # render della Despedida: la 60 m e' la linea verde; distinta dalla 70 m gialla
    # per l'etichetta («Despedida 60m» accanto al capo verde) e per la lunghezza sul
    # render (272 px contro 283). Capi per tinta 95-140° nel riquadro del pilastro.
    'posizione': {
        'render': 'Despedida',
        'estremi': ((847 / 1526, 499 / 920), (1094 / 1526, 612 / 920)),
        'ritaglio': (0.46, 0.44, 0.84, 0.76),
        'colore': (60, 200, 60),
        'didascalia': 'Dove corre la 60 m nella vista i-pietra della Despedida: i due cerchi '
                      'sono i capi',
        'nota': 'Le quattro linee corte della Despedida partono dallo stesso pilastro e si '
                'aprono a ventaglio; la 60 m e la 70 m corrono vicine. Quale capo sia quello '
                'fotografato non è noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Nessuna fotografia, nessuna nota nel file'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['Una fettuccia piatta nera «GIBBON» che gira attorno alla base di un albero '
                 'grosso e, al bordo, passa accanto a tre moschettoni a ghiera: se sia una '
                 'sola, e dove finisca ' + DC,
                 'Una corda arancione annodata attorno allo stesso albero',
                 'Sul bordo un tronco sottile in piedi, con una protezione azzurra a fantasia, '
                 'una slinga verde lime e la corda arancione',
                 'Accanto, un tronco inclinato e due o tre bastoni sottili incrociati in alto: '
                 'un cavalletto? ' + DC,
                 'Tre moschettoni a ghiera (azzurro, arancione, argento) e una fettuccia rosa',
                 'Punti su roccia: nessuno visibile'],
    },
    'lati_nota': ('Per la 60 m il file ha solo la tipologia: nessuno schema, nessuna nota. La '
                  'linea con l’highliner nella nebbia della prima foto potrebbe essere la 70 m: '
                  'è la stessa scena della foto d’autunno di quella linea.'),

    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['lontano', 'Fettuccia piatta nera con scritta gialla', 'GIBBON'],
            ['lontano', 'Protezioni sulla fettuccia: una verde alla base dell’albero, una rossa '
                        'legata con laccio verde', ''],
            ['lontano', 'Corda arancione annodata all’albero e al tronco in piedi', ''],
            ['lontano', 'Corda verde-azzurra doppia; cordino bianco con tratti verdi', ''],
            ['lontano', 'Slinga verde lime sul tronco in piedi', ''],
            ['lontano', 'Protezione azzurra a fantasia sul tronco in piedi', 'solo «…INB…»'],
            ['lontano', 'Tre moschettoni a ghiera: azzurro, arancione, argento; fettuccia rosa', ''],
            ['lontano', 'Tronco inclinato e bastoni sottili incrociati, uno chiaro con adesivi '
                        + DC, ''],
        ],
        'nota': 'Riconosciuto per forma, salvo la fettuccia. Nessuna quantità e nessuna misura.',
    },

    'foto': [
        ('despedida-60_02_lontano_tronco-con-corde-e-fettuccia.jpg',
         '«Lontano»: tronco in piedi, fettuccia Gibbon, moschettoni',
         'despedida-60_06_lontano_fettuccia-alla-base-dell-albero.jpg',
         'La fettuccia Gibbon alla base dell’albero', 0.66, 0.5),
        ('despedida-60_01_lontano_linea-nella-nebbia.jpg',
         'La sosta sul bordo; nella nebbia, un highliner',
         'despedida-60_05_lontano_fettuccia-a-terra.jpg',
         'La fettuccia Gibbon a terra, protezione rossa', 0.66, 0.5),
    ],

    'da_rilevare': [
        'Quale lato è quello di tensione.',
        'Se l’ancoraggio è sugli alberi: quanti, e come; se la fettuccia Gibbon è una sola e '
        'che cosa fa; che cosa fa la corda arancione annodata all’albero.',
        'Se il tronco inclinato e i bastoni sono un cavalletto, e di che materiale.',
        'Il lato «vicino»: nessuna foto, nessuna nota.',
        'Se la linea con l’highliner nella nebbia è la 60 m o la 70 m.',
        'Date e persone: nessuna foto ha i metadati.',
    ],
}
