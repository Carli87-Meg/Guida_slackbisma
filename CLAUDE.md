# Manuale di rigging — Highline 50 m, Pietra di Bismantova

Progetto: produrre un manuale PDF del rigging della highline da 50 m alla Pietra di
Bismantova (Castelnovo ne' Monti, RE), partendo da una cartella di video del montaggio.

## Regola numero uno

**Non inventare nulla.** Questo documento verrà usato da persone che montano una linea
sospesa nel vuoto. Ogni misura, ogni lunghezza di fettuccia, ogni numero di grilli, ogni
coppia di serraggio deve provenire da:

1. la trascrizione audio dei video, oppure
2. ciò che si vede in modo inequivocabile nei fotogrammi, oppure
3. una risposta esplicita dell'utente.

Se un dato manca o è ambiguo, va marcato come **`[DA CONFERMARE]`** nel testo e raccolto
in `DUBBI.md`. Un campo vuoto dichiarato è sempre meglio di un dato dedotto: un numero
plausibile ma sbagliato in un manuale di rigging è un rischio reale.

Non colmare i buchi con conoscenza generica di highlining. Se la trascrizione dice
"metti due fettucce" senza specificare la lunghezza, il manuale scrive "2 fettucce
`[DA CONFERMARE: lunghezza]`", non "2 fettucce da 2 m".

## Cosa esiste già

- `design/design.py` — sistema grafico completo e funzionante (ReportLab). Font, palette,
  componenti: `LineHeader`, `ChipRow`, `gear_block`, `callout`, `data_table`, `PhotoStrip`,
  `photo_row`, `Steps`, `Bars`, `ColorKey`, `two_cols`. **Riusalo, non riscriverlo.**
- `riferimento/build_guida_sillschlucht_it.py` — guida di 16 pagine costruita con quel
  sistema. È il modello di riferimento per struttura e tono.
- `riferimento/build_scheda_campo_it.py` — scheda da campo su una pagina A4.
- `tools/` — script di partenza per la pipeline video (vedi sotto).

## Vincoli tecnici

- I video superano i 3 GB: **non caricarli mai nel contesto**. Si lavora solo su
  trascrizioni testuali e su fotogrammi estratti e ridimensionati (max ~1600 px lato lungo).
- Trascrizione in locale. La macchina è AMD senza CUDA: usare `faster-whisper` in modalità
  CPU int8, oppure `whisper.cpp`. Lingua italiana, timestamp a livello di parola.
- Output finale: PDF A4. Toolchain identica a quella del progetto Sillschlucht.

## Struttura di lavoro

```
video/                    # input, non toccare, sola lettura
lavorazione/
  audio/                  # wav 16 kHz mono estratti
  trascrizioni/           # .json con timestamp + .md leggibili
  frame_grezzi/           # fotogrammi candidati
  frame_annotati/         # fotogrammi con frecce e etichette
build/
  design.py               # copiato da design/
  build_manuale.py        # script di assemblaggio PDF
output/
  Bismantova_Rigging_50m.pdf
NOTE_RIGGING.md           # sintesi strutturata estratta dai video
DUBBI.md                  # elenco di tutto ciò che va confermato
```

## Pipeline

1. **Inventario** — `tools/01_inventario.sh`: durata, risoluzione, fps di ogni video.
   Produrre una tabella e chiedere all'utente quale video copre quale fase.
2. **Trascrizione** — `tools/02_trascrivi.py`: audio → testo con timestamp. Salvare sia
   JSON che Markdown leggibile.
3. **Lettura e strutturazione** — leggere le trascrizioni e produrre `NOTE_RIGGING.md`:
   fasi del montaggio in ordine, materiale nominato, misure, avvertenze, punti in cui il
   parlato è confuso. Ogni voce con il timestamp `[video.mp4 @ 12:34]` da cui proviene.
   **Fermarsi qui e far validare le note all'utente prima di andare avanti.**
4. **Selezione fotogrammi** — `tools/03_estrai_frame.py`: estrarre i frame ai timestamp
   scelti. Guardarli davvero (tool `view`), scartare i mossi e i fuori fuoco, tenere quelli
   in cui la manovra è leggibile.
5. **Annotazione** — `tools/annota.py`: frecce, cerchi, etichette numerate sui frame.
6. **Impaginazione** — adattare lo script di riferimento e produrre il PDF.

## Convenzioni del manuale

Ereditate dal progetto Sillschlucht, da mantenere:

- **Codice colore**: un colore per ogni fase o per ogni ancoraggio, coerente in tutto il
  documento (testata, blocchi materiale, annotazioni sui frame, filetto a piè di pagina).
- **Struttura di ogni scheda**: testata → paragrafo introduttivo → riga di pastiglie dati
  → materiale in due colonne (lato tension / lato statico) → fotografie con didascalia.
- **Doppia colonna materiale**: `gear_block()` con coordinate cliccabili nell'intestazione
  quando disponibili.
- **Dati mancanti dichiarati**: dove il video non mostra o non dice, il manuale lo scrive.
- **Nomi commerciali invariati**: Weblock, Softrelease, Microtrax, Tibloc, Grigri, Treepro,
  Petzl, ecc.
- **Terminologia italiana** già fissata nel progetto precedente:
  - `Schlinge` → fettuccia · `Rundschlinge` → braca ad anello
  - `Schäkel` → grillo · `Softschäkel` → softshackle · `Quicklink` → maglia rapida
  - `Baumschutz` → protezione per l'albero
  - Tension-Anker / Statik-Anker → ancoraggio di tensione / ancoraggio statico
  - Restano in gergo: highline, tagline, fishingline, weblock, softrelease, A-frame,
    offlevel, permarig, backup, masterpoint, leash
- **Sezioni di apparato** da includere: introduzione allo spot, planimetria/schema, tabella
  materiale completo, glossario, checklist pre-uscita, sequenza di montaggio, note finali
  con disclaimer.

## Differenza rispetto a Sillschlucht

Bismantova è **roccia**, non alberi. Gli ancoraggi saranno spit, fix, clessidre o sosta su
più punti: la terminologia va adattata di conseguenza (placchette, fittoni, cordini di
collegamento, equalizzazione, angolo di apertura). Verificare sempre nel video invece di
trasporre meccanicamente il vocabolario da Sillschlucht.

Va anche verificato con l'utente il quadro di accesso: la Pietra di Bismantova è area
protetta e sede di falesia storica, quindi eventuali autorizzazioni, divieti stagionali per
nidificazione o accordi con il gestore vanno indicati se rilevanti — ma solo se l'utente li
fornisce, non dedotti.

## Disclaimer obbligatorio

Ultima pagina, sempre presente:

> Highlining e slacklining comportano rischi. Questo manuale documenta un montaggio già
> realizzato da persone esperte: non sostituisce formazione, esperienza diretta e verifica
> autonoma di ogni ancoraggio prima di ogni utilizzo.
