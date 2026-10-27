# Dubbi da chiarire prima della pubblicazione

Elenco di tutto ciò che nel manuale sarebbe marcato `[DA CONFERMARE]`.
Nessuna di queste voci va risolta per deduzione: servono risposte da chi ha montato la linea.

Stato al 27/10/2026: pipeline conclusa per la 53 m (fasi 1-6), guida all'edizione del 27/10.
Bloccanti risolti il 19/08/2026. Tutte le voci aperte qui sotto, comprese quelle con una
parte ancora aperta, sono anche nella scheda da campo `output/Bismantova_Dubbi_Scheda_Campo.pdf`
(`python build/build_scheda_dubbi.py`); la 55 vi compare dentro la 54.

**Conteggio al 27/10/2026**, voci numerate 1-74:

| Stato | Quante | Quali |
|---|---|---|
| Chiuse | 7 | 3, 45, 47, 48, 52, 53, 56 |
| Con risposta, ma una parte ancora aperta | 4 | 17, 39, 40, 43 |
| Aperte | 63 | tutte le altre; 16 sono nate dal file LineeBisma e dalle sue foto (59-74) |

Criterio: **chiusa** se lo Stato comincia con ✅ e non lascia niente da chiedere; **con una
parte aperta** se la domanda principale ha risposta (✅) ma resta un dato, come marca,
modello o file; **aperta** tutto il resto, comprese le voci «parziale», «riaperto» e
«rimandato al campo». Fuori conteggio: B1-B3 e M2 chiusi, M1 e M3 segnalati, N1-N3 note da
stampare.

**27/10/2026 — fonti lette per le domande della lista «S1».** Sono state lette in sola lettura:
- SlackMap dell'International Slackline Association: tutte le 24 linee della Pietra;
- il progetto i-pietra: lotto 31 e export del 21/10;
- il catalogo del materiale: Foglio Google e foto delle etichette;
- i metadati GPS di foto e video;
- OpenStreetMap e theCrag.

Esito:
- **chiusi i dubbi 3 e 56**;
- **aggiornati** i dubbi 1, 28, 37, 38, 39, 45, 50, 54;
- **nuova** la voce 58.

(Prima qui la 3 stava fra le aggiornate, mentre la sua riga la dava già chiusa: corretto il
27/10/2026.)

**27/10/2026 — decisioni dell'utente** (nell'artefatto «Dalle riunioni alla guida»):
- **D3**: nel titolo la 53 m dell'Anfiteatro si chiama **«GAS-OH»**, il nome che ha su
  SlackMap (`nym-s4g`). «La 50» resta il soprannome del gruppo, e resta la nota N3 sull'altra
  50 m della Pietra, al Settore Giallo. **Chiude il dubbio 45.**
- **D4**: per le linee da 22, 30 e 135 m il settore è **«Anfite-altro»**, come la locandina;
  dove la guida cita i-pietra dice che nei suoi render sono etichettate «Anfiteatro».
  **Chiude il dubbio 52.**
- **D6**: il file LineeBisma diventa una fonte dopo un controllo con chi l'ha compilato, che
  non è ancora avvenuto: nella guida resta «da controllare».

**27/10/2026 — verifica del lavoro sulle foto del file.** Dieci copie erano ancora coricate:
raddrizzate e rilette. Riscritte le voci 59, 60, 61, 63, 64, 65, 66, 67 e 69; nuove le voci
70-73; aggiornata la 53 (i-pietra al 21/10: 24 linee su 24).

**27/10/2026 — seconda verifica (fonti, privacy, coerenza).** Corrette le voci 59, 60, 61,
64, 65, 67, 70 e 72: gli elementi neri di 46 e 53 sono «in calza nera», non «fettucce nere»
(di nero si vede solo la calza, e dalle calze escono anelli lilla e giallo-verde); il
cavalletto d'autunno della 46 ha forse tre pali; la fettuccia Gibbon della 60 «passa
accanto» ai moschettoni, e se sia una sola non si vede; la sosta con il tronco sta sulle due
righe con scatti diversi, non con le stesse foto; le «piastrine» del file restano fra
virgolette. Nuova la voce 74 (la seconda linea a festoni della 113). Ogni Stato dice che
cosa c'era prima.

