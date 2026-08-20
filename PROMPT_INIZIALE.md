# Prompt da incollare nel primo messaggio di Claude Code

Copia tutto quello che sta sotto la riga.

---

Ciao. Dobbiamo produrre un manuale di rigging in PDF per la highline da 50 m alla Pietra di
Bismantova (Castelnovo ne' Monti, Reggio Emilia), partendo da una cartella di video del
montaggio che trovi in `./video/`.

Prima di qualsiasi cosa: leggi `CLAUDE.md` in questa cartella. Contiene le regole del
progetto, la pipeline e le convenzioni grafiche. Leggi anche
`riferimento/build_guida_sillschlucht_it.py` e `design/design.py`: è il sistema con cui è
stata fatta una guida analoga per la Sillschlucht di Innsbruck, e va riusato così com'è.

La regola più importante: **non inventare dati tecnici**. Misure, lunghezze, quantità e
sequenze devono venire dalle trascrizioni audio o da ciò che si vede chiaramente nei
fotogrammi. Tutto il resto va marcato `[DA CONFERMARE]` e raccolto in `DUBBI.md`.

I video superano i 3 GB complessivi: non caricarli mai nel contesto, lavora solo su
trascrizioni e su fotogrammi estratti e ridimensionati.

Procedi per fasi, fermandoti alla fine di ognuna per farmi validare:

**Fase 1 — Inventario.** Esegui `tools/01_inventario.sh`, mostrami la tabella dei video
(nome, durata, risoluzione, fps) e chiedimi quale copre quale parte del montaggio.

**Fase 2 — Trascrizione.** Estrai l'audio e trascrivi con `tools/02_trascrivi.py`
(faster-whisper, italiano, CPU int8 — la macchina è AMD, niente CUDA). Salva JSON con
timestamp e Markdown leggibile in `lavorazione/trascrizioni/`.

**Fase 3 — Note strutturate.** Leggi le trascrizioni e produci `NOTE_RIGGING.md`: le fasi
del montaggio in ordine, il materiale nominato, le misure, le avvertenze, e i punti in cui
il parlato è confuso o inudibile. Ogni voce con il riferimento `[nomevideo.mp4 @ mm:ss]`.
Poi fermati: le rileggo io prima di andare avanti.

**Fase 4 — Fotogrammi.** Per ogni passo, estrai i frame candidati ai timestamp giusti con
`tools/03_estrai_frame.py`, guardali davvero con il tool `view`, scarta i mossi e i fuori
fuoco, e proponimi la selezione.

**Fase 5 — Annotazione.** Annota i frame scelti con `tools/annota.py`: frecce, cerchi ed
etichette numerate, usando la palette di `design.py`.

**Fase 6 — Impaginazione.** Assembla il PDF adattando lo script di riferimento.

Parti dalla Fase 1.
