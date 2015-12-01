import sys
sys.path.append("C:/Users/Rudy-/Desktop/MIG SE/Fonction effacement")
import Machine_verif
import datetime_to_temperature_verif

def actualise_etat_et_gene(instance_machine, date):
    if instance_machine.renvoyerEtatContinu():
        instance_machine.modifierEtatActuel( - 0.01 )
        instance_machine.modifierGene(instance_machine.renvoyerGene() + get_delta_gene(instance_machine, date))
    else:
        instance_machine.modifierEtatActuel( 0 )
        instance_machine.modifierGene(instance_machine.renvoyerGene() + get_delta_gene(instance_machine, date))
        
    
    
def get_delta_gene(instance_machine, date, Tint):
    if (instance_machine.renvoyerNom() == "chauffage" or instance_machine.renvoyerNom() == "clim") :
        Pq_actuelle = instance_machine.consoMachine()
        Text = datetime_to_temperature(date) #température extérieure, implémenter le fichier
        temp_apres = calcul_temp(Tint, Text, Pq_actuelle) #Tint à implémenter
        gene_apres = calcul_gene(temp_apres) 
        delta_gene = gene_apres - instance_machine.renvoyerGene() 
        return( delta_gene )  
    else:
        instance_machine.modifierEtatActuel(instance_machine.renvoyerEtatActuel() - 0.01)
        gene_apres = calcul_gene(instance_machine, Tint, date) 
        instance_machine.modifierEtatActuel(instance_machine.renvoyerEtatActuel() + 0.01)
        delta_gene = gene_apres - instance_machine.renvoyerGene() 
        return( delta_gene )  
    
        

def calcul_gene(instance_machine, date, Tint):   #calcul de la gene
    if instance_machine.renvoyerNom() == "chauffage" or instance_machine.renvoyerNom() == "clim" :	
        if 19 <= Tint <= 25:
            return((Tint-22)**4)/81 
        else:
            return(1)
    if instance_machine.renvoyerNom() == "lumiere" :
        if date.hour < 9 or date.hour > 19 :
            return 0.0
        elif (date.hour >=16 and date.hour <19) and (date.month >=10 or date.month <=3) :
            return ( 1-instance_machine.renvoyerEtatActuel() )*3
        else :
            return 1-instance_machine.renvoyerEtatActuel() 
    if instance_machine.renvoyerNom() == "PC normal":
        return (etatRef / instance_machine.renvoyerEtatActuel)**instance_machine.renvoyerImportance() -1 
    if instance_machine.renvoyerNom() == "bouilloire":
        if date.hour < 9 or date.hour > 19 :
            return 0.0
        else:
            return ( etatRef / instance_machine.renvoyerEtatActuel)**instance_machine.renvoyerImportance() -1 )
    if instance_machine.renvoyerNom() == "splash battle":
        if date.hour < 7 or date.hour > 21:
            return 0.0
        else:
            return ( etatRef / instance_machine.renvoyerEtatActuel)**instance_machine.renvoyerImportance() -1 )
    if instance_machine.renvoyerNom() == "creperie":
        if date.hour < 9 or date.hour > 19 :
            return 0.0
        else:
            return 1.0
        
    
        
def calcul_temp(p):
    return() #calcul de la température en fonction de la Puiss. Calorifique
    
    
    


    
    

        
            
        