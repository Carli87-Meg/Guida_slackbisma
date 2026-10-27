# Analisi della guida — edizione del 27/10/2026

Rilettura completa della guida (28 pagine), del fascicolo delle schede di rilievo
(24 pagine), dei sorgenti in `build/`, del registro `dati/linee.py` e di `DUBBI.md`.
Obiettivo: capire che cosa manca perché la bozza diventi **la guida ufficiale alle
highline della Pietra**, e proporre una struttura per arrivarci.

**Stato al 27/10/2026, sera:** i passi 2-5 del piano (sezione 7) sono stati eseguiti
nell'edizione 0.4, con le scelte A-E nella forma proposta qui (per la C: i principi generici
sono stati tolti e restano come domande nel capitolo 6 del metodo). Restano il passo 1,
già deciso, e il passo 6: la revisione su Figma e il giro di domande al gruppo.
**Aggiunta della sera:** su richiesta dell'utente le sei linee fotografate hanno la scheda
completa (non più la mezza colonna del punto 3.2), con render, capi SlackMap, foto e
materiale; i nomi SlackMap di tutte le linee sono nel registro (punto 3.3 fatto).

---

## 1. In breve

La guida è onesta, ben disegnata e tecnicamente solida nel modo in cui tratta le
fonti. Il suo limite è un altro: **è ancora scritta dal punto di vista di chi l'ha
costruita, non di chi la userà**. Un lettore che apre il PDF per montare la 46 m
dell'Anfiteatro trova la storia della copertura del catalogo i-pietra, le colonne di un
file Excel, la differenza fra «vicino» e «lontano», e la 46 m sparsa in tre posti (tabella
del settore, scheda fotografata, scheda di rilievo in un altro fascicolo).

Le cinque mosse che la trasformano in una guida ufficiale:

1. **Separare la guida dal cantiere.** Il lettore vede le linee e il metodo; la storia
   delle fonti, i confronti fra cataloghi e le trascrizioni del file del gruppo vanno
   nell'apparato o nei documenti di lavoro.
2. **Una scheda per linea, sempre nello stesso posto**, con un livello di documentazione
   dichiarato (quattro livelli, una legenda, un simbolo), invece di capitoli nati dalle
   fonti («le linee fotografate») e di avvertenze ripetute ad ogni pagina.
3. **Un nome stabile per ogni linea**: codice di settore e numero, nome SlackMap dove
   esiste, lunghezza di catalogo. Oggi «la 50» viene disinnescata tre volte in tre pagine.
4. **Il metodo chiamato con il suo nome**, «l'ancoraggio standard Bisma», ricompattato da
   dieci capitoli a sei, con i principi generici separati da ciò che viene dal gruppo.
5. **Un'architettura dati che regga 24 linee**: oggi la 53 m è un modulo Python a parte;
   la seconda linea documentata richiederebbe di copiarlo.

---

## 2. Che cos'è oggi la guida

| Pagine | Contenuto | Riempimento |
|---|---|---|
| 1–2 | Copertina, indice a due livelli | pieno |
| 3–4 | Lo spot; le linee della Pietra con la panoramica | pieno |
| 5–9 | Un settore per pagina: render i-pietra + tabella delle linee | 5, 7, 8 vuote per un terzo |
| 10 | Frontespizio della parte 2 | vuota per metà |
| 11–18 | Il metodo, dieci capitoli | 16 vuota per due terzi |
| 19 | Frontespizio della parte 3 | vuota per tre quarti |
| 20–23 | Scheda di GAS-OH, 53 m | pieno |
| 24–26 | Le linee fotografate: scheda del file + sei schede | 26 vuota per due terzi |
| 27–28 | Glossario; fonti e avvertenza | pieno |

Che cosa funziona e va tenuto:

- Il **sistema grafico**: testate, pastiglie, blocchi materiale a due colonne, colore per
  settore, rimandi di pagina risolti in più passate, indice che dichiara lo stato di ogni
  parte («completo», «parziale», «1 linea su 24»).
- La **pagina di settore** (render + tabella), disegnata su Figma: è il modulo giusto per
  il catalogo, e l'ordine lungo la cresta è quello che serve sul posto.
