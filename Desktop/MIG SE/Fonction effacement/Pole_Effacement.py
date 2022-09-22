import pandas as pd
import copy
import random as rd
import marshal as ms
from liste_ordres import *
from datetime import *

##################################### Pole effacement ###############################################
#####################################################################################################
########## Fonctions pour ecrire les résultats dans un fichier a l'aide du module marshal  ##########
#####################################################################################################


#convertit une datetime en chaine de caracteres
def datetime_to_str(date_time):
    date = ""
    if date_time.day < 10:
        date+='0'+str(date_time.day)
    else:
        date+=str(date_time.day)
    date+='/'
    if date_time.month < 10:
        date+='0'+str(date_time.month)
    else:
        date+=str(date_time.month)
    date+='/' + str(date_time.year) + ' '
    if date_time.hour < 10:
        date+='0'+str(date_time.hour)
    else:
        date+=str(date_time.hour)
    date+=':'
    if date_time.minute < 10:
        date+='0'+str(date_time.minute)
    else:
        date+=str(date_time.minute)
    date+=':'
    if date_time.second < 10:
        date+='0'+str(date_time.second)
    else:
        date+=str(date_time.second)
    return(date)

#ecrit les donnees sous format binaire dans un fichier
def donnees_to_bytes(liste_dates,liste_temperatures,liste_effacements,liste_matrices,liste_puiss_fin,liste_puiss_init):
    liste_dates_str = []
    liste_effacements_str = []
    for date_time in liste_dates:
        liste_dates_str.append(datetime_to_str(date_time))
    for temps_effacements in liste_effacements:
        liste_effacements_str.append((datetime_to_str(temps_effacements[0]),temps_effacements[1]))
    ms.dump([liste_dates_str,liste_temperatures,liste_effacements_str,liste_matrices,liste_puiss_fin,liste_puiss_init],open('file_dataeffacement.dat','wb'))

#lit les donnees ecrites sous format binaire dans ce fichier
def bytes_to_donnees(file_path):
    file_data = open(file_path,'rb')
    liste_donees = ms.load(file_data)
    print(len(liste_donnees))
    dates = []
    print(liste_donnees[0])
    for date in liste_donnees[0]:
        print(date)
        jours = int(date[0:2])
        mois= int(date[3:5])
        annees = int(date[6:10])
        heures = int(date[11:13])
        minutes = int(date[14:16])
        secondes = int(date[17:19])
        dates.append(datetime(annee,mois,jours,heures,minutes,secondes))
    effacement = []
    for effacements in liste_donnees[3]:
        datetime = effacements[0]
        jours = int(datetime[0:2])
        mois= int(datetime[3:5])
        annee = int(datetime[6:10])
        heures = int(datetime[11:13])
        minutes = int(datetime[14:16])
        secondes = int(datetime[17:19])
        effacement.append((datetime(annee,mois,jours,heures,minutes,secondes),effacements[1]))
    return([dates,liste_donnees[1],effacement,liste_donnees[3],liste_donnees[4],liste_donnees[5]])

##################################### Pole effacement ###############################################
#####################################################################################################
#################### la classe machine, avec ses attributs et ses methodes ##########################
#####################################################################################################

