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
import copy
##


proba_infection = 0.2
proba_mort = 0.25
proba_soin = 0.1
rayon_infection = 2

min_etape = 200
max_etape = 1000

def compte(grille):
    compteur = [0, 0, 0, 0]
    for i in range(grille.taille):
        for j in range(len(grille.cellules[i])):
            for k in range(len(grille.cellules[i][j].repartition)):
                compteur[k] += grille.cellules[i][j].repartition[k]

    return compteur


def statistiques_final(grille, virus, quantite):

    # Ces variables sont des listes de listes, qui contiennent la variation de la population
    # au cours du temps, pour chaque itération

    sains = []
    infectes = []
    morts = []
    soignes = []

    for i in range(quantite):
        nouvelle_grille = copy.deepcopy(grille)
        sain, infecte, mort, soigne = statistiques_liste(nouvelle_grille, virus)
        sains.append(sain)
        infectes.append(infecte)
        morts.append(mort)
        soignes.append(soigne)
    
    return sains, infectes, morts, soignes
        

def statistiques_liste(grille, virus):
    k = 0
    stats = []
    while compte(grille)[1] !=0:
        k += 1
        stats.append(grille.stats())
        grille.next(virus)
        if k > max_etape:
            break
    
    return zip(*stats)i


def statistiques_courbe(grille, virus):
    r = list(statistiques_liste(grille, virus))
    sains, infectes, morts, soignes = r[0], r[1], r[2], r[3]
    fig = plt.figure()
    fig.suptitle('Évolution de la population en fonction du temps', fontsize=14)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Jours')
    ax.set_ylabel('Individus')

    etapes = np.array(range(len(sains)))

<<<<<<< HEAD
    sains_courbe, = plt.plot(etapes, sains, 'b', label='Sains')
    infectes_courbe, = plt.plot(etapes, infectes, 'r', label='Infectés')
    morts_courbe, = plt.plot(etapes, morts, 'k', label='Retraités')
    # soignes_courbe, = plt.plot(etapes, soignes, 'g', label='Soignés')
=======
    sains_courbe, = plt.plot(etapes, sains,'b', label='Sains')
    infectes_courbe, = plt.plot(etapes, infectes,'r', label='Infectés')
    morts_courbe, = plt.plot(etapes, morts,'k', label='Morts')
    soignes_courbe, = plt.plot(etapes, soignes,'g', label='Soignés')
>>>>>>> 0cfda680a880b2d1abb4649042284d8e0ef88b67

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()


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
            if intensite == 0:
                im.putpixel((i, j), (255,255,255))
            if intensite > 255:
                intensite = 255
            if intensite > 0:
                im.putpixel((i, j), (255, 255-intensite, 255-intensite))
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
    while compte(grille)[1] != 0:
        k += 1
        
        im = transition_image_sains(grille, im, coeff)
        im.save( str(k)+'_sains'+'.png')
        gif.append( str(k)+'_sains'+'.png')
        grille.next(virus)
        if k > max_etape:
            break
        if compte(grille)[0] == 0:
            break
    return gif

def simulation_image_malades(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//(3*grille.taille)**2
    coeff = 127/moyenne 
    print(coeff)
    print(moyenne)
    while compte(grille)[1] != 0:
        k += 1
        if sum(compte(grille)) > 2 * grille.population_initiale:
            print(compte(grille))
            print(k)
        im = transition_image_malades(grille, im, coeff)
        im.save( str(k)+'_malades'+'.png')
        gif.append( str(k)+'_malades'+'.png')
        grille.next(virus)
        if k > max_etape:
            print(population(grille))
            break
    print(population(grille),k)
    return gif

def simulation_image_morts(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    while compte(grille)[1] != 0:
        k += 1
        
        im = transition_image_morts(grille, im, coeff)
        im.save( str(k)+'_morts'+'.png')
        gif.append( str(k)+'_morts'+'.png')
        grille.next(virus)
        if k > max_etape:
            break
    return gif

def simulation_image_gueris(grille, virus):
    im = init_im(grille.taille)
    gif = []
    k = 0
    moyenne = grille.population_initiale//grille.taille**2
    coeff = 127/moyenne 
    while compte(grille)[1] != 0:
        k += 1
        
        im = transition_image_gueris(grille, im, coeff)
        im.save( str(k)+'_gueris'+'.png')
        gif.append( str(k)+'_gueris'+'.png')
        grille.next(virus)
        if k > max_etape:
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
    output_file =   name + '-' + etat + '-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    if images != []:
        imageio.mimsave(output_file, images, duration=duration)

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