# -*- coding: utf-8 -*-
#ligne du dessus pour avoir les accents dans les commentaires (et ailleurs)

from urlparse import urlparse
#la liste des pages		
pages = set()


#fonction qui teste si une chaine de caracteres peut etre consideree comme une bougie
#plusieurs mots à supprimer : voiture, batonnet, tartelette, scenterpiece...

def est_ce_une_bougie(item):
	marques_et_mots = ["rigaud","baobab","nimbus", "bahoma", "vranjes", "popup", "ecoya", "exclusifs", "panckoucke", "yankee candle", "jarre", "kerzon", "quintessence", "de nicola", "boule d'ambre", "boule de provence", "dl & co", "scandles", "note parisienne"]
	mots_interdits = ["voiture","batonnet","tartelette", "scenterpiece", "accessoire", "allume", "massage", "lumignon", "lanterne", "bougeoir", "cloche en", "cloche pour", "diffuseur", "parfum d'ambiance", "bulles de savon", "coupe-meche", "encens", "personnaliser", "anniversaire", "product_compare","flambeau", "led", "kit ", "coffret 12 bougies", "coffret 20 bougies", "4 bougies longues", "lot de 50 bougies", "photophore", "colle à bougie", "taille bougie", "sachet", "suspension", "100ml", "500ml", "500 ml", "1000ml", "vaporisateur", "camée", "ciseaux", "teignoir", "socle", "parfums bougies", "creer", "pot verre", "verre a bougie", "moule pour bougie", "pot de jardin", "parfum d’intérieur", "baume", "couvercle de", "pastille", "brule-parfum", "cire parfumee", "votive", "bougie colonne", "chauffe-plat", "12 bougies", "58x100", "78x200", "th arrondissement", "st arrondissement", "cierge", "10cm 50h", "15cm 75h", "20cm 125h", "15cm 25h", "25cm 40h", "decorative", "bougie ronde", "articielle", "stany de flamant", "elise de flamant", "brown sugar", "coffret 4 bougies", "coffret cuir + bougie", "coffret noir th", "magnolia en porcelaine", "bougie a led", "baume du tigre", "bougie led", "parfum d’intérieur", "tart parfum", "lumign", "non parfum", "dessous de bougie", "coffret bouquet royal", "recharge-boule", "calendrier", "jelly", "flamme artificielle", "stany de flamant",  "assiette", "rateur", "clip", "support jarre", "patere", "coupe a bougie", "rechaud", "fumeur", "spray", "scented", "galets"]
	
	for mot in mots_interdits:
		try:
			if item.lower().find(mot) >= 0:
				print "Mot interdit", mot
				return False
		except:
			#return False
			#print "mot illisible"
			kwz = 0
				

	if item.lower().find('bougie') >= 0:
		return True
	else:
		for marque in marques_et_mots:
			if item.lower().find(marque) >= 0:
				print "Marque"
				return True
				
	return False


# ----------------------------------------------------
def add_scheme_if_required(par_url, par_site):

	pageUrl = par_site.url_etudiee
	
	parsed_url = urlparse(pageUrl)
	g_netloc = parsed_url.netloc
	g_scheme = parsed_url.scheme
	
	url_etudiee = urlparse(par_url)
	if url_etudiee.netloc == "":
		url_retour = g_scheme + "://" + g_netloc + par_url	
	else:
		url_retour = par_url
			
	return par_url
	
	
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

#Joomla
#La Lumiere Des Fées : 22


# ----------------------------------------------------

#Prestashop 
#La Boite à Bougies : 42 
#Bougiz : 43
#Historiae : 44
#Geodesis : 45
#Papillon Rouge : 46
#Balamata : 47 

#fonction qui retourne le CMS de la page etudiée pour les sites connus
#parmi Magento Prestashop Woocommerce Drupal
#Magento 1
#PrestaShop 2
#WooCommerce Wordpress 3
#Joomla 4
#Magento Diptyque 5
#Magento Open Graph 6 lebonmarche
#Generic 9


def check_cms(pageUrl):

	#rang domaine cms
	#Durance : 0, 1, 32 (11 dans la nouvelle version)
	#Esteban : 1, 1, 34 (12 dans la nouvelle version)
	#Scandles 8, 3, 33
	#Yankee : 3, 1, 36 (13 http://www.bougies-parfums.fr/)
	#Diptyque Paris : 1, 14, 15 (15 dans la nouvelle version)
	#Comptoir de famille : 20, 1, 16 (16 dans la nouvelle version)
	#Synopsis Paris : 5, 1, 17 (17 dans la nouvelle version)
	#Decos du Monde : 19, 1, 18 (18 dans la nouvelle version)
	#Le Bon Marche : 17, 1, 19 (19 dans la nouvelle version)
	#Le Bon Marche : 18, 1, 20 (20 dans la nouvelle version)

	
	#La Boite à Bougies : 4, 2, 14 (14 dans la nouvelle version)
	#Bougiz : 11, 2, 43
	#Historiae : 7, 2, 44
	#Geodesis : 12, 2, 45
	#Papillon Rouge : 21, 2, 46
	#Balamata : 22, 2, 47 
	
	#Scandles : 8, 3, 21
	#L'Occitane : 23, 9, 23
	
	#La Lumiere Des Fées : 2, 4, 22
	#Bougies La Française : 24, 9, 24
	
	#Maisons du Monde : 25, 9, 25

	
	domain_liste = ["www.durance.fr", "www.esteban.fr", "lalumieredesfees.fr","www.bougies-parfums.fr","www.laboiteabougies.fr", "www.synopsisparis.com", "www.desfillesalavanille.com", "www.historiae.fr", "www.scandles.fr", "www.jewelcandle.fr", "www.kerzon.fr", 
	"www.bougiz.fr", "www.geodesis.com", "decobiance.pswebshop.com", "www.diptyqueparis.fr", "www.ambiancedelamaison.fr", "www.emoi-emoi.com", 
	"www.lebonmarche.com", "www.sia-homefashion.fr", "www.decosdumonde.com", "www.comptoir-de-famille.com", "papillonrougeparis.com", 
	"www.balamata.fr", "fr.loccitane.com", "www.bougies-la-francaise.com", "www.maisonsdumonde.com"]
	cms_liste = [1, 1, 4, 1, 2, 1, 1, 2, 3, 3, 3, 2, 2, 2, 5, 2, 1, 6, 1, 1, 1, 2, 2, 9, 9, 9]
	categorie_liste = [11, 12, 22, 13, 14, 17, 1, 44, 21, 3, 3, 43, 45, 2, 15, 2, 1, 19, 20, 18, 16, 46, 47, 23, 24, 25]

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
	
	