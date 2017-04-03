# -*- coding: utf-8 -*-

import requests
import re
import dryscrape
from bs4 import BeautifulSoup
from urlparse import urlparse
from check_cms import *
from url_accepted import *
from mot_get_product_data_generic_parameter import *
from enregistrement import *
#from tools_moteur import *
from mot_generic_tools import * 

import mysql.connector

#la liste des pages		
pages = set()
path_et_query = set()



#Pour Amazon 
#global amazon_first_qid
#amazon_first_qid = None


#------------------------------------------------------------------------------
# retourne_bsObj
#------------------------------------------------------------------------------
def retourne_bsObj(site_etudie, pageUrl, headers):
	
	bsObj = None
	#print "pageUrl dans retourne_bsObj", pageUrl
	
	if doit_on_utiliser_dryscrape(site_etudie):
		session = dryscrape.Session()
		try:
			session.visit(pageUrl)
			response = session.body()
			bsObj = BeautifulSoup(response)
		except:
			print "Erreur de lecture dans la session"
			return None
		
		
	else:	
		try:
			#print "Lecture de "
			#print pageUrl
			html = requests.get(pageUrl, headers=headers) 
			data = html.content
			
			#Cas particulier de Premiere Avenue
			# JBS le 11/1/2017
			print "Categorie : ", site_etudie.categorie
			if site_etudie.categorie=='108':
				print "Premiere Avenue"
				data = html.text
			
			bsObj = BeautifulSoup(data)	
			
		except:
			print "Erreur de lecture de la page"
			print pageUrl
			pages.add(pageUrl)
			return
	
	return(bsObj)


#------------------------------------------------------------------------------
# recherche_url_produit
#------------------------------------------------------------------------------

def recherche_url_produit(wcapi, numero_du_produit):

	# Tout d'abord on lit le produit dans la BdD
	x1="products/"
	y1=str(numero_du_produit)
	z1=x1+y1
	
	try:
		produit_dans_la_bdd=wcapi.get(z1).json()
	except:
		print "Erreur de lecture de la BDD en local"
		return
		
	try:
		description_produit_dans_la_bdd=produit_dans_la_bdd["product"]["description"]
		#print "Description : "
		#print description_produit_dans_la_bdd
	except:
		print "Erreur de lecture"
		return
	
	#il n'y a qu'une URL dans la description, celle du lien qui mène vers le produit	
	z=re.findall("<a href.*\"", description_produit_dans_la_bdd)
	q=z[0]

	# On récupère l'URL dans la description
	# L'URL est entre guillemets
	s=re.findall("\".*\"", q)
	t=s[0]
	# On supprime les guillemets
	url_produit_dans_la_bdd=t.replace("\"","")
	print "url_produit_dans_la_bdd : ", url_produit_dans_la_bdd
	
	return(url_produit_dans_la_bdd)



#------------------------------------------------------------------------------
# end_path_and_query
# prend que la derniere partie du path 
# ajoute query
#------------------------------------------------------------------------------

def end_path_and_query(u):

	o = urlparse(u)
	o_1 = o.path
	o_2 = o.query
		
	i=-1
	for m in re.finditer('/',o_1):
		i = m.end()
			
	if i!=-1:
		o_1=o_1[i:]
		
	if o_2 != '':
		st=o_1+'?'+o_2
	else:
		st=o_1

	return(st)
	
	
	

#------------------------------------------------------------------------------
# recherche_tous_produits_de_cette_categorie
#------------------------------------------------------------------------------

