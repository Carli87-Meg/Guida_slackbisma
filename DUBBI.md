# Dubbi da chiarire prima della pubblicazione

Elenco di tutto ciò che nel manuale sarebbe marcato `[DA CONFERMARE]`.
Nessuna di queste voci va risolta per deduzione: servono risposte da chi ha montato la linea.

Stato: Fasi 1-4 concluse. Bloccanti risolti il 19/08/2026.

**La copertura di i-pietra è un dato con una data, non un fatto fisso.**
- Al **5 agosto 2026** — data dello snapshot `tool/catalog-admin/.cache/catalog-snapshot.json`,
  l'unica fonte disponibile il 19/08 — il catalogo conteneva 551 rotte e 37 settori, e
  i settori `despedida` e `settore-giallo` **non esistevano affatto**. Da lì il conteggio
  di 12 linee su 24 in `NOTE_RIGGING.md`: era corretto per quello snapshot.
- Al **20 agosto 2026** i render 3D forniti dall'utente mostrano censite anche Despedida
  (6 linee) e Settore Giallo (4). Copertura: **22 su 24**, mancano solo la 20 m e la 108 m
  dell'Anfiteatro.

Nell'intervallo il catalogo è stato ampliato, oppure i render leggono i dati vivi invece
della cache. In ogni caso **vale il dato del 20/08**, ed è quello che il manuale stampa —
ma datato. Dubbio 53, chiuso. Dal confronto fra le due fonti nasce il dubbio 52.

Fonti aggiuntive acquisite: catalogo **i-pietra** (sola lettura), che ha chiuso nome, lunghezza
e tipo di roccia.

## Bloccanti — ✅ chiusi

