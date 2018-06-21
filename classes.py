import random
import copy

# Repartition est [Sain, Malade, Mort, Gueri]
# Population est malade + sain + gueri


campagne = 3
ville = 90
route = 0
montagne = 2

class Cellule:
    def __init__(self, population, prob_mvt, coeff_attractivite):
        self.repartition = [population, 0, 0, 0]
        self.prob_mvt = prob_mvt
        self.coeff_attractivite = coeff_attractivite

    def population(self):
        return self.repartition[0] + self.repartition[1]+ self.repartition[3]

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
                repartition_pourcentage.append(i / self.population())

        return repartition_pourcentage

    # virus = [proba_infection, proba_mort, proba_soin]
    def changement_interne(self, virus):
        ancien_etat = copy.copy(self.repartition)
        # On calcule les infectés
        if self.repartition[1] != 0:
            self.repartition[1] += int(ancien_etat[0] * virus[0])
            self.repartition[0] = ancien_etat[0] +  ancien_etat[1] - self.repartition[1]

        # On calcule les morts avant les gueris

        self.repartition[2] += int(self.repartition[1] * virus[1])
        if int(self.repartition[1]*virus[1])==0 and self.repartition[1] >= 1 :
            self.repartition[2] += 1
            self.repartition[1] -=1
        self.repartition[1] -= int(self.repartition[1] * virus[1])
        self.repartition[3] += int(self.repartition[1] * virus[2])
        if int(self.repartition[1]*virus[2])==0 and self.repartition[1] >= 1 :
            self.repartition[3] += 1
            self.repartition[1] -=1
        self.repartition[1] -= int(self.repartition[1] * virus[2])


# Fonctions auxilliaires servant à la classe grille.

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
                    attractivite = 0.2
                    proba_mvt = 0.2
                elif(geographie[i][j] == ville):
                    attractivite = 0.5
                    proba_mvt = 0.3
                elif(geographie[i][j] == route):
                    attractivite = 0.7
                    proba_mvt = 0.7
                elif(geographie[i][j] == montagne):
                    attractivite = 0.1
                    proba_mvt = 0.1

                # On ajoute une part d'aléatoire dans la répartition de la population

                sous_liste.append(Cellule(int(population_totale * geographie[i][j] / total_geo * random.uniform(0.98, 1.02)), proba_mvt, attractivite))

            self.cellules.append(sous_liste)

    def next(self, virus):
        # On applique d'abord les changements relatifs à la maladie.
        for i in range(len(self.cellules)):
            for j in range(len(self.cellules)):
                self.cellules[i][j].changement_interne(virus)

        # On calcule ensuite les mouvements de population
        nouvelle_cellules = copy.deepcopy(self.cellules)

        for i in range(len(self.cellules)):
            for j in range(len(self.cellules[i])):
                repartitions = self.cellules[i][j].repartition_pr_vivant()
                # Calcul de la population partie de la case (i, j)

                population_partie = int(self.cellules[i][j].population() * self.cellules[i][j].prob_mvt)

                # On répartit les pertes de population

                sains_partis = int(population_partie * repartitions[0])
                malades_partis = int(population_partie * repartitions[1])
                soignes_partis = int(population_partie * repartitions[3])

                nouvelle_cellules[i][j].repartition[0] -= sains_partis
                nouvelle_cellules[i][j].repartition[1] -= malades_partis
                nouvelle_cellules[i][j].repartition[3] -= soignes_partis


                # Choix de la case où la population part
                # Ici le rayon vaut 1 car on considére que les populations ne peuvent, par exemple
                # prendre l'avion.
                voisins = cases_touchees(i, j, 1, 0, self.taille, 0, self.taille)

                liste_probas = [self.cellules[x][y].coeff_attractivite for x, y in voisins]
                nouvelle_liste_probas = []
                
                # On recalcule les probas afin que la somme des probas fasse 1.

                for k in range(len(liste_probas)):
                    nouvelle_liste_probas.append(liste_probas[k]/sum(liste_probas))

                x, y = voisins[choix_proba(nouvelle_liste_probas)]
 
                nouvelle_cellules[x][y].repartition[0] += sains_partis
                nouvelle_cellules[x][y].repartition[1] += malades_partis
                nouvelle_cellules[x][y].repartition[3] += soignes_partis
        
        self.cellules = nouvelle_cellules


    def stats(self):
        valeur_de_retour = [0, 0, 0, 0]
        for ligne in self.cellules:
            for cellule in ligne:
                for i in range(4):
                    valeur_de_retour[i] += cellule.repartition[i]
        return valeur_de_retour


# Fonctions utilisées pour débugger.

def grille_pop(g):
    L = []
    for i in range(len(g.cellules)):
        D = []
        for j in range(len(g.cellules[0])):
            D.append(int(g.cellules[i][j].population()))
        L.append(D)
    return L


def grille_pop_sum(g):
    somme = 0
    for i in range(len(g.cellules)):
        for j in range(len(g.cellules)):
            somme += g.cellules[i][j].population()
    
    return somme