import sys
sys.path.append("C:/Users/Rudy-/Desktop/MIG SE/Fonction effacement")
import pandas
import datetime
from datetime import datetime
import time
from numpy import arange
import Outils
import matplotlib.pyplot as plt
import numpy as np
import os, sys
dateTest = datetime(2015,5,1)


# TEST : A lance tout les fichiers qui n'ont pas 
#d'accents a l'origine (9) : temps execution releve = 2'59''35



def renvoyerJourneeTypeTest( date):
    #remplacer sys.argv[1] par nomFichier
    deb = datetime.now()
    n = len(sys.argv)
    for i in range(1,n):
        df = Outils.puissanceReferenceMachine(sys.argv[i], date)
        x = arange(0,144,1)
        res = Outils.faireMoyenneJour(df)
        plt.figure(1)
        plt.plot(x,res[1::])
    
    fin = datetime.now()
    print(fin-deb)
    plt.show()
    
renvoyerJourneeTypeTest(dateTest)


# res[0] = maximum de la puissance de la journee type 
#prendre res[1::] pour obtenir reelement la journee type

def renvoyerJourneeTypeAvecMax(nomFichier, date):
    #remplacer sys.argv[1] par nomFichier
    df = Outils.puissanceReferenceMachine(nomFichier, date)
    res = Outils.faireMoyenneJour(df)
    return res


def renvoyerJourneeType(nomFichier, date) :
    res = renvoyerJourneeTypeAvecMax(nomFichier, date)
    return res[1::]

