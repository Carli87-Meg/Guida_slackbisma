# Fotografie degli ancoraggi

Le foto che documentano **i punti di sosta**, scattate sul campo. Sono la fonte
che manca al manuale: la scheda dell'Anfiteatro 53 m dichiara oggi, per iscritto,
che «nessuna immagine disponibile inquadra i tre punti insieme, e l'angolo di
apertura non è quindi verificabile».

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

`A_` e `B_` davanti al nome, con il lato dichiarato da chi ha scattato. **Non si
ricava dall'immagine**: due soste di arenaria si somigliano, e attribuire un
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
