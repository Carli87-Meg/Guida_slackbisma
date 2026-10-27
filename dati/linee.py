# -*- coding: utf-8 -*-
"""Registro delle highline della Pietra di Bismantova.

Dati puri, nessuna dipendenza da ReportLab: li legge sia il build della guida sia
qualunque altro strumento. Qui stanno le ventiquattro linee con settore, codice,
nome, lunghezza di catalogo e il loro **livello di documentazione**, che non si
dichiara: si calcola da cio' che esiste (una scheda in `dati/schede/`, fotografie
in `lavorazione/foto_linee/`).

FONTI — e solo queste:

* **locandina** «La Pietra — Yeah Vez!», fornita dall'utente: censisce cinque
  aree e ventiquattro linee. E' la fonte dell'elenco e delle lunghezze.
* **i-pietra**, catalogo consultato in sola lettura. Accorpa Anfite-altro dentro
  Anfiteatro. La copertura e' cambiata nel tempo (IPIETRA_STORIA): al 21/10/2026
  registra tutte e 24 le linee; i render del 20/08/2026, che la guida stampa, ne
  mostrano 22 (la 20 m e la 108 m dell'Anfiteatro sono state create il
  21/08/2026). Dubbio 53 di DUBBI.md, chiuso e aggiornato.
* **SlackMap** (International Slackline Association), letta dall'API il
  27/10/2026 (tools/06_slackmap.py -> dati/slackmap.py): censisce tutte e 24 le
  linee, con nome, lunghezza del segmento disegnato e coordinate dei due capi.
  Gli id sono quelli abbinati dall'utente nel lotto 31 di i-pietra (20/10/2026).
  Le coordinate non sono misurate: sulla 53 m scartano di 10-19 m verso ovest
  rispetto alle letture del telefono fatte agli ancoraggi.

Il confronto fra locandina e i-pietra sta in NOTE_RIGGING.md, sezione «La
locandina non coincide con i-pietra», ed e' gia' stato validato dall'utente.

**Nessuna lunghezza qui e' misurata sul posto.** Sono tutti valori di catalogo:
il dubbio 1 di DUBBI.md tiene aperta la rimisurazione della 53 m, e per le altre
ventitre' non esiste nemmeno un tentativo di misura.
"""
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FOTO_LINEE = RADICE / 'lavorazione' / 'foto_linee'
_ESTENSIONI = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

# ---------------------------------------------------------------- livelli
# Il livello di documentazione di una linea. E' la legenda della guida («Come
# leggere questa guida») e si calcola in livello(): nessuna linea lo dichiara.
CENSITA, FOTOGRAFATA, RILEVATA, DOCUMENTATA = 0, 1, 2, 3
LIVELLI = {
    CENSITA: ('censita',
              'Se ne conoscono settore e lunghezza di catalogo. Nessuna ripresa, nessuna '
              'fotografia, nessun rilievo.'),
    FOTOGRAFATA: ('fotografata',
                  'Esistono fotografie della linea montata: mostrano che è stata attrezzata '
                  'e camminata, non come è stata ancorata.'),
    RILEVATA: ('rilevata',
               'La scheda di rilievo è stata compilata sul posto da chi ha montato: punti, '
               'materiale, coordinate.'),
    DOCUMENTATA: ('documentata',
                  'Il montaggio è documentato da riprese e fotogrammi, con i dubbi chiusi da '
                  'chi ha montato.'),
}

# settore secondo la locandina -> settore secondo i-pietra
SETTORE_IPIETRA = {
    'Rookie': 'Rookie',
    'Settore Giallo': 'Settore Giallo',
    'Anfiteatro': 'Anfiteatro',
    'Anfite-altro': 'Anfiteatro',    # i-pietra le accorpa dentro Anfiteatro
    'Despedida': 'Despedida',
}

