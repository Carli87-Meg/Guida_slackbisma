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

## Le foto del file LineeBisma (27/10/2026)

Le cartelle `anfiteatro-46`, `-53`, `-97`, `-108`, `-113`, `despedida-60` e `-70`
contengono le fotografie del file del gruppo `LineeBisma.xlsx` (Drive, 20/10/2026),
una riga per linea e una colonna per lato. Ogni cartella ha un `ORIGINE.md` con
scheda, cella, colonna del file («vicino»/«lontano»: le sue colonne «Near Side» e
«Far Side», non tensione/statico), descrizione e se nella foto c'è qualcuno di
riconoscibile (senza descrivere le persone). I file si chiamano
`<linea>_<NN>_<lato>_<soggetto>.jpg`: NN è solo l'ordine (la 01 è la miniatura
stampata nella guida: non deve mostrare volti riconoscibili), il lato è la colonna del
file (`lato-nd` = fuori dalle colonne dei lati), il soggetto è ciò che si vede
nell'immagine, senza nomi di dispositivi, lati o tipi di ancoraggio che la foto non
dimostra. Nessuna ha EXIF (Excel li toglie): data e luogo vanno chiesti a chi ha
compilato il file.

**Rotazione.** Diciannove foto sono salvate nel file ruotate di 90°: Excel le mostra
dritte perché nel disegno hanno `rot="5400000"`. Le copie sono state ruotate di 90° in
senso orario, come le mostra Excel: nove al momento della copia, le altre dieci dopo la
verifica del 27/10/2026, rigenerandole dall'originale (tutte segnate «raddrizzata»
negli `ORIGINE.md`). Gli originali in `fonti/lineebisma/` restano come sono.

**Persone riconoscibili.** Le jpg di queste cartelle sono **fuori da git** (`.gitignore`)
finché l'utente non decide se e quali versionare. Prima di decidere, contano otto foto:

| Foto | Persona | Stato |
|---|---|---|
| `46_05`, `113_08` | volto riconoscibile | copiate in locale su decisione dell'utente; se versionarle: da decidere |
| `97_03` | volto riconoscibile | non dichiarata alla copia; da decidere |
| `108_02`, `108_04`, `113_03`, `113_06` | volto non visibile, ma riconoscibile da chi la conosce | da decidere |
| `113_02` | in parte coperta dal palo: riconoscibilità al limite | da decidere |

Nessuna di queste è una miniatura: la 97 è stata rinumerata apposta (vedi il suo
`ORIGINE.md`). Le altre 23 non mostrano persone riconoscibili, secondo gli `ORIGINE.md`.

**Senza le jpg il capitolo non esce.** Le jpg non sono in git: un build fatto senza di
esse stampa sulla console un AVVISO, e le linee tornano «non documentate».

Sono quasi tutte foto delle **soste**, non della linea in opera: qui mostrano
che la linea è stata montata; per usarle come documentazione degli ancoraggi
vanno spostate in `lavorazione/ancoraggi/<id>/` con il lato nel nome, e il lato
di tensione va dichiarato da chi c'era (vedi il LEGGIMI lì). **Attenzione:**
`lavorazione/ancoraggi/` è versionata, quindi una foto spostata lì finisce nel
repository pubblico al primo `git add`: si spostano solo foto senza persone
riconoscibili e con l'ok dell'utente.

### Le letture (27/10/2026)

Ogni cartella ha anche un **`LETTURA.md`**: che cosa ciascuna foto mostra in modo
inequivocabile (elementi dell'ancoraggio, materiale riconoscibile per marca o per
forma, stagione), il confronto con le parole del file, e l'elenco di ciò che resta
`[DA CONFERMARE]`. Nessuna misura è letta a occhio; il tipo di ancoraggio (alberi,
roccia, cavalletto) si scrive solo dove la foto lo mostra senza dubbi. Le letture sono
state rifatte il 27/10/2026 sulle copie dritte. Il riassunto che il build stampa sta
in `dati/foto_carlo.py`: la guida mostra le sei linee fotografate nella parte 3,
capitolo «Le linee fotografate» (una scheda per linea: che cosa dice il file e che
cosa si vede per ciascuna colonna, e ciò che resta `[DA CONFERMARE]`), e la scheda di
rilievo di ciascuna dice che le foto esistono. I dubbi che le foto aprono sono le voci
59-74 di `DUBBI.md`. Chi aggiunge foto nuove a una di queste cartelle aggiorna la
lettura e la riga in `dati/foto_carlo.py`.

## Formato

JPEG o PNG, lato lungo max ~2000 px. Le fotografie a piena risoluzione dei
telefoni pesano diversi MB l'una e non servono: il manuale le stampa al massimo
a mezza pagina A4.
