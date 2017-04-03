# -*- coding: utf-8 -*-

#Dans l'ordre : cms, url_etudiee, url_format, catégorie
# check_GenericIsItAproduct_(par1..3)

# Le nom du produit a 3 paramètres de décision + 1
# check_give_GenericProductName_(par1..3) si par1 == gettext 0 0 0 alors gettext()
# check_give_give_GenericProductName_nom_produit (pour savoir si on fait un get_text (1) ou autre chose)

# check_GenericProductPriceNorma_(par1..3)
# check_GenericProductPriceAvantSoldes_(par1..3)

# give_GenericProductImgURL_(par1..4)
# get_GenericProductDescription_(par1..4) si par4 ==1 alors str = description["content"], si par4==2 alors str = description.get_text()
# dryscrape (pour savoir si JS est requis) si 1 alors requis

listes_site = {}

listes_site["bougies-la-francaise"]="10","https://www.bougies-la-francaise.com/41-bougies-parfumees?controllerUri=category&id_category=41&n=45","bougie.*-parfumee.*html|bougies-parfumees\?", "24", "meta", "property", "og:type", "h1", "class", "product-name", "1", "span", "id", "our_price_display", "p", "id", "old_price", "span", "id", "view_full_size", "src", "meta", "name", "description", "1", "0"

listes_site["maisons-du-monde"]="10","http://www.maisonsdumonde.com/FR/fr/decoration/bougies-f7f933a233de5a794622944afd6d24b6.htm","bougie", "25", "div", "class", "price", "h1", "class", "name-product", "1", "span", "class", "product-price", "span", "class", "old_price", "img", "class", "picture-img", "data-src", "div", "id", "description", "2", "0"

listes_site["durance"]= "10", "https://www.durance.fr/bougies-parfumees.html?limit=all", "www.durance.fr\/.*(bougie-parfumee|bougies-parfumees)", "11", "li", "class", "product", "gettext", "0", "0", "1", "D", "D", "D", "D", "D", "D", "div", "class", "product-image-gallery", "src", "div", "class", "boxProductViewDescription", "2", "0"

listes_site["esteban"]= "10", "http://www.esteban.fr/fr/parfums-interieur/produits/bougies-parfumees.html?limit=all", "bougie-|p=2$", "12", "li", "class", "product", "title", "", "", "1", "D", "D", "D", "D", "D", "D", "p", "class", "main-product-img", "href", "div", "class", "std", "2", "0"

listes_site["la-lumiere-des-fees"]="10","http://lalumieredesfees.fr/bougie/bougies-artisanales-vegetales","\/bougie", "22", "div", "id", "hikashop_product_right_part", "title", "", "", "1", "span", "class", "hikashop_product_price", "span", "class", "hikashop_product_price_before_discount", "meta", "property", "og:image", "content", "div", "id", "description", "2", "0"

listes_site["la-boite-a-bougies"]= "10", "http://www.laboiteabougies.fr/search?search_query=bougie+parfumée&orderby=position&orderway=desc&submit_search=&n=1000", "bougie-parfumee", "14", "body", "id", "product", "title", "", "", "1", "span", "id", "our_price_display", "p", "id", "old_price", "img", "id", "bigpic", "imagesrc", "div", "class", "rte", "2", "0"

listes_site["diptyqueparis"]= "10", "http://www.diptyqueparis.fr/home-fragrances.html", "(.*bougie)|(.*candle)", "15", "div", "class", "product-shop details details-top", "title", "", "", "1", "F", "F", "F", "F", "F", "F", "img", "id", "large-image", "imagesrc", "div", "class", "tabs-cnt", "2", "0"

listes_site["comptoir-de-famille"]= "10", "http://www.comptoir-de-famille.com/fr/senteurs/notre-offre/bougies.html", "www.comptoir-de-famille.com\/fr\/senteurs\/notre-offre\/bougies\/[a-zA-Z0-9_\-]*.html", "16", "li", "class", "product", "gettext", "0", "0", "1", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "div", "class", "product-img-box", "href", "div", "class", "std", "2", "0"

listes_site["synopsisparis"]= "10", "http://www.synopsisparis.com/", "synopsisparis.com\/fr_fr\/.*bougie", "17", "li", "class", "product", "gettext", "0", "0", "1", "synopsisparis", "synopsisparis", "synopsisparis", "synopsisparis", "synopsisparis", "synopsisparis", "div", "class", "product-img-box", "src", "div", "class", "std", "2", "0"

listes_site["decosdumonde"]= "10", "http://www.decosdumonde.com/bougies-parfumees.html", "www.decosdumonde.com\/bougie", "18", "li", "class", "product", "gettext", "0", "0", "1", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "div", "class", "product-img-box", "src", "div", "class", "std", "2", "0"

