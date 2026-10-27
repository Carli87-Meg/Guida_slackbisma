# -*- coding: utf-8 -*-
"""Scheda di GAS-OH, Anfiteatro 53 m, detta «la 50»: la linea documentata.

E' il modello delle schede: ogni campo e' commentato. I dati vengono da
NOTE_RIGGING.md (trascrizioni e fotogrammi del 16/05/2026), dalle fotografie del
22/08/2026 all'altro capo, dalle risposte dell'utente (DUBBI.md) e dai metadati
GPS delle immagini. Niente e' dedotto: dove un dato manca la voce lo dice.

Marcatori nel testo (li colora il build):
  [DA CONFERMARE]  dato incerto, o contraddetto da un'altra fonte (rosso);
  «da rilevare»    dato non raccolto, da leggere sul pezzo o chiedere (grigio);
  cella vuota      nelle tabelle, lo stesso di «da rilevare».

Titolo e soprannome stanno nel registro (dati/linee.py: NOMI, SOPRANNOMI).
Fino all'edizione 0.3 questa scheda era il modulo build/scheda_53.py, con i dati
dentro il codice di impaginazione.
"""

DC = '[DA CONFERMARE]'
DR = 'da rilevare'

# Dieci letture del 22/08/2026 entro 3 m, a 51,4 m dal main: coordinate dal
# telefono (EXIF), non un rilievo. Dubbio 3, chiuso.
MAPPA_T = 'https://www.google.com/maps?q=44.419869,10.412353'
MAPPA_S = 'https://www.google.com/maps?q=44.419453,10.412072'

