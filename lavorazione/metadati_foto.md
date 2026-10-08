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
| `IMG_1360` | 16/05/2026 13:07:45 | Apple iPhone 14 Pro | 44.419839, 10.412339 | 1024 m | 1980×3520 |
| `IMG_3311` | 22/08/2026 14:10:53 | Apple iPhone 14 Pro | 44.422817, 10.415500 | 1013 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3323` | 22/08/2026 15:55:53 | Apple iPhone 14 Pro | 44.419453, 10.412072 | 1026 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3324` | 22/08/2026 15:55:57 | Apple iPhone 14 Pro | 44.419456, 10.412078 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3325` | 22/08/2026 15:55:59 | Apple iPhone 14 Pro | 44.419456, 10.412075 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3327` | 22/08/2026 15:56:05 | Apple iPhone 14 Pro | 44.419453, 10.412064 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3328` | 22/08/2026 15:56:10 | Apple iPhone 14 Pro | 44.419461, 10.412064 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3329` | 22/08/2026 15:56:18 | Apple iPhone 14 Pro | 44.419461, 10.412064 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3330` | 22/08/2026 15:56:25 | Apple iPhone 14 Pro | 44.419453, 10.412072 | 1025 m | 4032×3024 |
| `ancoraggi/anfiteatro-53/IMG_3332` | 22/08/2026 15:56:41 | Apple iPhone 14 Pro | 44.419453, 10.412086 | 1025 m | 4032×3024 |

Le altre fotografie in `foto_dritte/` sono state importate prima che questo
registro esistesse e la loro copia in repo non porta più l'EXIF. Per recuperarlo
basta ripassare gli originali dal telefono attraverso `importa_foto.py`.

## Due letture a quattro ore di distanza

`IMG_1360` (13:07) e `IMG_1416` (17:14) sono state scattate entrambe all'ancoraggio
main, a quattro ore l'una dall'altra, e le due posizioni distano **una manciata di
metri**. Non e' una misura ripetuta — sono due letture dello stesso telefono nello
stesso posto — ma concordano, e questo e' quanto di piu' vicino a una verifica il
progetto abbia oggi su quella coordinata.

## Che valore ha la posizione

La coordinata è **dove stava il telefono**, con la precisione del GPS di un
telefono sotto una parete: buona per collocare l'ancoraggio su una mappa, non è
un rilievo topografico. Non va stampata come se fosse una misura strumentale, e
non sostituisce il sopralluogo che il dubbio 3 di `DUBBI.md` chiede.

Anche la quota viene dal telefono. Il valore di 1025 m è compatibile con un
punto poco sotto la cima della Pietra, data a 1047 m dalla locandina, ma resta
una lettura barometrica, non una quotatura.

## 22 agosto 2026: l'altro capo della 53 m

Fornite dall'utente l'8 ottobre 2026, dalla cartella `foto/Foto di iCloud/` (25 scatti,
IMG_3308-3332). Due gruppi:

- **IMG_3323-3332, 15:55-15:56** — una sosta montata su placchette, con slinghe
  viola, corda verde annodata fra i punti e la linea che esce nella guaina dei
  bungee. Secondo l'utente è **la 53 m dell'Anfiteatro, montata con i bungee**.
  Il GPS lo conferma per un'altra strada: le dieci letture stanno entro 3 m
  l'una dall'altra e a **51,5 m** dalla posizione dell'ancoraggio main
  (`IMG_1416`). Una linea di 53 m ha i due capi a quella distanza: queste foto
  sono state scattate all'**altro capo**. Il lato non è nel nome dei file perché
  nessuno l'ha dichiarato (vedi `ancoraggi/LEGGIMI.md`): per il modello della
  guida è il lato statico, dubbio 56.
  Il montaggio con i bungee è una variante: slinghe, corda verde, fettucce rosse
  e bungee sono quelli di quel giorno, non il materiale del 16 maggio.
  Nessuna inquadratura mostra tutti i punti insieme: il dubbio 28 resta aperto.
- **IMG_3308-3322, 14:10-14:14** — a circa 400 m a nord-est, sulla cresta,
  durante un sopralluogo alle linee della Despedida. Secondo l'utente alcune sono
  del Settore Giallo, e la roccia sullo sfondo di `IMG_3311` «dovrebbe essere» la
  linea della Despedida da 165 m: dubbio 57. `IMG_3316` ha un GPS fuori di 3 km e
  senza quota, errore del telefono.

Restano solo sul disco locale, e non entrano nella guida, gli scatti in cui si
riconosce una persona (IMG_3313, 3316-3321, 3331): il repository è pubblico.
