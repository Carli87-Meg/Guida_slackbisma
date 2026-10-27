# Fotografie degli ancoraggi

Le foto che documentano **i punti di sosta**, scattate sul campo. Sono la fonte
che manca al manuale: la scheda dell'Anfiteatro 53 m chiede ancora, fra le cose da
rilevare, «una fotografia d'insieme dei tre punti, per l'angolo di apertura».

In `anfiteatro-53/` ci sono otto scatti del 22/08/2026 all'altro capo della linea,
fra `IMG_3323` e `IMG_3332` (data e GPS in `lavorazione/metadati_foto.md`). Sono del
**lato statico**: il 27/10/2026 l'utente ha dichiarato che la tensione sta sul capo sopra
il settore Cocoa, cioè al main (dubbio 56, chiuso). Restano senza prefisso perché il build
li usa con il nome originale.

Una cartella per linea, chiamata con l'**id** che la linea ha in `dati/linee.py`
— settore in minuscolo, spazi sostituiti da trattini, poi la lunghezza in metri:

```
lavorazione/ancoraggi/
  anfiteatro-53/
    A_insieme.jpg          lato A, i punti tutti insieme
    A_punto1_targhetta.jpg
    B_insieme.jpg          lato B
```

Gli id validi si stampano con `python dati/linee.py --id`.

## Il nome del file dice il lato

`A_` e `B_` davanti al nome, con il lato dichiarato da chi ha scattato (nella guida
i lati si chiamano **di tensione** e **statico**: chi scatta dica quale dei due è
A). **Non si ricava dall'immagine**: due soste di arenaria si somigliano, e attribuire un
ancoraggio al lato sbagliato è l'errore che manda a montare dalla parte sbagliata.
Se il lato non è noto, il file resta senza prefisso e la didascalia lo dice.

## Ingresso

```
python tools/importa_foto.py --in <file...> --out lavorazione/ancoraggi/anfiteatro-53
```

Raddrizza secondo l'EXIF, riduce il lato lungo a 2000 px e **stampa i metadati**:
data e ora dello scatto, dispositivo, e le coordinate GPS se il telefono le ha
registrate. Le coordinate sono dati veri quanto il parlato dei video: il dubbio 3
di `DUBBI.md` — le coordinate dei due ancoraggi — si chiude con una foto
geolocalizzata, non con una stima sulla mappa.

Con `--solo-dati` legge e non scrive niente.

## Che cosa può chiudere una fotografia, e che cosa no

| Dubbio | Serve | Si chiude a immagine? |
|---|---|---|
| 28 · collegamento ed equalizzazione dei tre punti | inquadratura d'insieme del lato A | sì, se si vedono i tre punti e il masterpoint |
| 38 · protezione veloce accanto ai fissi | stessa inquadratura, a fuoco | sì |
| 37 · portata delle slinghe | **etichetta cucita** della braca, leggibile | solo l'etichetta: il colore non è una marcatura |
| 39 · marca e diametro del bullone | dettaglio ravvicinato della placchetta | la marca sì, il diametro **no** — serve una misura |
| 3 · coordinate degli ancoraggi | GPS nell'EXIF | sì, se il telefono lo registra |
| — · numero dei punti sul lato B | inquadratura del lato B | sì |

Una misura non si legge in fotografia. Diametri, lunghezze e angoli restano
`[DA CONFERMARE]` finché qualcuno non li misura sul posto, anche quando la foto
è nitida: è la regola numero uno di `CLAUDE.md`, e vale soprattutto qui.
