def test(taille_grille):
    GEO2 = [[3 for i in range(taille_grille)] for j in range(taille_grille)]
    population_initiale = 700*taille_grille**2
    g = Grille(taille_grille, GEO2, population_initiale)
    g.cellules[int(taille_grille/2)][int(taille_grille/2)].repartition[1] += 1000
    return g
virus = [0.4,0.1,0.1]

g=test(10)