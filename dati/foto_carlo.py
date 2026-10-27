# -*- coding: utf-8 -*-
"""Le linee fotografate da Carlo: le sue parole e ciò che le foto mostrano.

Due fonti, tenute distinte in ogni voce:

* **Carlo** — il file `LineeBisma.xlsx` (Drive del gruppo, 20/10/2026), riportato
  con le sue parole nel Foglio Google «Linee della Pietra di Bismantova», scheda
  «Linee» (id 1O6A56y96ivtnw3Kx5f5ceNjhXtLhGK8eMDUHzkeAatY, gid 1). Carlo ha
  segnato tutto «da controllare»: sono proposte, non rilievi. «Vicino» e
  «lontano» sono i suoi lati («Near Side», «Far Side»), NON il lato tensione e il
  lato statico della guida: quale sia quale non lo dice nessuna fonte.
* **Le foto** — lette una per una il 27/10/2026, con ingrandimenti, in
  `lavorazione/foto_linee/<id>/LETTURA.md`. Qui ne sta il riassunto: solo ciò che
  si vede in modo inequivocabile. Nessuna misura letta a occhio.

Questo modulo non deduce nulla: dove la foto non mostra, la voce dice che manca.
Il registro delle linee resta `dati/linee.py`; qui ci sono solo le righe che Carlo
ha compilato o fotografato.

    import foto_carlo as FC
    FC.LINEE['anfiteatro-46']['vicino']        # lo schema di Carlo
    FC.LINEE['anfiteatro-46']['foto_vicino']   # che cosa mostra la foto
"""

FONTE_CARLO = 'LineeBisma.xlsx di Carlo, Drive del gruppo, 20/10/2026'
DATA_LETTURA = '27/10/2026'

# Gli schemi di Carlo, dalla sua scheda «Sosta Bisma Standard». Sono le sue
# parole; dove non dà un numero, qui non c'è un numero.
SCHEMI = {
    'Bisma standard':
        'ancoraggio su 3 spit in loco, con 3 piastrine da 10 mm e 3 delta da portare; '
        'sosta main a doppio sliding x, con un omega fra le slinghe e uno per lo sliding '
        'x; sosta backup su corda per BFK da 15 m, con omega; cavalletto di 2 pali da '
        '1,5 m, legati con corda e legati alla roccia con corda, slinga e omega',
    'Bisma standard senza cavalletto':
        'lo stesso schema, senza il cavalletto',
}

# Nota ai termini di Carlo: «omega» è il grillo, «delta» la maglia rapida a
# delta, «slinga» la braca ad anello, «spit» il punto fisso (che tipo sia è
# un'altra questione: dubbio 39).

