from math import exp, log

def proba_infection(R_0, tau, n):
    return 1 - exp((log((n - R_0)/ n)) / tau)

def proba_quitter(tau, mortalite):
    return (mortalite/ tau, (1-mortalite)/tau)