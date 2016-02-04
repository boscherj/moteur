# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from xml.sax.saxutils import escape


#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_GenericProductImgURL(bsObj):

	#L'occitane
	image=bsObj.find("div", {"class":"carousel-page-wrapper"})
	if image != None:
		#print "Cas 1 image"
		imgUrlSrc = image.img['src']
		return imgUrlSrc
				
	#Bougies LA Française
	image=bsObj.find("span", {"id":"view_full_size"})
	if image != None:
		#print "Cas 2 image"
		imgUrlSrc = image.img['src']
		return imgUrlSrc



	return ""

#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_GenericProductName(bsObj, produit):

	nom_produit = None
	
	#cas 1 - Occitane
	produit_title = bsObj.find("meta", {"property":"og:title"})
	if produit_title != None:
		nom_produit = produit_title["content"]
		#if check_est_une_bougie_Generic(bsObj):
		if  est_ce_une_bougie(nom_produit):
			#print(produit_title)
			#return(produit_title)
			return(nom_produit)
	
	#cas 2 - Bougies La Française
	produit_title = bsObj.find("h1", {"class":"title_product"})
	if produit_title != None:
		nom_produit = produit_title.get_text()
		#if check_est_une_bougie_Generic(bsObj):
		if  est_ce_une_bougie(nom_produit):
			#print(produit_title)
			#return(produit_title)
			return(nom_produit)
					
	return nom_produit

#---------------------------------------------------------------------------------
# on vérifie que c'est bien un produit 
# Le plus simple est de vérifier s'il y a un prix
# Mais il y a aussi les meta tags og: qui permettent de reperer un produit
# On peut aussi vérifier s'il y a un bouton Acheter
def check_GenericIsItAproduct(bsObj):

	#cas 1 - Occitane	
	produit = bsObj.find("a", {"class":"add_to_bag"})
	if produit != None: 
		return produit

	#cas 1 - Bougies La Française	
	#Un SKU indique un produit
	produit = bsObj.find("meta", {"itemprop":"sku"})
	if produit != None: 
		return produit
		
		
	#ce n'est pas un produit
	return produit

#---------------------------------------------------------------------------------
#On cherche le prix affiche
def check_GenericProductPriceNorma(bsObj):
	
	#Cas L'Occitane	
	prix = bsObj.find("span", {"data-bind":"html: price"})
	if prix != None:
		return prix
		
	#Cas Bougies La Française
	prix = bsObj.find("span", {"id":"our_price_display"})
	if prix != None:
		return prix
		
	return prix
	
#---------------------------------------------------------------------------------
#On cherche le prix avant les soldes
def check_GenericProductPriceAvantSoldes(bsObj):
	
	#Cas L'Occitane	
	ps=bsObj.find("span", {"class":"product_price_before"})
	if ps != None:
		return ps
		
	#Cas Bougies La Française
	ps=bsObj.find("p", {"id":"old_price"})
	if ps != None:
		return ps
		
		
	return ps
		
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Generic
def check_GenericProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Cas Affiche
	prix = check_GenericProductPriceNorma(bsObj)
	if prix != None:
		prixTxt = prix.get_text()
		old_prixValueTxt = prixTxt
					
	#prix avant sold	
	#Cas L'Occitane
	ps=check_GenericProductPriceAvantSoldes(bsObj)
	if ps != None:
		special_prixValueTxt = ps.get_text()

				
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	
#---------------------------------------------------------------------------------
#Retourne la description du produit
#On sait ici que la page est une celle du produit - il y a un prix - un nom
def get_GenericProductDescriptionExtractStr(bsObj, description):

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
		
		#Modification pour la Lumiere des Fees				
		for x in description.findAll('span'):
			new_tag = bsObj.new_tag("br")
			if x.string != None:
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
def get_GenericProductDescription(bsObj):

	#L'Occitane
	str = ""
	description=bsObj.find("meta", {"property":"og:description"})
	if description != None:
		str = description["content"]
		return str
	
	#Bougies La Française
	str = ""
	description=bsObj.find("meta", {"name":"description"})
	if description != None:
		str = description["content"]
		return str
					
	return str 
	


#---------------------------------------------------------------------------------
def get_GenericProduct(bsObj):
		
	produit = check_GenericIsItAproduct(bsObj)
	if produit != None: 
		
		#on teste si c'est une bougie
		nom_produit = give_GenericProductName(bsObj, produit)
		if (nom_produit != "") & (nom_produit != None):
			#print(nom_produit)
			produit_actif.add_NomProduit(nom_produit)

			prix, old_price, special_price = check_GenericProductPrice(bsObj)		
			if prix != None: 	
				produit_actif.add_PrixProduit(prix, old_price, special_price)		
				imgUrlSrc = give_GenericProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_GenericProductDescription(bsObj)
					produit_actif.add_Description_Produit(description)
			
