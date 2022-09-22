import pandas as pd
from datetime import *
import Machine_verif 
import Gene_verif
import Outils
## déboguer les fonctions appelées
## fournir matrice exemple à l'équipe affichage

def datetime_to_temperature(datetime1):
    str1 = str(datetime1.day) + '/' + str(datetime1.month) + '/' +str(datetime1.year) + ' '             +str(datetime1.hour) + ':' +str(datetime1.minute) + ":" + str(datetime1.second)
    Data_frame_temperature =    pd.read_csv(Fichier,sep = ";",names=["date et heure","lieu","type1","type2","valeur","unité"],header=None)
    if str1 in Data_frame_temperature["date et heure"]:
        k = Data_frame_temperature["date et heure"].index(str1)
        return(Data_frame_temperature["valeur"][k])
    else:
        return("Date et heure non compatibles") ##path à régler selon l'ordi
        

def effacement_main( date_debut, Puissance_a_effacer, liste_temperatures_sans_effacement, liste_temperatures_avec_effacement, liste_temperatures_ext, liste_matrices, liste_machines, liste_consos ):

    ##instancier: liste_machines

#Objets return
    liste_dates = [ date_debut + timedelta(seconds = i*600) for i in range(7) ]
    liste_temp_int_simul = []
    #Initialisation de la matrice renvoyée, à l'état initial
    matrice = [[]]
    for mac in liste_machines:
        matrice[0].append( [ mac.renvoyerNom(), mac.renvoyerEtatActuel(), mac.consoMachine(), mac.renvoyerGene() ] )
    print ("Hello !")
    print ( matrice )

    Puissance_effacee = 0   
    plus_modifiables = [machine for machine in liste_machines if machine.renvoyerEtatActuel() == 0]
    nb_iter = 0
    
    
    #Début de l'algorithme
    while Puissance_effacee < Puissance_a_effacer and len(plus_modifiables) != len(liste_machines):
        
        liste_tuples = []  
        i=0
        for machine in liste_machines:
            i+=1
            if not (machine in plus_modifiables):
                if machine.renvoyerGene() >= 0.95:
                    liste_tuples.append( (0, machine) )
                    plus_modifiables.append(machine)
                elif machine.renvoyerEtatContinu():
                    if machine.renvoyerEtatActuel() >= 0.01:
                        deltagene = get_delta_gene(machine, date_debut, liste_consos[i][renvoyerIndiceJournee(date)-renvoyerIndiceJournee(origine_de_la_simulation)])
                        priorite = machine.consoMachine()/(deltagene*100)
                        liste_tuples.append( (priorite, machine) )
                    else:
                        liste_tuples.append( (0, machine) )
                        machine.modifierEtatActuel( 0 )
                        plus_modifiables.append(machine)
                else:
                    priorite = machine.renvoyerConsoMax()/machine.renvoyerGene() 
                    liste_tuples.append( (priorite, machine) )
                    plus_modifiables.append(machine)
            else:
                liste_tuples.append( (0, machine) )
                       
        liste_tuples_sorted = sorted(liste_tuples, reverse = True)
        machine_prior = liste_tuples_sorted[0](1)
        if not ( len(plus_modifiables) == len(liste_machines) and machine_prior.renvoyerEtatContinu() ):
            Puissance_effacee += machine_prior.renvoyerConso()
            machine_prior.actualise_etat_et_gene(machine, date_debut)
        for k, mach in enumerate( liste_tuples_sorted ):
            matrice[nb_iter][k]=[ mach.renvoyerNom(), mach.renvoyerEtatActuel(), mach.consoMachine(), mach.renvoyerGene() ]
        nb_iter += 1
        
    i = 0 
    #Début de la boucle temporelle:
    for date in liste_dates[1::]:
        i += 1
        Puissance_tot = sum( [matrice[nb_iter][x][2] for x in range( len(liste_machines) ) ])
        
        liste_temp_int_simul.append(prevision_temperature(liste_temp_int_simul[-1], chauffage.renvoyerEtatActuel() * chauffage.renvoyerConsoMax() , liste_temperatures_ext[Outils.renvoyerIndiceJournee(date_debut)-Outils.renvoyerIndiceJournee(origine_de_la_simulation)], nom_temperature))
        
        ##fonction calcul_temp à définir en fonction de P_tot, T_préc, T_ext(date)
    
    #retour de la liste des temps, liste temporelle des températures simulées, et la matrice pas à pas


    liste_matrices.append(matrice)
    
        
        
            
                
                
                
    
    




