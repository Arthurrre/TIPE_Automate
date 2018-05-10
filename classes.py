import random

# Repartition est [Sain, Malade, Mort, Gueri]
# Population est malade + sain + gueri


class Cellule:
    def __init__(self, population, prob_mvt, coeff_attractivite):
        self.population = population
        self.repartition = [population, 0, 0, 0]
        self.prob_mvt = prob_mvt
        self.coeff_attractivite = coeff_attractivite

    def repartition_pr(self):
        repartition_pourcentage = []
        for i in self.repartition:
            repartition_pourcentage.append(i / sum(self.repartition))

        return repartition_pourcentage

    # virus = [proba_infection, proba_mort, proba_soin]
    def changement_interne(self, virus):
        ancien_etat = self.repartition.copy()
        if self.population == 0:
            self.repartition[1] = 0
        else :
<<<<<<< HEAD
            self.repartition[1] += (ancien_etat[0] *
                                   virus[0] * self.repartition[1] / self.population)
        self.repartition[0] = ancien_etat[0] + \
            ancien_etat[1] - self.repartition[1]
=======
            self.repartition[1] += int(ancien_etat[0] * virus[0] * ancien_etat[1] / self.population)
        self.repartition[0] = ancien_etat[0] + ancien_etat[1] - self.repartition[1]
>>>>>>> d116b173577508c28836276cee850ed9c5a71f8e

    # On calcule les morts avant les gueris car, je cite "mourir c'est plus rapide que guerir"

        self.repartition[2] += int(ancien_etat[1] * virus[1])
        self.repartition[3] += int(self.repartition[1] * virus[2])
        self.repartition[1] = sum(ancien_etat[1:]) - sum(self.repartition[1:3])


campagne = 3
ville = 90
route = 0
montagne = 2


def cases_touchees(x, y, rayon, minx, maxx, miny, maxy):
    coords = []

    for i in range(max(minx, x - rayon), min(maxx, x + rayon + 1)):
        for j in range(max(miny, y - rayon), min(maxy, y + rayon + 1)):
            if j == y and i == x:
                continue
            coords.append((i, j))

    return coords


def choix_proba(liste_proba):
    r = random.random()
    somme_cumulée = 0
    for i in range(len(liste_proba)):
        somme_cumulée += liste_proba[i]
        if r >= somme_cumulée:
            return i

    return 0


class Grille:
    # Geographie c'est une grille de valeur discretes décrivant l'environnement
    # 3 -> campagne
    # 90 -> ville
    # 0 -> routes
    # 2 -> montagnes

    def __init__(self, taille, geographie, population_totale):
        self.taille = taille
        self.population_initiale = population_totale
        total_geo = sum([item for sublist in geographie for item in sublist])
        self.cellules = []
        for i in range(taille):
            sous_liste = []
            for j in range(taille):
                if(geographie[i][j] == campagne):
                    attractivite = 0.1
                    proba_mvt = 0.001
                elif(geographie[i][j] == ville):
                    attractivite = 0.3
                    proba_mvt = 0.01
                elif(geographie[i][j] == route):
                    attractivite = 0.6
                    proba_mvt = 1
                elif(geographie[i][j] == montagne):
                    attractivite = 0.1
                    proba_mvt = 0.002

                # On ajoute une part d'aléatoire dans la répartition de la population

                sous_liste.append(
                    Cellule(int(population_totale * geographie[i][j] / total_geo * random.uniform(0.98, 1.02)), proba_mvt, attractivite))

            self.cellules.append(sous_liste)

    def next(self, virus):
        nouvelle_cellules = self.cellules.copy()
        # On commence par calculer les mouvements de population

        for i in range(len(self.cellules)):
            for j in range(len(self.cellules[i])):
                nouvelle_cellules[i][j].changement_interne(virus)
                population_partie = self.cellules[i][j].population * self.cellules[i][j].prob_mvt
                

                nouvelle_cellules[i][j].population -= population_partie
                # Choix de la case où la population part
                voisins = cases_touchees(i, j, 1, 0, self.taille, 0, self.taille)

                liste_probas = [self.cellules[x][y].coeff_attractivite for x, y in voisins]

                for k in range(len(liste_probas)):
                    liste_probas[k] /= sum(liste_probas)

                x, y = voisins[choix_proba(liste_probas)]
                nouvelle_cellules[x][y].population += population_partie
                nouvelle_cellules[x][y].repartition[0] += int(population_partie * self.cellules[i][j].repartition_pr()[0])
                nouvelle_cellules[x][y].repartition[1] += int(population_partie * self.cellules[i][j].repartition_pr()[1])
                nouvelle_cellules[x][y].repartition[1] += int(population_partie * self.cellules[i][j].repartition_pr()[3])
                if nouvelle_cellules[x][y].repartition[1] < 0:
                    print(nouvelle_cellules[x][y].repartition)
                    print(self.cellules[i][j].repartition_pr())
            

        self.cellules = nouvelle_cellules


def grille_pop(g):
    L = []
    for i in range(len(g.cellules)):
        D = []
        for j in range(len(g.cellules[0])):
            D.append(int(g.cellules[i][j].population))
        L.append(D)
    return L


if __name__ == '__main__':
    GEO = [[3, 3, 3], [3, 90, 3], [3, 3, 3]]
    GEO2 = [[3 for i in range(100)] for j in range(100)]
    g = Grille(100, GEO2, 10000000)
    print(grille_pop(g))
    virus = [1, 1, 0.2]
