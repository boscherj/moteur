# -*- coding: utf-8 -*-
import requests
import re

#------------------------------------------------------------------------------
# Pour l'Occitane qui utilise des accents dans ses URLs	

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
