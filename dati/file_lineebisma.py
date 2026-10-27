# -*- coding: utf-8 -*-
"""Le linee del file LineeBisma: le parole del file e ciò che le sue foto mostrano.

Due fonti, tenute distinte in ogni voce:

* **Il file** — `LineeBisma.xlsx` (Drive del gruppo, 20/10/2026), riportato con le
  sue parole anche nel Foglio "Linee della Pietra di Bismantova" sul Drive del
  gruppo. Il file è segnato tutto «da controllare»: sono proposte, non rilievi.
  «Vicino» e «lontano» sono le sue colonne («Near Side», «Far Side»), NON il lato
  tensione e il lato statico della guida: quale sia quale non lo dice nessuna fonte
  (DUBBI 60).
* **Le foto** — le immagini del file, copiate in `lavorazione/foto_linee/<id>/` e
  lette una per una nei `LETTURA.md` (27/10/2026, rilette dopo aver raddrizzato le
  dieci copie ancora coricate). Qui ne sta il riassunto: ciò che si vede in modo
  inequivocabile, e ciò che non lo è porta [DA CONFERMARE]. Nessuna misura letta a
  occhio.

Questo modulo non deduce nulla: le celle del file sono trascritte con le sue parole
(anche gli errori di battitura), le equivalenze con il materiale della guida non ci
sono, e dove la foto non mostra la voce lo dice. Il registro delle linee resta
`dati/linee.py`; qui ci sono solo le righe del file compilate o fotografate.

Il testo che finisce stampato non contiene numeri di dubbio né percorsi: i rimandi
a DUBBI.md stanno in questi commenti. Il build colora di rosso ogni
«[DA CONFERMARE…]».

    import file_lineebisma as FC
    FC.LINEE['anfiteatro-46']['vicino']        # la colonna «Near Side» del file
    FC.LINEE['anfiteatro-46']['foto_vicino']   # che cosa mostrano le sue foto
"""

FONTE = 'file LineeBisma del gruppo (LineeBisma.xlsx, Drive, 20/10/2026)'
DATA_LETTURA = '27/10/2026'
DC = '[DA CONFERMARE]'

# I nomi di schema che il file usa nelle colonne dei lati. Solo il primo ha una
# scheda sua nel file («Sosta Bisma Standard»); il secondo no.
NOMI_SCHEMA = ('Bisma standard', 'Bisma standard senza cavalletto')

# La scheda «Sosta Bisma Standard» del file, cella per cella e con le sue parole
# (anche «Slinding» e «1.5»). Un blocco per ogni intestazione della colonna A, piu'
# il blocco «Cavalletto» delle colonne E-F. Dove il file non da' un numero, qui non
# c'e' un numero. B11 e B16-B19 sono vuote. Che «Cavalletto» (B12) stia nel blocco
# «Materiale da portare» lo dice la posizione: fra A7 e A13.
SCHEDA_SOSTA_TITOLO = 'Ancoraggio Standard Bisma'                       # B4
SCHEDA_SOSTA = [
    ('Ancoraggio', [['3 spit']]),                                       # A5: B5
    ('Materiale in loco', [['Spit e Dadi']]),                           # A6: B6
    ('Materiale da portare', [['3 piastrine da 10 mm'], ['3 delta'],    # A7: B7-B10, B12
                              ['1 omega fra le slinghe'],
                              ['1 omega per sliding x'], ['Cavalletto']]),
    ('Sosta Main', [['Doppio Slinding x'], ['Omega fra slinghe'],       # A13: B13-B15
                    ['Omega per sliding x']]),
    ('Sosta Backup', [['Corda per BFK', '15 metri'], ['Omega']]),        # A20: B20, C20, B21
    ('Cavalletto', [['2 pali da 1.5 metri'], ['Corda per legatura'],    # E4: F4-F7
                    ['Corda per legare cavalletto alla roccia'],
                    ['Slinga e omega']]),
]

# Che cosa la scheda lascia aperto. Sono osservazioni sulla scheda, non deduzioni:
# ognuna dice dove il file e' ambiguo.
#  - omega due volte: verifica del 27/10, punto 11; nel Foglio del gruppo sono
#    contati una volta sola, per scelta non dichiarata.
#  - piastrine da portare / in loco: verifica del 27/10, punto 10 (la scheda della
#    53 m le dice fisse: voce nuova da aprire in DUBBI).
#  - «senza cavalletto»: il file non la definisce.
#  - termini: prima qui stava «omega = grillo, delta = maglia rapida a delta,
#    slinga = braca ad anello»; era una deduzione e non si stampa.
SCHEDA_SOSTA_DA_CONFERMARE = [
    'Gli omega sono elencati due volte, in «Materiale da portare» e in «Sosta Main»: '
    'se siano gli stessi pezzi o pezzi in più ' + DC + '.',
    'In loco il file mette «Spit e Dadi», da portare «3 piastrine da 10 mm»: se le '
    '«piastrine» restino sul posto ' + DC + '.',
    '«Bisma standard senza cavalletto» non ha una scheda sua: che sia la stessa senza '
    'il blocco «Cavalletto» ' + DC + '.',
    'A quali pezzi del materiale corrispondano «spit», «piastrine», «delta», «omega», '
    '«slinga», «sliding x» e «BFK» ' + DC + '.',
]

