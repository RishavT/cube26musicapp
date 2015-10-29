#!/usr/bin/python
import smtplib
import os
from musicapp import GMAIL_USERNAME,GMAIL_PASS
def send_email(email, passw):
	# Specifying the from and to addresses

	fromaddr = 'rishavbot@gmail.com'
	toaddrs  = email

	# Writing the message (this message will appear in the email)

	msg = 'Subject: Password Reset\n\nHere is your new password: \n%r\n\nPlease Log in with this password and change it immediately.' % passw

	# Gmail Login

	username = GMAIL_USERNAME
	password = GMAIL_PASS
	# Sending the mail  

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
