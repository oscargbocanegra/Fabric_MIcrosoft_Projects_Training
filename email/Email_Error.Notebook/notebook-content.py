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
from email.mime.text import MIMEText

subject = 'Pipeline Error'
body = 'l proceso del pipeline ha caido en error debido a que no se encuentra la carpeta'
sender = "oscargiovanni@gmail.com"
my_password = 'gexhmyjudrpewylw'
recipients = ["oscargiovanni@gmail.com"]

def send_mail(subject, body, sender, recipients):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, my_password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    print("Message sent!")

send_mail(subject, body, sender, recipients)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