class Machine :
        
	def __init__(self, nom, consoMax, etatActuel, importance, etatContinu, gene) :
		self.__nom = nom

		if(consoMax >= 0) :
			self.__consoMax = consoMax
		else :
			print("ERROR ("+nom+") ==> consoMax mis a 0")
			self.__consoMax = 0



		if (not etatContinu) :
			if(etatActuel > 0) :
				if(etatActuel !=1) :
					print("ERROR ("+nom+") ==> etatActuel mis a 1")
				etatActuel = 1
			elif(etatActuel < 0) : 
				if(etatActuel !=0) :
					print("ERROR ("+nom+") ==> etatActuel mis a 0")
				etatActuel = 0
		else : 
			if (etatActuel < 0) :
				print("ERROR ("+nom+") ==> etatActuel mis a 0")
				etatActuel = 0
			elif (etatActuel > 1) :
				print("ERROR ("+nom+") ==> etatActuel mis a 1")
				etatActuel = 1
		self.__etatActuel = etatActuel


		self.__importance = importance
		self.__etatContinu = etatContinu
		self.__gene = gene
    
	def __str__(self) :
		s = "Machine : [nom="+str(self.__nom)
		s += ", consoMax="+str(self.__consoMax)
		s +=  ", etatActuel="+str(self.__etatActuel)
		s += ", importance="+str(self.__importance)
		s += ", etatContinu="+str(self.__etatContinu)
		s += ", gene="+str(self.__gene)+"]"
		return s


#||||||||||||||||||||||||  DONNES //  |||||||||||||||||||||||||||||||
	def renvoyerNom(self) :
		return self.__nom            
	def renvoyerConsoMax(self) :
		return self.__consoMax            
	def renvoyerEtatActuel(self) :
		return self.__etatActuel            
	def renvoyerImportance(self) :
		return self.__importance           
	def renvoyerEtatContinu(self) :
		return self.__etatContinu            
	def renvoyerGene(self):
		return self.__gene


#||||||||||||||||||||||||  MODIFIER  |||||||||||||||||||||||||||||
	def modifierEtatActuel(self, nouvelEtatActuel) :
		if(self.__etatContinu) :
			self.__etatActuel = nouvelEtatActuel
			return True
		elif (nouvelEtatActuel in [0,1]):
			self.__etatActuel = nouvelEtatActuel
			return True
		return False

	def modifierGene(self, nouvelleGene):
		self._gene = nouvelleGene
		

#||||||||||||||||||||||||  METHODES  |||||||||||||||||||||||||||||
	def consoMachine (self) :
		return self.__consoMax * self.__etatActuel



##################################### Pole effacement ###############################################
#####################################################################################################
#### Le bloc qui suit correspond aux fonctions utiles pour actualiser de de la gene et de l'etat ####
#####################################################################################################

#liste de machines DANS LE CADRE DU TEST
def indice_machine(machine) :
    nom = machine.renvoyerNom()
    k=0
    l=["Chauffage", "Lumiere", "Bouilleur", "Splash_Battle", "Creperie", "PC_Normal" ]
    for i in range(len(l)):
        if nom == l[i]:
            k=i
    return k

#si jamais l'algorithme decide d'eteindre (partiellement ou totalement) une machine. Actualise alors les valeurs d'etat et de gene
def actualise_etat_et_gene(instance_machine, date, liste_temperatures_ext, liste_temperatures_int_simul, liste_ref): 
    etatActuel = instance_machine.renvoyerEtatActuel()   
    if (instance_machine.renvoyerEtatContinu() and etatActuel>=0.01) :
        instance_machine.modifierEtatActuel( etatActuel - 0.01 )
        instance_machine.modifierGene(instance_machine.renvoyerGene() + get_delta_gene(instance_machine, date,liste_temperatures_ext,liste_temperatures_int_simul,liste_ref))
            
    else:
        instance_machine.modifierEtatActuel(0)
        instance_machine.modifierGene(instance_machine.renvoyerGene() + get_delta_gene(instance_machine, date, liste_temperatures_ext, liste_temperatures_int_simul, liste_ref))
        
    
