import math
import random
import matplotlib.pyplot as plt
import numpy as np
proba_infection = 0.0375
proba_mort = 0.001
proba_soin = 0.2
rayon_infection = 1 

def init_grid(size):
    G = []
    for i in range(size):
        sG = []
        for j in range(size):
            sG.append(0)
        G.append(sG)
    G[size // 2][size // 2] = 1
    return G


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
# contacts avec des infectés et une probabilité dépendante de la maladie, ainsi que
# de la densité de population

def calcul_proba_infection(contacts, rayon, base_proba, i, j):
    return contacts * base_proba


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


def etat_suivant(grille, virus, rayon):
    G = init_grid(len(grille))
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                contacts = contact(grille, i, j)
                G[i][j] = binomial(calcul_proba_infection(contacts, rayon, virus[0], i, j))
            elif grille[i][j] == 1:
                G[i][j] = mort_ou_soigne(virus[1], virus[2])
            else:
                G[i][j] = grille[i][j]

    return G


def compte(grille):
    compteur = [0, 0, 0, 0]
    for i in grille:
        for j in i:
            compteur[j] += 1

    return compteur


def print_grille(grille):
    for i in grille:
        print(i)


def simulation(taille, virus, rayon):
    grille = init_grid(taille)
    etape = 0
    while compte(grille)[1] != 0:
        etape += 1
        grille = etat_suivant(grille, virus, rayon)

    return etape, compte(grille)


def statistiques(taille, echantillon, virus, rayon):
    etapes = []
    comptes = []

    for i in range(echantillon):
        etape, compte = simulation(taille, virus, rayon)
        etapes.append(etape)
        comptes.append(compte)

    sains, infectes, morts, soignes = zip(*comptes)
    return sains, infectes, morts, soignes


def courbe(taille, virus, rayon):
    grille = init_grid(taille)
    etape = 0
    suivi = [0]
    sains = [taille**2-1]
    infectes = [1]
    morts = [0]
    soignes = [0]
    while compte(grille)[1] != 0:
        etape += 1
        suivi.append(etape)
        sains.append(0)
        infectes.append(0)
        morts.append(0)
        soignes.append(0)
        for i in range(taille):
            for j in range(taille):
                if grille[i][j] == 0:
                    sains[etape] += 1
                elif grille[i][j] == 1:
                    infectes[etape] += 1
                elif grille[i][j] == 2:
                    morts[etape] += 1
                else :
                    soignes[etape] += 1
        grille = etat_suivant(grille, virus, rayon)

    fig = plt.figure()
    fig.suptitle('Evolution de la population en fonction du nombre d\'étapes', fontsize=14)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Etapes')
    ax.set_ylabel('Individus')

    etapes = np.array(range(len(sains)))

    sains_courbe, = plt.plot(suivi, sains, label='Sains')
    infectes_courbe, = plt.plot(suivi, infectes, label='Infectés')
    morts_courbe, = plt.plot(suivi, morts, label='Morts')
    soignes_courbe, = plt.plot(suivi, soignes, label='Soignés')

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()


def ancienne_simulation_image(taille):
    im = init_im(taille)
    grille = init_grid(taille)
    etape = 0
    plt.imshow(im)
    plt.show
    gif=[]
    k=0
    while compte(grille)[1] != 0:
        k+=1
        grille = etat_suivant(grille)
        im = transition(grille,im)
        im.save(str(k)+'.png')
        gif.append(str(k)+'.png')
    im = transition(grille,im)
    plt.imshow(im)
    plt.show()
    return gif
    

def ancien_create_gif(filenames, duration,name):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = name + '-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images, duration=duration)