# Sigla di ogni settore: con il numero d'ordine forma il codice della linea
# («AN-4»), che e' il nome stabile con cui la guida la cita (edizione 0.4,
# decisione B dell'utente). Il numero segue l'ordine della locandina dentro il
# settore, per lunghezza crescente.
CODICE_SETTORE = {
    'Rookie': 'RK',
    'Anfiteatro': 'AN',
    'Anfite-altro': 'AA',
    'Settore Giallo': 'SG',
    'Despedida': 'DE',
}

# Ordine di presentazione delle aree: come stanno sulla cresta, da sinistra a
# destra nella vista d'insieme di i-pietra (fonti/render_ipietra/panoramica.jpg,
# settori indicati dall'utente il 21/08/2026). La locandina resta la fonte di QUALI
# linee esistono e di quanto sono lunghe; qui cambia soltanto l'ordine.
AREE = ['Rookie', 'Anfiteatro', 'Anfite-altro', 'Settore Giallo', 'Despedida']

# La copertura di i-pietra cambia nel tempo: si stampa sempre con la sua data.
IPIETRA_STORIA = [
    ('05/08/2026', 12, 'snapshot di catalog-admin, senza Despedida e Settore Giallo'),
    ('20/08/2026', 22, 'render 3D dei cinque settori'),
    ('21/10/2026', 24, 'export di i-pietra e lotto 31'),
]
IPIETRA_DATA = IPIETRA_STORIA[-1][0]
RENDER_DATA = '20/08/2026'

# Linee che i render del 20/08/2026 non mostrano perche' in i-pietra sono state
# create il 21/08/2026 (createdAt nell'export del 21/10/2026).
DOPO_I_RENDER = {'anfiteatro-20', 'anfiteatro-108'}

# Nomi propri delle linee: quelli che hanno su SlackMap (dati/slackmap.py, letto
# dall'API con gli id abbinati dall'utente nel lotto 31 di i-pietra, 20/10/2026).
# Su SlackMap molti sono tutti in maiuscolo: qui si scrivono con la sola iniziale
# maiuscola, come l'utente ha deciso per i-pietra il 21/10/2026. GAS-OH resta
# GAS-OH per la decisione D3 (27/10/2026). Le linee senza nome restano senza.
import slackmap as _SM

_NOMI_FISSI = {'anfiteatro-53': 'GAS-OH'}


def _nome_da_slackmap(id_linea):
    if id_linea in _NOMI_FISSI:
        return _NOMI_FISSI[id_linea]
    v = _SM.di(id_linea)
    n = (v or {}).get('nome')
    if not n:
        return None
    return n[0] + n[1:].lower() if n.isupper() else n


NOMI = {l: _nome_da_slackmap(l) for l in _SM.LINEE}
# Soprannomi del gruppo, da stampare accanto al nome e mai da soli.
SOPRANNOMI = {
    'anfiteatro-53': 'la 50',
}

# (settore locandina, lunghezza m, presente in i-pietra al 21/10/2026)
_GREZZO = [
    ('Rookie',         18,  True),
    ('Rookie',         27,  True),
    ('Rookie',         40,  True),
    ('Rookie',         60,  True),

    ('Settore Giallo', 28,  True),
    ('Settore Giallo', 45,  True),
    ('Settore Giallo', 50,  True),
    ('Settore Giallo', 55,  True),

    # 20 e 108: assenti dai render del 20/08, censite dal 21/08 (DOPO_I_RENDER)
    ('Anfiteatro',     20,  True),
    ('Anfiteatro',     27,  True),
    ('Anfiteatro',     46,  True),
    ('Anfiteatro',     53,  True),      # GAS-OH, la linea documentata
    ('Anfiteatro',     97,  True),
    ('Anfiteatro',    108,  True),
    ('Anfiteatro',    113,  True),

    ('Anfite-altro',   22,  True),
    ('Anfite-altro',   30,  True),
    ('Anfite-altro',  135,  True),

    ('Despedida',      35,  True),
    ('Despedida',      45,  True),
    ('Despedida',      60,  True),
    ('Despedida',      70,  True),
    ('Despedida',      85,  True),
    ('Despedida',     165,  True),
]