#calcule le delta(gene) correspondant à une diminution de l'etat d'1%. N'est appele que sur les machines a etat continu
def get_delta_gene(instance_machine, date, liste_temperatures_ext, liste_temperatures_int_simul, liste_ref):
    indice_date = renvoyerIndiceJournee(date)
    
    tInt = liste_temperatures_int_simul[indice_date]
    if (instance_machine.renvoyerNom() == "Chauffage" ) :
        Pq_actuelle = instance_machine.consoMachine()
        tExt = liste_temperatures_ext[indice_date]
        puissance = instance_machine.renvoyerEtatActuel() * instance_machine.renvoyerConsoMax()
        temp_apres = prevision_temperature(tInt, puissance, tExt, "T° Bureau Administration Assistantes de Direction")  #tInt à implémenter
        gene_apres = calcul_gene(instance_machine, None, temp_apres, -1) 
        delta_gene = gene_apres - instance_machine.renvoyerGene() 
        return( delta_gene )  
    else:
        
        instance_machine.modifierEtatActuel(instance_machine.renvoyerEtatActuel() - 0.01)
        gene_apres = calcul_gene(instance_machine, date , tInt, liste_ref[indice_date]) 
        instance_machine.modifierEtatActuel(instance_machine.renvoyerEtatActuel() + 0.01)
        delta_gene = gene_apres - instance_machine.renvoyerGene()
        return( delta_gene )  
    

#calcul de la gene effective liee a l'etat d'utilisation d'une machine. Depend de la nature de la machine, de la date, de la temperature et de l'etat d'utilisation par rapport a la normale (traduit par etatRef)
def calcul_gene(instance_machine, date, tInt, etatRef):   #calcul de la gene
    
    epsilon = 0.00001
    geneRetourne = -1
    
    etat_actuel = instance_machine.renvoyerEtatActuel() + epsilon
    if instance_machine.renvoyerNom() == "Chauffage"  :	
        if 19 <= tInt <= 25:
            geneRetourne =((tInt-22)**4)/81 
        else:
            geneRetourne =(1)
    
    
    elif instance_machine.renvoyerNom() == "Lumiere" :
        if date.hour < 9 or date.hour > 19 :
            geneRetourne = 0.0
        elif (date.hour >=16 and date.hour <19) and (date.month >=10 or date.month <=3) :
            geneRetourne = ( 1-etat_actuel )*3
        else :
            geneRetourne = 1-etat_actuel 
    elif instance_machine.renvoyerNom() == "PC_Normal":
        importance = instance_machine.renvoyerImportance()  
        geneRetourne = (etatRef / etat_actuel)**importance -1 
    elif instance_machine.renvoyerNom() == "Bouilleur":
        
        if date.hour < 9 or date.hour > 19 :
            geneRetourne = 0.0
        else:
            geneRetourne = ( etatRef / etat_actuel)**instance_machine.renvoyerImportance() -1 
    elif instance_machine.renvoyerNom() == "Splash_Battle":
        if date.hour < 7 or date.hour > 21:
            geneRetourne = 0.0
        else:
            geneRetourne = ( etatRef / etat_actuel)**instance_machine.renvoyerImportance() -1 
    elif instance_machine.renvoyerNom() == "Creperie":
        if date.hour < 9 or date.hour > 19 :
            geneRetourne = 0.0
        else:
            geneRetourne = 1.0
    #le else ci-dessous sert a gerer les bogues imprevus. on n'est pas cense y entrer
        else:
        geneRetourne = ( etatRef /etat_actuel)**instance_machine.renvoyerImportance() -1 
    
    return min(max(geneRetourne, 0),1)


##################################### Pole effacement ###############################################
#####################################################################################################
# Le bloc qui suit correspond a l'algorithme glouton effacement_main et a ses fonctions auxiliaires #
#####################################################################################################

 #fonction auxiliaire : tri par selection d'une liste de tuples selon le premier parametre
def renvoyer_machine_prior_max(liste_tuples):
    prio_max =-1
    machine_prio_max = None
    for (prio,machine) in liste_tuples:
        if prio > prio_max:
            machine_prio_max = machine
            prio_max = prio
    return((prio_max,machine_prio_max))
        
def tri(liste_tuples) :
    res = []
    while(len(liste_tuples) != 0) :
        tuple_prio = renvoyer_machine_prior_max(liste_tuples)
        res.append(tuple_prio)
        liste_tuples.remove(tuple_prio)
    return(res)

