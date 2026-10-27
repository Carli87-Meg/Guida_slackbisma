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
| `costruisci.py` | Prende grafica e funzioni da `inventario.html` (la pagina claude.ai), la mette in sola lettura, aggiunge la parola d'ordine, la mappa oggetto → foto e monta il Rig planner (copia i moduli di `../rig/` in `rig/`) |
| `rig/` | I moduli del Rig planner, copiati da `../rig/` a ogni costruzione: **non si modificano qui** |
| `dati_pagina/` | Esportazione del database della pagina claude.ai, da cui `costruisci.py` prende le foto di ogni voce. Resta sul disco: non va su Vercel |
| `api/catalogo.js` | La funzione sul server: controlla la parola d'ordine, legge il Foglio come CSV, **toglie i prezzi** e risponde con le voci. Se è configurato il Foglio delle linee, risponde anche con `linee` e `schemi` |
| `api/_prova/` | `linee.csv` e `schemi.csv`: dati di prova per lo sviluppo in locale, con le stesse colonne del Foglio delle linee. **Non vanno su Vercel** (`.vercelignore`) e l'API li legge solo se manca `LINEE_ID` |
| `linee_ipietra.json` | Le 24 highline con nome, id, colore e coordinate 3D dal catalogo i-pietra (snapshot 21/10/2026). Lo genera `../selettore/esporta_linee_ipietra.py` |
| `3d/pietra.glb` | Il terreno della vista 3D: il collider di i-pietra convertito da `../selettore/converti_collider.py` (513 KB) |
| `img/render/` | I render i-pietra dei cinque settori, ridotti da `costruisci.py` a partire da `fonti/render_ipietra/` |
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
leggere). Per il Rig planner, facoltative: `LINEE_ID` (il Foglio «Linee della Pietra di
Bismantova»), `LINEE_GID_LINEE` e `LINEE_GID_SCHEMI` (le sue schede «Linee» e «Schemi»).
Dal 27/10/2026 sono impostate: il Foglio sta nel Drive del gruppo in «02 Materiale», con le
schede «Linee» (gid 0) e «Schemi» (gid 1) riempite dai CSV di `api/_prova/`; da lì in poi
si aggiorna il Foglio, non i CSV.
Senza, il planner elenca le linee ma dice che gli schemi non sono collegati. Dopo averne
cambiata una va ripubblicato.

**Provare in locale.** La via semplice è il server di anteprima, che non vuole la parola
vera (si entra con «prova») e legge linee e schemi di prova da `api/_prova/`; serve solo il
Foglio in `vercel/.env` (`SHEET_ID=…`, `SHEET_GID=…`, file che resta sul disco):

```
node inventario/selettore/anteprima.js 3100
```

Nell'app desktop di Claude è la configurazione `inventario-anteprima` di
`.claude/launch.json`. L'alternativa fedele a Vercel (parola vera in `.env`):

```
npx vercel@65.4.0 dev --cwd inventario/vercel --listen 3000 --scope carli87-projects
```

Per cambiare la parola d'ordine:

```
npx vercel env rm PAROLA production --scope carli87-projects
npx vercel env add PAROLA production --scope carli87-projects
npx vercel deploy --prod --scope carli87-projects
```

**Attenzione:** il sito legge il Foglio perché il Foglio è condiviso come «chiunque abbia
il link può visualizzare». Se si toglie quella condivisione il sito smette di funzionare;
finché c'è, chi ha il link del Foglio vede anche i prezzi. Il link del Foglio non va
quindi girato fuori dal gruppo.

## Il Rig planner («Costruisci una linea»)

Sta nel sito, sopra i filtri, ed è un'app a sé in `rig/` (dal 27/10/2026 sostituisce il
selettore a tre modalità). Nel sito parte **ripiegato**: una riga con «Apri il planner» (o
«Riprendi il piano»), così chi viene per il catalogo trova subito i filtri; un link `#rig=`
lo apre da solo. Porta dal catalogo alla parete in sei passi, con un riquadro a lato che
riassume il piano:

1. **Linea** — una delle 24 highline della Pietra (elenco per settore, mappa 3D cliccabile,
   render del settore, lati e note dal Foglio) oppure nome e campata a mano. Sul telefono
   e con poca rete la mappa 3D (circa 1 MB) parte solo premendo «Mostra la mappa 3D»; un
   dito scorre la pagina, due dita girano la Pietra.
2. **Ancoraggi** — lo schema di sosta di ogni lato, le sue righe e il disegno in sezione dei
   due ancoraggi (SVG, non in scala): spit, piastrine, delta, rami dello sliding x, omega,
   weblock, fettuccia, backup con BFK, cavalletto. Clic su un pezzo evidenzia la voce.
3. **Fettuccia e backup** — la **lista base del planner**, quello che serve per camminare
   oltre alle soste: fettuccia main e backup lunghe almeno campata + margine per lato (i
   margini li scrivi tu), weblock, softrelease, paranco, connettori, leash e imbrago per
   persona. Ogni riga dichiara di non venire dagli schemi del gruppo; le quantità che
   dipendono dal montaggio restano «da definire».
4. **Pezzi** — per ogni voce i candidati del catalogo e una **proposta automatica**: pezzi
   adatti, non in uso, dello stesso proprietario quando si può, mai più di quanti ne ha una
   riga anche contando le altre voci. Spunta, togli, cambia il numero: la voce resta tua
   finché non torni alla proposta. «↗» apre la scheda del pezzo. Un pezzo scelto a mano
   ma non adatto (più corto, in uso) resta segnato con ⚠ fino alla lista e al messaggio.
5. **Carichi** — facoltativo: la stima statica di prima, sui pezzi assegnati, con le
   ipotesi sempre scritte accanto ai numeri. Il fattore è verde solo con pezzi assegnati e
   tutti con un dato certo; giallo se è una stima sui candidati o manca un dato.
6. **Lista** — chi porta cosa (per proprietario e luogo), i pezzi che mancano, ciò che va
   portato ma non è in catalogo (i pali del cavalletto), ciò che è già sul posto (gli
   spit), le voci da definire, le domande aperte; «Copia per WhatsApp», link del piano,
   stampa, salvataggio.

Il piano vive nel browser (memoria locale, ultimo piano e piani salvati) e **nel link**
(`#rig=…`), che la barra degli indirizzi segue a ogni modifica: chi lo apre ritrova
tutto, anche su un altro telefono. Il link e il salvataggio **congelano la lista**: portano
anche i pezzi proposti, così chi apre vede la stessa lista del messaggio; se intanto un
pezzo è sparito dal catalogo o è stato segnato in uso, il planner lo dice fra le domande
aperte. Alla riapertura un avviso dice se si sta continuando un piano lasciato a metà o
uno ricevuto da un link (il piano precedente finisce nei piani salvati, «prima del link»).
Non scrive mai sui Fogli.

Regole, le stesse del catalogo:

- **Le linee** vengono da `linee_ipietra.json` (registro `dati/linee.py` + i-pietra) e, per
  i lati e le note di montaggio, dal Foglio «Linee della Pietra di Bismantova».
- **Gli schemi** (che cosa serve per una sosta) dalla scheda «Schemi» dello stesso Foglio,
  nata da «Sosta Bisma Standard» di `LineeBisma.xlsx` di Carlo. Una quantità che la fonte
  non scrive esce come **«da definire»**: il planner non la inventa; se una voce ha una
  parte nota («1 omega» più «omega, quanti?») propone la parte nota.
- **Brache**: la portata vale solo se «Etichetta» vale «Letta»; altrimenti «portata da
  leggere sull'etichetta».
- **In uso**: una riga con «In uso da» compilato non è disponibile (vale per tutti i pezzi
  della riga). Si può comunque scegliere a mano, con la pastiglia che lo dice.
- **Misure**: «10 mm» va cercato uguale nel pezzo; una lunghezza in metri accetta i pezzi
  lunghi almeno così, segna gli altri «più corta di …» e preferisce il più corto che basta.

