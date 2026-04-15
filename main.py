from tkinter import *

#création de la fenêtre
fenetre = Tk()
fenetre.title("Mastermind")

#création des menus
menu = Menu(fenetre)
fenetre.config(menu = menu)

#fonctions pour les menus
def charge_partie():
    """Permet de charger le fichier sauvegarde"""
    pass

def sauve_partie():
    """Permet de sauvegarder la partie en cours dans un fichier"""
    pass

def supr_partie():
    """Permet de supprimer une sauvegarde"""
    pass

def ouvrir_param():
    """Permet de charger un fichier de paramètres"""
    pass

# paramètres
menu_parametre= Menu(menu, tearoff = 0)
ai_var = StringVar(value="knuth")
menu_ia = Menu(menu_parametre, tearoff=0)
menu_ia.add_radiobutton(label="Knuth's Algorithm", variable=ai_var, value="knuth")
menu_ia.add_radiobutton(label="Expected-Size Algorithm", variable=ai_var, value="exp_size")
menu.add_cascade(label = "Paramètres", menu = menu_parametre)
menu_parametre.add_command(label = "Ouvrir", command = ouvrir_param)
menu_parametre.add_cascade(label = "IA", menu = menu_ia)

#fichier
menu_fichier = Menu(menu, tearoff = 0)
menu.add_cascade(label = "Fichier", menu = menu_fichier)
menu_fichier.add_command(label = "Sauvegarder", command = sauve_partie)
menu_fichier.add_command(label = "Charger", command = charge_partie)
menu_fichier.add_command(label = "Supprimer", command = supr_partie)

fenetre.mainloop()