#auxiliaire : renvoie la temperature correspondant a un instant precis (sous format datetime) dans un fichier de donnees brutes (où elles sont sous forme de String)
def datetime_to_temperature(datetime1):
    str1 = str(datetime1.day) + '/' + str(datetime1.month) + '/' +str(datetime1.year) + ' ' +str(datetime1.hour) + ':' +str(datetime1.minute) + ":" + str(datetime1.second)
    Data_frame_temperature = pd.read_csv(Fichier,sep = ";",names=["date et heure","lieu","type1","type2","valeur","unite"],header=None) #on lit le fichier sous la forme d'un dataframe, plus facilement exploitable
######## l'utilisateur doit remplacer Fichier (ci-dessus) par le nom du fichier des temperatures sur son ordinateur pour que le programme fonctionne
    if str1 in Data_frame_temperature["date et heure"]:
        k = Data_frame_temperature["date et heure"].index(str1)
        return(Data_frame_temperature["valeur"][k])
    else:
        return("Date et heure non compatibles") #lorsque la date entree en argument n'apparait pas dans le fichier

#
def estDansLaSemaineTravail(date):
    return (date.weekday() <= 4)

def renvoyerIndiceJournee(d):
    if(DEBUG) :
        print("DEBUG (Conso) : d=",d)
        print("res = ",6*d.hour + d.minute//10)
    return (6*d.hour + d.minute//10)


#conso() permet d'intialiser la liste des consommations dans l'etat de reference a partir des donnees brutes d'energie (et pas directement d'energie, cela permet de lisser les courbes)
def conso(nom_machine, date_debut, date_fin):
    nom_machine = str(nom_machine)
    data_lisse = pd.HDFStore('data_lisse.h5')
    df = data_lisse[nom_machine]
    data_lisse.close()
    df = df[(df["date et heure"] >= date_debut)]
    df = df[(df["date et heure"] < date_fin)]
    liste_energies = df["Energie"]
    liste_puissances = [round(k*6000,2) for k in liste_energies]
    return (liste_puissances)
    
#conso2() permet d'intialiser la liste des consommations dans l'etat de reference a partir des donnees brutes de puissance (moins bien que la methode precedente, mais necessaire lorsqu'il manque des donnee0s d'energie, comme pour le bouilleur)
def conso2(nom_machine, date_debut, date_fin):
    nom_machine = str(nom_machine)
    data_lisse = pd.HDFStore('data_lisse.h5')
    df = data_lisse[nom_machine]
    data_lisse.close()
    df = df[(df["date et heure"] >= date_debut)]
    df = df[(df["date et heure"] < date_fin)]
    liste_energies = df["Puissance"]
    liste_puissances = [round(k,2) for k in liste_energies]
    return (liste_puissances)

def liste_dates(date_debut,date_fin):
    list = [date_debut]
    delta = datetime.timedelta(0,600,0)
    while (list[-1]+delta) < date_fin:
        list.append(list[-1]+delta)
    return(list)

#####################################################################################################
#Ici, le coeur de leffacement : l'algorithme glouton procede a l'effacement

def effacement_main( date_debut, origine_de_la_simulation, Puissance_a_effacer, liste_temperatures_int_simul, liste_temperatures_ext, liste_matrices, liste_machines, liste_puissances, liste_consos, nombre_effacement_consecutif ):	
	# on prend en argument toutes les caracteristiques du bâtiments : ses machines, leur consommation, les temperatures interieure et exterieure
	# nombre_effacement_consecutif est le numero de l'effacement actuel, chaque effacement durant une heure.
	# selon les circonstances, le pole marche peut nous demander d'operer plusieurs effacements consecutifs, mais pour optimiser le confort des usagers, nous choisissons de rallumer automatiquement la pompe a chaleur a la troisieme heure d'effacement consecutive.

    liste_dates_effacement = [ date_debut + timedelta(seconds = i*600) for i in range(6) ]	#liste_dates_effacement contient six dates sous format datetime,par pas de 600 secondes (une date encode l'annee, le mois, le jour, l'heure et la minute)
    #pour que le pole affichage puisse afficher le fonctionnement pas a pas de notre algorithme d'effacement, nous lui renvoyons une matrice dont les elements sont des listes de caracteristiques des machines
    #Initialisation de la matrice avec les caracteristiques des machines (nom, etat_actuel, consommation_actuelle, gene_causee) a l'instant initial
    matrice = [[]]	#en ordonnee, les machines; en abscisse, les iterations de l'algorithme.
    for mac in liste_machines:
        matrice[0].append( [ mac.renvoyerNom(), mac.renvoyerEtatActuel(), mac.consoMachine(), mac.renvoyerGene() ] )

	#plus_modifiables est la liste des machines dont on ne peut plus diminuer l'etat d'utilisation, parce qu'elles sont deja completement eteintes, ou qu'on ne veut plus le faire, parce que la gene deviendrait trop elevee
    plus_modifiables = [machine for machine in liste_machines if machine.renvoyerEtatActuel() == 0]	
    ind_date_debut = renvoyerIndiceJournee(date_debut) #stocke l'indice correspondant a date_debut dans liste_dates_simulations (liste globale cree par le main)
    #Debut de l'algorithme : on efface tant qu'il reste des machines modifiables et qu'on n'a pas atteint le quotat requis par le pole marche
	Puissance_effacee = 0 
    while( Puissance_effacee < Puissance_a_effacer) and (len(plus_modifiables) != len(liste_machines)):

        liste_tuples = [] #les tuples sont des couples (priorite de la machine, machine). On efface toujours la machine de priorite maximale.
      
        if (nombre_effacement_consecutif % 3 == 0 and nombre_effacement_consecutif != 0): #La pompe a chaleur (liste_machines[0]) est souvent l'une des premieres machines a etre coupees. Pour le confort des usagers, on decide qu'elle doit etre automatiquement rallumee au bout de 2h
       		liste_tuples.append( (0, liste_machines[0]) )	#on affecte une priorite nulle au chauffage
            plus_modifiables.append(liste_machines[0]) #on le place dans la liste des machines a ne plus modifier
            liste_machines[0].modifierEtatActuel(liste_consos[0][indice_date]/renvoyerConsoMax())
            etatRef = liste_consos[0][ind_date_debut]
            liste_machines[0].modifierGene(calcul_gene(liste_machines[0], date_debut, tInt, etatRef ))
                     
                     
        for machine in liste_machines:
            ind_machine = indice_machine(machine)
            if not (machine in plus_modifiables):	#si on peut encore modifier l'etat de la machine
                if machine.renvoyerGene() >= 0.9:	#si l'extinction de la machine occasionne trop de gene

                    tInt = liste_temperatures_int_simul[ind_date_debut]
                    etatRef = liste_consos[ind_machine][ind_date_debut]
                    liste_tuples.append( (0, machine) )	#on affecte une priorite nulle a la machine
                    plus_modifiables.append(machine)	#on la place dans la liste des machines a ne plus eteindre (dans le cadre de cet ordre d'effacement-la)
                    conso_avant = machine.consoMachine()
                    #on remet la machine dans son etat pre-effacement, on actualise sa gene, et on diminue si besoin la puissance qu'on avait reussi a effacer jusque-la
                    machine.modifierEtatActuel(liste_consos[ind_machine][indice_date]/machine.renvoyerConsoMax())
                    machine.modifierGene(calcul_gene(machine, date_debut, tInt, etatRef ))
                    
                    conso_apres = machine.consoMachine()                     
                    Puissance_effacee -= conso_apres - conso_avant
                    
                elif machine.renvoyerEtatContinu(): #si la machine est modulable et utilisee a plus d'1%, on essaye de diminuer son utilisation d'1%
                    if machine.renvoyerEtatActuel() >= 0.01: 
                        deltagene = epsilon + get_delta_gene(machine, date_debut,  liste_temperatures_ext, liste_temperatures_int_simul, liste_consos[ind_machine]) # on calcule l'eventuelle variation de gene si l'on effaçait encore un peu plus la machine
                        priorite = machine.consoMachine()/(deltagene*100)
                        liste_tuples.append( (priorite, machine) )
                    else:
                        liste_tuples.append( (0, machine) )	#si l'etat de la machine est inferieur a 0.01, c'est comme si elle etait eteinte : on la considere donc comme telle.
                        machine.modifierEtatActuel( 0 )
                        plus_modifiables.append(machine)
                else:
                    priorite = machine.renvoyerConsoMax()/(machine.renvoyerGene() + epsilon)
                    liste_tuples.append( (priorite, machine) )	#on a vu ici les deux moyens de calculer la priorite selon le type de machine
                    plus_modifiables.append(machine)
            else:
                liste_tuples.append( (0, machine) )
                
		#ci-dessous, on trie la liste des machines par priorite decroissante, on selectionne la premiere de la liste, on procede a l'effacement total ou partiel (selon le type de machine) et on actualise l'etat, la gene et Puissance_effacee                          
        liste_tuples_sorted = tri(liste_tuples)
        machine_prior = liste_tuples_sorted[0][1]	
        conso_avant = machine_prior.consoMachine()
        if machine_prior.renvoyerEtatContinu(): #tous les tests effectués avant nous permettent de ne pas nous poser de question
        	machine_prior.modifierEtatActuel(machine_prior.renvoyerEtatActuel - 0.01)
        	conso_apres = machine_prior.consoMachine()
        else : 
        	machine_prior.modifierEtatActuel(0)
        	conso_apres = 0
        ind_machine = indice_machine(machine_prior) 
        etatRef = liste_consos[ind_machine][ind_date_debut]
        machine_prior.modifierGene(machine_prior, date_debut, tInt, etatRef)

        Puissance_effacee += conso_avant - conso_apres

        #et maintenant, on ajoute cette iteration a la matrice pas a pas
        l = []
        for (prio,mach) in liste_tuples_sorted:
            l.append([ mach.renvoyerNom(), mach.renvoyerEtatActuel(), mach.consoMachine(), mach.renvoyerGene() ])
        matrice.append(l)
    
    #Debut de la boucle temporelle:
    for date in liste_dates_effacement:
        
        indice_date = renvoyerIndiceJournee(date)
        #pour chaque ordre d'effacement, les valeurs ne varient pas pendant les dix premieres minutes, donc les dates d'indices 0 et 1 se traitent de meme
        if(indice_date == 0) :
            indice_date = 1
        else : 
            nouvelle_temperature = prevision_temperature(liste_temperatures_int_simul[indice_date-1], liste_machines[0].renvoyerEtatActuel() * liste_machines[0].renvoyerConsoMax() , liste_temperatures_ext[indice_date], "T° Bureau Administration Assistantes de Direction")
            liste_temperatures_int_simul[indice_date] = nouvelle_temperature
        
        for num_machine in range(len(liste_machines)): #on modifie la matrice globale liste_puissances, pour qu'elle stocke les puissances apres effacement
            liste_puissances[num_machine][indice_date] = max(0,liste_machines[num_machine].consoMachine() + liste_consos[num_machine][indice_date] - liste_consos[num_machine][ind_date_debut])
            
    #retour de puissance_effacee. Les listes des temps, des temperatures simulees, des puissances, et la matrice pas a pas sont des listes globales qu'on a modifiees au fur et a mesure, pas besoin de les retourner
    liste_matrices.append(matrice)
    return Puissance_effacee


##################################### Pole effacement ###############################################
#####################################################################################################
#####  Le bloc qui suit correspond a la fonction main, qui recoit des ordres du pole marche, cree les 
##### variables globales utiles pour l'algorithme glouton, appelle ce-dernier, et ecrit les resultats 
##### dans un fichier texte qui sera lu par le pole affichage #######################################
#####################################################################################################

#fonctions auxiliaires pour recuperer sous forme de listes les donnees prealablement converties en dateframe (structure du module pandas, adaptee pour les bases de donnees)
#pour que ces fonctions fonctionnent, le programme doit etre enregistre dans le meme repertoire que la data_base data_lisse
#data_lisse a ete construite en lissant les donnees brutes dont nous disposions

def liste_temperature_exterieure(date_debut, date_fin):
     data_lisse = pd.HDFStore('data_lisse.h5')
     dfext = data_lisse['Temperature_exterieure']
     data_lisse.close()
     dfext = dfext[(dfext["date et heure"] >= date_debut)]
     dfext = dfext[(dfext["date et heure"] < date_fin)]
     dfext.index = [k for k in range(len(dfext))]
     return(dfext['T° Exterieure'])
     
def liste_temperature_interieure(date_debut, date_fin):
     data_lisse = pd.HDFStore('data_lisse.h5')
     dfint = data_lisse['Temperatures2']
     data_lisse.close()
     dfint = dfint[(dfint["date et heure"] >= date_debut)]
     dfint = dfint[(dfint["date et heure"] < date_fin)]
     dfint.index = [k for k in range(len(dfint))]
     return(dfint['T° Bureau Administration Assistantes de Direction'])

#####################################################################################################

#DANS LE CADRE DU TEST : instanciation des 6 machines
conso_chauffage = conso("General_Clim", origine_de_la_simulation, fin_de_la_simulation)
conso_max_chauffage  = max(conso_chauffage)
chauffage = Machine( "Chauffage", conso_max_chauffage, conso_chauffage[0]/conso_max_chauffage, 0.5, True, 0 )

conso_lumiere = conso("General_Eclairage", origine_de_la_simulation, fin_de_la_simulation)
conso_max_lumiere = max(conso_lumiere)
lumiere = Machine( "Lumiere", conso_max_lumiere, conso_lumiere[0]/conso_max_lumiere, 0.5, True, 0 )

conso_bouilleur = conso2("Bouilleur_Friteuses_Vaisselle", origine_de_la_simulation, fin_de_la_simulation)
conso_max_bouilleur  = max(conso_bouilleur)  
bouilleur = Machine( "Bouilleur", conso_max_bouilleur, conso_bouilleur[0]/conso_max_bouilleur, 0.5, True, 0 )

conso_splash_battle = conso( "Splash_Battle", origine_de_la_simulation, fin_de_la_simulation)
for i in range(len(conso_splash_battle)):
    conso_splash_battle[i] /=50
conso_max_splash_battle = max(conso_splash_battle)
splash_battle = Machine( "Splash_Battle", conso_max_splash_battle, conso_splash_battle[0]/conso_max_splash_battle, 0.5, True, 0 )

conso_creperie = conso( "Creperie_Gaufrier_Rotissoire", origine_de_la_simulation, fin_de_la_simulation )
conso_max_creperie = max(conso_creperie)    
creperie = Machine( "Creperie", conso_max_creperie, conso_creperie[0]/conso_max_creperie, 0.5, True, 0 )

conso_PC_Normal = conso( "General_PC_Normal", origine_de_la_simulation, fin_de_la_simulation )
conso_max_PC_Normal = max(conso_PC_Normal) 
PC_Normal = Machine( "PC_Normal", conso_max_PC_Normal, conso_PC_Normal[0]/conso_max_PC_Normal, 0.5, True, 0 )

#on cree la liste d'ordres avec la fonction list_eff du pole marche
#DANS LE CADRE DU TEST eff_max = 1500 W
liste_ordres = list_eff(opfile_prix_avr, 1500, 'avr')

#INSTANCIATION des variables globales
origine_de_la_simulation = liste_ordres[0][0]
fin_de_la_simulation = liste_ordres[-1][0]
nombre_effacement_consecutif = 0
periode_rallumage = 0
liste_temperatures_ext = liste_temperature_exterieure(origine_de_la_simulation, fin_de_la_simulation)
liste_temperatures_sans_effacement = liste_temperature_interieure(origine_de_la_simulation, fin_de_la_simulation)
liste_temperatures_avec_effacement = copy.deepcopy(liste_temperatures_sans_effacement)
liste_dates_simulation = liste_dates(origine_de_la_simulation, fin_de_la_simulation)        
liste_matrices = []
liste_machines = [chauffage, lumiere, bouilleur, splash_battle, creperie, PC_Normal ]
liste_consos = [conso_chauffage, conso_lumiere, conso_bouilleur, conso_splash_battle, conso_creperie, conso_PC_Normal]
liste_puissances = copy.deepcopy(liste_consos)

#####################################################################################################

def main( origine_de_la_simulation, fin_de_la_simulation, liste_ordres ):
    
    #compléter les listes températures réelles et simulées, y compris en dehors de la période d'effacement
    #et actualiser la gene de chaque machine avant d'appliquer l'algo d'effacement
    taille = len(liste_dates_simulation)
    j=0    
    while j < taille :
        date = liste_dates_simulation[j]
        booleen = liste_ordres[j//6][1] > 0
        if booleen :
              
########  la gene depend de la date, il faut donc la reactualiser  ###################################                 
                                  
            for i in range(len(liste_machines)) :
                etat_ref = liste_consos[i][j]/liste_machines[i].renvoyerConsoMax()
                nouvelle_gene = calcul_gene(liste_machines[i], date, liste_temperatures_avec_effacement[j], etat_ref)
                liste_machines[i].modifierGene(nouvelle_gene)

###############################   APPEL D'EFFACEMENT_MAIN   ###########################################                 

            effacement_main( date, origine_de_la_simulation, liste_ordres[j//6][1], liste_temperatures_avec_effacement, liste_temperatures_ext, liste_matrices, liste_machines, liste_puissances, liste_consos, nombre_effacement_consecutif )
            nombre_effacement_consecutif += 1
            j+=6  # on est en effacement. main passe la main a effacement_main pour une heure. On incrémente donc l'indice de six pas de dix minutes.
            
        else :
        	# en periode normale, il faut actualiser l'etat et la gene de la machine a chaque instant, car ils dependent de la date
        	# NB :  pas besoin d'actualiser la liste des puissances quand on n'est pas en effacement, car c'est une (deep) copie de liste_consos
            for k in range(len(liste_machines)):
                etat_ref = liste_consos[k][j]/liste_machines[k].renvoyerConsoMax()
                liste_machines[k].modifierEtatActuel(etat_ref)
                liste_machines[k].modifierGene(calcul_gene(liste_machines[k], date, liste_temperatures_avec_effacement[k], etat_ref))
            #lorsqu'on coupe le chauffage depuis trop longtemps, il faut le rallumer pendant une heure (ie six pas de dix minutes)
			if (nombre_effacement_consecutif % 3 == 0 and nombre_effacement_consecutif != 0):
			    periode_rallumage = 6
                nombre_effacement_consecutif = 0            
                
            if(periode_rallumage > 0) :
                liste_temperatures_avec_effacement[j] = rallumer_chauffage(date, liste_temperatures_avec_effacement)                
                periode_rallumage -= 1
            j += 1  #on est en période normale : la boucle doit faire des pas de minutes.
            
    #on retourne les listes globales 

    #return (liste_dates_simulation, liste_temperatures_avec_effacement, liste_matrices, liste_puissances, liste_consos)

###########################  ECRITURE DES RESULTATS DANS UN FICHIER   #################################                 

donnees_to_bytes(liste_dates_simulation,liste_temperatures_avec_effacement,liste_ordres,liste_matrices,liste_puissances,liste_consos)