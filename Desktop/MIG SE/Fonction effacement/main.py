import sys
sys.path.append("C:/Users/Rudy-/Desktop/MIG SE/Fonction effacement")
import analyseDonnees
from datetime import datetime
import Machine_verif
dateTest = datetime(2015,5,1)

journeeTypeFrigo = analyseDonnees.renvoyerJourneeTypeAvecMax("../MIG DATA/DATA/SmartEnCo/kids_island/Frigo grainerie.csv", dateTest)

consoMax = journeeTypeFrigo[0]

frigo = Machine("Frigo", consoMax, journeeTypeFrigo[1]/consoMax, 0.8, True, 0)

print(frigo)