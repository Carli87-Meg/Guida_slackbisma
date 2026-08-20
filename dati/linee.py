# -*- coding: utf-8 -*-
"""Registro delle highline della Pietra di Bismantova.

Dati puri, nessuna dipendenza da ReportLab: li legge sia il build del manuale
sia qualunque altro strumento.

FONTI — e solo queste:

* **locandina** «La Pietra — Yeah Vez!», fornita dall'utente: censisce cinque
  aree e ventiquattro linee. E' la fonte dell'elenco e delle lunghezze.
* **i-pietra**, catalogo consultato in sola lettura: ne registra dodici, e
  accorpa Anfite-altro dentro Anfiteatro. Confermato a immagine dai render 3D
  del settore Anfiteatro e del settore Rookie (20/08/2026), dove le etichette
  leggibili coincidono riga per riga con la tabella di NOTE_RIGGING.md.

Il confronto fra le due fonti sta in NOTE_RIGGING.md, sezione «La locandina non
coincide con i-pietra», ed e' gia' stato validato dall'utente.

**Nessuna lunghezza qui e' misurata sul posto.** Sono tutti valori di catalogo:
il dubbio 1 di DUBBI.md tiene aperta la rimisurazione della 53 m, e per le altre
ventitre' non esiste nemmeno un tentativo di misura.
"""

# stato della documentazione di rigging di una linea
DOCUMENTATA = 'documentata'          # esistono video, trascrizioni, fotogrammi
NON_DOCUMENTATA = 'non documentata'  # si conosce solo nome, settore, lunghezza

# settore secondo la locandina -> settore secondo i-pietra
# (None = il settore non compare affatto nel catalogo i-pietra)
SETTORE_IPIETRA = {
    'Rookie': 'Rookie',
    'Settore Giallo': None,
    'Anfiteatro': 'Anfiteatro',
    'Anfite-altro': 'Anfiteatro',    # i-pietra le accorpa dentro Anfiteatro
    'Despedida': None,
}

# Ordine di presentazione delle aree, come sulla locandina.
AREE = ['Rookie', 'Settore Giallo', 'Anfiteatro', 'Anfite-altro', 'Despedida']

# (settore locandina, lunghezza m, presente in i-pietra, stato)
_GREZZO = [
    ('Rookie',         18,  True,  NON_DOCUMENTATA),
    ('Rookie',         27,  True,  NON_DOCUMENTATA),
    ('Rookie',         40,  True,  NON_DOCUMENTATA),
    ('Rookie',         60,  True,  NON_DOCUMENTATA),

    ('Settore Giallo', 28,  False, NON_DOCUMENTATA),
    ('Settore Giallo', 45,  False, NON_DOCUMENTATA),
    ('Settore Giallo', 50,  False, NON_DOCUMENTATA),
    ('Settore Giallo', 55,  False, NON_DOCUMENTATA),

    ('Anfiteatro',     20,  False, NON_DOCUMENTATA),
    ('Anfiteatro',     27,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',     46,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',     53,  True,  DOCUMENTATA),      # la linea del manuale
    ('Anfiteatro',     97,  True,  NON_DOCUMENTATA),
    ('Anfiteatro',    108,  False, NON_DOCUMENTATA),
    ('Anfiteatro',    113,  True,  NON_DOCUMENTATA),

    ('Anfite-altro',   22,  True,  NON_DOCUMENTATA),
    ('Anfite-altro',   30,  True,  NON_DOCUMENTATA),
    ('Anfite-altro',  135,  True,  NON_DOCUMENTATA),

    ('Despedida',      35,  False, NON_DOCUMENTATA),
    ('Despedida',      45,  False, NON_DOCUMENTATA),
    ('Despedida',      60,  False, NON_DOCUMENTATA),
    ('Despedida',      70,  False, NON_DOCUMENTATA),
    ('Despedida',      85,  False, NON_DOCUMENTATA),
    ('Despedida',     165,  False, NON_DOCUMENTATA),
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
        'documentate': len(documentate()),
    }


# Discrepanza fra le due fonti sul nome del settore: i-pietra chiama
# «Anfiteatro» anche le tre linee che la locandina mette sotto «Anfite-altro».
# Va dichiarata nel manuale, non risolta d'ufficio: e' lo stesso tipo di
# ambiguita' del dubbio 45.
SETTORI_IN_CONFLITTO = ['Anfite-altro']


if __name__ == '__main__':
    c = conteggi()
    print('linee totali: %(totale)d · in i-pietra: %(in_ipietra)d · '
          'documentate: %(documentate)d' % c)
    for a in AREE:
        ls = per_area(a)
        print('  %-15s %d linee: %s' % (
            a, len(ls), ' · '.join(str(l['lunghezza']) for l in ls)))