listes_site["sia"]= "10", "https://www.sia-deco.fr/sc/%7B|f|:%7B|cat|:%5B|19|,|20|,|21|%5D,|t|:%5B|20|%5D%7D%7D", "bougie-parfumee", "20", "body", "class", "product", "meta", "property", "og:title", "0", "div", "class", "col-xs-12 col-md-6 col-md-push-3 title-container", "span", "class", "price color-red", "meta", "property", "og:image", "content", "div", "class", "responsive-list attributes-items", "2", "0"

listes_site["le-bon-marche"]= "10", "http://www.lebonmarche.com/catalogue/maison/bougies-et-parfums-d-interieur.html", "(\/produit\/)|(p=)", "19", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "class", "actuel", "pasdesoldes", "pasdesoldes", "pasdesoldes", "div", "class", "large", "image_a_img_src", "p", "id", "product-description", "2", "0"

listes_site["historiae"]= "10", "http://www.historiae.fr/fr/11-bougies-parfumees", "bougie|coffret", "28", "body", "id", "product", "h1", "class", "productTitle", "1", "p", "class", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["ebougie"]= "10", "http://www.ebougie.fr/", "http:\/\/www.ebougie.fr\/", "29", "body", "id", "product", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "span", "id", "view_full_size", "src", "div", "id", "short_description_content", "2", "0"

listes_site["saltcity"]= "10", "http://www.bougiesaltcity.fr/", "http:\/\/www.bougiesaltcity.fr\/", "30", "span", "id", "our_price_display", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "span", "id", "view_full_size", "src", "div", "id", "short_description_content", "2", "0"

listes_site["amara"]= "10", "https://fr.amara.com/boutique/bougies-parfumees-1", "(https:\/\/fr.amara.com\/produits\/.*bougie)|(^\/produits\/.*bougie)", "32", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "data-is-product-price", "1", "strong", "class", " product-main-price old", "meta", "property", "og:image", "content", "div", "id", "info", "2", "0"

listes_site["archipel-parfums"]= "10", "http://www.archipelparfums.com/31-bougies-parfumees", ".*bougie", "33", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "meta", "property", "og:description", "1", "0"

listes_site["guerlain"]= "10", "http://www.guerlain.com/fr/fr-fr/les-collections-exclusives/les-parfums-dinterieur", "\/fr\/fr-fr\/les-collections-exclusives\/les-parfums-dinterieur", "34", "span", "itemprop", "price", "h1", "itemprop", "name", "1", "span", "itemprop", "price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "itemprop", "image", "imagesrc", "p", "itemprop", "description", "2", "0"

listes_site["la-belle-meche"]= "10", "http://www.labellemeche.com/fr/4-bougies-parfumees", "http:\/\/www.labellemeche.com\/fr\/bougies-parfumees", "35", "body", "id", "product", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "content", "meta", "property", "og:description", "1", "0"

listes_site["leon-panckoucke"]= "10", "http://www.leonpanckoucke.com", "(\d)+(.)*html$", "36", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "content", "div", "id", "product-description-tab-content", "2", "0"

listes_site["nature-et-decouvertes"]= "10", "http://www.natureetdecouvertes.com/deco-maison/parfums-interieur/bougies-parfumees", "bougie-parfumee|bougies-parfumees", "37", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "class", "product-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "itemprop", "image", "imagesrc", "div", "class", "product-description-wrapper", "2", "0"

listes_site["galeries-lafayette"]= "10", "http://www.galerieslafayette.com/c/maison/f/bougies+parfumees", "bougie\+parfumee|bougies\+parfumees", "38", "span", "id", "current-price", "meta", "property", "og:title", "0", "span", "id", "current-price", "del", "id", "old-price", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["bougies-shop"]= "10", "https://www.bougiesshop.com/6-bougies-parfumees", "bougie-parfumee", "39", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["hypsoe"]= "10", "http://www.hypsoe.fr/bougies-parfumees-c33.html", "bougie.*-", "40", "div", "class", "liste_produit-prix-normal", "meta", "property", "og:title", "0", "div", "class", "liste_produit-prix-normal", "pasdesoldes", "pasdesoldes", "pasdesoldes", "span", "itemprop", "image", "og", "meta", "property", "og:description", "1", "0"

listes_site["delyss"]= "10", "http://www.delyss.com/fr/bougies/bougies-parfumees.html", "(\/fr\/.*bougie-.*html$)|(bougies-parfumees.*p=)", "42", "meta", "property", "og:type", "meta", "property", "og:title", "0", "D", "class", "regular-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "div", "class", "easyzoom", "image_a_img_src", "div", "class", "wrap_for_mob", "2", "0"

listes_site["rose-et-marius"]= "10", "https://www.roseetmarius.com/fr/creation-coffret?add=1", "step=2.*tid=.*add=.*", "43", "span", "id", "our_price_display", "span", "itemprop", "name", "1", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "1"