- La **regola delle fonti**: ogni dato ha una provenienza, ogni fonte ha una data, nessun
  numero è dedotto. È ciò che rende la guida credibile, e non va annacquato.
- Il **fascicolo di rilievo** separato dalla guida, come deciso su Figma.
- La **scheda di GAS-OH** come forma: testata, dove corre, due ancoraggi con coordinate
  cliccabili, materiale, A-frame, varianti, che cosa manca.

---

## 3. I problemi di coerenza

### 3.1 La guida parla di sé più che delle linee

Il lettore incontra, prima ancora di una linea, il rapporto fra la locandina e i-pietra:

- p. 3, tabella dello spot: «Di cui in i-pietra: 24», «Rigging documentato: 1 — fonte:
  questa guida». Sono dati sulla guida, non sullo spot.
- p. 4, il primo riquadro rosso della guida è «Le due fonti non concordano sui settori»:
  una questione editoriale (Anfite-altro / Anfiteatro), non un rischio per chi monta.
- Ogni pagina di settore porta nell'occhiello «in i-pietra «Rookie»», in didascalia
  «4 linee tracciate sul render, 4 censite sulla locandina», e in tabella la colonna
  «In i-pietra», che dal 21/10 dice «sì» su tutte e 24 le righe: non distingue più nulla.
- La storia 12 → 22 → 24 compare quattro volte (p. 3, 4, 6, 28).

Tutto questo è corretto e va conservato, ma nell'**apparato** («Da dove viene ogni dato»),
in una frase: «I render stampati sono del 20/08/2026 e mostrano 22 linee; la 20 m e la 108 m
dell'Anfiteatro sono entrate nel catalogo il giorno dopo». Nel corpo della guida resta
solo ciò che serve a riconoscere e montare.

### 3.2 La stessa linea sta in tre posti

Per la 46 m dell'Anfiteatro: riga nella tabella del settore (p. 6), scheda fra «le linee
fotografate» (p. 25), scheda di rilievo n. 7 nel fascicolo. Il capitolo «Le linee
fotografate» esiste perché esiste il file LineeBisma: è un capitolo nato da una fonte, non
dall'argomento. La prova è il suo contenuto: la scheda «Sosta Bisma Standard» del file
(p. 24) parla del **metodo**, non delle linee fotografate, ed è stampata lì solo perché
viene dallo stesso file.

Proposta: ogni linea ha **un solo posto**, nel suo settore, e il suo contenuto dipende
dal livello di documentazione:

| Livello | Che cosa si sa | Come appare | Oggi |
|---|---|---|---|
| 0 · censita | settore e lunghezza di catalogo | solo la riga nella tabella del settore | 17 linee |
| 1 · fotografata | foto della linea montata, nessun rilievo | mezza pagina: foto, che cosa si vede, che cosa manca | 6 linee |
| 2 · rilevata | scheda di rilievo compilata sul campo | una pagina: dati, ancoraggi, materiale | nessuna |
| 3 · documentata | riprese, fotogrammi, dubbi chiusi | scheda completa, come GAS-OH | 1 linea |

La legenda sta una volta sola, nella pagina «Come leggere questa guida»; nelle tabelle e
nelle testate compare come pastiglia. Spariscono così le frasi ripetute «le foto non
documentano il montaggio» (oggi a p. 19, 24, 25, 26, 28 e nel fascicolo) e «DA
CONTROLLARE» su ogni scheda. Le 17 linee di livello 0 **non hanno una scheda vuota**:
questa era la scelta fatta su Figma e resta.

### 3.3 I nomi delle linee

Oggi una linea si chiama «settore · lunghezza»; la 53 m ha anche GAS-OH; il soprannome «la
50» viene spiegato a p. 6, p. 8, p. 20 e nella scheda di rilievo 16. SlackMap censisce
tutte e 24 le linee (lettura del 27/10) e almeno due hanno un nome proprio (GAS-OH,
Brifing per la 113 m).

Proposta: un **codice per linea**, settore e numero nell'ordine della cresta
(`RK-1`…`RK-4`, `AN-1`…`AN-7`, `AA-1`…`AA-3`, `SG-1`…`SG-4`, `DE-1`…`DE-6`), il nome
SlackMap dove esiste, la lunghezza di catalogo. La testata della scheda di GAS-OH, con la
pastiglia «AN» e il «53 m», è già quasi questo. Con il codice, la nota su «la 50» si scrive
una volta nel glossario («la 50» → AN-4, GAS-OH; da non confondere con SG-3, 50 m).

