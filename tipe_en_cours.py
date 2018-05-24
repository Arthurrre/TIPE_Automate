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

from classes import *
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


def statistiques_2(grille, virus):
    k = 0
    stats = []
    while compte(grille)[1] != 0:
        k += 1
        print(grille_pop_sum(grille))
        stats.append(grille.stats())
        grille.next(virus)
        if k > 99:
            break
    sains, infectes, morts, soignes = zip(*stats)
    fig = plt.figure()
    fig.suptitle('Evolution de la population en fonction du nombre d\'étapes', fontsize=14)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Etapes')
    ax.set_ylabel('Individus')

    etapes = np.array(range(len(sains)))

    sains_courbe, = plt.plot(etapes, sains, label='Sains')
    infectes_courbe, = plt.plot(etapes, infectes, label='Infectés')
    morts_courbe, = plt.plot(etapes, morts, label='Morts')
    soignes_courbe, = plt.plot(etapes, soignes, label='Soignés')

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()


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


def transition_image_sains(grille, im, coeff):
    for i in range(grille.taille):
        for j in range(grille.taille):
            intensite = int(grille.cellules[i][j].repartition[0]*coeff)
            if intensite < 0:
                intensite = 0
            if intensite > 255:
                intensite = 255
            im.putpixel((i, j), (intensite, intensite, intensite))
    return im

def transition_image_malades(grille, im, coeff):
    for i in range(grille.taille):
        for j in range(grille.taille):
            intensite = int(grille.cellules[i][j].repartition[1]*coeff)
            if intensite < 0:
                intensite = 0
            if intensite > 255:
                intensite = 255
            im.putpixel((i, j), (intensite, 0, 0))
    return im

def transition_image_morts(grille, im, coeff):
    for i in range(grille.taille):
        for j in range(grille.taille):
            intensite = int(grille.cellules[i][j].repartition[2]*coeff)
            if intensite < 0:
                intensite = 0
            if intensite > 255:
                intensite = 255
            im.putpixel((i, j), (intensite, 0, intensite))
    return im

def transition_image_gueris(grille, im, coeff):
    for i in range(grille.taille):
        for j in range(grille.taille):
            intensite = int(grille.cellules[i][j].repartition[3]*coeff)
            if intensite < 0:
                intensite = 0
            if intensite > 255:
                intensite = 255
            im.putpixel((i, j), (0, intensite, 0))
    return im

def simulation_image_sains(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    print(moyenne,coeff)
    while compte(grille)[1] != 0:
        print(population(g)[0])
        k += 1
        
        im = transition_image_sains(grille, im, coeff)
        im.save("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_sains'+'.png')
        gif.append("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_sains'+'.png')
        grille.next(virus)
        if k > 9999:
            break
        if compte(grille)[0] == 0:
            break
    return gif

def simulation_image_malades(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    print(moyenne,coeff)
    while compte(grille)[1] != 0:
        k += 1
        if sum(compte(grille)) > 10000000:
            print(compte(grille))
            print(k)
        im = transition_image_malades(grille, im, coeff)
        im.save("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_malades'+'.png')
        gif.append("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_malades'+'.png')
        grille.next(virus)
        if k > 9999:
            break
    return gif

def simulation_image_morts(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    print(moyenne,coeff)
    while compte(grille)[1] != 0:
        k += 1
        
        im = transition_image_morts(grille, im, coeff)
        im.save("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_morts'+'.png')
        gif.append("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_morts'+'.png')
        grille.next(virus)
        if k > 9999:
            break
    return gif

def simulation_image_gueris(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    print(moyenne,coeff)
    while compte(grille)[1] != 0:
        k += 1
        
        im = transition_image_gueris(grille, im, coeff)
        im.save("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_gueris'+'.png')
        gif.append("D:\\autres\\Me\\Github\\pics\\"+str(k)+'_gueris'+'.png')
        grille.next(virus)
        if k > 9999:
            break
    return gif


def create_gif(etat, grille, virus, duration, name):
    images = []
    if etat == "sain":
        filenames = simulation_image_sains(grille, virus)
    elif etat == "malade":
        filenames = simulation_image_malades(grille, virus)
    elif etat == "mort":
        filenames = simulation_image_morts(grille, virus)
    elif etat == "gueri":
        filenames = simulation_image_gueris(grille, virus)
    else:
        return("etat incorrect")
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = "D:\\autres\\Me\\Github\\pics\\"+ name + '-' + etat + '-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images, duration=duration)

##
if __name__ == '__main__':
    #GEO2 = [[3 for i in range(100)] for j in range(100)]
    g = Grille(100, GEO2, 1000000)
    g.cellules[50][50].repartition[1] += 300
    g.cellules[50][50].population += 300

    virus = [1, 0.1, 0.1]
##
def population (grille):
    S=0
    Ma=0
    Mo=0
    G=0
    for i in range(grille.taille):
        for j in range(grille.taille):
            S+= grille.cellules[i][j].repartition[0]
            Ma+= grille.cellules[i][j].repartition[1]
            Mo+= grille.cellules[i][j].repartition[2]
            G+= grille.cellules[i][j].repartition[3]
    return (S,Ma,Mo,G,S+Ma+Mo+G)

def verif_geo(geo):
    im = Image.new("RGB", (len(geo), len(geo)), "white")
    for i in range(len(geo)):
        for j in range(len(geo)):
            if geo[i][j] == 90:
                im.putpixel((j, i), (200, 0, 0))
            elif geo[i][j] == 0:
                im.putpixel((j, i), (0, 0, 0))
            elif geo[i][j] == 2:
                im.putpixel((j, i), (100, 90, 100))
    plt.imshow(im)
    plt.show()