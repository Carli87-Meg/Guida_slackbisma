# -*- coding: utf-8 -*-
"""Scheda di La lenza, Despedida 70 m (DE-4): linea fotografata.

Fonti: le tre fotografie del file LineeBisma (lavorazione/foto_linee/
despedida-70/, lette il 27/10/2026 e riguardate per questa scheda), la tipologia
del file (che per questa linea non ha altro), il render i-pietra e il segmento
SlackMap. La foto del lato «vicino» era della 53 m (utente, 27/10/2026, dubbio 66):
ora e' la 53_04. Dubbi 60, 66.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'despedida-70',
    'occhiello': 'fotografata · 3 fotografie del gruppo',
    'intro': ('<b>La lenza</b> è il nome che la linea ha su SlackMap. Le fotografie del gruppo '
              'mostrano un capo solo, il «lontano» del file, d’autunno: un cavalletto di tre '
              'pali e la sosta sul bordo. Il lato di tensione non è dichiarato.'),
    'chips': [('Lunghezza', '70 m · catalogo'),
              ('Tipologia · file', 'Freestyle/Highline'),
              ('Cavalletto', '3 pali · «lontano»'),
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
                '«vicino» del file non è noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Nessuna foto: quella che il file metteva qui è della 53 m dell’Anfiteatro'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['Cavalletto di tre pali tondi legati in cima con una slinga rossa (autunno)',
                 'Due slinghe verdi tubolari (su una, una scritta: forse «GIBBON») che '
                 'convergono in un nodo di cordino grigio; da lì una '
                 'corda chiara doppia verso l’interno: ancorata a che cosa ' + DC,
                 'Una slinga verde su una protezione tubolare bianca che gira attorno a un '
                 'masso sul bordo e arriva alla base di un alberello: chiusa su quale dei due '
                 + DC,
                 'Fettucce gialla e azzurra, corda grigia a matassa',
                 'Sulla linea, vicino al cavalletto, un tratto in calza rossa',
                 'Punti su roccia: nessuno visibile'],
    },
    'lati_nota': ('Per la 70 m il file ha solo la tipologia: nessuno schema, nessuna nota.'),

    'slackmap': True,
    'foto_dopo_lati': True,      # le foto subito sotto i lati che descrivono
    'file_gruppo': True,

    'foto': [
        ('despedida-70_02_lontano_cavalletto-e-linea.jpg',
         '«Lontano»: cavalletto di tre pali, nebbia (autunno)',
         'despedida-70_03_lontano_sosta-sul-bordo.jpg',
         'Le slinghe verdi annodate alla corda doppia', 0.66, 0.5),
        {'file': 'despedida-70_04_lontano_slinga-al-bordo.jpg',
         'cap': 'La protezione bianca attorno al masso', 'ratio': 0.5, 'focus': 0.5},
    ],

    'da_rilevare': [
        'Il lato «vicino» del file: nessuna foto, nessuna nota.',
        'Quale lato è quello di tensione.',
        'A che cosa è ancorata la corda doppia; che cosa c’è sotto la protezione bianca e su '
        'che cosa è chiusa: il masso, l’alberello o entrambi.',
        'Se ci sono punti fissi su roccia.',
        'Date e persone: nessuna foto ha i metadati.',
    ],
}