SCHEDA = {
    'id': 'anfiteatro-53',

    # testata: riga sotto il titolo e paragrafo di apertura
    'occhiello': 'detta «la 50» · A-frame sul lato tensione',
    'intro': ('<b>GAS-OH</b> è il nome che la linea ha su SlackMap; sul campo la chiamano '
              '<b>«la 50»</b>. Come si monta una linea è descritto nella parte 3; qui c’è '
              'com’è fatta questa.'),

    # pastiglie dei dati, subito sotto la testata: (etichetta, valore)
    'chips': [('Lunghezza', '53 m · catalogo'),
              ('Dislivello', DR),
              ('Ancoraggi', 'roccia · roccia'),       # B3: solo roccia
              ('A-frame', 'lato tensione'),
              ('Montaggi', '2 documentati')],

    # i montaggi di cui esiste documentazione: (data, che cosa)
    # Questa chiave e' cio' che rende la linea «documentata».
    'montaggi': [('16/05/2026', 'il montaggio ripreso nei video, con A-frame'),
                 ('22/08/2026', 'la stessa linea con i bungee; fotografie all’ancoraggio '
                                'statico')],

    # dove corre: il render i-pietra del settore ritagliato sulla linea, con i due
    # capi cerchiati. `estremi` sono frazioni dell'immagine, trovati per colore
    # (i-pietra disegna la 53 m in arancio #f97316) e verificati a vista: su un
    # render 1354 x 884 sono i pixel (476, 299) e (840, 337). Se il render viene
    # riesportato vanno ritrovati: python build/scheda_linea.py anfiteatro-53
    'posizione': {
        'render': 'Anfiteatro',
        'estremi': ((476 / 1354, 299 / 884), (840 / 1354, 337 / 884)),
        'ritaglio': (0.20, 0.16, 0.82, 0.62),       # sinistra, alto, destra, basso
        'colore': (249, 115, 22),
        'didascalia': 'Dove corre la 53 m nella vista i-pietra dell’Anfiteatro: '
                      'i due cerchi sono gli ancoraggi',
        # dubbio 56, chiuso il 27/10/2026: risposta dell'utente («la parte sopra
        # Cocoa»), coerente con il GPS delle riprese. Il render non dice quale
        # cerchio sia quale, e la didascalia non lo inventa.
        'nota': 'L’ancoraggio di tensione è il capo nord, sopra il settore di falesia '
                'Cocoa: lì ci sono sosta main, sosta backup e A-frame. La sosta su tre '
                'punti è all’altro capo. Il render non distingue i due cerchi.',
    },

    # i due lati. Coordinate: IMG_1416 (16/05, al main) e IMG_3323-3332 (22/08,
    # l'altro capo). Materiale: NOTE_RIGGING «Materiale nominato», sezioni A-F.
    'tensione': {
        'coord': '44.419869 · 10.412353 · 1025 m',
        'url': MAPPA_T,
        'voci': ['Sosta main: slinghe viola (quante e quanto lunghe, ' + DR + ')',
                 'Sosta backup: corde rosa, collegate con 1 BFK',
                 '1 weblock («banana») con grillo a lira',
                 '1 paranchino di tensionamento della base',
                 'Blocco del backup su sosta main e sosta backup',
                 'A-frame: 2 pali di legno tondo sul bordo'],
    },
    'statico': {
        'coord': '44.419453 · 10.412072 · 1025 m',
        'url': MAPPA_S,
        # placchette: viste il 16/05 e il 22/08; il file del gruppo le mette «da
        # portare» (dubbio 70): le fonti si contraddicono, resta rosso
        'voci': ['3 placchette su bullone: in loco o da portare ' + DC,
                 '1 corda verde acqua fra i punti',
                 'Slinga viola e carrucola bloccante',
                 '1 corda azzurra: linea vita',
                 'Sosta backup: com’è fatta, ' + DR],
    },
    # la scheda e' lunga: come nell'edizione 0.3, pagina nuova dopo i lati e dopo il materiale
    'pagina_dopo_lati': True,
    'pagina_dopo_materiale': True,
    'nota_coordinate': ('Le coordinate sono quelle registrate dal telefono stando agli '
                        'ancoraggi: servono ad avvicinarsi, non a ritrovare il singolo '
                        'punto, che va cercato a vista. Le due posizioni distano circa '
                        '51 m, coerente con i 53 m della linea: non è una misura.'),

    # il materiale di questa linea, con le quantita'. Colonne: quantita', articolo,
    # dove si usa, misura. Le celle vuote sono dati non rilevati; il rosso resta
    # per i dati incerti (dubbi 12, 13, 40, 70).
    'materiale': {
        'titolo': 'Il materiale del montaggio del 16 maggio',
        'righe': [
            ['3', 'Placchette su bullone — in loco o da portare ' + DC, 'ancoraggio statico', ''],
            ['', 'Slinghe viola — brache ad anello industriali', 'sosta main', ''],
            ['', 'Corde rosa', 'sosta backup', ''],
            ['1', 'BFK, moschettone d’acciaio grande', 'sulla corda rosa del backup', ''],
            ['4', 'Maglie rapide delta', '', ''],
            ['1', '«Mighty Lock», «quello quadratino» — nome incerto ' + DC, 'backup', ''],
            ['1', 'Slinga verde lunga, «la più grossa che c’è»', '', ''],
            ['1', 'Slinga piccola viola', '', ''],
            ['≥1', 'Slinga verde e nera', '', ''],
            ['1', 'Corda azzurra', 'tagline, poi linea vita', ''],
            ['1', 'Corda verde acqua', 'collegamento fra i punti', ''],
            ['≥1', 'Carrucola bloccante · EN 567:2013 · Ø 7,8-11 mm',
             'vista sull’ancoraggio statico; funzione ' + DC, ''],
            ['1', 'Weblock azzurro anodizzato, detto «banana»', 'lato tensione', ''],
            ['≥1', 'Grillo a lira in acciaio', 'collegamento della sosta', ''],
            ['1', 'Paranchino', 'tensionamento della base', ''],
            ['1', 'Softrelease', '', ''],
            ['≥2', 'Grigri', 'backup e calata', '—'],
            ['1', 'Corda di backup', 'per chi lavora in sosta', ''],
            ['', 'Nastro, backup della linea, leash', '', ''],
        ],
        'nota': ('Le celle vuote sono dati non rilevati: quantità, misure e modelli si leggono '
                 'sul pezzo o si chiedono a chi ha montato. In rosso i dati incerti o '
                 'contraddetti da un’altra fonte.'),
        # (file, didascalia, rapporto altezza/larghezza, fuoco verticale)
        'foto': ('IMG_1360.jpg', 'Il materiale steso prima del montaggio, 16 maggio 2026',
                 0.28, 0.42),
    },

    # fotografie dei due lati e della linea in opera: coppie
    # (file1, didascalia1, file2, didascalia2, rapporto, fuoco)
    'foto': [
        # sullo sfondo di IMG_1416 corre un'altra linea dello spot (dubbio 54)
        ('IMG_1416.jpg', 'Lato tensione: l’A-frame; sullo sfondo, un’altra linea',
         'IMG_3329.jpg', 'Lato statico: placchette e slinghe', 0.82, 0.6),
        ('IMG_1401.jpg', 'La linea in opera, percorsa con il leash',
         'IMG_1398.jpg', 'La campata vista dal bordo', 0.68, 0.55),
    ],

    # l'A-frame di questa linea. IMG_1396 e IMG_1416; posizione sul lato main dalla
    # risposta del 20/08. Filo ai piedi, cordino in testa, slinga lilla e corde
    # rosa: dubbio 50, 27/10/2026.
    'aframe': {
        'chips': [('Pali', '2 · legno tondo'), ('Testa', 'Incrociata e legata'),
                  ('Piede', 'Appoggiato su roccia'), ('Altezza', DR)],
        'come': ['Due pali di legno tondo, incrociati e legati in testa',
                 'Slinga lilla avvolta sulla testa dei pali',
                 'Cordino annodato sotto l’incrocio; corda verde fluo e fettuccia blu in testa',
                 'Dall’A-frame passano le corde rosa della sosta backup',
                 'La linea passa sul fianco esterno di un palo, poco sotto l’incrocio',
                 'Piedi appoggiati sulla roccia del bordo',
                 'Filo metallico al piede dei pali: due o tre giri a quello di sinistra'],
        'da_rilevare': ['Altezza dei pali',
                        'Diametro e tipo del legno',
                        'Come sono legati in testa',
                        'Se i piedi sono fermati o solo appoggiati',
                        'Se il filo metallico tiene il palo o è un recinto',
                        'Di quanto solleva la linea sopra il bordo'],
    },

    # varianti documentate: dizionari con titolo, testo e coppia di foto
    # IMG_3323-3332, 22/08/2026, all'altro capo (51,4 m dal main). In IMG_3324-3326
    # una slinga viola entra nel grillo a lira (dubbio 28). L'utente: «il montaggio
    # fatto quel giorno era della 53 ma con i bungee».
    'varianti': [{
        'titolo': 'La stessa linea, montata con i bungee',
        'testo': ('Il 22 agosto 2026 la 53 m è stata montata con i <b>bungee</b>. Le '
                  'fotografie sono state scattate all’ancoraggio statico: si vedono le '
                  'placchette su bullone, una slinga viola che entra in un grillo a lira, '
                  'senza maglia rapida visibile, e la corda annodata fra i punti. Il '
                  'materiale di questa variante non è stato rilevato.'),
        'foto': ('IMG_3324.jpg', 'Placchette, slinghe viola e corda annodata',
                 'IMG_3325.jpg', 'Dal grillo a lira ai bungee', 0.72, 0.45),
    }],

    # che cosa resta da rilevare su questa linea (dubbi 1, 2, 28, 37, 38, 39)
    'da_rilevare': [
        'La lunghezza, misurata sui punti, e il dislivello.',
        'I punti dell’ancoraggio di tensione: quanti e di che tipo.',
        'Una fotografia d’insieme dei tre punti, per l’angolo di apertura.',
        'Diametro e marca del bullone, e se è un tassello meccanico o una barra resinata '
        '(su una placchetta si legge «FOR 1 PERSON», logo e codice incerti); marca della '
        'carrucola bloccante.',
        'Più in basso c’è un altro bullone: con placchetta il 16 maggio, senza il 22 agosto. '
        'Se sia lo stesso punto, e a che cosa serva.',
        'Se accanto ai punti fissi c’è protezione veloce.',
        # dubbio 37: le etichette viola del catalogo dicono 1 t, ma nessuna e' di un
        # pezzo che si sa usato il 16/05. La portata non si stampa finche' non si sa.
        'Le etichette delle slinghe della sosta main, lilla e viola scuro: sulla lilla si '
        'vedono una linguetta blu e un’etichetta bianca, illeggibili in tutte le fotografie. '
        'Vanno lette sul pezzo, sapendo di chi era.',
        'Nastro, backup della linea e leash: marca e tipo.',
    ],
}