I nomi SlackMap vanno **raccolti** (fonte già consultata in sola lettura, non ancora
trascritta nel registro): un compito di dati, non di impaginazione.

### 3.4 Che cosa manca davvero a una guida «ufficiale»

Le cose che un rigger esterno cerca per prime non dipendono dai video, e nessun documento
del progetto le raccoglie in forma di domanda:

- **accesso e avvicinamento** a ciascun settore, parcheggio, tempi;
- **regole dello spot**: area protetta, divieti stagionali per nidificazione, accordi con
  il gestore, permarig sì o no, cosa fare delle linee di notte;
- **chi è il gruppo** e come lo si contatta (nel rispetto del repository pubblico);
- **emergenze**: numeri, punto di raccolta, rifugio;
- per ogni linea: **altezza dal suolo / esposizione**, tipologia (il file usa Beginner,
  Freestyle, Highline), A-frame necessario o no, chi la monta di solito.

Oggi queste voci sono due righe «[DA CONFERMARE]» a p. 3 e i dubbi 4 e 5. Proposta: una
pagina «Lo spot» con queste sezioni **presenti e dichiaratamente vuote**, e un foglio nel
fascicolo di rilievo, «Rilievo dello spot», con le domande da fare al gruppo. È lo stesso
meccanismo delle schede di linea applicato allo spot. La guida resta sincera: dice che cosa
dovrebbe esserci e che non c'è ancora.

Manca anche una **planimetria vera**. La panoramica i-pietra serve a riconoscere la parete,
non a muoversi: una mappa (OpenStreetMap, fonte dichiarata) con i cinque settori, i
sentieri di accesso e, man mano che arrivano dai rilievi, le coordinate degli ancoraggi.
Oggi le coordinate note sono due, entrambe di GAS-OH.

### 3.5 Il metodo

Dieci capitoli in otto pagine; tre sono di poche righe («Portare la linea», quattro righe
e un rimando; «Lo smontaggio», due righe; «Una linea, due lati» che ripete la sequenza).
Nel frattempo il nome che il gruppo dà al proprio metodo, **«Ancoraggio standard Bisma»**,
compare solo a p. 24, dentro il capitolo delle foto.

Proposta: sei capitoli, e un titolo che dica di chi è il metodo.

| Oggi (10) | Proposta (6) |
|---|---|
| 1 Una linea, due lati · 3 La sequenza · 7 Portare la linea · 10 Smontaggio | **1 Lo schema**: due lati, la sequenza in undici passi, tagline e linea vita, smontaggio dichiarato mancante come dodicesimo passo |
| 2 Prima di uscire: il materiale | **2 Il materiale**, con accanto lo schema «Ancoraggio standard Bisma» del file (finché non è controllato: «proposta del gruppo, da controllare»), che oggi sta a p. 24 |
| 4 Gli ancoraggi su roccia | **3 I punti su roccia** |
| 5 Le soste · 6 Instradamento della slinga | **4 Le due soste del lato tensione**: main, backup, instradamento, portata delle brache |
| 8 Il lato tensione · 9 L'A-frame | **5 Tensione, blocco del backup, anti-slip, A-frame** |
| — | **6 Che cosa il metodo non copre ancora**: una lista sola di ciò che è [DA CONFERMARE] nel metodo, al posto delle liste «Ancora da rilevare» sparse nei capitoli |

Tre punti di merito, oltre alla forma:

- **Regola numero uno, zona grigia.** Alcuni passaggi del metodo sono conoscenza generica,
  non del gruppo: «arenaria, meno tenace del calcare» (p. 13), la checklist «Controlli prima
  di caricare un punto» (che il testo stesso dice «discende dal tipo di ancoraggio»), il
  riquadro su spit, tasselli e resinati, la spiegazione di che cosa fa l'A-frame. Sono
  ragionevoli e probabilmente giusti, ma per la regola del progetto vanno o attribuiti
  esplicitamente («controlli generali, non la checklist del gruppo: [DA CONFERMARE]», come
  già fa la riga sotto la checklist) o sostituiti dalla versione del gruppo quando arriva.
  Da decidere insieme: tenerli con l'etichetta, o toglierli.
