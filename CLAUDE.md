# Guida alle highline della Pietra di Bismantova

Progetto: produrre in PDF una guida alle highline della Pietra di Bismantova
(Castelnovo ne' Monti, RE).

Il perimetro è cresciuto rispetto all'impostazione iniziale. Si partiva dal solo
montaggio della «50» — che il catalogo i-pietra registra come **Anfiteatro 53 m** e che
sul campo chiamano così — documentato da una cartella di video. La locandina «La Pietra»
e i render i-pietra hanno poi mostrato che le linee censite sono **ventiquattro su cinque
aree**, e la guida le copre tutte.

Di una sola esiste documentazione di rigging. Le altre ventitré hanno una **scheda di
rilievo**: campi vuoti da compilare sul posto e riportare in `dati/linee.py`. La guida è
anche lo strumento con cui si documenta ciò che manca.

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

- `build/design.py` — sistema grafico (ReportLab): font, palette, componenti
  `LineHeader`, `ChipRow`, `gear_block`, `callout`, `data_table`, `PhotoStrip`,
  `photo_row`, `Steps`, `Bars`, `ColorKey`, `two_cols`, `Checklist`, `livello_chip`. È partito da `design/design.py`
  (quello della Sillschlucht) ed è stato esteso per questa guida: **si modifica
  `build/design.py`**, `design/design.py` resta com'era come riferimento. Riusare i
  componenti, non riscriverli.
- `riferimento/build_guida_sillschlucht_it.py` — guida di 16 pagine costruita con quel
  sistema. È il modello di riferimento per struttura e tono; la scheda della 53 m segue il
  suo modello di scheda di linea.
- `riferimento/build_scheda_campo_it.py` — scheda da campo su una pagina A4.
- `tools/` — pipeline video e foto: inventario, trascrizione, ricerca nelle trascrizioni,
  fotogrammi, provini, annotazione, importazione delle foto con EXIF.

## Com'è fatta la guida

`build/build_manuale.py` assembla la guida (edizione 0.4, 27/10/2026):

0. **Come leggere questa guida** — i quattro livelli di documentazione (censita,
   fotografata, rilevata, documentata), i due marcatori, i codici delle linee,
   l'avvertenza, le edizioni. Poi l'indice.
1. **La Pietra** — lo spot; accesso e regole, presenti e dichiaratamente vuoti; i cinque
   settori sulla vista d'insieme (`panoramica_settori.py`).
2. **Le linee** — la tavola di stato delle 24 linee, poi una pagina per settore
   nell'ordine della cresta, seguita dalle schede complete delle sue linee che hanno un
   file di dati: oggi GAS-OH e le cinque fotografate dal gruppo (la 108 è censita dal 27/10: le foto del file erano della 113). Nessuna scheda per le
   censite (`schede_linee.py`, `scheda_linea.py`, `dati/linee.py`, `dati/schede/<id>.py`).
   Una scheda mostra solo le sezioni con dati: dove corre sul render i-pietra con i capi
   cerchiati, i due lati con il materiale che si vede (con i nomi del file, «vicino» e
   «lontano», finché nessuno dichiara quale sia quello di tensione), le fotografie, i
   capi secondo SlackMap, le parole del file del gruppo, che cosa manca. Le note comuni
   a tutte le schede dalle fotografie (che cosa valgono le coordinate SlackMap, che cos'è
   il file, come è riconosciuto il materiale) stanno una volta in «Come leggere».
3. **Come si monta: il metodo Bisma** — sei capitoli, validi per ogni linea
   (`metodo.py`). Niente regole generiche di highlining a colmare i vuoti: ciò che il
   gruppo non ha detto sta nel capitolo 6, come domanda.
4. **Apparato** — glossario e terminologia, protocollo di rilievo, fonti con le loro
   date, avvertenza, colophon.

**I dati stanno in un posto solo.** Il registro `dati/linee.py` ha settore, codice
(`AN-4`: sigla del settore e numero d'ordine sulla locandina), nome SlackMap, lunghezza
di catalogo; il **livello** di una linea non si dichiara, si calcola da ciò che esiste.
`dati/slackmap.py` è generato da `tools/06_slackmap.py` dall'API pubblica di SlackMap
(nome, lunghezza del segmento disegnato, coordinate dei due capi, per tutte e 24 le
linee): le coordinate **non sono misurate**, sulla 53 m scartano di 10-19 m dal GPS del
telefono, e la guida lo dichiara ogni volta che le stampa. Tutto ciò che è proprio di una linea (coordinate, ancoraggi,
materiale, A-frame, varianti, che cosa manca) sta in `dati/schede/<id>.py`, e
`build/scheda_linea.py` lo impagina mostrando solo le sezioni con dati: documentare una
linea nuova significa scrivere il suo file di dati, non toccare il build. Il file del
gruppo LineeBisma è trascritto in `dati/file_lineebisma.py`.

**Due marcatori**, spiegati in «Come leggere»: `[DA CONFERMARE]` in rosso per un dato
incerto o contraddetto da un'altra fonte; «da rilevare» in grigio, o la cella vuota in
tabella, per un dato che nessuno ha raccolto. Il rosso non si usa per i dati
semplicemente assenti.

Ogni informazione al suo posto: il **metodo** dice come si fa (funzioni, tipi di
materiale, principi; le foto di una linea solo come esempi dichiarati); la **scheda** dice
com'è fatta quella linea (quantità, colori, punti, coordinate, varianti, cosa manca).
Niente racconto del montaggio nel testo: minuti dei video e cronologia stanno nei commenti
del codice e nell'apparato. Le schede di rilievo delle linee non documentate, il foglio
dello spot e le parole del file del gruppo sulle linee fotografate escono in un fascicolo
a parte (`build_schede_rilievo.py`); i dubbi da chiedere sul campo in
`build_scheda_dubbi.py`.

L'impaginazione si rivede su Figma insieme all'utente; Figma è il tavolo di revisione, la
fonte resta il codice: le modifiche fatte là vanno rilette e riportate qui.

## Vincoli tecnici

- I video superano i 3 GB: **non caricarli mai nel contesto**. Si lavora solo su
  trascrizioni testuali e su fotogrammi estratti e ridimensionati (max ~1600 px lato lungo).
- Trascrizione in locale. La macchina è AMD senza CUDA: usare `faster-whisper` in modalità
  CPU int8, oppure `whisper.cpp`. Lingua italiana, timestamp a livello di parola.
- Output finale: PDF A4. Toolchain identica a quella del progetto Sillschlucht.

## Struttura di lavoro

```
video/  video_icloud/     # riprese del 16/05/2026: sola lettura, fuori da git
foto/                     # foto originali (16/05 e 22/08/2026), fuori da git
fonti/                    # locandina, render i-pietra: fonti esterne con i loro limiti
dati/linee.py             # registro delle 24 linee: codici, nomi, livelli, campi di rilievo
dati/schede/<id>.py       # i dati propri di una linea (oggi: la 53 m e le cinque fotografate)
dati/slackmap.py          # generato da tools/06_slackmap.py: nomi e capi di SlackMap
dati/file_lineebisma.py   # il file del gruppo, con le sue parole, «da controllare»
lavorazione/
  audio/                  # wav 16 kHz mono estratti
  trascrizioni/           # .json con timestamp + .md leggibili
  frame_grezzi/           # fotogrammi candidati
  frame_annotati/         # fotogrammi con frecce e etichette
  foto_dritte/            # foto raddrizzate e ridotte: quelle che usa il build
  ancoraggi/  foto_linee/ # foto nuove dal campo, una cartella per linea (vedi i LEGGIMI)
  metadati_foto.md        # data e GPS letti dagli originali, prima che si perdano
build/
  design.py               # sistema grafico
  build_manuale.py        # assemblaggio della guida
  scheda_linea.py         # la scheda di qualunque linea, dal suo file di dati
  metodo.py  schede_linee.py  build_schede_rilievo.py  build_scheda_dubbi.py
output/                   # i tre PDF, fuori da git
NOTE_RIGGING.md           # sintesi strutturata estratta dai video
DUBBI.md                  # elenco di tutto ciò che va confermato
riunioni/                 # riunioni del gruppo: fuori da git, solo il LEGGIMI
inventario/               # catalogo del materiale e sito: fuori da git, solo il LEGGIMI
```

**Il repository GitHub è pubblico.** Prima di versionare materiale del gruppo (nomi,
prezzi, soldi, trascrizioni delle riunioni, foto in cui si riconosce una persona) va
chiesto all'utente; per default resta fuori, come `riunioni/` e `inventario/`.

## Nomi delle persone

La trascrizione automatica storpia i nomi del gruppo. Nei documenti si usano: **Ermy**
(non Erman, Herman, Hermann), **Matte Kode** (non Code, Malte), **Lasa** (non Lars),
**Desi** (non Daisy), **Carlos** (l'utente, «Carlitos») che **non** è Carlo. In una
citazione si lascia il testo trascritto e si mette il nome giusto fuori dalle virgolette.

## Pipeline

Per la 53 m è stata percorsa tutta nell'agosto 2026; resta lo schema da seguire
per ogni linea nuova di cui arrivino riprese con audio.

1. **Inventario** — `tools/01_inventario.sh`: durata, risoluzione, fps di ogni video.
   Produrre una tabella e chiedere all'utente quale video copre quale fase.
2. **Trascrizione** — `tools/02_trascrivi.py`: audio → testo con timestamp. Salvare sia
   JSON che Markdown leggibile.
3. **Lettura e strutturazione** — leggere le trascrizioni e produrre `NOTE_RIGGING.md`:
   fasi del montaggio in ordine, materiale nominato, misure, avvertenze, punti in cui il
   parlato è confuso. Ogni voce con il timestamp `[video.mp4 @ 12:34]` da cui proviene.
   **Fermarsi qui e far validare le note all'utente prima di andare avanti.**
4. **Selezione fotogrammi** — `tools/03_estrai_frame.py`: estrarre i frame ai timestamp
   scelti. Guardarli davvero (tool Read sull'immagine), scartare i mossi e i fuori fuoco, tenere quelli
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
