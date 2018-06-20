from tipe_en_cours import *
from classes import *
import ancien_automate
import pickle

taille_grille = 50
population_initiale = 1000000000
malades_initiaux = 300
x_malade_initial = 25
y_malade_initial = 25

ebola = [0.0187, 0.0818, 0.00909]
grippe = [0.406, 0.0002, 0.1998]
rayon_normal = 1

virus_colore = [0.2, 0.25, 0.2]
rayon_virus_colore = 2

# Vieux gifs

ancien_automate.old_create_gif(ancien_automate.old_simulation_image(taille_grille, ebola, rayon_normal), 0.01, "ebola1")
ancien_automate.old_create_gif(ancien_automate.old_simulation_image(taille_grille, grippe, rayon_normal), 0.01, "grippe1")
ancien_automate.old_create_gif(ancien_automate.old_simulation_image(taille_grille, virus_colore, rayon_virus_colore), 0.01, "colore")

# Nombre moyen d'étapes

nom_fichier = "1er_automate_ebola.pickle"

sains, malades, morts, soignes = ancien_automate.old_statistiques_liste(taille_grille, 1000, ebola, rayon_normal)

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)


nom_fichier = "1er_automate_grippe.pickle"

sains, malades, morts, soignes = ancien_automate.old_statistiques_liste(taille_grille, 1000, grippe, rayon_normal)

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)

GEO2 = [[3 for i in range(taille_grille)] for j in range(taille_grille)]

# On fait varier le nombre de villes

# Une seule ville

ville = cases_touchees(25, 25, 2, 0, taille_grille, 0, taille_grille)

for x, y in ville:
    GEO2[x][y] = 90

g = Grille(taille_grille, GEO2, population_initiale)
create_gif("malade", g, ebola, 0.01, "1_ville_malade")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("sain", g, ebola, 0.01, "1_ville_sain")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("gueri", g, ebola, 0.01, "1_ville_gueri")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("mort", g, ebola, 0.01, "1_ville_mort")


g.cellules[x_malade_initial][y_malade_initial].repartition[1] += malades_initiaux

sains, malades, morts, soignes = statistiques_final(g, ebola, 100)

nom_fichier = "1_ville_repartitions.pickle"

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)

# Deux villes

ville = cases_touchees(13, 13, 2, 0, taille_grille, 0, taille_grille)

for x, y in ville:
    GEO2[x][y] = 90

g = Grille(taille_grille, GEO2, population_initiale)
create_gif("malade", g, ebola, 0.01, "2_ville_malade")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("sain", g, ebola, 0.01, "2_ville_sain")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("gueri", g, ebola, 0.01, "2_ville_gueri")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("mort", g, ebola, 0.01, "2_ville_mort")

g = Grille(taille_grille, GEO2, population_initiale)
g.cellules[x_malade_initial][y_malade_initial].repartition[1] += malades_initiaux


sains, malades, morts, soignes = statistiques_final(g, ebola, 100)

nom_fichier = "2_ville_repartitions.pickle"

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)

# Trois villes

ville = cases_touchees(14, 42, 2, 0, taille_grille, 0, taille_grille)

for x, y in ville:
    GEO2[x][y] = 90

g = Grille(taille_grille, GEO2, population_initiale)
create_gif("malade", g, ebola, 0.01, "3_ville_malade")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("sain", g, ebola, 0.01, "3_ville_sain")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("gueri", g, ebola, 0.01, "3_ville_gueri")
g = Grille(taille_grille, GEO2, population_initiale)
create_gif("mort", g, ebola, 0.01, "3_ville_mort")

g = Grille(taille_grille, GEO2, population_initiale)
g.cellules[x_malade_initial][y_malade_initial].repartition[1] += malades_initiaux

sains, malades, morts, soignes = statistiques_final(g, ebola, 100)

nom_fichier = "3_ville_repartitions.pickle"

with open(nom_fichier, 'wb') as handle:
    pickle.dump([sains, malades, morts, soignes], handle, protocol=pickle.HIGHEST_PROTOCOL)