| # | Fase | Cosa mancava | Risposta dell'utente (19/08/2026) | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| B1 | tutto | I video sono della highline da 50 m? L'audio nomina 50, 90 e 55 come linee distinte | **Sì, tutti e 28.** 90 e 55 sono altre linee, non questo montaggio | `[IMG_1350 @ 0:48]`, `[IMG_1395 @ 2:29]` | ✅ chiuso |
| B2 | tutto | La località è la Pietra di Bismantova? Mai nominata in 22 min di audio | **Sì, Pietra di Bismantova** (Castelnovo ne' Monti, RE) | `[IMG_1373 @ 0:24]` | ✅ chiuso |
| B3 | D | Ancoraggi su roccia, su albero, o misti? Si parla di un ramo che si taglia | **Solo roccia.** Terminologia: placchette, fittoni, clessidre, cordini di collegamento, equalizzazione, angolo di apertura | `[IMG_1375 @ 0:00]` | ✅ chiuso |

> ⚠ Da tenere d'occhio: la frase «se si taglia un ramo si sfila tutta» `[IMG_1375 @ 0:00]`
> resta in contrasto apparente con «solo roccia». Va guardata a immagine — può essere un
> modo di dire, una trascrizione imprecisa, o un ramo non portante. **Non implica un
> ancoraggio su albero**, ma finché non è chiarita non entra nel manuale.

## Quadro generale della linea

| # | Fase | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 1 | intro | Lunghezza effettiva della campata | Dato di testata | mai pronunciata | **riaperto** — i-pietra e locandina danno 53 m, ma l'utente rimisurerà sui punti. Nome di lavoro: «la 50» |
| 2 | intro | Dislivello / offlevel fra i due lati | Dato di testata, influenza il tensionamento | mai pronunciato | aperto |
| 3 | intro | Coordinate dei due ancoraggi | Intestazione dei blocchi materiale (cliccabili) | mai pronunciate | aperto — **i-pietra non aiuta**: i suoi `linePoints` sono coordinate della scena 3D, non GPS |
| 4 | intro | Accesso e avvicinamento | Sezione di apparato prevista | mai descritto | aperto |
| 5 | intro | Autorizzazioni, divieti stagionali, accordi con il gestore | Richiesto da CLAUDE.md se rilevante | mai nominati | aperto |
| 6 | intro | Tempo reale di montaggio | I video coprono 2 h 38 min ma non dicono inizio e fine | metadati dei file | aperto |
| 7 | intro | Quante persone erano necessarie (non quante c'erano) | Checklist pre-uscita | `[IMG_1373 @ 0:24]` cita «quattro» ma in un'altra frase | aperto |

## Materiale

| # | Fase | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 8 | A | Lunghezza e tipo delle fettucce **viola** della sosta main | Tabella materiale | `[IMG_1349 @ 0:00]` | aperto |
| 9 | A | Diametro, tipo e lunghezza delle corde **rosa** del backup | Tabella materiale | `[IMG_1349 @ 0:00]` | aperto |
| 10 | A | Modello del **BFK** sulla corda rosa | Tabella materiale | `[IMG_1350 @ 0:00]` | aperto |
| 11 | A | Diametro e lunghezza della corda **azzurra** (tagline, poi linea vita) | Tabella materiale | `[IMG_1350 @ 0:37]` | aperto |
| 12 | A | Misura e materiale delle **4 maglie delta** | Unica quantità certa del corpus, manca la misura | `[IMG_1350 @ 0:53]` | aperto |
| 13 | A | Cos'è il «**Mighty Lock**», «quello quadratino» | Nome commerciale storpiato dalla trascrizione | `[IMG_1351 @ 0:19-0:28]` | aperto |
| 14 | C | Misura della fettuccia **verde lunga**, «la più grossa che c'è» | Tabella materiale | `[IMG_1369 @ 0:31]` | aperto |
| 15 | D | Misura della fettuccia **piccola viola** | Tabella materiale | `[IMG_1373 @ 0:41]` | aperto |
| 16 | G | Misura della fettuccia **verde e nera** | Tabella materiale | `[IMG_1389 @ 0:02]` | aperto |
| 17 | E–G | «**Banana**»: è il weblock? Quale modello? | Nome di gergo non risolto | `[IMG_1381 @ 0:12]`, `[IMG_1395 @ 0:25]` | ✅ **weblock azzurro anodizzato**, visibile in `IMG_1384 @ 0:03` e `0:50`. Modello ancora aperto |
| 18 | G | Modello del **softrelease** | Tabella materiale | `[IMG_1394 @ 0:15]` | aperto |
| 19 | F | Misura e tipo dei **grilli** | Tabella materiale | `[IMG_1384 @ 0:00]` | aperto |
| 20 | E | Composizione del **paranchino di tensionamento della base** (carrucole, rapporto) | Sequenza di tensionamento | `[IMG_1380 @ 0:09]` | aperto |
| 21 | E | Quanti **Grigri** in totale e su cosa | «un altro Grigri» implica almeno due | `[IMG_1378 @ 0:42]` | aperto |
| 22 | — | Nastro della highline: marca, larghezza, tipo | Mai nominato in nessun video | — | aperto |
| 23 | — | Backup della linea: nastro o corda, quale | Mai specificato | — | aperto |
| 24 | — | Leash e ancoraggio della leash | Mai nominati | — | aperto |

## Manovre

| # | Fase | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 25 | B | **Che nodo è** quello descritto come «pista, pif, paf, sotto, torna sotto» | È il passaggio centrale della sosta e l'audio non lo nomina | `[IMG_1366 @ 0:00]` | aperto |
| 26 | B | **Che nodo è** quello «per forzare la slinga», regolabile | Unica manovra motivata a voce, ma senza nome | `[IMG_1367 @ 0:43]` | aperto |
| 27 | D | «**slide next**» su 3 punti: termine reale | Nome del sistema di collegamento dei 3 punti | `[IMG_1374 @ 0:42]` | aperto |
| 28 | D | Come sono collegati ed equalizzati i 3 punti; angolo di apertura | Sezione ancoraggi | `IMG_1371.JPEG` | **parziale**: si vede il collegamento fra i punti fatto con **corda verde acqua annodata**, non con fettuccia scorrevole. Manca l'inquadratura d'insieme dei 3 punti e l'angolo |
| 29 | C | **Quale componente** «ruotando può cadere» | Va in una callout di avvertenza, ma non si sa di cosa | `[IMG_1370 @ 0:00-0:15]` | aperto |
| 30 | E | **Quale operazione** «andrebbe fatta dopo, quando c'è del peso» | Avvertenza sulla sequenza | `[IMG_1380 @ 0:57]` | aperto |
| 31 | F | Come si costruisce l'**anti-slip** (nodo, materiale, dove) | Funzione chiara, esecuzione no | `[IMG_1395 @ 0:25]`, `[IMG_1384 @ 0:55]` | aperto |
| 32 | F | Cos'è il «**blocco del backup**» che prende sia sosta backup che sosta main | Concetto centrale, mai illustrato a parole | `[IMG_1384 @ 0:37]` | aperto |
| 33 | E | Tensione finale raggiunta e come è stata misurata | Dato di testata; l'audio dice solo «la tensioniamo a modo» | `[IMG_1383 @ 0:19]` | aperto |
| 34 | A | Come è stata portata la linea da un lato all'altro (tagline a mano? drone?) | Sequenza di montaggio. Il drone è citato ma riferito ad altri | `[IMG_1363 @ 0:10-0:14]` | aperto |
| 35 | — | Sequenza di **smontaggio** | Non ripresa in nessun video | — | aperto |
| 36 | — | Checklist pre-uscita realmente usata | Sezione di apparato prevista da CLAUDE.md | — | aperto |

## Aperti dopo la Fase 4 (fotogrammi)

| # | Fase | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 37 | A–D | **Portata (WLL) delle slinghe.** Tipo ✅ confermato: brache ad anello industriali. Resta la portata: in `IMG_1366 @ 0:17` la viola ha **una riga nera**; viola + 1 riga = 1 t in EN 1492-2 | Due indizi convergenti non sono una marcatura. Scrivere una portata sbagliata è il danno peggiore possibile in questo documento | `IMG_1366 @ 0:17` + conferma utente | **aperto — serve foto di un'etichetta** |
| 38 | D | **Nell'ancoraggio c'è protezione veloce (friend) accanto ai punti fissi?** Un dispositivo compatibile si intravede ma il fotogramma è mosso | Cambia la sezione ancoraggi e la checklist | `IMG_1374 @ 0:33` | **rimandato al campo** — l'utente farà lo scatto. Il manuale porta una nota esplicita al posto del dato |
| 39 | D | **Che tipo sono i «punti»** | Sezione ancoraggi | `IMG_1371.JPEG`, `IMG_1372.JPEG` (foto iCloud, 13:41) | ✅ **placchetta metallica su bullone con dado esagonale** — quindi tassello/fittone meccanico, **non** spit a vite né resinato con occhiello integrato. Marca e diametro del bullone restano aperti |
| 40 | D | Marca e modello del dispositivo nero | Tabella materiale | `IMG_1371.JPEG` (dettaglio in `lavorazione/dettagli/`) | ✅ **carrucola bloccante**, guancie nere e puleggia arancio. Marcature lette: `CE 0082`, `UK CA 20`, **`EN 567:2013`**, `Ø 7,8-11 mm`. ⚠ Avevo letto `EN 892` dal video: la foto smentisce. Marca ancora aperta (logo non leggibile) |
| 41 | A | La **corda verde acqua** è la «linea vita» o il cordino di collegamento fra i punti? In `IMG_1371.JPEG` la si vede annodata **fra i punti dell'ancoraggio** | Cambia sia la tabella materiale sia la sequenza | `IMG_1371.JPEG`, `[IMG_1350 @ 0:33]` | aperto — le due funzioni potrebbero coesistere |

| 42 | intro | Dati da i-pietra da validare: settore **Anfiteatro**, roccia **arenaria**, colore linea **#f97316** | Se il manuale li stampa, devono essere corretti anche fuori dall'app | catalogo i-pietra | aperto |
| 43 | — | **Locandina delle linee** ✅ ricevuta: «La Pietra — Yeah Vez!», 5 aree e 24 linee | Fonte per la planimetria d'insieme | locandina | ✅ letta — **manca il file** per riprodurla nel PDF |
| 44 | intro | **Anno del Bismantova Highline Meeting** sul logo della locandina | Didascalia della planimetria | locandina, logo poco leggibile | aperto |
| 45 | intro | **Titolo definitivo del manuale.** «La 50» collide con la **50 M del Settore Giallo**, che esiste davvero | Un lettore potrebbe attrezzare la linea sbagliata: è l'ambiguità più pericolosa del documento | locandina | aperto — per ora «la 50, settore Anfiteatro», mai «la 50» da sola |
| 46 | — | Cos'è la **«Bifida»** `[IMG_1373 @ 0:24]`: non compare sulla locandina | Capire a cosa si riferisce l'aneddoto | locandina | aperto |

| 47 | — | **Materiale iCloud** acquisito: 19 foto + 14 video (1 min 57 s), 16/05/2026 | Immagini di apertura e prova del montaggio concluso | `foto/`, `video_icloud/` | ✅ esaminato. Le foto 17:08-17:14 mostrano **la linea montata e camminata**, oltre 1 h 30 dopo l'ultimo video di montaggio |
| 49 | intro | **La giornata prosegue fino alle 17:14**, ma fra 15:38 e 17:08 non c'è nulla: manca la documentazione di tensionamento finale e primi passaggi | Il manuale deve dichiarare il buco | metadati | aperto |
| 48 | — | I video nuovi contengono parlato tecnico? | Speranza di colmare i buchi dell'audio | `video_icloud/` | ✅ **no.** Trascritti tutti e 14: 11 sono Live Photo da 1-3 s; `IMG_1408` (0:49) dice solo «Olé, olé, olé», `IMG_1411` e `IMG_1417` sono muti. Valgono come **immagini**, non come fonte parlata |
| 50 | E | **C'è un A-frame** — due pali di legno con fettucce — visibile in `IMG_1396.JPG`, mai nominato in nessuna trascrizione né notato prima | Elemento strutturale del lato tensione: altezza, materiale e ancoraggio a terra sono tutti ignoti | `foto/IMG_1396.JPG` | aperto |
| 51 | — | Il **nastro della linea appare bianco/crema** in `IMG_1401`, con un secondo nastro chiaro parallelo (backup?) | Chiude i dubbi 22 e 23 se confermato | `foto/IMG_1401.JPG` | aperto |
| 52 | intro | **I due cataloghi non concordano sul nome del settore.** i-pietra etichetta «Anfiteatro» anche le tre linee che la locandina mette sotto **Anfite-altro** (22, 30, 135 m). Qual è il nome che usate voi? | Stesso rischio del dubbio 45: chi cerca una linea partendo dall'app e chi parte dalla locandina finisce in due settori diversi | render 3D i-pietra, forniti dall'utente il 20/08/2026 | **confermato a immagine** — in `fonti/render_ipietra/anfite-altro.png` le tre linee portano l'etichetta «Anfiteatro». Resta da decidere quale nome usa il manuale |
| 53 | intro | **La copertura di i-pietra è cambiata fra le due letture.** Il 19/08 lo snapshot del 5 agosto dava 12 linee su 24, senza i settori Despedida e Settore Giallo; il 20/08 i render ne mostrano 22 su 24 | Il numero finisce stampato nel capitolo sulle linee | snapshot 05/08/2026 + render 3D 20/08/2026 | ✅ **chiuso** — vale il dato del 20/08: **22 su 24**, mancano la 20 m e la 108 m dell'Anfiteatro. ⚠ Non era una lettura sbagliata: lo snapshot del 5 agosto quei settori non li conteneva proprio. Il manuale stampa il dato **con la data** |

## Note da riportare nel manuale

Richieste esplicite dell'utente, da stampare nel PDF e non solo qui.

| # | Dove | Testo della nota |
|---|---|---|
| N1 | Sezione ancoraggi | Il dettaglio dei punti dell'ancoraggio non è documentato dai video disponibili: **fotografia da fare sul campo alla prossima uscita**. Fino ad allora la scheda resta incompleta e dichiarata tale. |
| N2 | Testata / planimetria | La lunghezza della campata è **da rimisurare**: il valore di 53 m viene dal catalogo i-pietra e dalla locandina, non da una misura fatta sul posto. |
| N3 | Planimetria | Alla Pietra esiste **un'altra linea da 50 m, al Settore Giallo**. Questo manuale riguarda la linea dell'**Anfiteatro**. |

## Questioni di metodo

| # | Cosa | Nota | Stato |
|---|---|---|---|
| M1 | `IMG_1379` — trascrizione allucinata dal modello («iscrivetevi al canale»). Da cestinare, il video va guardato | non è un dato, è un artefatto | segnalato |
| M2 | `IMG_1375 @ 0:29-0:39` — «non pubblicare» | ✅ l'utente conferma che era una battuta: file utilizzabile. Restano fuori dal manuale i commenti sul materiale delle singole persone, privi di valore tecnico | ✅ chiuso |
| M3 | I video coprono 22 min 47 s su un arco di 2 h 38 min: parte del montaggio non è filmata | i buchi vanno dichiarati nel manuale | segnalato |
