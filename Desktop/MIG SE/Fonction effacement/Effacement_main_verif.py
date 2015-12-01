import sys
sys.path.append("C:/Users/Rudy-/Desktop/MIG SE/Fonction effacement")
import pandas as pd
from datetime import *
from Machine_verif import * 
from Batiment_verif import *
from Gene_verif import *
from datetime_to_temp_verif import *

## déboguer les fonctions appelées

def datetime_to_temperature(datetime1, nom_Fichier):
    str1 = str(datetime1.day) + '/' + str(datetime1.month) + '/' +str(datetime1.year) + ' '             +str(datetime1.hour) + ':' +str(datetime1.minute) + ":" + str(datetime1.second)
    Data_frame_temperature =    pd.read_csv(nom_Fichier,sep = ";",names=["date et heure","lieu","type1","type2","valeur","unité"],header=None)
    if str1 in Data_frame_temperature["date et heure"]:
        k = Data_frame_temperature["date et heure"].index(str1)
        return(Data_frame_temperature["valeur"][k])
    else:
        return("Date et heure non compatibles") ##path à régler selon l'ordi
        

def effacement_main( date_debut, Puissance_a_effacer ):

    ##instancier: liste_machines

#Objets return
    liste_dates = [ date_debut + timedelta(seconds = i*600) for i in range(7) ]
    liste_temp_int_simul = []*7
    #Initialisation de la matrice renvoyée, à l'état initial
    matrice = [[[]]]
    for (i,mac) in enumerate(liste_machines):
        matrice[0][i]=[ mac.renvoyerNom(), mac.renvoyerEtatActuel(), mac.consoMachine(), mac.renvoyerGene() ] 
        

    Puissance_effacee = 0   
    liste_temp_int_simul[0] = [datetime_to_temperature(date_debut, nom_Fichier_Tint_Reel)] ##à configurer selon le path
    plus_modifiables = [machine for machine in liste_machines if machine.renvoyerEtatActuel() == 0]
    nb_iter = 0
    
    
    #Début de l'algorithme
    while Puissance_effacee < Puissance_a_effacer and len(plus_modifiables) != len(liste_machines):
        
        liste_tuples = []  
        for machine in liste_machines:
            if not (machine in plus_modifiables):
                if machine.renvoyerGene() >= 0.95: 
                    liste_tuples.append( (0, machine) )
                    plus_modifiables.append(machine)
                elif machine.renvoyerEtatContinu():
                    if machine.renvoyerEtat() >= 0.01:
                        deltagene = get_delta_gene( machine, date_debut, liste_temp_int_simul[nb_iter] )
                        priorite = machine.consoMachine()/(deltagene*100)
                        liste_tuples.append( (priorite, machine) )
                    else:
                        liste_tuples.append( (0, machine) )
                        plus_modifiables.append(machine)
                else:
                    priorite = machine.renvoyerConsoMax()/machine.renvoyerGene() 
                    liste_tuples.append( (priorite, machine) )
            else:
                liste_tuples.append( (0, machine) )
                       
        liste_tuples_sorted = sorted(liste_tuples, reverse = True)
        machine_prior = liste_tuples_sorted[0](1)
        if not (machine_prior in plus_modifiables):
            if not (machine_prior.EtatContinu()):
                Puissance_effacee += machine_prior.renvoyerConso()
            else:
                Puissance_effacee += machine_prior.renvoyerConsoMax()/100
            machine_prior.actualise_etat_et_gene(machine, date_debut)
        for (k, mach) in enumerate( liste_tuples_sorted ):
            matrice[nb_iter][k]=[ mach.renvoyerNom(), mach.renvoyerEtatActuel(), mach.consoMachine(), mach.renvoyerGene() ]
        nb_iter += 1
        
        
    #Début de la boucle temporelle:
    Puissance_chauff = matrice[nb_iter][0][2]
    for i in liste_dates[1::]:
        liste_temp_int_simul.append( calcul_temp(Puissance_chauff, liste_temp_int_simul[i-1], datetime_to_temperature(i, nom_Fichier_Text_Reel)) ) 
        ##fonction calcul_temp à définir, et path à configurer
    
    #retour de la liste des temps, liste temporelle des températures simulées, et la matrice pas à pas
    return(liste_dates, liste_temp_int_simul, matrice)
        
        
        
            
                
                
                
    
    




