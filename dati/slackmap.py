# -*- coding: utf-8 -*-
"""Le linee della Pietra su SlackMap. FILE GENERATO: non modificare a mano.

Scritto da tools/06_slackmap.py il 27/10/2026, dall'API pubblica
https://api.slackmap.com/line/<id>/details. Gli id vengono dal lotto 31 del
catalogo i-pietra (20/10/2026), dove l'utente ha abbinato ogni linea della
locandina alla sua voce SlackMap.

Le coordinate sono quelle del segmento DISEGNATO sulla mappa, non misurate
(`misurata` e' falso per tutte): sulla 53 m risultano spostate di 10-19 m
verso ovest rispetto alle letture del telefono fatte agli ancoraggi. Servono
ad avvicinarsi, non a trovare un punto. La lunghezza e' quella del segmento.
"""

LETTO_IL = '27/10/2026'

# id linea -> dati SlackMap
LINEE = {
    'rookie-18': {
        'id': 'Sn8f0SS',
        'nome': 'Trapano?',
        'lunghezza_segmento': 17.7,
        'misurata': False,
        'capi': [(44.419490, 10.409120), (44.419390, 10.409300)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/Sn8f0SS',
    },
    'rookie-27': {
        'id': 'r3yyHbn',
        'nome': 'OCIO',
        'lunghezza_segmento': 26.7,
        'misurata': False,
        'capi': [(44.419460, 10.409040), (44.419350, 10.409340)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/r3yyHbn',
    },
    'rookie-40': {
        'id': '8y7K14L',
        'nome': 'Bella il Prof!',
        'lunghezza_segmento': 39.7,
        'misurata': False,
        'capi': [(44.419410, 10.409060), (44.419210, 10.409480)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/8y7K14L',
    },
    'rookie-60': {
        'id': 'O9z7pFx',
        'nome': 'Highline Tribe',
        'lunghezza_segmento': 60.0,
        'misurata': False,
        'capi': [(44.419400, 10.408950), (44.419030, 10.409490)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/O9z7pFx',
    },
    'anfiteatro-20': {
        'id': 'JG8Yi5z',
        'nome': 'APPUNTAMENTO AL BUIO',
        'lunghezza_segmento': 19.5,
        'misurata': False,
        'capi': [(44.419750, 10.411910), (44.419600, 10.411780)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/JG8Yi5z',
    },
    'anfiteatro-27': {
        'id': 'PX29ZPA',
        'nome': 'BATTESIMO',
        'lunghezza_segmento': 26.5,
        'misurata': False,
        'capi': [(44.419580, 10.411810), (44.419770, 10.412010)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/PX29ZPA',
    },
    'anfiteatro-46': {
        'id': 'FlwIt50',
        'nome': 'Double Rainbow',
        'lunghezza_segmento': 46.0,
        'misurata': False,
        'capi': [(44.419910, 10.412290), (44.420050, 10.412830)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/FlwIt50',
    },
    'anfiteatro-53': {
        'id': 'nym-s4g',
        'nome': 'GAS-OH',
        'lunghezza_segmento': 52.8,
        'misurata': False,
        'capi': [(44.419500, 10.411840), (44.419890, 10.412220)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/nym-s4g',
    },
    'anfiteatro-97': {
        'id': 'F4sDJKQ',
        'nome': '420',
        'lunghezza_segmento': 96.9,
        'misurata': False,
        'capi': [(44.419440, 10.411870), (44.420020, 10.412790)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/F4sDJKQ',
    },
    'anfiteatro-108': {
        'id': 'mXFD-6Q',
        'nome': None,
        'lunghezza_segmento': 107.7,
        'misurata': False,
        'capi': [(44.419390, 10.411880), (44.420040, 10.412890)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/mXFD-6Q',
    },
    'anfiteatro-113': {
        'id': 't2qJAK8',
        'nome': 'Brifing',
        'lunghezza_segmento': 113.2,
        'misurata': False,
        'capi': [(44.419360, 10.411910), (44.420030, 10.412970)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/t2qJAK8',
    },
    'anfite-altro-22': {
        'id': 'UQ2_y7z',
        'nome': 'La Borra',
        'lunghezza_segmento': 21.8,
        'misurata': False,
        'capi': [(44.420130, 10.413090), (44.420280, 10.413270)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/UQ2_y7z',
    },
    'anfite-altro-30': {
        'id': '1SJ6phO',
        'nome': 'CATCH ME BABY',
        'lunghezza_segmento': 29.6,
        'misurata': False,
        'capi': [(44.420100, 10.413130), (44.420300, 10.413380)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/1SJ6phO',
    },
    'anfite-altro-135': {
        'id': 'QPp5V-S',
        'nome': None,
        'lunghezza_segmento': 134.8,
        'misurata': False,
        'capi': [(44.420070, 10.413160), (44.420770, 10.414540)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/QPp5V-S',
    },
    'settore-giallo-28': {
        'id': 'NYQcHAC',
        'nome': None,
        'lunghezza_segmento': 34.9,
        'misurata': False,
        'capi': [(44.423380, 10.415230), (44.423060, 10.415240)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/NYQcHAC',
    },
    'settore-giallo-45': {
        'id': 'UvttZ72',
        'nome': None,
        'lunghezza_segmento': 44.9,
        'misurata': False,
        'capi': [(44.423390, 10.415270), (44.422990, 10.415360)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/UvttZ72',
    },
    'settore-giallo-50': {
        'id': 'aUYtQdd',
        'nome': None,
        'lunghezza_segmento': 49.9,
        'misurata': False,
        'capi': [(44.423390, 10.415300), (44.422960, 10.415480)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/aUYtQdd',
    },
    'settore-giallo-55': {
        'id': 'jKzSch5',
        'nome': None,
        'lunghezza_segmento': 54.6,
        'misurata': False,
        'capi': [(44.423380, 10.415380), (44.422910, 10.415590)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/jKzSch5',
    },
    'despedida-35': {
        'id': 'svysOPW',
        'nome': None,
        'lunghezza_segmento': 34.8,
        'misurata': False,
        'capi': [(44.422810, 10.414950), (44.422520, 10.414790)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/svysOPW',
    },
    'despedida-45': {
        'id': '4z4WcEl',
        'nome': 'FATTI L.8 BEL',
        'lunghezza_segmento': 44.6,
        'misurata': False,
        'capi': [(44.422840, 10.415050), (44.422470, 10.414820)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/4z4WcEl',
    },
    'despedida-60': {
        'id': 'Rp-QqWJ',
        'nome': 'IL SASO',
        'lunghezza_segmento': 60.0,
        'misurata': False,
        'capi': [(44.422840, 10.415140), (44.422330, 10.414870)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/Rp-QqWJ',
    },
    'despedida-70': {
        'id': 'f4EyGNs',
        'nome': 'LA LENZA',
        'lunghezza_segmento': 70.0,
        'misurata': False,
        'capi': [(44.422830, 10.415250), (44.422240, 10.414940)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/f4EyGNs',
    },
    'despedida-85': {
        'id': 'PPySEMm',
        'nome': 'La Sposa',
        'lunghezza_segmento': 84.5,
        'misurata': False,
        'capi': [(44.422210, 10.414800), (44.421450, 10.414730)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/PPySEMm',
    },
    'despedida-165': {
        'id': 'pqhMd2D',
        'nome': 'S BEAM',
        'lunghezza_segmento': 164.5,
        'misurata': False,
        'capi': [(44.421310, 10.414780), (44.422730, 10.415390)],
        'creata': '2019-11-27',
        'url': 'https://slackmap.com/line/pqhMd2D',
    },
}


def di(id_linea):
    return LINEE.get(id_linea)


def mappa(lat, lon):
    return 'https://www.google.com/maps?q=%.6f,%.6f' % (lat, lon)
