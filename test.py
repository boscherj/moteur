# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

def test(bsObj): 
	description=bsObj.find("div", {"class":"boxProductViewDescription"})
	
	for x in description.findAll('span'):
		new_tag = bsObj.new_tag("br")
		str=x.string
		new_tag.string = str
		x.replace_with(new_tag)

	for x in description.findAll('p'):
		new_tag = bsObj.new_tag("br")
		if x.string != None:
			print x.string 
			str=x.string
		else:
			print "no data"
			str=" "
		new_tag.string = str
		x.replace_with(new_tag)
		print new_tag.string  
		
		
	for x in description.findAll('p'):
		description.p.unwrap()

	for x in description.findAll('div'):
		description.div.unwrap()
		
	for x in description.findAll('br'):
		new_tag = bsObj.new_tag("xxx")
		new_tag.string = "_CR_"
		description.br.replace_with(new_tag)
		
	str = description.get_text()
	str2 = str.replace("_CR_", "//n")
	
	print str2
		
	return str2