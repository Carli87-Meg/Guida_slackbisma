# -*- coding: utf-8 -*-
"""Scheda di Double Rainbow, Anfiteatro 46 m (AN-3): linea fotografata.

Fonti, e solo queste: le cinque fotografie del file LineeBisma del gruppo
(lavorazione/foto_linee/anfiteatro-46/, lette il 27/10/2026 e riguardate una per
una il 27/10 sera per questa scheda), le parole del file stesso («da
controllare»), il render i-pietra dell'Anfiteatro e il segmento disegnato su
SlackMap. Nessuna di queste fonti dice quale lato sia quello di tensione:
«vicino» e «lontano» sono le colonne del file. Dubbi 60, 61, 64, 65 di DUBBI.md.

Le fotografie 46_05 (una persona riconoscibile) non si stampa.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-46',
    'occhiello': 'fotografata · 5 fotografie del gruppo',
    'intro': ('<b>Double Rainbow</b> è il nome che la linea ha su SlackMap. Di questa linea '
              'esistono le fotografie del gruppo, di almeno due giornate diverse, e le note '
              'del file LineeBisma: mostrano com’è stata attrezzata, non come si monta. Il '
              'lato di tensione non è dichiarato da nessuna fonte.'),
    'chips': [('Lunghezza', '46 m · catalogo'),
              ('Tipologia', 'Beginner · file'),
              ('Cavalletto', 'sì · «vicino»'),
              ('Punti visti', '1 · «lontano»'),
              ('Tensione', DR)],

    # il render dell'Anfiteatro: la 46 m e' la linea verde, l'unica del render con
    # quella tinta; capi trovati per colore (tinta 95-160°) il 27/10/2026, verificati
    # a vista sull'etichetta «Anfiteatro – 46m», che poggia su quella linea
    'posizione': {
        'render': 'Anfiteatro',
        'estremi': ((882 / 1354, 362 / 884), (1180 / 1354, 488 / 884)),
        'ritaglio': (0.56, 0.28, 0.96, 0.66),
        'colore': (31, 190, 136),
        'didascalia': 'Dove corre la 46 m nella vista i-pietra dell’Anfiteatro: i due cerchi '
                      'sono i capi',
        'nota': 'Quale dei due capi sia il «vicino» del file, e quale il lato di tensione, '
                'non è noto.',
    },

    # i due lati con i nomi del file: il blocco dice che cosa si vede nelle foto
    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Cavalletto di pali tondi di legno: due pali legati con fettuccia azzurra '
                 'd’estate; d’autunno forse tre, legati con corda color canapa ' + DC,
                 'Brache lilla e viola, slinghe verdi attorno ai pali',
                 'Due elementi in calza nera, da cui escono anelli lilla e giallo-verde su '
                 'grilli a lira: che cosa siano ' + DC,
                 'Protezione nera imbottita con etichetta «SPIDER» su uno dei due',
                 'Connettori con un anello arancione, da cui parte il nastro bianco',
                 'Punti fissi: nessuno in inquadratura'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['1 placchetta con dado esagonale su bullone, con grillo a lira a perno '
                 'filettato: altri punti ' + DR,
                 'Brache lilla (una con riga nera) nel grillo; anello di fettuccia nera; calza '
                 'verde su cordino giallo-verde',
                 'Elemento metallico con il nastro bianco avvolto, da cui parte verso il vuoto '
                 'un elemento in calza nera: un weblock? ' + DC,
                 'Dietro le brache due elementi verticali, uno di legno: un cavalletto? ' + DC],
    },
    'lati_nota': ('Il file assegna al lato «vicino» lo schema «Bisma standard» e al «lontano» '
                  '«Bisma standard senza cavalletto». Se l’elemento con il nastro avvolto fosse '
                  'un weblock, la tensione starebbe sul lato «lontano»: è un’ipotesi, non un '
                  'dato.'),

    # coordinate: il segmento disegnato su SlackMap (dati/slackmap.py)
    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto

    # le parole del file del gruppo, da dati/file_lineebisma.py
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['vicino', 'Cavalletto di pali tondi di legno, legature in corda o fettuccia', ''],
            ['vicino', 'Brache ad anello lilla e viola; slinghe verdi', ''],
            ['vicino', 'Due elementi in calza nera con anelli colorati, su grilli a lira', ''],
            ['vicino', 'Protezione nera imbottita', 'SPIDER'],
            ['vicino', 'Anello arancione e connettori metallici alla convergenza ' + DC, ''],
            ['vicino', 'Nastro bianco con bordo blu (la linea)', ''],
            ['vicino', 'Corda rosa dalla legatura del cavalletto (estate)', ''],
            ['lontano', 'Placchetta con dado esagonale; grillo a lira con perno filettato', ''],
            ['lontano', 'Brache lilla, anello di fettuccia nera, calza verde su cordino', ''],
            ['lontano', 'Elemento metallico con il nastro avvolto: un weblock? ' + DC, ''],
        ],
        'nota': ('Riconosciuto per forma, non per marca, salvo dove indicato. Nessuna quantità '
                 'e nessuna misura: le foto non le danno. Le etichette delle brache non si '
                 'leggono.'),
    },

    # coppie: (file1, didascalia1, file2, didascalia2, rapporto, fuoco)
    'foto': [
        ('anfiteatro-46_01_vicino_cavalletto-e-due-elementi-in-calza.jpg',
         '«Vicino»: cavalletto e due elementi in calza (autunno)',
         'anfiteatro-46_03_lontano_ancoraggio-placchetta.jpg',
         '«Lontano»: la placchetta con il grillo a lira', 0.66, 0.5),
        ('anfiteatro-46_02_vicino_elementi-in-calza-dall-alto.jpg',
         'I due elementi in calza, protezione «SPIDER»',
         'anfiteatro-46_04_lontano_ancoraggio-placchetta-dettaglio.jpg',
         'Il punto da vicino: placchetta, dado, grillo', 0.66, 0.5),
    ],

    'da_rilevare': [
        'Quale lato è quello di tensione, e dove si tensiona.',
        'Numero e tipo dei punti su ciascun lato: sul «lontano» se ne vede uno solo, il file '
        'ne scrive tre.',
        'Che cosa sono i due elementi in calza nera, che cosa c’è dentro le calze, e che cosa '
        'è l’anello arancione.',
        'Che cosa è l’elemento metallico con il nastro avvolto sul lato «lontano».',
        'Quanti pali ha il cavalletto d’autunno, e come è ancorato a terra.',
        'Misure di brache e fettucce; diametro del bullone; modello del grillo.',
        'Data di ogni fotografia e chi c’era: nessuna ha i metadati.',
    ],
}