# Una voce per riga del file. Le celle sono dalla scheda «Elenco»:
#   C «Near Side», D «Schetchy», E «Persone»   -> 'vicino', 'schetchy'[0], 'persone'[0]
#   F «Far Side», G «Schetchy2», H «Persone3»  -> 'lontano', 'schetchy'[1], 'persone'[1]
#   I «Note», J «Tipologia».
# «Schetchy» non e' una difficolta': che cosa misuri (e in che verso) il file non lo
# dice; «No» fra i valori fa pensare a un si'/no. Si stampa con il nome del file.
# Le coppie seguono le colonne: prima quella accanto a «Near Side», poi quella
# accanto a «Far Side». Le intestazioni («Schetchy/Persone», «Schetchy2/Persone3»)
# non nominano il lato: l'abbinamento viene solo dalla posizione delle colonne.
# 'foto_fuori': foto sulla riga della linea ma fuori dalle colonne dei lati.
# 'nota_rilievo': una frase in piu' per la scheda di rilievo della linea.
LINEE = {
    'anfiteatro-46': {
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto',
        'schetchy': ('No', '4'),
        'persone': ('No problem', '2 persone in calata'),
        'note': 'Tag da passare calandosi + Calarsi pochi metri per montare',
        'tipologia': 'Beginner',
        # Cavalletto: 01 (autunno, corda color canapa, forse tre pali: due teste tagliate
        # sopra l'incrocio e il palo in primo piano) e 05 (estate, fettuccia azzurra,
        # due pali); DUBBI 61. Gli elementi neri di 01 e 02: di nero si vede solo la
        # calza, dalle calze escono anelli lilla e giallo-verde; prima qui stava «due
        # fettucce nere», che non si vede (DUBBI 64). «SPIDER» e' sull'etichetta di una
        # protezione. Dietro la sosta di 03-04 due elementi verticali: legno solo uno.
        # 27/10/2026: la 01 e la 02 erano il montaggio con i bungee su GAS-OH (DUBBI 64),
        # ora anfiteatro-53_02 e _03. Resta la 05, d'estate.
        'foto_vicino': ('cavalletto di due pali di legno legati con una fettuccia azzurra '
                        '(estate); brache viola e lilla, slinghe verdi; due elementi neri con '
                        'calza verso la parete [DA CONFERMARE: che cosa siano]'),
        'foto_lontano': ('un punto fisso su roccia: placchetta con dado e grillo a lira, brache '
                         'lilla; il nastro bianco avvolto su un elemento metallico [DA '
                         'CONFERMARE: che cosa sia]; dietro, due elementi verticali, uno di '
                         'legno [DA CONFERMARE: se siano un cavalletto]'),
        'da_confermare': 'lato di tensione; numero e tipo dei punti; misure; data delle foto',
    },
    'anfiteatro-53': {
        # Documentata: la sua scheda e' dati/schede/anfiteatro-53.py, e il build non stampa questa riga.
        # Serve a non perdere cio' che dice il file e l'unica foto (autunno: ne' 16/05
        # ne' 22/08). I pali in basso a sinistra toccano DUBBI 64 e, senza chiuderla, 56.
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto',
        'schetchy': ('No', '3'),
        'persone': ('No problem', '2 persone'),
        'note': 'Tag da passare calandosi',
        'tipologia': 'Freestyle',
        'foto_vicino': ('due elementi in calza nera, da cui escono anelli lilla e giallo-verde, '
                        'che convergono su connettori e un anello arancione [DA CONFERMARE: che '
                        'cosa siano]; brache lilla; due pali di legno con brache avvolte [DA '
                        'CONFERMARE: se siano un cavalletto]'),
        'foto_lontano': None,
        'da_confermare': 'se il «vicino» del file sia il lato tensione della guida; se i '
                         'pali siano l\'A-frame; data della foto',
    },
    'anfiteatro-97': {
        # Il file la chiama «91»: messa sulla 97 per posizione (DUBBI 62).
        # La foto del lato vicino (ora 97_03) nel file e' ritagliata sull'ancoraggio in
        # basso a destra: per il ritaglio la 97 e' la linea che parte da li' (DUBBI 69).
        # La 97_03 mostra un volto riconoscibile: la miniatura e' la 97_01.
        'vicino': 'Bisma standard senza cavalletto',
        'lontano': None,
        'schetchy': ('3', '2'),
        'persone': ('Disarrampicare - Poco spazio', '3 persone'),
        'note': 'Tag da passare calandosi + Difficolta a trovare gli ancoraggi - '
                'Cavalletto fra alberi in loco',
        'tipologia': 'Highline',
        # dubbio 69, utente 27/10/2026: da sinistra la 113, la 108 e la 97
        'foto_vicino': ('linee controluce verso la torre di fronte: da sinistra la 113, la 108 '
                        'e la 97, che parte dall’ancoraggio su cui il file ritaglia la foto'),
        'foto_lontano': ('brache viola fra gli alberi, riunite da un grillo; un moschettone su un '
                         'elemento metallico sulla roccia, forse una placchetta; una corda '
                         'arancione annodata; un palo legato a un tronco '
                         '[DA CONFERMARE: se l’ancoraggio sia sugli alberi, sulla roccia o su '
                         'entrambi, e se il palo sia un cavalletto]'),
        'da_confermare': 'lato di tensione; che la «91» del file sia questa linea; misure; data '
                         'delle foto',
    },
    'anfiteatro-108': {
        # La sosta con il tronco sta anche sulla riga della 113 (DUBBI 59). «Senza
        # alberi» e «scortecciato» erano letture sbagliate: accanto alla sosta c'e' un
        # albero, il tronco ha la corteccia. Le foto non smentiscono la descrizione del
        # file (DUBBI 63).
        'vicino': 'Bisma standard',
        'lontano': 'Montaggio con alberi e uno spit. Sosta molto lunga, portare corde '
                   'lunghe anche per fare un deviatore',
        'schetchy': ('No', '2'),
        'persone': ('No problem', '2-3 persone'),
        'note': 'Tag da passare calandosi + Difficolta a trovare gli ancoraggi',
        'tipologia': 'Highline',
        'foto_vicino': None,
        # 27/10/2026: le quattro foto della riga (D7, U7, L7) sono della 113 (DUBBI 59 e
        # 63, «in queste foto abbiamo montato la 113»): ora anfiteatro-113_09-12. Della
        # 108 non resta nessuna foto, e la linea e' censita.
        'foto_lontano': None,
        'nota_rilievo': ('Le quattro foto che il file mette su questa riga, con la sosta con il '
                         'tronco, sono della 113 m: della 108 non c’è nessuna foto.'),
        'da_confermare': 'dove siano gli alberi e lo spit del file; lato di tensione',
    },
    'anfiteatro-113': {
        # Cavalletto: due pali tondi (02, 03, 08), tre pali (01), due assi squadrate di
        # notte (04). Sosta con il tronco: 05, 06, 07 (e 108_01-03, DUBBI 59).
        # «Tre punti fissi» non si contano: placchetta con dado in 05, un elemento
        # metallico sotto la braca viola in 06; l'«anello» era la placchetta.
        # SlackMap, scheda della Brifing (113 m): «barre filettate incollate
        # chimicamente» (DUBBI 39). Etichette illeggibili: DUBBI 68.
        'vicino': 'Bisma standard',
        'lontano': 'Bisma standard senza cavalletto + tronco',
        'schetchy': ('No', '2'),
        'persone': ('No problem', '2-3 persone'),
        'note': 'Tag da passare calandosi',
        'tipologia': 'Highline',
        # La seconda linea a festoni sotto la linea (01, 03, 08): che sia il backup e'
        # una lettura, come per la 53 m (DUBBI 55 e 74).
        'foto_vicino': ('cavalletti di legno in tre forme (due pali tondi, tre pali, due assi '
                        'squadrate); la linea verso una torre di roccia e, sotto, il backup '
                        'appeso a festoni'),
        'foto_lontano': ('la sosta con il tronco (anche nelle quattro foto che il file metteva '
                         'sulla riga della 108): un tronco con la corteccia, coperto '
                         'in parte da un’imbottitura bianca, sotto le slinghe verdi; un albero '
                         'accanto; una slinga su moschettone a ghiera e placchetta con dado; '
                         'elementi metallici nella roccia [DA CONFERMARE: numero e tipo]'),
        'nota_rilievo': ('La sosta con il tronco è di questa linea: il file la metteva anche '
                         'sulla riga della 108 m.'),
        # SlackMap e' una terza fonte, non il file ne' le foto: sta fra le cose da
        # confermare, non nella riga «nelle foto» (DUBBI 39)
        'da_confermare': ('che cosa faccia il tronco; numero e tipo dei punti (su SlackMap la '
                          '«Brifing», 113 m, ha barre filettate incollate chimicamente: se sia '
                          'questa linea); lato di tensione; data delle foto'),
    },
    'despedida-60': {
        # Il file ha solo la tipologia. 01 e' la stessa scena della 70_02: l'highliner
        # nella nebbia puo' essere sulla 70. 04 letta coricata dava «tronco a terra»:
        # e' un albero in piedi (DUBBI 67).
        'vicino': None,
        'lontano': None,
        'schetchy': (None, None),
        'persone': (None, None),
        'note': None,
        'tipologia': 'Freestyle',
        'foto_vicino': None,
        # Gibbon: in 02 passa accanto ai moschettoni e prosegue oltre il bordo
        # dell'immagine; in 04 e 06 gira attorno alla base dell'albero. Una o piu'
        # fettucce non si vede (verifica «fonti» del 27/10, punto 6).
        'foto_lontano': ('un tronco sottile in piedi con protezione, slinga e corda arancione; '
                         'accanto un tronco inclinato e bastoni incrociati [DA CONFERMARE: se '
                         'siano un cavalletto]; fettuccia nera «GIBBON» [DA CONFERMARE: una o '
                         'più]: in una foto passa accanto a tre moschettoni sul bordo, in altre '
                         'gira attorno alla base di un albero [DA CONFERMARE: se l’ancoraggio '
                         'sia sugli alberi]'),
        # la miniatura (60_01) mostra in alto un tratto della linea nella nebbia, su
        # cui nella foto intera c'e' un highliner: e' la stessa scena della 70_02
        'da_confermare': 'il lato vicino, senza foto; lato di tensione; se la linea nella '
                         'nebbia della miniatura sia la 60 m o la 70 m; funzione di fettuccia '
                         'e corde; data delle foto',
    },
    'despedida-70': {
        # Lato vicino d'estate, lontano d'autunno, con cavalletti diversi (DUBBI 66).
        'vicino': None,
        'lontano': None,
        'schetchy': (None, None),
        'persone': (None, None),
        'note': None,
        'tipologia': 'Freestyle / Highline',
        # 27/10/2026: la foto del vicino (70_01) era della 53 m, ora anfiteatro-53_04
        'foto_vicino': None,
        'foto_lontano': ('cavalletto di tre pali; slinghe verdi annodate a una corda doppia che '
                         'esce dall’inquadratura; una slinga su una protezione bianca attorno '
                         'a un masso, fino a un alberello [DA CONFERMARE: a che cosa sia '
                         'chiusa]'),
        'da_confermare': 'il lato «vicino», senza foto; a che cosa sia ancorata la corda '
                         'doppia; lato di tensione; data delle foto',
    },
}


