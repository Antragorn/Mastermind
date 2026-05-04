from tkinter import *
from random import randint
import itertools
from tkinter import messagebox
from json import load, dump
from tkinter import Frame


def sauve_partie():
    """Permet de sauvegarder la partie en cours dans un fichier"""
    sauv_fenetre = Toplevel(fenetre)
    sauv_fenetre.title("Sauvegarder une partie")
    Label(sauv_fenetre, text="Nom de la partie :").pack(padx=50, pady=50)
    entry = Entry(sauv_fenetre, justify=CENTER)
    entry.pack(ipadx=10, ipady=5, fill=BOTH)

    def sauvegarder():
        nom_partie = entry.get().strip()

        # Lire le fichier existant
        try:
            with open("save.txt", "r") as f:
                data = load(f)
        except FileNotFoundError:
            data = {}
        data[nom_partie] = {
            "code_secret": list(code_secret),
            "historique": [list(e) for e in historique_essais],
            "num_essai": num_essai
        }  # Ajouter la nouvelle partie
        # Écrire dans le fichier
        with open("save.txt", "w") as f:
            dump(data, f)
        sauv_fenetre.destroy()
        messagebox.showinfo("Sauvegarde", "Partie sauvegardée avec succès !")

    Button(sauv_fenetre, text="Sauvegarder", command=sauvegarder).pack(padx=70, pady=50)


def charge_partie():
    """Permet de charger le fichier sauvegarde"""
    try:
        with open("save.txt", "r") as f:
            data = load(f)
            if len(data) == 0:
                raise FileNotFoundError
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucune partie sauvegardée trouvée !")
        return

    # Créer la fenêtre pour choisir la partie
    choix_fenetre = Toplevel(fenetre)
    choix_fenetre.title("Charger une partie")

    nom_var = StringVar()
    noms_parties = list(data.keys())
    nom_var.set(noms_parties[0])  # valeur par défaut

    menu = OptionMenu(choix_fenetre, nom_var, *noms_parties)
    menu.pack(ipadx=100, ipady=100, fill=BOTH)

    def charger_selection():
        global code_secret, historique_essais, num_essai, code_entered, chargement, historique_essais_rep
        partie = nom_var.get()
        rejouer()  # réinitialiser le plateau

        sauvegarde = data[partie]

        code_secret = tuple(sauvegarde["code_secret"])
        historique_essais = [tuple(e) for e in sauvegarde["historique"]]
        num_essai = sauvegarde["num_essai"]
        code_entered = True

        code_aleatoire.grid_forget()

        chargement = True
        for essai in historique_essais:
            for couleur in essai:
                switch_callback(couleur)
        chargement = False
        historique_essais_rep = [(essai, calculer_essai(essai, code_secret)) for essai in historique_essais]

        choix_fenetre.destroy()
        messagebox.showinfo("Chargement", f"Partie '{partie}' rechargée avec succès !")

    bouton_charger = Button(choix_fenetre, text="Charger", command=charger_selection)
    bouton_charger.pack(padx=10, pady=10)


def supr_partie():
    """Permet de supprimer une sauvegarde"""
    try:
        with open("save.txt", "r") as f:
            data = load(f)
            if len(data) == 0:
                raise FileNotFoundError
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucune partie sauvegardée trouvée !")
        return

    # Créer la fenêtre pour choisir la partie
    choix_fenetre = Toplevel(fenetre)
    choix_fenetre.title("Supprimer une partie")

    nom_var = StringVar()
    noms_parties = list(data.keys())
    nom_var.set(noms_parties[0])  # valeur par défaut

    menu = OptionMenu(choix_fenetre, nom_var, *noms_parties)
    menu.pack(ipadx=100, ipady=100, fill=BOTH)

    def supprimer():
        nom_partie = nom_var.get()

        # Lire le fichier existant
        try:
            with open("save.txt", "r") as f:
                data = load(f)
        except FileNotFoundError:
            data = {}
        del data[nom_partie]
        # Écrire dans le fichier
        with open("save.txt", "w") as f:
            dump(data, f)
        choix_fenetre.destroy()
        messagebox.showinfo("Suppression", f"Partie {nom_partie} supprimée avec succès !")

    Button(choix_fenetre, text="Supprimer", command=supprimer).pack(padx=70, pady=50)


