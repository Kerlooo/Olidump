import requests
import json
import sys
import os

def main():
    url = "https://training.olicyber.it/api"
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".olicyber_login.json")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            login_data = json.load(f)
    except FileNotFoundError:
        print(f"File non trovato. Creazione del template in {config_file}...")

        template = {
            "username": "INSERISCI_QUI_USERNAME", 
            "password": "INSERISCI_QUI_PASSWORD"
        }
        
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4)
            
        print("File creato! Apri il file, inserisci le tue credenziali e riavvia lo script.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Errore: Il file {config_file} non è formattato correttamente.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Devi inserire il codice della challenge.")
        sys.exit(1)

    challenge_id = str(sys.argv[1])
    if not challenge_id.isnumeric():
        print("Codice della challenge non valido.")
        sys.exit(1)

    s = requests.Session()
    r_login = s.post(f"{url}/login", json=login_data)

    if r_login.status_code != 200:
        print(f"Errore di login ({r_login.status_code}): {r_login.text}")
        sys.exit(1)

    dati_risposta = r_login.json()
    token = dati_risposta.get("token")
        
    s.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
    })

    r_challenge = s.get(f"{url}/challenges/{challenge_id}")

    if r_challenge.status_code != 200:
        print(f"Errore: {r_challenge.status_code}")
        sys.exit(1)

    challenge_data = r_challenge.json()

    os.makedirs(challenge_data.get('title'), exist_ok=True)
    md_path = os.path.join(challenge_data.get('title'), "challenge.md")

    with open(md_path, "w", encoding="utf-8") as readme:
        readme.write(f"# {challenge_data.get('title')}\n## Autore: **{challenge_data.get('authors')}**\n## **TAG**: {challenge_data.get('tags')}\n\n## Challenge:\n{challenge_data.get('description')}")
        
    files = challenge_data.get("files", [])
    if files:
        print(f"Trovati {len(files)} allegati. Inizio il download...")
        for f in files:
            nome_file = f.get("name")
            file_url = f.get("url")
            
            if file_url.startswith("/"):
                file_url = f"https://training.olicyber.it{file_url}"
                
            print(f"Scaricando {nome_file}...")
            r_file = s.get(file_url, stream=True)
            
            if r_file.status_code != 200:
                print(f"[ERRORE] Impossibile scaricare {nome_file}. Status: {r_file.status_code}")
                continue 
            file_path = os.path.join(challenge_data.get('title'), nome_file)
            with open(file_path, "wb") as out_file:
                for chunk in r_file.iter_content(chunk_size=8192):
                    out_file.write(chunk)
                print(f"[OK] {nome_file} salvato in {challenge_data.get('title')}/")
    print("FINITO")

if __name__ == "__main__":
    main()