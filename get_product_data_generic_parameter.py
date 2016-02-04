# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from xml.sax.saxutils import escape
from mot_generic_tools import *

#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_GenericProductImgURL(bsObj, site):

	par1 = site.give_GenericProductImgURL_par1
	par2 = site.give_GenericProductImgURL_par2
	par3 = site.give_GenericProductImgURL_par3
	par4 = site.give_GenericProductImgURL_par4
	print par1
	print par2
	print par3
	print par4
					
	#Bougies LA Française
	image=bsObj.find(par1, {par2:par3})
	
	if image != None:
		#print "Cas 2 image"
		imgUrlSrc = image.img[par4]
		return imgUrlSrc



	return ""

#---------------------------------------------------------------------------------
#on cherche le nom du produit 
def give_GenericProductName(bsObj, produit, site):

	nom_produit = None
	par1 = site.check_give_GenericProductName_par1
	par2 = site.check_give_GenericProductName_par2
	par3 = site.check_give_GenericProductName_par3
	
	par4 = site.check_give_give_GenericProductName_nom_produit
	print "Par 4"
	print par4
	
	#cas 2 - Bougies La Française
	produit_title = bsObj.find(par1, {par2:par3})
	if produit_title != None:
		if par4 == "1":
			print "nom_produit =" 
			nom_produit = produit_title.get_text()
			print nom_produit
		#if check_est_une_bougie_Generic(bsObj):
		else:
			nom_produit = produit_title["content"]
			
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
def check_GenericIsItAproduct(bsObj, site):

	par1 = site.check_GenericIsItAproduct_par1
	par2 = site.check_GenericIsItAproduct_par2
	par3 = site.check_GenericIsItAproduct_par3

	produit = bsObj.find(par1, {par2:par3})
	if produit != None: 
		return produit
		
		
	#ce n'est pas un produit
	return produit

#---------------------------------------------------------------------------------
#On cherche le prix affiche
def check_GenericProductPriceNorma(bsObj, site):
	
	par1 = site.check_GenericProductPriceNorma_par1
	par2 = site.check_GenericProductPriceNorma_par2	
	par3 = site.check_GenericProductPriceNorma_par3
	
	#Cas Bougies La Française
	prix = bsObj.find(par1, {par2:par3})
	if prix != None:
		return prix
		
	return prix
	
#---------------------------------------------------------------------------------
#On cherche le prix avant les soldes
def check_GenericProductPriceAvantSoldes(bsObj, site):
	

	par1 = site.check_GenericProductPriceAvantSoldes_par1
	par2 = site.check_GenericProductPriceAvantSoldes_par2	
	par3 = site.check_GenericProductPriceAvantSoldes_par3
			
	#Cas Bougies La Française
	ps=bsObj.find(par1, {par2:par3})
	if ps != None:
		return ps
		
		
	return ps
		
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Generic
def check_GenericProductPrice(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Cas Affiche
	prix = check_GenericProductPriceNorma(bsObj, site)
	if prix != None:
		prixTxt = prix.get_text()
		old_prixValueTxt = prixTxt
					
	#prix avant sold	
	#Cas L'Occitane
	ps=check_GenericProductPriceAvantSoldes(bsObj, site)
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
def get_GenericProductDescription(bsObj, site):

	par1 = site.get_GenericProductDescription_par1
	par2 = site.get_GenericProductDescription_par2
	par3 = site.get_GenericProductDescription_par3
	par4 = site.get_GenericProductDescription_par4
	
	
	#Bougies La Française
	str = ""
	description=bsObj.find(par1, {par2:par3})
	if description != None:
		if par4=="1":
			str = description["content"]
			return str
		elif par4=="2":
			str = get_GenericProductDescriptionExtractStr(bsObj, description)
			return str
					
	return str 
	


#---------------------------------------------------------------------------------
def get_GenericProduct(bsObj, site_etudie):
	
	site_etudie_par = Site()
	site_etudie_par.creation(site_etudie)
		
	produit = check_GenericIsItAproduct(bsObj, site_etudie_par)
	if produit != None: 
		
		#on teste si c'est une bougie
		nom_produit = give_GenericProductName(bsObj, produit, site_etudie_par)
		if (nom_produit != "") & (nom_produit != None):
			#print(nom_produit)
			produit_actif.add_NomProduit(nom_produit)

			prix, old_price, special_price = check_GenericProductPrice(bsObj, site_etudie_par)		
			if prix != None: 	
				produit_actif.add_PrixProduit(prix, old_price, special_price)		
				imgUrlSrc = give_GenericProductImgURL(bsObj, site_etudie_par)
				if imgUrlSrc != "":
					#print imgUrlSrc
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_GenericProductDescription(bsObj, site_etudie_par)
					produit_actif.add_Description_Produit(description)
			
