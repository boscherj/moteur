# -*- coding: utf-8 -*-
import requests
import re

#------------------------------------------------------------------------------
# Pour l'Occitane qui utilise des accents dans ses URLs	

#Pour Durance
#http://stackoverflow.com/questions/2783079/how-do-i-convert-a-unicode-to-a-string-at-the-python-level
#Autre façon de faire : 
# s = ''.join(map(lambda x: chr(ord(x)),v))
#ou
# ''.join(chr(ord(c)) for c in u'Andr\xc3\xa9')
#Les 2 marchent

def from_unicode_to_utf8(u):
	# y=u.encode('latin-1').decode('utf-8')
	y = ''.join(map(lambda x: chr(ord(x)),u))
	return y
	
	
def put_accents(chaine):
	y=chaine.encode('utf-8')
	z=y.decode('utf-8').encode('latin1')
	w=unicode(z, "utf-8")
	return w

def rem_accents(pageUrl)	:

	url = pageUrl
	url = re.sub(r"à", r"%C3%A0",url)
	url = re.sub(r"á", r"%C3%A1",url)
	url = re.sub(r"â", r"%C3%A2",url)
	url = re.sub(r"ä", r"%C3%A4",url)
	url = re.sub(r"ç", r"%C3%A7",url)
	url = re.sub(r"è", r"%C3%A8",url)
	url = re.sub(r"é", r"%C3%A9",url)
	url = re.sub(r"ê", r"%C3%AA",url)
	url = re.sub(r"ë", r"%C3%AB",url)
	url = re.sub(r"ì", r"%C3%AC",url)
	url = re.sub(r"í", r"%C3%AD",url)
	url = re.sub(r"î", r"%C3%AE",url)
	url = re.sub(r"ï", r"%C3%AF",url)
	url = re.sub(r"ô", r"%C3%B4",url)
	url = re.sub(r"ö", r"%C3%B6",url)
	url = re.sub(r"ù", r"%C3%B9",url)
	url = re.sub(r"ú", r"%C3%BA",url)
	url = re.sub(r"û", r"%C3%BB",url)
	url = re.sub(r"ü", r"%C3%BC",url)
	
	print "rem_accents début"
	print url
	print "rem_accents fin"

	return url