def recherche_tous_produits_de_cette_categorie(wcapi, categorie):

	global pages
	global path_et_query

	print "recherche_tous_produits_de_cette_categorie"
	
	# recheche de toutes les categories
	#print "categorie cherchee : ", categorie
	cnx = mysql.connector.connect(user='jboscher', password='JBSJBSjbs1', host='localhost', port='8889', database='bougies')
	cursor = cnx.cursor(buffered=True)
	
	x  = (wcapi.get("products/categories").json())
	#x['product_categories'][1]['count']
	#x['product_categories'][1]['id']
	#x['product_categories'][1]['slug']
	
	#recherche l'ID de cette categorie
	y=x['product_categories']
	longueur_list = len(y)
	i = 0
	id_categorie = 0
	
	while i < longueur_list:
		if y[i]['slug']==categorie:
				id_categorie = y[i]['id']
				break
		else:
			i=i+1

	#query = ("SELECT ID FROM wp_posts WHERE post_type='product' and post_status='publish' AND ID in (SELECT object_id FROM wp_term_relationships WHERE term_taxonomy_id in (%s) ) ")
	
	query="SELECT ID FROM wp_posts WHERE post_type='product' and post_status='publish' AND ID in (SELECT object_id FROM wp_term_relationships WHERE term_taxonomy_id in ("+str(id_categorie)+") )"
	
	print query
	
	#Recherche de tous les ID concernés dans un tuple
	cursor.execute(query)
	for (x) in cursor:
		#print x[0]
		u=recherche_url_produit(wcapi, x[0])
		pages.add(u)
		
		path_et_query.add(end_path_and_query(u))
				
	
	cnx.commit()
	cursor.close()
	cnx.close()
	
	#Affiche la liste
	print "Affichage de la liste en BDD "
	for (x) in pages:
		print x
	
	#for (x) in path_et_query:
		#print x
		
	return(id_categorie)

#------------------------------------------------------------------------------
# getLinksInit
#------------------------------------------------------------------------------


def getLinksInit(site):
	global global_regexes
	global global_cms
	global global_netloc
	global global_scheme
	global global_path
	
	print "getLinksInit"
	
	site_etudie = Site()
	site_etudie.creation(site)
	global_cms = cms = site_etudie.cms
	pageUrl = site_etudie.url_etudiee
	pageUrlFormat = site_etudie.url_format
	#print "pageUrlFormat", pageUrlFormat
	categorie = site_etudie.categorie
	print "categorie", categorie
	
		
	global_regexes = re.compile(pageUrlFormat)
	
	
	wcapi = initBDD()	
	#init_Global()
	print "wcapi", wcapi
	
	#wcapi2 = initBDDremote_2() pour la nlle version Woocommerce API REST
	wcapi2 = initBDDremote()
	print "wcapi2", wcapi2

	
	
	parsed_url = urlparse(pageUrl)
	global_netloc = parsed_url.netloc
	global_scheme = parsed_url.scheme
	global_path = parsed_url.path
	
	#On ajoute tous les liens déja en BdD
	#tous_produits_de_cette_categorie = recherche_tous_produits_de_cette_categorie(wcapi, site)


	
	print "pageUrl", pageUrl
	getLinks(pageUrl, wcapi, site_etudie)
	
	#liste_produits.print_ProduitListe()
	
	#Enregistrement dans la BDD
	# Enregistrement en local
	try:
		print "Enregistrement en local"
		liste_produits.store_ProduitListe(wcapi)
	except:
		print "Pb de stockage local"
	
	# Enregistrement en remote
	try:
		print "Enregistrement en remote"
		liste_produits.store_ProduitListe(wcapi2)
	except:
		print "Pb de stockage remote"
	
	# Reinit de la liste
	liste_produits.vide_ProduitListe()



#------------------------------------------------------------------------------
# getLinks
#------------------------------------------------------------------------------


