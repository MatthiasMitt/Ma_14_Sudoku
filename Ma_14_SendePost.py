# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
#with open(textfile) as fp:
#    # Create a text/plain message
#    msg = EmailMessage()
#    msg.set_content(fp.read())

msg = EmailMessage()
msg.set_content('Der Runpf der Test-e-Mail')
# me == the sender's email address
# you == the recipient's email address
me = 'Matthias@Mittelstein.name'
you = 'Matthias@M-Mittelstein.de'
msg['Subject'] = 'Python schreibt selbst' # 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
