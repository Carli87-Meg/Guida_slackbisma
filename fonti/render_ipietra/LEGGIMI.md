# Render 3D del catalogo i-pietra

Viste del modello tridimensionale della Pietra con le linee di un settore
tracciate ed etichettate, esportate da i-pietra.

Un file per settore, chiamato con il nome del settore in minuscolo e gli spazi
sostituiti da trattini:

```
fonti/render_ipietra/
  rookie.jpg
  anfiteatro.jpg
  anfite-altro.jpg
  settore-giallo.jpg
  despedida.jpg
```

Ci sono tutti e cinque: il dubbio 53, che teneva aperta la copertura del Settore
Giallo, è chiuso dal render del 20/08/2026.

## La vista d'insieme

Oltre ai render per settore c'è una **panoramica** dell'intero massiccio:

```
  panoramica.jpg                    ← la base, senza etichette
  riferimento_settori_utente.jpg    ← non è un render: vedi sotto
```

`panoramica.jpg` apre il capitolo «Le linee della Pietra». Deve arrivare
**pulita, senza etichette impresse**: le pastiglie dei settori le disegna
`build/panoramica_settori.py` con i colori del manuale e il numero di linee
preso da `dati/linee.py`. Una panoramica già etichettata produce due giri di
scritte sovrapposte.

`riferimento_settori_utente.jpg` è lo screenshot su cui l'utente ha segnato a
mano dove cade ciascun settore, il 21/08/2026. Non entra nel manuale: è la
**fonte delle posizioni** in `POSIZIONI`, e si conserva perché quelle coordinate
non sono ricavabili dai render per settore. Il nome non contiene «panoramica»
apposta, così il build non lo scambia per la base.

Le posizioni valgono per l'inquadratura di `panoramica.jpg`. **Se la panoramica
viene riesportata da un altro punto di vista, vanno rifatte**: `--griglia`
sovrappone caselle nominate per farsele indicare senza stimare coordinate.

Estensioni accettate: `.jpg`, `.jpeg`, `.png`. **Preferire JPEG**: questi render
sono immagini fotografiche, e in PNG pesano dieci volte tanto senza guadagno
visibile. I cinque file di partenza erano PNG per 14,5 MB complessivi e hanno
portato il PDF a 32,9 MB, oltre il limite di 30 MB per la consegna; convertiti a
JPEG qualita' 90 occupano 1,6 MB e le etichette restano identiche a un
ingrandimento 200%.

Per convertirli:

    python -c "from PIL import Image; import glob; \
    [Image.open(f).convert('RGB').save(f[:-4]+'.jpg','JPEG',quality=90, \
    optimize=True,progressive=True) for f in glob.glob('*.png')]"

Il build li impagina da solo nel capitolo 7. Non serve toccare il codice: basta
mettere i file qui e rilanciare `python build/build_manuale.py`. I settori senza
render vengono semplicemente saltati, e il manuale lo dichiara.

## Che cosa sono e che cosa non sono

**Non sono una planimetria topografica.** Sono viste prospettiche di un modello
fotogrammetrico: mostrano dove corre ciascuna linea sulla parete e quanto è
lunga secondo il catalogo, non distanze misurate né quote.

Mostrano inoltre **le linee secondo i-pietra**, che non coincidono con quelle
della locandina: i-pietra accorpa Anfite-altro dentro Anfiteatro (dubbio 52) e
la sua copertura è cambiata nel tempo (dubbio 53). La didascalia nel manuale lo
dichiara.

## Formato

Esportare a piena risoluzione, **senza ritagliare le etichette**: sono i nomi e
le lunghezze delle linee a rendere il render una fonte e non una decorazione.
Lato lungo utile ~2000 px; oltre è spreco, il manuale li stampa a larghezza di
colonna su A4.

Il nome del file non deve essere esatto: basta che contenga il nome del settore.
`python build/schede_linee.py` stampa quale file viene assegnato a quale settore.