listes_site["geodesis"]= "10", "http://www.geodesis.com/fr/46-bougies", "www.geodesis.com\/fr", "45", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["v-inc"]= "10", "https://www.v-inc.fr/fr/recherche?search_query=bougie&orderby=position&orderway=desc&n=60", "v-inc.fr\/fr\/.*(yankee|bougie|candleberry|40|19)", "86", "meta", "property", "og:type", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "idTab1", "2", "0"

listes_site["memento-mori"]= "10", "http://www.mementomori-shop.com/64-bougies", "www.mementomori-shop.com\/(parfumer\/|bougies\/)", "87", "body", "id", "product", "title", "", "", "1", "span", "class", "our_price_display", "p", "id", "old_price", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["laduree"]= "10", "https://beaute.laduree.com/fr_fr/boutique/bougies/toutes?limit=all", "bougie-", "89", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "class", "regular-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "div", "id", "visuel", "src", "div", "class", "description_produit", "2", "0"

listes_site["yssia"]= "10", "http://www.yssia.fr/12-bougies-parfumees-naturelles?id_category=12&n=100", "bougie-parfumee|bougies-parfumees", "90", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["spirit-opus"]= "10", "http://www.spiritopus.com/fr/36-toutes-les-bougies-parfumees", "bougie-parfumee", "91", "body", "id", "product", "span", "itemprop", "name", "1", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "bigpic", "imagesrc", "div", "class", "reference", "2", "0"

listes_site["le-bazaristain"]= "10", "http://www.lebazaristain.com/bougie-c102x2479949", "bougie-|candle-", "92", "meta", "itemprop", "price", "h1", "itemprop", "name", "1", "span", "class", "PBSalesPrice", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "name", "description", "1", "0"

listes_site["candle-lite"]= "10", "http://www.candle-lite.fr/index.php?id_category=6&controller=category&n=30", "id_product|bougie", "93", "meta", "property", "og:type", "meta", "property", "og:title", "0", "p", "class", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["the-beautyst"]= "10", "http://fr.thebeautyst.com/bien-etre/bougie.html", "(bougie|jarre).*html$", "94", "meta", "property", "og:type", "meta", "property", "og:title", "0", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "decosdumonde", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["la-note-parisienne"]= "10", "http://www.lanoteparisienne.com/fr/6-collections", "arrondissement|collection", "97", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", " old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "idTab1", "2", "0"

listes_site["nose"]= "10", "http://nose.fr/fr/marques/maison", "http:\/\/nose.fr\/fr\/marques\/(astier-de-villatte|birch-brook|carriere-freres|cire-trudon|linari|lorenzo-villoresi|maison-francis-kurkdjian|maison-martin-margiela|malin-goetz|odin|penhaligon-s|diptyque|l-artisan-parfumeur)", "99", "span", "class", "price", "div", "class", "product-name", "1", "span", "class", "price", "pasdesoldes", "pasdesoldes", " pasdesoldes", "div", "class", "slideshow", "src", "div", "class", "accontent", "2", "0"

listes_site["ma-jolie-bougie"]= "10", "http://www.majoliebougie.com/14-bougie-parfumee?id_category=14&n=180", "\.html$|-bougie-parfumee", "100", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["l-artisan-parfumeur"]= "10", "http://www.artisanparfumeur.fr/shop/bougies-et-parfum-maison.html", "bougie", "101", "span", "class", "value", "title", "", "", "1", "span", "class", "price", "pasdesoldes", "pasdesoldes", " pasdesoldes", "span", "class", "image_url", "gettxt", "div", "class", "snippet", "2", "0"

listes_site["rive-sud-interior"]= "10", "http://www.rivesudinterior.com", "http:\/\/www.rivesudinterior.com", "102", "span", "class", "prix", "title", "", "", "1", "span", "class", "prix", "pasdesoldes", "pasdesoldes", " pasdesoldes", "section", "class", "visuel", "src", "p", "class", "big", "2", "0"

listes_site["l-art-ose"]= "10", "http://lart-ose.fr/categorie-produit/bougies-parfumees/", "produit", "104", "meta", "itemprop", "price", "meta", "property", "og:description", "0", "metaitempropprice", "metaitempropprice", "metaitempropprice", "pasdesoldes", "pasdesoldes", " pasdesoldes", "meta", "property", "og:image", "og", "div", "itemprop", "description", "2", "0"

