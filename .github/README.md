# Olidump
Olidump ti permette di scaricare direttamente le challenge di OliCyber e scaricare anche gli allegati (nel caso ci fossero).
---
## Configurazione iniziale:
Crea il file `.olicyber_login.json` sulla directory home (`/home/tuoutente/` su Linux e `C:\Users\tuoutente\` su Windows) e inserisci queste informazioni:
```json
{
    "email": "la_tua_email@esempio.com",
    "password": "la_tua_password"
}
```

## Installazione:
> **Important Note**
> 
> È consigliato utilizzare un ambiente virtuale per non creare problemi con l'installazione di python

### Installazione globale (Linux)
```bash
git clone https://github.com/Kerlooo/Olidump.git
cd Olidump
pip install . --break-system-packages
```

### Installazione globale (Windows)
```bash
git clone https://github.com/Kerlooo/Olidump.git
cd Olidump
pip install . 
```

### Installazione su `venv` (Linux)
```bash
python3 -m venv myenv
source myenv/bin/activate
git clone https://github.com/Kerlooo/Olidump.git
cd Olidump
pip install .
```

### Installazione su `venv` (Windows)
```bash
python3 -m venv myenv
myenv\Scripts\activate
git clone https://github.com/Kerlooo/Olidump.git
cd Olidump
pip install .
```

## Utilizzo:
Una volta installato il pacchetto (e con il `venv` attivo, se ne hai usato uno), puoi avviare il tool direttamente da terminale usando il comando `olidump` seguito dall'ID della challenge.

**Sintassi:**
```bash
olidump <id_challenge>
```
---
## Licenza
Questa guida è distribuita sotto la licenza **Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0)**.

**Sei libero di:**
- **Condividere** — copiare e redistribuire il materiale in qualsiasi mezzo o formato.
- **Adattare** — remixare, trasformare e sviluppare il materiale per qualsiasi scopo, anche commerciale.

**Alle seguenti condizioni:**
- **Attribuzione** — Devi fornire il dovuto riconoscimento, fornire un collegamento alla licenza e indicare se sono state apportate modifiche.

Per ulteriori dettagli, consulta il file [LICENSE](../LICENSE) o visita [creativecommons.org](https://creativecommons.org/licenses/by/4.0/).