- **Il riquadro «Due avvertenze da chiarire»** (p. 12) dice al lettore che «un componente
  può cadere» e «un'operazione andrebbe fatta dopo», senza dire quali. Per chi monta è
  un'informazione inutilizzabile: resti in `DUBBI.md` finché non si sa, ed entri nella
  guida solo con il suo oggetto.
- **La carrucola bloccante** è elencata a p. 11 sotto «Per: l'ancoraggio». È stata vista
  sull'ancoraggio (IMG_1371), ma la sua funzione non è detta da nessuna fonte: la riga
  andrebbe formulata come osservazione, non come ruolo.

### 3.6 La scheda di GAS-OH

È la scheda modello e regge bene, con quattro correzioni:

- **I dati di testata stanno in fondo.** La tabella «Lunghezza, dislivello, nastro,
  montaggi documentati» è a p. 23, dopo l'A-frame. Nel modello Sillschlucht la riga delle
  pastiglie viene subito dopo l'introduzione. Ordine proposto: testata → pastiglie dei dati
  → dove corre → i due ancoraggi → materiale → A-frame → foto in opera → varianti → che cosa
  manca.
- **«Quale lato è quale»** è detto tre volte (sotto il render a p. 20, nelle etichette T/S,
  nel riquadro a p. 23). Una volta, accanto agli ancoraggi.
- **La tabella del materiale** (p. 21) ha 24 marcature [DA CONF.] su 19 righe: il lettore
  non distingue più ciò che è noto da ciò che manca. Proposta: le misure mancanti sono
  **celle vuote**, con una nota sotto la tabella («le misure vuote sono da rilevare sul
  pezzo»), come chiede `CLAUDE.md` («un campo vuoto dichiarato»). Il marcatore rosso resta
  per i dati **incerti** (il «Mighty Lock», la carrucola «sull'ancoraggio»), non per quelli
  semplicemente assenti. Lo stesso vale per il blocco «Ancora da rilevare» dell'A-frame, dove
  ogni voce ripete «[DA CONF.]» sotto un titolo che lo dice già.
- **Il lessico dei lati.** La scheda usa T/S (tensione/statico), le schede di rilievo usano
  lato A/B, il metodo «lato tensione / lato statico», i blocchi «ancoraggio di tensione» che
  contiene «sosta main» e «sosta backup». La gerarchia è giusta (linea → lato → ancoraggio →
  soste → punti) ma non è mai dichiarata: una riga nel glossario la fissa, e A/B nelle schede
  di rilievo va spiegato («finché non si sa quale lato è quello di tensione»).

### 3.7 Le schede del file LineeBisma (p. 25–26)

Sono trascrizioni di una fonte: «Lato «vicino» (in miniatura) · nel file: schema «Bisma
standard» · nelle foto: … · Schetchy (dal file) No / 4 · persone «No problem» / «2 persone in
calata»». Un lettore esterno non sa che cosa sia il file né che cosa sia Schetchy, e la
guida glielo spiega con un riquadro rosso di sette righe. Questo materiale è prezioso **per
chi va a rilevare**, non per chi legge: il suo posto è la scheda di rilievo della linea,
come suggerimento precompilato («il file del gruppo dice: …, da controllare»). Nella guida
restano, per ciascuna delle sei linee, la fotografia e tre righe su ciò che si vede.

### 3.8 L'apparato

- L'**avvertenza** che conta («Nessuna parte di questo documento va usata come riferimento
  operativo finché…») è l'ultimo paragrafo dell'ultima pagina, dopo una tabella di tredici
  fonti. Va anche **davanti**, nella pagina «Come leggere questa guida».
- La guida non dice **di chi è**: «Bismaliners» non compare in nessuna pagina (solo come
  autore del PDF del fascicolo). Una guida ufficiale ha un proprietario, un numero di
  edizione, una data e un modo per segnalare errori. Proposta: in copertina «a cura dei
  Bismaliners · edizione 0.3 · ottobre 2026»; in chiusura un colophon con le edizioni
  (poche righe, non la cronologia dei dubbi) e il canale per le correzioni, da scegliere
  tenendo conto che il repository è pubblico.
