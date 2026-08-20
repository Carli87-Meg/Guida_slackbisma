# Kit di partenza — Manuale rigging Pietra di Bismantova

Cartella da aprire con Claude Code, con i video del montaggio in `./video/`.

## Avvio

1. Copia questa cartella dove stanno i video (o sposta i video qui dentro, in `video/`).
2. `pip install -r requirements.txt` e assicurati di avere `ffmpeg` nel PATH.
3. Apri Claude Code nella cartella.
4. Incolla come primo messaggio il contenuto di `PROMPT_INIZIALE.md`.

`CLAUDE.md` viene letto automaticamente da Claude Code a ogni sessione: contiene le regole
del progetto, la pipeline e le convenzioni grafiche.

## Cosa c'è dentro

| File | A cosa serve |
|---|---|
| `CLAUDE.md` | Istruzioni permanenti di progetto |
| `PROMPT_INIZIALE.md` | Il messaggio da incollare per iniziare |
| `design/design.py` | Sistema grafico: font, palette, componenti di impaginazione |
| `riferimento/build_guida_sillschlucht_it.py` | Guida di 16 pagine già fatta, da usare come modello |
| `riferimento/build_scheda_campo_it.py` | Scheda da campo su una pagina |
| `tools/01_inventario.sh` | Durata, risoluzione e peso dei video |
| `tools/02_trascrivi.py` | Audio → trascrizione italiana con timestamp |
| `tools/03_estrai_frame.py` | Fotogrammi a timestamp precisi, con stima di nitidezza |
| `tools/annota.py` | Frecce, cerchi, riquadri, numeri e didascalie sui frame |
| `NOTE_RIGGING_TEMPLATE.md` | Struttura delle note intermedie |
| `DUBBI_TEMPLATE.md` | Registro dei dati da confermare |

## Prova rapida di `annota.py`

```python
from tools.annota import Annotatore
a = Annotatore('frame.jpg')
a.freccia((0.15, 0.85), (0.45, 0.58), '1', 'rosso')
a.cerchio((0.48, 0.52), 0.09, 'grillo di collegamento', 'rosso')
a.riquadro([0.62, 0.30, 0.92, 0.66], 'backup', 'verde')
a.didascalia('Fase 3 — collegamento al masterpoint')
a.salva('out.jpg')
```

Coordinate sempre relative (0–1): valgono a qualsiasi risoluzione.
Colori disponibili: rosso, arancio, ambra, oliva, verde, acqua, azzurro, blu.

## Il punto che conta

I video sono la sola fonte di verità. Quello che non si sente e non si vede non entra nel
manuale come dato: entra come `[DA CONFERMARE]`. Su un documento di rigging, un numero
inventato è peggio di un campo vuoto.