**27/10/2026 — le foto del file LineeBisma.** Le 31 fotografie di `LineeBisma.xlsx` (Drive
del gruppo, 20/10/2026) sono state lette una per una, con ingrandimenti, in
`lavorazione/foto_linee/<id>/LETTURA.md`, rilette lo stesso giorno sulle copie raddrizzate, e
confrontate con le parole del file. Ne nascono le voci **59-74**, nella sezione «Aperti dal
file LineeBisma e dalle sue foto». Nessuna chiude un dubbio della 53 m: la sola foto di
quella linea è di una terza uscita, in autunno, e mostra due pali di legno con brache
avvolte, forse un cavalletto `[DA CONFERMARE]`.

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
- Al **21 ottobre 2026** — export di i-pietra del 21/10 e lotto 31
  (`data/catalog/riscrittura/31-highline.md`, applicato il 21/10), letti il 27/10/2026 — il
  catalogo contiene **tutte e 24** le linee. La 20 m e la 108 m dell'Anfiteatro risultano
  create il **21/08/2026** (campo `createdAt`), il giorno dopo i render. Copertura: **24 su 24**.

Fra il 5 e il 20 agosto il catalogo è stato ampliato, oppure i render leggono i dati vivi
invece della cache. Vale sempre il dato più recente, stampato **con la sua data**: fino al
27/10 il manuale stampava 22 su 24 al 20/08; dal 27/10 stampa 24 su 24 al 21/10, con la
storia. I render del 20/08 restano le figure del catalogo e mostrano 22 linee: la didascalia
del render dell'Anfiteatro dice che la 20 m e la 108 m sono entrate in i-pietra dopo.
Dubbio 53, chiuso e aggiornato. Dal confronto fra le due fonti era nato il dubbio 52, chiuso
il 27/10/2026 dalla decisione D4.

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
| 1 | intro | Lunghezza effettiva della campata | Dato di testata | mai pronunciata | **riaperto** — i-pietra e locandina danno 53 m, ma l'utente rimisurerà sui punti. Nome di lavoro: «la 50» (dal 27/10/2026 nel titolo «GAS-OH», voce 45). **27/10/2026**: nessuna delle fonti nuove è una misura. SlackMap dà 52,84 m, ma è la lunghezza del segmento disegnato (`isMeasured: false`). La linea 3D di i-pietra dà 46,7 m, e i-pietra stesso stampa la lunghezza di catalogo (`31-highline.md:11`). Fra le due posizioni del telefono ci sono 51,4 m (voce 3). Resta la misura sui punti |
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
| 13 | A | Cos'è il «**Mighty Lock**», «quello quadratino» | Nome commerciale da identificare | `[IMG_1351 @ 0:19-0:28]` | aperto, **con una pista** — il nome non è storpiato: c'è un **anello quadrato MightyLock nella lista della cernita del gruppo** (09/10/2026), di Balance Community, che il produttore descrive come anello di forma quadrata. È coerente con «quello quadratino», ma che sia il pezzo usato il 16/05 e come lavorasse nel backup lo deve dire chi c'era |
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
| 45 | intro | **Titolo definitivo del manuale.** «La 50» collide con la **50 M del Settore Giallo**, che esiste davvero | Un lettore potrebbe attrezzare la linea sbagliata: è l'ambiguità più pericolosa del documento | locandina | ✅ **chiuso il 27/10/2026 dalla decisione dell'utente D3**: nel titolo la linea si chiama **«GAS-OH»**, il nome che ha su SlackMap (`nym-s4g`); «la 50» resta il soprannome del gruppo e compare nell'occhiello della scheda; resta la nota N3 sulla 50 m del Settore Giallo. Fino al 27/10: aperto — «la 50, settore Anfiteatro», mai «la 50» da sola. Prima della decisione, **27/10/2026**: su SlackMap la linea si chiama **«GAS-OH»** (`nym-s4g`, 52,84 m). i-pietra l'ha ripreso da SlackMap (lotto 31, applicato il 21/10: «Gas-oh», con «detta la 50» come soprannome), quindi non è una seconda fonte. Il nome compare anche in una riunione del gruppo di ottobre. Un nome proprio scioglierebbe la collisione con la 50 m del Settore Giallo, che su SlackMap non ha nome. La scelta del titolo resta del gruppo |
| 46 | — | Cos'è la **«Bifida»** `[IMG_1373 @ 0:24]`: non compare sulla locandina | Capire a cosa si riferisce l'aneddoto | locandina | aperto |
| 47 | — | **Materiale iCloud** acquisito: 19 foto + 14 video (1 min 57 s), 16/05/2026 | Immagini di apertura e prova del montaggio concluso | `foto/`, `video_icloud/` | ✅ esaminato. Le foto 17:08-17:14 mostrano **la linea montata e camminata**, oltre 1 h 30 dopo l'ultimo video di montaggio |
| 48 | — | I video nuovi contengono parlato tecnico? | Speranza di colmare i buchi dell'audio | `video_icloud/` | ✅ **no.** Trascritti tutti e 14: 11 sono Live Photo da 1-3 s; `IMG_1408` (0:49) dice solo «Olé, olé, olé», `IMG_1411` e `IMG_1417` sono muti. Valgono come **immagini**, non come fonte parlata |
| 49 | intro | **La giornata prosegue fino alle 17:14**, ma fra 15:38 e 17:08 non c'è nulla: manca la documentazione di tensionamento finale e primi passaggi | Il manuale deve dichiarare il buco | metadati | aperto |
| 50 | E | **C'è un A-frame** — due pali di legno con fettucce — mai nominato in nessuna trascrizione | Elemento strutturale del lato tensione: altezza, materiale e ancoraggio a terra sono tutti ignoti | `IMG_1396`, `IMG_1416` | **parziale** — con `IMG_1416` (utente, 20/08/2026) l'A-frame ha una sezione nel manuale. Si vede che sta **sul lato dell'ancoraggio main**, che i piedi **appoggiano sulla roccia** e che attorno al piede di un palo ci sono **giri di filo metallico** che proseguono orizzontali. Restano aperti: altezza, diametro del legno, legatura in testa, di quanto solleva la linea, e **se quel filo tenga il palo o sia un recinto preesistente**. **27/10/2026**, dalle immagini (`IMG_1396`, `IMG_1416`):<br>• c'è filo metallico al piede di **tutti e due i pali**, non di uno solo: 2-3 giri a quello di sinistra, almeno uno, in parte coperto dalla corda verde, a quello di destra. Da un palo all'altro corrono fili orizzontali;<br>• in testa ci sono un cordino marrone annodato sotto l'incrocio, una fettuccia blu ad anse, una corda verde lime e la braca lilla;<br>• la linea arriva sul fianco esterno del palo di sinistra, visto dall'ancoraggio, poco sotto l'incrocio;<br>• dall'A-frame passano anche le corde rosa della sosta backup.<br>Che il filo leghi i piedi è compatibile, ma non dimostrato. Altezza e diametro non si ricavano: nelle foto manca un oggetto di misura nota |
| 51 | — | Il **nastro della linea appare bianco/crema** in `IMG_1401`, con un secondo nastro chiaro parallelo (backup?) | Chiude i dubbi 22 e 23 se confermato | `foto/IMG_1401.JPG` | aperto |
| 52 | intro | **I due cataloghi non concordano sul nome del settore.** i-pietra etichetta «Anfiteatro» anche le tre linee che la locandina mette sotto **Anfite-altro** (22, 30, 135 m). Qual è il nome che usate voi? | Stesso rischio del dubbio 45: chi cerca una linea partendo dall'app e chi parte dalla locandina finisce in due settori diversi | render 3D i-pietra, forniti dall'utente il 20/08/2026 | ✅ **chiuso il 27/10/2026 dalla decisione dell'utente D4**: il manuale usa **«Anfite-altro»**, come la locandina, e dove cita i-pietra dice che nei suoi render le tre linee sono etichettate «Anfiteatro». Prima: **confermato a immagine** — in `fonti/render_ipietra/anfite-altro.png` (oggi `.jpg`) le tre linee portano l'etichetta «Anfiteatro»; restava da decidere quale nome usasse il manuale. Nota: dall'export del 21/10 i-pietra ha per queste tre linee anche un campo area «anfite-altro», ma lo ha preso dalla bozza della guida dell'8/10 (lotto 31, fonti): non è una seconda fonte. Nel catalogo restano nel settore `anfiteatro` |
| 53 | intro | **La copertura di i-pietra è cambiata fra le letture.** Il 19/08 lo snapshot del 5 agosto dava 12 linee su 24, senza i settori Despedida e Settore Giallo; il 20/08 i render ne mostrano 22 su 24; l'export del 21/10 ne contiene 24 | Il numero finisce stampato nel capitolo sulle linee | snapshot 05/08/2026 + render 3D 20/08/2026 + export i-pietra e lotto 31 del 21/10/2026 | ✅ **chiuso** — vale il dato più recente, con la data. **Aggiornato il 27/10/2026**: al **21/10/2026** le linee sono **24 su 24**; la 20 m e la 108 m dell'Anfiteatro risultano create in i-pietra il 21/08/2026 (`createdAt`), il giorno dopo i render. In `dati/linee.py` hanno ora `in_ipietra` vero e restano fuori da `sul_render`: la guida stampa 24 al 21/10, la storia (12 al 05/08, 22 al 20/08) e, nella didascalia del render dell'Anfiteatro, che le due linee sono entrate dopo. Prima: vale il dato del 20/08, **22 su 24**. ⚠ Non era una lettura sbagliata: lo snapshot del 5 agosto quei settori non li conteneva proprio |
| 54 | — | **Nello sfondo di `IMG_1416` e `IMG_1396` corre una linea tesa con, sotto, una seconda linea chiara appesa a festoni.** Non si capisce se sia la campata della 53 m vista di scorcio o un'altra linea dello spot | Se fosse un'altra linea, due fotografie del capitolo della 53 m ne mostrerebbero una diversa senza dirlo | `IMG_1416`, `IMG_1396` | **chiarito a immagine il 27/10/2026: è un'altra linea.** In `IMG_1396`, `IMG_1407` e `IMG_1416` la 53 m si vede a parte, dall'A-frame alla sommità del pilastro opposto, con una persona sopra. La coppia di linee (tesa e a festoni) parte dallo stesso pilastro e va verso sinistra nell'immagine; la direzione non si ricava da una foto sola. Quale linea sia, e quindi la voce 55, resta da chiedere |
| 55 | E | **Che cos'è la seconda linea appesa a festoni** sotto quella tesa: backup, tagline lasciata in posa, o altro | Chiude in parte i dubbi 23 e 24 | `IMG_1416`, `IMG_1396` | aperto |
| 56 | A, D, E, F | **Quale lato è quale sulla 53 m.** La guida è organizzata per lati: *lato tensione* = dove stanno sosta main e sosta backup, dove si tensiona e dove sta l'A-frame; *lato statico* = la sosta su tre punti con le placchette e la linea vita. È **ricostruito** dall'ordine delle operazioni (sezione D «sosta sull'altro lato, su 3 punti»; il blocco del backup che prende sia main sia backup) e dalla risposta del 20/08 sull'A-frame, non dichiarato | Un lato scambiato in una guida di montaggio manda a costruire la sosta sbagliata dalla parte sbagliata | NOTE_RIGGING A-F, risposta utente 20/08/2026 | ✅ **chiuso il 27/10/2026.** L'utente: «il lato di tensione è quello della parte sopra Cocoa». Alla domanda di verifica ha confermato che Cocoa è il settore di falesia che sta al main: OSM `node/11925326320`; theCrag area `7751514930`; in i-pietra «Cocoa» (falesia.it lo chiama «Cocoa - Anfiteatro Alto»). È il terrazzo sopra la Pincelli-Brianti, 10 m sotto il bordo della sommità. Il punto OSM di Cocoa sta a 10,9 m dal main e a 46,5 m dall'altro capo; il main sta a nord-nord-est dell'altro capo. **Tensione al main** (44.419869, 10.412353): sosta main, sosta backup, A-frame. **Statico all'altro capo** (44.419453, 10.412072): la sosta su tre punti. La ricostruzione era giusta, e anche il GPS delle riprese è coerente. `IMG_1373`-`1375` sono a 6-8 m dall'altro capo, i video del tensionamento `IMG_1378`-`1395` a 5-13 m dal main. Le posizioni dei video sono registrate con quattro decimali, cioè su una griglia di circa 11 × 8 m: le distanze valgono a meno di qualche metro, ma i due capi distano 51 m. Fa eccezione `IMG_1384`, con un'accuratezza di 63,8 m: inutilizzabile. Vedi anche la voce 58 |
| 57 | — | **Le foto del 22/08 sulla cresta (IMG_3308-3322)**: quali sono della Despedida e quali del Settore Giallo; e se la roccia sullo sfondo di `IMG_3311` è davvero quella della **Despedida 165 m** («dovrebbe essere», utente 08/10/2026) | Una vista del settore entra nella guida solo con la linea giusta in didascalia | `IMG_3308`-`IMG_3322` | aperto — **da chiedere a chi ha accompagnato il sopralluogo**; possibile fonte anche i video delle linee montate pubblicati online |
| 58 | A–F | **Il GPS dei video sposta un'attribuzione di fase.** `IMG_1376` sta in `NOTE_RIGGING.md` nella fase D, «sosta sull'altro lato», ma è stato girato **al main**: 5,4 m, accuratezza 13,3 m. Le fasi A e B (`IMG_1349`, `1351`, `1363`, `1366`, `1367`) sono girate al main, a 5-15 m; `IMG_1368` sta a metà strada (29 m dal main, 39 m dall'altro capo) e non si attribuisce a nessuno dei due capi; `IMG_1369` (fase C) sta vicino all'altro capo. Le posizioni dei video sono su una griglia di circa 11 × 8 m (quattro decimali). Alcuni GPS non sono usabili: `IMG_1384` (63,8 m), `IMG_1370` (69,8 m), `IMG_1377` (186 m), `IMG_1350` (36,5 m) | Una manovra attribuita al lato sbagliato finisce nella sosta sbagliata | metadati QuickTime `com.apple.quicktime.location` dei video, letti il 27/10/2026 | aperto — rivedere la fase D in `NOTE_RIGGING.md` e chiedere che cosa si faceva al main in `IMG_1376` |

## Aperti dal file LineeBisma e dalle sue foto (27/10/2026)

Le fotografie stanno in `lavorazione/foto_linee/<id>/`, con `ORIGINE.md` (scheda, cella,
colonna del file) e `LETTURA.md` (che cosa si vede, che cosa manca), rilette il 27/10/2026
sulle copie raddrizzate. «Vicino» e «lontano» sono le colonne del file, non tensione e
statico. Tutto ciò che il file scrive è segnato dal file stesso «da controllare». Nessuna
foto ha EXIF. Le voci vanno chieste **a chi ha compilato il file** e a chi era sul posto.
Le correzioni del 27/10 sono annotate nello Stato di ogni voce, con quello che c'era prima.

| # | Linea | Cosa manca | Perché serve | Fonte del dubbio | Stato |
|---|---|---|---|---|---|
| 59 | 108 / 113 | **Di quale linea è la sosta con il tronco.** Foto diverse della stessa sosta stanno sia sulla riga della 108 (D7, U7) sia su quella della 113 (D8): un **tronco con la corteccia**, tagliato netto a un'estremità, coperto in parte da un'**imbottitura bianca** con sotto un tessuto rosso e legato con cordino viola; due slinghe verdi che lo scavalcano; una slinga su moschettone a ghiera e **placchetta con dado**; calza grigia e rossa; braca viola. **Subito accanto alla sosta, sul bordo, c'è un albero** (`108_01`, `113_05`). Il file chiama il lato lontano della 113 «Bisma standard senza cavalletto + tronco» e descrive quello della 108 «con alberi e uno spit»: con un tronco e un albero nelle foto, **nessuna delle due descrizioni è esclusa**. `108_03` ha quasi la stessa inquadratura di `113_07`; `108_04` (autunno) sembra la stessa sosta in un'altra stagione | Una sosta attribuita alla linea sbagliata manda a cercarla sul capo sbagliato | `anfiteatro-108_01`-`_04`; `anfiteatro-113_05`, `_06`, `_07` | aperto — da chiedere a chi ha compilato il file. **27/10/2026**, rilettura sulle copie dritte: prima la voce diceva «tronco chiaro scortecciato», «moschettone su anello fisso», terrazza «senza alberi» e concludeva che le foto «corrispondono al lato lontano della 113»; le foto lo smentiscono. Poi, nella seconda verifica: la voce diceva «le stesse foto» sulle due righe, ma sono scatti diversi (gli originali hanno md5 tutti diversi) |
| 60 | 46, 97, 108, 113, 60, 70 (e il «vicino» della 53) | **Il lato di tensione di ogni linea fotografata.** Nessuna foto lo mostra con certezza. Indizi, non prove: sul lato lontano della 46 un **elemento metallico con il nastro bianco avvolto**, da cui parte un elemento in calza nera (`46_03`, `_04`; un weblock? voce 65), e dietro le brache due elementi verticali, uno di legno (voce 65); sul lato vicino di 46 e 53 due elementi in calza nera, da cui escono anelli lilla e giallo-verde, che convergono su connettori metallici con un anello arancione (`46_01`, `53_01`; voce 64); in `53_01` **due pali di legno con brache avvolte**, forse un cavalletto: sulla 53 m l'A-frame sta sul lato tensione (voce 56), ma che quei pali siano l'A-frame, e che il «vicino» del file sia il main, la foto non lo dice; un cavalletto sul lato vicino di 46, 113, 70 e sul lato lontano di 70 | La guida è organizzata per lati: senza questo dato le foto restano foto, non documentazione degli ancoraggi (vedi `lavorazione/ancoraggi/LEGGIMI.md`) | tutte le cartelle | aperto — lo deve dichiarare chi c'era. **27/10/2026**: prima «un dispositivo bianco/argento della forma di un weblock» e fettucce che convergono «su grillo e softshackle»; aggiunti i pali di `53_01` e gli elementi verticali di `46_03`/`_04`. Poi, nella seconda verifica: «due fettucce nere con calza» e «elementi verticali di legno» erano più di quanto si veda |
| 61 | tutte | **Data e autore di ogni foto.** Excel ha tolto gli EXIF. Si legge solo la stagione: il cavalletto della 113 compare in tre configurazioni (due pali tondi con corda verde d'estate, **tre pali** con fascia viola/rosa d'autunno, due assi squadrate di notte), quello della 46 in due (corda color canapa d'autunno, con **forse tre pali**: sopra l'incrocio di `46_01` ci sono due teste tagliate più il palo in primo piano; **fettuccia azzurra** d'estate, con due pali, da cui pende una corda rosa): sono almeno tre e due uscite | Senza data non si sa quale montaggio sia e se il materiale sia ancora quello | `113_01`-`_04`, `_08`; `46_01`, `_05` | aperto — da chiedere a chi ha compilato il file. **27/10/2026**: prima «pali tondi con fascia viola» d'autunno per la 113 (sono tre pali) e «corda rosa» d'estate per la legatura della 46 (è una fettuccia azzurra). Poi, nella seconda verifica: la guida stampava «cavalletto di due pali» anche per la 46 d'autunno |
| 62 | 97 | **La «91» del file è la 97 m del registro?** Le sue righe (schema, note, foto) sono state messe sulla 97 per posizione: Anfiteatro 46, 53, 91, 108, 113 nel file contro 46, 53, 97, 108, 113 nel registro | Un dato attribuito alla linea sbagliata | `LineeBisma.xlsx`, scheda «Elenco» | aperto — anche nel Foglio «Da chiarire» |
| 63 | 108 | **Dove sono «alberi e uno spit» del lato lontano.** Il file descrive il montaggio («Montaggio con alberi e uno spit. Sosta molto lunga, portare corde lunghe anche per fare un deviatore»). Le foto sulla sua riga mostrano la sosta con il tronco (voce 59) con **un albero accanto** e corde e brache che escono dall'inquadratura verso l'interno: **non smentiscono il file**, ma non mostrano né lo spit né una braca legata all'albero. La calza grigia e rossa diretta verso l'interno potrebbe essere la «sosta molto lunga»: è un'ipotesi | La descrizione è l'unico dato sul lato lontano della 108 e le foto non bastano a riscontrarla | `anfiteatro-108/LETTURA.md` | aperto. **27/10/2026**: prima la voce diceva che «nessuna foto sulla sua riga mostra alberi» e che, se la sosta con il tronco fosse della 113, della 108 non resterebbe nessuna foto: la prima affermazione è falsa |
| 64 | 46, 53 | **Che cosa sono i due elementi in calza nera** che convergono su connettori metallici con un **anello arancione** e un cordino azzurro (`46_01`, `53_01`), e che cos'è l'anello. Di nero si vede solo la calza, increspata: dalla bocca delle calze escono **anelli tubolari colorati**, lilla da una e giallo-verde dall'altra (`46_02`; in `53_01` lo stesso), ciascuno su un grillo. Che dentro ci siano fettucce non si vede: un elemento in calza nera su grillo a lira si vede anche nei **bungee** della 53 m del 22/08 (`IMG_3325`), ma è un indizio, non una prova. In `46_02` su uno dei due è infilata una protezione nera con l'etichetta **«SPIDER»**: la marca vale per la protezione, non per ciò che sta dentro la calza. Stesso materiale, stessa stagione (autunno), stesso parcheggio sotto in 46 e 53; in `53_01` ci sono anche due pali di legno con brache avvolte, nella stessa disposizione del cavalletto di `46_01`. Se siano la stessa giornata, o la stessa sosta messa dal file su due righe | Se fossero la stessa sosta, una delle due linee non avrebbe foto del lato vicino | `46_01`, `46_02`, `53_01` | aperto — da chiedere a chi ha compilato il file. **27/10/2026**: prima «fettucce marcate Spider» che convergono «su grillo e softshackle arancione»; aggiunti i pali di `53_01`. Poi, nella seconda verifica: prima «due fettucce nere con calza»; le copie `46_01`, `46_02` e `53_01` sono state rinominate («…elementi-in-calza…») |
| 65 | 46 | **L'elemento metallico del lato lontano**, con il nastro bianco e una fettuccia nera avvolti, da cui parte verso il vuoto un elemento in calza nera (`46_03`, `_04`): un weblock? Marca e modello non leggibili. Se lo fosse, il lato di tensione sarebbe il lontano. Dietro le brache ci sono **due elementi verticali**, uno di legno grigio e screpolato e uno sottile e bianco con un nastro grigio, di materiale non leggibile: se fossero un cavalletto, il lato non sarebbe «senza cavalletto», come lo chiama il file | Decide la voce 60 per la 46 | `46_03`, `46_04` | aperto. **27/10/2026**: prima «dispositivo bianco/argento», e senza gli elementi verticali |
| 66 | 70 | **Un cavalletto a tutti e due i capi?** Il lato vicino (`70_01`, estate) mostra un cavalletto di due pali, il lato lontano (`70_02`, autunno) uno di **tre pali**; `70_02` è la stessa scena di `60_01`. Sul lato lontano: a che cosa è ancorata la corda chiara doppia su cui si annodano le slinghe verdi (`70_03`), e su che cosa è chiusa la protezione tubolare bianca che gira attorno a un masso sul bordo e con un capo arriva alla base di un **alberello** (`70_04`): il masso, l'alberello o tutti e due | Un capo senza punti fissi cambia tutto il metodo | `despedida-70/LETTURA.md` | aperto. **27/10/2026**: prima «cavalletto di due pali» anche sul lato lontano e calza bianca «attorno a un masso», senza l'alberello |
| 67 | 60 | **Il lato lontano: alberi?** Una fettuccia nera **Gibbon** (una sola o più di una: non si vede) passa accanto a tre moschettoni a ghiera sul bordo e prosegue oltre il bordo dell'immagine (`60_02`, `_03`), e gira attorno alla base di un **albero in piedi** (`60_04`, `_06`); una corda arancione è annodata a quell'albero (`60_04`). Accanto a un tronco sottile in piedi ci sono un tronco inclinato e due o tre **bastoni sottili incrociati** (`60_02`, `_03`): un cavalletto? Che funzione abbiano fettuccia e corde, e se la Gibbon sia una sola. **Del lato vicino non c'è nessuna foto.** L'highliner nella nebbia di `60_01` può essere sulla linea della 70: è la stessa scena di `70_02` | Unico dato sulla 60 m: il file ha solo la tipologia | `despedida-60_01`-`_06` | aperto. **27/10/2026**: la `60_04`, letta coricata, sembrava un «tronco grosso orizzontale»: è un albero in piedi; prima «due pali sottili incrociati». Rinominate le copie 02, 03, 04 e 06: i numeri restano. Poi, nella seconda verifica: prima la Gibbon «arriva a» tre moschettoni, come una fettuccia sola; la guida stampa ora «una o più» `[DA CONFERMARE]`, e fra le cose da confermare della 60 c'è se la linea della miniatura sia la 60 o la 70 |
| 68 | 113 (o 108) | **Le etichette alla sosta con il tronco.** Sulla calza di una slinga verde una scritta scura (sembra «2 t», non leggibile con certezza); sulla braca viola un'etichetta azzurra cucita, illeggibile. Vanno fotografate distese, come per il dubbio 37 | La portata delle brache è il dato più pericoloso da sbagliare | `113_05`, `113_06` | aperto — foto da fare sul campo |
| 69 | 97 | **Quale linea della foto del lato vicino è la 97.** In `97_03` (prima `97_01`) entrano da sinistra, da fuori inquadratura, due linee, rosa e bianca, con un highliner ciascuna; una **terza linea**, chiara con tratti rosa, parte da un **ancoraggio in basso a destra**. Nel file la foto è ritagliata e mostra solo quell'ancoraggio con la linea che ne parte: **per il ritaglio del file, la 97 è la terza linea**. Da confermare, insieme all'ancoraggio, che in controluce non si legge. Sul lato lontano (`97_01`) un moschettone su un elemento metallico nella roccia, forse una placchetta: l'ancoraggio può essere sugli alberi, sulla roccia o su tutti e due | Una linea scambiata manda a cercare l'ancoraggio sbagliato | `anfiteatro-97_03`; ritaglio della cella nel file | aperto. **27/10/2026**: prima la voce chiedeva quale «delle due linee parallele» fosse la 97 e diceva che partivano «dalla stessa cima»; la foto, che ha un volto riconoscibile, è stata rinumerata da 01 a 03, e la miniatura della guida è ora `97_01` (brache fra gli alberi), che non mostra le linee |
| 70 | 53 e tutte le soste «Bisma standard» | **Placchette: in loco o da portare?** Il file, nella scheda «Sosta Bisma Standard», mette in loco «Spit e Dadi» (B6) e da portare «3 piastrine da 10 mm» (B7). La scheda della 53 m elenca 3 placchette su bullone all'ancoraggio statico, viste il 16/05 e il 22/08; il 22/08, più in basso, c'era un bullone senza placchetta (voce 28). Se le «piastrine» del file siano le placchette (voce 72), e se restino sul posto, nessuna fonte lo dice | Arrivare all'ancoraggio senza placchette | `LineeBisma.xlsx`, scheda «Sosta Bisma Standard»; `IMG_3331`; `build/scheda_53.py` | aperto. **27/10/2026**: la scheda della 53 m le dava fisse («valgono per ogni montaggio»), senza fonte; ora stampa «in loco o da portare `[DA CONFERMARE]`». Poi, nella seconda verifica: la voce dava le «piastrine» per placchette; le placchette entrano, con `[DA CONFERMARE]`, anche nella lista «Prima di uscire» della parte 2 e nella tabella del materiale della 53 m; nella scheda da campo la voce è PRIORITARIO |
| 71 | «Bisma standard» | **Gli omega elencati due volte.** Il file li elenca in «Materiale da portare» («1 omega fra le slinghe», «1 omega per sliding x»; B9-B10) e di nuovo in «Sosta Main» («Omega fra slinghe», «Omega per sliding x»; B14-B15). Sono gli stessi pezzi o pezzi in più? Il Foglio del gruppo li conta una volta sola | Se sono pezzi distinti, il conto del materiale ne perde due per lato | `LineeBisma.xlsx`, scheda «Sosta Bisma Standard» | aperto — da chiedere a chi ha compilato il file |
| 72 | «Bisma standard» | **Le parole del file.** A quali pezzi corrispondono «spit», «piastrine», «delta», «omega», «slinga», «sliding x» e «BFK»; e che cos'è «Bisma standard senza cavalletto», che non ha una scheda sua: la stessa senza il blocco «Cavalletto»? E lo schema «Bisma standard» delle righe è la scheda «Sosta Bisma Standard»? Lo suggerisce solo il nome | Un'equivalenza dedotta («omega = grillo») era stata stampata ed è stata tolta: finché non c'è risposta, la scheda del file resta con le sue parole | `LineeBisma.xlsx`, schede «Sosta Bisma Standard» ed «Elenco» | aperto — da chiedere a chi ha compilato il file |
| 73 | 46, 53, 97, 108, 113 | **Che cosa misura «Schetchy».** Il file ha due colonne, «Schetchy» e «Schetchy2», con valori «No» e da 2 a 5. Le intestazioni non nominano il lato: che valgano per il «vicino» e il «lontano» lo dice solo la posizione delle colonne (lo stesso per «Persone» e «Persone3»). Non è detto che sia una difficoltà: scala e verso sono ignoti | La guida le stampava come «difficoltà»; ora le riporta con il nome del file | `LineeBisma.xlsx`, scheda «Elenco», D3 e G3 | aperto |
| 74 | 113 | **La seconda linea appesa a festoni** sotto la linea, sul lato vicino (`113_01`, `_03`, `_08`): è il backup della linea? Che lo sia è una lettura, come per la linea a festoni sullo sfondo delle foto della 53 m (voce 55) | La guida la stampava come «backup a festoni», un dato che la foto non dà | `113_01`, `113_03`, `113_08` | aperto — da chiedere a chi ha compilato il file. **27/10/2026**, seconda verifica: prima la scheda stampava «la linea con un backup a festoni»; ora «una seconda linea appesa a festoni sotto `[DA CONFERMARE: se sia il backup]`» |

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
