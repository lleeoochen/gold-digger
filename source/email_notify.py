import os
from os.path import basename
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication

#Setup constants
PASSWORD = os.environ.get('TESTBOT_PASSWORD')
FROM_EMAIL = "testbotchen@gmail.com"
TO_EMAIL = ["lleeoochen@gmail.com", "nick.duncan567@gmail.com"]

#Condition check
if PASSWORD == None:
    print ('Password not found. Please set to environment variable TESTBOT_PASSWORD')
    exit()

#Setup email title
msg = MIMEMultipart()
msg['From'] = FROM_EMAIL
msg['To'] = ", ".join(TO_EMAIL)
msg['Subject'] = "GOLD DIGGER IS TRIGGERED! [From CSIL]"

#Setup email message
body = "Dear GOLD Diggers,\n\nThe daily UCSB course scraping is triggered on a CSIL machine. Thank you and have a nice day!\n\nSincerely,\nYour Lovely GOLD Digging Bot"
msg.attach(MIMEText(body, 'plain'))

#Setup attachment
with open('log.txt', "rb") as fread:
    part = MIMEApplication(fread.read(), Name=basename('log.txt'))
part['Content-Disposition'] = 'attachment; filename="%s"' % basename('log.txt')
msg.attach(part)

#Send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(FROM_EMAIL, PASSWORD)
text = msg.as_string()
server.sendmail(FROM_EMAIL, TO_EMAIL, text)
server.quit()
 