def di(id_linea):
    """La voce di una linea, o None se il file non la compila e non la fotografa."""
    return LINEE.get(id_linea)


# Sintesi per la guida: tre righe per linea su cio' che le foto mostrano, senza
# fatti nuovi rispetto a 'foto_vicino' e 'foto_lontano' qui sopra. La guida stampa
# questa, con la fotografia; le righe complete del file vanno nel fascicolo di
# rilievo, dove servono a chi va a rilevare (edizione 0.4, decisione E).
SINTESI = {
    'anfiteatro-46': (
        'A un capo un cavalletto di due pali di legno, d’estate; all’altro un punto fisso su '
        'roccia: placchetta con dado e grillo a lira, brache lilla.'),
    'anfiteatro-97': (
        'Linee in controluce verso la torre di fronte. A un capo brache viola fra gli alberi, '
        'riunite da un grillo, un moschettone su un elemento metallico nella roccia e un palo '
        'legato a un tronco: se l’ancoraggio sia sugli alberi, sulla roccia o su entrambi '
        '[DA CONFERMARE]. Il file la chiama «91»: che sia questa linea [DA CONFERMARE].'),
    'anfiteatro-113': (
        'Cavalletti di legno in tre forme (due pali tondi, tre pali, due assi squadrate); la '
        'linea verso una torre di roccia e, sotto, il backup a festoni. All’altro capo la '
        'sosta con il tronco, una '
        'slinga su moschettone a ghiera e placchetta con dado.'),
    'despedida-60': (
        'Un tronco sottile in piedi con protezione, slinga e corda arancione; accanto un '
        'tronco inclinato e bastoni incrociati [DA CONFERMARE: se siano un cavalletto]. Una '
        'fettuccia «GIBBON» passa accanto a tre moschettoni sul bordo e gira attorno alla '
        'base di un albero: se l’ancoraggio sia sugli alberi [DA CONFERMARE].'),
    'despedida-70': (
        'A un capo un cavalletto di tre pali, slinghe verdi annodate a una corda doppia e '
        'una protezione bianca attorno a un masso, fino a un alberello: a che cosa sia chiusa '
        '[DA CONFERMARE]. Dell’altro capo nessuna foto.'),
}


def sintesi(id_linea):
    return SINTESI.get(id_linea)
