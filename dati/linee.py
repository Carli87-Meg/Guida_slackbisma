# -*- coding: utf-8 -*-
"""Registro delle highline della Pietra di Bismantova.

Dati puri, nessuna dipendenza da ReportLab: li legge sia il build del manuale
sia qualunque altro strumento.

FONTI — e solo queste:

* **locandina** «La Pietra — Yeah Vez!», fornita dall'utente: censisce cinque
  aree e ventiquattro linee. E' la fonte dell'elenco e delle lunghezze.
* **i-pietra**, catalogo consultato in sola lettura. Accorpa Anfite-altro dentro
  Anfiteatro. La copertura e' stata verificata a immagine sui render 3D forniti
  dall'utente il 20/08/2026:

  - Anfiteatro e Rookie: le etichette leggibili coincidono riga per riga con la
    tabella di NOTE_RIGGING.md;
  - **Despedida: tutte e sei le linee risultano censite** (35, 45, 60, 70, 85,
    165 m). **Settore Giallo: censito**, tutte e quattro (28, 45, 50, 55 m).

    Questo non contraddice NOTE_RIGGING.md: lo contestualizza. Quella nota fu
    scritta il 19/08 leggendo l'unica fonte allora disponibile, lo snapshot
    `tool/catalog-admin/.cache/catalog-snapshot.json` **datato 5 agosto 2026**,
    che conteneva 551 rotte e 37 settori fra cui `despedida` e `settore-giallo`
    **non comparivano affatto**. Il conteggio di dodici su ventiquattro era
    dunque esatto per quello snapshot. I render sono di quindici giorni dopo: nel
    frattempo il catalogo e' stato ampliato, oppure i render leggono i dati vivi
    invece della cache. Vale il dato piu' recente, ma va sempre stampato con la
    sua data. Dubbio 53 di DUBBI.md.

  Esito al 20/08/2026: i-pietra copre **22 linee su 24**. Mancano solo la 20 m e
  la 108 m dell'Anfiteatro. Il conteggio di dodici che si legge in NOTE_RIGGING.md
  e' superato: dubbio 53, chiuso.

  **Al 21/10/2026 le linee sono 24 su 24** (letto il 27/10/2026): l'export
  Firestore di i-pietra del 21/10 e il lotto 31 (data/catalog/riscrittura/
  31-highline.md, applicato il 21/10) contengono anche la 20 m e la 108 m
  dell'Anfiteatro, create il 21/08/2026 (campo createdAt), il giorno dopo i
  render. I render del 20/08 restano le figure del catalogo e mostrano 22 linee:
  per questo il registro tiene due campi, `in_ipietra` (al 21/10) e `sul_render`
  (al 20/08). Dubbio 53, aggiornato.

Il confronto fra le due fonti sta in NOTE_RIGGING.md, sezione «La locandina non
coincide con i-pietra», ed e' gia' stato validato dall'utente.

**Nessuna lunghezza qui e' misurata sul posto.** Sono tutti valori di catalogo:
il dubbio 1 di DUBBI.md tiene aperta la rimisurazione della 53 m, e per le altre
ventitre' non esiste nemmeno un tentativo di misura.
"""

# stato della documentazione di rigging di una linea
DOCUMENTATA = 'documentata'          # esistono video, trascrizioni, fotogrammi
FOTOGRAFATA = 'fotografata'          # esistono foto della linea montata, non il rigging
NON_DOCUMENTATA = 'non documentata'  # si conosce solo nome, settore, lunghezza

# Lo stato «fotografata» non e' scritto qui: si ricava dalla presenza di una
# cartella in lavorazione/foto_linee/<id>/. Vedi il LEGGIMI li' dentro.
# Una foto della linea in opera NON documenta il rigging: mostra che la linea
# esiste ed e' stata camminata, non come e' stata ancorata.

# settore secondo la locandina -> settore secondo i-pietra
# (None = il settore non compare affatto nel catalogo i-pietra)
SETTORE_IPIETRA = {
    'Rookie': 'Rookie',
    'Settore Giallo': 'Settore Giallo',  # render 20/08/2026: tutte e quattro
    'Anfiteatro': 'Anfiteatro',
    'Anfite-altro': 'Anfiteatro',    # i-pietra le accorpa dentro Anfiteatro
    'Despedida': 'Despedida',  # render 20/08/2026: tutte e sei censite
}