listes_site["la-redoute"]= "10", "http://www.laredoute.fr/psrch/psrch.aspx?kwrd=bougies+parfumees&virtualsite=100", "prod-50|bougie", "105", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "itemprop", "price", "span", "class", "sale-price-before", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["premiere-avenue"]= "10", "https://shopping-premiereavenue.com/index.php?mod=recherche&search_query=&lang=fr", "(acqua|diptyque|comme|culti|mad-et|frederic|annick-goutal|lm-parfum|mizensir|onno|bernardaud|baobab).*fr.*html", "108", "h2", "id", "desc-du-produit", "span", "class", "bold-desc", "1", "premiere-avenue", "premiere-avenue", "premiere-avenue", "premiere-avenue", "premiere-avenue", "premiere-avenue", "div", "id", "bloc_produit_photo_principale", "src", "p", "id", "description_prod", "2", "0"

listes_site["elysees-parfums"]= "10", "http://www.elysees-parfums.fr/105-bougies", "bougie", "114", "meta", "property", "og:type", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["mise-en-scene"]= "10", "http://www.mise-en-scene.com/catalogue/deco/bougies/show/96.html", "(bougie-baobab|bougies.*page).*html", "116", "span", "class", "price", "title", "", "", "1", "mise-en-scene", "mise-en-scene", "mise-en-scene", "mise-en-scene", "mise-en-scene", "mise-en-scene", "a", "id", "zoom1", "nextimg", "div", "id", "mesProdDesc", "2", "0"

listes_site["epicuriens-de-france"]= "10", "http://www.epicuriensdefrance.com/Bougies-Bougies-photophores-et-parfums-d-interieur-Art-et-Art-de-vivre/p/3/2312/0/", ".*(Bougie|.*Rigaud|.*Laduree)", "117", "span", "id", "price", "title", "", "", "1", "span", "id", "price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "main-picture", "imagesrc", "div", "class", "em-description", "2", "0"

listes_site["prodige"]= "10", "http://prodige.eu/Boutique/fr/13-bougie-parfumee", "bougie", "118", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["memo-paris"]= "10", "http://www.memoparis.com/fr/10-bougies-parfumees", "memoparis.com\/fr\/bougie.*", "119", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "class", "olfactive-pyramid", "2", "0"

listes_site["compagnie-de-provence"]= "10", "http://www.compagniedeprovence.com/fr/41-bougies-parfumees", "bougie", "121", "span", "id", "our_price_display", "h1", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "idTab1001", "2", "0"

listes_site["mathilde-m"]= "10", "http://www.mathilde-m.com/fr/boutique/catalogue/MPBPBO-bougies-parfumees#form_catalogue_l", "bougie.*-parfumee", "122", "p", "class", "prix", "title", "", "", "1", "p", "class", "prix", "pasdesoldes", "pasdesoldes", "pasdesoldes", "a", "rel", "shadowbox[produit]", "nextimg", "p", "class", "description", "2", "0"

listes_site["palais-des-bougies"]= "10", "https://www.palaisdesbougies.com/recherche", "palaisdesbougies.com/.*bougie", "124", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "class", "product-description_short", "2", "0"

listes_site["rituals"]= "10", "https://eu.rituals.com/fr-fr/pour-la-maison/bougies/", "fr-fr.*-(\d+).*html", "125", "span", "class", "price-sales", "title", "", "", "1", "span", "class", "price-sales", "span", "class", "price-standard", "img", "class", "primary-image", "imagesrc", "div", "itemprop", "description", "2", "0"

listes_site["dior"]= "10", "http://www.dior.com/beauty/fr_fr/parfum-beaute/parfum/parfums-dexception/les-bougies-de-la-collection-privee-christian-dior/fr-cpcdcandles-lesbougiesdelacollectionprivéechristiandior.html", "bougie", "127", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "class", "details-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "class", "block-fp--text", "2", "0"


listes_site["ma-bougie-et-moi"]= "10", "http://www.mabougieetmoi.com/?s=bougie&post_type=product", "http:\/\/www\.mabougieetmoi\.com\/.*(bougie|bonbonniere)", "128", "meta", "property", "og:type", "meta", "property", "og:title", "0", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "div", "class", "featured_img_temp", "src", "meta", "property", "og:description", "1", "0"

listes_site["kerzon"]= "10", "http://www.kerzon.paris/categorie-produit/bougies-parfumees/", "bougies-parfumees", "130", "meta", "property", "og:type", "meta", "property", "og:title", "0", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "meta", "property", "og:image", "og", "div", "itemprop", "description", "2", "0"

listes_site["hermes"]= "10", "http://france.hermes.com/catalogsearch/result/get?q=bougie", "france.hermes.com\/parfums\/parfum-de-la-maison\/.*bougie", "132", "meta", "property", "og:type", "title", "", "", "1", "span", "class", "regular-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["balamata"]= "10", "http://www.balamata.fr/fr/13-bougies-parfumees?id_category=13&n=40", "www.balamata.fr\/fr\/bougies-parfumees\/.*bougie-parfume", "142", "span", "id", "our_price_display", "h1", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_block", "2", "0"

