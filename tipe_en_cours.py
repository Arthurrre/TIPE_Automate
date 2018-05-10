import random
import numpy as np
import imageio
import sys
import datetime
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from scipy import ndimage
import math
import os

##

proba_infection = 0.2
proba_mort = 0.25
proba_soin = 0.1
rayon_infection = 2


def init_grid(size):
   # G = []
    # for i in range(size):
     #   sG = []
      #  for j in range(size):
       #     sG.append(0)
        # G.append(sG)
    #G[size // 2][size // 2] = 1
    # return G
    GEO = [[3, 3, 3], [3, 90, 3], [3, 3, 3]]
    g = Grille(3, GEO, 10000000)
    return g


def cases_touchees(x, y, rayon, minx, maxx, miny, maxy):
    coords = []

    for i in range(max(minx, x - rayon), min(maxx, x + rayon + 1)):
        for j in range(max(miny, y - rayon), min(maxy, y + rayon + 1)):
            if j == y and i == x:
                continue
            coords.append((i, j))

    return coords


def contact(grille, i, j):
    compteur = 0
    for i in cases_touchees(i, j, rayon_infection, 0, len(grille), 0, len(grille[0])):
        if grille[i[0]][i[1]] == 1:
            compteur += 1

    return compteur


# Cette fonction retourne la probabilité d'être infecté, dépendant du nombre de
# contacts avec des infectés et une probabilité dépendante de la maladie

def calcul_proba_infection(contacts, rayon, base_proba):
    max_contact = (1 + 2 * rayon)**2 - 1
    return base_proba * math.log(1 + contacts) / math.log(1 + max_contact)


def binomial(p):
    if random.random() <= p:
        return 1
    return 0


def mort_ou_soigne(p1, p2):
    if random.random() <= p1:
        return 2
    if random.random() <= p2:
        return 3
    return 1


def etat_suivant(grille):
    G = init_grid(len(grille))
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                contacts = contact(grille, i, j)
                G[i][j] = binomial(calcul_proba_infection(
                    contacts, rayon_infection, proba_infection))
            elif grille[i][j] == 1:
                G[i][j] = mort_ou_soigne(proba_mort, proba_infection)
            else:
                G[i][j] = grille[i][j]

    return G


def compte(grille):
    compteur = [0, 0, 0, 0]
    for i in range(grille.taille):
        for j in range(len(grille.cellules[i])):
            for k in range(len(grille.cellules[i][j].repartition)):
                compteur[k] += grille.cellules[i][j].repartition[k]

    return compteur


def print_grille(grille):
    for i in grille:
        print(i)


def simulation(taille):
    grille = init_grid(taille)
    etape = 0
    while compte(grille)[1] != 0:
        etape += 1
        grille = etat_suivant(grille)

    return etape, compte(grille)


def statistiques(taille, echantillon):
    etapes = []
    comptes = []

    for i in range(echantillon):
        etape, compte = simulation(taille)
        etapes.append(etape)
        comptes.append(compte)
        print(i)

    sains, infectes, morts, soignes = zip(*comptes)
    print('Moyenne = {}'.format(sum(etapes) / len(etapes)))
    print('Max = {}'.format(max(etapes)))
    print('Sains:\n\tMoyenne =  {}'.format(sum(sains) / len(sains)))
    print('\tMax =  {}'.format(max(sains)))
    print('\tMin =  {}'.format(min(sains)))
    print('Infectés:\n\tMoyenne =  {}'.format(sum(infectes) / len(infectes)))
    print('\tMax =  {}'.format(max(infectes)))
    print('\tMin =  {}'.format(min(infectes)))
    print('Morts:\n\tMoyenne =  {}'.format(sum(morts) / len(morts)))
    print('\tMax =  {}'.format(max(morts)))
    print('\tMin =  {}'.format(min(morts)))
    print('Soignés:\n\tMoyenne =  {}'.format(sum(soignes) / len(soignes)))
    print('\tMax =  {}'.format(max(soignes)))
    print('\tMin =  {}'.format(min(soignes)))


def init_im(taille):
    im = Image.new("RGB", (taille, taille), "white")
    return im


def transition_image_sains(grille, im):
    moyenne = grille.population_initiale//grille.taille
    coeff = 127/moyenne
    for i in range(grille.taille):
        for j in range(grille.taille):
            intensite = int(grille.cellules[i][j].repartition[0]*coeff)
            if intensite > 255:
                intensite = 255
            im.putpixel((i, j), (255, 255-intensite, 255))
    return im


def simulation_image_sains(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    while compte(grille)[0] != 0:
        k += 1
        grille.next(virus)
        im = transition_image_sains(grille, im)
        im.save(str(k)+'_sains'+'.png')
        gif.append(str(k)+'_sains'+'.png')
        if k > 10000:
            break
    return gif


def create_gif_sains(filenames, duration, name):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = name + 'sains' + \
        '-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images, duration=duration)
