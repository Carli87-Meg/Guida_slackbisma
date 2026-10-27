# Guida alle highline della Pietra di Bismantova

Guida in PDF alle ventiquattro highline della Pietra di Bismantova (Castelnovo ne' Monti,
RE), fatta per i Bismaliners. Una sola linea, l'**Anfiteatro 53 m** (sul campo «la 50»), ha
il rigging documentato da riprese e fotografie; le altre ventitré hanno una scheda di
rilievo da compilare in parete.

Le regole del progetto stanno in [`CLAUDE.md`](CLAUDE.md), che Claude Code legge a ogni
sessione. La più importante: **non si inventa niente**. Quello che non si sente nei video,
non si vede nelle foto e non dice chi ha montato entra nella guida come `[DA CONFERMARE]` e
finisce in [`DUBBI.md`](DUBBI.md).

## Cosa esce

| File in `output/` | Che cos'è | Come si rifà |
|---|---|---|
| `Pietra_Bismantova_Highline.pdf` | La guida | `python build/build_manuale.py` |
| `Pietra_Bismantova_Schede_Rilievo.pdf` | Le schede di rilievo delle 23 linee non documentate, da stampare | esce insieme alla guida, oppure `python build/build_schede_rilievo.py` |
| `Bismantova_Dubbi_Scheda_Campo.pdf` | I dubbi aperti di `DUBBI.md`, da compilare con chi ha montato | `python build/build_scheda_dubbi.py` |

Requisiti: `pip install -r requirements.txt`, e `ffmpeg` nel PATH solo per lavorare sui
video. I font (Poppins, Lora) li trova o li scarica `build/font.py`.

## Com'è fatta la guida

| Parte | Contenuto | Dove sta nel codice |
|---|---|---|
| 1 · La Pietra | Lo spot, la panoramica dei cinque settori, il catalogo delle 24 linee | `build/build_manuale.py`, `build/schede_linee.py`, `build/panoramica_settori.py`, `dati/linee.py` |
| 2 · Come si monta una linea | Il metodo, valido per ogni linea | `build/metodo.py` |
| 3 · Le linee | La scheda della 53 m, modello per le altre | `build/scheda_53.py` |
| 4 · Apparato | Glossario, fonti con le loro date, avvertenza finale | `build/build_manuale.py` |

Il **metodo** dice come si fa; la **scheda** dice com'è fatta quella linea (quantità,
colori, punti, coordinate, cosa manca). Un dato che vale per una linea sola va nella sua
scheda, non nel metodo.

Il sistema grafico è `build/design.py`: è partito da `design/design.py` (quello della guida
della Sillschlucht, in `riferimento/`) ed è stato esteso per questa guida. **Si modifica
`build/design.py`**; `design/design.py` resta com'era, come riferimento.

L'impaginazione si rivede su Figma (vedi `CLAUDE.md`): Figma è il tavolo di revisione, il
PDF lo genera sempre il codice.

## Cartelle

| Cartella | Contenuto | In git |
|---|---|---|
| `build/` | Gli script che generano i PDF | sì |
| `dati/linee.py` | Registro delle 24 linee: area, lunghezza, stato, campi del rilievo | sì |
| `tools/` | Pipeline video e foto (vedi sotto) | sì |
| `fonti/` | Locandina, render i-pietra: fonti esterne con i loro limiti | sì, tranne i PNG originali |
| `foto/` | Fotografie originali del 16/05 e del 22/08/2026 | no: in git vanno le copie raddrizzate di `lavorazione/foto_dritte/` |
| `lavorazione/` | Trascrizioni, fotogrammi, foto raddrizzate e annotate, metadati | in parte: audio, frame grezzi e provini no |
| `output/` | I PDF | no: si rigenerano |
| `video/`, `video_icloud/` | Le riprese del montaggio del 16/05/2026: sola lettura | no |
| `riunioni/` | Trascrizioni delle riunioni del gruppo | **no**: solo il LEGGIMI |
| `inventario/` | Catalogo del materiale e sito online | **no**: solo il LEGGIMI |
| `riferimento/` | La guida della Sillschlucht e la sua scheda da campo, come modello | sì |

**Il repository è pubblico.** Nomi, soldi, prezzi e questioni interne del gruppo restano
sul disco locale: per questo `riunioni/` e `inventario/` sono esclusi in `.gitignore`.

## Strumenti

| Script | A cosa serve |
|---|---|
| `tools/01_inventario.sh` · `01_inventario.py` | Durata, risoluzione, fps e data dei video (la versione Python non chiede ffprobe) |
| `tools/02_trascrivi.py` | Audio → trascrizione italiana con timestamp (faster-whisper, CPU int8) |
| `tools/cerca.py` | Cerca parole nelle trascrizioni e risponde con `[file @ mm:ss]` |
| `tools/03_estrai_frame.py` | Fotogrammi a timestamp precisi, con stima di nitidezza |
| `tools/rotazione.py` | Legge la rotazione dei video MOV/MP4 degli iPhone, senza la quale i fotogrammi escono coricati |
| `tools/provini.py` | Provini a contatto dei fotogrammi di un video |
| `tools/annota.py` | Frecce, cerchi, riquadri, numeri e didascalie sui fotogrammi |
| `tools/importa_foto.py` | Raddrizza e riduce una foto e ne stampa data e GPS dall'EXIF |
| `tools/provini_pdf.py` | Tutte le pagine del PDF su pochi fogli, per rivedere l'impaginazione |
| `build/annotazioni.py` | Le annotazioni dei fotogrammi usati nella guida |

Le coordinate di `annota.py` sono relative (0–1) e valgono a qualsiasi risoluzione:

```python
from tools.annota import Annotatore
a = Annotatore('frame.jpg')
a.freccia((0.15, 0.85), (0.45, 0.58), '1', 'rosso')
a.cerchio((0.48, 0.52), 0.09, 'grillo di collegamento', 'rosso')
a.didascalia('Collegamento al masterpoint')
a.salva('out.jpg')
```

## Documenti di lavoro

| File | Che cos'è |
|---|---|
| `DUBBI.md` | Tutto ciò che è da confermare, con la fonte del dubbio e lo stato |
| `NOTE_RIGGING.md` | Cosa dicono le trascrizioni dei 28 video (Fase 3, 19/08/2026) |
| `SELEZIONE_FRAME.md` | La scelta dei fotogrammi (Fase 4) |
| `lavorazione/metadati_foto.md` | Data e GPS delle fotografie, letti dagli originali |
| `PROMPT_INIZIALE.md`, `*_TEMPLATE.md` | Il kit con cui il progetto è partito: storici |

I `LEGGIMI.md` dentro le cartelle spiegano come ci si mettono i file nuovi (render, foto
delle linee, foto degli ancoraggi) senza toccare il codice.