def _slug(settore, lunghezza):
    base = settore.lower().replace(' ', '-').replace('à', 'a')
    return '%s-%d' % (base, lunghezza)


def _costruisci():
    linee, contatore = [], {}
    for settore, lung, in_ipietra in _GREZZO:
        contatore[settore] = contatore.get(settore, 0) + 1
        id_ = _slug(settore, lung)
        linee.append({
            'id': id_,
            'codice': '%s-%d' % (CODICE_SETTORE[settore], contatore[settore]),
            'settore': settore,
            'settore_ipietra': SETTORE_IPIETRA[settore] if in_ipietra else None,
            'lunghezza': lung,
            'nome': NOMI.get(id_),
            'soprannome': SOPRANNOMI.get(id_),
            'slackmap': _SM.di(id_),
            'in_ipietra': in_ipietra,
            # tracciata sui render del 20/08/2026, quelli che la guida stampa
            'sul_render': in_ipietra and id_ not in DOPO_I_RENDER,
        })
    return linee


LINEE = _costruisci()
_PER_ID = {l['id']: l for l in LINEE}


def di(id_linea):
    return _PER_ID.get(id_linea)


def per_area(area):
    return [l for l in LINEE if l['settore'] == area]


def in_ordine():
    """Le linee nell'ordine della cresta: per settore, poi per lunghezza."""
    return [l for area in AREE for l in per_area(area)]


# ---------------------------------------------------------------- nomi
def nome(l):
    """Nome completo: nome proprio se c'e', poi settore e lunghezza."""
    if l['nome']:
        return '%s · %s' % (l['nome'], nome_catalogo(l))
    return nome_catalogo(l)


def nome_catalogo(l):
    """«Anfiteatro · 53 m»: settore e lunghezza, mai la lunghezza da sola."""
    return '%s · %d m' % (l['settore'], l['lunghezza'])


def titolo(l):
    """Il titolo della scheda: il nome proprio, altrimenti settore e lunghezza."""
    return l['nome'] or nome_catalogo(l)


# ---------------------------------------------------------------- livello
def foto_di(l):
    """Fotografie della linea montata, se qualcuno ne ha messe.

    Una cartella per linea in lavorazione/foto_linee/, chiamata con l'id. La prima
    in ordine di nome e' la miniatura stampata: per convenzione la 01, che non deve
    mostrare volti riconoscibili (vedi il LEGGIMI li' dentro).
    """
    d = FOTO_LINEE / l['id']
    if not d.is_dir():
        return []
    return sorted(f for f in d.iterdir() if f.suffix in _ESTENSIONI)


def scheda_di(l):
    """La scheda di dati della linea (dati/schede/<id>.py), o None."""
    import schede
    return schede.di(l['id'])


def livello(l):
    """Il livello di documentazione, calcolato da cio' che esiste.

    Una scheda con un montaggio documentato vale «documentata»; una scheda nata
    da un rilievo sul campo vale «rilevata»; una cartella di fotografie vale
    «fotografata»; altrimenti la linea e' soltanto censita.
    """
    s = scheda_di(l)
    if s is not None and s.get('montaggi'):
        return DOCUMENTATA
    if s is not None and s.get('rilievo'):
        return RILEVATA
    if foto_di(l):
        return FOTOGRAFATA
    return CENSITA


def nome_livello(l):
    return LIVELLI[livello(l)][0]


def documentate():
    return [l for l in in_ordine() if livello(l) == DOCUMENTATA]


def da_documentare():
    """Le linee senza documentazione di rigging: hanno una scheda di rilievo."""
    return [l for l in in_ordine() if livello(l) < DOCUMENTATA]


