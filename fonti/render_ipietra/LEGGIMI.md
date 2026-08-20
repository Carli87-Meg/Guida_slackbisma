# Render 3D del catalogo i-pietra

Viste del modello tridimensionale della Pietra con le linee di un settore
tracciate ed etichettate, esportate da i-pietra.

Un file per settore, chiamato con il nome del settore in minuscolo e gli spazi
sostituiti da trattini:

```
fonti/render_ipietra/
  anfiteatro.jpg
  rookie.jpg
  despedida.jpg
  settore-giallo.jpg      ← manca: è il dubbio 53
```

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
