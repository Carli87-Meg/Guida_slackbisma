# Dubbi da chiarire prima della pubblicazione

Elenco di tutto ciò che nel manuale sarebbe marcato `[DA CONFERMARE]`.
Nessuna di queste voci va risolta per deduzione: servono risposte da chi ha montato la linea.

Stato al 27/10/2026: pipeline conclusa per la 53 m (fasi 1-6), guida all'edizione del 27/10.
Bloccanti risolti il 19/08/2026. Le voci aperte qui sotto sono anche nella scheda da campo
`output/Bismantova_Dubbi_Scheda_Campo.pdf` (`python build/build_scheda_dubbi.py`).

**27/10/2026 — fonti lette per le domande della lista «S1».** Sono state lette in sola lettura:
- SlackMap dell'International Slackline Association: tutte le 24 linee della Pietra;
- il progetto i-pietra: lotto 31 e export del 21/10;
- il catalogo del materiale: Foglio Google e foto delle etichette;
- i metadati GPS di foto e video;
- OpenStreetMap e theCrag.

Esito:
- **chiuso il dubbio 56**;
- **aggiornati** i dubbi 1, 3, 28, 37, 38, 39, 45, 50, 54;
- **nuova** la voce 58.

**27/10/2026 — le foto di Carlo.** Le 31 fotografie di `LineeBisma.xlsx` (Drive, 20/10/2026)
sono state lette una per una, con ingrandimenti, in `lavorazione/foto_linee/<id>/LETTURA.md`
e confrontate con le parole di Carlo nel Foglio «Linee». Ne nascono le voci **59-69**, nella
sezione «Aperti dalle foto di Carlo». Nessuna chiude un dubbio della 53 m: la sola foto di
quella linea è di una terza uscita, in autunno, e non mostra il cavalletto.

