# Catalogo del materiale — Bismaliners

Chi ha cosa, dove si trova, se è fuori. Nato dalle riunioni del 01/10 e dell'08/10/2026:
ognuno fa la cernita del suo materiale; il catalogo lo tengono Carlos e Matte Kode per il
materiale di Reggio e Carlo («tesoriere del materiale») per quello di Parma; poi i due
elenchi si uniscono. La prima lista è quella scritta da Matte Kode alla cernita di Reggio
del 09/10/2026.

**Questa cartella resta fuori da git** (il repository è pubblico, il catalogo ha nomi,
prezzi e foto). Su GitHub c'è solo questo file.

## Dove vive il catalogo

**La versione buona è il Foglio Google** «Catalogo materiale Bismaliners», nella cartella
Drive «Bismaliners» → «02 Materiale». Si modifica solo lì. Si consulta in tre modi:

| Dove | Chi lo usa | Cosa fa |
|---|---|---|
| **Foglio Google** | Tutti, dal telefono o dal computer | Si legge e si modifica. Le istruzioni sono nel suo primo foglio, «Leggimi» |
| **Sito** `inventario-bismaliners.vercel.app` | Chi vuole solo guardare | Schede con foto, filtri e ordinamento. **Sola lettura**, con parola d'ordine (si passa nel gruppo WhatsApp, non si scrive nei documenti). **Niente prezzi.** Legge il Foglio a ogni apertura, quindi è sempre aggiornato. Ogni scheda ha il collegamento «Modifica questa riga sul foglio» |
| **Pagina claude.ai** | Carlos | La prima versione interattiva, con un database suo. **Non è collegata al Foglio**: se il Foglio cambia, la pagina resta indietro |

Fogli del Foglio Google: **Leggimi** · **Catalogo** (una riga per oggetto, filtri, menu,
colori) · **Riepilogo** (conteggi per gruppo, categoria, proprietario, luogo, regime) ·
**Glossario** (il gergo della guida) · **Foto cernita** · **Liste** (voci dei menu).

## Regole

- Essenziali per ogni oggetto: **Cosa, Qtà, Proprietario, Dove si trova** (riunione 08/10).
- **Non si inventa niente.** Un dato che non conosciamo resta vuoto; la domanda va in
  «Da chiarire».
- **Brache: vale solo l'etichetta.** «Portata dichiarata» è quella scritta nella lista o
  nell'ordine; «Etichetta» dice se qualcuno l'ha letta davvero (dalla guida, «La portata
  delle brache»). Nel sito una braca con etichetta «Non controllata» porta la pastiglia
  «Etichetta da leggere».
- **Nomi** («Cosa»): tipo al singolare + marca o modello + lunghezza + diametro + portata +
  colore + dettagli, per esempio «Braca 2 m 1T viola». Quello che c'era scritto nella lista
  resta in «Nella lista».
- **Carico di rottura**: il valore del produttore, con la fonte, solo se il prodotto è
  riconosciuto dal nome. «da confermare (Spider simile: …)» vuol dire che il numero è di un
  prodotto Spider dello stesso tipo, **non** del nostro pezzo.
- **Larghezza** solo per le fettucce.
- **Foto**: le foto Spider («foto Spider · solo il tipo») mostrano il tipo di oggetto, non il
  pezzo preciso. Le foto delle etichette sono nostre.

## Il sito: come è fatto e come si aggiorna

Sta in `vercel/`, progetto Vercel `inventario-bismaliners` del team di Carlos.

| File | Che cos'è |
|---|---|
| `index.html` | La pagina. **Non si modifica a mano**: la genera `costruisci.py` |
| `costruisci.py` | Prende grafica e funzioni da `inventario.html` (la pagina claude.ai), la mette in sola lettura, aggiunge la parola d'ordine e la mappa oggetto → foto |
| `dati_pagina/` | Esportazione del database della pagina claude.ai, da cui `costruisci.py` prende le foto di ogni voce. Resta sul disco: non va su Vercel |
| `api/catalogo.js` | La funzione sul server: controlla la parola d'ordine, legge il Foglio come CSV, **toglie i prezzi** e risponde con le voci |
| `img/` | Le cinque foto delle etichette, ridotte. Le foto dei prodotti si caricano dai siti dei produttori |
| `.vercel/`, `.env.local` | Collegamento al progetto e token creati da `vercel link`: non si toccano e non si condividono |

**Cambiare i dati:** si cambia il Foglio, il sito lo legge da solo. Non serve ripubblicare.

**Cambiare la pagina** (dopo aver cambiato `inventario.html`), dentro `vercel/`:

```
python costruisci.py
npx vercel deploy --prod --scope carli87-projects
```

**Impostazioni sul server** (Vercel → progetto → Settings → Environment Variables):
`PAROLA` (la parola d'ordine), `SHEET_ID` e `SHEET_GID` (quale Foglio e quale scheda
leggere). Dopo averne cambiata una va ripubblicato. Per cambiare la parola d'ordine:

```
npx vercel env rm PAROLA production --scope carli87-projects
npx vercel env add PAROLA production --scope carli87-projects
npx vercel deploy --prod --scope carli87-projects
```

**Attenzione:** il sito legge il Foglio perché il Foglio è condiviso come «chiunque abbia
il link può visualizzare». Se si toglie quella condivisione il sito smette di funzionare;
finché c'è, chi ha il link del Foglio vede anche i prezzi. Il link del Foglio non va
quindi girato fuori dal gruppo.

## File in questa cartella

| File | Che cos'è |
|---|---|
| `inventario.html`, `img/` | La pagina claude.ai e le sue immagini (foto Spider `tipo-*`, prodotti, etichette). È anche la sorgente della grafica del sito |
| `vercel/` | Il sito, vedi sopra |
| `Catalogo_Bismaliners.xlsx` | Il file da cui è nato il Foglio Google il 10/10 (87 voci). Superato dal Foglio |
| `crea_catalogo.py` | Lo genera leggendo `Inventario_Bismaliners.xlsx` |
| `Inventario_Bismaliners.xlsx` | Inventario del 10/10: ordine Spider + lista della cernita (97 voci, 192 pezzi). Archivio e sorgente dello script |
| `foto_cernita/` | Le 8 foto della cernita arrivate il 10/10, già caricate su Drive in «Foto cernita» |
| `materiale.csv`, `build_inventario.py`, `export/` | Prima versione (08/10): Excel generato da CSV. Superati |
