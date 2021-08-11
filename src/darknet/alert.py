import smtplib
from email.mime.text import MIMEText
import datetime

SENDER = 'alertscrapy4@gmail.com'
PASSWORD = 'qgg^ta5cw$e'
RECIPIENT = 'alertscrapy4@gmail.com'
SUBJECT = f'Scrapy Project Alert for {datetime.datetime.now()}'

def send_email():
	message = ''

	myfile = open('alert_message.txt', 'r', encoding='utf-8')
	for line in myfile.readlines:
		message+=line+"\n"
	myfile.close()

	msg = MIMEText(message)
	msg['Subject'] = SUBJECT
	msg['From'] = SENDER
	msg['To'] = RECIPIENT

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()
	s.login(SENDER, PASSWORD)
	s.sendmail(SENDER, RECIPIENT, msg.as_string())
	s.quit()

send_email()