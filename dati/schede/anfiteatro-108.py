# -*- coding: utf-8 -*-
"""Scheda della Anfiteatro 108 m (AN-6), senza nome su SlackMap: linea fotografata.

Fonti: le quattro fotografie del file LineeBisma (lavorazione/foto_linee/
anfiteatro-108/, lette il 27/10/2026 e riguardate per questa scheda), le parole
del file, il segmento SlackMap. Non c'e' un render: la 108 m e' entrata in
i-pietra il 21/08/2026, il giorno dopo i render. Le foto della sosta con il
tronco stanno anche sulla riga della 113 m: di quale linea sia la sosta e'
il dubbio 59. Dubbi 59, 60, 63.

Le fotografie 108_02 e 108_04 (una persona riconoscibile da chi la conosce) non
si stampano.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

SCHEDA = {
    'id': 'anfiteatro-108',
    'occhiello': 'fotografata · 4 fotografie del gruppo',
    'intro': ('La 108 m non ha un nome su SlackMap. Le fotografie sulla sua riga del file '
              'mostrano la <b>sosta con il tronco</b>, d’estate e d’autunno: la stessa sosta '
              'che il file mette anche sulla riga della 113 m. Di quale delle due linee sia '
              'non lo dice nessuna foto.'),
    'chips': [('Lunghezza', '108 m · catalogo'),
              ('Tipologia', 'Highline · file'),
              ('Ancoraggio', 'alberi e spit · file'),
              ('Sosta', 'tronco: 108 o 113?'),
              ('Tensione', DR)],

    # nessun render: lo dice la scheda
    'posizione_nota': ('La 108 m non è tracciata sul render i-pietra del 20/08/2026: è stata '
                       'creata nel catalogo il giorno dopo. Corre dall’Anfiteatro verso la '
                       'torre di fronte, come la 97 m e la 113 m; dove esattamente lo dice '
                       'solo il segmento di SlackMap qui sotto.'),

    'lato_a': {
        'titolo': 'Lato «vicino» del file',
        'voci': ['Nessuna fotografia',
                 'Il file: schema «Bisma standard»'],
    },
    'lato_b': {
        'titolo': 'Lato «lontano» del file',
        'voci': ['Un tronco con la corteccia, tagliato netto a un capo, posato sulla roccia '
                 'del bordo e legato con cordino viola alle due estremità',
                 'Sopra il tronco un’imbottitura bianca e un tessuto rosso; sopra, due slinghe '
                 'verdi tubolari verso il bordo',
                 'Una slinga verde finisce, con un cordino annodato, su un moschettone a ghiera '
                 'agganciato a una placchetta con dado',
                 'Una calza grigia e poi rossa va verso l’interno e finisce in un connettore '
                 'con cordino viola: ancorata a che cosa ' + DC,
                 'Una braca viola annodata su un elemento metallico nella roccia; una braca '
                 'azzurra; una corda blu; una matassa di fettuccia bianco-nera',
                 'Un albero con la chioma piena subito accanto alla sosta: se ne faccia parte '
                 + DC],
    },
    'lati_nota': ('Il file descrive il lato «lontano» così: «Montaggio con alberi e uno spit. '
                  'Sosta molto lunga, portare corde lunghe anche per fare un deviatore». Le '
                  'foto non lo smentiscono e non lo confermano: l’albero c’è, lo spit e le '
                  'corde verso l’interno escono dall’inquadratura.'),

    'slackmap': True,
    'foto_in_coda': True,        # avvertenza e «da rilevare» prima delle foto
    'file_gruppo': True,

    'materiale': {
        'titolo': 'Il materiale che si vede nelle foto',
        'colonne': ['Lato', 'Che cosa si vede', 'Marca leggibile'],
        'larghezze': [70, 331, 90],
        'righe': [
            ['lontano', 'Tronco con la corteccia, imbottitura bianca e tessuto rosso, cordino '
                        'viola di legatura', ''],
            ['lontano', 'Due slinghe verdi tubolari (su una, una scritta scura non leggibile)', ''],
            ['lontano', 'Moschettone a ghiera su placchetta con dado', ''],
            ['lontano', 'Corda in calza grigia e rossa verso l’interno, con connettore e '
                        'cordino viola', ''],
            ['lontano', 'Braca viola con etichetta azzurra illeggibile; braca azzurra', ''],
            ['lontano', 'Matassa di fettuccia piatta bianco-nera; corda blu', ''],
        ],
        'nota': 'Riconosciuto per forma. Nessuna quantità e nessuna misura.',
    },

    'foto': [
        ('anfiteatro-108_01_lontano_sosta-con-tronco.jpg',
         '«Lontano»: la sosta con il tronco, verso la torre (estate)',
         'anfiteatro-108_03_lato-nd_sosta-con-tronco-altra-vista.jpg',
         'La stessa sosta: slinghe, placchetta, calza rossa', 0.66, 0.45),
    ],

    'avvertenza': ('Una sosta, due linee',
                   'Fotografie diverse della stessa sosta con il tronco stanno sulla riga della '
                   '108 m e su quella della 113 m. Chi va a cercarla potrebbe trovarla al capo '
                   'di un’altra linea: prima di attrezzare, chiedere a chi ha compilato il file '
                   'di quale linea è.'),

    'da_rilevare': [
        'Di quale linea è la sosta con il tronco: 108 m o 113 m.',
        'Dove sono gli alberi e lo spit del file, e se l’albero accanto alla sosta ne fa parte.',
        'A che cosa sono ancorate la calza grigia e rossa, la braca viola e i cordini che '
        'escono dall’inquadratura.',
        'Che cosa fa il tronco, e se resta sul posto da una stagione all’altra.',
        'Quale lato è quello di tensione; l’ancoraggio del lato «vicino», senza foto.',
        'La scritta sulla slinga verde e l’etichetta della braca viola: da fotografare distese.',
        'Date e persone: nessuna foto ha i metadati.',
    ],
}