def fotografate():
    return [l for l in in_ordine() if livello(l) == FOTOGRAFATA]


def conteggi():
    c = {'totale': len(LINEE),
         'in_ipietra': sum(1 for l in LINEE if l['in_ipietra']),
         'sul_render': sum(1 for l in LINEE if l['sul_render'])}
    for liv in LIVELLI:
        c[LIVELLI[liv][0]] = sum(1 for l in LINEE if livello(l) == liv)
    c['documentate'] = c['documentata']
    return c


def numero_scheda(l):
    """Numero della scheda di rilievo di una linea, nell'ordine della cresta.

    Le schede stanno in un fascicolo a parte: un numero di pagina del fascicolo
    stampato nella guida si confonderebbe con le pagine della guida stessa. Il
    numero di scheda no, ed e' quello che si scrive sul foglio.
    """
    for i, x in enumerate(da_documentare(), start=1):
        if x['id'] == l['id']:
            return i
    return None


# Discrepanza fra le due fonti sul nome del settore: nei render i-pietra del
# 20/08/2026 le tre linee che la locandina mette sotto «Anfite-altro» sono
# etichettate «Anfiteatro», e nel catalogo stanno nel settore anfiteatro.
# Decisione D4 dell'utente (27/10/2026, dubbio 52 chiuso): la guida usa il nome
# della locandina, «Anfite-altro», e dove cita i-pietra dice come le etichetta.
SETTORI_IN_CONFLITTO = ['Anfite-altro']

# La 50 m del Settore Giallo e' l'altra «50» della Pietra. «La 50» e' il soprannome
# che il gruppo da' alla 53 m dell'Anfiteatro, GAS-OH (decisione D3). La nota resta
# dove c'e' il rischio di confondersi: nel glossario e sotto la tabella del Settore
# Giallo (nota N3 di DUBBI.md).
COLLISIONE_NOME = ['settore-giallo-50']

# Settori la cui presenza in i-pietra non e' stata verificata su un render.
NON_VERIFICATI = []


# ---------------------------------------------------------------- rilievo
# Campi che una scheda di linea non ancora documentata chiede di compilare sul
# campo. Sono qui, e non nell'impaginazione, per la stessa ragione delle
# lunghezze: i dati stanno in un posto solo.
#
# L'elenco ricalca le voci che per la 53 m sono state ricavate dalle riprese e
# quelle che in DUBBI.md risultano ancora aperte anche per quella linea: cio' che
# e' mancato una volta manchera' anche alle altre. Dall'edizione 0.4 chiede anche
# le coordinate dei due capi (dubbio 3), quale lato e' quello di tensione (56, 60)
# e l'A-frame (50): erano i dati che per la 53 m si sono dovuti ricostruire.
#
# Ogni voce e' (etichetta, righe_di_scrittura). Le righe sono un'indicazione di
# spazio; il passo lo calcola l'impaginazione perche' la scheda arrivi a fondo pagina.
CAMPI_RILIEVO = [
    ('Nome (SlackMap) e tipologia', 1),
    ('Lunghezza misurata sui punti', 1),
    ('Dislivello / offlevel', 1),
    ('Lato di tensione: A o B, e perché', 1),
    ('Coordinate GPS lato A', 1),
    ('Coordinate GPS lato B', 1),
    ('Ancoraggio lato A — tipo e numero punti', 3),
    ('Ancoraggio lato B — tipo e numero punti', 3),
    ('Angolo di apertura', 1),
    ('Collegamento fra i punti', 2),
    ('Nastro e backup della linea, leash', 2),
    ('Materiale del lato tensione', 2),
    ('A-frame: se c’è, da che lato, com’è fatto', 2),
    ('Accesso e avvicinamento', 2),
    ('Vincoli: autorizzazioni, stagionalità', 1),
    ('Rilevata da · data del rilievo', 1),
]

