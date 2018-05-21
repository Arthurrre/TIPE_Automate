import random
import copy

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
    
    def repartition_pr_vivant(self):
        repartition_pourcentage = []
        for i in self.repartition:
            if self.population == 0:
                repartition_pourcentage.append(0)
            else :
                repartition_pourcentage.append(i / self.population)

        return repartition_pourcentage

    # virus = [proba_infection, proba_mort, proba_soin]
    def changement_interne(self, virus):
        self.population = self.repartition[0] + self.repartition[1] + self.repartition[3]
        ancien_etat = copy.copy(self.repartition)
        # On calcule les infectés
        if self.population == 0:
            self.repartition[1] = 0
            self.repartition[0] = 0
            self.repartition[3] = 0
            print("Pas très normal que ça s'affiche.")
            return
        else :
            self.repartition[1] += int(ancien_etat[0] * virus[0])
            self.repartition[0] = ancien_etat[0] +  ancien_etat[1] - self.repartition[1]

        # On calcule les morts avant les gueris car, je cite "mourir c'est plus rapide que guerir"

        self.repartition[2] += int(self.repartition[1] * virus[1])
        self.repartition[1] -= int(self.repartition[1] * virus[1])

        self.repartition[3] += int(self.repartition[1] * virus[2])
        self.repartition[1] -= int(self.repartition[1] * virus[2])
        
        self.population = self.repartition[0] + self.repartition[1] + self.repartition[3]



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
        if r <= somme_cumulée:
            return i

    return random.choice(list(range(len(liste_proba))))


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
                    attractivite = 0.01
                    proba_mvt = 0.01
                elif(geographie[i][j] == ville):
                    attractivite = 0.3
                    proba_mvt = 0.5
                elif(geographie[i][j] == route):
<<<<<<< HEAD
                    attractivite = 0.7
                    proba_mvt = 0.7
=======
                    attractivite = 0.9
                    proba_mvt = 1
>>>>>>> 9472ede8ce95fbcf2c89be2c7c263bff34fd6bd0
                elif(geographie[i][j] == montagne):
                    attractivite = 0.1
                    proba_mvt = 0.1

                # On ajoute une part d'aléatoire dans la répartition de la population

                sous_liste.append(Cellule(int(population_totale * geographie[i][j] / total_geo * random.uniform(0.98, 1.02)), proba_mvt, attractivite))

            self.cellules.append(sous_liste)

    def next(self, virus):
        nouvelle_cellules = copy.deepcopy(self.cellules)
        print(grille_pop_sum(self))
        for i in range(len(self.cellules)):
            for j in range(len(self.cellules[i])):
                # Calcul de la population partie

                repartitions = self.cellules[i][j].repartition_pr_vivant()
                population_partie = int(self.cellules[i][j].population * self.cellules[i][j].prob_mvt)
                nouvelle_cellules[i][j].population -= population_partie

                # On répartit les pertes de population
                nouvelle_cellules[i][j].repartition[0] = int(nouvelle_cellules[i][j].population * repartitions[0])
                nouvelle_cellules[i][j].repartition[1] = int(nouvelle_cellules[i][j].population * repartitions[1])
                nouvelle_cellules[i][j].repartition[3] = int(nouvelle_cellules[i][j].population * repartitions[3])


                # Choix de la case où la population part
                voisins = cases_touchees(i, j, 1, 0, self.taille, 0, self.taille)

                liste_probas = [self.cellules[x][y].coeff_attractivite for x, y in voisins]
                nouvelle_liste_probas = []
                
                for k in range(len(liste_probas)):
                    nouvelle_liste_probas.append(liste_probas[k]/sum(liste_probas))

                x, y = voisins[choix_proba(nouvelle_liste_probas)]
                nouvelle_cellules[x][y].population += population_partie
                nouvelle_cellules[x][y].repartition[0] += int(population_partie * repartitions[0])
                nouvelle_cellules[x][y].repartition[1] += int(population_partie * repartitions[1])
                nouvelle_cellules[x][y].repartition[3] += int(population_partie * repartitions[3])
        
        self.cellules = nouvelle_cellules

        for i in range(len(self.cellules)):
            for j in range(len(self.cellules)):
                self.cellules[i][j].changement_interne(virus)

        print(grille_pop_sum(self))

    def stats(self):
        valeur_de_retour = [0, 0, 0, 0]
        for ligne in self.cellules:
            for cellule in ligne:
                for i in range(4):
                    valeur_de_retour[i] += cellule.repartition[i]
        return valeur_de_retour

def grille_pop(g):
    L = []
    for i in range(len(g.cellules)):
        D = []
        for j in range(len(g.cellules[0])):
            D.append(int(g.cellules[i][j].population))
        L.append(D)
    return L


def grille_pop_sum(g):
    somme = 0
    for i in range(len(g.cellules)):
        for j in range(len(g.cellules)):
            somme += g.cellules[i][j].population
    
    return somme
        