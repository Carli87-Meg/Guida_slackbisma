# -*- coding: utf-8 -*-
"""Scheda di 420, Anfiteatro 97 m (AN-5): linea fotografata.

Fonti: le tre fotografie del file LineeBisma (lavorazione/foto_linee/anfiteatro-97/,
lette il 27/10/2026 e riguardate per questa scheda), le parole del file (che la
chiama «91»: dubbio 62), il render i-pietra e il segmento SlackMap. Il lato di
tensione non e' dichiarato. Dubbi 60, 62, 69.

La fotografia 97_03 (un volto riconoscibile) non si stampa.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-97',
    'occhiello': 'fotografata · 3 fotografie del gruppo',
    'intro': ('<b>420</b> è il nome che la linea ha su SlackMap. Il file del gruppo la chiama '
              '«91»: è stata messa sulla 97 m per la posizione nell’elenco, e che sia la '
              'stessa linea resta da confermare. Le fotografie mostrano un capo fra gli '
              'alberi, d’autunno; il lato di tensione non è dichiarato.'),
    'chips': [('Lunghezza', '97 m · catalogo'),
              ('Tipologia', 'Highline · file'),
              ('Cavalletto', 'fra alberi · file'),
              ('Ancoraggio', 'alberi, roccia?'),
              ('Tensione', DR)],

    # render: la 97 m e' la linea blu; distinta dalla 113 m gialla per l'etichetta
    # («Anfiteatro – 97m» sta sopra «113m», come la linea blu sta sopra la gialla)
    # e per la lunghezza sul render (776 px contro 843). Capi per tinta 215-250°.
    'posizione': {
        'render': 'Anfiteatro',
        'estremi': ((456 / 1354, 280 / 884), (1232 / 1354, 509 / 884)),
        'ritaglio': (0.14, 0.18, 1.00, 0.70),
        'colore': (47, 60, 230),
        'didascalia': 'Dove corre la 97 m nella vista i-pietra dell’Anfiteatro: i due cerchi '
                      'sono i capi',
        'nota': 'La 97 m corre accanto alla 113 m, sulla stessa parete. Quale capo sia il '
                '«vicino» del file, e quale il lato di tensione, non è noto.',
    },

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Nessuna fotografia leggibile: l’unica è in controluce e non si stampa',
                 'Il file: schema «Bisma standard senza cavalletto»'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['Due brache viola, una larga e una stretta, fra i tronchi, riunite da un '
                 'grillo a lira',
                 'Un moschettone su un elemento metallico nella roccia, forse una placchetta '
                 + DC,
                 'Una corda arancione con un nodo ad anello su un moschettone a ghiera, allo '
                 'stesso elemento',
                 'Un palo di legno orizzontale legato a un tronco con molti giri di cordino: '
                 'parte di un cavalletto? ' + DC,
                 'Braca viola con protezione nera (scritta bianca, non leggibile)',
                 'Se le brache girino attorno agli alberi non si vede: ancoraggio su alberi, '
                 'su roccia o su entrambi ' + DC],
    },
    'lati_nota': ('Per il lato «lontano» il file non scrive uno schema. Le sue note: «Tag da '
                  'passare calandosi · Difficoltà a trovare gli ancoraggi · Cavalletto fra '
                  'alberi in loco».'),

    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['lontano', 'Due brache ad anello viola, una larga con cuciture in vista e una '
                        'stretta', ''],
            ['lontano', 'Grillo a lira che riunisce le brache', ''],
            ['lontano', 'Moschettone su un elemento metallico nella roccia ' + DC, ''],
            ['lontano', 'Corda arancione con nodo ad anello, su moschettone a ghiera', ''],
            ['lontano', 'Palo di legno con fascia nera, legato a un tronco con cordino '
                        'verde-blu', ''],
            ['lontano', 'Protezione nera su una braca viola, scritta bianca', 'non leggibile'],
        ],
        'nota': ('Riconosciuto per forma. Nessuna quantità e nessuna misura. Del lato «vicino» '
                 'non si vede il materiale.'),
    },

    'foto': [
        ('anfiteatro-97_01_lontano_brache-fra-gli-alberi.jpg',
         '«Lontano»: brache viola fra gli alberi, grillo, corda',
         'anfiteatro-97_02_lontano_palo-legato-a-un-albero.jpg',
         'Il palo legato al tronco, la braca e la protezione', 0.66, 0.5),
    ],

    'avvertenza': ('Il nome nel file è «91»',
                   'Il file del gruppo non ha una riga «97»: ha una «91», messa qui per la '
                   'posizione nell’elenco dell’Anfiteatro (46, 53, 91, 108, 113 contro 46, 53, '
                   '97, 108, 113). App, locandina e SlackMap dicono 97 m. Finché chi ha '
                   'compilato il file non conferma, note e foto di questa scheda potrebbero '
                   'essere di un’altra linea.'),

    'da_rilevare': [
        'Che la «91» del file sia questa linea.',
        'Quale lato è quello di tensione.',
        'Se l’ancoraggio del lato «lontano» è sugli alberi, sull’elemento nella roccia o su '
        'entrambi: quanti alberi, quali punti.',
        'Se il palo legato al tronco è parte di un cavalletto, e se resta sul posto.',
        'L’ancoraggio del lato «vicino»: non si vede in nessuna foto.',
        'Nodo della corda arancione; misure delle brache.',
        'Date e persone: nessuna foto ha i metadati.',
    ],
}
