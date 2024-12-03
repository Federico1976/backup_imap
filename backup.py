import imaplib
import email
from email.header import decode_header
import os
import re

def sanitize_filename(filename):
    """Rimuove caratteri non validi dai nomi dei file."""
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def backup_emails(imap_server, email_user, email_pass, output_dir):
    try:
        # Connessione al server IMAP
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        print("Login effettuato con successo!")

        # Elenco delle caselle da salvare
        folders = {
            "INBOX": "Posta_in_arrivo",
            "INBOX.Sent": "Posta_inviata"
        }

        for folder, folder_name in folders.items():
            print(f"\nBackup della cartella: {folder}")
            
            # Seleziona la casella
            status, messages_count = mail.select(folder)
            if status != "OK":
                print(f"Errore nel selezionare la cartella {folder}.")
                continue

            # Cerca tutte le email nella casella
            status, messages = mail.search(None, "ALL")
            if status != "OK":
                print(f"Errore nel recuperare le email dalla cartella {folder}.")
                continue

            # Ottieni la lista di ID delle email
            email_ids = messages[0].split()
            print(f"Totale email trovate nella cartella {folder}: {len(email_ids)}")

            # Creare la directory specifica per la cartella
            folder_output_dir = os.path.join(output_dir, folder_name)
            os.makedirs(folder_output_dir, exist_ok=True)

            # Iterare sulle email
            for email_id in email_ids:
                # Fetch dell'email
                res, msg = mail.fetch(email_id, "(RFC822)")
                if res != "OK":
                    print(f"Errore nel recuperare l'email ID: {email_id} dalla cartella {folder}.")
                    continue

                for response_part in msg:
                    if isinstance(response_part, tuple):
                        # Parse del messaggio
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decodifica del soggetto
                        raw_subject = msg.get("Subject")
                        if raw_subject is None:
                            subject = "email_senza_soggetto"
                        else:
                            subject, encoding = decode_header(raw_subject)[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or "utf-8")
                            subject = sanitize_filename(subject)

                        # Decodifica dell'indirizzo email mittente
                        from_ = msg.get("From") or "Mittente Sconosciuto"
                        print(f"Scaricando: {subject} da {from_} (Cartella: {folder})")

                        # Salva l'email in un file
                        filename = f"{subject}.eml"
                        filepath = os.path.join(folder_output_dir, filename)

                        # Salva il contenuto dell'email
                        with open(filepath, "wb") as f:
                            f.write(response_part[1])

            print(f"Backup completato per la cartella {folder}. Email salvate in: {folder_output_dir}")

        # Disconnessione
        mail.logout()

    except Exception as e:
        print(f"Errore: {e}")

# Richiedi all'utente le informazioni necessarie
imap_server = input("Inserisci il server IMAP (es. imap.gmail.com): ").strip()
email_user = input("Inserisci il tuo indirizzo email: ").strip()
email_pass = input("Inserisci la tua password: ").strip()
output_dir = input("Inserisci la directory di output per il backup (es. ./backup_email): ").strip()

# Usa una directory di default se l'utente non ne specifica una
if not output_dir:
    output_dir = "./backup_email"

# Avvia il backup
backup_emails(imap_server, email_user, email_pass, output_dir)