listes_site["quintessence"]= "10", "http://quintessence-paris.com/category/bougie-particuliere/", "product|bougie|boutique\/page", "146", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "class", "price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "class", "accordion_content ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom", "2", "0"

listes_site["ines-de-nicolay"]= "10", "http://inesdenicolay.com/bougies-parfumees/", "bougie", "150", "meta", "itemprop", "price", "meta", "property", "og:title", "0", "metaitempropprice", "metaitempropprice", "metaitempropprice", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["ejea"]= "10", "http://www.ejea.fr/1128-bougies-et-galets-heart-home-", "(\d+).*bougie.*html", "156", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["senteurs-d-interieur"]= "10", "https://www.senteurs-interieur.fr/5-bougies-parfumees", "", "158", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "class", "rte", "2", "0"

listes_site["marschalle"]= "10", "http://www.marschalle.fr/35-bougies-parfumees", "bougie-naturel|bougie-par|bougies-par", "163", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["fnac"]= "10", "http://www.fnac.com/Bougies-parfumees/Bougies-et-senteurs/nsh377764/w-4#int=S:Par%20cat%C3%A9gorie|Bougies%20&%20senteurs|377764|NonApplicable|BL1|NonApplicable", "Bougies-parfumees|Bougie-.arfumee", "166", "meta", "property", "og:type", "span", "itemprop", "name", "1", "metaitemproplowprice", "metaitemproplowprice", "metaitemproplowprice", "metaitemproplowprice", "metaitemproplowprice", "metaitemproplowprice", "img", "class", "js-ProductVisuals-imagePreview", "imagesrc", "div", "class", "whiteContent", "2", "0"

listes_site["bzh-bougies"]= "10", "http://www.bzh-bougies.fr/s/bougie-parfumee/", "bougies-parfumees", "171", "span", "itemprop", "price", "p", "id", "prod-summary", "1", "span", "itemprop", "price", "span", "class", "price-old", "meta", "property", "og:image", "og", "p", "itemprop", "description", "2", "0"

listes_site["blanc-d-ivoire"]= "10", "http://www.blancdivoire.com/fr/272-senteurs-", "bougie", "173", "span", "id", "our_price_display", "div", "id", "short_description_content", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "more_info_sheets", "2", "0"

listes_site["fariboles"]= "10", "http://www.fariboles.com/fr/30_1.cfm?f=60-bougie-parfumee-paillette-message-senteur", "bougie", "174", "div", "class", "tarif", "h1", "class", "nom_produit", "1", "fariboles", "fariboles", "fariboles", "fariboles", "fariboles", "fariboles", "img", "id", "imagev1", "imagesrc", "div", "class", "cellule bloc_description", "2", "0"

listes_site["ambiance-de-la-maison"]= "10", "http://www.ambiancedelamaison.fr/3-bougies-parfumees", "grande|petite|moyenne|cylindre", "175", "meta", "property", "og:type", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["phaedon"]= "10", "http://www.phaedonparis.com/bougies-parfumees-maison.html", "bougie|page=", "176", "p", "class", "pxpdt", "h1", "itemprop", "name", "1", "p", "class", "pxpdt", "pasdesoldes", "pasdesoldes", "pasdesoldes", "figure", "", "", "src", "section", "itemprop", "description", "2", "0"

listes_site["oliria"]= "10", "http://www.oliria.fr/index.php", "", "178", "td", "class", "fiche_prix", "td", "class", "fiche_titre", "1", "td", "class", "fiche_prix", "span", "class", "fiche_prix_barre", "div", "id", "fiche_photo_face", "nextimg", "td", "class", "fiche_desc", "2", "0"

listes_site["camif"]= "10", "http://www.camif.fr/decoration/bougies-savons-et-senteurs/bougies.html", "bougie-parfumee|bougie-esprit", "179", "meta", "property", "og:type", "meta", "property", "og:title", "0", "ogpriceamount", "ogpriceamount", "ogpriceamount", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "content", "meta", "name", "description", "1", "0"

listes_site["le-joli-shop"]= "10", "http://www.lejoli-shop.com/bougies/toutes-les-bougies-senteurs/", "bougie-|page", "180", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "class", "prod-price", "span", "class", "prod-special-price", "meta", "property", "og:image", "content", "meta", "property", "og:description", "1", "0"

listes_site["les-sens-du-monde"]= "10", "http://www.lessensdumonde.com/bougies-parfumees.htm", "bougie|page", "183", "span", "class", "PBSalesPrice", "h1", "itemprop", "name", "1", "span", "class", "PBSalesPrice", "div", "class", "PBStrike", "meta", "property", "og:image", "content", "ol", "", "", "2", "0"

listes_site["cfoc"]= "10", "http://www.cfoc.fr/124-bougies-parfumees?n=100", "bougies-parfumees", "185", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "class", "rte", "2", "0"