**Lo studio dei carichi** è statico e dichiara le ipotesi: persona ferma a metà campata,
fettuccia senza peso, rami dello sliding x caricati in parti uguali. Si scrivono freccia,
massa, angolo di apertura (il campo della scheda di rilievo), rami che lavorano, tensione a
vuoto e un fattore dinamico (1 = statico). Da lì: tensione della fettuccia
T = √(H² + V²) con H = m·g·L/(4f) e V = m·g/2; forza su ogni ramo F = T / (n · cos(θ/2));
backup 0 in esercizio, T se cede la main; cavalletto e materiale personale non vedono la
tensione. Il confronto usa **solo resistenze di fonte certa**: il dato del produttore se il
prodotto è riconosciuto, l'etichetta letta per le brache (WLL, non rottura). I valori «da
confermare (Spider simile …)» non contano. Il fattore è resistenza / forza; sotto 5 è in
rosso. Caso di controllo: 53 m, freccia 3 m, 80 kg, 60° → T = 3,49 kN, ramo 1,34 kN.

**Com'è fatto** (`rig/`, moduli ES senza framework e senza build):

| File | Che cos'è |
|---|---|
| `modello.js` | Le funzioni pure: fabbisogno, assegnazione, carichi, confronto, lista, piano nel link. Niente DOM |
| `rig.js` | L'app: `monta(el, { spot, apri })` → `{ dati(d), carica(piano), piano }`. I sei passi, il riquadro, le azioni |
| `schema.js` | Il disegno SVG degli ancoraggi, con le frecce delle forze |
| `spot-bismantova.js` | Il pacchetto spot: le 24 linee, i render, la mappa 3D (three.js 0.160 da jsdelivr, caricato solo lì). Facoltativo |
| `rig.css` | Lo stile, con le variabili della pagina che lo ospita; tutte le classi iniziano con `rg-` |
| `index.html`, `tema.css`, `prova/` | La pagina autonoma con dati di prova (`prova/dati.json`, generato da `prova/genera.py`): `http://localhost:3100/rig/` con il server di anteprima; `?spot=no` toglie la Pietra, `?dati=URL` cambia i dati |
| `test/modello.test.mjs` | I test del modello: `node --test test/modello.test.mjs` dentro `rig/` |

**Per darlo a un altro gruppo**: si copia `rig/`, si monta `rig.js` in una pagina qualsiasi
e si passa a `dati()` un JSON con `materiale` (le voci del catalogo con gli stessi nomi di
campo), `schemi` (le righe degli schemi) e, se ci sono, `linee`; senza pacchetto spot
l'elenco delle linee viene dal Foglio e non c'è mappa. La lista base del planner e il
calcolo dei carichi valgono per qualunque highline.

## File in questa cartella

| File | Che cos'è |
|---|---|
| `inventario.html`, `img/` | La pagina claude.ai e le sue immagini (foto Spider `tipo-*`, prodotti, etichette). È anche la sorgente della grafica del sito |
| `rig/` | Il Rig planner: sorgente, pagina autonoma, dati di prova, test (vedi sopra) |
| `selettore/` | Gli script che preparano modello 3D e linee (`converti_collider.py`, `esporta_linee_ipietra.py`), il server di anteprima locale (`anteprima.js`) e il vecchio selettore `selettore_v1.html`, superato dal Rig planner |
| `vercel/` | Il sito, vedi sopra |
| `Catalogo_Bismaliners.xlsx` | Il file da cui è nato il Foglio Google il 10/10 (87 voci). Superato dal Foglio |
| `crea_catalogo.py` | Lo genera leggendo `Inventario_Bismaliners.xlsx` |
| `Inventario_Bismaliners.xlsx` | Inventario del 10/10: ordine Spider + lista della cernita (97 voci, 192 pezzi). Archivio e sorgente dello script |
| `foto_cernita/` | Le 8 foto della cernita arrivate il 10/10, già caricate su Drive in «Foto cernita» |
| `materiale.csv`, `build_inventario.py`, `export/` | Prima versione (08/10): Excel generato da CSV. Superati |
