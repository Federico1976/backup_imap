import imaplib

def list_mailboxes(imap_server, email_user, email_pass):
    try:
        # Connessione al server IMAP
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        print("Login effettuato con successo!")

        # Elenco delle cartelle
        status, mailboxes = mail.list()
        if status == "OK":
            print("\nElenco delle cartelle disponibili:")
            for mailbox in mailboxes:
                print(mailbox.decode())
        else:
            print("Errore nel recuperare l'elenco delle cartelle.")

        # Disconnessione
        mail.logout()
    except Exception as e:
        print(f"Errore: {e}")

# Richiedi all'utente le informazioni necessarie
imap_server = input("Inserisci il server IMAP (es. imap.gmail.com): ").strip()
email_user = input("Inserisci il tuo indirizzo email: ").strip()
email_pass = input("Inserisci la tua password: ").strip()

# Esegui il comando per elencare le cartelle
list_mailboxes(imap_server, email_user, email_pass)
