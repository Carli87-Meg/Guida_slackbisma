# Guida Slackbisma — Manuale Rigging

Repository per il manuale di rigging Slackbisma, migrato dall'archivio locale
`C:\Users\Carli\.ARCHIVIO\MANUALE_RIGGING_SLACKBISMA`.

## Come caricare i file dal PC locale

Il repository è già inizializzato con `.gitignore` e `.gitattributes`.
Da Windows, apri **PowerShell** ed esegui i comandi qui sotto.

### 1. Clona il repository in una cartella di lavoro

```powershell
cd C:\Users\Carli
git clone https://github.com/Carli87-Meg/Guida_slackbisma.git
cd Guida_slackbisma
git checkout claude/migrate-rigging-folder-cloud-6vj35n
```

### 2. Copia dentro il contenuto della cartella locale

```powershell
robocopy "C:\Users\Carli\.ARCHIVIO\MANUALE_RIGGING_SLACKBISMA" "C:\Users\Carli\Guida_slackbisma" /E /XD .git
```

`/E` copia anche le sottocartelle (comprese quelle vuote), `/XD .git` evita di
sovrascrivere i metadati git. Robocopy considera normale un exit code 1: vuol
dire "file copiati con successo".

### 3. Controlla cosa stai per caricare

```powershell
git status
git add -A
git status --short
```

Prima di procedere, verifica che non ci siano file oltre i 100 MB (limite di
GitHub per singolo file):

```powershell
Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 100MB } |
  Select-Object FullName, @{n='MB';e={[math]::Round($_.Length/1MB,1)}}
```

Se il comando non stampa nulla, sei a posto: salta al punto 4.
Se stampa qualcosa, vedi la sezione "File pesanti" più sotto.

### 4. Commit e push

```powershell
git commit -m "Import manuale rigging Slackbisma da archivio locale"
git push -u origin claude/migrate-rigging-folder-cloud-6vj35n
```

Al primo push Git chiederà le credenziali GitHub: usa un
[Personal Access Token](https://github.com/settings/tokens) al posto della
password, oppure installa [GitHub CLI](https://cli.github.com/) e autenticati
una volta sola con `gh auth login`.

## File pesanti (oltre 100 MB)

GitHub rifiuta i singoli file sopra i 100 MB. Se ne hai (video tutorial, scene
`.blend` complete, texture ad alta risoluzione), hai due strade.

**Opzione A — Git LFS** (consigliata se i file servono davvero nel repo):

```powershell
git lfs install
git lfs track "*.mp4"
git lfs track "*.blend"
git add .gitattributes
```

Poi riprendi dal punto 3. Nota che il piano gratuito GitHub include 1 GB di
storage LFS e 1 GB/mese di banda.

**Opzione B — tenerli fuori dal repo**: aggiungi i pattern corrispondenti a
`.gitignore` e archivia quei file su Google Drive o simili, linkandoli dal
manuale.

## Struttura

Da compilare una volta caricati i contenuti.