listes_site["tendances-du-monde"]= "10", "http://www.tendances-du-monde.fr/bougies-parfumees-c102x2920232", "bougie|page", "186", "span", "class", "PBSalesPrice", "h1", "class", "PBItemTitle", "1", "span", "class", "PBSalesPrice", "div", "class", "PBStrike", "meta", "property", "og:image", "content", "span", "itemprop", "description", "2", "0"

listes_site["costes"]= "10", "http://shop.hotelcostes.com/fr/10-bougies-parfumees", "bougie-|page", "188", "span", "id", "our_price_display p-price", "meta", "property", "og:title", "2", "span", "id", "our_price_display p-price", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "itemprop", "description", "2", "0"

listes_site["bleujaune"]= "10", "http://bleujaune.com/15-bougies-parfumees", "bougie-|page", "189", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "class", "rte", "2", "0"

listes_site["lovethesign"]= "10", "http://www.lovethesign.com/fr/listing/accessoires-maison/bougies-et-bougeoirs#", "bougie-|page", "191", "span", "class", "price", "meta", "property", "og:title", "2", "span", "class", "price", "span", "class", "list_price", "span", "class", "image_url", "gettxt", "span", "class", "description", "2", "1"

listes_site["farfetch"]= "10", "https://www.farfetch.com/fr/shopping/women/search/items.aspx?q=bougies&rnd=1478085554434&view=180", "bougie-|page", "192", "meta", "property", "og:type", "meta", "property", "og:title", "2", "ogpriceamount", "ogpriceamount", "ogpriceamount", "span", "class", "strike", "meta", "property", "og:image", "og", "p", "itemprop", "description", "2", "0"

listes_site["ecumes-des-sens"]= "10", "http://www.ecumes-dessens.fr/store/25-bougies-parfumees-aux-huiles-essentielles", "bougie-|page", "193", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["menlook"]= "10", "http://www.menlook.com/fr/bougies", "bougie-|fr\/bougies", "194", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "class", "product-sales-price", "span", "class", "product-standard-price", "meta", "property", "og:image", "og", "div", "class", "description", "2", "0"

listes_site["ichor"]= "10", "https://www.bougies-ichor.fr/collection/", "produit", "195", "meta", "property", "og:type", "meta", "property", "og:title", "2", "metaitempropprice", "metaitempropprice", "metaitempropprice", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["village-candle"]= "10", "http://www.villagecandlefrance.fr/12-senteurs", "\d", "196", "span", "id", "our_price_display", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "product-description-tab-content", "2", "0"

listes_site["les-nereides"]= "10", "http://www.lesnereides.com/fr/91-bougies-parfumees", "bougies-senteur", "199", "span", "id", "our_price_display", "h1", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["mademoiselle-daisy"]= "10", "https://www.mademoiselle-daisy.com/fr/96-bougies-voluspa", "bougie", "200", "span", "id", "our_price_display", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"

listes_site["papillon-rouge"]= "10", "http://www.papillonrouge-parfums.com/108-bougies-parfumees?id_category=108&n=45", ".*bougie", "44", "meta", "property", "og:type", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["quali-art"]= "10", "https://www.bougiesdumonde.fr/search?type=product&q=bougie", "bougie-|q=bougie", "31", "meta", "property", "og:type", "meta", "property", "og:title", "0", "button", "id", "add", "span", "id", "old_price_display", "div", "class", "main", "image_a_img_src", "div", "id", "product-description", "2", "0"

listes_site["imagineair"]= "10", "http://imageinair.fr/fr/3-les-bougies-parfumees", "imageinair.fr\/fr\/", "201", "span", "id", "our_price_display", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "0"


listes_site["mugler"]= "10", "http://www.mugler.fr/parfums-bougies/", "bougie-parfumee", "203", "meta", "property", "og:type", "meta", "property", "og:title", "2", "mugler", "mugler", "mugler", "mugler", "mugler", "mugler", "div", "class", "productimage", "href", "meta", "property", "og:description", "1", "0"

listes_site["odyssee-des-sens"]= "10", "http://www.odysseedessens.net/index.php?id_category=3&controller=category&id_lang=5", "id_category=3.controller=category.id_lang=5|id_product=.*controller=product.id_lang=5", "205", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "id", "product-description-tab-content", "2", "0"

listes_site["preziosa"]= "10", "http://www.my-preziosa.fr/cat/1/bougies-parfum%C3%A9es", "bougie.*-parfumee", "206", "div", "id", "produit_image", "h3", "", "", "1", "span", "id", "prix", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "big", "imagesrc", "div", "id", "tab-details", "2", "0"


listes_site["carrement-belle"]= "10", "http://www.carrementbelle.com/fr/5-bougies-parfumees", "bougie.*-parfumee", "207", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "id", "short_description_block", "2", "0"