- Il **glossario** è buono; vi entrano la gerarchia dei termini (3.6), il codice delle
  linee (3.3) e la nota su «la 50».
- Un **protocollo di rilievo** di una pagina: che cosa misurare e fotografare quando si
  monta una linea, ricavato da ciò che è mancato per la 53 m (inquadratura d'insieme dei
  punti, etichette delle brache distese, GPS dei due capi, dettaglio dei bulloni, A-frame
  con un riferimento di misura). È la lezione più concreta del progetto, e oggi non è
  scritta da nessuna parte in forma di istruzione.

### 3.9 Grafica e colori

- **Due sistemi di colore sulla stessa tavolozza.** I settori usano `LC[6] [4] [2] [1] [7]`;
  il metodo usa `LC[1]` per gli ancoraggi, `LC[7]` per le soste e come colore della parte
  2, `LC[3]` per la tensione. Risultato: le pagine «Gli ancoraggi su roccia» hanno il rosso
  dell'Anfite-altro, il frontespizio della parte 2 ha l'azzurro della Despedida (p. 9 e
  p. 10 sono affiancate con lo stesso colore), e nella scheda di GAS-OH il blocco
  dell'ancoraggio statico è rosso Anfite-altro dentro una scheda arancio Anfiteatro.
  Proposta: i settori tengono le tinte; il metodo usa il colore della parte, con i colori
  delle componenti solo nelle annotazioni sui fotogrammi.
- **Frontespizi**: le parti 2 e 3 li hanno (mezza pagina vuota ciascuno), le parti 1 e 4
  no. O tutti o nessuno. Se restano, che portino contenuto: il frontespizio della parte
  «Le linee» può essere la **tavola di stato delle 24 linee** (codice, nome, lunghezza,
  livello, pagina), che oggi non esiste in nessun posto unico.
- **Pagine semivuote**: 5, 7, 8, 10, 16, 19, 26. Con la ricompattazione del metodo e lo
  spostamento delle foto nei settori, la guida scende attorno alle 22–24 pagine con lo
  stesso contenuto.
- **Minuzie**: il campo di rilievo «stagionalita» è senza accento; «Lunghezza (catalogo)»
  in tabella basta scriverlo una volta nella legenda; la foto «Da terra» della Despedida ha
  come didascalia un soggetto da confermare, e una figura dal soggetto incerto orienta male
  più di quanto aiuti.

---

## 4. Struttura proposta per l'edizione 1.0

| | Parte | Contenuto | Pagine stimate |
|---|---|---|---|
| 0 | Copertina | titolo, a cura di, edizione, data | 1 |
| 1 | Come leggere questa guida | a chi serve, i quattro livelli di documentazione, i marcatori, l'avvertenza, l'indice | 1–2 |
| 2 | La Pietra | lo spot; accesso e regole (sezioni presenti, compilate quando il gruppo risponde); la panoramica dei settori; la planimetria | 3 |
| 3 | Le linee | tavola di stato delle 24 linee; poi, settore per settore lungo la cresta: pagina del settore (render + tabella) seguita dalle schede delle sue linee di livello ≥ 1 | 12–13 |
| 4 | Come si monta: il metodo Bisma | sei capitoli (3.5) | 6 |
| 5 | Apparato | glossario e terminologia; protocollo di rilievo; fonti e date; avvertenza; colophon | 3–4 |

A parte, come oggi: il **fascicolo di rilievo** (con un foglio per lo spot, i campi GPS e
la lista delle foto da fare) e la **scheda dei dubbi**.

**Ordine delle parti.** Oggi il metodo precede le linee. Per una «guida alle highline» le
linee sono il centro e il metodo è il riferimento; e il metodo, oggi, è ricavato da una
linea sola. Propongo **linee prima, metodo dopo**, con la scheda che rimanda al capitolo del
metodo quando serve. L'alternativa (metodo prima, perché introduce «lato tensione» e «sosta
main») si risolve con la pagina «Come leggere» e il glossario. È una scelta da confermare.

---

## 5. Che cosa può dare solo il gruppo

Niente di questo si risolve impaginando. Conviene chiederlo in una volta, con la scheda dei
dubbi già prevista, aggiungendo le voci che oggi non ci sono:

1. Accesso, avvicinamenti, parcheggio per ciascun settore.
2. Regole dello spot: autorizzazioni, periodi di divieto, accordi, permarig, notte.
3. Il controllo del file LineeBisma con chi l'ha compilato (decisione D6): sblocca
   «Ancoraggio standard Bisma» nel metodo e le tipologie delle linee.
4. I nomi SlackMap delle 24 linee (lettura da fare, fonte già nota).
5. Il lato di tensione delle sei linee fotografate (dubbio 60).
6. Chi firma la guida e come si segnalano le correzioni.

---

## 6. Interventi sul codice

Sono la condizione perché le proposte sopra non restino una tantum.

- **Un registro per tutto.** `dati/linee.py` conosce settore, lunghezza e stato;
  `dati/foto_carlo.py` conosce le sei linee del file; `build/scheda_53.py` ha dentro di sé
  tutti i dati della 53 m (coordinate, materiale, A-frame, varianti). Proposta: una voce per
  linea in `dati/linee/<id>.py` (o un unico file con un dizionario per linea) con tutti i
  campi; il livello di documentazione si **calcola** dai campi presenti invece di essere
  dichiarato.
- **Una scheda generica.** `build/scheda_linea.py` disegna qualunque linea dal suo
  dizionario, mostrando solo le sezioni per cui esistono dati; `scheda_53.py` diventa il
  primo caso d'uso e sparisce come modulo speciale. Documentare la seconda linea significa
  compilare un file di dati, non copiare 370 righe.
- **Le didascalie e le note calcolate** (già fatto per `nota_settori`, `nota_copertura`,
  `FONTI`) vanno estese ai conteggi che compaiono in copertina, indice e colophon.
- **Un nome di file** da rivedere: `dati/foto_carlo.py` porta il nome di una persona del
  gruppo in un repository pubblico; il contenuto parla già di «file del gruppo». Rinominarlo
  (`dati/file_lineebisma.py`) costa poco.
- `DUBBI.md` resta il registro dei dubbi; il protocollo di rilievo e la lista delle domande
  al gruppo possono derivarne, ma vanno scritti come istruzioni, non come tabella di stato.

---

## 7. Piano proposto, in passi verificabili

1. **Decidere la struttura** (questo documento): ordine delle parti, livelli di
   documentazione, codici delle linee, sorte dei principi generici nel metodo.
2. **Registro unico e scheda generica**: migrare la 53 m nel nuovo formato e ottenere un
   PDF identico nel contenuto. Criterio: stesso testo, stesse foto, stessi rimandi.
3. **Riorganizzare le parti**: «Come leggere», «La Pietra» con le sezioni vuote dichiarate,
   linee per settore con le sei fotografate al loro posto, metodo in sei capitoli, apparato
   con protocollo di rilievo e colophon. Criterio: nessuna informazione persa rispetto
   all'edizione del 27/10 (confronto del testo estratto dai due PDF), pagine semivuote
   azzerate.
4. **Pulizia dei marcatori**: celle vuote per le misure assenti, rosso solo per i dati
   incerti, avvertenze senza oggetto tolte. Criterio: conteggio dei [DA CONFERMARE] per
   pagina, oggi 89 in totale con un massimo di 24 su una pagina.
5. **Fascicolo di rilievo**: foglio dello spot, campi GPS e foto da fare, suggerimenti dal
   file per le sei linee. Criterio: una scheda compilata per prova contiene tutto ciò che
   serve a produrre una scheda di livello 2.
6. **Revisione su Figma** dell'impaginazione, come da prassi, e poi il giro di domande al
   gruppo (sezione 5).

Scelte da confermare prima di scrivere codice:

- **A.** Ordine: linee prima del metodo (proposta) oppure metodo prima (come oggi).
- **B.** Codici delle linee (`AN-4`) sì o no; e se sì, con i nomi SlackMap raccolti prima.
- **C.** I principi generici nel metodo (checklist dei punti, spit/tasselli/resinati, ruolo
  dell'A-frame): tenerli etichettati come «non del gruppo» oppure toglierli.
- **D.** Frontespizi di parte: nessuno (proposta), oppure per tutte le parti con contenuto.
- **E.** Il materiale del file LineeBisma: nel fascicolo di rilievo (proposta) oppure
  ancora nella guida, ridotto.
