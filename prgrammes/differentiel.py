import copy
import numpy as np
import matplotlib.pyplot as plt

def deriver(y, virus):
    proba_infection = virus[0]
    proba_mort = virus[1]
    proba_soin = virus[2]
    
    sain, malade, soigne, mort = y
    total = sain + malade + mort + soigne
    dsain = -proba_infection * sain * malade
    dmalade = proba_infection * sain * malade- proba_mort * malade - proba_soin * malade
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
    #mettre la répartition initiale en paramètres
    y =[1-0.00044247787,0.00044247787,0,0]
    k=0
    while y[1] > 10**-9:
        L.append(copy.deepcopy(y))
        y = suivant(y, virus, pas)
        k+=1
        print(L[-1][0] + L[-1][1] + L[-1][2] + L [-1][3])
    print(L[-1])
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
    
    sains_courbe, = plt.plot(suivi, a,'b', label='Sains')
    infectes_courbe, = plt.plot(suivi, b,'r', label='Infectés')
    morts_courbe, = plt.plot(suivi, c,'k', label='Morts')
    soignes_courbe, = plt.plot(suivi, d,'g', label='Soignés')

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()

#paramètres fonctions du temps

def deriver_variable(y, virus, t):
    proba_infection = virus[0]
    proba_mort = virus[1]
    proba_soin = virus[2]
    
    sain, malade, soigne, mort = y
    dsain = -proba_infection(t) * sain * malade
    dmalade = proba_infection(t) * sain * malade - proba_mort(t) * malade - proba_soin(t) * malade
    dsoigne = proba_soin(t) * malade
    dmort = proba_mort(t) * malade

    return [dsain, dmalade, dsoigne, dmort] 

def suivant_variable(y_n, virus, pas, t): 
    k_1 = deriver_variable(y_n, virus, t)

    y_n_k_2 = [y_n[i] + (pas/2) * k_1[i] for i in range(len(y_n))]
    k_2 = deriver_variable(y_n_k_2, virus, t)

    y_n_k_3 = [y_n[i] + (pas/2) * k_2[i] for i in range(len(y_n))]
    k_3 = deriver_variable(y_n_k_3,virus, t)

    y_n_k_4 = [y_n[i] + pas * k_3[i] for i in range(len(y_n))]
    k_4 = deriver_variable(y_n_k_4, virus, t)

    return [y_n[i] + (1/6) * (k_1[i] + 2*k_2[i] + 2*k_3[i] + k_4[i]) for i in range(len(y_n))]

    
def simulation_differentielle_variable(virus, pas):
    L=[]
    y =[0.9,0.1,0,0]
    t=0
    while y[1] > 10**-6 and t<10:
        L.append(copy.deepcopy(y))
        y = suivant_variable(y, virus, pas, t)
        t+=pas
    return L

def courbe_differentielle_variable(virus, pas):
    resultat = simulation_differentielle_variable(virus, pas)
    suivi =[]
    for i in range(len(resultat)):
        suivi.append(i*pas)
    fig = plt.figure()
    fig.suptitle('Evolution de la population en fonction du temps', fontsize=14)

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel('temps')
    ax.set_ylabel('Individus')
    
    print(len(resultat))
    etapes = np.array(range(len(resultat)))
    a,b,c,d = zip(*resultat)
    
    sains_courbe, = plt.plot(suivi, a,'b', label='Sains')
    infectes_courbe, = plt.plot(suivi, b,'r', label='Infectés')
    morts_courbe, = plt.plot(suivi, c,'k', label='Morts')
    soignes_courbe, = plt.plot(suivi, d,'g', label='Soignés')

    plt.legend(handles=[sains_courbe, infectes_courbe, morts_courbe, soignes_courbe])

    plt.show()

def beta(t):
    return t* np.exp(-t)

def gamma(t):
    return np.log(t+1)/2

def delta(t):
    return np.log(t+1)/3
