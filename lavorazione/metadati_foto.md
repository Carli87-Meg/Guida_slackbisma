# Metadati delle fotografie

Le immagini in `foto_dritte/` sono derivati: raddrizzarle e ridimensionarle
**azzera l'EXIF**, e con l'EXIF se ne va l'ora dello scatto e la posizione. Sono
dati di fonte quanto il parlato dei video, quindi si trascrivono qui alla prima
lettura dell'originale.

Letti con `python tools/importa_foto.py --in <file> --solo-dati`. Dove una riga
dice «non letto», l'originale non è passato dallo strumento e il dato non è perso:
è semplicemente ancora dentro il file sul telefono.

| File | Scatto | Dispositivo | GPS | Quota | Pixel originali |
|---|---|---|---|---|---|
| `IMG_1416` | 16/05/2026 17:14:38 | Apple iPhone 14 Pro | 44.419869, 10.412353 | 1025 m | 1980×3520 |

Le altre fotografie in `foto_dritte/` sono state importate prima che questo
registro esistesse e la loro copia in repo non porta più l'EXIF. Per recuperarlo
basta ripassare gli originali dal telefono attraverso `importa_foto.py`.

## Che valore ha la posizione

La coordinata è **dove stava il telefono**, con la precisione del GPS di un
telefono sotto una parete: buona per collocare l'ancoraggio su una mappa, non è
un rilievo topografico. Non va stampata come se fosse una misura strumentale, e
non sostituisce il sopralluogo che il dubbio 3 di `DUBBI.md` chiede.

Anche la quota viene dal telefono. Il valore di 1025 m è compatibile con un
punto poco sotto la cima della Pietra, data a 1047 m dalla locandina, ma resta
una lettura barometrica, non una quotatura.
