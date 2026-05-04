from itertools import product
from main import calculer_essai

def knuth(essais:tuple) -> list[int]:
    """essais: tuple des essais et réponses précédentes
    --> prochain_essai: list[int], réponse de l'algorithme
    """

    if not essais:
        return list(range(4)) #initial try for the five-guess algorithm
    
    codes = list(product(range(8), repeat=4))

    possible = [
        code for code in codes
        if all(calculer_essai(guess, code) == response for guess, response in essais)
    ]

    if len(possible) == 1:
        return possible[0]

    best_guess = None
    best_score = float('inf')

    for guess in codes:
        partition = {}
        for p in possible:
            r = calculer_essai(guess, p)
            partition[r] = partition.get(r, 0) + 1
        
        worst_case = max(partition.values())

        if worst_case < best_score or (worst_case == best_score and guess in possible):
            if worst_case < best_score or best_guess not in possible:
                best_score = worst_case
                best_guess = guess

    return best_guess



# reference : https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind