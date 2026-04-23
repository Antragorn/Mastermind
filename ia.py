
def knuth(essais:dict[str:tuple]) -> list[int]:
    """essais: dictionnaire qui associe à chaque essai précédent sa réponse
    --> prochain_essai: list[int], réponse de l'algorithme
    """

    if not len(essais):
        return [1, 1, 2, 2] #initial try for the five-guess algorithm
    
    all_codes = {f"{a}{b}{c}{d}" for a in range(8) for b in range(8) for c in range(8) for d in range(8)}
    s = all_codes.copy()

    for guess in essais:
        #todo remove de s tous les codes qui ne peuvent pas avoir donné la réponse qui a été donnée à l'essai
        pass

    prochain_essai = []

    return prochain_essai

knuth({"0012":(1, 1)})

# reference : https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind