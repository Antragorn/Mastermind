import numpy as np
from itertools import product
from main import calculer_essai

def knuth(essais:tuple) -> list[int]:
    """essais: tuple des essais et réponses précédentes
    --> prochain_essai: list[int], réponse de l'algorithme
    """

    if not essais:
        return [1, 1, 2, 2] #initial try for the five-guess algorithm
    
    codes = list(product(range(8), repeat=4))

    possible = [
        code for code in codes
        if all(calculer_essai(guess, code) == response for guess, response in essais)
    ]

    if len(possible) == 1:
        return possible[0]

    prochain_essai = []

    return prochain_essai



# reference : https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind