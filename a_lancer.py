from classes import *
from tipe_en_cours import *

GEO2 = [[3 for i in range(50)] for j in range(50)]

ville = cases_touchees(25, 25, 2, 0, 50, 0, 50)

g = Grille(50, GEO2, 10000000)
g.cellules[25][25].repartition[1] += 300

virus = [0.8, 0.2, 0.2]

statistiques_2(g, virus)

"""
ville = cases_touchees(150, 150, 1, 0, 300, 0, 300)
for i, j in ville:
    GEO2[i][j] = 90

g2 = Grille(300, GEO2, 10000000)
g2.cellules[150][150].repartition[1] += 30000


virus = [0.7, 0.7, 0.7]

statistiques_2(g2, virus)
"""
