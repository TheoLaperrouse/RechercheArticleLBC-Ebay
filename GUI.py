from tkinter import messagebox, Label, StringVar, IntVar, Tk, Button, Entry, Checkbutton
import rechercheArticle as rA
import string
import time


def parserListe(motAParser):
    res = []
    mots = motAParser.strip().lower().split()
    for mot in mots:
        res.append(mot)
    return res


def initGUI(mySearchGUI):
    mySearch = rA.maRecherche()
    mySearch.motRecherche = mySearchGUI.motRecherche
    mySearch.motRechercheEbay = mySearchGUI.motRecherche.strip().replace(' ',
                                                                         '%20').lower()
    mySearch.motRechercheLBC = mySearchGUI.motRecherche.strip().replace(' ',
                                                                        '+').lower()
    mySearch.boolEbay = mySearchGUI.boolEbay
    mySearch.boolLBC = mySearchGUI.boolLBC
    tableauMot = mySearchGUI.motRecherche.strip().split()
    mySearchGUI.motRecherche = ''

    for mot in tableauMot:
        mySearch.motRecherche = mySearchGUI.motRecherche + \
            mot[0].upper() + mot[1:].lower()

    mySearch.prixMax = int(mySearchGUI.prixMax)
    mySearch.prixMin = int(mySearchGUI.prixMin)
    mySearch.motCles = mySearchGUI.motObligatoires
    mySearch. motInterdits = mySearchGUI.motInterdits
    return rA.main(mySearch)


def clicked():
    global recherche, prixMax, prixMin, Ebay_state, LBC_state, motInterdits, motObligatoires
    mySearch = rA.maRecherche()
    mySearch.motRecherche = recherche.get()
    mySearch.prixMin = prixMin.get()
    mySearch.prixMax = prixMax.get()
    mySearch.boolEbay = bool(Ebay_state.get())
    mySearch.boolLBC = bool(LBC_state.get())

    if(mySearch.prixMax < mySearch.prixMin):
        messagebox.askretrycancel(
            'Warning prixMin > PrixMax', "Le prix Minimum est supérieur au prix maximum, vous n'avez pas du bien réfléchir")
    elif(not mySearch.prixMin.isdigit() or not mySearch.prixMax.isdigit()):
        messagebox.askretrycancel(
            'Warning intError', "Veuillez rentrer des nombres dans Prix max et Prix Min")
    elif(not mySearch.boolEbay and not mySearch.boolLBC):
        messagebox.askretrycancel(
            'Warning selectErrir', "Veuillez sélectionner au moins une plateforme de vente")
    else:
        mySearch.motObligatoires = parserListe(motObligatoires.get())
        mySearch.motInterdits = parserListe(motInterdits.get())

        res = initGUI(mySearch)
        resWindow = Tk()
        resWindow.title(f'Résultats {mySearch.motRecherche}')

        resWindow.geometry('540x60')
        resText = Label(
            resWindow, text=res)
        resText.pack()
        resWindow.mainloop()

        # resWindow


window = Tk()

window.title("Ebay/LBC Search")
window.geometry('330x170')

lblPrixMax = Label(
    window, text="Prix Max (en €):")
lblPrixMax.grid(row=3, column=0)

lblPrixMin = Label(
    window, text="Prix Min (en €):")
lblPrixMin.grid(row=2, column=0)

lblRecherche = Label(
    window, text="Recherche :")
lblRecherche.grid(row=1, column=0)

lblMotsObligatoires = Label(
    window, text="Mots Obligatoires :")
lblMotsObligatoires.grid(row=4, column=0)

lblMotsInterdits = Label(
    window, text="Mots Interdits :")
lblMotsInterdits.grid(row=5, column=0)

recherche = Entry(window)
prixMin = Entry(window)
prixMax = Entry(window)
motObligatoires = Entry(window)
motInterdits = Entry(window)

recherche.grid(row=1, column=1)

prixMin.grid(row=2, column=1)
prixMax.grid(row=3, column=1)
motObligatoires.grid(row=4, column=1)
motInterdits.grid(row=5, column=1)

LBC_state = IntVar()
LBC = Checkbutton(window, text='LeBonCoin', variable=LBC_state)
LBC.select()
LBC.grid(row=6, column=1)

Ebay_state = IntVar()
Ebay = Checkbutton(window, text='Ebay', variable=Ebay_state)
Ebay.select()
Ebay.grid(row=6, column=0)

btn = Button(window, text="Valider la recherche", command=clicked)
btn.grid(row=8, column=0, columnspan=1)
window.mainloop()
