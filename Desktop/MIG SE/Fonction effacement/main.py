# -*- coding: utf-8 -*-
from Machine_verif import Machine
import random
import datetime as dt
from Conso import *
from Effacement_main_verif import *
from Outils import renvoyerIndiceJournee
#initialisation du programme général



def liste_temperature_exterieure(date_debut, date_fin):
     data_brut = pd.HDFStore('data_brut.h5')
     dfext = data_brut['Temperature_exterieure']
     data_brut.close()
     dfext = dfext[(dfext["date et heure"] >= date_debut)]
     dfext = dfext[(dfext["date et heure"] <= date_fin)]
     dfext.index = [k for k in range(len(dfext))]
     return(dfext['T° Exterieure'])


origine_de_la_simulation = dt.datetime(2015, 5, 1)
fin_de_la_simulation = dt.datetime(2015,5,2)

liste_temperatures_ext = liste_temperature_exterieure(origine_de_la_simulation, fin_de_la_simulation)


#instanciation des 7 machines
conso_chauffage = conso("General_Clim", origine_de_la_simulation, fin_de_la_simulation)
print("apres conso")
conso_max_chauffage  = max(conso_chauffage)  
print(conso_max_chauffage)
chauffage = Machine( "Chauffage", conso_max_chauffage, conso_chauffage[0]/conso_max_chauffage, 0.5, True, 0 )
conso_bouilleur = conso("Bouilleur_Friteuses_Vaisselle", origine_de_la_simulation, fin_de_la_simulation)	
conso_max_bouilleur  = max(conso_bouilleur)  
bouilleur = Machine( "Bouilleur", conso_max_bouilleur, conso_bouilleur[0]/conso_max_bouilleur, 0.5, True, 0 )
    
conso_splash_battle = conso( "Splash_Battle", origine_de_la_simulation, fin_de_la_simulation)
conso_max_splash_battle = max(conso_splash_battle)
splash_battle = Machine( "Splash_Battle", conso_max_splash_battle, conso_splash_battle[0]/conso_max_splash_battle, 0.5, True, 0 )
    
conso_creperie = conso( "Creperie_Gaufrier_Rotissoire", origine_de_la_simulation, fin_de_la_simulation )
conso_max_creperie = max(conso_creperie)    
creperie = Machine( "Creperie", conso_max_creperie, conso_creperie[0]/conso_max_creperie, 0.5, False, 0 )
    
conso_PC_Normal = conso( "General_PC_Normal", origine_de_la_simulation, fin_de_la_simulation )
conso_max_PC_Normal = max(conso_PC_Normal) 
PC_Normal = Machine( "PC_Normal", conso_max_PC_Normal, conso_PC_Normal[0]/conso_max_PC_Normal, 0.5, False, 0 )

conso_lumiere = conso("General_Eclairage", origine_de_la_simulation, fin_de_la_simulation)
conso_max_lumiere = max(conso_lumiere)
lumiere = Machine( "Lumiere", conso_max_lumiere, conso_lumiere[0]/conso_max_lumiere, 0.5, True, 0 ) 

liste_machines = [chauffage, lumiere, bouilleur, splash_battle, creperie, PC_Normal ]
liste_consos = [conso_chauffage, conso_lumiere, conso_bouilleur, conso_splash_battle, conso_creperie, conso_PC_Normal]

liste_temp_ext = liste_temperature_exterieure(dateTest, origine_de_la_simulation)
print(liste_temp_ext)

def main( origine_de_la_simulation, fin_de_la_simulation, liste_ordres ):
    
    
#----------------------------------------------------
    #indiquer les périodes d'effacement sur la liste de tuples liste_dates_simulation
    liste_dates_simulation = liste_dates_avec_booleens(origine_de_la_simulation, fin_de_la_simulation)
    for l in liste_dates_simulation:
        for ordre in liste_ordres:
            if ordre[0]==l[0]:
                l[1] = True
        
    liste_matrices = []
    
    Tint = 22
    ##importation de la liste Tint

    liste_temperatures_sans_effacement = [random.random()+22 for i in range(144)]
    liste_temperatures_avec_effacement = list(liste_temperatures_sans_effacement)
    #compléter les listes températures réelles et simulées, y compris en dehors de la période d'effacement
    #et actualiser la gene de chaque machine avant d'appliquer l'algo d'effacement
    
    for (date, booleen) in liste_dates_simulation :
        
        if True :
            #les fonctions ci-dessous doivent être implémentées précisément (inertie, datetimetotemperature...)
            #on prend la température régnant initialement dans la pièce (on suppose qu'elle a la valeur indiquée dans les relevés)                        
            for i in range(len(liste_machines)) :
                liste_machines[i].modifierGene(calcul_gene(liste_machines[i], date, Tint, liste_consos[i][renvoyerIndiceJournee(date)-renvoyerIndiceJournee(origine_de_la_simulation)]))
            (liste_dates, liste_temp_int_simul, matrice) = effacement_main( date, 400, liste_temperatures_sans_effacement, liste_temperatures_avec_effacement, liste_temperatures_ext, liste_matrices, liste_machines, liste_consos )
            liste_matrices.append(matrice)
        else :
            #en jouant sur la puissance de chauffage/clim, il faut proposer une solution pour que la température rejoigne son niveau d'avant effacement, et l'implémenter ci-dessous
            #...
            #...
            #Tint = 
            liste_temperatures_avec_effacement.append(Tint)

    return (liste_date_simulation, liste_temperatures_avec_effacement, liste_matrices)

conso_bouilleur = conso("Bouilleur_Friteuses_Vaisselle", origine_de_la_simulation, fin_de_la_simulation)

for ordre in [(origine_de_la_simulation, 1200),(fin_de_la_simulation, 1500)]:
    print(ordre[0])

main(origine_de_la_simulation,fin_de_la_simulation,[(origine_de_la_simulation, 100)])
