# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from xml.sax.saxutils import escape

#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_MagentoProductImgURL(bsObj):

#durance
	image=bsObj.find("div", {"class":"product-image-gallery"})
	if image != None:
		#print "Cas 1 image"
		imgUrlSrc = image.img['src']
		return imgUrlSrc
				
	#esteban
	image=bsObj.find("p", {"class":"main-product-img"})
	if image != None:
		#print "Cas 2 image"
		imgUrlSrc = image.a["href"]
		return imgUrlSrc
						
	#synopsisparis
	image=bsObj.find("div", {"class":"product-img-box"})
	if image != None:
		#print "Cas 3 image"
		imgUrlSrc = image.img["src"]
		return imgUrlSrc

	#Diptyqueparis
	image=bsObj.find("img", {"id":"large-image"})
	if image != None:
		#print "Cas 4 image"
		imgUrlSrc = image["src"]
		return imgUrlSrc

	#Le Bon Marche
	image=bsObj.find("meta", {"property":"og:image"})
	if image!= None:
		imgUrlSrc= image["content"]	
		return imgUrlSrc

	return ""

#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_MagentoProductName(bsObj, produit):

	#cas 1 - par exemple Le Bon Marche
	produit_title = bsObj.find("meta", {"property":"og:title"})
	if produit_title != None:
		nom_produit = produit_title["content"]
		#if check_est_une_bougie_Magento(bsObj):
		if  est_ce_une_bougie(nom_produit):
			#print(produit_title)
			#return(produit_title)
			return(nom_produit)

	if produit.h3 != None:
		nom_produit = produit.h3.get_text()
		#if check_est_une_bougie_Magento(bsObj):
		if  est_ce_une_bougie(nom_produit):
			#print(nom_produit)
			return(nom_produit)

	else:
		nom_produit = produit.get_text()
		#if check_est_une_bougie_Magento(bsObj):
		if  est_ce_une_bougie(nom_produit):
			#print(nom_produit)
			
			#on ajoute enventuellement la collection (Esteban)
			collection = bsObj.find("span", {"class":"product-coll"})
			if collection != None:
				nom_produit = nom_produit + " - " + collection.get_text()	
				
			return(nom_produit)
		else:
			#print 'pas une bougie'
			return ""

#---------------------------------------------------------------------------------
#on vérifie que c'est bien un produit 
def check_MagentoIsItAproduct(bsObj):

	#cas 1 - par exemple Durance
	produit = bsObj.find("li", {"class":"product"})
	if produit != None: 
		return produit

	#cas 2 - par exemple Diptyqueparis
	produit = bsObj.find("div", {"class":"product-shop details details-top"})
	if produit != None: 
		return produit

	#cas 3 - par exemple Le Bon Marche
	produit = bsObj.find("meta", {"property":"og:type"})
	if produit != None: 
		if produit["content"] == "product":
			return produit

	#ce n'est pas un produit
	return produit

#---------------------------------------------------------------------------------
#cherche le prix d'un produit Magento
def check_MagentoProductPrice(bsObj):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
		
	#pas de prix soldé
	prix = bsObj.find("span", {"class":"price"})
	if prix != None:
		prixTxt = prix.get_text()
		#print prixTxt
	
	#Diptyqueparis
	else:
		prixProduit = bsObj.find("div", {"class":"product"})
		if prixProduit != None: 
			x=bsObj.find("div", {"class":"features-holder"})
			if x != None:
				y=x.find("div", {"id":"candle-care-div"})
				if y != None: 
					z=y.find_next_siblings("strong")
					if z != None:
						print "Prix du produit Diptyqueparis"
						prixTxt= z[0].get_text()
						print prixTxt
					
	#prix soldé	
	ps=bsObj.find("div", {"class":"product-shop"})
	
	if ps != None:
		old_prix = ps.find("p", {"class":"old-price"})	
		if old_prix != None:
			old_prixValue = old_prix.find("span", {"class":"price"})
			old_prixValueTxt = old_prixValue.get_text()
			#print old_prixValueTxt
		
		special_prix = ps.find("p", {"class":"special-price"})	
		if special_prix != None:
			special_prixValue = special_prix.find("span", {"class":"price"})
			special_prixValueTxt = special_prixValue.get_text()
			#print special_prixValueTxt

	#si on touve un prix et un prix de solde différent du prix initial alors ce n'est pas le bon produit
	if prixTxt != None:
		if old_prixValueTxt != None:
			if old_prixValueTxt != prixTxt:
				print "Anomalie"
				return(prixTxt, None, None)
				
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	
#---------------------------------------------------------------------------------
def get_MagentoProductLeBonMarche(bsObj):
	
	print "Magento Le Bon Marche"
	
	produit = check_MagentoIsItAproduct(bsObj)
	if produit != None: 
		nom_produit = give_MagentoProductName(bsObj, produit)
		if nom_produit != "":
			print(nom_produit)
			
		#ce n'est pas une bougie				
		else:
			print "Pas une bougie"	
			return

	else:
		print "Pas un produit"
		return

	
	
	#L'image
	imgUrlSrc = give_MagentoProductImgURL(bsObj)

	if imgUrlSrc!= "":
		print imgUrlSrc	
			
	price, old_price, special_price = check_MagentoProductPrice(bsObj)

	
