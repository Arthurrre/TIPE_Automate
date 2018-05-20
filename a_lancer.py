from classes import *
from tipe_en_cours import *

GEO2 = [[3 for i in range(300)] for j in range(300)]

ville = cases_touchees(72, 198, 2, 0, 300, 0, 300)

for i, j in ville:
    GEO2[i][j] = 90

g = Grille(300, GEO2, 10000000)
g.cellules[150][150].repartition[1] += 30000
g.cellules[150][150].population += 30000

virus = [0.6, 0.5, 0.3]

statistiques_2(g, virus)

ville = cases_touchees(150, 150, 1, 0, 300, 0, 300)
for i, j in ville:
    GEO2[i][j] = 90

g2 = Grille(300, GEO2, 10000000)
g2.cellules[150][150].repartition[1] += 30000
g2.cellules[150][150].population += 30000

virus = [0.6, 0.5, 0.3]

statistiques_2(g2, virus)