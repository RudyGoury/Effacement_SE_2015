import Machine

def actualise_etat_et_gene(instance_machine, date):
    instance_machine.modifierEtatActuel( - 0.01 )
    instance_machine.modifierGene(instance_machine.renvoyerGene() + get_delta_gene(instance_machine, date))
    
    
def get_delta_gene(instance_machine, date):
    if (instance_machine.renvoyerNom() == "chauffage" or instance_machine.renvoyerNom() == "clim") :
        Pq_actuelle = instance_machine.consoMachine()
        Pq_après = Pq_actuelle - 0.01*instance_machine.renvoyerConsoMax()
        Text = datetime_to_temperature(date) #température extérieure, implémenter le fichier
        temp_apres = calcul_temp(Tint, Text, Pq_actuelle) #Tint à implémenter
        gene_apres = calcul_gene(temp_apres)
        delta_gene = gene_apres - instance_machine.renvoyerGene() 
        return( delta_gene )        

def calcul_gene(instance_machine, Tint, date):   #calcul de la gene
    if instance_machine.renvoyerNom() == "chauffage" or instance_machine.renvoyerNom() == "clim" :			
        if 19 <= Tint <= 25:
            return((Tint-22)**4)/81 
        else:
            return(1)
    if instance_machine.renvoyerNom() == "lumiere" :
        if date.hour < 9 or date.hour > 19 :
            return 0.0
            
        elif (date.hour >=16 and date.hour <19) and (date.month >=10 or date.month <=3) :
            return 0.8
        else :
            return 0.2 
    
        
def calcul_temp(p):
    return() #calcul de la température en fonction de la Puiss. Calorifique
    
    
    


    
    

        
            
        