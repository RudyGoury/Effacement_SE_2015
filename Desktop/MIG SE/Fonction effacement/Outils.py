

import pandas
import datetime
from datetime import date
import time
from numpy import arange

SEMAINE = datetime.timedelta(days = 7)
JOUR = datetime.timedelta(days = 1)
HEURE =datetime.timedelta(hours = 1)
MINUTES = datetime.timedelta(minutes = 1)
def estDansLaSemaineTravail(dateStr, dateRef) :
    try :
        date = datetime.datetime.strptime(dateStr,'%d/%m/%Y %H:%M')
    except :
        return False 
    if(date.weekday() == 5 or date.weekday() == 6):
        return False
    if (date == None):
        return False
    return dateRef - SEMAINE <= date and date < dateRef


def puissanceReferenceMachine(nomFichier, date) :
    print(nomFichier)
    try : 
        df = pandas.read_csv(nomFichier, sep = ';', names = ["Dates","Batiment","Machine","???","Valeurs","Unites"])
    except : 
        print("ERROR OPEN FILE")
        return;
    
    listeBooleen = []
    n = len(df)
    for i in arange(0,n,1) :
        listeBooleen.append(((estDansLaSemaineTravail(df['Dates'][i], date)) & (df['???'][i]>='Puissance Active')))
        
    #print(listeBooleen)
    
    df = df[listeBooleen]
    df['index']=range(0,len(df))
    df=df.set_index('index')
    return df
    #and (datetime.datetime.strptime(df['Dates'],'%d/%m/%y %H:%M') <= date) and (datetime.datetime.strptime(df['Dates'],'%d/%m/%y %H:%M') > date - SEMAINE) 
    
def estALHeure(dateStr, heures, minutes) :
    try :
        date = datetime.datetime.strptime(dateStr,'%d/%m/%Y %H:%M')
    except :
        print("LOOL")
        return False
    return date.hour == heures and date.minute == minutes
    
    
    
def faireMoyenne(dataFrame, heures, minutes):
    #print(dataFrame)
    taille = len(dataFrame)
    compteur = 0
    somme = 0
    for i in arange(0, taille, 1) :
        if(estALHeure(dataFrame['Dates'][i], heures, minutes)) :
            tmp = float(dataFrame['Valeurs'][i].replace(',','.'))
            s = dataFrame['???'][i]
            if(tmp > 0) :
                compteur += 1
                somme += tmp
                if(s == "Puissance Active L2" or s == "Puissance Active L3") :
                    compteur -= 1;
            
    if(compteur == 0):
        return 0
    return somme/compteur
    
    
#Retourne liste de consomation au temps t 
#pendant la journéee calcule a partir le la consommation moyenne (en excluant le week end) de ma semaine passe.
#!!! res[0] = maximum de la liste
def faireMoyenneJour(dataFrame) :
    res = []    
    max = 0
    for i in arange(0,144,1) :# 144 = nombre de 10minutes par jours
        tmp = faireMoyenne(dataFrame, i//6,i%6 * 10)
        if(tmp > max) :
            max = tmp
        res.append(tmp)
    res.insert(0, max)
    return res
    
def renvoyerIndiceJournee(d) :
    return d.hour*6+d.minute//10
