import copy
import numpy as np
import matplotlib.pyplot as plt
proba_infection = 0.05
proba_mort = 0.001
proba_soin = 0.2
virus =[proba_infection, proba_mort, proba_soin]

def deriver(y, virus):
    proba_infection = virus[0]
    proba_mort = virus[1]
    proba_soin = virus[2]
    
    sain, malade, soigne, mort = y
    dsain = -proba_infection * sain * malade
    dmalade = proba_infection * sain * malade - proba_mort * malade - proba_soin * malade
    dsoigne = proba_soin * malade
    dmort = proba_mort * malade

    return [dsain, dmalade, dsoigne, dmort] 


def suivant(y_n, virus, pas): 
    k_1 = deriver(y_n, virus)

    y_n_k_2 = [y_n[i] + (pas/2) * k_1[i] for i in range(len(y_n))]
    k_2 = deriver(y_n_k_2, virus)

    y_n_k_3 = [y_n[i] + (pas/2) * k_2[i] for i in range(len(y_n))]
    k_3 = deriver(y_n_k_3,virus )

    y_n_k_4 = [y_n[i] + pas * k_3[i] for i in range(len(y_n))]
    k_4 = deriver(y_n_k_4, virus)

    return [y_n[i] + (1/6) * (k_1[i] + 2*k_2[i] + 2*k_3[i] + k_4[i]) for i in range(len(y_n))]
    
def simulation_differentielle(virus, pas):
    L=[]
    y =(99990,10,0,0)
    while y[1] > 10**-1:
        L.append(copy.deepcopy(y))
        y = suivant(y, virus, pas)
    return L

def courbe_differentielle(virus, pas):
    resultat = simulation_differentielle(virus, pas)
    suivi =[]
    for i in range(len(resultat)):
        suivi.append(i)
    fig = plt.figure()
    fig.suptitle('Evolution de la population en fonction du temps', fontsize=14)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('Jours')
    ax.set_ylabel('Individus')
    
    print(len(resultat))
    
    etapes = np.array(range(len(resultat)))
    a,b,c,d = zip(*resultat)
    
    sains_courbe, = plt.plot(suivi, a, label='Sains')
    infectes_courbe, = plt.plot(suivi, b, label='Infectés')
    morts_courbe, = plt.plot(suivi, c, label='Morts')
    soignes_courbe, = plt.plot(suivi, d, label='Soignés')

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()