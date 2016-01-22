# -*- coding: utf-8 -*-
#ligne du dessus pour avoir les accents dans les commentaires (et ailleurs)

from urlparse import urlparse
#la liste des pages		
pages = set()


#fonction qui teste si une chaine de caracteres peut etre consideree comme une bougie
def est_ce_une_bougie(item):
	marques_et_mots = ["rigaud","baobab","nimbus"]
	
	if item.lower().find('bougie') >= 0:
		return True
	else:
			for marque in marques_et_mots:
				if item.lower().find(marque) >= 0:
					print "Marque"
					return True
	return False


# ----------------------------------------------------

#Magento 
#Durance : 32
#Esteban : 34
#Scandles : 33
#Diptyque Paris : 37
#Comptoir-de-famille : 38
#Synopsis Paris : 39
#Decos du Monde : 40
#Le Bon Marche : 41



# ----------------------------------------------------

#Prestashop 
#La Boite à Bougies : 42 
#Bougiz : 43
#Historiae : 44
#Geodesis : 45

#fonction qui retourne le CMS de la page etudiée pour les sites connus
#parmi Magento Prestashop Woocommerce Drupal
#Magento 1
#PrestaShop 2
#WooCommerce Wordpress 3
#Joomla 4
#Magento Diptyque 5
#Magento Open Graph 6 lebonmarche



def check_cms(pageUrl):

	#rang domaine cms
	#Durance : 0, 1, 32
	#Esteban : 1, 1, 34
	#Scandles 8, 3, 33
	#Yankee : 3, 1, 36 (http://www.bougies-parfums.fr/)
	#Diptyque Paris : 1, 14, 37
	#Comptoir de famille : 20, 1, 38
	#Synopsis Paris : 5, 1, 39
	#Decos du Monde : 19, 1, 40
	#Le Bon Marche : 17, 1, 41
	
	#La Boite à Bougies : 4, 2, 42
	#Bougiz : 11, 2, 43
	#Historiae : 7, 2, 44
	#Geodesis : 12, 2, 45
	
	domain_liste = ["www.durance.fr", "www.esteban.fr", "lalumieredesfees.fr","www.bougies-parfums.fr","www.laboiteabougies.fr", "www.synopsisparis.com", "www.desfillesalavanille.com", "www.historiae.fr", "www.scandles.fr", "www.jewelcandle.fr", "www.kerzon.fr", 
	"www.bougiz.fr", "www.geodesis.com", "decobiance.pswebshop.com", "www.diptyqueparis.fr", "www.ambiancedelamaison.fr", "www.emoi-emoi.com",
	"www.lebonmarche.com", "www.sia-homefashion.fr", "www.decosdumonde.com", "www.comptoir-de-famille.com"]
	cms_liste = [1, 1, 4, 1, 2, 1, 1, 2, 3, 3, 3, 2, 2, 2, 5, 2, 1, 6, 1, 1, 1]
	categorie_liste = [32, 34, 4, 36, 42, 39, 1, 44, 3, 3, 3, 43, 45, 2, 37, 2, 1, 41, 1, 40, 38]

	parsed_uri = urlparse(pageUrl)	
	check_in_list = parsed_uri.netloc in domain_liste
	
	cms = 0
	if check_in_list:
		position_cms = domain_liste.index(parsed_uri.netloc)
		cms = cms_liste[position_cms]
		categorie = categorie_liste[position_cms]

	return (cms, categorie)
#----------------------------------------------------------------------------------------------
#fonction qui verifie que la page produit  CMS Wordpress - Woocommerce est celle d une bougie	
def check_est_une_bougie_woocommerce(bsObj):
	check = False
	
	print "check_est_une_bougie_woocommerce"
	titre = bsObj.find("title")
	nom_titre = titre.get_text()
	if nom_titre.lower().find('bougie') >= 0:
		print titre
		check = True

	else:
		#On cherche dans h1 
		nom = bsObj.find("h1", {"itemprop":"name"})
		nom_produit = nom.get_text()
		
		if nom_produit.lower().find('bougie') >= 0:
			check = True
			
		#On cherche la categorie
		else:
			categorie_produit = bsObj.find("div", {"class":"product_category"})
			
			if categorie_produit != None:
				nom_categorie_produit = categorie_produit.get_text()
				
				if nom_categorie_produit.lower().find('bougie') >= 0:
					check = True
					
	if check == False:
		description = bsObj.find("div", {"itemprop":"description"})
		if description != None:
			nom_description = description.get_text()
			if nom_description.lower().find('bougie') >= 0:
				check = True
		
		
		
	return check
	
	

#----------------------------------------------------------------------------------------------
#fonction qui verifie que la page produit  CMS Magento
def check_est_une_bougie_Magento(bsObj):
	
	check = False
	print "check_est_une_bougie_Magento"
	#produit = bsObj.find("title")
	#nom_produit = produit.get_text()
	#if nom_produit.lower().find('bougie') >= 0:
		#print nom_produit	
		#check = True	
		
					
	nom = bsObj.find("title")
	if nom != None:
		nom_produit = nom.get_text()
		print "1er cas"
		print nom_produit
		if est_ce_une_bougie(nom_produit):
			check = True
			return check


	produit = bsObj.find("div", {"class":"product-shop details details-top"})
	if produit != None: 
		if produit.h3 != None:
			nom_produit = produit.h3.get_text()
			if est_ce_une_bougie(nom_produit):
				check = True
				return check
			
	categorie_produit = bsObj.find("li", {"class":"product-categorie"})
	if categorie_produit != None:
		nom_categorie_produit = nom.get_text()
		print "3eme cas"
		print nom_categorie_produit
		if est_ce_une_bougie(nom_categorie_produit):
			check = True
			return check
			
			
	return check
	
	