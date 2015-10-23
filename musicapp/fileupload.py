#!/usr/bin/python

# Include the Dropbox SDK
import dropbox

# Get your app key and secret from the Dropbox developer website
app_key = 'INSERT_APP_KEY'
app_secret = 'INSERT_APP_SECRET'
access_token = "nZ3DGwWQrRIAAAAAAAABSSMf-rSqqQK1GYuK1MboOQ_WQ3HFSiwAZMn3_smsHGwg"
user_id = "9716375"

client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

def upload(f,songdata):
	response = client.put_file('/' + songdata.lower() + '.mp3', f)
	return response
def download(songdata):
	f, metadata = client.get_file_and_metadata('/' + songdata.lower() + '.mp3')
	return (f,metadata)
def delete(songdata):
	response = client.file_delete('/' + songdata.lower() + ".mp3")
	return response