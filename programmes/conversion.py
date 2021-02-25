def p_infection(R_0, tau, voisins):
    return 1 - ((voisins - R_0)/voisins)**(1/tau)

def p_mort(tau, mortalite):
    return mortalite/tau

def p_guerison(tau, mortalite):
    return (1 - mortalite)/tau

def parametres(R_0, tau, voisins, mortalite):
    return(p_infection(R_0, tau, voisins), p_mort(tau, mortalite), p_guerison(tau, mortalite))

if __name__ == '__main__':
    R_0 = float(input('Entrez le taux de reproduction de base (R_0) : '))
    tau = float(input("Entrez le temps moyen d'infection (tau) : " ))
    voisins = float(input("Entrez le nombre de voisins entrant en compte dans l'infection : "))
    mortalite = float(input("Entrez la mortalité du virus(par rapport à la population infectée) : "))

    p_i = p_infection(R_0, tau, voisins)
    p_m = p_mort(tau, mortalite)
    p_g = p_guerison(tau, mortalite)

    print("La probabilité d'infection vaut : {}\nLa probabilité de mort vaut : {}\nLa probabilité de guérision vaut {}\n".format(p_i, p_m, p_g))
    print((p_i, p_m, p_g))