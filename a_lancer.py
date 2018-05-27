from classes import *
from tipe_en_cours import *

import pickle

taille_grille = 50
population_initiale = 1000000000
malades_initiaux = 300
x_malade_initial = 25
y_malade_initial = 25

GEO2 = [[3 for i in range(taille_grille)] for j in range(taille_grille)]

virus = [0.8, 0.2, 0.2]

# On fait varier le nombre de villes

# Une seule ville

ville = cases_touchees(25, 25, 2, 0, taille_grille, 0, taille_grille)

for x, y in ville:
    GEO2[x][y] = 90

g = Grille(taille_grille, GEO2, population_initiale)
g.cellules[x_malade_initial][y_malade_initial].repartition[1] += malades_initiaux


simulation_image_malades(g, virus)


"""
sains, malades, morts, soignes = statistiques_finale(g, virus, 10)

nom_fichier = "1_ville_repartitions.pickle"

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)

ville = cases_touchees(13, 13, 2, 0, taille_grille, 0, taille_grille)


ville = cases_touchees(14, 42, 2, 0, taille_grille, 0, taille_grille)




ville = cases_touchees(150, 150, 1, 0, 300, 0, 300)
for i, j in ville:
    GEO2[i][j] = 90

g2 = Grille(300, GEO2, 10000000)
g2.cellules[150][150].repartition[1] += 30000


virus = [0.7, 0.7, 0.7]

statistiques_2(g2, virus)
"""