# Ordine di presentazione delle aree: come stanno sulla cresta, da sinistra a
# destra nella vista d'insieme di i-pietra (fonti/render_ipietra/panoramica.jpg,
# settori indicati dall'utente il 21/08/2026).
#
# Prima era l'ordine della locandina, che metteva il Settore Giallo secondo
# mentre sulla montagna e' quarto. Un documento che si legge sul posto conviene
# che elenchi i settori nell'ordine in cui li si incontra: cosi' il catalogo, le
# schede di rilievo e i render si susseguono come la parete.
#
# La locandina resta la fonte di QUALI linee esistono e di quanto sono lunghe.
# Qui cambia soltanto l'ordine in cui vengono presentate.
AREE = ['Rookie', 'Anfiteatro', 'Anfite-altro', 'Settore Giallo', 'Despedida']

# La copertura di i-pietra cambia nel tempo: si stampa sempre con la sua data.
# Ogni riga: (data, linee censite, fonte). L'ultima e' quella che vale per
# `in_ipietra`; le altre sono la storia, e la guida la dichiara.
IPIETRA_STORIA = [
    ('05/08/2026', 12, 'snapshot di catalog-admin, senza Despedida e Settore Giallo'),
    ('20/08/2026', 22, 'render 3D dei cinque settori'),
    ('21/10/2026', 24, 'export di i-pietra e lotto 31'),
]
IPIETRA_DATA = IPIETRA_STORIA[-1][0]
RENDER_DATA = '20/08/2026'

# Linee che i render del 20/08/2026 non mostrano perche' in i-pietra sono state
# create il 21/08/2026 (createdAt nell'export del 21/10/2026): sono censite, ma
# non tracciate sulle figure che la guida stampa.
DOPO_I_RENDER = {'anfiteatro-20', 'anfiteatro-108'}