Su SlackMap la scheda della 53 m («GAS-OH», `nym-s4g`) non ha nessun testo. Fra le 24 linee
l'unica con una descrizione di ancoraggi e materiale è la **Brifing** (113 m, `t2qJAK8`),
scritta il 10/11/2025 da un account che risulta di Lasa. Riguarda un'altra linea e non si
trasferisce alla 53 m. Lasa resta un candidato a cui chiedere: per la 53 m SlackMap non dice nulla.

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
| 1 | intro | Lunghezza effettiva della campata | Dato di testata | mai pronunciata | **riaperto** — i-pietra e locandina danno 53 m, ma l'utente rimisurerà sui punti. Nome di lavoro: «la 50». **27/10/2026**: nessuna delle fonti nuove è una misura. SlackMap dà 52,84 m, ma è la lunghezza del segmento disegnato (`isMeasured: false`). La linea 3D di i-pietra dà 46,7 m, e i-pietra stesso stampa la lunghezza di catalogo (`31-highline.md:11`). Fra le due posizioni del telefono ci sono 51,4 m (voce 3). Resta la misura sui punti |
| 2 | intro | Dislivello / offlevel fra i due lati | Dato di testata, influenza il tensionamento | mai pronunciato | aperto |
| 3 | intro | Coordinate dei due ancoraggi | Intestazione dei blocchi materiale (cliccabili) | mai pronunciate | ✅ **chiuso il 27/10/2026** (posizioni dal telefono, lati dalla voce 56) — **ancoraggio main** a `44.419869, 10.412353`, quota 1025 m: EXIF di `IMG_1416`, scattata stando lì il 16/05/2026 alle 17:14 (utente, 20/08/2026). **Altro capo** a `44.419453, 10.412072`, quota 1025 m: dieci letture entro 3 m del 22/08/2026 (`IMG_3323`-`3332`, la 53 m montata con i bungee, utente 08/10/2026), a 51,4 m dal main (ricalcolata il 27/10/2026; prima scritto 51,5), coerente con una linea di 53 m. L'accuratezza dichiarata è di 4,5 m per `IMG_1416` e di 4,8 m per `IMG_3323`. Sono posizioni del telefono, non un rilievo. Le quote del telefono non danno il dislivello: all'altro capo `IMG_1371` legge 1008 m, `IMG_3323`-`3332` 1025 m. I `linePoints` di i-pietra si convertono in GPS con la calibrazione della scena, ma i capi della linea 3D cadono a 6 m dal main e a 12 m dall'altro capo: per la posizione valgono le letture del telefono. **Il lato tensione è il main**: dubbio 56, chiuso il 27/10/2026 |
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
| 12 | A | Misura e materiale delle **4 maglie delta** | Unica quantità certa del corpus, manca la misura | `[IMG_1350 @ 0:53]`, `IMG_1360` | aperto — in `IMG_1360` se ne vede una **d'acciaio, con ghiera filettata incisa**, ma l'incisione non è leggibile |
| 13 | A | Cos'è il «**Mighty Lock**», «quello quadratino» | Nome commerciale da identificare | `[IMG_1351 @ 0:19-0:28]` | aperto, **con una pista** — il nome non è storpiato: nella lista della cernita di Matte Kode (09/10/2026) c'è un «Mightylock», catalogato come **MightyLock di Balance Community** (KOD-009), che il produttore descrive come anello di forma quadrata. È coerente con «quello quadratino», ma che sia il pezzo usato il 16/05 e come lavorasse nel backup lo deve dire chi c'era |
| 14 | C | Misura della fettuccia **verde lunga**, «la più grossa che c'è» | Tabella materiale | `[IMG_1369 @ 0:31]` | aperto |
| 15 | D | Misura della fettuccia **piccola viola** | Tabella materiale | `[IMG_1373 @ 0:41]` | aperto |
| 16 | G | Misura della fettuccia **verde e nera** | Tabella materiale | `[IMG_1389 @ 0:02]` | aperto |
| 17 | E–G | «**Banana**»: è il weblock? Quale modello? | Nome di gergo non risolto | `[IMG_1381 @ 0:12]`, `[IMG_1395 @ 0:25]` | ✅ **weblock azzurro anodizzato**, visibile in `IMG_1384 @ 0:03` e `0:50`. Modello ancora aperto |
| 18 | G | Modello del **softrelease** | Tabella materiale | `[IMG_1394 @ 0:15]` | aperto |
| 19 | F | Misura e tipo dei **grilli** | Tabella materiale | `[IMG_1384 @ 0:00]`, `IMG_1360` | aperto — in `IMG_1360` si vedono **grilli a lira d'acciaio con perno**, marcature non leggibili |
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
| 28 | D | Come sono collegati ed equalizzati i 3 punti; angolo di apertura | Sezione ancoraggi | `IMG_1371.JPEG` | **parziale**: si vede il collegamento fra i punti fatto con **corda verde acqua annodata**, non con fettuccia scorrevole. Manca l'inquadratura d'insieme dei 3 punti e l'angolo. **27/10/2026**, dalle immagini: `IMG_1369` è girato vicino all'altro capo. Fra `0:05` e `0:45` si vedono **almeno tre placchette lungo la stessa parete**; a `0:27` ce n'è una nuda più in basso. Il 22/08, più in basso, `IMG_3331` mostra invece un bullone **senza** placchetta: se sia lo stesso punto, e se la placchetta sia stata tolta, non si sa. Il fotogramma più leggibile della sosta è `IMG_1374 @ 0:48`: HMS sulla placchetta, nodo della corda verde acqua, cordino rosso, braca viola, moschettone arancio, carrucola. Il 22/08 (`IMG_3329`) due placchette affiancate portano ciascuna una braca viola, e in `IMG_3324`-`3326` la braca entra **direttamente in un grillo a lira**, senza maglia rapida visibile. L'angolo non si ricava da nessuna immagine |
| 29 | C | **Quale componente** «ruotando può cadere» | Va in una callout di avvertenza, ma non si sa di cosa | `[IMG_1370 @ 0:00-0:15]` | aperto |
| 30 | E | **Quale operazione** «andrebbe fatta dopo, quando c'è del peso» | Avvertenza sulla sequenza | `[IMG_1380 @ 0:57]` | aperto |
| 31 | F | Come si costruisce l'**anti-slip** (nodo, materiale, dove) | Funzione chiara, esecuzione no | `[IMG_1395 @ 0:25]`, `[IMG_1384 @ 0:55]` | aperto |
| 32 | F | Cos'è il «**blocco del backup**» che prende sia sosta backup che sosta main | Concetto centrale, mai illustrato a parole | `[IMG_1384 @ 0:37]` | aperto |
| 33 | E | Tensione finale raggiunta e come è stata misurata | Dato di testata; l'audio dice solo «la tensioniamo a modo» | `[IMG_1383 @ 0:19]` | aperto |
| 34 | A | Come è stata portata la linea da un lato all'altro (tagline a mano? drone?) | Sequenza di montaggio. Il drone è citato ma riferito ad altri | `[IMG_1363 @ 0:10-0:14]` | aperto |
| 35 | — | Sequenza di **smontaggio** | Non ripresa in nessun video | — | aperto |
| 36 | — | Checklist pre-uscita realmente usata | Sezione di apparato prevista da CLAUDE.md | — | aperto |

