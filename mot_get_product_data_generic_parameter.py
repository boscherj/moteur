# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from check_cms import *
from enregistrement import *
from xml.sax.saxutils import escape
from mot_generic_tools import *
import dryscrape
from urlparse import urlparse

#---------------------------------------------------------------------------------
#on cherche l'URL de l'image
def give_GenericProductImgURL(bsObj, site):

	par1 = site.give_GenericProductImgURL_par1
	par2 = site.give_GenericProductImgURL_par2
	par3 = site.give_GenericProductImgURL_par3
	par4 = site.give_GenericProductImgURL_par4
	
									
	#image=bsObj.find(par1, {par2:par3})
	#JBS le 30 mars 2016
	try:
		image=bsObj.find(par1, {par2:par3})
	except:
		print "Erreur - image absente"
		return ""
					
	
	if image != None:
		if par4=="href":
			imgUrlSrc = image.a[par4]
		elif par4=="content":
			imgUrlSrc = image[par4]
		elif par4=="imagesrc":
			imgUrlSrc = image["src"]
		elif par4=="image_a_img_src":
			imgUrlSrc = image.a.img["src"]
		elif par4=="data-zoomsrc":
			imgUrlSrc = image["data-zoomsrc"]
		elif par4=="og":
			imgUrlSrc = image["content"]
		elif par4=="data-src":
			imgUrlSrc = image["data-src"]
		elif par4=="bon-marche":
			imgUrlSrc = image.picture.img["src"]
			
		#Ajout JBS le 2/6/2016 
		elif par4=="gettxt":
			imgUrlSrc = image.get_text()
			
		elif par4=="nextimg":
			x=image.find_all("img")
			try:
				imgUrlSrc = x[1]["src"]
			except:
				imgUrlSrc = x[0]["src"]
		else:
			try:
				imgUrlSrc = image.img[par4]
			except:
				print "Erreur - image absente"
				return ""
		
		#Pour Net a Porter
		if site.categorie=="120":
			imgUrlSrc = imgUrlSrc.replace('in_ml.jpg','in_pp.jpg')	
			
		#Pour The Conran Shop
		#if site.categorie=="187":
			#imgUrlSrc = imgUrlSrc.replace('https','http')		
			
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
	euro="euro"
	lalique = "france ("
	
	
	if par1=="gettext":
		nom_produit = produit.get_text()	
		if est_ce_une_bougie(nom_produit):
			return(nom_produit)
		else:
			return None 
	
	#cas 2 - Bougies La Française
	produit_title = bsObj.find(par1, {par2:par3})
	if produit_title != None:
	
		#cas Jovoy - le nom bougie n'est pas dans le titre
		#JBS le 15/4/2016 
		bougiedanslebreadcrumb=False
		if par4 == "2":
			p=bsObj.find("a", {"title":"Bougies"})
			if p!= None:
				bougiedanslebreadcrumb=True
				#print "bougiedanslebreadcrumb"
	
			
				
				
		if par4 == "1":
			#print "nom_produit =" 
			nom_produit = produit_title.get_text()
			#print nom_produit
			
			#Ajout JBS le 28/4/2016
			#Pour Papillon Rouge
			breadcrumb = bsObj.find("div", {"class":"breadcrumb_inner"})
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Atelier des Martyrs
			#JBS le 16/5/2016
			breadcrumb = bsObj.find("nav", {"class":"woocommerce-breadcrumb"})
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Blanc d'Ivoire
			#JBS le 31/5/2016
			breadcrumb = bsObj.find("div", {"class":"breadcrumb"})
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					
			
			#Pour Ambiance de la maison
			#JBS le 31/5/2016
			breadcrumb = bsObj.find("span", {"class":"navigation_page"})
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Phaedon
			#JBS le 1/6/2016
			breadcrumb = bsObj.find("ul", {"class":"arianne"})
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Imagineair
			#JBS le 17/10/2016
			breadcrumb = bsObj.find("title")
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("ateur de bougies parfum")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Premiere Avenue
			#JBS le 31/10/2016
			#breadcrumb = bsObj.find("nav", {"class":"woocommerce-breadcrumb"})
			breadcrumb = bsObj.find("div", {"class":"ariane"})
			
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				#x = breadcrumbTxt.lower().find("bougies parfum")
				x = breadcrumbTxt.lower().find("bougie")
				if x>0:
					bougiedanslebreadcrumb=True
					#JBS le 10/1/2017 probleme d'encodage chez Premiere Avenue
					#nom_produit = nom_produit.encode('latin-1')
					
					
					
			#Pour Herve Gambs
			#JBS le 2/11/2016
			breadcrumb = bsObj.find("div", {"class":"breadcrumb"})
			
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougies parfum")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Jovoy
			#JBS le 3/11/2016
			breadcrumb = bsObj.find("div", {"class":"breadcrumb"})
			
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougies")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
					
			#Pour Guerlain
			#JBS le 18/11/2016
			breadcrumb = bsObj.find("div", {"class":"breadcrumbs"})
			
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougies")
				if x>0:
					bougiedanslebreadcrumb=True
					
					
			#Pour Papillon Rouge
			#JBS le 24/11/2016
			breadcrumb = bsObj.find("ul", {"itemprop":"breadcrumb"})
			
			if breadcrumb!=None:
				breadcrumbTxt = breadcrumb.get_text()
				x = breadcrumbTxt.lower().find("bougies")
				if x>0:
					bougiedanslebreadcrumb=True


					
							
		#if check_est_une_bougie_Generic(bsObj):
		else:
			nom_produit = produit_title["content"]
		
		#JBS le 15/4/2016 ajout de bougiedanslebreadcrumb 	
		if  est_ce_une_bougie(nom_produit) or bougiedanslebreadcrumb :
			
			#Modification le 14/3/2016	
			extension_nom = bsObj.find("option", {"selected":"selected"})
			if extension_nom != None:
				extension_str = extension_nom.get_text() 
				x = extension_str.lower().find(euro)
				x2 = extension_str.lower().find(lalique)
				
				if (not extension_str.isdigit()) and (x <0) and (x2 <0) :
					nom_produit = nom_produit + " " + extension_str
			
			#Cas particulier de Hermes - je ne veux pas la totalité du nom
			#JBS le 20/4/2016
			hermes = nom_produit.find('Herm')
			if hermes >=0:
				#A priori on a une bougie Hermes
				m = nom_produit.find('|')
				if m >=0:
					nom_produit=nom_produit[0:m]	
							 
			#return(nom_produit)
			
			ensavoirplus = nom_produit.find('En savoir plus')
			if ensavoirplus >=0:
				nom_produit=nom_produit[0:ensavoirplus]	
				print "Nom du produit : "
				print nom_produit
				
			#return(nom_produit)
			
			
		else:
			return None
					
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

	#print "par1, par2, par3 : ", par1,par2,par3
	
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
# Cas de Dyptique Paris
def check_GenericProductPriceCasComplexe_2(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	prixProduit = bsObj.find("div", {"class":"product"})
	if prixProduit != None: 
			
		x=bsObj.find("div", {"class":"features-holder"})
		if x != None:
			y=x.find("div", {"id":"candle-care-div"})
			if y != None: 
				z=y.find_next_siblings("strong")
				if z != None:
					prixTxt= z[0].get_text()
					#print prixTxt

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	
	
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Generic
def check_GenericProductPriceCasComplexe_1(bsObj, site, classprice):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	ps=bsObj.find("div", {"class":classprice})
	
	if ps != None:

		
		prix = ps.find("span", {"class":"regular-price"})	
		if prix != None:
			prixValue = prix.find("span", {"class":"price"})
			prixTxt = prixValue.get_text()
			
			
		old_prix = ps.find("p", {"class":"old-price"})	
		if old_prix != None:
			old_prixValue = old_prix.find("span", {"class":"price"})
			old_prixValueTxt = old_prixValue.get_text()
		
		special_prix = ps.find("p", {"class":"special-price"})	
		if special_prix != None:
			special_prixValue = special_prix.find("span", {"class":"price"})
			special_prixValueTxt = special_prixValue.get_text()
			prixTxt = special_prixValueTxt 

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit type Collines de Provence
def check_GenericProductPriceCasComplexe_3(bsObj, site, classprice):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	ps=bsObj.find("div", {"class":classprice})
	
	if ps != None:

		
		prix = ps.find("span", {"class":"price"})	
		if prix != None:
			prixTxt = prix.get_text()
			
			
		old_prix = ps.find("p", {"class":"old-price"})	
		if old_prix != None:
			old_prixValue = old_prix.find("span", {"class":"price"})
			old_prixValueTxt = old_prixValue.get_text()
		
		special_prix = ps.find("p", {"class":"special-price"})	
		if special_prix != None:
			special_prixValue = special_prix.find("span", {"class":"price"})
			special_prixValueTxt = special_prixValue.get_text()
			prixTxt = special_prixValueTxt 

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# cherche le prix d'un produit type Collines de Provence
def check_GenericProductPriceMugler(bsObj, site, classprice):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	ps=bsObj.find("div", {"class":classprice})
	
	if ps != None:

		
		prix = ps.find("div", {"class":"price"})	
		if prix != None:
			prixTxt = prix.get_text()
			
		
		# Les lignes suivantes sont inutiles car je n'ai pas encore vu de soldes chez Mugler	
		#old_prix = ps.find("p", {"class":"old-price"})	
		#if old_prix != None:
			#old_prixValue = old_prix.find("span", {"class":"price"})
			#old_prixValueTxt = old_prixValue.get_text()
		
		#special_prix = ps.find("p", {"class":"special-price"})	
		#if special_prix != None:
			#special_prixValue = special_prix.find("span", {"class":"price"})
			#special_prixValueTxt = special_prixValue.get_text()
			#prixTxt = special_prixValueTxt 

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	

# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Scandles
def check_GenericProductPriceCasScandles(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Deux possibilites pour le prix affiche
	
	ps1=bsObj.find("div", {"itemprop":"offers"})	
	
	if ps1==None:
		ps1=bsObj.find("div", {"class":"single_variation"})
		
		
	
	if ps1 != None:
		
		ps = ps1.find("span", {"class":"amount"})
		if ps == None:
			ps = ps1.find("p", {"class":"price large"})			
		else:
			prixTxt = ps.get_text()
					
		#prix affiche - prix des soles
		prix = ps1.find("ins")	
		if prix != None:
			prixTxt = prix.get_text()
			
		#ancien prix	
		old_prix = ps1.find("del")	
		if old_prix != None:
			old_prixValueTxt = old_prix.get_text()			
			special_prixValueTxt = prixTxt

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)



# ---------------------------------------------------------------------------------
# cherche le prix d'un produit SynopsisParis
def check_GenericProductPriceCasSynopsisParis(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes	
	p = bsObj.find("div", {"class":"price-box"})
	if p!=None:
		prix = p.find("span", {"class":"regular-price"})	
		if prix!=None:
			prixTxt = prix.get_text()
			return(prixTxt, old_prixValueTxt, special_prixValueTxt)
		
		else:
			special_price = bsObj.find("p", {"class":"special-price"})	
			if special_price != None:
				special_prixValueTxt = special_price.get_text()
				prixTxt = special_prixValueTxt
				old_prix = bsObj.find("p", {"class":"old-price"})
				if old_prix != None:
					old_prixValueTxt = old_prix.get_text()
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit MiseEnScene
def check_GenericProductPriceCasMiseEnScene(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes	
	p = bsObj.find("div", {"class":"product-type-data"})
	if p!=None:
		prix = p.find("span", {"class":"regular-price"})	
		if prix!=None:
			prixTxt = prix.get_text()
			return(prixTxt, old_prixValueTxt, special_prixValueTxt)
		
		else:
			special_price = bsObj.find("p", {"class":"special-price"})	
			if special_price != None:
				special_prixValueTxt = special_price.get_text()
				prixTxt = special_prixValueTxt
				old_prix = bsObj.find("p", {"class":"old-price"})
				if old_prix != None:
					old_prixValueTxt = old_prix.get_text()
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Decos du Monde
def check_GenericProductPriceCasDecosDuMonde(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	prixBox = bsObj.find("div", {"class":"price-box"})	
	if prixBox!=None:
		prix = prixBox.find("span", {"class":"regular-price"})
		if prix!=None:
			prixTxt = prix.get_text()
			
		else:
			special_price = prixBox.find("p", {"class":"special-price"})	
				
			if special_price != None:
				special_prixValueTxt = special_price.get_text()
				prixTxt = special_prixValueTxt
		
			old_prix = prixBox.find("p", {"class":"old-price"})
			if old_prix != None:
				old_prixValueTxt = old_prix.get_text()
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Conran Shop
def check_GenericProductPriceCasConranShop(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	
	#Prix sans soldes
	prixBox = bsObj.find("div", {"id":"price-info-grouped"})	
	if prixBox!=None:
		prix = prixBox.find("span", {"class":"regular-price"})
		if prix!=None:
			prixTxt = prix.get_text()
			
		else:
			special_price = prixBox.find("p", {"class":"special-price"})	
				
			if special_price != None:
				special_prixValueTxt = special_price.get_text()
				prixTxt = special_prixValueTxt
		
			old_prix = prixBox.find("p", {"class":"old-price"})
			if old_prix != None:
				old_prixValueTxt = old_prix.get_text()
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)
	
	

# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Le Cedre Rouge
def check_GenericProductPriceLeCedreRouge(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	prixBox = bsObj.find("div", {"class":"price-box"})	
	if prixBox!=None:
		prix = prixBox.find("span", {"class":"special-price"})
		if prix!=None:
			prixTxt = prix.get_text()
			
		else:
			special_price = prixBox.find("span", {"class":"special-price"})	
				
			if special_price != None:
				special_prixValueTxt = special_price.get_text()
				prixTxt = special_prixValueTxt
		
			old_prix = prixBox.find("span", {"class":"old-price"})
			if old_prix != None:
				old_prixValueTxt = old_prix.get_text()
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)



# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Premiere Avenue
def check_GenericProductPricePremiereAvenue(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	prixBox = bsObj.find("p", {"class":"product__price"})	
	
	
	if prixBox!=None:
		
		special_price = prixBox.find("span", {"class":"price--new"})	
				
		if special_price != None:
			special_prixValueTxt = special_price.get_text()
			prixTxt = special_prixValueTxt
		
		old_prix = prixBox.find("span", {"class":"price--old"})
		if old_prix != None:
			old_prixValueTxt = old_prix.get_text()
		
		if special_price == None:
			prix = prixBox.find("span", {"itemprop":"price"})
			if prix!=None:
				prixTxt = prix.get_text()
					
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)





# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Jo Malone
def check_GenericProductPriceCasJoMalone(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	#Les prix sont sour la forme €80.00 200gr
	prix = bsObj.find("div", {"class":"sku_price"})	
	if prix!=None:
		prixTxtavecEuros = prix.get_text()
		prixTxtGroup = re.search("(\d)+((.)?|(,)?)(\d)+",prixTxtavecEuros)
		if prixTxtGroup != None:
			prixTxt = prixTxtGroup.group(0)
			old_prixValueTxt = prixTxt
			
	#Je n'ai pas encore vu de soldes
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)


# ---------------------------------------------------------------------------------
# cherche le prix Ines ...
def check_GenericProductPriceCasMetaItempropPrice(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	#Les prix sont sour la forme €80.00 200gr
	prix = bsObj.find("meta", {"itemprop":"price"})	
	if prix!=None:
		prixTxt = prix["content"]
		old_prixValueTxt = prixTxt
			
	#Je n'ai pas encore vu de soldes
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		


# ---------------------------------------------------------------------------------
# cherche le prix Fnac ...
def check_GenericProductPriceCasMetaItempropLowPrice(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	#Les prix sont sour la forme €80.00 200gr
	prix = bsObj.find("meta", {"itemprop":"lowPrice"})	
	if prix!=None:
		prixTxt = prix["content"]
		old_prixValueTxt = prixTxt
			
	#Je n'ai pas encore vu de soldes
		

	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		
	
	
	
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit og:price:amount
def check_GenericProductPriceCasOgPriceAmount(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	#Les prix sont sour la forme meta property og:price:amount	
	prix = bsObj.find("meta", {"property":"og:price:amount"})	
	if prix!=None:
		prixTxt = prix["content"]
		old_prixValueTxt = prixTxt
			
	#Je n'ai pas encore vu de soldes
	#Soldes pour lovethesign
	#Bidouille temporaire
	#print "site", site.categorie
	if site.categorie == "191":
		solde_prix = bsObj.find("li", {"class":"sconto"})	
		if solde_prix!=None:
			special_prixValueTxt = solde_prix.get_text()
		
	#Soldes pour farfetch
	#Bidouille temporaire
	#print "site", site.categorie
	if site.categorie == "192":
		solde_prix = bsObj.find("span", {"class":"strike"})	
		if solde_prix!=None:
			special_prixValueTxt = solde_prix.get_text()


	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Ma Joplie Bougie

def check_GenericProductPriceCasWooCommerce(bsObj, site):

	# price : Current product price. This is setted from regular_price and sale_price
	# sale_price : Product sale price
	# regular_price : Product regular price
	
	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	prix = bsObj.find("p", {"class":"price"})	
	if prix!=None:
		p = prix.find("span", {"class":"amount"})
		if p!=None:
			prixTxt = p.get_text()
			
		soldes=prix.find("del")		
		if soldes!=None:
			old_prixValueTxt = soldes.get_text()
			#JBS le 16/5/2016 mise en commentaires
			#special_prixValueTxt = old_prixValueTxt
			
		nouveauprix=prix.find("ins")
		if nouveauprix != None:	
			prixTxt = nouveauprix.get_text()
			#JBS le 16/5/2016 ajout
			special_prixValueTxt = prixTxt


	#print prixTxt, old_prixValueTxt, special_prixValueTxt
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		
	
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Fariboles
# JBS le 31/05/2016

def check_GenericProductPriceCasFariboles(bsObj, site):

	# price : Current product price. This is setted from regular_price and sale_price
	# sale_price : Product sale price
	# regular_price : Product regular price
	
	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	prix = bsObj.find("div", {"class":"tarif cellule"})	
	if prix!=None:
		p = prix.find("span", {"class":"prix"})
		if p!=None:
			prixTxt = p.get_text()
			
		#soldes=prix.find("del")		
		#if soldes!=None:
			#old_prixValueTxt = soldes.get_text()
			#JBS le 16/5/2016 mise en commentaires
			#special_prixValueTxt = old_prixValueTxt
			
		#nouveauprix=prix.find("ins")
		#if nouveauprix != None:	
			#prixTxt = nouveauprix.get_text()
			#JBS le 16/5/2016 ajout
			#special_prixValueTxt = prixTxt


	#print prixTxt, old_prixValueTxt, special_prixValueTxt
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		
	
	
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Ma Joplie Bougie

def check_GenericProductPriceCasNetAporter(bsObj, site):

	# price : Current product price. This is setted from regular_price and sale_price
	# sale_price : Product sale price
	# regular_price : Product regular price
	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	
	p = bsObj.find("nap-price")
	if p!=None:
		# j'enleve le link mais ce n'est pas obligatoire
		q = p.link.extract()
		s = p.attrs["price"]
		if len(s)!=0:
			d1=re.search("amount\":",s).end()
			d2=re.search("amount\":\d*",s).end()
			if (d1 !=0) and (d2!=0) and (d2>d1):
				n=s[d1:d2]
				n1=int(n)/100
				ns=str(n1)
				prixTxt = ns
			
	#PAS VU DE SOLDES 
	
	#print prixTxt, old_prixValueTxt, special_prixValueTxt
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Ma Joplie Bougie

def check_GenericProductPriceHypsoe(bsObj, site, classprice):

	# Le prix est scindé en une partie entière et une partie décimale
	# sale_price : Product sale price
	# regular_price : Product regular price
	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	
	p = bsObj.find("nap-price")
	if p!=None:
		# j'enleve le link mais ce n'est pas obligatoire
		q = p.link.extract()
		s = p.attrs["price"]
		if len(s)!=0:
			d1=re.search("amount\":",s).end()
			d2=re.search("amount\":\d*",s).end()
			if (d1 !=0) and (d2!=0) and (d2>d1):
				n=s[d1:d2]
				n1=int(n)/100
				ns=str(n1)
				prixTxt = ns
			
	#PAS VU DE SOLDES 
	
	#print prixTxt, old_prixValueTxt, special_prixValueTxt
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		


# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Nose

def check_GenericProductPriceNose(bsObj, site):

	# Le prix est scindé en une partie entière et une partie décimale
	# sale_price : Product sale price
	# regular_price : Product regular price

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	#Prix sans soldes
	#prix = bsObj.find("div", {"class":"price-box"})	
	prix = bsObj.find("ul", {"class":"productIds"})
	if prix!=None:
		p = prix.find("span", {"class":"price"})
		if p!=None:
			prixTxt = p.get_text()
			
		#soldes=prix.find("del")		
		#if soldes!=None:
			#old_prixValueTxt = soldes.get_text()
			#JBS le 16/5/2016 mise en commentaires
			#special_prixValueTxt = old_prixValueTxt
			
		#nouveauprix=prix.find("ins")
		#if nouveauprix != None:	
			#prixTxt = nouveauprix.get_text()
			#JBS le 16/5/2016 ajout
			#special_prixValueTxt = prixTxt


	#print prixTxt, old_prixValueTxt, special_prixValueTxt
	return(prixTxt, old_prixValueTxt, special_prixValueTxt)		


	
# ---------------------------------------------------------------------------------
# cherche le prix d'un produit Generic
def check_GenericProductPrice(bsObj, site):

	prixTxt = None
	old_prixValueTxt = None
	special_prixValueTxt = None
	
	par1 = site.check_GenericProductPriceNorma_par1
	if par1 == "D":
		return check_GenericProductPriceCasComplexe_1(bsObj, site, "product-shop")
		
	if par1 == "E":
		return check_GenericProductPriceCasComplexe_1(bsObj, site, "price-box")

	if par1 == "F":
		return check_GenericProductPriceCasComplexe_2(bsObj, site)	
		
	if par1 == "G":
		return check_GenericProductPriceCasComplexe_3(bsObj, site, "price-box")
		
	if par1 == "scandles":
		return check_GenericProductPriceCasScandles(bsObj, site)	
		
	if par1 == "synopsisparis":
		return check_GenericProductPriceCasSynopsisParis(bsObj, site)	
		
	if par1 == "decosdumonde":
		return check_GenericProductPriceCasDecosDuMonde(bsObj, site)
		
	if par1 == "conranshop":	
		return check_GenericProductPriceCasConranShop(bsObj, site)
		
	if par1 == "lecedrerouge":
		return check_GenericProductPriceLeCedreRouge(bsObj, site)
				
	if par1 == "jomalone":
		return check_GenericProductPriceCasJoMalone(bsObj, site)	

	if par1 == "metaitempropprice":
		return check_GenericProductPriceCasMetaItempropPrice(bsObj, site)
		
	if par1 == "metaitemproplowprice":
		return check_GenericProductPriceCasMetaItempropLowPrice(bsObj, site)

	if par1 == "ogpriceamount":
		return check_GenericProductPriceCasOgPriceAmount(bsObj, site)

	if par1 == "woocommerce":
		return check_GenericProductPriceCasWooCommerce(bsObj, site)
		
	if par1 == "fariboles":
		return check_GenericProductPriceCasFariboles(bsObj, site)
	
	if par1 == "net-a-porter":
		return check_GenericProductPriceCasNetAporter(bsObj, site)	
		
	if par1 == "mugler":	
		return check_GenericProductPriceMugler(bsObj, site, "pricing newPriceDisplay")
		
	if par1 == "hypsoe":	
		return check_GenericProductPriceHypsoe(bsObj, site, "")
	
	if par1 == "premiere-avenue":	
		return check_GenericProductPricePremiereAvenue(bsObj, site)
	
	if par1 == "mise-en-scene":	
		return check_GenericProductPriceCasMiseEnScene(bsObj, site)
				
	if par1 == "nose":	
		return check_GenericProductPriceNose(bsObj, site)

		
			
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
		
		#Modification JBS le 9/5/2016
		start=special_prixValueTxt.find('Au lieu de')
		if start >=0:
			special_prixValueTxt=special_prixValueTxt[start+10:len(special_prixValueTxt)]
		
		if old_prixValueTxt > special_prixValueTxt:
			x = old_prixValueTxt
			old_prixValueTxt = special_prixValueTxt
			special_prixValueTxt = x
			

				
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
		
		#Modification le 14/3/2016
		#Modification pour la Lumiere des Fees				
		#for x in description.findAll('span'):
			#new_tag = bsObj.new_tag("br")
			#if x.string != None:
				#str=x.string
				#new_tag.string = str
			#x.replace_with(new_tag)	
		
		#En remplacement des lignes precedentes	
		for x in description.findAll('span'):
			new_tag = bsObj.new_tag("br")
			
			for y in x.findAll('br'):
				new_new_tag = bsObj.new_tag("xxx")
				new_new_tag.string = "_CR_"
				y.insert_after(new_new_tag)
				
			s = x.get_text()
			if s!= "":			
				new_tag.string = s
			x.replace_with(new_tag)			
			
		for x in description.findAll('h3'):
			new_tag = bsObj.new_tag("br")
			if x.string != "":
				str="_CR_"
			else:
				str=x.string
			new_tag.string = str
			x.replace_with(new_tag)
		
		#Ajout JBS le 19/3/2016 
		for x in description.findAll('h4'):
			new_tag = bsObj.new_tag("br")
			if x.string != "":
				str="_CR_"
			else:
				str=x.string
			new_tag.string = str
			x.replace_with(new_tag)
			
				
		for x in description.findAll('p'):
			description.p.unwrap()

		#for x in description.findAll('div'):
			#description.div.unwrap()
		
		#Modification le 14/3/2016	
		for x in description.findAll('div'):
			new_tag = bsObj.new_tag("xxx")
			new_tag.string = "_CR_"
			x.insert_after(new_tag)
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
	

#------------------------------------------------------------------------------
# dryscrape permet de travailler sur des fichiers qui utlisent Javascript
# et dont le chargement complet de JS et requis avant de commencer l'analyse
# c'est le cas de Scandles
# Mais comme ça ralentit le traitement je ne l'utilise que lorsque c'est nécessaire
def doit_on_utiliser_dryscrape(site_etudie):
	#print "dryscrape ?"	
	if site_etudie.dryscrape == "0":
		return False
	else:	
		return True


#---------------------------------------------------------------------------------
def get_GenericProduct(bsObj, site_etudie_par, pageUrl):
	
	#Le Paramètre pageUrl ne semble pas être utilisé
	
	UpageUrl = site_etudie_par.url_etudiee
	Uparsed_url = urlparse(UpageUrl)
	netloc = Uparsed_url.netloc
	scheme = Uparsed_url.scheme
	
	#print "UpageUrl : ", UpageUrl
	#print "Uparsed_url : ", Uparsed_url
	#print  bsObj
	
	# Si c'est OK on retourne 1 sinon 0
	response = 0
		
	produit = check_GenericIsItAproduct(bsObj, site_etudie_par)				
	if produit != None: 
	
		#on teste si c'est une bougie
		nom_produit = give_GenericProductName(bsObj, produit, site_etudie_par)
		#print "Le nom du produit dans get_GenericProduct est : ", nom_produit
		
		if (nom_produit != "") & (nom_produit != None):
			#print(nom_produit)
			produit_actif.add_NomProduit(nom_produit)

			prix, old_price, special_price = check_GenericProductPrice(bsObj, site_etudie_par)	
			#print prix, old_price, special_price	
			if prix != None: 	
				produit_actif.add_PrixProduit(prix, old_price, special_price)		
				imgUrlSrc = give_GenericProductImgURL(bsObj, site_etudie_par)
				if imgUrlSrc != "":
					#print imgUrlSrc
					
					parsed_url = urlparse(imgUrlSrc)
					urlnetloc = parsed_url.netloc
					s = urlnetloc.strip()
					slash=""
					
					#Ajout JBS le 27/4/2016
					#p=parsed_url.path
					if s.find("/") <0:
						#Il faut ajouter /
						slash="/"
						
					if parsed_url.netloc == "":
						imgUrlSrc = scheme + "://" + netloc + slash + imgUrlSrc
						#Ajout le 30/3/2016
						parsed_url = urlparse(imgUrlSrc)
						
					#Ajout le 14/3/2016
					if parsed_url.scheme == "":
						imgUrlSrc = scheme + ":" + imgUrlSrc
					
					produit_actif.add_UrlImageProduit(imgUrlSrc)
					
					description=get_GenericProductDescription(bsObj, site_etudie_par)
					#JBS le 10/1/2017
					#Pour les pb d'encodage de Premiere Avenue
					#if site_etudie_par.categorie==108:
						#description=description.encode('latin-1')	
					
					
					#print description
					produit_actif.add_Description_Produit(description)
			
					response = 1

	return response