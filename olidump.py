import requests
import json
import sys
import os
import argparse

URL = "https://training.olicyber.it/api"
TIMEOUT = 30


def safe_name(name):
    """Restituisce un nome file/cartella sicuro (no path traversal)."""
    if not name:
        return None
    base = os.path.basename(str(name).strip())
    if base in ("", ".", ".."):
        return None
    return base


def main():
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".olicyber_login.json")

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            login_data = json.load(f)
    except FileNotFoundError:
        print(f"File non trovato. Creazione del template in {config_file}...")

        template = {
            "email": "INSERISCI_QUI_LA_EMAIL",
            "password": "INSERISCI_QUI_PASSWORD"
        }

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4)

        # Permessi ristretti: il file contiene credenziali in chiaro.
        if os.name == "posix":
            os.chmod(config_file, 0o600)

        print("File creato! Apri il file, inserisci le tue credenziali e riavvia lo script.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Errore: Il file {config_file} non è formattato correttamente.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Scarica una challenge di OliCyber (testo + allegati)."
    )
    parser.add_argument("challenge_id", type=int, help="ID numerico della challenge")
    args = parser.parse_args()
    challenge_id = args.challenge_id

    s = requests.Session()

    try:
        r_login = s.post(f"{URL}/login", json=login_data, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete durante il login: {e}")
        sys.exit(1)

    if r_login.status_code != 200:
        print(f"Errore di login ({r_login.status_code}): {r_login.text}")
        sys.exit(1)

    token = r_login.json().get("token")
    if not token:
        print("Errore: login riuscito ma token assente nella risposta.")
        sys.exit(1)

    s.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    })

    try:
        r_challenge = s.get(f"{URL}/challenges/{challenge_id}", timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        sys.exit(1)

    if r_challenge.status_code != 200:
        print(f"Errore: {r_challenge.status_code}")
        sys.exit(1)

    challenge_data = r_challenge.json()

    title = safe_name(challenge_data.get("title"))
    if not title:
        print("Errore: titolo della challenge assente o non valido.")
        sys.exit(1)

    os.makedirs(title, exist_ok=True)
    md_path = os.path.join(title, "challenge.md")

    with open(md_path, "w", encoding="utf-8") as readme:
        readme.write(
            f"# {challenge_data.get('title')}\n"
            f"## Autore: **{challenge_data.get('authors')}**\n"
            f"## **TAG**: {challenge_data.get('tags')}\n\n"
            f"## Challenge:\n{challenge_data.get('description')}"
        )

    files = challenge_data.get("files", [])
    if files:
        print(f"Trovati {len(files)} allegati. Inizio il download...")
        for f in files:
            nome_file = safe_name(f.get("name"))
            file_url = f.get("url")

            if not nome_file or not file_url:
                print("[ERRORE] Allegato con nome o URL non valido, salto.")
                continue

            if file_url.startswith("/"):
                file_url = f"https://training.olicyber.it{file_url}"

            print(f"Scaricando {nome_file}...")
            try:
                r_file = s.get(file_url, stream=True, timeout=TIMEOUT)
            except requests.exceptions.RequestException as e:
                print(f"[ERRORE] Impossibile scaricare {nome_file}: {e}")
                continue

            if r_file.status_code != 200:
                print(f"[ERRORE] Impossibile scaricare {nome_file}. Status: {r_file.status_code}")
                continue

            file_path = os.path.join(title, nome_file)
            with open(file_path, "wb") as out_file:
                for chunk in r_file.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            print(f"[OK] {nome_file} salvato in {title}/")
    print("FINITO")


if __name__ == "__main__":
    main()