LINEE = {
    'anfiteatro-46': {
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto',
        'difficolta': ('No', '4'),
        'persone': ('No problem', '2 persone in calata'),
        'note': 'Tag da passare calandosi + Calarsi pochi metri per montare',
        'tipologia': 'Beginner',
        'foto_vicino': 'cavalletto di due pali di legno, in due uscite (estate e autunno); '
                       'due fettucce nere Spider con calza che convergono su grillo e '
                       'softshackle',
        'foto_lontano': 'placchetta con dado esagonale e grillo a lira: un punto in '
                        'inquadratura; braca lilla; nessun cavalletto',
        'confronto': 'coerente con lo schema su tutti e due i lati; dei 3 spit dello '
                     'schema se ne vede uno',
        'manca': 'lato di tensione; numero di punti; misure; che cosa siano le fettucce '
                 'Spider; date e persone',
    },
    'anfiteatro-53': {
        # documentata: la sua scheda è scheda_53.py. Questa riga serve solo a non
        # perdere ciò che Carlo ha scritto e l'unica foto (autunno: né 16/05 né 22/08).
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto',
        'difficolta': ('No', '3'),
        'persone': ('No problem', '2 persone'),
        'note': 'Tag da passare calandosi',
        'tipologia': 'Freestyle',
        'foto_vicino': 'due fettucce nere con calza su grillo e softshackle, braca lilla; '
                       'nessun cavalletto in inquadratura',
        'foto_lontano': None,
        'confronto': 'la foto non conferma né smentisce; è di una terza uscita, in autunno',
        'manca': 'se il «vicino» del file sia il main della guida; data e persone',
    },
    'anfiteatro-97': {
        'vicino': 'Bisma standard senza cavalletto',
        'lontano': None,
        'difficolta': ('3', '2'),
        'persone': ('Disarrampicare - Poco spazio', '3 persone'),
        'note': 'Tag da passare calandosi + Difficolta a trovare gli ancoraggi - '
                'Cavalletto fra alberi in loco',
        'tipologia': 'Highline',
        'foto_vicino': 'due linee parallele partono da questa cima; l\'ancoraggio non si '
                       'vede',
        'foto_lontano': 'alberi: brache viola attorno a due tronchi con grillo a lira, corda '
                        'arancione annodata su moschettone; un palo legato a un albero con '
                        'cordino',
        'confronto': 'il lato lontano, vuoto nel Foglio, è su alberi; il palo legato '
                     'all\'albero è coerente con «cavalletto fra alberi in loco»',
        'manca': 'quale delle due linee sia la 97; lato di tensione; se il palo sia un '
                 'cavalletto completo; misure; date e persone. Il file la chiama «91»',
    },
    'anfiteatro-108': {
        'vicino': 'Bisma standard',
        'lontano': 'Montaggio con alberi e uno spit. Sosta molto lunga, portare corde '
                   'lunghe anche per fare un deviatore',
        'difficolta': ('No', '2'),
        'persone': ('No problem', '2-3 persone'),
        'note': 'Tag da passare calandosi + Difficolta a trovare gli ancoraggi',
        'tipologia': 'Highline',
        'foto_vicino': None,
        'foto_lontano': 'la sosta con il tronco chiaro su terrazza di roccia, senza alberi '
                        '(le stesse foto stanno sulla riga della 113); la linea verso una '
                        'torre a sommità piatta',
        'confronto': 'le foto non mostrano alberi: non corrispondono alla descrizione '
                     'del file e corrispondono invece al lato lontano della 113',
        'manca': 'di quale linea sia la sosta con il tronco; dove siano alberi e spit; '
                 'lato di tensione; date e persone',
    },
    'anfiteatro-113': {
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto + tronco',
        'difficolta': ('No', '2'),
        'persone': ('No problem', '2-3 persone'),
        'note': 'Tag da passare calandosi',
        'tipologia': 'Highline',
        'foto_vicino': 'cavalletto di due pali in tre configurazioni (almeno tre uscite); la '
                       'linea con backup a festoni verso una torre di roccia',
        'foto_lontano': 'sosta su roccia con un tronco chiaro scavalcato dalle slinghe verdi; '
                        'moschettone su anello fisso, corda in calza fino a un secondo '
                        'elemento fisso, braca viola a un terzo; nastro sottile bianco-azzurro',
        'confronto': 'coerente su tutti e due i lati: cavalletto da una parte, tronco e '
                     'punti fissi senza cavalletto dall\'altra. Le stesse foto del tronco '
                     'stanno anche sulla riga della 108',
        'manca': 'di quale linea sia la sosta con il tronco; che cosa faccia il tronco; '
                 'numero e tipo dei punti; lato di tensione; date e persone',
    },
    'despedida-60': {
        'vicino': None,
        'lontano': None,
        'difficolta': (None, None),
        'persone': (None, None),
        'note': None,
        'tipologia': 'Freestyle',
        'foto_vicino': None,
        'foto_lontano': 'alberi: un tronco sottile con protezione, slinga e corda arancione; '
                        'fettuccia nera Gibbon dal tronco a tre moschettoni a ghiera; un '
                        'tronco grosso con la corda arancione; forse due pali a cavalletto',
        'confronto': 'il Foglio è vuoto; le foto danno il tipo di ancoraggio del lato lontano',
        'manca': 'tutto il lato vicino; lato di tensione; funzione della fettuccia Gibbon e '
                 'della corda; se i pali siano un cavalletto; date e persone',
    },
    'despedida-70': {
        'vicino': None,
        'lontano': None,
        'difficolta': (None, None),
        'persone': (None, None),
        'note': None,
        'tipologia': 'Freestyle / Highline',
        'foto_vicino': 'cavalletto di due pali (estate)',
        'foto_lontano': 'anche qui un cavalletto di due pali (autunno); slinghe verdi annodate '
                        'con cordino a una corda doppia; una slinga su calza bianca attorno a '
                        'un masso sul bordo',
        'confronto': 'il Foglio è vuoto; tutti e due i lati del file mostrano un cavalletto',
        'manca': 'se il cavalletto stia a tutti e due i capi; a che cosa sia ancorata la '
                 'corda doppia; lato di tensione; date e persone',
    },
}


def di(id_linea):
    """La voce di una linea, o None se Carlo non l'ha né compilata né fotografata."""
    return LINEE.get(id_linea)