# (settore locandina, lunghezza m, presente in i-pietra al 21/10/2026, stato)
_GREZZO = [
    ('Rookie',         18,  True,  NON_DOCUMENTATA),
    ('Rookie',         27,  True,  NON_DOCUMENTATA),
    ('Rookie',         40,  True,  NON_DOCUMENTATA),
    ('Rookie',         60,  True,  NON_DOCUMENTATA),

    ('Settore Giallo', 28,  True, NON_DOCUMENTATA),
    ('Settore Giallo', 45,  True, NON_DOCUMENTATA),
    ('Settore Giallo', 50,  True, NON_DOCUMENTATA),
    ('Settore Giallo', 55,  True, NON_DOCUMENTATA),

    # 20 e 108: assenti dai render del 20/08, censite dal 21/08 (DOPO_I_RENDER)
    ('Anfiteatro',     20,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',     27,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',     46,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',     53,  True,  DOCUMENTATA),      # la linea del manuale: GAS-OH
    ('Anfiteatro',     97,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',    108,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',    113,  True,  NON_DOCUMENTATA),

    ('Anfite-altro',   22,  True,  NON_DOCUMENTATA),
    ('Anfite-altro',   30,  True,  NON_DOCUMENTATA),
    ('Anfite-altro',  135,  True,  NON_DOCUMENTATA),

    ('Despedida',      35,  True, NON_DOCUMENTATA),
    ('Despedida',      45,  True, NON_DOCUMENTATA),
    ('Despedida',      60,  True, NON_DOCUMENTATA),
    ('Despedida',      70,  True, NON_DOCUMENTATA),
    ('Despedida',      85,  True, NON_DOCUMENTATA),
    ('Despedida',     165,  True, NON_DOCUMENTATA),
]


def _slug(settore, lunghezza):
    base = settore.lower().replace(' ', '-').replace('à', 'a')
    return '%s-%d' % (base, lunghezza)


LINEE = [
    {
        'id': _slug(settore, lung),
        'settore': settore,
        'settore_ipietra': SETTORE_IPIETRA[settore] if in_ipietra else None,
        'lunghezza': lung,
        'in_ipietra': in_ipietra,
        # tracciata sui render del 20/08/2026, quelli che la guida stampa
        'sul_render': in_ipietra and _slug(settore, lung) not in DOPO_I_RENDER,
        'stato': stato,
    }
    for settore, lung, in_ipietra, stato in _GREZZO
]


def per_area(area):
    return [l for l in LINEE if l['settore'] == area]


def documentate():
    return [l for l in LINEE if l['stato'] == DOCUMENTATA]


def da_documentare():
    return [l for l in LINEE if l['stato'] != DOCUMENTATA]


def conteggi():
    return {
        'totale': len(LINEE),
        'in_ipietra': sum(1 for l in LINEE if l['in_ipietra']),
        'sul_render': sum(1 for l in LINEE if l['sul_render']),
        'documentate': len(documentate()),
    }


# Discrepanza fra le due fonti sul nome del settore: nei render i-pietra del
# 20/08/2026 le tre linee che la locandina mette sotto «Anfite-altro» sono
# etichettate «Anfiteatro», e nel catalogo stanno nel settore anfiteatro.
# Decisione D4 dell'utente (27/10/2026, dubbio 52 chiuso): il manuale usa il nome
# della locandina, «Anfite-altro», e dove cita i-pietra dice come le etichetta.
# (Dal 21/10 i-pietra ha anche un campo area «anfite-altro», ma lo ha preso dalla
# bozza della guida dell'8/10: non e' una seconda fonte.)
SETTORI_IN_CONFLITTO = ['Anfite-altro']

# La 50 m del Settore Giallo e' l'altra «50» della Pietra. «La 50» e' il soprannome
# che il gruppo da' alla 53 m dell'Anfiteatro, che nel titolo della guida si chiama
# GAS-OH (decisione D3 dell'utente, 27/10/2026, dubbio 45 chiuso). La nota
# sull'altra 50 m resta, ovunque compaia (nota N3 di DUBBI.md).
COLLISIONE_NOME = ['settore-giallo-50']

# Settori la cui presenza in i-pietra non e' stata verificata su un render.
# Vuoto: al 20/08/2026 esiste un render per tutti e cinque i settori.
NON_VERIFICATI = []


# ---------------------------------------------------------------- rilievo
# Campi che una scheda di linea non ancora documentata chiede di compilare sul
# campo. Sono qui, e non nell'impaginazione, per la stessa ragione delle
# lunghezze: i dati stanno in un posto solo.
#
# L'elenco ricalca le voci che per la 53 m sono state ricavate dalle riprese, e
# quelle che in DUBBI.md risultano ancora aperte anche per quella linea: cio' che
# e' mancato una volta manchera' anche alle altre.
#
# Ogni voce e' (etichetta, righe_di_scrittura).
# Etichetta e numero di righe su cui scrivere. Il numero di righe e' una
# indicazione di spazio, non un dato: descrivere un ancoraggio a tre punti
# richiede piu' spazio che scrivere una data. Il passo fra le righe lo calcola
# l'impaginazione perche' la scheda arrivi a fondo pagina.
CAMPI_RILIEVO = [
    ('Lunghezza misurata', 1),
    ('Dislivello / offlevel', 1),
    ('Ancoraggio lato A — tipo e numero punti', 3),
    ('Ancoraggio lato B — tipo e numero punti', 3),
    ('Angolo di apertura', 1),
    ('Collegamento fra i punti', 2),
    ('Nastro e backup della linea', 3),
    ('Materiale del lato tensione', 3),
    ('Accesso e avvicinamento', 3),
    ('Vincoli: autorizzazioni, stagionalita', 3),
    ('Rilevata da', 1),
    ('Data del rilievo', 1),
]


def campi_rilievo():
    """Copia dei campi di rilievo, cosi' chi impagina non muta l'originale."""
    return list(CAMPI_RILIEVO)


def aree_assenti_da_ipietra():
    return [a for a in AREE if not any(l['in_ipietra'] for l in per_area(a))]


def lunghezze_assenti(area):
    """Lunghezze di un'area presenti sulla locandina ma non in i-pietra."""
    return [l['lunghezza'] for l in per_area(area) if not l['in_ipietra']]


if __name__ == '__main__':
    import sys as _s
    if '--id' in _s.argv:
        for l in LINEE:
            print('%-18s %s · %d m' % (l['id'], l['settore'], l['lunghezza']))
        raise SystemExit(0)
    c = conteggi()
    print('linee totali: %(totale)d · in i-pietra: %(in_ipietra)d · '
          'sui render: %(sul_render)d · documentate: %(documentate)d' % c)
    for a in AREE:
        ls = per_area(a)
        print('  %-15s %d linee: %s' % (
            a, len(ls), ' · '.join(str(l['lunghezza']) for l in ls)))
