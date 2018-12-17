from math import exp, log

def proba_infection(R_0, tau, n):
    return 1 - ((n-R_0)/n)**(1/tau)

def proba_quitter(tau, mortalite):
    return (mortalite/ tau, (1-mortalite)/tau)

def param_diff(R_0, tau, x_0,mortalite):
    delta = mortalite/tau
    gamma = 1/tau-delta
    beta = (R_0)/(x_0*tau)
    return [beta,delta,gamma]