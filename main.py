from tkinter import *
from random import randint
import itertools

# fonctions pour les menus
from tkinter import Frame


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


def init_ui():
    """création de la fenêtre"""
    global code_aleatoire, frame_jeu, frame_essai_actuel
    fenetre.title("Mastermind")
    fenetre.state("zoomed")

    # création des menus
    menu = Menu(fenetre)
    fenetre.config(menu=menu)

    # paramètres
    menu_parametre = Menu(menu, tearoff=0)
    ai_var = StringVar(value="knuth")
    menu_ia = Menu(menu_parametre, tearoff=0)
    menu_ia.add_radiobutton(label="Knuth's Algorithm", variable=ai_var, value="knuth")
    menu_ia.add_radiobutton(label="Expected-Size Algorithm", variable=ai_var, value="exp_size")
    menu.add_cascade(label="Paramètres", menu=menu_parametre)
    menu_parametre.add_command(label="Ouvrir", command=ouvrir_param)
    menu_parametre.add_cascade(label="IA", menu=menu_ia)

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
    frame_jeu = Frame(fenetre)
    rejoue.grid(row=2, column=0)
    annule.grid(row=2, column=0, columnspan=len(liste_couleurs), sticky="n")
    code_aleatoire.grid(row=3, column=0, columnspan=len(liste_couleurs), sticky="n")
    quitter.grid(row=2, column=len(liste_couleurs) - 1)
    for i, couleur in enumerate(liste_couleurs):
        boutcoul = Button(fenetre, command=lambda n=i: switch_callback(n), bg=couleur, width=11, height=2)
        boutcoul.grid(row=1, column=i, sticky=EW)
        fenetre.grid_columnconfigure(i, weight=1)
    frame_jeu.grid(row=0, column=0, columnspan=len(liste_couleurs), sticky=NSEW)
    fenetre.grid_rowconfigure(0, weight=1)
    frame_essai_actuel=Frame(frame_jeu)
    frame_essai_actuel.pack(side=TOP)


# variables
code_entered: bool = False
code_secret: tuple[int] = (0,)
longueur_code: int = 4
liste_couleurs: list[str] = ['#000000', '#ffffff', '#00ff00', '#ff0000', '#0000ff', '#00ffff', '#ff00ff', '#ffff00']
# noinspection PyTypeChecker
set_possibilites: set[tuple[int]] = set(itertools.product(range(len(liste_couleurs)), repeat=longueur_code))
prec_essai: list[int] = []
code_aleatoire: Button
frame_jeu: Frame
frame_essai_actuel: Frame
essais_max: int = 10
num_essai: int = 0

# Callbacks
def switch_callback(num_couleur: int):
    """Callback des boutons de couleur, redirige vers la création du code ou la tentative d'un essai"""
    global set_possibilites, num_essai, frame_essai_actuel
    prec_essai.append(num_couleur)
    canvas = Canvas(frame_essai_actuel,height=75,width=75)
    canvas.pack(side=LEFT)
    canvas.create_oval(5, 5, 70, 70, fill=liste_couleurs[num_couleur])
    if len(prec_essai) < longueur_code:
        return
    if code_entered:
        num_essai += 1
        essai_tuple = tuple(prec_essai)
        reponse = calculer_essai(essai_tuple, code_secret)
        set_possibilites = {pos for pos in set_possibilites if calculer_essai(essai_tuple, pos) == reponse}
        afficher_reponse(reponse)
    else:
        entrer_code(tuple(prec_essai))
    frame_essai_actuel.destroy()
    frame_essai_actuel = Frame(frame_jeu)
    frame_essai_actuel.pack(side=TOP)
    prec_essai[:] = []


def entrer_code(code: tuple[int]):
    """définit le code entré comme code_secret pour la partie"""
    global code_secret, code_entered
    code_secret = code[:]
    code_entered = True
    code_aleatoire.grid_forget()


def random_code():
    """callback du bouton "Code Aléatoire"
    """
    entrer_code(tuple(randint(0, 7) for _ in range(4)))


def calculer_essai(essai: tuple[int], code: tuple[int]) -> tuple[int, int]:
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


def afficher_reponse(reponse: tuple[int, int]):
    bien, mal = reponse
    label = Label(fenetre, text=f"{bien} bien placés, {mal} mal placés")
    label.grid(row=4)


def aide() -> tuple[int]:
    return next(iter(set_possibilites))


def rejouer():
    pass


def annuler():
    pass


if __name__ == '__main__':
    fenetre = Tk()
    init_ui()
    fenetre.mainloop()