def init_ui():
    """
    Initialise l'interface graphique principale du jeu Mastermind.

    Crée :
    - La fenêtre principale (plein écran)
    - Les menus (Fichier, Paramètres, IA)
    - Les boutons d'action (rejouer, annuler, quitter, code aléatoire)
    - Les boutons de sélection des couleurs
    - Les frames pour afficher les essais et l'historique

    """
    global code_aleatoire, frame_jeu, frame_essai_actuel, frame_historique
    fenetre.title("Mastermind")
    fenetre.state("zoomed")

    # création des menus
    menu = Menu(fenetre)
    fenetre.config(menu=menu)

    # paramètres
    menu_parametre = Menu(menu, tearoff=0)
    menu.add_cascade(label="Paramètres", menu=menu_parametre)
    menu_parametre.add_command(label="Ouvrir", command=ouvrir_param)

    # fichier
    menu_fichier = Menu(menu, tearoff=0)
    menu.add_cascade(label="Fichier", menu=menu_fichier)
    menu_fichier.add_command(label="Sauvegarder", command=sauve_partie)
    menu_fichier.add_command(label="Charger", command=charge_partie)
    menu_fichier.add_command(label="Supprimer", command=supr_partie)

    # bouton
    rejoue = Button(fenetre, command=rejouer, text="rejouer")
    code_aleatoire = Button(fenetre, command=random_code, text="code aleatoire")
    annule = Button(fenetre, command=annuler, text="annuler")
    quitter = Button(fenetre, command=fenetre.destroy, text="quitter")
    coup_ia_button = Button(fenetre, command=coup_ia_callback, text="coup de l'IA")
    efface = Button(fenetre, command=effacer, text="effacer")

    frame_jeu = Frame(fenetre)
    frame_historique = Frame(frame_jeu)

    rejoue.grid(row=2, column=0)
    annule.grid(row=2, column=0, columnspan=len(liste_couleurs), sticky="n")
    code_aleatoire.grid(row=3, column=0, columnspan=len(liste_couleurs), sticky="n")
    coup_ia_button.grid(row=2, column=1, sticky="n")
    quitter.grid(row=2, column=len(liste_couleurs) - 1)
    efface.grid(row=2, column=2)

    for i, couleur in enumerate(liste_couleurs):
        boutcoul = Button(fenetre, command=lambda n=i: switch_callback(n), bg=couleur, width=11, height=2)
        boutcoul.grid(row=1, column=i, sticky=EW)
        fenetre.grid_columnconfigure(i, weight=1)
    
    frame_jeu.grid(row=0, column=0, columnspan=len(liste_couleurs), sticky=NSEW)
    frame_historique.pack(side=TOP, fill=BOTH, expand=True)
    fenetre.grid_rowconfigure(0, weight=1)
    frame_essai_actuel=Frame(frame_historique)
    frame_essai_actuel.pack(side=TOP)


# variables
code_entered: bool = False
partie_terminee: bool = False
code_secret: tuple[int] = (0,)
longueur_code: int = 4
liste_couleurs: list[str] = ['#000000', '#ffffff', '#00ff00', '#ff0000', '#0000ff', '#00ffff', '#ff00ff', '#ffff00']
prec_essai: list[int] = []
code_aleatoire: Button
frame_jeu: Frame
frame_historique: Frame
frame_essai_actuel: Frame
essais_max: int = 10
num_essai: int = 0
historique_essais: list = []
historique_essais_rep: list = []  # [(essai, reponse), ...]
chargement: bool = False

# Callbacks
def switch_callback(num_couleur: int):
    """Callback des boutons de couleur, redirige vers la création du code ou la tentative d'un essai"""
    global num_essai, frame_essai_actuel, partie_terminee
    if partie_terminee:
        return
    prec_essai.append(num_couleur)
    canvas = Canvas(frame_essai_actuel,height=50,width=50)
    canvas.pack(side=LEFT)
    canvas.create_oval(5, 5, 45, 45, fill=liste_couleurs[num_couleur])
    if len(prec_essai) < longueur_code:
        return

    ancien_frame = frame_essai_actuel

    if code_entered:
        num_essai += 1
        essai_tuple = tuple(prec_essai)
        if not chargement:
            historique_essais.append(essai_tuple)

        reponse = calculer_essai(essai_tuple, code_secret)
        if not chargement:
            historique_essais_rep.append((essai_tuple, reponse))

        afficher_reponse(ancien_frame, reponse)
        if essai_tuple == code_secret:
            partie_terminee = True
            popup = Toplevel(fenetre)
            popup.title("Victoire !")
            popup.geometry("300x150")
            Label(popup, text="🎉 Bravo ! Vous avez trouvé le code !", font=("Arial", 12)).pack(pady=20)
            return

        if num_essai >= essais_max and not partie_terminee:
            partie_terminee = True

            popup = Toplevel(fenetre)
            popup.title("Défaite")
            popup.geometry("300x200")

            Label(popup, text="❌ Vous avez perdu ! Le code secret était :", font=("Arial", 12)).pack(pady=10)

            frame_code = Frame(popup)
            frame_code.pack(pady=10)

            for couleur in code_secret:
                canvas = Canvas(frame_code, width=30, height=30)
                canvas.pack(side=LEFT, padx=5)
                canvas.create_oval(5, 5, 25, 25, fill=liste_couleurs[couleur])
    else:
        entrer_code(tuple(prec_essai))
        

    frame_essai_actuel = Frame(frame_historique)
    frame_essai_actuel.pack(side=TOP)

    prec_essai[:] = []


