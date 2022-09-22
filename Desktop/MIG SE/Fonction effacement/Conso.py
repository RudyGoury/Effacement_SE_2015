# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 00:35:51 2015

@author: Aymeric
"""
import pandas as pd
import datetime

def estDansLaSemaineTravail(date):
    return (date.weekday() <= 4)

def conso(nom_machine, date_debut, date_fin):
    nom_machine = str(nom_machine)
    data_brut = pd.HDFStore('data_brut.h5')
    df = data_brut[nom_machine]
    data_brut.close()
    df = df[(df["date et heure"] >= date_debut)]
    df = df[(df["date et heure"] <= date_fin)]
    liste_energies = df["Energie"]
    liste_puissances = [round(k*6000,2) for k in liste_energies]
    return (liste_puissances)

def liste_dates(date_debut,date_fin):
    list = [date_debut]
    while (list[-1]+datetime.timedelta(0,600,0)) <= date_fin:
        list.append(list[-1]+datetime.timedelta(0,600,0))
    return(list)
				
def liste_dates_avec_booleens(date_debut,date_fin):
    list=[(date_debut,False)]
    while (list[-1][0]+datetime.timedelta(0,600,0)) <= date_fin:
        list.append((list[-1][0]+datetime.timedelta(0,600,0), False))
    return(list)

def convert_to_datetime(date):
    jour = int(date[0:2])
    mois = int(date[3:5])
    annee = int(date[6:10])
    if len(date)<=10:
        return(datetime.datetime(annee,mois,jour))
    else:
        heure = int(date[11:13])
        minut = int(date[14:16])
        sec = 00
        return(datetime.datetime(annee,mois,jour,heure,minut,sec))
								
a=datetime.datetime(15, 1, 31, 0, 0)
b=datetime.datetime(15, 2, 2, 0, 0)

date1 = convert_to_datetime("06/12/2014 06:00")
date2 = convert_to_datetime("06/12/2014 08:00")
l1 = conso("General_Clim",date1,date2)
l2 = liste_dates_avec_booleens(a,b)
#print(l1)
print(l2)

def renvoyerIndiceJournee(d) :
    return d.hour*6+d.minute//10