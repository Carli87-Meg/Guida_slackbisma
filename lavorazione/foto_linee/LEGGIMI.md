# Fotografie delle linee montate

Una cartella per linea, chiamata con l'**id** che la linea ha in `dati/linee.py`:
settore in minuscolo, spazi sostituiti da trattini, poi la lunghezza in metri.

```
lavorazione/foto_linee/
  despedida-165/
    IMG_1234.jpg
    IMG_1235.jpg
  rookie-60/
    IMG_1240.jpg
```

Gli id validi si stampano con:

```
python dati/linee.py --id
```

## Che cosa cambia nel manuale

Una linea con almeno una fotografia passa dallo stato `non documentata` a
**`fotografata`**: la sua scheda segnaposto mostra la miniatura e dichiara
«montata e fotografata, rigging non documentato». Non serve toccare il codice —
basta creare la cartella e metterci dentro i file.

Resta `non documentata` finché non arrivano riprese del montaggio con audio,
trascrizione e fotogrammi: **una fotografia della linea in opera non documenta
il rigging.** Mostra che la linea esiste ed è stata camminata, non come è stata
ancorata.

## Formato

JPEG o PNG, lato lungo max ~2000 px. Le fotografie a piena risoluzione dei
telefoni pesano diversi MB l'una e non servono: il manuale le stampa al massimo
a mezza pagina A4.
