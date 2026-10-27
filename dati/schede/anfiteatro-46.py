# -*- coding: utf-8 -*-
"""Scheda di Double Rainbow, Anfiteatro 46 m (AN-3): linea fotografata.

Fonti, e solo queste: le cinque fotografie del file LineeBisma del gruppo
(lavorazione/foto_linee/anfiteatro-46/, lette il 27/10/2026 e riguardate una per
una il 27/10 sera per questa scheda), le parole del file stesso («da
controllare»), il render i-pietra dell'Anfiteatro e il segmento disegnato su
SlackMap. Nessuna di queste fonti dice quale lato sia quello di tensione:
«vicino» e «lontano» sono le colonne del file. Dubbi 60, 61, 64, 65 di DUBBI.md.

La 46_01 e la 46_02 erano qui: il 27/10/2026 l'utente ha detto che mostrano il montaggio
con i bungee su GAS-OH (dubbio 64), e ora sono la 53_02 e la 53_03. Restano tre foto.
La 46_05 (una persona riconoscibile) non si stampa.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-46',
    'occhiello': 'fotografata · 3 fotografie del gruppo',
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
        # ritaglio piu' basso del 0.28-0.66 di prima: la figura alta 305 pt spingeva
        # i due lati sulla pagina dopo e la scheda finiva con una pagina quasi vuota
        'ritaglio': (0.56, 0.31, 0.96, 0.61),
        'colore': (31, 190, 136),
        'didascalia': 'Dove corre la 46 m nella vista i-pietra dell’Anfiteatro: i due cerchi '
                      'sono i capi',
        'nota': 'Quale dei due capi sia il «vicino» del file non è noto.',
    },

    # i due lati con i nomi del file: il blocco dice che cosa si vede nelle foto
    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        # dalla sola 46_05 (estate): le due d'autunno erano della 53 m
        'voci': ['Cavalletto di due pali tondi incrociati, legati in cima con una fettuccia '
                 'azzurra; dalla legatura pende una corda rosa (estate)',
                 'Dalla cima brache viola e lilla e slinghe verdi',
                 'Due elementi neri con calza e una corda verde verso la parete: che cosa '
                 'siano ' + DC,
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
                  'dato. Le etichette delle brache non si leggono. Le due foto d’autunno del '
                  'lato «vicino» che il file metteva su questa riga sono della 53 m; quella '
                  'rimasta mostra una persona riconoscibile e non si stampa.'),

    # coordinate: il segmento disegnato su SlackMap (dati/slackmap.py)
    'slackmap': True,
    'foto_dopo_lati': True,      # le foto subito sotto i lati che descrivono

    # le parole del file del gruppo, da dati/file_lineebisma.py
    'file_gruppo': True,

    # coppie: (file1, didascalia1, file2, didascalia2, rapporto, fuoco)
    'foto': [
        ('anfiteatro-46_03_lontano_ancoraggio-placchetta.jpg',
         '«Lontano»: la placchetta con il grillo a lira',
         'anfiteatro-46_04_lontano_ancoraggio-placchetta-dettaglio.jpg',
         'Il punto da vicino: placchetta, dado, grillo', 0.66, 0.5),
    ],

    'da_rilevare': [
        'Quale lato è quello di tensione, e dove si tensiona.',
        'Numero e tipo dei punti su ciascun lato: sul «lontano» se ne vede uno solo, il file '
        'ne scrive tre.',
        'Che cosa sono i due elementi neri con calza che salgono verso la parete (estate).',
        'Che cosa è l’elemento metallico con il nastro avvolto sul lato «lontano».',
        'Come è ancorato a terra il cavalletto.',
        'Misure di brache e fettucce; diametro del bullone; modello del grillo.',
        'Data di ogni fotografia e chi c’era: nessuna ha i metadati.',
    ],
}