listes_site["huygens"]= "10", "http://www.huygens.fr/category.php?id_category=50", "id_product", "208", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_block", "2", "0"

listes_site["ma-kibell"]= "10", "http://www.makibell.com/31-bougies-parfumees", "bougie.*-parfumee", "209", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"

listes_site["ombres-portees"]= "10", "http://www.ombresportees.fr/fr/181-bougies-parfumees", "bougie.*-parfumee", "210", "meta", "property", "og:type", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "section", "class", "page-product-box", "2", "0"

listes_site["candyblue"]= "10", "http://www.candyblue.fr/pages/bougies-parfumees.html", "bougie.*-parfumee|boutique\/collection", "211", "span", "class", "final-price", "title", "", "", "1", "span", "class", "final-price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "id", "item-description", "2", "0"

listes_site["lalique"]= "10", "http://www.lalique.com/fr/catalogue/parfums/parfums-d-interieur", "bougie.*-parfumee", "213", "span", "class", "line-center", "meta", "property", "og:title", "2", "span", "class", "line-center", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "class", "col-md-12 heading text-center", "2", "0"

listes_site["ex_zip_line"]= "10", "https://www.zib-line.fr/12-bougies-parfumees#", "bougie.*-parfumee|page-", "214", "span", "id", "our_price_display", "h1", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "prductdesc", "2", "0"

listes_site["hopono"]= "10", "http://hopono-shop.com/fr/200-bougies-parfumees?id_category=200&n=24", "bougie.*-parfumee", "215", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "span", "id", "old_price_display", "meta", "property", "og:image", "og", "div", "id", "short_description_content", "2", "0"

listes_site["moamo"]= "10", "http://www.moamobougies.fr/12-collection-scandinave", "html", "217", "meta", "property", "og:type", "meta", "property", "og:title", "2", "span", "id", "our_price_display", "span", "id", "old_price_display", "span", "id", "view_full_size", "href", "div", "id", "short_description_content", "2", "0"

listes_site["bougie-sylvie"]= "10", "https://www.bougiesylvie.com/bougies-parfumees-300-g-2-meches-b26616.html", "bougie.*html", "218", "span", "class", "impact_price", "span", "itemprop", "name", "1", "span", "class", "impact_price", "pasedsoldes", "pasedsoldes", "pasedsoldes", "div", "class", "grande-image", "href", "p", "class", "description", "2", "0"


# --------------------------------------------------
# NECESSITE JS

#Pour les accents 
listes_site["jovoy"]= "10", "http://www.jovoyparis.com/fr/44-bougies", "bougie", "123", "span", "id", "our_price_display", "h1", "itemprop", "name", "1", "span", "id", "our_price_display", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "bigpic", "imagesrc", "div", "id", "short_description_content", "2", "1"

listes_site["bougies-parfums"]= "10", "http://www.bougies-parfums.fr/vente-bougies.html", "(yankee|vente-bougies).*html$", "13", "li", "class", "product", "gettext", "0", "0", "0", "E", "E", "E", "E", "E", "E", "img", "id", "image-main", "imagesrc", "div", "class", "std", "2", "1"

listes_site["scandles"]= "10", "http://www.scandles.fr/categorie-produit/marques/", "produit", "21", "meta", "itemprop", "price", "h1", "itemprop", "name", "1", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "div", "class", "easyzoom", "src", "div", "id", "paneldescription", "2", "1"


listes_site["jo-malone"]= "10", "http://www.jomalone.fr/products/3560/Pour-la-Maison/Bougies-Parfumes#", "bougie-parfumee", "41", "div", "class", "sku_price", "meta", "property", "og:title", "0", "jomalone", "jomalone", "jomalone", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "1"

listes_site["collines-de-provence"]= "10", "http://www.collinesdeprovence.com/bougies-parfumees.html?limit=all", "bougie-parfumee", "95", "span", "class", "price", "div", "class", "product-name", "1", "G", "G", "G", "G", "G", "G", "img", "id", "image-main", "imagesrc", "div", "class", "short-description", "2", "1"

listes_site["we-candle"]= "10", "http://www.wecandle.fr/7-bougies-parfumees/", "7-bougies-parfumees\/.*(bougie|jarre)", "96", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", " old_price_display", "img", "class", "zoomImg", "imagesrc", "div", "id", "short_description_content", "2", "1"

listes_site["le-cedre-rouge"]= "10", "http://www.lecedrerouge.com/catalogsearch/advanced/?___SID=U&q=bougies", "lecedrerouge.com\/(bougie)", "115", "span", "class", "price", "title", "", "", "1", "lecedrerouge", "lecedrerouge", "lecedrerouge", "lecedrerouge", "lecedrerouge", "lecedrerouge", "div", "class", "area-illustration", "image_a_img_src", "div", "id", "pdt_short_description", "2", "1"


