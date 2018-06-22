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
for i in range(10):
    ancien_automate.old_create_gif(ancien_automate.old_simulation_image(taille_grille, ebola, rayon_normal), 0.01, "ebola" + str(i+1))