def entrer_code(code: tuple[int]):
    """définit le code entré comme code_secret pour la partie"""
    global code_secret, code_entered, prec_essai, frame_essai_actuel
    frame_essai_actuel.destroy()
    prec_essai.clear()
    code_secret = code[:]
    code_entered = True
    code_aleatoire.grid_forget()


def random_code():
    """callback du bouton "Code Aléatoire"
    """
    global frame_essai_actuel
    entrer_code(tuple(randint(0, 7) for _ in range(4)))
    frame_essai_actuel = Frame(frame_historique)
    frame_essai_actuel.pack(side=TOP)


def calculer_essai(essai: tuple[int], code: tuple[int]) -> tuple[int, int]:
    """
    Compare un essai avec le code secret.
    """
    bonne_places = 0
    mauvaise_places = 0
    code_restant = list(code)
    essai_restant = []

    for i in range(len(code)):
        if essai[i] == code[i]:
            bonne_places += 1
            code_restant[i] = None
        else:
            essai_restant.append(essai[i])

    code_restant = [c for c in code_restant if c is not None]

    for couleur in essai_restant:
        if couleur in code_restant:
            mauvaise_places += 1
            code_restant.remove(couleur)

    return bonne_places, mauvaise_places


def afficher_reponse(frame, reponse: tuple[int, int]):
    """
    Affiche visuellement la réponse à un essai mais sans donner la reponse exact
    """
    bien, mal = reponse

    frame_rep = Frame(frame)
    frame_rep.pack(side=RIGHT, padx=10)

    pions = ["black"] * bien + ["white"] * mal

    for i, couleur in enumerate(pions):
        canvas = Canvas(frame_rep, width=20, height=20)
        canvas.grid(row=i // 2, column=i % 2)
        canvas.create_rectangle(2, 2, 18, 18, fill=couleur)


def rejouer():
    """
    Permet de recommencer une nouvelle partie.
    """
    global code_entered, code_secret, set_possibilites, prec_essai, num_essai, partie_terminee, frame_essai_actuel, historique_essais_rep
    partie_terminee = False
    code_entered = False
    code_secret = (0,)
    prec_essai.clear()
    num_essai = 0
    historique_essais_rep.clear()

    for widget in frame_historique.winfo_children():
        widget.destroy()

    if frame_essai_actuel:
        frame_essai_actuel.destroy()
    frame_essai_actuel = Frame(frame_historique)
    frame_essai_actuel.pack(side=TOP)

    code_aleatoire.grid(row=3, column=0, columnspan=len(liste_couleurs), sticky="n")


def effacer():
    """
    Annule la dernière couleur selectionne mais ne fait rien si aucune couleur n'est choisi.
    """
    global prec_essai, frame_essai_actuel, partie_terminee
    if partie_terminee:
        return
    if prec_essai:
        prec_essai.pop()
        frame_essai_actuel.winfo_children()[-1].destroy()

def annuler():
    global num_essai, historique_essais, partie_terminee, prec_essai, frame_essai_actuel
    if not(num_essai or historique_essais) or partie_terminee:
        return
    
    historique_essais.pop()
    historique_essais_rep.pop()
    num_essai -= 1
    prec_essai.clear()

    for widget in frame_historique.winfo_children():
        widget.destroy()
    
    for essai in historique_essais:
        frame_essai = Frame(frame_historique)
        frame_essai.pack(side=TOP)
        
        for couleur_idx in essai:
            canvas = Canvas(frame_essai, height=50, width=50)
            canvas.pack(side=LEFT)
            canvas.create_oval(5, 5, 45, 45, fill=liste_couleurs[couleur_idx])
        
        reponse = calculer_essai(essai, code_secret)
        afficher_reponse(frame_essai, reponse)
    
    frame_essai_actuel = Frame(frame_historique)
    frame_essai_actuel.pack(side=TOP)


def coup_ia_callback():
    """Joue un coup proposé par l'IA (algorithme de Knuth)"""
    global prec_essai
    if not code_entered or partie_terminee:
        return
    
    from ia import knuth

    coup = knuth(historique_essais_rep)
    
    # Jouer le coup proposé en appelant switch_callback pour chaque couleur
    for couleur in coup:
        switch_callback(couleur)

if __name__ == '__main__':
    fenetre = Tk()
    init_ui()
    
    messagebox.showinfo(
        "Bienvenue au Mastermind!",
        "Objectif: Trouver le code secret en 10 essais maximum.\n\n"
        "Chaque code est composé de 4 couleurs\n"
        "Après chaque tentative, vous recevez des indices:\n"
        "  - Carrés NOIRS: couleur correcte à la bonne place\n"
        "  - Carrés BLANCS: couleur correcte à la mauvaise place\n\n"
        "Maintenant, le joueur 1 peut entrer un code en cachette ou vous pouvez cliquer sur le bouton "
        "\"code aleatoire\" pour commencer la partie."
    )
    
    fenetre.mainloop()
