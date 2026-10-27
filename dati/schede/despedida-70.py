# -*- coding: utf-8 -*-
"""Scheda di La lenza, Despedida 70 m (DE-4): linea fotografata.

Fonti: le quattro fotografie del file LineeBisma (lavorazione/foto_linee/
despedida-70/, lette il 27/10/2026 e riguardate per questa scheda), la tipologia
del file (che per questa linea non ha altro), il render i-pietra e il segmento
SlackMap. Dubbi 60, 66.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'despedida-70',
    'occhiello': 'fotografata · 4 fotografie del gruppo',
    'intro': ('<b>La lenza</b> è il nome che la linea ha su SlackMap. Le fotografie del gruppo '
              'mostrano un cavalletto su tutti e due i lati del file, in due stagioni e di '
              'forma diversa: se la linea abbia davvero un cavalletto a ciascun capo non si '
              'ricava dalle immagini. Il lato di tensione non è dichiarato.'),
    'chips': [('Lunghezza', '70 m · catalogo'),
              ('Tipologia · file', 'Freestyle/Highline'),
              ('Cavalletto', 'uno o due capi?'),
              ('Ancoraggio', 'masso, alberello?'),
              ('Tensione', DR)],

    # render della Despedida: la 70 m e' la linea gialla, la piu' lunga delle quattro
    # corte del pilastro (283 px); l'etichetta «Despedida 70m» sta sotto il suo capo.
    # Capi per tinta 45-75° nel riquadro del pilastro.
    'posizione': {
        'render': 'Despedida',
        'estremi': ((830 / 1526, 497 / 920), (1083 / 1526, 628 / 920)),
        'ritaglio': (0.46, 0.44, 0.84, 0.76),
        'colore': (230, 220, 40),
        'didascalia': 'Dove corre la 70 m nella vista i-pietra della Despedida: i due cerchi '
                      'sono i capi',
        'nota': 'La 70 m corre accanto alla 60 m, dallo stesso pilastro. Quale capo sia il '
                '«vicino» del file, e quale il lato di tensione, non è noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Cavalletto di due pali tondi, legati in cima con corda color canapa e più in '
                 'basso con una fettuccia bianca e rossa (estate)',
                 'Slinga verde acqua, fettuccia bianca, cordino verde, corda bianca',
                 'La linea, bianca con tratti scuri, verso una cima boscosa',
                 'Punti e ancoraggio a terra: non in inquadratura'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['Cavalletto di tre pali tondi legati in cima con una slinga rossa (autunno)',
                 'Due slinghe verdi che convergono in un nodo di cordino grigio; da lì una '
                 'corda chiara doppia verso l’interno: ancorata a che cosa ' + DC,
                 'Una slinga verde su una protezione tubolare bianca che gira attorno a un '
                 'masso sul bordo e arriva alla base di un alberello: chiusa su quale dei due '
                 + DC,
                 'Fettucce gialla e azzurra, corda grigia a matassa',
                 'Sulla linea, vicino al cavalletto, un tratto in calza rossa',
                 'Punti su roccia: nessuno visibile'],
    },
    'lati_nota': ('Per la 70 m il file ha solo la tipologia: nessuno schema, nessuna nota. Le '
                  'foto dei due lati sono di stagioni diverse: potrebbero essere dello stesso '
                  'capo in due giornate, o di linee diverse.'),

    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['vicino', 'Cavalletto di due pali tondi; legature in corda color canapa e '
                       'fettuccia bianca e rossa', ''],
            ['vicino', 'Slinga verde acqua, fettuccia bianca, cordino verde, corda bianca', ''],
            ['lontano', 'Cavalletto di tre pali tondi; legatura con slinga rossa', ''],
            ['lontano', 'Slinghe verdi tubolari (su una, una scritta: forse «GIBBON»)', ''],
            ['lontano', 'Nodo di cordino grigio su una corda chiara doppia', ''],
            ['lontano', 'Protezione tubolare bianca attorno a un masso, fino a un alberello', ''],
            ['lontano', 'Fettucce gialla e azzurra; corda grigia a matassa', ''],
            ['lontano', 'Tratto in calza rossa sulla linea, vicino al cavalletto', ''],
        ],
        'nota': 'Riconosciuto per forma. Nessuna quantità e nessuna misura.',
    },

    'foto': [
        ('despedida-70_01_vicino_cavalletto-e-linea.jpg',
         '«Vicino»: cavalletto di due pali e la linea (estate)',
         'despedida-70_02_lontano_cavalletto-e-linea.jpg',
         '«Lontano»: cavalletto di tre pali, nebbia (autunno)', 0.66, 0.5),
        ('despedida-70_03_lontano_sosta-sul-bordo.jpg',
         'Le slinghe verdi annodate alla corda doppia',
         'despedida-70_04_lontano_slinga-al-bordo.jpg',
         'La protezione bianca attorno al masso', 0.66, 0.5),
    ],

    'da_rilevare': [
        'Se c’è un cavalletto a tutti e due i capi, o se le due foto sono dello stesso capo.',
        'Quale lato è quello di tensione.',
        'A che cosa è ancorata la corda doppia; che cosa c’è sotto la protezione bianca e su '
        'che cosa è chiusa: il masso, l’alberello o entrambi.',
        'Se ci sono punti fissi su roccia.',
        'Date e persone: nessuna foto ha i metadati.',
    ],
}
