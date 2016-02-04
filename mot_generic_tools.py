# -*- coding: utf-8 -*-

#Dans l'ordre : cms, url_etudiee, url_format, catégorie
# check_GenericIsItAproduct_(par1..3)
# check_give_GenericProductName_(par1..3)
# check_give_give_GenericProductName_nom_produit (pour savoir si on fait un get_text ou autre chose)
# check_GenericProductPriceNorma_(par1..3)
# check_GenericProductPriceAvantSoldes_(par1..3)
# give_GenericProductImgURL_(par1..4)
# get_GenericProductDescription_(par1..4) si par4 ==1 alors str = description["content"], si par4==2 alors str = description.get_text()
# dryscrape (pour savoir si JS est requis)

listes_site = {}

listes_site["bougies-la-francaise"]="10","http://www.bougies-la-francaise.com/41-bougies-parfumees","www.bougies-la-francaise.com/", "24", "meta", "itemprop", "sku", "h1", "class", "title_product", "1", "span", "id", "our_price_display", "p", "id", "old_price", "span", "id", "view_full_size", "src", "meta", "name", "description", "1", "0"


listes_site["maisons-du-monde"]="10","http://www.maisonsdumonde.com/FR/fr/decoration/bougies-f7f933a233de5a794622944afd6d24b6.htm","\/FR\/fr\/produits\/fiche\/bougie", "25", "div", "class", "price", "h1", "class", "name-product", "1", "span", "class", "product-price", "span", "class", "old_price", "div", "class", "picture", "data-src", "div", "id", "description", "2", "0"


listes_site["rigaud"]="10","http://www.bougies-rigaud.com","\/", "26", "div", "class", "price", "h1", "class", "name-product", "1", "span", "class", "product-price", "span", "class", "old_price", "div", "class", "picture", "data-src", "div", "id", "description", "2", "0"


class Site:
	'Site en cours Analyse'
	def __init__(self):
		self.cms=""
		self.url_etudiee=None
		self.url_format = None
		self.categorie=None
		self.check_GenericIsItAproduct_par1=None
		self.check_GenericIsItAproduct_par2=None
		self.check_GenericIsItAproduct_par3=None
		self.check_give_GenericProductName_par1=None
		self.check_give_GenericProductName_par2=None
		self.check_give_GenericProductName_par3=None
		self.check_give_give_GenericProductName_nom_produit=0
		self.check_GenericProductPriceNorma_par1=None
		self.check_GenericProductPriceNorma_par2=None
		self.check_GenericProductPriceNorma_par3=None
		self.check_GenericProductPriceAvantSoldes_par1=None
		self.check_GenericProductPriceAvantSoldes_par2=None
		self.check_GenericProductPriceAvantSoldes_par3=None
		self.give_GenericProductImgURL_par1=None
		self.give_GenericProductImgURL_par2=None
		self.give_GenericProductImgURL_par3=None
		self.give_GenericProductImgURL_par4=None
		self.get_GenericProductDescription_par1=None
		self.get_GenericProductDescription_par2=None
		self.get_GenericProductDescription_par3=None
		self.get_GenericProductDescription_par4=None
		self.dryscrape=None
	

	def creation(self, site):
		self.cms=listes_site[site][0]
		self.url_etudiee=listes_site[site][1]
		self.url_format =listes_site[site][2]
		self.categorie=listes_site[site][3]		
		self.check_GenericIsItAproduct_par1=listes_site[site][4]	
		self.check_GenericIsItAproduct_par2=listes_site[site][5]	
		self.check_GenericIsItAproduct_par3=listes_site[site][6]	
		self.check_give_GenericProductName_par1=listes_site[site][7]	
		self.check_give_GenericProductName_par2=listes_site[site][8]	
		self.check_give_GenericProductName_par3=listes_site[site][9]	
		self.check_give_give_GenericProductName_nom_produit=listes_site[site][10]	
		self.check_GenericProductPriceNorma_par1=listes_site[site][11]	
		self.check_GenericProductPriceNorma_par2=listes_site[site][12]	
		self.check_GenericProductPriceNorma_par3=listes_site[site][13]	
		self.check_GenericProductPriceAvantSoldes_par1=listes_site[site][14]	
		self.check_GenericProductPriceAvantSoldes_par2=listes_site[site][15]	
		self.check_GenericProductPriceAvantSoldes_par3=listes_site[site][16]	
		self.give_GenericProductImgURL_par1=listes_site[site][17]	
		self.give_GenericProductImgURL_par2=listes_site[site][18]	
		self.give_GenericProductImgURL_par3=listes_site[site][19]	
		self.give_GenericProductImgURL_par4=listes_site[site][20]	
		self.get_GenericProductDescription_par1=listes_site[site][21]	
		self.get_GenericProductDescription_par2=listes_site[site][22]	
		self.get_GenericProductDescription_par3=listes_site[site][23]
		self.get_GenericProductDescription_par4=listes_site[site][24]	
		self.dryscrape=listes_site[site][25]

