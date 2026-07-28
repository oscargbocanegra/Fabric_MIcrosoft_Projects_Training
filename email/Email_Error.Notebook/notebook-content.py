# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

import smtplib
import notebookutils
from email.mime.text import MIMEText

subject = 'Pipeline Error'
body = 'l proceso del pipeline ha caido en error debido a que no se encuentra la carpeta'
sender = "oscargiovanni@gmail.com"
recipients = ["oscargiovanni@gmail.com"]

# Configure these values as deployment parameters or a non-versioned environment
# configuration. The secret itself must remain in the approved secret store.
key_vault_name = "<environment-key-vault>"
smtp_secret_name = "<smtp-secret-name>"

def get_smtp_password():
    if "<" in key_vault_name or "<" in smtp_secret_name:
        raise RuntimeError(
            "Configure the environment Key Vault and SMTP secret name before enabling notifications."
        )
    return notebookutils.credentials.getSecret(key_vault_name, smtp_secret_name)

def send_mail(subject, body, sender, recipients):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, get_smtp_password())
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent!")

send_mail(subject, body, sender, recipients)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
