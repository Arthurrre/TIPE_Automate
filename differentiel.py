proba_infection = 0.8
proba_mort = 0.5
proba_soin = 0.2

pas = 10**-10

def deriver(t, y):
    sain, malade, soigne, mort = y
    dsain = -proba_infection * sain * malade
    dmalade = proba_infection * sain * malade - proba_mort * malade - proba_soin * malade
    dsoigne = proba_soin * malade
    dmort = proba_mort * malade

    return [dsain, dmalade, dsoigne, dmort] 


def suivant(y_n, t_n):
    k_1 = deriver(t_n, y_n)

    y_n_k_2 = [y_n[i] + (pas/2) * k_1[i] for i in range(len(y_n))]
    k_2 = deriver(map((lambda x: x+ pas/2), t_n) , y_n_k_2)

    y_n_k_3 = [y_n[i] + (pas/2) * k_2[i] for i in range(len(y_n))]
    k_3 = deriver(map((lambda x: x+ pas/2), t_n), y_n_k_3)

    y_n_k_4 = [y_n[i] + pas * k_3[i] for i in range(len(y_n))]
    k_4 = deriver(map((lambda x: x+ pas), t_n), y_n_k_3)

    return [y_n[i] + (1/6) * (k_1[i] + 2*k_2[i] + 2*k_3[i] + k_4[i]) for i in range(len(y_n))]