#---------------------------------------------------------------------------------
def get_MagentoProductDiptyqueparis(bsObj):
	
	print "Magento Diptyqueparis"
	
	produit = check_MagentoIsItAproduct(bsObj)
	if produit != None: 
		nom_produit = give_MagentoProductName(bsObj, produit)
		#on teste si c'est une bougie
		if nom_produit != "":
			print(nom_produit)
			
		#ce n'est pas une bougie				
		else:
			print "Pas une bougie"	
			return

	prixProduit = bsObj.find("div", {"class":"product"})
	if prixProduit != None: 
		x=bsObj.find("div", {"class":"features-holder"})
		if x != None:
			y=x.find("div", {"id":"candle-care-div"})
			if y != None: 
				z=y.find_next_siblings("strong")
				if z != None:
					print "Prix du produit Diptyqueparis"
					print z[0].get_text()

	else:
		return
		#je ne m'occupe pas des soldes pour l'instant
	
	
	#L'image
	imgUrlSrc=give_MagentoProductImgURL(bsObj)
	if imgUrlSrc!= "":
		print imgUrlSrc	

#---------------------------------------------------------------------------------

def removeForm(description):
	if description.form.decompose() != None:
		removeForm(description)
		
def removeScript(description):
	if description.script.decompose() != None:
		removeScript(description)
				
#---------------------------------------------------------------------------------
#Retourne la description du produit
#On sait ici que la page est une celle du produit - il y a un prix - un nom
def get_MagentoProductDescriptionExtractStr(bsObj, description):

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
def get_MagentoProductDescription(bsObj):

	#Durance
	str = ""
	description=bsObj.find("div", {"class":"boxProductViewDescription"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str
	
	#Esteban
	#Bougies Parfums
	#Sia	
	description=bsObj.find("div", {"class":"std"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str	
	
	#La Boîte à Bougies	
	description=bsObj.find("div", {"id":"short_description_content"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str	
		
	#Diptyque	
	description=bsObj.find("div", {"class":"tabs-cnt"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str		
		
		
	#Le Bon Marché	
	description=bsObj.find("p", {"id":"product-description"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str		
	
	#Sia	
	#Traité plus haut
	description=bsObj.find("p", {"class":"details-p"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str	
	
	#La Boîte à Bougies	
	#Traité plus haut
	description=bsObj.find("div", {"itemprop":"description"})
	if description != None:
		str = get_MagentoProductDescriptionExtractStr(bsObj, description)
		return str	
						
	#return str 
	


#---------------------------------------------------------------------------------
def get_MagentoProduct(bsObj):
		
	produit = check_MagentoIsItAproduct(bsObj)
	if produit != None: 
		
		#on teste si c'est une bougie
		nom_produit = give_MagentoProductName(bsObj, produit)
		if (nom_produit != "") & (nom_produit != None):
			#print(nom_produit)
			produit_actif.add_NomProduit(nom_produit)

			prix, old_price, special_price = check_MagentoProductPrice(bsObj)		
			if prix != None: 	
				produit_actif.add_PrixProduit(prix, old_price, special_price)		
				imgUrlSrc = give_MagentoProductImgURL(bsObj)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_MagentoProductDescription(bsObj)
					produit_actif.add_Description_Produit(description)
			
