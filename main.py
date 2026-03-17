from tkinter import *

#création de la fenêtre
fenetre = Tk()
fenetre.title("Mastermind")

#création des menues
menu = Menu(fenetre)
fenetre.config(menu = menu)

# paramètres
menu_parametre= Menu(menu, tearoff = 0)
menu.add_cascade(label = "Paramètres", menu = menu_parametre)
menu_parametre.add_command(label = "ouvrir", command = None)

#fichier
menu_fichier = Menu(menu, tearoff = 0)
menu.add_cascade(label = "fichier", menu = menu_fichier)
menu_fichier.add_command(label = "Sauvegarder", command = None)
menu_fichier.add_command(label = "Charger", command = None)
menu_fichier.add_command(label = "Supprimer", command = None)

fenetre.mainloop()
