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

## Le foto di Carlo (27/10/2026)

Le cartelle `anfiteatro-46`, `-53`, `-97`, `-108`, `-113`, `despedida-60` e `-70`
contengono le fotografie che Carlo ha messo nel suo `LineeBisma.xlsx` (Drive,
20/10/2026), una riga per linea e una colonna per lato. Ogni cartella ha un
`ORIGINE.md` con scheda, cella, lato dichiarato da Carlo («vicino»/«lontano»: i suoi,
non tensione/statico), descrizione e persone visibili. I file si chiamano
`<linea>_<NN>_<lato>_<soggetto>.jpg`: NN è solo l'ordine (la 01 è la miniatura), il
lato è la colonna di Carlo (`lato-nd` = fuori dalle colonne dei lati), il soggetto è
ciò che si vede nell'immagine. Nessuna ha EXIF (Excel li toglie): data
e luogo vanno chiesti a Carlo. Nove foto erano salvate ruotate di 90° nel file: sono state
raddrizzate il 27/10/2026 (segnate «raddrizzata» negli `ORIGINE.md`). Due foto (46 e 113, lato vicino) mostrano una persona
riconoscibile: Carlos ha deciso di tenerle qui, sapendo che il repository è pubblico.

Sono quasi tutte foto delle **soste**, non della linea in opera: qui mostrano
che la linea è stata montata; per usarle come documentazione degli ancoraggi
vanno spostate in `lavorazione/ancoraggi/<id>/` con il lato nel nome, e il lato
di tensione va dichiarato da chi c'era (vedi il LEGGIMI lì).

### Le letture (27/10/2026)

Ogni cartella ha anche un **`LETTURA.md`**: che cosa ciascuna foto mostra in modo
inequivocabile (tipo di ancoraggio, materiale riconoscibile per marca o per forma,
stagione), il confronto con le parole di Carlo nel Foglio «Linee», e l'elenco di ciò
che resta `[DA CONFERMARE]`. Nessuna misura è letta a occhio. Il riassunto che il
build stampa sta in `dati/foto_carlo.py`: la guida mostra le sei linee fotografate
nella parte 3, capitolo «Le linee fotografate» (una scheda per linea: lato vicino e
lontano di Carlo, che cosa si vede, che cosa manca), e la scheda di rilievo di
ciascuna dice che le foto esistono. I dubbi che le foto aprono sono le voci 59-69 di
`DUBBI.md`. Chi aggiunge foto nuove a una di queste cartelle aggiorna la lettura e
la riga in `dati/foto_carlo.py`.

## Formato

JPEG o PNG, lato lungo max ~2000 px. Le fotografie a piena risoluzione dei
telefoni pesano diversi MB l'una e non servono: il manuale le stampa al massimo
a mezza pagina A4.
