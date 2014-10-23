import os
import re
import sys
import uuid
import requests
import subprocess
from ast import literal_eval

conf = {} # populated by given command line arguments via start()

def request(context, flow):
	request = flow.request
	x = request.path
	if(request.host == "feelinsonice-hrd.appspot.com" and x.startswith('/ph/blob', 0, 8)):
		blobURI = "http://"+request.host+request.path
		log("Downloading intercepted blob ("+blobURI+")")
		r = requests.get(blobURI)
		blobFile = "./blob"
		b = open(blobFile, 'w+')
		print >> b, r.content
		log("Downloaded blob")
		
		log("Decrypting file...")
		if(not os.path.exists(os.path.expanduser(conf['snapsDir']))):
			os.makedirs(os.path.expanduser(conf['snapsDir']))
		outputFile = os.path.expanduser(conf['snapsDir']) + 'snap_%s' % str(uuid.uuid4())
		rubyFile = conf['pyDir']+'/decrypt_snap.rb'
		subprocess.call(['ruby', rubyFile, blobFile, outputFile])
		log("File decrypted! Your picture is now available.")
		log("---- Waiting for a Snapchat... ----")

def start(context, argv):
	global conf
	conf = literal_eval(argv[1]) # decode all script arguments
	conf['pyDir'] = os.path.dirname(argv[0])

	snapsDir = conf['snapsDir']
	if(not snapsDir[-1:] == '/'):
		snapsDir = snapsDir+'/' 
	conf['snapsDir'] = snapsDir

	print 'Snapception is now running on Port %s. Configure your device to point to this port via a proxy. Intercepted snaps will appear in \"%s\"' % (conf['port'], conf['snapsDir'][:-1])
	print 'If you have not already done so, you will need to install a Certificate Authority. The easiest way to do this is to visit mitm.it on your device.'
	log("---- Waiting for a Snapchat... ----")

def log(str):
	if(not conf['verbose']):
		print str

