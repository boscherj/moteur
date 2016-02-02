# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from xml.sax.saxutils import escape

#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_WoocommerceWordpressProductImgURL(bsObj):

	#Scandles
	image=bsObj.find("div", {"class":"easyzoom"})
	if image != None:
		#print "Cas 1 image"
		imgUrlSrc = image.img['src']
		return imgUrlSrc
				

	return ""

#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_WoocommerceWordpressProductName(bsObj, produit):

	#cas 1 - par exemple Scandles
	produit_title = bsObj.find("h1", {"itemprop":"name"})
	if produit_title != None:
		nom_produit = produit_title.get_text()
		return(nom_produit)

	return ""

#---------------------------------------------------------------------------------
#on vérifie que c'est bien un produit 
def check_WoocommerceWordpressIsItAproduct(bsObj):

#Il y a plusieurs possibilites pour que ce soit une page produit
	#Soit il y a un prix dans meta itemprop
	#Soit il y a un prix dans p itemprop
	produit=bsObj.find("meta", {"itemprop":"price"})
	if produit!= None: 
		return produit
		
	#cas 2	
	produit= bsObj.find("p", {"itemprop":"price"})
	if produit!= None: 
		return produit

	#ce n'est pas un produit
	return produit	

#---------------------------------------------------------------------------------
#cherche le prix d'un produit Prestashop
def check_WoocommerceWordpressProductPriceSolde(bsObj):

	old_prix = None
	
	allprix = bsObj.find("div", {"itemprop":"offers"})
	if allprix != None:
		delprix=allprix.find("del")
		if delprix != None:
			old_prix=delprix.get_text()
			return old_prix
	
	return old_prix
	
#---------------------------------------------------------------------------------
#cherche le prix d'un produit WoocommerceWordpress
def check_WoocommerceWordpressProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
		
	#pas de prix soldé
	prix = bsObj.find("meta", {"itemprop":"price"})
	if prix != None:
		prixTxt = prix['content']		
		
	else:
		prix = bsObj.find("p", {"itemprop":"price"})
		if prix != None:	
			prixTxt = prix.get_text()	
			
					
	#prix soldé	
	old_prix = check_WoocommerceWordpressProductPriceSolde(bsObj)
	if old_prix != None:
		old_prixValueTxt = old_prix
		#print old_prixValueTxt
			
		#On a un ancien prix et un prix affiché
		#Le prix affiché est alors le prix soldé
		#et l'ancien prix le prix d'origine
		if prix != None:
			#Le prix soldé est le prix affiché
			special_prixValueTxt = prixTxt	
			#l"ancien prix est le prix
							
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	

				
#---------------------------------------------------------------------------------
#Retourne la description du produit
#On sait ici que la page est une celle du produit - il y a un prix - un nom
def get_WoocommerceWordpressProductDescriptionExtractStr(bsObj, description):

	#Durance
	str2 = ""
	if description != None:
	
		#Pour Dyptique
		#removeForm(description)
		#removeScript(description)		
		
		for x in description.findAll('form'):
			description.form.extract()
			
		for x in description.findAll('script'):
			description.script.extract()
		
		#Ajout pour Diptyque	
		for x in description.findAll('a'):
			description.a.extract()
	
		for x in description.findAll('p'):
			x.name="br"
						
		for x in description.findAll('span'):
			new_tag = bsObj.new_tag("br")
			str=x.string
			new_tag.string = str
			x.replace_with(new_tag)			
			
		for x in description.findAll('h3'):
			new_tag = bsObj.new_tag("br")
			if x.string != "":
				str="_CR_"
			else:
				str=x.string
			new_tag.string = str
			x.replace_with(new_tag)
			
		for x in description.findAll('p'):
			description.p.unwrap()

		for x in description.findAll('div'):
			description.div.unwrap()
		
		for x in description.findAll('br'):
			new_tag = bsObj.new_tag("xxx")
			new_tag.string = "_CR_"
			x.insert_after(new_tag)
			
		str = description.get_text()
		str2 = str.replace("_CR_", "\n")
		return str2
		
		#il n'y a pas de </ br>	 c'est un div seul
		#return description.get_text()
			
	return str2		

#---------------------------------------------------------------------------------
#Retourne la description du produit
#On sait ici que la page est une celle du produit - il y a un prix - un nom
def get_WoocommerceWordpressProductDescription(bsObj):

	print "get_WoocommerceWordpressProductDescription"
	str = ""
	description=bsObj.find("div", {"id":"paneldescription"})
	if description != None:
		str = get_WoocommerceWordpressProductDescriptionExtractStr(bsObj, description)
		print str
		return str
		
		
	description=bsObj.find("div", {"class":"woocommerce-variation-description"})
	if description != None:
		str = get_WoocommerceWordpressProductDescriptionExtractStr(bsObj, description)
		print str
		return str
	
						
	return str 
	


#---------------------------------------------------------------------------------
def get_WoocommerceWordpressProduct(bsObj):
		
	produit = check_WoocommerceWordpressIsItAproduct(bsObj)
	if produit != None: 
		
		#on teste si c'est une bougie
		nom_produit = give_WoocommerceWordpressProductName(bsObj, produit)
		if (nom_produit != "") & (nom_produit != None):
			#print(nom_produit)
			produit_actif.add_NomProduit(nom_produit)

			prix, old_price, special_price = check_WoocommerceWordpressProductPrice(bsObj)		
			if prix != None: 	
				produit_actif.add_PrixProduit(prix, old_price, special_price)		
				imgUrlSrc = give_WoocommerceWordpressProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_WoocommerceWordpressProductDescription(bsObj)
					produit_actif.add_Description_Produit(description)
			
