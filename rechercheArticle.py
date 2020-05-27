# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import string
import time
import csv


class maRecherche:
    """Tous les paramètres utiles à une recherche"""

    def __init__(self):
        self.nbResultat = 0
        self.motRecherche = ""
        self.motRechercheLBC = ""
        self.motRechercheEbay = ""
        self.motCles = []
        self.motInterdits = []
        self.prixMin = 50
        self.prixMax = 1000
        self.boolEbay = True
        self.boolLBC = True


dictio = {}
dictio['Article'] = []


def initRecherche():
    mySearch = maRecherche()
    mySearch.motRecherche = input("Qu'est ce que vous recherchez?\n")
    mySearch.motRechercheEbay = mySearch.motRecherche.strip().replace(' ',
                                                                      '%20').lower()
    mySearch.motRechercheLBC = mySearch.motRecherche.strip().replace(' ', '+').lower()

    tableauMot = mySearch.motRecherche.strip().split()
    mySearch.motRecherche = ''

    for mot in tableauMot:
        mySearch.motRecherche = mySearch.motRecherche + \
            mot[0].upper() + mot[1:].lower()

    prixTemp = int(input("Quel est le prix min?\n"))
    if prixTemp >= 0:
        mySearch.prixMin = prixTemp

    prixTemp = int(input("Quel est le prix max?\n"))
    while prixTemp < 0 or prixTemp < mySearch.prixMin:
        prixTemp = int(
            input("Quel est le prix max? Renseigner un chiffre > au Prix Minimum\n"))

    mySearch.prixMax = prixTemp
    print(f'Le prix min est de {mySearch.prixMin}')
    print(f'Le prix max est de {mySearch.prixMax}')

    motCle = input(
        "\nRenseignez les mots obligatoires dans le titre de l'annonce :\n")
    if motCle != '':
        mySearch.motCles.append(motCle.lower())
    while (motCle) != '':
        motCle = input()
        if motCle != '':
            mySearch.motCles.append(motCle.lower())

    motInterdit = input(
        "Renseignez les mots interdits dans le titre de l'annonce :\n")
    if motInterdit != '':
        mySearch.motInterdits.append(motInterdit.lower())
    while (motInterdit) != '':
        motInterdit = input()
        if motInterdit != '':
            mySearch.motInterdits.append(motInterdit.lower())
    return mySearch


def presentDansmotCles(mySearch, texte):
    if len(mySearch.motCles) == 0:
        return True
    for motCle in mySearch.motCles:
        if motCle in texte.lower():
            for motInterdit in mySearch.motInterdits:
                if motInterdit in texte.lower():
                    return False
            return True


def csvPrinter(motRecherche):
    tableurArticle = open(f'listArticles{motRecherche}.csv', 'w')
    writer = csv.writer(tableurArticle, delimiter=',', dialect='excel')
    writer.writerow(["Article", "Lien", "Lieu", "Prix"])
    for [a, b, c, d] in dictio['Article']:
        writer.writerow([a, b, c, d])
    tableurArticle.close()


def rechercheArticlesLBC(mySearch, URL):
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    page = requests.get(URL, headers=headers)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    compteurArticle = 0
    articles = page_soup.findAll("a", {'class': 'clearfix trackable'})
    for article in articles:
        titre = article.get('title')
        if (presentDansmotCles(mySearch, titre)):
            spanPrix = article.find('span', {'itemprop': 'priceCurrency'})
            if spanPrix is not None:
                compteurDigits = 0
                grpDigits = spanPrix.text.split()
                spanPrixConcat = ''
                while grpDigits[compteurDigits].isdigit():
                    spanPrixConcat = spanPrixConcat + grpDigits[compteurDigits]
                    compteurDigits += 1
                prix = int(spanPrixConcat)
            else:
                prix = 0
            if (mySearch.prixMin < prix < mySearch.prixMax):
                lien = f"http://leboncoin.fr{article.get('href')}"
                lieu = article.find(
                    'p', {'itemprop': 'availableAtOrFrom'}).text
                toDic = titre, lien, lieu, f'{prix} €'
                dictio['Article'].append(toDic)
                compteurArticle += 1
    return compteurArticle


def rechercheArticlesEbay(mySearch, URL):
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    page = requests.get(URL, headers=headers)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    compteurArticle = 0

    articlesSet = page_soup.find('div', {'id': 'ResultSetItems'})
    if articlesSet is not None:
        if articlesSet.findAll('li', {'class': 'sresult lvresult clearfix li'}) is not None:
            articles = articlesSet.findAll(
                'li', {'class': 'sresult lvresult clearfix li'})
        if articlesSet.findAll('li', {'class': 'sresult lvresult clearfix  shic'}) is not None:
            articles = articles + articlesSet.findAll(
                'li', {'class': 'sresult lvresult clearfix  shic'})
        for article in articles:
            titre = article.find('a', {'class': 'vip'}).text
            if (presentDansmotCles(mySearch, titre)):
                lien = article.find('a', {'class': 'vip'}).get('href')
                spanPrix = article.find('span', {'class': "bold"})
                lieu = 'pasImp'
                if spanPrix is not None:
                    prix = float(spanPrix.text.split()[0].replace(',', '.'))
                else:
                    prix = 0
                if mySearch.prixMin < prix < mySearch.prixMax:
                    toDic = titre, lien, lieu, f'{prix} €'
                    dictio['Article'].append(toDic)
                    compteurArticle += 1
    return compteurArticle


# Debut du decompte du temps
def main(mySearch):

    start_time = time.time()
    if mySearch.boolEbay:
        URL = f'https://www.ebay.fr/sch/i.html?LH_SellerType=1&_nkw={mySearch.motRechercheEbay}'
        print(URL)
        mySearch.nbResultat += rechercheArticlesEbay(mySearch, URL)
        for numPage in range(2, 11):
            URL = f'https://www.ebay.fr/sch/i.html?LH_SellerType=1&_nkw={mySearch.motRechercheEbay}&_pgn={numPage}'
            print(URL)
            mySearch.nbResultat += rechercheArticlesEbay(mySearch, URL)
    if mySearch.boolLBC:
        for numPage in range(1, 11):
            URL = f'https://www.leboncoin.fr/recherche/?text={mySearch.motRechercheLBC}&locations=r_6&page={numPage}'
            print(URL)
            mySearch.nbResultat += rechercheArticlesLBC(mySearch, URL)

    for article in dictio['Article']:
        print(
            f"Article : {article[0]}\nLien : {article[1]}\nLieu: {article[2]}\nPrix : {article[3]}\n")
    res = f"Il y a {mySearch.nbResultat} résultats pour la recherche\nCes résultats ont été enregistrés dans listArticles{mySearch.motRecherche}.csv dans le dossier courant"
    csvPrinter(mySearch.motRecherche)

    # Affichage du temps d execution
    res = res + \
        f"\nTemps d\'exécution : {time.time() - start_time} secondes ---"
    print(res)
    return res


if __name__ == "__main__":
    # execute only if run as a script
    mySearch = initRecherche()
    main(mySearch)