## Aperti dopo la Fase 4 e con le fonti arrivate dopo

Fotogrammi (Fase 4), locandina, materiale iCloud, render i-pietra, foto del 22/08.

| # | Fase | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 37 | A–D | **Portata (WLL) delle slinghe.** Tipo ✅ confermato: brache ad anello industriali. Resta la portata: in `IMG_1366 @ 0:17` la viola ha **una riga scura** per il lungo | Due indizi convergenti non sono una marcatura. Scrivere una portata sbagliata è il danno peggiore possibile in questo documento | `IMG_1366 @ 0:17`, `IMG_1360`, `IMG_1357` | **aperto, ma adesso si sa dove guardare** — in `IMG_1360` (utente, 20/08/2026) **l'etichetta si vede**: bianca, cucita con filo blu sulla cucitura della calza, **rivoltata e illeggibile**. Ne compare una anche in `IMG_1357`. Serve **una foto ravvicinata dell'etichetta distesa**, nient'altro. **10/10/2026**: con l'inventario del materiale del gruppo sono arrivate le foto di cinque etichette leggibili, tutte EN 1492-2; due sono di brache **viola FAS**, da 1 m e da 2 m, con **WLL 1 Ton**. Non chiude il dubbio: non è stabilito che le viola della sosta main del 16/05 fossero quelle. Va chiesto di chi erano e, se erano FAS, letta l'etichetta di quelle. **27/10/2026**: l'utente indica il catalogo come fonte dell'etichetta. Quello che il catalogo dice:<br>• le righe di brache viola sono 7, per **8 pezzi**. Tutte hanno **etichetta «Non controllata»**; il «1T» della colonna portata viene dalla lista della cernita del 09/10, non da un'etichetta;<br>• le foto di etichette viola sono tre, nessuna legata a un pezzo: FAS 1 m **WLL 1 Ton**; FAS 2 m, 2024, **WLL 1 Ton**; Spider EN 1492-2:2000, con un «1 T» probabile sotto un riflesso. Tutte EN 1492-2.<br>Dalle foto del 16/05: alla sosta main ci sono **due tinte**, lilla chiaro e viola scuro (`IMG_1359`, `IMG_1364`). La lilla porta una **linguetta blu stampata** accanto all'etichetta bianca, tutte e due illeggibili (`IMG_1357`), e compare anche all'A-frame (`IMG_1396`). Il 22/08, su una viola scuro, si legge solo «…ING LOAD LI…» (`IMG_3326`).<br>**Resta aperto**: le due FAS dicono 1 t e la Spider probabilmente anche, ma nessuna è di un pezzo che si sa usato il 16/05. Serve sapere quali erano e leggerne l'etichetta. Fino ad allora la scheda non stampa la portata |
| 38 | D | **Nell'ancoraggio c'è protezione veloce (friend) accanto ai punti fissi?** Un dispositivo compatibile si intravede ma il fotogramma è mosso | Cambia la sezione ancoraggi e la checklist | `IMG_1374 @ 0:33` | **rimandato al campo** — l'utente farà lo scatto. Il manuale porta una nota esplicita al posto del dato. **27/10/2026**: l'oggetto mosso di `IMG_1374 @ 0:33` ha moschettone con ghiera rossa e parti arancio, come la carrucola bloccante, che nel fotogramma nitido `0:48` sta nello stesso gruppo. In nessuna immagine si vede una camma. Non vedere un friend non prova che non ci fosse |
| 39 | D | **Che tipo sono i «punti»** | Sezione ancoraggi | `IMG_1371.JPEG`, `IMG_1372.JPEG` (foto iCloud, 13:41) | ✅ **placchetta metallica su bullone con dado esagonale** — quindi tassello/fittone meccanico, **non** spit a vite né resinato con occhiello integrato. Marca e diametro del bullone restano aperti. **27/10/2026**, dalle foto dell'altro capo:<br>• su una placchetta si legge «**FOR 1 PERSON**», con un codice incerto simile a «KD08KL» (`IMG_3324`);<br>• in `IMG_1372` c'è un'incisione incerta «…0210…»; in `IMG_3329` le incisioni non sono leggibili;<br>• più in basso c'è un **prigioniero senza placchetta** (`IMG_3331`; la foto mostra una persona e non va pubblicata). Il 16/05, nello stesso punto, c'era forse una placchetta: voce 28.<br>Il produttore non si identifica. Su SlackMap la scheda della Brifing parla di barre filettate incollate chimicamente: che i punti della 53 m siano tasselli meccanici e non barre resinate va quindi confermato. Chi abbia posato i punti non lo dice nessuna fonte: da chiedere al gruppo |
| 40 | D | Marca e modello del dispositivo nero | Tabella materiale | `IMG_1371.JPEG` (dettaglio in `lavorazione/dettagli/`) | ✅ **carrucola bloccante**, guancie nere e puleggia arancio. Marcature lette: `CE 0082`, `UK CA 20`, **`EN 567:2013`**, `Ø 7,8-11 mm`. ⚠ Avevo letto `EN 892` dal video: la foto smentisce. Marca ancora aperta (logo non leggibile) |
| 41 | A | La **corda verde acqua** è la «linea vita» o il cordino di collegamento fra i punti? In `IMG_1371.JPEG` la si vede annodata **fra i punti dell'ancoraggio** | Cambia sia la tabella materiale sia la sequenza | `IMG_1371.JPEG`, `[IMG_1350 @ 0:33]` | aperto — le due funzioni potrebbero coesistere |
| 42 | intro | Dati da i-pietra da validare: settore **Anfiteatro**, roccia **arenaria**, colore linea **#f97316** | Se il manuale li stampa, devono essere corretti anche fuori dall'app | catalogo i-pietra | aperto |
| 43 | — | **Locandina delle linee** ✅ ricevuta: «La Pietra — Yeah Vez!», 5 aree e 24 linee | Fonte per la planimetria d'insieme | locandina | ✅ letta — **manca il file** per riprodurla nel PDF |
| 44 | intro | **Anno del Bismantova Highline Meeting** sul logo della locandina | Didascalia della planimetria | locandina, logo poco leggibile | aperto |
| 45 | intro | **Titolo definitivo del manuale.** «La 50» collide con la **50 M del Settore Giallo**, che esiste davvero | Un lettore potrebbe attrezzare la linea sbagliata: è l'ambiguità più pericolosa del documento | locandina | aperto — per ora «la 50, settore Anfiteatro», mai «la 50» da sola. **27/10/2026**: su SlackMap la linea si chiama **«GAS-OH»** (`nym-s4g`, 52,84 m). i-pietra l'ha ripreso da SlackMap (lotto 31, applicato il 21/10: «Gas-oh», con «detta la 50» come soprannome), quindi non è una seconda fonte. Il nome compare anche in una riunione del gruppo di ottobre. Un nome proprio scioglierebbe la collisione con la 50 m del Settore Giallo, che su SlackMap non ha nome. La scelta del titolo resta del gruppo |
| 46 | — | Cos'è la **«Bifida»** `[IMG_1373 @ 0:24]`: non compare sulla locandina | Capire a cosa si riferisce l'aneddoto | locandina | aperto |
| 47 | — | **Materiale iCloud** acquisito: 19 foto + 14 video (1 min 57 s), 16/05/2026 | Immagini di apertura e prova del montaggio concluso | `foto/`, `video_icloud/` | ✅ esaminato. Le foto 17:08-17:14 mostrano **la linea montata e camminata**, oltre 1 h 30 dopo l'ultimo video di montaggio |
| 48 | — | I video nuovi contengono parlato tecnico? | Speranza di colmare i buchi dell'audio | `video_icloud/` | ✅ **no.** Trascritti tutti e 14: 11 sono Live Photo da 1-3 s; `IMG_1408` (0:49) dice solo «Olé, olé, olé», `IMG_1411` e `IMG_1417` sono muti. Valgono come **immagini**, non come fonte parlata |
| 49 | intro | **La giornata prosegue fino alle 17:14**, ma fra 15:38 e 17:08 non c'è nulla: manca la documentazione di tensionamento finale e primi passaggi | Il manuale deve dichiarare il buco | metadati | aperto |
| 50 | E | **C'è un A-frame** — due pali di legno con fettucce — mai nominato in nessuna trascrizione | Elemento strutturale del lato tensione: altezza, materiale e ancoraggio a terra sono tutti ignoti | `IMG_1396`, `IMG_1416` | **parziale** — con `IMG_1416` (utente, 20/08/2026) l'A-frame ha una sezione nel manuale. Si vede che sta **sul lato dell'ancoraggio main**, che i piedi **appoggiano sulla roccia** e che attorno al piede di un palo ci sono **giri di filo metallico** che proseguono orizzontali. Restano aperti: altezza, diametro del legno, legatura in testa, di quanto solleva la linea, e **se quel filo tenga il palo o sia un recinto preesistente**. **27/10/2026**, dalle immagini (`IMG_1396`, `IMG_1416`):<br>• c'è filo metallico al piede di **tutti e due i pali**, non di uno solo: 2-3 giri a quello di sinistra, almeno uno, in parte coperto dalla corda verde, a quello di destra. Da un palo all'altro corrono fili orizzontali;<br>• in testa ci sono un cordino marrone annodato sotto l'incrocio, una fettuccia blu ad anse, una corda verde lime e la braca lilla;<br>• la linea arriva sul fianco esterno del palo di sinistra, visto dall'ancoraggio, poco sotto l'incrocio;<br>• dall'A-frame passano anche le corde rosa della sosta backup.<br>Che il filo leghi i piedi è compatibile, ma non dimostrato. Altezza e diametro non si ricavano: nelle foto manca un oggetto di misura nota |
| 51 | — | Il **nastro della linea appare bianco/crema** in `IMG_1401`, con un secondo nastro chiaro parallelo (backup?) | Chiude i dubbi 22 e 23 se confermato | `foto/IMG_1401.JPG` | aperto |
| 52 | intro | **I due cataloghi non concordano sul nome del settore.** i-pietra etichetta «Anfiteatro» anche le tre linee che la locandina mette sotto **Anfite-altro** (22, 30, 135 m). Qual è il nome che usate voi? | Stesso rischio del dubbio 45: chi cerca una linea partendo dall'app e chi parte dalla locandina finisce in due settori diversi | render 3D i-pietra, forniti dall'utente il 20/08/2026 | **confermato a immagine** — in `fonti/render_ipietra/anfite-altro.png` le tre linee portano l'etichetta «Anfiteatro». Resta da decidere quale nome usa il manuale |
| 53 | intro | **La copertura di i-pietra è cambiata fra le due letture.** Il 19/08 lo snapshot del 5 agosto dava 12 linee su 24, senza i settori Despedida e Settore Giallo; il 20/08 i render ne mostrano 22 su 24 | Il numero finisce stampato nel capitolo sulle linee | snapshot 05/08/2026 + render 3D 20/08/2026 | ✅ **chiuso** — vale il dato del 20/08: **22 su 24**, mancano la 20 m e la 108 m dell'Anfiteatro. ⚠ Non era una lettura sbagliata: lo snapshot del 5 agosto quei settori non li conteneva proprio. Il manuale stampa il dato **con la data** |
| 54 | — | **Nello sfondo di `IMG_1416` e `IMG_1396` corre una linea tesa con, sotto, una seconda linea chiara appesa a festoni.** Non si capisce se sia la campata della 53 m vista di scorcio o un'altra linea dello spot | Se fosse un'altra linea, due fotografie del capitolo della 53 m ne mostrerebbero una diversa senza dirlo | `IMG_1416`, `IMG_1396` | **chiarito a immagine il 27/10/2026: è un'altra linea.** In `IMG_1396`, `IMG_1407` e `IMG_1416` la 53 m si vede a parte, dall'A-frame alla sommità del pilastro opposto, con una persona sopra. La coppia di linee (tesa e a festoni) parte dallo stesso pilastro e va verso sinistra nell'immagine; la direzione non si ricava da una foto sola. Quale linea sia, e quindi la voce 55, resta da chiedere |
| 55 | E | **Che cos'è la seconda linea appesa a festoni** sotto quella tesa: backup, tagline lasciata in posa, o altro | Chiude in parte i dubbi 23 e 24 | `IMG_1416`, `IMG_1396` | aperto |
| 56 | A, D, E, F | **Quale lato è quale sulla 53 m.** La guida è organizzata per lati: *lato tensione* = dove stanno sosta main e sosta backup, dove si tensiona e dove sta l'A-frame; *lato statico* = la sosta su tre punti con le placchette e la linea vita. È **ricostruito** dall'ordine delle operazioni (sezione D «sosta sull'altro lato, su 3 punti»; il blocco del backup che prende sia main sia backup) e dalla risposta del 20/08 sull'A-frame, non dichiarato | Un lato scambiato in una guida di montaggio manda a costruire la sosta sbagliata dalla parte sbagliata | NOTE_RIGGING A-F, risposta utente 20/08/2026 | ✅ **chiuso il 27/10/2026.** L'utente: «il lato di tensione è quello della parte sopra Cocoa». Alla domanda di verifica ha confermato che Cocoa è il settore di falesia che sta al main: OSM `node/11925326320`; theCrag area `7751514930`; in i-pietra «Cocoa» (falesia.it lo chiama «Cocoa - Anfiteatro Alto»). È il terrazzo sopra la Pincelli-Brianti, 10 m sotto il bordo della sommità. Il punto OSM di Cocoa sta a 10,9 m dal main e a 46,5 m dall'altro capo; il main sta a nord-nord-est dell'altro capo. **Tensione al main** (44.419869, 10.412353): sosta main, sosta backup, A-frame. **Statico all'altro capo** (44.419453, 10.412072): la sosta su tre punti. La ricostruzione era giusta, e anche il GPS delle riprese è coerente. `IMG_1373`-`1375` sono a 6-8 m dall'altro capo, i video del tensionamento `IMG_1378`-`1395` a 5-13 m dal main. Le posizioni dei video sono registrate con quattro decimali, cioè su una griglia di circa 11 × 8 m: le distanze valgono a meno di qualche metro, ma i due capi distano 51 m. Fa eccezione `IMG_1384`, con un'accuratezza di 63,8 m: inutilizzabile. Vedi anche la voce 58 |
| 57 | — | **Le foto del 22/08 sulla cresta (IMG_3308-3322)**: quali sono della Despedida e quali del Settore Giallo; e se la roccia sullo sfondo di `IMG_3311` è davvero quella della **Despedida 165 m** («dovrebbe essere», utente 08/10/2026) | Una vista del settore entra nella guida solo con la linea giusta in didascalia | `IMG_3308`-`IMG_3322` | aperto — **da chiedere a chi ha accompagnato il sopralluogo**; possibile fonte anche i video delle linee montate pubblicati online |
| 58 | A–F | **Il GPS dei video sposta un'attribuzione di fase.** `IMG_1376` sta in `NOTE_RIGGING.md` nella fase D, «sosta sull'altro lato», ma è stato girato **al main**: 5,4 m, accuratezza 13,3 m. Le fasi A e B (`IMG_1349`, `1351`, `1363`, `1366`, `1367`) sono girate al main, a 5-15 m; `IMG_1368` sta a metà strada (29 m dal main, 39 m dall'altro capo) e non si attribuisce a nessuno dei due capi; `IMG_1369` (fase C) sta vicino all'altro capo. Le posizioni dei video sono su una griglia di circa 11 × 8 m (quattro decimali). Alcuni GPS non sono usabili: `IMG_1384` (63,8 m), `IMG_1370` (69,8 m), `IMG_1377` (186 m), `IMG_1350` (36,5 m) | Una manovra attribuita al lato sbagliato finisce nella sosta sbagliata | metadati QuickTime `com.apple.quicktime.location` dei video, letti il 27/10/2026 | aperto — rivedere la fase D in `NOTE_RIGGING.md` e chiedere che cosa si faceva al main in `IMG_1376` |

## Aperti dalle foto di Carlo (27/10/2026)

Le fotografie stanno in `lavorazione/foto_linee/<id>/`, con `ORIGINE.md` (scheda, cella,
lato di Carlo) e `LETTURA.md` (che cosa si vede, che cosa manca). «Vicino» e «lontano» sono
i lati di Carlo, non tensione e statico. Tutto ciò che Carlo scrive è segnato da lui «da
controllare». Nessuna foto ha EXIF. Le voci vanno chieste **a Carlo**, che ha messo le foto
nel file, e a chi era sul posto.

| # | Linea | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 59 | 108 / 113 | **Di quale linea è la sosta con il tronco.** Le stesse foto (tronco chiaro scortecciato legato con cordino viola, slinghe verdi che lo scavalcano, moschettone su anello fisso, corda in calza grigia e rossa, braca viola) stanno sia sulla riga della 108 (D7, U7) sia su quella della 113 (D8). Sono su una terrazza di roccia **senza alberi**: corrispondono al lato lontano che Carlo dà alla 113 («Bisma standard senza cavalletto + tronco»), non a quello della 108 («alberi e uno spit») | Una sosta attribuita alla linea sbagliata manda a cercarla sul capo sbagliato | `anfiteatro-108_01`, `_02`, `_03`; `anfiteatro-113_05`, `_06`, `_07` | aperto — da chiedere a Carlo |
| 60 | 46, 97, 108, 113, 60, 70 | **Il lato di tensione di ogni linea fotografata.** Nessuna foto lo mostra con certezza. Indizi, non prove: sul lato lontano della 46 un dispositivo bianco/argento della forma di un weblock (`46_03`, `_04`); sul lato vicino di 46 e 53 due fettucce con calza che convergono su grillo e softshackle (`46_01`, `53_01`); un cavalletto sul lato vicino di 46, 113, 70 e sul lato lontano di 70 | La guida è organizzata per lati: senza questo dato le foto restano foto, non documentazione degli ancoraggi (vedi `lavorazione/ancoraggi/LEGGIMI.md`) | tutte le cartelle | aperto — lo deve dichiarare chi c'era |
| 61 | tutte | **Data e autore di ogni foto.** Excel ha tolto gli EXIF. Si legge solo la stagione: il cavalletto della 113 compare in tre configurazioni (pali tondi con corda verde d'estate, pali tondi con fascia viola d'autunno, assi squadrate di notte), quello della 46 in due (corda canapa d'autunno, corda rosa d'estate): sono almeno tre e due uscite | Senza data non si sa quale montaggio sia e se il materiale sia ancora quello | `113_01`-`_04`, `_08`; `46_01`, `_05` | aperto — da chiedere a Carlo |
| 62 | 97 | **La «91» di Carlo è la 97 m del registro?** Le sue righe (schema, note, foto) sono state messe sulla 97 per posizione: Anfiteatro 46, 53, 91, 108, 113 nel suo file contro 46, 53, 97, 108, 113 nel registro | Un dato attribuito alla linea sbagliata | `LineeBisma.xlsx`, scheda «Elenco» | aperto — anche nel Foglio «Da chiarire» |
| 63 | 108 | **Dove sono «alberi e uno spit» del lato lontano.** Carlo descrive il montaggio («Montaggio con alberi e uno spit. Sosta molto lunga, portare corde lunghe anche per fare un deviatore»), ma nessuna foto sulla sua riga mostra alberi. Se la sosta con il tronco è della 113 (voce 59), della 108 non resta nessuna foto | La descrizione è l'unico dato sul lato lontano della 108 e non ha riscontro | `anfiteatro-108/LETTURA.md` | aperto |
| 64 | 46, 53 | **Che cosa sono le due fettucce nere con calza marcate Spider** (`46_02`, etichetta leggibile) che convergono su grillo e softshackle arancione (`46_01`, `53_01`), e che cosa fa il piccolo elemento su cui convergono. Stesso materiale, stessa stagione (autunno), stesso parcheggio sotto in 46 e 53: se siano la stessa giornata, o la stessa sosta messa da Carlo su due righe | Se fossero la stessa sosta, una delle due linee non avrebbe foto del lato vicino | `46_01`, `46_02`, `53_01` | aperto — da chiedere a Carlo |
| 65 | 46 | **Il dispositivo bianco/argento del lato lontano**, con fettuccia nera avvolta, da cui parte la fettuccia con calza: weblock? Marca e modello non leggibili. Se fosse un weblock, il lato di tensione sarebbe il lontano, quello senza cavalletto | Decide la voce 60 per la 46 | `46_03`, `46_04` | aperto |
| 66 | 70 | **Un cavalletto a tutti e due i capi?** Il lato vicino (`70_01`, estate) e il lato lontano (`70_02`, autunno) di Carlo mostrano tutti e due un cavalletto di due pali. E sul lato lontano: a che cosa è ancorata la corda doppia su cui si annodano le slinghe verdi (`70_03`), e che cos'è la calza bianca che gira attorno a un masso sul bordo (`70_04`) | Un capo senza punti fissi cambia tutto il metodo | `despedida-70/LETTURA.md` | aperto |
| 67 | 60 | **Il lato lontano su alberi**: funzione della fettuccia nera Gibbon (dal tronco sottile a tre moschettoni a ghiera) e della corda arancione annodata al tronco grosso; se i due pali sottili incrociati siano un cavalletto. **Del lato vicino non c'è nessuna foto** | Unico dato sulla 60 m: il Foglio di Carlo è vuoto | `despedida-60_01`-`_06` | aperto |
| 68 | 113 (o 108) | **Le etichette alla sosta con il tronco.** Sulla calza di una slinga verde una scritta scura (sembra «2 t», non leggibile con certezza); sulla braca viola un'etichetta azzurra cucita, illeggibile. Vanno fotografate distese, come per il dubbio 37 | La portata delle brache è il dato più pericoloso da sbagliare | `113_05`, `113_06` | aperto — foto da fare sul campo |
| 69 | 97 | **Quale delle due linee parallele è la 97.** La foto del lato vicino mostra due linee (rosa e bianca) che partono dalla stessa cima, con un highliner su ciascuna | La miniatura della 97 nella guida mostra due linee senza dire quale sia | `anfiteatro-97_01` | aperto |

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
