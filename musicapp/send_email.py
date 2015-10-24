#!/usr/bin/python
import smtplib
def send_email(email, passw):
	# Specifying the from and to addresses

	fromaddr = 'rishavbot@gmail.com'
	toaddrs  = email

	# Writing the message (this message will appear in the email)

	msg = 'Subject: Password Reset\n\nHere is your new password: \n%r\n\nPlease Log in with this password and change it immediately.' % passw

	# Gmail Login

	username = 'rishavbot'
	password = 'FF^FFS$$D&G123'

	# Sending the mail  

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()