# Je ne suis pas certain que conran ait besoin de JS - je l'enleve pour l'instant
listes_site["the-conran-shop"]= "10", "https://www.conranshop.fr/accessoires-de-decoration/bougies-and-bougeoirs.html?limit=96", "bougie-|page", "187", "meta", "property", "og:type", "meta", "property", "og:title", "2", "conranshop", "conranshop", "conranshop", "conranshop", "conranshop", "conranshop", "div", "class", "zoom", "nextimg", "meta", "property", "og:description", "1", "0"

listes_site["monde-bio"]= "10", "https://www.mondebio.com/aromatherapie-bio-bougies-parfumees/306_119_0_2.bio", "bougie-|page", "190", "meta", "property", "og:type", "meta", "property", "og:title", "2", "p", "class", "product_price", "strike", "", "", "meta", "property", "og:image", "og", "div", "class", "product_desc", "2", "1"

listes_site["alix-d-reynis"]= "10", "http://alixdreynis.bigcartel.com/category/bougie-parfumee", "bougie-|bougies-", "198", "meta", "property", "og:type", "h2", "", "", "1", "ogpriceamount", "ogpriceamount", "ogpriceamount", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "meta", "property", "og:description", "1", "0"



# --------------------------------------------------
# PROBLEME DE SCAN

listes_site["di-toscana"]= "10", "http://www.ditoscana.fr/boutique/recherche_resultats.cfm?code_lg=lg_fr&mot=bougie", ".*bougie", "103", "meta", "property", "og:type", "meta", "property", "og:title", "0", "span", "id", "prix_pas_promotion_euro_fiche_produit", "pasdesoldes", "pasdesoldes", " pasdesoldes", "meta", "property", "og:image", "og", "span", "id", "texte_description_fiche_produit", "2", "0"

listes_site["herve-gambs"]= "10", "http://www.hervegambs.fr/shop/fr/13-bougies-parfumees", "shop\/fr\/.*(2|3|bougie).*html", "149", "span", "id", "our_price_display", "title", "", "", "1", "span", "id", "our_price_display", "span", "id", "old_price_display", "img", "id", "bigpic", "imagesrc", "div", "id", "idTab1", "2", "0"

listes_site["atelier-des-martyrs"]= "10", "https://atelierdesmartyrs.com/?lang=fr", "bougie|product", "165", "span", "class", "amount", "title", "", "", "1", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "woocommerce", "a", "class", "fresco", "nextimg", "div", "itemprop", "description", "2", "0"

listes_site["net-a-porter"]= "10", "https://www.net-a-porter.com/Shop/Search/bougies", "bougie-parfume|bougies", "120", "meta", "property", "og:type", "meta", "property", "og:title", "0", "net-a-porter", "net-a-porter", "net-a-porter", "net-a-porter", "net-a-porter", "net-a-porter", "meta", "property", "og:image", "og", "widget-show-hide", "id", "accordion-2", "2", "0"


# --------------------------------------------------
# PAS DE SCAN POSSIBLE

listes_site["rigaud"]="10","http://www.bougies-rigaud.com/prodcut-category/les-bougies-parfumees","product.*modele|bougies-parfumees|voyage|coffret|prestige", "216", "p", "class", "price", "title", "", "", "1", "p", "class", "price", "padedesoldes", "padedesoldes", "padedesoldes", "meta", "property", "og:image", "content", "div", "itemprop", "description", "2", "0"


listes_site["nour-bougies"]= "10", "http://nourbougies.fr/products/bougies-parfum%C3%A9es-40heures", "product\/bougie", "151", "span", "itemprop", "price", "meta", "property", "og:title", "0", "span", "itemprop", "price", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "og", "div", "itemprop", "description", "2", "0"

listes_site["amazon"]= "10", "https://www.amazon.fr/s/ref=sr_hi_1/278-2648066-8386228?rh=n%3A197858031%2Ck%3Abougies+parfum%C3%A9es&keywords=bougies+parfum%C3%A9es&ie=UTF8", "bougies|Bougie-parfumee", "168", "span", "id", "priceblock_ourprice", "span", "id", "productTitle", "1", "span", "id", "priceblock_ourprice", "pasdesoldes", "pasdesoldes", "pasdesoldes", "img", "id", "landingImage", "imagesrc", "ul", "class", "a-vertical a-spacing-none", "2", "0"

listes_site["aquarelle"]= "10", "http://www.aquarelle.com/boutique/bougies", "boutique|produit|bougie", "177", "meta", "property", "og:type", "meta", "property", "og:title", "0", "div", "class", "prixParfums", "pasdesoldes", "pasdesoldes", "pasdesoldes", "meta", "property", "og:image", "content", "div", "class", "description_produit_description active", "2", "0"


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
		#print listes_site, site, listes_site[site][0]
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