#fonction qui prend en parametre une url et son type de CMS et ajoute les liens de la page a pages
def getLinks(pageUrl, wcapi, site_etudie):
	
	#REGARDER S'IL FAUT LA LIGNE CI-DESSOUS
	global pages
	#global amazon_nb_url_etudie 
	#global amazon_first_qid
	
	
	#Amazon
	#if site_etudie.categorie=="168":
	
		#if amazon_first_qid == None:
			#amazon_first_qid = get_amazon_first_qid(pageUrl)
			#print "Amazon_first_qid : "
			#print amazon_first_qid
	
		#else:
			#print ";;;;;;;;;;;"
			#print pageUrl
			#print "amazon_first_qid : "
			#print amazon_first_qid
			#pages.add(pageUrl)
			
			#pageUrl= keep_amazon_qid(pageUrl, amazon_first_qid)
			#print pageUrl
			#print ";---;;;;;;;"
	
	global path_et_query
	
			
	#Ajout le 1/4/2016
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
	
	#Changement JBS le 6/10/2016
	#print "Appel de retourne_bsObj"
	bsObj = retourne_bsObj(site_etudie, pageUrl, headers)
	#print "bsObj", bsObj
	
	#JBS le 17/11/2016
	if bsObj == None:
		print "Erreur de lecture"
		return
	
	#Pour l'Occitane (accents dans les url)
	#pageUrl = rem_accents(pageUrl)
	#
	
	#if doit_on_utiliser_dryscrape(site_etudie):
		#session = dryscrape.Session()
		#session.visit(pageUrl)
		#response = session.body()
		#bsObj = BeautifulSoup(response)
		
		
	#else:	
	#try:
		#print "Lecture de "
		#print pageUrl
		#html = requests.get(pageUrl, headers=headers) 
	#except:
		#print "Erreur de lecture de la page"
		#print pageUrl
		#pages.add(pageUrl)
		#return
	
	# http://stackoverflow.com/questions/25483726/python-encoding-error-not-unicode-string
	# auparavant je faisais data = html.text
	# ce qui entrainait des problèmes avec les accents
	#data = html.content
	#cette page est transformee en objet bs4
	#bsObj = BeautifulSoup(data)	
	
	#Ajout JBS le 25/3/2016
	for x in bsObj.findAll('script'):
		bsObj.script.extract()
	for x in bsObj.findAll('noscript'):
		bsObj.noscript.extract()
	
	#print bsObj
	#getproductData(bsObj, global_cms)
	#print bsObj
	
	#print "get_GenericProduct"
	get_GenericProduct(bsObj, site_etudie, pageUrl)
	
	
	produit_actif.add_UrlProduit(pageUrl)
	
	categorie=site_etudie.categorie
	produit_actif.add_Categorie_Produit(categorie)
	#produit_actif.printProduit()
	storeProduitActif(wcapi, categorie)
		
	produit_actif.reinit()
	
	links = bsObj.findAll("a", href=global_regexes)
	#print links
                                   
	for link in bsObj.findAll("a", href=global_regexes):
		#print "Link : ", link
		#si c'est un lien
		if 'href' in link.attrs:
			#si le lien n'a pas ete traite
			#print "Lien en etude :"
			#print link

			
			v = end_path_and_query(link.attrs['href'])
			#print "v : ", v
			
			if (link.attrs['href'] not in pages) and (v not in path_et_query) :
			#We have encountered a new page
				
				#print "We have encountered a new page"
				newPage = link.attrs['href'] 
				pages.add(newPage) 
				print "ADD : "
				print newPage
				
				#JBS le 30/3/2016 - cas particulier des URL qui commencent par ../
				#JBS le 20/4/2016
				#newPage=re.sub('^../','',newPage)
				newPage=re.sub('^\.\./','',newPage)

				
				#Pour la lumiere des fees car les URL ne sont pas completes
				parsed_url = urlparse(newPage)
				
				#Ajout JBS le 25/3/2016
				urlnetloc = parsed_url.netloc
				s = urlnetloc.strip()
				
				#Ajout JBS le 27/4/2016
				p=parsed_url.path
				
				slash=""
				#Ajout JBS le 27/4/2016
				if (s.find("/") <0) and (p.find("/") !=0):
					#Il faut ajouter /
					slash="/"
					
				#Ajout JBS le 25/3/2016
				if (urlnetloc != "") and (urlnetloc != global_netloc):
					pages.add(newPage)
					#print "ADD 2 : "
					#print newPage
					#print urlnetloc
					#print "different de : "
					#print global_netloc
					#print "Ignore "
					return	
				
				if urlnetloc == "":
				
					#Cas particulier de le-joli-shop
					if site_etudie.categorie=="180":
						newPage = site_etudie.url_etudiee + newPage	
						pages.add(newPage)
						print "Cas joli-shop : ", newPage
						
					else:
						# Rose et Marius (43)
						# Je n'aime pas trop faire ça mais je ne vois pas comment résoudre le pb (qui n'existait pas auparavant)
						# Wait and see
						# JBS le 16/3/2017
						if site_etudie.categorie=="43":
							newPage = global_scheme + "://" + global_netloc + slash + "creation-coffret" + newPage	
							pages.add(newPage)
						
						else:
							newPage = global_scheme + "://" + global_netloc + slash + newPage
							pages.add(newPage)
							#print "ADD 3 : "
							#print newPage
					
					
				#on verifie que les mots interdits ne sont pas presents dans l url
				if url_accepted(newPage): 
					print "URL accepted : "
					print newPage
					getLinks(newPage, wcapi, site_etudie)
				else:
					print "URL refusee : "
					print newPage