# Le fotografie da fare quando si rileva una linea: ciascuna e' una foto che per la
# 53 m e' mancata, con il dubbio di DUBBI.md che l'ha fatta mancare.
FOTO_DA_FARE = [
    ('Ogni ancoraggio d’insieme, con tutti i punti nell’inquadratura', 28),
    ('Ogni punto da vicino: placchetta, dado, bullone, con un riferimento di misura', 39),
    ('Le etichette di ogni braca, distese e leggibili', 37),
    ('Il materiale steso prima di montare, etichette in vista', 37),
    ('L’A-frame intero e i suoi piedi, con un riferimento di misura', 50),
    ('Il weblock, il blocco del backup e l’anti-slip, da vicino', 31),
    ('La linea intera dal bordo, da tutti e due i capi', 54),
]

# Il protocollo di rilievo: che cosa misurare, dichiarare e fotografare. E' la
# lezione del montaggio della 53 m, scritta come istruzione. Ogni voce e'
# (titolo, dettaglio).
PROTOCOLLO_RILIEVO = [
    ('Dichiarare il lato di tensione',
     'Prima di tutto, a voce e sulla scheda: quale capo ha sosta main, sosta backup e '
     'sistema di tensione. Per la 53 m è stato ricostruito dopo.'),
    ('Segnare la posizione ai due capi',
     'Una lettura GPS stando sull’ancoraggio, per ciascun capo, con l’ora. Serve ad '
     'avvicinarsi, non a ritrovare il singolo punto.'),
    ('Contare e fotografare i punti',
     'Quanti sono, di che tipo, come sono collegati; una foto d’insieme e una per punto, '
     'con un riferimento di misura accanto al bullone.'),
    ('Leggere le etichette',
     'La portata di una braca è solo quella stampata sull’etichetta: fotografarla distesa, '
     'per ogni braca usata, sapendo di chi è il pezzo.'),
    ('Misurare la linea',
     'Lunghezza sui punti e dislivello fra i due capi. Le lunghezze di catalogo non sono '
     'misure.'),
    ('Elencare il materiale con le misure',
     'Quantità, lunghezze, diametri, modelli: ciò che nei video della 53 m non è mai stato '
     'detto.'),
    ('Annotare l’A-frame',
     'Se c’è, da che lato, altezza e diametro dei pali, come è legato in testa, se i piedi '
     'sono fermati.'),
    ('Scrivere chi, quando, quanto',
     'Presenti, data, ora di inizio e fine, quante persone sono servite davvero.'),
]

# Il rilievo dello spot: le domande a cui la guida non puo' rispondere senza il
# gruppo (dubbi 4, 5, 36). Un foglio nel fascicolo, con questi campi.
CAMPI_SPOT = (
    [('Avvicinamento a %s: sentiero, tempi' % a, 2) for a in AREE]
    + [('Parcheggio e punto di partenza', 2),
       ('Autorizzazioni, accordi con il gestore', 2),
       ('Divieti stagionali: nidificazione, altro', 2),
       ('Linee lasciate montate, notte, permarig', 2),
       ('Emergenze: numeri, punto di raccolta, rifugio', 2),
       ('Referente della guida e correzioni', 2),
       ('Rilevato da', 1),
       ('Data', 1)])


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
        for l in in_ordine():
            print('%-18s %-5s %s' % (l['id'], l['codice'], nome(l)))
        raise SystemExit(0)
    c = conteggi()
    print('linee totali: %(totale)d · in i-pietra: %(in_ipietra)d · '
          'sui render: %(sul_render)d' % c)
    print('livelli: ' + ' · '.join('%s %d' % (LIVELLI[k][0], c[LIVELLI[k][0]])
                                    for k in LIVELLI))
    for a in AREE:
        ls = per_area(a)
        print('  %-15s %d linee: %s' % (
            a, len(ls), ' · '.join('%s %d' % (l['codice'], l['lunghezza']) for l in ls)))
